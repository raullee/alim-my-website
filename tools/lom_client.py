# -*- coding: utf-8 -*-
"""
Client for the AGC "Laws of Malaysia" portal (lom.agc.gov.my).

The portal renders nothing server-side. Every list and search result comes from
POST /fess-proxy.php, which answers with AES-256-GCM ciphertext whose key is
printed in the page's own inline JS as SEARCH_RESPONSE_KEY.

Payload layout (see /js/responseCrypto.js):   iv[12] || tag[16] || ciphertext
"""
import base64
import http.cookiejar
import json
import re
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE = "https://lom.agc.gov.my/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# Categories used by the portal's own menus.
KAT_PRINCIPAL = "iagcact,iagcact_repealed,iagcact_revised,iagcact_translated,iagcact_updated"
KAT_PUA = "iagcpuab_pua"

_cj = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))
_opener.addheaders = [("User-Agent", UA), ("Referer", BASE + "search.php")]

_key_cache = None


def response_key():
    """Read SEARCH_RESPONSE_KEY off a live page rather than hardcoding it.

    AGC will rotate this eventually; a stale key fails as a bare auth-tag error,
    which is impossible to diagnose from the outside.
    """
    global _key_cache
    if _key_cache:
        return _key_cache
    for page in ("principal.php", "subsid.php?type=pua", "search-legislation.php"):
        try:
            with _opener.open(BASE + page, timeout=60) as r:
                html = r.read().decode("utf-8", "replace")
        except Exception:
            continue
        m = re.search(r"SEARCH_RESPONSE_KEY\s*=\s*['\"]([0-9a-fA-F]{64})['\"]", html)
        if m:
            _key_cache = bytes.fromhex(m.group(1))
            return _key_cache
    raise RuntimeError("SEARCH_RESPONSE_KEY not found; the portal changed.")


def _decrypt(raw):
    payload = json.loads(raw)
    if not payload.get("encrypted"):
        return payload
    blob = base64.b64decode(payload["data"])
    iv, tag, ct = blob[:12], blob[12:28], blob[28:]
    return json.loads(AESGCM(response_key()).decrypt(iv, ct + tag, None))


def fess(q, start=0, rows=100, kategori="all", sort="", tries=4):
    body = urllib.parse.urlencode({
        "q": q, "fq": "", "start": start, "rows": rows,
        "sort": sort, "lookup": "all", "kategori": kategori, "draw": 1,
    }).encode()
    req = urllib.request.Request(BASE + "fess-proxy.php", body)
    req.add_header("X-Requested-With", "XMLHttpRequest")
    for attempt in range(tries):
        try:
            with _opener.open(req, timeout=120) as r:
                return _decrypt(r.read())
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(2 + 4 * attempt)


def catalogue(kategori=KAT_PRINCIPAL, q="*", page=100, pause=0.4):
    """Page through an entire category."""
    out, start = [], 0
    while True:
        d = fess(q, start, page, kategori)
        docs = d["response"]["docs"]
        total = d["response"]["numFound"]
        out += docs
        start += page
        if start >= total or not docs:
            return out, total
        time.sleep(pause)


# --------------------------------------------------------------------------
# record -> PDF paths
# --------------------------------------------------------------------------
_DUP = re.compile(r"^(upload/portal/akta/outputaktap/)+")


def _from_token(html):
    m = re.search(r"token=([A-Za-z0-9+/=_%-]+)", html or "")
    if not m:
        return None
    tok = urllib.parse.unquote(m.group(1))
    tok += "=" * (-len(tok) % 4)
    try:
        url = base64.b64decode(tok).decode("utf-8", "replace").split("|")[0]
    except Exception:
        return None
    return url.split("/ilims/", 1)[-1] if url.endswith(".pdf") else None


def pdf_paths(rec):
    """Return {'BI': path, 'BM': path} for one catalogue record."""
    out = {}
    for lang, field in (("BI", "docNameBI"), ("BM", "docNameBM")):
        if rec.get(field):
            out[lang] = rec[field]

    # The "As At" (consolidated) records carry their paths here instead, with
    # the outputaktap/ prefix doubled. Un-double it or every fetch 404s.
    raw = rec.get("DOC2DOWNLOAD_GENERATEPDF") or ""
    if raw:
        try:
            for item in json.loads(raw):
                path = _DUP.sub("upload/portal/akta/outputaktap/",
                                (item["path"] + item["docName"]).lstrip("/"))
                lang = "BM" if "_BM/" in item["path"] else "BI"
                out.setdefault(lang, path)
        except Exception:
            pass

    for lang, field in (("BI", "DOC2DOWNLOADBI"), ("BM", "DOC2DOWNLOADBM"),
                        ("BI", "DOC2DOWNLOAD")):
        if lang not in out:
            p = _from_token(rec.get(field))
            if p:
                out[lang] = p
    return out


def pdf_url(path):
    return BASE + "ilims/" + urllib.parse.quote(path)


def act_detail_url(act_no, lang="BI"):
    return f"{BASE}act-detail.php?act={act_no}&lang={lang}"


_ASAT = re.compile(r"\s+As At (\d{2})-(\d{2})-(\d{4})\s*$", re.I)
_SEBAGAIMANA = re.compile(r"\s+Sebagaimana Pada .*$", re.I)


def split_records(records):
    """Separate a single act's records into (original, newest consolidated)."""
    originals, updated = [], []
    for r in records:
        if _ASAT.search(r.get("titleBI") or "") or _SEBAGAIMANA.search(r.get("titleBM") or ""):
            updated.append(r)
        else:
            originals.append(r)

    def sort_key(r):
        m = _ASAT.search(r.get("titleBI") or "")
        return (m.group(3), m.group(2), m.group(1)) if m else ("0000", "00", "00")

    updated.sort(key=sort_key)
    return (originals[0] if originals else None,
            updated[-1] if updated else None)


def as_at(rec):
    m = _ASAT.search((rec or {}).get("titleBI") or "")
    return "-".join(m.groups()[::-1]) if m else ""   # YYYY-MM-DD


def clean_title(t):
    t = _SEBAGAIMANA.sub("", _ASAT.sub("", t or ""))
    return re.sub(r"\s+", " ", t).strip()


_LOWER = {"and", "or", "of", "for", "the", "to", "in", "on", "by", "a", "an", "at", "as"}
_KEEP = {"FINAS", "PLT", "EPF", "SOCSO", "ASWARA", "P.U.", "II", "III", "IV", "VI"}


def title_case(t):
    """AGC titles arrive shouted. Title-case them without mangling the odd bits."""
    words = re.sub(r"\s+", " ", (t or "")).strip().split(" ")
    out = []
    for i, w in enumerate(words):
        if w.upper() in _KEEP or re.fullmatch(r"[\d/().,'-]+", w):
            out.append(w.upper() if w.upper() in _KEEP else w)
        elif w.lower() in _LOWER and i not in (0, len(words) - 1):
            out.append(w.lower())
        else:
            # keep bracketed/hyphenated parts capitalised piecewise
            out.append(re.sub(r"[A-Za-z]+", lambda m: m.group(0).capitalize(), w.lower()))
    return " ".join(out)


def download(url, dest, referer=BASE + "search.php", tries=3, min_bytes=8000):
    """Fetch a PDF and refuse anything that is not really one."""
    req = urllib.request.Request(url)
    req.add_header("Referer", referer)
    last = None
    for attempt in range(tries):
        try:
            with _opener.open(req, timeout=300) as r:
                ctype = r.headers.get("Content-Type", "")
                data = r.read()
            if "pdf" not in ctype.lower() or not data.startswith(b"%PDF"):
                raise ValueError(f"not a PDF (content-type {ctype!r}, {len(data)} bytes)")
            if len(data) < min_bytes:
                raise ValueError(f"suspiciously small ({len(data)} bytes)")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return len(data)
        except Exception as e:
            last = e
            time.sleep(2 + 4 * attempt)
    raise last
