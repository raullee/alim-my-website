# -*- coding: utf-8 -*-
"""
Harvest the ALIM legislation library from the AGC portal.

  python3 tools/harvest.py            # full run
  python3 tools/harvest.py --no-pdf   # metadata + section headings only
  python3 tools/harvest.py --refresh  # re-check As At dates, report drift, don't refetch

Writes legislation/data/library.json, which tools/build.py turns into pages.
Every act number, title and As At date in the output came from the live portal on
the run date. Nothing here is recalled.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import lom_client as lom
from registry import REGISTRY, SUBSIDIARY, OBJECTIVES, SEGMENTS

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "legislation" / "data"
PDFDIR = ROOT / "legislation" / "pdf"
CACHE = DATA / "_catalogue.json"

# Mirror the AGC PDFs, or link out to them?  Malaysian government works are in
# copyright and LOM carries an AGC notice, so this is a judgement call, not a
# technical one.  Flip to False and the build links to lom.agc.gov.my instead;
# nothing else changes.
HOST_PDFS = True

HEADING_MIN, HEADING_MAX = 4, 90


# ---------------------------------------------------------------------------
# section headings, read out of the PDF rather than recalled
# ---------------------------------------------------------------------------
_NUM_ONLY = re.compile(r"^\s*(\d{1,3}[A-Za-z]{0,2})\.\s*$")
_NUM_HEAD = re.compile(r"^\s*(\d{1,3}[A-Za-z]{0,2})\.\s+(\S.*)$")
_STRUCT = re.compile(r"^\s*(PART|BAHAGIAN|CHAPTER|BAB|SCHEDULE|JADUAL|DIVISION|SUBDIVISION)\b",
                     re.I)
_STOP = re.compile(r"^\s*(An Act (to|for)\b|ENACTED BY|BE IT ENACTED|Suatu Akta untuk)", re.I)
_NOISE = re.compile(r"^[\s.…·_\d/\-]*$")
# Page furniture that repeats down the arrangement and would otherwise be
# swallowed into a heading or mistaken for the end of it.
_FURNITURE = re.compile(
    r"^\s*(LAWS OF MALAYSIA|UNDANG-UNDANG MALAYSIA|ARRANGEMENT OF SECTIONS|"
    r"SUSUNAN SEKSYEN|Sect?ion|Seksyen|Akta \d+|Act \d+[A-Z]?|"
    r"\d{2}/\d{2}/\d{4}.*|.*\.indd\s.*|\d{1,2}:\d{2}\s*(AM|PM))\s*$", re.I)


def extract_sections(pdf_path, scan_pages=60):
    """Pull (number, heading) pairs from an Act's Arrangement of Sections.

    The consolidated AGC PDFs are born-digital, so the arrangement is real text.
    AGC sets it two ways: "13.<tab>Nature of copyright" on one line, or the
    number on its own line with the heading (often wrapped) beneath. Handle both.
    Returns [] for a scanned PDF, which is the honest answer.
    """
    try:
        import fitz
    except ImportError:
        return [], 0, False
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return [], 0, False

    pages = doc.page_count
    chunks = [doc.load_page(i).get_text() for i in range(min(pages, scan_pages))]
    doc.close()

    text = "\n".join(chunks)
    if sum(len(c) for c in chunks[:30]) < 500:
        return [], pages, False

    start = text.upper().find("ARRANGEMENT OF SECTIONS")
    if start < 0:
        start = text.upper().find("SUSUNAN SEKSYEN")
    body = text[start:] if start >= 0 else text

    # A running head repeats on every page of the arrangement; anything short
    # that appears four or more times is furniture, whatever it says.
    from collections import Counter
    freq = Counter(l.strip() for l in body.split("\n") if 0 < len(l.strip()) <= 60)
    repeated = {k for k, v in freq.items() if v >= 4 and not _NUM_ONLY.match(k)}

    out, seen, cur, buf = [], set(), None, []

    def flush():
        if cur is None:
            return
        head = re.sub(r"\s+", " ", " ".join(buf)).strip(" .…·\t")
        head = re.sub(r"[\s.…]*\d{1,4}$", "", head).strip()
        # Page furniture that wrapped onto a heading line: running heads, the
        # printer's job number, the reprint date stamp.
        head = re.sub(r"\s*\d*\s*(Laws of Malaysia|Undang-undang Malaysia)\b.*$", "",
                      head, flags=re.I)
        head = re.sub(r"\s*(WJW|MJW)\S*.*$", "", head)
        head = re.sub(r"\s*\d{1,2}/\d{2}/\d{4}.*$", "", head)
        # A run of shouted words is the next Part/title bleeding in; cut it off.
        head = re.split(r"\s+(?=[A-Z]{2,}(?:\s+[A-Z]{2,})+)", head)[0]
        head = re.sub(r"\s*\((Omitted|Deleted)\)\.\s+(?=[A-Z])", ". ", head).strip(" .")
        key = cur.upper()
        if (HEADING_MIN <= len(head) <= 160 and key not in seen
                and not _NOISE.match(head)):
            seen.add(key)
            out.append({"s": key, "t": head})

    for raw in body.split("\n"):
        line = raw.replace("\t", " ").rstrip()
        if not line.strip():
            continue
        # Number matchers run before the noise filter: a bare "2." is a section
        # number, not noise, and it looks identical to a stray page number.
        m = _NUM_ONLY.match(line)
        if m:
            flush()
            cur, buf = m.group(1), []
            continue
        m = _NUM_HEAD.match(line)
        if m:
            flush()
            cur, buf = m.group(1), [m.group(2)]
            continue
        if _NOISE.match(line) or _FURNITURE.match(line) or line.strip() in repeated:
            continue
        if _STOP.match(line) and out:
            break
        if _STRUCT.match(line):
            flush()
            cur, buf = None, []
            continue
        if cur is not None and len(buf) < 4:
            buf.append(line.strip())
    flush()
    return out, pages, True


_BM_WORDS = re.compile(r"\b(yang|dan|bagi|kepada|seksyen|akta|undang|hendaklah|dalam|"
                       r"tafsiran|tajuk ringkas|susunan|bahagian|peraturan)\b", re.I)
_BI_WORDS = re.compile(r"\b(the|and|of|shall|section|act|interpretation|short title|"
                       r"arrangement|part|regulations|any|this)\b", re.I)


def path_lang(path):
    """AGC's own directory tree leaks the language even when the field lies.

    Act 336's consolidated record is filed as BI but points at
    upload/portal/akta/LOM/MY/Akta 336 (Disemak 1987).pdf, which is the Malay
    reprint and is a scan, so text detection cannot save us. The path can.
    """
    p = (path or "").replace("\\", "/")
    if "/LOM/MY/" in p or "_BM/" in p or "/Akta " in p:
        return "BM"
    if "_BI/" in p or "/Act " in p:
        return "BI"
    return None


def detect_lang(pdf_path):
    """AGC mislabels some files (Act 254's 'BI' slot holds the Malay text).

    Trust the words on the page, not the field name.
    """
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = "\n".join(doc.load_page(i).get_text()
                         for i in range(min(doc.page_count, 8)))
        doc.close()
    except Exception:
        return None
    if len(text) < 300:
        return None          # scanned: no basis to judge
    bm, bi = len(_BM_WORDS.findall(text)), len(_BI_WORDS.findall(text))
    if bm > bi * 1.2:
        return "BM"
    if bi > bm * 1.2:
        return "BI"
    return None


def _norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def match_keys(wanted, sections):
    """Attach the real section number to each curated key heading.

    Exact match only, and only when the heading is unique in the Act. Fuzzy
    matching was tried and produced confident wrong answers: "Nature of
    copyright" happily matched s.15 "Nature of copyright in broadcasts" when
    the provision meant was s.13. A wrong section number is worse than none,
    so anything that is not an exact, unambiguous hit is marked unverified and
    renders as a topic label with no number.
    """
    index = {}
    for x in sections:
        index.setdefault(_norm(x["t"]), []).append(x)
    out = []
    for w in wanted:
        cands = index.get(_norm(w), [])
        hit = cands[0] if len(cands) == 1 else None
        out.append({"label": w, "s": hit["s"] if hit else None,
                    "t": hit["t"] if hit else w, "verified": bool(hit)})
    return out


# ---------------------------------------------------------------------------
def load_catalogue(refresh=False):
    DATA.mkdir(parents=True, exist_ok=True)
    if CACHE.exists() and not refresh:
        return json.loads(CACHE.read_text("utf-8"))
    print("  fetching principal act catalogue ...", flush=True)
    acts, total = lom.catalogue(lom.KAT_PRINCIPAL)
    print(f"    {len(acts)}/{total} principal act records", flush=True)
    print("  fetching subsidiary legislation ...", flush=True)
    subs = []
    for q in ("Copyright", "Film Censorship", "Gig Workers", "Personal Data",
              "Communications and Multimedia", "Employment"):
        d = lom.fess(q, 0, 60, lom.KAT_PUA)
        subs += d["response"]["docs"]
        time.sleep(0.3)
    cat = {"fetched": dt.date.today().isoformat(), "acts": acts, "pua": subs}
    CACHE.write_text(json.dumps(cat, ensure_ascii=False), "utf-8")
    return cat


def find_pua(cat, pu_no):
    want = re.sub(r"\s+", "", pu_no).upper()
    for r in cat["pua"]:
        if re.sub(r"\s+", "", r.get("noPU") or "").upper() == want:
            return r
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch the catalogue and report As At drift")
    args = ap.parse_args()

    print("ALIM legislation harvest", dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    cat = load_catalogue(refresh=args.refresh)

    by_act = {}
    for r in cat["acts"]:
        by_act.setdefault(str(r.get("actNo")), []).append(r)

    previous = {}
    out_path = DATA / "library.json"
    if out_path.exists():
        try:
            for e in json.loads(out_path.read_text("utf-8"))["entries"]:
                if e.get("act"):
                    previous[e["act"]] = e.get("as_at")
        except Exception:
            pass

    entries, drift, problems = [], [], []

    for spec in REGISTRY:
        kind = spec.get("kind", "federal_act")
        entry = {
            "kind": kind,
            "objectives": spec["obj"],
            "segments": spec["seg"],
            "tier": spec["tier"],
            "why": spec["why"],
            "watch": spec.get("watch"),
            "internal": spec.get("internal"),
            "issuer": spec.get("issuer"),
            "also": [],
        }

        if kind != "federal_act":
            entry.update({
                "id": spec["id"] if "id" in spec else spec["act"].lower(),
                "act": spec.get("act") if spec.get("act") != "FEDCON" else None,
                "short": spec["short"],
                "title_en": spec["title_en"],
                "title_bm": spec.get("title_bm"),
                "source": spec.get("url"),
                "sections": [{"label": k, "s": None, "t": k, "verified": False}
                             for k in spec.get("keys", [])],
                "pdf": {}, "pages": 0, "text_layer": False, "as_at": None,
            })
            entries.append(entry)
            print(f"  · {entry['short']}  ({kind})")
            continue

        act = spec["act"]
        recs = by_act.get(act, [])
        if not recs:
            problems.append(f"act {act}: not found in catalogue")
            continue
        original, updated = lom.split_records(recs)
        chosen = updated or original
        title_en = lom.clean_title(chosen.get("titleBI") or (original or {}).get("titleBI"))
        title_bm = lom.clean_title(chosen.get("titleBM") or (original or {}).get("titleBM"))
        stamp = lom.as_at(updated) if updated else None

        if act in previous and previous[act] and stamp and previous[act] != stamp:
            drift.append(f"Act {act} {title_en}: As At {previous[act]} -> {stamp}")

        entry.update({
            "id": f"act-{act}",
            "act": act,
            "short": spec.get("short") or lom.title_case(title_en),
            "title_en": title_en,
            "title_bm": title_bm,
            "as_at": stamp,
            "consolidated": bool(updated),
            "source": lom.act_detail_url(act),
        })

        paths = lom.pdf_paths(chosen)
        if not paths and original:
            paths = lom.pdf_paths(original)

        pdfs, pages, text_layer, sections = {}, 0, False, []
        staged = []
        for lang, path in sorted(paths.items()):
            if args.no_pdf:
                pdfs[lang] = {"remote": lom.pdf_url(path)}
                continue
            tmp = ROOT / f"legislation/pdf/.tmp-act-{act}-{lang.lower()}.pdf"
            final = ROOT / f"legislation/pdf/act-{act}-{lang.lower()}.pdf"
            try:
                if final.exists() and final.stat().st_size > 8000:
                    staged.append([lang, path, final, final.stat().st_size])
                else:
                    size = lom.download(lom.pdf_url(path), tmp)
                    time.sleep(0.3)
                    staged.append([lang, path, tmp, size])
            except Exception as e:
                problems.append(f"act {act} {lang}: {e}")
                pdfs[lang] = {"remote": lom.pdf_url(path), "error": str(e)[:120]}

        # AGC's BI/BM field names are not always right. Re-label from the text,
        # and only if that yields two distinct languages.
        # text first, then the path as a fallback for scans
        detected = [(s, detect_lang(s[2]) or path_lang(s[1])) for s in staged]
        langs = [d for _, d in detected if d]
        relabel = ((len(staged) == len(langs) == 2 and len(set(langs)) == 2)
                   or (len(staged) == 1 and len(langs) == 1))
        if relabel:
            for s, d in detected:
                if d != s[0]:
                    problems.append(f"act {act}: AGC labelled a {d} file as {s[0]}; relabelled")
                s[0] = d
        if original and chosen is not original and not any(s[0] == "BI" for s in staged):
            fallback = lom.pdf_paths(original)
            if fallback.get("BI") and path_lang(fallback["BI"]) != "BM":
                # distinct name: the relabelled file may still be staged under
                # .tmp-act-<n>-bi.pdf and would be renamed out from under us
                tmp = ROOT / f"legislation/pdf/.tmp-act-{act}-bi-orig.pdf"
                try:
                    size = lom.download(lom.pdf_url(fallback["BI"]), tmp)
                    staged.append(["BI", fallback["BI"], tmp, size])
                    problems.append(f"act {act}: consolidated text is Malay only; "
                                    f"took the English text from the original record")
                except Exception as e:
                    problems.append(f"act {act} BI fallback: {e}")

        for lang, path, src, size in staged:
            final = ROOT / f"legislation/pdf/act-{act}-{lang.lower()}.pdf"
            if src != final:
                src.replace(final)
            pdfs[lang] = {"local": f"/legislation/pdf/act-{act}-{lang.lower()}.pdf",
                          "remote": lom.pdf_url(path), "bytes": size}
        for leftover in (ROOT / "legislation/pdf").glob(f".tmp-act-{act}-*.pdf"):
            leftover.unlink()

        # Prefer the English arrangement; fall back to the Malay one where AGC
        # publishes no English text at all (Act 254 is the live example).
        primary = (pdfs.get("BI") or {}).get("local") or (pdfs.get("BM") or {}).get("local")
        if primary:
            sections, pages, text_layer = extract_sections(ROOT / primary.lstrip("/"))
            entry["arrangement_lang"] = "BI" if (pdfs.get("BI") or {}).get("local") else "BM"

        entry["pdf"] = pdfs
        entry["pages"] = pages
        entry["text_layer"] = text_layer
        entry["sections"] = match_keys(spec.get("keys", []), sections)
        entry["arrangement"] = sections[:1200]

        for pu in spec.get("also", []):
            if pu in SUBSIDIARY:
                rec = find_pua(cat, pu)
                item = {"no": pu, "title": SUBSIDIARY[pu]}
                if rec:
                    p = lom.pdf_paths(rec)
                    if p.get("BI"):
                        item["remote"] = lom.pdf_url(p["BI"])
                entry["also"].append(item)
            else:
                entry["also"].append({"no": pu, "title": pu})

        entries.append(entry)
        v = sum(1 for s in entry["sections"] if s["verified"])
        flag = "" if text_layer else "  [no text layer]"
        print(f"  · Act {act:<4} {entry['short'][:44]:<46} as at {stamp or '-':<10} "
              f"{pages:>4}pp  {v}/{len(entry['sections'])} sections{flag}")

    payload = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "source": "Laws of Malaysia, Attorney General's Chambers (lom.agc.gov.my)",
        "catalogue_fetched": cat["fetched"],
        "host_pdfs": HOST_PDFS and not args.no_pdf,
        "objectives": OBJECTIVES,
        "segments": SEGMENTS,
        "entries": entries,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), "utf-8")

    hosted = sum(1 for e in entries for p in e["pdf"].values() if p.get("local"))
    mb = sum(p.get("bytes", 0) for e in entries for p in e["pdf"].values()) / 1e6
    print(f"\n  {len(entries)} instruments, {hosted} PDFs hosted ({mb:.1f} MB)")
    if drift:
        print("\n  AS AT DRIFT since last run:")
        for d in drift:
            print("   !", d)
    if problems:
        print("\n  PROBLEMS:")
        for p in problems:
            print("   !", p)
    print(f"\n  wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
