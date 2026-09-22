# -*- coding: utf-8 -*-
"""
Generate the ALIM legislation library from legislation/data/library.json plus
the scenario layer in tools/scenarios.py.

  python3 tools/build.py

Produces
  legislation/index.html                  library: search, scenarios, framework matrix
  legislation/<instrument>/index.html     one page per instrument
  legislation/doing/<scenario>/index.html one page per real-world scenario
  legislation/data/search.json            instruments + scenarios, for the client search
  legislation/data/sections.json          every harvested section heading

Pages are built in the live alim.my "dossier" design system (assets/alim.css +
assets/alim.js, Literata / Archivo / JetBrains Mono), pillar 03 Education.
"""
import datetime as dt
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scenarios import SCENARIOS, ALIASES
from review_status import state_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "legislation" / "data"
OUT = ROOT / "legislation"

E = html.escape
TODAY = dt.date.today()

# The riso inks are the site's palette, but white text on them fails WCAG AA at
# badge size (green measured 2.56:1). These are the same hues darkened until
# white passes, and they are used only for the badges.
OBJ_INK = {"socio": "#00663A", "ip": "#005A90", "freedom": "#574281"}
KIND_LABEL = {
    "federal_act": "Federal Act", "constitution": "Constitution",
    "state_enactment": "State law", "industry_code": "Industry code",
    "guideline": "Guidelines", "treaty": "Treaty",
    "collecting": "Licensing bodies",
}
TIER_LABEL = {1: "Core", 2: "Situational", 3: "Background"}

TICKER = """<div id="ticker" class="tape" aria-hidden="true">
  <div class="tape-track">
    <span class="hot">In defence of makers, builders, dreamers</span><span>·</span>
    <span>A non-profit legal clinic</span><span>·</span>
    <span>Pro bono since 2025</span><span>·</span>
    <span class="hot">★ As featured in The Star</span><span>·</span>
    <span>Free &amp; confidential</span><span>·</span>
    <span>Art × Law Initiative Malaysia</span><span>·</span>
    <span class="hot">★ Know your rights</span><span>·</span>
    <span>@artxlawmas</span><span>·</span>
    <span class="hot">In defence of makers, builders, dreamers</span><span>·</span>
    <span>A non-profit legal clinic</span><span>·</span>
    <span>Pro bono since 2025</span><span>·</span>
    <span class="hot">★ As featured in The Star</span><span>·</span>
    <span>Free &amp; confidential</span><span>·</span>
    <span>Art × Law Initiative Malaysia</span><span>·</span>
    <span class="hot">★ Know your rights</span><span>·</span>
    <span>@artxlawmas</span><span>·</span>
  </div>
</div>"""

EXTRA_CSS = """
.lg-chip{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.1em;
  text-transform:uppercase; background:var(--paper); color:var(--ink-3);
  border:1.5px solid var(--rule); padding:6px 11px; cursor:pointer; white-space:nowrap;
  text-decoration:none; display:inline-block;
  transition:background .15s ease,color .15s ease,border-color .15s ease; }
.lg-chip:hover{ color:var(--ink); border-color:var(--ink-3); }
.lg-chip[aria-pressed="true"]{ background:var(--ink); color:var(--paper); border-color:var(--ink); }
.lg-chip.lg-alt{ border-style:dashed; }
.lg-chiprow{ display:flex; gap:8px; overflow-x:auto; padding-bottom:4px; align-items:center;
  flex-wrap:nowrap; }
.lg-chiprow>.label{ flex:0 0 auto; padding-right:4px; }
.lg-wrapchips{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.lg-search{ width:100%; font-family:'Archivo',sans-serif; font-size:16px; color:var(--ink);
  background:var(--paper-2); border:1.5px solid var(--ink); padding:15px 44px 15px 16px; }
.lg-search:focus{ outline:2px solid var(--pillar); outline-offset:2px; }
.lg-searchwrap{ position:relative; }
.lg-slash{ position:absolute; right:12px; top:50%; transform:translateY(-50%);
  font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--ink-3);
  border:1px solid var(--rule); padding:2px 7px; pointer-events:none; }
.lg-tools{ position:sticky; top:0; z-index:60; background:var(--paper);
  border-bottom:1px solid var(--rule); padding:18px 0 14px; margin-bottom:26px; }
.lg-ink{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.1em;
  text-transform:uppercase; padding:3px 8px; color:#FFFFFF; display:inline-block;
  font-weight:500; }
.lg-card{ display:block; text-decoration:none; }
.lg-card[hidden],[hidden]{ display:none !important; }
.lg-card h3{ font-size:19px; margin:10px 0 6px; line-height:1.25; }
.lg-card .lg-meta{ font-family:'JetBrains Mono',monospace; font-size:11px;
  color:var(--ink-3); letter-spacing:.04em; }
.lg-sec{ display:grid; grid-template-columns:5rem 1fr; gap:12px; padding:9px 0;
  border-bottom:1px solid var(--rule-soft); font-size:14.5px; align-items:baseline; }
.lg-sec:last-child{ border-bottom:0; }
.lg-num{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--pillar);
  letter-spacing:.04em; }
.lg-num.lg-topic{ color:var(--ink-3); }
.lg-arr{ max-height:460px; overflow-y:auto; padding-right:10px; margin-top:14px; }
.lg-hit{ display:block; text-decoration:none; background:var(--paper-2);
  border:1px solid var(--rule-soft); padding:11px 14px; }
.lg-hit:hover{ border-color:var(--ink-3); }
mark{ background:rgba(216,49,31,.22); color:inherit; padding:0 2px; }
details.lg-fold>summary{ cursor:pointer; list-style:none; display:flex;
  justify-content:space-between; align-items:center; gap:12px; }
details.lg-fold>summary::-webkit-details-marker{ display:none; }
.lg-warn{ border-left:4px solid var(--pillar); background:var(--paper-2);
  padding:14px 18px; font-size:14px; line-height:1.6; color:var(--ink-2); }
.lg-warn.lg-old{ border-left-color:var(--vermillion); }
.lg-prov{ display:flex; gap:12px; align-items:flex-start; border:1px solid var(--rule);
  background:var(--paper-2); padding:14px 18px; margin-top:22px; }
.lg-prov .lg-provtag{ font-family:'JetBrains Mono',monospace; font-size:10px;
  letter-spacing:.12em; text-transform:uppercase; padding:3px 8px; white-space:nowrap;
  border:1.5px solid var(--ink-3); color:var(--ink-3); }
.lg-prov[data-tone="good"] .lg-provtag{ border-color:var(--riso-green); color:var(--riso-green); }
.lg-prov[data-tone="warn"] .lg-provtag{ border-color:var(--vermillion); color:var(--vermillion); }
.lg-prov p{ margin:0; font-size:13px; line-height:1.6; color:var(--ink-2); }
/* the review bar: two buttons, and nothing else to think about */
.lg-rev{ position:sticky; top:0; z-index:70; background:var(--ink); color:var(--paper);
  padding:12px 0; margin-bottom:0; }
.lg-rev .wrap{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.lg-rev-who{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.1em;
  text-transform:uppercase; opacity:.75; flex:1 1 auto; }
.lg-rev-btn{ font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:.1em;
  text-transform:uppercase; padding:11px 18px; min-height:44px; cursor:pointer;
  border:1.5px solid var(--paper); background:transparent; color:var(--paper); }
.lg-rev-btn.lg-yes{ background:var(--paper); color:var(--ink); font-weight:500; }
.lg-rev-btn:disabled{ opacity:.45; cursor:default; }
.lg-rev textarea{ width:100%; margin-top:10px; padding:12px; font-family:'Archivo',sans-serif;
  font-size:15px; border:1.5px solid var(--paper); background:var(--ink); color:var(--paper); }
.lg-rev a{ color:var(--paper); }
.lg-revdone{ font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:.08em; }
.lg-rev-ask{ flex:1 1 100%; font-size:14px; line-height:1.55; margin:0 0 4px; }
.lg-rev-ask small{ display:block; opacity:.7; font-size:12.5px; margin-top:4px; }
.lg-rev-change{ background:none; border:0; color:var(--paper); opacity:.7;
  text-decoration:underline; cursor:pointer; font-family:'JetBrains Mono',monospace;
  font-size:11px; letter-spacing:.06em; padding:6px 0; }
@media(max-width:600px){ .lg-rev .wrap{ gap:8px } .lg-rev-btn{ flex:1 1 40%; text-align:center } }
.lg-notice p{ font-size:13.5px; line-height:1.7; color:var(--ink-2); margin:12px 0 0; }
.lg-notice p.lg-notice-cta{ color:var(--ink); font-size:14.5px; margin-top:16px; }

/* answer chain: a numbered docket, which is what this site already is */
.lg-step{ display:grid; grid-template-columns:2.6rem 1fr; gap:16px; padding:18px 0;
  border-top:1px solid var(--rule-soft); }
.lg-step:first-of-type{ border-top:0; }
.lg-step-n{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--pillar);
  padding-top:3px; letter-spacing:.06em; }
.lg-step h4{ font-family:'Literata',Georgia,serif; font-size:18px; font-weight:normal;
  margin:0 0 3px; line-height:1.3; }
.lg-step h4 a{ text-decoration:none; border-bottom:1px solid var(--rule); }
.lg-step h4 a:hover{ border-bottom-color:var(--pillar); }
.lg-step .lg-ref{ font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--ink-3);
  letter-spacing:.06em; }
.lg-step p{ font-size:14.5px; line-height:1.65; color:var(--ink-2); margin:8px 0 0; }
.lg-roleb{ font-family:'JetBrains Mono',monospace; font-size:9.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-3); border:1px solid var(--rule);
  padding:1px 6px; margin-right:5px; display:inline-block; }
.lg-step[data-dim="1"]{ opacity:.62; }
.lg-step[data-dim="1"] .lg-roleb{ opacity:.8; }

/* framework matrix */
.lg-matrix{ width:100%; border-collapse:collapse; font-size:13px; }
.lg-matrix th,.lg-matrix td{ border:1px solid var(--rule); padding:0; text-align:center; }
.lg-matrix thead th{ background:var(--paper-2); font-family:'JetBrains Mono',monospace;
  font-size:10px; letter-spacing:.1em; text-transform:uppercase; font-weight:500;
  color:var(--ink-3); padding:10px 8px; vertical-align:bottom; line-height:1.3;
  min-width:78px; }
.lg-matrix tbody th{ background:var(--paper-2); text-align:left; padding:12px 14px;
  font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:.1em;
  text-transform:uppercase; font-weight:500; white-space:nowrap; position:sticky; left:0;
  z-index:2; }
.lg-cell{ display:block; text-decoration:none; padding:16px 6px;
  font-family:'JetBrains Mono',monospace; font-size:15px; color:var(--ink);
  transition:background .15s ease; }
.lg-cell:hover{ background:var(--paper-3); }
.lg-cell[data-n="0"]{ color:var(--ink-3); opacity:.4; }
.lg-matrixscroll{ overflow-x:auto; border:1px solid var(--rule); }
.lg-tabs{ display:flex; gap:0; border-bottom:2px solid var(--ink); margin-bottom:26px;
  overflow-x:auto; }
.lg-tab{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.12em;
  text-transform:uppercase; padding:12px 18px; cursor:pointer; background:none;
  border:0; color:var(--ink-3); white-space:nowrap; }
.lg-tab[aria-selected="true"]{ background:var(--ink); color:var(--paper); }
@media(max-width:600px){ .lg-sec{ grid-template-columns:4rem 1fr; }
  .lg-step{ grid-template-columns:2rem 1fr; gap:10px; } }

@media print{
  #ticker,#nav,#foot,#dot,.lg-tools,.lg-tabs,.lg-chip,.skip-link{ display:none !important; }
  body::after{ display:none; }
  .lg-step{ break-inside:avoid; }
  a{ text-decoration:none; color:#000; }
  .page-emblem{ display:none; }
}
"""


def navbar(depth):
    up = "../" * depth
    return f"""<header id="nav">
  <div class="wrap row">
    <a class="wordmark" href="{up}index.html" aria-label="ALIM home">
      <span class="alim">Alim</span><span class="my">·my</span>
      <span class="sub">Art × Law Initiative Malaysia</span>
    </a>
    <nav class="links" aria-label="Primary">
      <a href="{up}get-help/">Get Help</a>
      <a href="{up}our-work/">Our Work</a>
      <a href="{up}resources/" aria-current="page">Resources</a>
      <a href="{up}join-us/">Join the Movement</a>
      <a href="{up}about-alim/">About Us</a>
    </nav>
    <div style="display:flex;align-items:center;gap:12px">
      <button id="theme-toggle" aria-label="Toggle night charter" aria-pressed="false">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.3 11.3 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4m11.3-11.3 1.4-1.4"/></svg>
      </button>
      <a class="navcta" href="{up}get-help/">Get Legal Help <span aria-hidden="true">→</span></a>
      <button id="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="mobile-nav">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <nav id="mobile-nav" aria-label="Mobile">
    <a href="{up}get-help/">Get Help</a>
    <a href="{up}our-work/">Our Work</a>
    <a href="{up}resources/">Resources</a>
    <a href="{up}join-us/">Join the Movement</a>
    <a href="{up}about-alim/">About Us</a>
    <a href="{up}request-consultation/">Request a Consultation</a>
  </nav>
</header>"""


def head(title, desc, canonical, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,200..900;1,7..72,200..900&family=Archivo:ital,wght@0,100..900;1,100..900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/alim.css">
<style>{EXTRA_CSS}</style>
</head>
<body data-pillar="education">
<a class="skip-link" href="#main">Skip to content</a>
{TICKER}
{navbar(depth)}
<main id="main">"""


def tail(depth, generated, catalogue_date, extra_js=""):
    up = "../" * depth
    return f"""</main>
<footer id="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-mark">
        <span class="alim">Alim<span style="font-family:'JetBrains Mono',monospace;font-size:14px;font-style:normal">·my</span></span>
        <p>Championing the legal rights of artists and cultural workers across Malaysia through advice, advocacy, and education.</p>
        <p style="margin-top:12px;font-size:13px;line-height:1.55;color:var(--ink-3)">Legislation sourced from the Attorney General's Chambers, <a class="ulink" href="https://lom.agc.gov.my/" target="_blank" rel="noopener">lom.agc.gov.my</a>. Catalogue checked {E(catalogue_date)}; pages generated {E(generated)}. The authoritative text of any Malaysian law is the version published in the Federal Gazette.</p>
      </div>
      <div>
        <h4>Navigate</h4>
        <ul>
          <li><a href="{up}get-help/">Get Help</a></li>
          <li><a href="{up}our-work/">Our Work</a></li>
          <li><a href="{up}mission/">Our Charter</a></li>
          <li><a href="{up}resources/">Resources</a></li>
          <li><a href="{up}legislation/">Legislation Library</a></li>
        </ul>
      </div>
      <div>
        <h4>More</h4>
        <ul>
          <li><a href="{up}about-alim/">About Us</a></li>
          <li><a href="{up}faq/">FAQ</a></li>
          <li><a href="{up}privacy/">Privacy Policy</a></li>
          <li><a href="{up}terms-of-service/">Terms of Service</a></li>
          <li><a href="{up}sitemap/">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Follow us</h4>
        <ul>
          <li><a href="https://www.instagram.com/artxlawmas/" target="_blank" rel="noopener">Instagram @artxlawmas</a></li>
          <li><a href="https://www.threads.net/@artxlawmas" target="_blank" rel="noopener">Threads</a></li>
          <li><a href="https://linktr.ee/artxlawinitiative" target="_blank" rel="noopener">Linktree</a></li>
          <li><a href="mailto:artxlawinitiative@gmail.com">Contact us</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© <span data-year>{TODAY.year}</span> ALIM.my (Art × Law Initiative Malaysia). All rights reserved.</span>
      <span>Made with purpose in Malaysia.</span>
    </div>
  </div>
</footer>
<div id="dot" aria-hidden="true"></div>
<script src="{up}assets/alim.js"></script>
{extra_js}
</body></html>"""


def disclaimer(depth):
    """The standing notice at the foot of every page in the library."""
    up = "../" * depth
    return f"""<div class="card lg-notice" style="padding:28px">
<span class="bar">Important notice</span>
<p>This page is published by ALIM (Art &times; Law Initiative Malaysia) as general legal
information for Malaysia&rsquo;s creative communities. It is not legal advice. It does not take
your circumstances into account, and reading it does not create a solicitor-client relationship
with ALIM or with anyone associated with it.</p>
<p>The law changes. Each Act reproduced here is the Attorney General&rsquo;s Chambers&rsquo;
consolidated reprint and carries the date it was consolidated to; amendments made after that date
do not appear in the text, and the authoritative version of any Malaysian law is the one published
in the Federal Gazette. Subsidiary legislation, state enactments and local authority by-laws may
also apply to your situation and are largely outside this library.</p>
<p>Please do not act, or decide not to act, on the strength of this page alone. Take advice from an
advocate and solicitor on your own facts. To the extent permitted by law, ALIM and its contributors
accept no liability for any loss arising from reliance on this page.</p>
<p class="lg-notice-cta">If you have a live problem,
<a class="ulink" href="{up}get-help/">talk to us</a>. It is free and confidential.</p>
</div>"""


def obj_inks(objs, objmeta):
    return "".join(
        f'<span class="lg-ink" style="background:{OBJ_INK.get(o, "var(--ink-3)")}">'
        f'{E(objmeta[o]["label"])}</span>' for o in objs)


def staleness(entry):
    if entry["kind"] != "federal_act" or not entry.get("as_at"):
        return ""
    d = dt.date(*(int(x) for x in entry["as_at"].split("-")))
    age = (TODAY - d).days // 365
    pretty = d.strftime("%-d %B %Y")
    old = age >= 3
    note = (f"This copy of the Act is {age} years old. Any amendment made since {pretty} is "
            f"<strong>not</strong> in this text."
            if old else
            f"Consolidated to {pretty}. Amendments made after that date are not in this text.")
    cls = "lg-warn lg-old" if old else "lg-warn"
    return (f'<div class="{cls}" style="margin:22px 0">{note} Check the '
            f'<a class="ulink" href="{E(entry["source"])}" target="_blank" rel="noopener">AGC '
            f'record</a> for later amendments.</div>')


def ref_of(e):
    return f"Act {e['act']}" if e.get("act") else KIND_LABEL.get(e["kind"], "")


# ---------------------------------------------------------------------------
def act_page(entry, lib, scen_for, depth=2):
    objmeta, segmeta = lib["objectives"], lib["segments"]
    label = KIND_LABEL.get(entry["kind"], entry["kind"])

    pdfs = []
    for lang, name in (("BI", "English text"), ("BM", "Teks Bahasa Malaysia")):
        p = entry["pdf"].get(lang)
        if not p:
            continue
        href = ("../.." + p["local"]) if p.get("local") else p.get("remote")
        size = f"PDF · {p['bytes']/1e6:.1f} MB" if p.get("bytes") else "PDF"
        where = "hosted by ALIM" if p.get("local") else "opens at AGC"
        pdfs.append(f'<a class="card lg-card" href="{E(href)}" target="_blank" rel="noopener">'
                    f'<span class="idx">{E(size)} · {where}</span><h3>{name}</h3>'
                    f'<p>Open the full text &rarr;</p></a>')
    if not pdfs:
        pdfs.append(f'<a class="card lg-card" href="{E(entry["source"] or "https://lom.agc.gov.my/")}" '
                    f'target="_blank" rel="noopener"><span class="idx">External</span>'
                    f'<h3>Read the source</h3><p>Open it &rarr;</p></a>')

    keys = ""
    if entry["sections"]:
        rows = "".join(
            '<div class="lg-sec">' +
            (f'<span class="lg-num">s.{E(s["s"])}</span>' if s["verified"] else
             '<span class="lg-num lg-topic" title="Topic reference; the section number could not '
             'be confirmed from the AGC text">topic</span>') +
            f'<span>{E(s["t"])}</span></div>' for s in entry["sections"])
        keys = f"""<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">Start here</span><h2>What to read first</h2></div></div>
  <p class="label" style="margin:0 0 14px">Section numbers read out of the AGC text itself</p>
  <div class="card" style="padding:18px 24px">{rows}</div>
</div></section>"""

    arrangement = ""
    arr = entry.get("arrangement") or []
    if arr:
        lang_note = ("" if entry.get("arrangement_lang", "BI") == "BI"
                     else " AGC publishes no English text for this Act, so the arrangement below "
                          "is in Bahasa Malaysia.")
        rows = "".join(f'<div class="lg-sec"><span class="lg-num">s.{E(a["s"])}</span>'
                       f'<span>{E(a["t"])}</span></div>' for a in arr)
        arrangement = f"""<section class="pad-sm"><div class="wrap-narrow">
  <details class="card lg-fold" style="padding:22px 24px">
    <summary><span style="font-family:'Literata',Georgia,serif;font-size:19px">Full arrangement of sections</span>
      <span class="label">{len(arr)} sections · show / hide</span></summary>
    <p class="label" style="margin:14px 0 0">Extracted from the AGC PDF on this page.{lang_note}</p>
    <div class="lg-arr">{rows}</div>
  </details>
</div></section>"""
    elif entry["kind"] == "federal_act" and not entry.get("text_layer"):
        arrangement = """<section class="pad-sm"><div class="wrap-narrow">
  <div class="lg-warn">AGC publishes this Act only as a scanned image with no text layer, so its
  sections cannot be listed or searched here. Open the PDF below to read it.</div>
</div></section>"""

    also = ""
    if entry["also"]:
        items = "".join(
            '<div class="lg-sec"><span class="lg-num">'
            + E(a["no"].replace("P.U. (A) ", "P.U.(A) ")) + "</span>"
            + (f'<a class="ulink" href="{E(a["remote"])}" target="_blank" rel="noopener">'
               f'{E(a["title"])} &rarr;</a>' if a.get("remote") else f'<span>{E(a["title"])}</span>')
            + "</div>" for a in entry["also"])
        also = f"""<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">Made under it</span><h2>Subsidiary legislation</h2></div></div>
  <div class="card" style="padding:18px 24px">{items}</div>
</div></section>"""

    watch = ""
    if entry.get("watch"):
        watch = f"""<section class="pad-sm"><div class="wrap-narrow">
  <div class="card card-dark" style="padding:26px">
    <span class="stamp" style="color:var(--riso-marigold);border-color:var(--riso-marigold)">Watch this</span>
    <p style="font-size:15.5px;line-height:1.65;margin:14px 0 0">{E(entry["watch"])}</p></div>
</div></section>"""

    internal = ""
    if entry.get("internal"):
        internal = (f'<section class="pad-sm"><div class="wrap-narrow">'
                    f'<a class="card lg-card" href="../..{E(entry["internal"])}">'
                    f'<span class="idx">ALIM guide</span>'
                    f'<h3>Plain-language guide to this Act</h3><p>Read it &rarr;</p></a>'
                    f'</div></section>')

    shows = ""
    hits = scen_for.get(entry["id"], [])
    if hits:
        cards = "".join(
            f'<a class="card lg-card" href="../doing/{E(s["id"])}/">'
            f'<span class="idx">Scenario</span><h3>{E(s["title"])}</h3>'
            f'<p>{E(s["lede"][:110])}&hellip;</p></a>' for s in hits[:6])
        shows = f"""<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">In practice</span><h2>Where this one bites</h2></div></div>
  <div class="grid grid-2">{cards}</div>
</div></section>"""

    segs = "".join(f'<span class="lg-chip" style="cursor:default">{E(segmeta[s])}</span>'
                   for s in entry["segments"])

    meta = [ref_of(entry)]
    if entry.get("as_at"):
        meta.append("consolidated to " + dt.date(
            *(int(x) for x in entry["as_at"].split("-"))).strftime("%-d %b %Y"))
    if entry.get("pages"):
        meta.append(f'{entry["pages"]} pp')
    if entry.get("issuer"):
        meta.append(entry["issuer"])

    body = f"""
<section class="dossier-head">
  <div class="wrap">
    <div class="dossier-meta">
      <span class="bar">{E(label)} · {TIER_LABEL[entry["tier"]]}</span>
      <div style="text-align:right">
        <span class="label">§ File · Legislation</span>
        <span class="label" style="display:block;margin-top:4px">Pillar 03 · Education</span>
      </div>
    </div>
    <p class="label" style="margin:0 0 10px"><a class="ulink" href="../">&larr; Legislation library</a></p>
    <h1 class="page-h1">{E(entry["short"])}</h1>
    <p class="page-lede" style="font-size:17px">{E(entry["title_en"] or "")}</p>
    {f'<p class="label" style="margin-top:6px">{E(entry["title_bm"])}</p>' if entry.get("title_bm") else ''}
    <p class="label" style="margin-top:14px">{E(" · ".join(meta))}</p>
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:14px">{obj_inks(entry["objectives"], objmeta)}</div>
    {staleness(entry)}
  </div>
  <div class="page-emblem" aria-hidden="true">03</div>
</section>

<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">Why it matters</span><h2>What this does to artists</h2></div></div>
  <p class="prose">{E(entry["why"])}</p>
</div></section>
{watch}
{internal}
{keys}
{shows}
{arrangement}
{also}
<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">Full text</span><h2>Read the law</h2></div></div>
  <div class="grid grid-2">{"".join(pdfs)}</div>
  <p class="label" style="margin-top:16px">Source of record ·
    <a class="ulink" href="{E(entry["source"] or 'https://lom.agc.gov.my/')}" target="_blank" rel="noopener">{E((entry["source"] or 'lom.agc.gov.my').replace('https://', ''))}</a></p>
</div></section>

<section class="pad-sm"><div class="wrap-narrow">
  <span class="label">Who this reaches</span>
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 26px">{segs}</div>
  {disclaimer(depth)}
</div></section>
"""
    return (head(f"{entry['short']} · ALIM Legislation Library",
                 entry["why"][:155].replace("\n", " ") + "…",
                 f"https://alim.my/legislation/{entry['id']}/", depth)
            + body + tail(depth, lib["generated"][:10], lib["catalogue_fetched"]))


# ---------------------------------------------------------------------------
def scenario_page(sc, lib, by_id, depth=3):
    objmeta, segmeta = lib["objectives"], lib["segments"]
    roles = sc.get("roles") or {}

    role_chips = "".join(
        f'<button class="lg-chip" data-role="{E(k)}" aria-pressed="false">{E(v)}</button>'
        for k, v in roles.items())
    if role_chips:
        role_chips = (f'<div class="lg-wrapchips" style="margin-top:18px">'
                      f'<span class="label" style="padding-right:4px">Narrow it down</span>'
                      f'{role_chips}'
                      f'<button class="lg-chip lg-alt" id="roleclear" aria-pressed="true">'
                      f'Show everything</button></div>')

    steps = []
    for i, (ref, rs, point) in enumerate(sc["steps"], 1):
        e = by_id[ref]
        badges = "".join(f'<span class="lg-roleb">{E(roles.get(r, r))}</span>' for r in rs)
        steps.append(
            f'<div class="lg-step" data-roles="{E(" ".join(rs))}">'
            f'<div class="lg-step-n">{i:02d}</div><div>'
            f'<h4><a href="../../{E(ref)}/">{E(e["short"])}</a></h4>'
            f'<span class="lg-ref">{E(ref_of(e))}</span>'
            f'<p>{E(point)}</p>'
            f'<div style="margin-top:9px">{badges}</div>'
            f'</div></div>')

    watch = ""
    if sc.get("watch"):
        watch = (f'<div class="card card-dark" style="padding:26px;margin-top:28px">'
                 f'<span class="stamp" style="color:var(--riso-marigold);'
                 f'border-color:var(--riso-marigold)">The one people miss</span>'
                 f'<p style="font-size:15.5px;line-height:1.65;margin:14px 0 0">'
                 f'{E(sc["watch"])}</p></div>')

    related = ""
    rel = [s for s in SCENARIOS if s["id"] in (sc.get("related") or [])]
    if rel:
        cards = "".join(
            f'<a class="card lg-card" href="../{E(r["id"])}/"><span class="idx">Scenario</span>'
            f'<h3>{E(r["title"])}</h3><p>{E(r["lede"][:110])}&hellip;</p></a>' for r in rel)
        related = f"""<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">Next door</span><h2>Related situations</h2></div></div>
  <div class="grid grid-2">{cards}</div></div></section>"""

    segs = "".join(f'<span class="lg-chip" style="cursor:default">{E(segmeta[s])}</span>'
                   for s in sc["segments"])

    # Only a positive attribution goes on the page. There is no "not yet
    # reviewed" badge: the standing notice at the foot of the page does that
    # work, professionally, without hedging in the reader's face.
    # On the page someone reads while it is actually happening, the route to a
    # person cannot be at the bottom behind the whole chain.
    help_line = ""
    if sc["id"] == "arrested":
        help_line = ('<p class="label" style="margin-top:14px">'
                     '<a class="ulink" href="../../../get-help/">'
                     'Talk to someone at ALIM &rarr;</a></p>')

    st = state_for(sc["id"])
    provenance = ""
    if st.get("show"):
        who = E(", ".join(st["reviewers"])) if st["reviewers"] else ""
        when = (" on " + E(st["date"])) if st.get("date") else ""
        line = st["line"] + ((f" Reviewed by {who}{when}." ) if who else "")
        provenance = (f'<div class="lg-prov" data-tone="{E(st["tone"])}">'
                      f'<span class="lg-provtag">{E(st["label"])}</span>'
                      f'<p>{line}</p></div>')

    body = f"""
<div class="lg-rev" id="revbar" hidden>
  <div class="wrap" id="revcredit" hidden></div>
  <div class="wrap" id="revmain">
    <span class="lg-rev-who" id="revwho"></span>
    <button class="lg-rev-btn lg-yes" id="revyes">&#10003;</button>
    <button class="lg-rev-btn" id="revno">&#9873;</button>
  </div>
</div>
<section class="dossier-head">
  <div class="wrap">
    <div class="dossier-meta">
      <span class="bar">Situation · {len(sc["steps"])} steps</span>
      <div style="text-align:right">
        <span class="label">§ File · Legislation</span>
        <span class="label" style="display:block;margin-top:4px">Pillar 03 · Education</span>
      </div>
    </div>
    <p class="label" style="margin:0 0 10px"><a class="ulink" href="../../">&larr; Legislation library</a></p>
    <h1 class="page-h1">{E(sc["title"])}</h1>
    <p class="page-lede">{E(sc["lede"])}</p>
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:16px">{obj_inks(sc["objectives"], objmeta)}</div>
    {role_chips}
    {help_line}
    {provenance}
  </div>
  <div class="page-emblem" aria-hidden="true">03</div>
</section>

<section class="pad-sm"><div class="wrap-narrow">
  <div class="sec-head"><div><span class="bar">The chain</span><h2>What reaches you, and in what order</h2></div></div>
  <div class="card" style="padding:8px 26px 20px">{"".join(steps)}</div>
  <p class="label" style="margin-top:14px" id="stepcount"></p>
  {watch}
</div></section>
{related}
<section class="pad-sm"><div class="wrap-narrow">
  <span class="label">Who this is for</span>
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 26px">{segs}</div>
  {disclaimer(depth)}
</div></section>
"""

    js = """
<script>
(function(){
  var steps=[].slice.call(document.querySelectorAll('.lg-step')),
      chips=[].slice.call(document.querySelectorAll('.lg-chip[data-role]')),
      clear=document.getElementById('roleclear'),
      out=document.getElementById('stepcount'),active=null;
  function paint(){
    var n=0;
    steps.forEach(function(s){
      var on=!active||s.dataset.roles.split(' ').indexOf(active)>-1;
      s.dataset.dim=on?'0':'1'; if(on)n++;
    });
    out.textContent=active?(n+' of '+steps.length+' apply to you'):'';
    chips.forEach(function(c){c.setAttribute('aria-pressed',c.dataset.role===active?'true':'false');});
    if(clear)clear.setAttribute('aria-pressed',active?'false':'true');
  }
  chips.forEach(function(c){c.addEventListener('click',function(){
    active=active===c.dataset.role?null:c.dataset.role;paint();});});
  if(clear)clear.addEventListener('click',function(){active=null;paint();});
  paint();
})();

/* ---- attribution: who reviewed this page, if anyone ------------------ */
(function(){
  var PAGE='__PAGE_ID__';
  fetch('../../review.php?state=1',{cache:'no-store'})
    .then(function(r){return r.ok?r.json():null;})
    .then(function(j){
      if(!j||!j[PAGE])return;
      var rec=j[PAGE],clean=function(x){return String(x||'').replace(/[<>&]/g,'');},
          head=document.querySelector('.dossier-head .wrap');
      if(!head)return;
      /* A plain-English check is not a legal sign-off and must never render as
         one, so the two are shown as separate lines with separate labels. */
      if(rec.legal){
        var d=document.createElement('div');
        d.className='lg-prov';d.setAttribute('data-tone','good');
        d.innerHTML='<span class="lg-provtag">Reviewed by counsel</span><p>'+
          'Act numbers, titles and section numbers are verified against the Attorney '+
          'General\u2019s Chambers text. The notes on this page were reviewed by '+
          clean(rec.legal.by)+', a practising lawyer, on '+clean(rec.legal.on)+'.</p>';
        head.appendChild(d);
      }
      if(rec.plain){
        var e=document.createElement('div');
        e.className='lg-prov';
        e.innerHTML='<span class="lg-provtag">Read for plain English</span><p>'+
          clean(rec.plain.by)+' read this page on '+clean(rec.plain.on)+
          ' to check it can be followed by someone who is not a lawyer. That is a '+
          'readability check, not a legal opinion.</p>';
        head.appendChild(e);
      }
    }).catch(function(){});
})();

/* ---- the review bar: two buttons, one click -------------------------- */
(function(){
  var PAGE='__PAGE_ID__',
      tok=new URLSearchParams(location.search).get('r');
  if(!tok)return;
  var bar=document.getElementById('revbar'),who=document.getElementById('revwho'),
      yes=document.getElementById('revyes'),no=document.getElementById('revno'),
      wrap=document.getElementById('revmain'),
      creditRow=document.getElementById('revcredit'),me=null;

  function esc(s){return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  fetch('../../review.php?whoami='+encodeURIComponent(tok))
    .then(function(r){return r.json();})
    .then(function(j){
      if(!j.ok)return;
      me=j;
      var done=j.pages.filter(function(p){return p.done;}).length,
          legal=(j.track!=='plain');
      yes.innerHTML='\u2713&nbsp; '+(legal?'This is right':'I could follow this');
      no.innerHTML='\u2691&nbsp; '+(legal?'Something is wrong':'This lost me');
      who.textContent=(legal?'Reviewing as ':'Reading as ')+j.name+' \u00b7 '+
        done+' of '+j.pages.length+' done';
      bar.hidden=false;
      if(!j.credit)askCredit(legal); else showCredit(j.credit,legal);
      var mine=j.pages.filter(function(p){return p.id===PAGE;})[0];
      if(mine&&mine.done)settled(mine.verdict,null,done,j.pages.length);
    }).catch(function(){});

  function post(verdict,note){
    yes.disabled=no.disabled=true;
    return fetch('../../review.php',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({token:tok,page:PAGE,verdict:verdict,note:note||''})})
      .then(function(r){return r.json();})
      .then(function(j){
        if(!j.ok){who.textContent=j.error||'could not record that';
          yes.disabled=no.disabled=false;return;}
        settled(verdict,j.next,j.done,j.of);
      }).catch(function(){who.textContent='no connection, try again';
        yes.disabled=no.disabled=false;});
  }

  function settled(verdict,next,done,of){
    var legal=!me||me.track!=='plain';
    var cr=me&&me.credit;
    var how=cr==='name'?' Your name is on it.'
           :cr==='role'?(legal?' Credited to a lawyer on the board, without your name.'
                             :' Credited to an ALIM director, without your name.')
           :' Nothing is published under your name.';
    var msg=verdict==='clear'
      ? ((legal?'Recorded as reviewed.':'Recorded as a plain-English check, not a legal sign-off.')+how)
      : 'Flagged. Raul has it.';
    var nx=next?(' <a class="ulink" href="../'+esc(next.id)+'/?r='+encodeURIComponent(tok)+
      '">Next: '+esc(next.title)+' \u2192</a>'):' <strong>That is your bundle done. Thank you.</strong>';
    wrap.innerHTML='<span class="lg-revdone">'+esc(msg)+' '+(done!=null?('('+done+' of '+of+')'):'')+
      nx+'</span> <button class="lg-rev-btn" id="revundo">Undo</button>';
    document.getElementById('revundo').addEventListener('click',function(){
      fetch('../../review.php',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({token:tok,page:PAGE,verdict:'undo'})})
        .then(function(){location.reload();});
    });
  }

  /* Nobody is named on a public page until they have said so. This asks once,
     before the first click, and never again. */
  function askCredit(legal){
    creditRow.hidden=false;
    creditRow.innerHTML='<p class="lg-rev-ask">Before you start: how would you like to be '+
      'credited on pages you clear?<small>'+
      (legal?'Your name would appear publicly on a statement of Malaysian law. Check your firm '+
             'and your own view on publicity first; there is no wrong answer and you can change '+
             'it any time.'
           :'Your name would appear publicly, noted as a plain-English check rather than legal '+
            'advice. You can change it any time.')+'</small></p>'+
      '<button class="lg-rev-btn" data-credit="name">Use my name</button>'+
      '<button class="lg-rev-btn" data-credit="role">'+
        (legal?'Say &ldquo;a lawyer on the board&rdquo;':'Say &ldquo;an ALIM director&rdquo;')+'</button>'+
      '<button class="lg-rev-btn" data-credit="none">Don\u2019t credit me</button>';
    wrap.hidden=true;
    creditRow.querySelectorAll('[data-credit]').forEach(function(b){
      b.addEventListener('click',function(){
        fetch('../../review.php',{method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({token:tok,verdict:'credit',credit:b.dataset.credit,page:PAGE})})
          .then(function(r){return r.json();})
          .then(function(j){ if(me)me.credit=b.dataset.credit;
            wrap.hidden=false; showCredit(b.dataset.credit,legal); });
      });
    });
  }
  function showCredit(mode,legal){
    var label=mode==='name'?'shown under your name'
             :mode==='role'?(legal?'shown as a lawyer on the board':'shown as an ALIM director')
             :'not credited publicly';
    creditRow.hidden=false;
    creditRow.innerHTML='<span class="lg-rev-who" style="flex:1 1 auto">Credit: '+label+
      '</span><button class="lg-rev-change" id="revrecredit">change</button>';
    document.getElementById('revrecredit').addEventListener('click',function(){askCredit(legal);});
  }

  yes.addEventListener('click',function(){post('clear');});
  no.addEventListener('click',function(){
    if(document.getElementById('revnote')){
      var v=document.getElementById('revnote').value.trim();
      if(!v){document.getElementById('revnote').focus();return;}
      post('flag',v);return;
    }
    var t=document.createElement('textarea');
    t.id='revnote';t.rows=3;
    t.placeholder=(!me||me.track!=='plain')
      ? 'What is wrong? Section numbers help but are not needed.'
      : 'Where did it lose you? Plain words are exactly what is useful here.';
    wrap.appendChild(t);t.focus();
    no.textContent='Send it';
  });
})();
</script>"""

    js = js.replace("__PAGE_ID__", sc["id"])
    return (head(f"{sc['title']} · ALIM Legislation Library",
                 sc["lede"][:155], f"https://alim.my/legislation/doing/{sc['id']}/", depth)
            + body + tail(depth, lib["generated"][:10], lib["catalogue_fetched"], js))


# ---------------------------------------------------------------------------
def index_page(lib, depth=1):
    objmeta, segmeta = lib["objectives"], lib["segments"]
    entries = sorted(lib["entries"], key=lambda e: (e["tier"], e["short"].lower()))

    cards = []
    for e in entries:
        asat = (dt.date(*(int(x) for x in e["as_at"].split("-"))).strftime("%b %Y")
                if e.get("as_at") else "")
        meta = " · ".join(x for x in (ref_of(e), f"as at {asat}" if asat else "") if x)
        cards.append(f"""<a class="card lg-card" href="{E(e['id'])}/"
  data-id="{E(e['id'])}" data-obj="{E(' '.join(e['objectives']))}"
  data-seg="{E(' '.join(e['segments']))}" data-tier="{e['tier']}">
  <div style="display:flex;flex-wrap:wrap;gap:5px">{obj_inks(e['objectives'], objmeta)}</div>
  <h3>{E(e['short'])}</h3>
  <p class="lg-meta" style="margin-bottom:8px">{E(meta)}</p>
  <p>{E(e['why'][:140])}&hellip;</p>
</a>""")

    scen_cards = "".join(
        f'<a class="card lg-card" href="doing/{E(s["id"])}/">'
        f'<div style="display:flex;flex-wrap:wrap;gap:5px">{obj_inks(s["objectives"], objmeta)}</div>'
        f'<h3>{E(s["title"])}</h3>'
        f'<p class="lg-meta" style="margin-bottom:8px">{len(s["steps"])} steps</p>'
        f'<p>{E(s["lede"][:125])}&hellip;</p></a>' for s in SCENARIOS)

    def chips(kind, items):
        return "".join(
            f'<button class="lg-chip" data-filter="{kind}" data-value="{E(str(k))}" '
            f'aria-pressed="false">{E(v)}</button>' for k, v in items)

    seg_keys = list(segmeta.keys())
    head_cells = "".join(f'<th>{E(segmeta[s])}</th>' for s in seg_keys)
    rows = []
    for ok, ov in objmeta.items():
        cells = []
        for sk in seg_keys:
            n = sum(1 for e in entries if ok in e["objectives"] and sk in e["segments"])
            cells.append(f'<td><a class="lg-cell" data-n="{n}" '
                         f'href="?view=instruments&amp;obj={E(ok)}&amp;seg={E(sk)}">{n}</a></td>')
        total = sum(1 for e in entries if ok in e["objectives"])
        rows.append(f'<tr><th><span class="lg-ink" style="background:{OBJ_INK[ok]}">'
                    f'{E(ov["label"])}</span></th>{"".join(cells)}'
                    f'<td><a class="lg-cell" data-n="{total}" '
                    f'href="?view=instruments&amp;obj={E(ok)}"><strong>{total}</strong></a></td></tr>')
    seg_totals = "".join(
        f'<td><a class="lg-cell" data-n="{sum(1 for e in entries if s in e["segments"])}" '
        f'href="?view=instruments&amp;seg={E(s)}">'
        f'{sum(1 for e in entries if s in e["segments"])}</a></td>' for s in seg_keys)

    n_pdf = sum(1 for e in entries for p in e["pdf"].values() if p.get("local"))
    n_sec = sum(len(e.get("arrangement") or []) for e in entries)

    pillars = "".join(f"""<div class="card">
      <span class="lg-ink" style="background:{OBJ_INK[k]}">{E(v['label'])}</span>
      <p style="margin-top:12px">{E(v['blurb'])}</p></div>""" for k, v in objmeta.items())

    try_chips = "".join(
        f'<button class="lg-chip lg-alt" data-try="{E(t)}">{E(t)}</button>'
        for t in ["DJing", "busking", "MCMC", "moral rights", "client won't pay",
                  "foreign artist", "mural", "sell merch", "Act 332"])

    body = f"""
<section class="dossier-head">
  <div class="wrap">
    <div class="dossier-meta">
      <span class="bar">Know your rights</span>
      <div style="text-align:right">
        <span class="label">§ File · Legislation</span>
        <span class="label" style="display:block;margin-top:4px">Pillar 03 · Education</span>
      </div>
    </div>
    <h1 class="page-h1">The law that governs <em>the arts</em>.</h1>
    <p class="page-lede">You don't need to know which Act to look for. Say what you're doing, or
      what's gone wrong, and we'll show you the laws that reach it, in the order they reach you.
      Everything here is the Attorney General's Chambers' own text, and every page tells you how old
      that text is. If you'd rather talk to a person, that's what
      <a class="ulink" href="../get-help/">Get Help</a> is for.</p>
    <div class="stat-row" style="margin-top:26px">
      <div class="stat red"><b>{len(SCENARIOS)}</b><s>situations mapped</s></div>
      <div class="stat"><b>{len(entries)}</b><s>laws &amp; codes</s></div>
      <div class="stat"><b>{n_pdf}</b><s>full texts hosted here</s></div>
      <div class="stat"><b>{n_sec:,}</b><s>sections searchable</s></div>
    </div>
  </div>
  <div class="page-emblem" aria-hidden="true">03</div>
</section>

<section class="pad-sm"><div class="wrap">
  <div class="lg-tools">
    <div class="lg-searchwrap">
      <input id="q" class="lg-search" type="search" autocomplete="off" spellcheck="false"
        placeholder="What are you doing? Try &ldquo;DJing&rdquo;, &ldquo;busking&rdquo;, &ldquo;client won&rsquo;t pay&rdquo;, &ldquo;Act 332&rdquo;">
      <span class="lg-slash" aria-hidden="true">/</span>
    </div>
    <div class="lg-wrapchips" style="margin-top:12px">
      <span class="label" style="padding-right:4px">Try</span>{try_chips}
    </div>
  </div>

  <div id="results" hidden>
    <div id="answer"></div>
    <div id="refine" hidden style="margin:22px 0 30px"></div>
    <div id="instrhits"></div>
    <div id="sechitswrap" hidden style="margin-top:34px">
      <span class="bar">Matching sections</span>
      <div id="sechits" style="display:grid;gap:8px;margin-top:14px"></div>
    </div>
    <div id="noresult" hidden></div>
  </div>

  <div id="browse">
    <div class="lg-tabs" role="tablist">
      <button class="lg-tab" role="tab" data-view="scenarios" aria-selected="true">What are you doing?</button>
      <button class="lg-tab" role="tab" data-view="framework" aria-selected="false">The big picture</button>
      <button class="lg-tab" role="tab" data-view="instruments" aria-selected="false">The full list</button>
    </div>

    <div data-panel="scenarios">
      <p class="label" style="margin-bottom:16px">{len(SCENARIOS)} things people come to us about</p>
      <div class="grid grid-3">{scen_cards}</div>
    </div>

    <div data-panel="framework" hidden>
      <div class="sec-head"><div><span class="bar">Three aims, ten fields</span>
        <h2>The whole library on one grid</h2></div></div>
      <p class="prose" style="margin-bottom:22px">Every law here is tagged by what it's for and who
        it reaches. The numbers are live filters, so click one to see what's behind it.</p>
      <div class="lg-matrixscroll">
        <table class="lg-matrix">
          <thead><tr><th style="text-align:left">Aim &#8595; / Field &#8594;</th>{head_cells}<th>All</th></tr></thead>
          <tbody>{"".join(rows)}
            <tr><th>Laws per field</th>{seg_totals}
              <td><a class="lg-cell" data-n="{len(entries)}" href="?view=instruments">{len(entries)}</a></td></tr>
          </tbody>
        </table>
      </div>
      <div class="grid grid-3" style="margin-top:26px">{pillars}</div>
    </div>

    <div data-panel="instruments" hidden>
      <div style="display:grid;gap:8px;margin-bottom:22px">
        <div class="lg-chiprow"><span class="label">Objective</span>{chips('obj', [(k, v['label']) for k, v in objmeta.items()])}</div>
        <div class="lg-chiprow"><span class="label">Segment</span>{chips('seg', list(segmeta.items()))}</div>
        <div class="lg-chiprow"><span class="label">Depth</span>{chips('tier', list(TIER_LABEL.items()))}
          <button id="clear" class="lg-chip lg-alt">Clear all</button></div>
      </div>
      <p id="count" class="label" style="margin-bottom:16px"></p>
      <div id="grid" class="grid grid-3">{"".join(cards)}</div>
      <p id="empty" hidden class="prose" style="text-align:center;padding:60px 0">Nothing matches
        those filters. Clear them and start again.</p>
    </div>
  </div>
</div></section>

<section class="pad tint"><div class="wrap">
  <div class="grid grid-2">
    <div class="card">
      <span class="bar">Known gap</span>
      <h3 style="margin-top:14px">What's not in here yet</h3>
      <p style="margin-top:10px">Entertainment licensing, public order by-laws and Syariah criminal
        offences sit on the State List, so the rules that decide whether a show can happen differ in
        every state and are not published on the federal portal at all. Neither are most local
        authority by-laws.</p>
      <p style="margin-top:10px">That gap is the single biggest one in any Malaysian legal resource
        for the arts, this one included. Building it out state by state is a standing ALIM research
        task, and the pages here say so rather than pretend otherwise.</p>
    </div>
    <div class="card">
      <span class="bar">Method</span>
      <h3 style="margin-top:14px">How this library is kept honest</h3>
      <p style="margin-top:10px">Every Act number, title and consolidation date is read from the AGC
        catalogue, not from memory. Where AGC publishes a consolidated &ldquo;as at&rdquo; text, that
        is the copy shown here, not the original enactment.</p>
      <p style="margin-top:10px">Section numbers under <em>What to read first</em> are extracted from
        the PDF itself. Where a number could not be confirmed, the entry is labelled <em>topic</em>
        rather than carrying a number we guessed. Where AGC publishes only a scan with no text layer,
        the page says so instead of showing an empty list.</p>
    </div>
  </div>
</div></section>

<section class="pad-sm"><div class="wrap-narrow">{disclaimer(depth)}</div></section>
"""

    js = r"""
<script>
(function(){
  var q=document.getElementById('q'),
      results=document.getElementById('results'),browse=document.getElementById('browse'),
      answer=document.getElementById('answer'),refine=document.getElementById('refine'),
      instrhits=document.getElementById('instrhits'),
      sechits=document.getElementById('sechits'),sechitswrap=document.getElementById('sechitswrap'),
      noresult=document.getElementById('noresult'),
      grid=document.getElementById('grid'),cards=[].slice.call(grid.children),
      count=document.getElementById('count'),empty=document.getElementById('empty'),
      IDX=null,SECS=null,VOCAB=[],
      active={obj:new Set(),seg:new Set(),tier:new Set()},
      role=null,view='scenarios';

  function esc(s){return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  /* "act"/"akta" are dropped so "Act 332" resolves on the number alone, and
     one-character fragments go too: "won't" tokenises to won + t, and a bare
     "t" matched nothing and killed the whole query under AND semantics. */
  var STOP={act:1,akta:1,the:1,a:1,an:1,and:1,or:1,of:1,for:1,to:1,in:1,on:1,at:1,
    is:1,are:1,was:1,were:1,be:1,been:1,my:1,me:1,i:1,we:1,our:1,you:1,your:1,
    it:1,its:1,this:1,that:1,these:1,those:1,with:1,by:1,from:1,about:1,
    do:1,does:1,did:1,can:1,will:1,would:1,should:1,have:1,has:1,had:1,get:1,
    not:1,no:1,but:1,if:1,how:1,what:1,when:1,where:1,who:1,am:1,as:1,so:1,up:1,
    someone:1,something:1,any:1,all:1,just:1,very:1,really:1,please:1,help:1};
  function toks(s){return String(s).toLowerCase()
    .replace(/[^a-z0-9]+/g,' ').trim().split(' ')
    .filter(function(w){return w&&!STOP[w]&&w.length>1;});}

  fetch('data/search.json').then(function(r){return r.json();}).then(function(j){
    IDX=j;
    var v={};
    j.instruments.forEach(function(e){
      e.tt.concat(e.at).forEach(function(w){if(w.length>2)v[w]=1;});});
    j.scenarios.forEach(function(s){
      s.tt.concat(s.at).forEach(function(w){if(w.length>2)v[w]=1;});});
    VOCAB=Object.keys(v);
    boot();
  });

  /* --- matching: whole words or word prefixes, never raw substrings.
         "dj" used to match "a-dj-acent" and return three wrong Acts. --- */
  /* Prefix match both ways so a plural finds its singular: the query "videos"
     has to reach the alias "video", and "contracts" the alias "contract". */
  function pm(list,t){
    for(var i=0;i<list.length;i++){
      var w=list[i];
      if(w.indexOf(t)===0) return true;
      if(t.length>3&&w.length>3&&t.indexOf(w)===0) return true;
    }
    return false;
  }
  function hitScore(tok,e){
    var s=0;
    if(pm(e.tt,tok)) s=45;
    if(s<35&&pm(e.at,tok)) s=35;
    if(e.num&&e.num.indexOf(tok)===0) s=Math.max(s,90);
    if(s===0&&pm(e.wt,tok)) s=8;
    return s;
  }
  function scoreInstruments(tk,phrase){
    var out=[];
    IDX.instruments.forEach(function(e){
      var total=0,matched=0,strong=0;
      for(var i=0;i<tk.length;i++){
        var s=hitScore(tk[i],e);
        if(s>0){matched++;total+=s;if(s>=35)strong++;}
      }
      /* needs one real hit on a title, alias or Act number, and has to cover
         most of what was typed. A weak why-text brush alone is not a result. */
      if(!strong||matched/tk.length<0.5) return;
      total+=matched*10;
      if(e.al.indexOf(phrase)>-1) total+=120;
      if(e.t.toLowerCase()===phrase) total+=140;
      total+=(e.tier===1?6:e.tier===2?3:0);
      out.push([total,e]);
    });
    out.sort(function(a,b){return b[0]-a[0];});
    return out;
  }
  function scoreScenarios(tk,phrase){
    var out=[];
    IDX.scenarios.forEach(function(s){
      var total=0,matched=0,strong=0;
      for(var i=0;i<tk.length;i++){
        var t=tk[i],best=0;
        if(pm(s.tt,t)) best=50;
        if(best<40&&pm(s.at,t)) best=40;
        if(best===0&&pm(s.lt,t)) best=6;
        if(best>0){matched++;total+=best;if(best>=40)strong++;}
      }
      if(!strong||matched/tk.length<0.5) return;
      total+=matched*10;
      if(s.al.indexOf(phrase)>-1) total+=160;
      out.push([total,s]);
    });
    out.sort(function(a,b){return b[0]-a[0];});
    return out;
  }

  /* --- typo tolerance: "Djiing" still has to find DJing --- */
  function lev(a,b,max){
    if(Math.abs(a.length-b.length)>max) return max+1;
    var prev=[],cur=[],i,j;
    for(j=0;j<=b.length;j++) prev[j]=j;
    for(i=1;i<=a.length;i++){
      cur=[i]; var best=i;
      for(j=1;j<=b.length;j++){
        cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a.charAt(i-1)===b.charAt(j-1)?0:1));
        if(cur[j]<best)best=cur[j];
      }
      if(best>max) return max+1;
      prev=cur.slice();
    }
    return prev[b.length];
  }
  function correct(tk){
    var out=[],changed=false;
    tk.forEach(function(t){
      if(t.length<4||VOCAB.indexOf(t)>-1){out.push(t);return;}
      var best=null,bd=3;
      for(var i=0;i<VOCAB.length;i++){
        var d=lev(t,VOCAB[i],2);
        if(d<bd){bd=d;best=VOCAB[i];if(d===1)break;}
      }
      if(best){out.push(best);changed=true;}else out.push(t);
    });
    return changed?out:null;
  }

  function instrCard(e){
    return '<a class="card lg-card" href="'+esc(e.id)+'/">'+
      '<div style="display:flex;flex-wrap:wrap;gap:5px">'+e.ink+'</div>'+
      '<h3>'+esc(e.t)+'</h3>'+
      '<p class="lg-meta" style="margin-bottom:8px">'+esc(e.meta)+'</p>'+
      '<p>'+esc(e.why)+'…</p></a>';
  }
  function renderAnswer(s){
    var roles=s.roles||{},rk=Object.keys(roles);
    var chips=rk.map(function(k){
      return '<button class="lg-chip" data-role="'+esc(k)+'" aria-pressed="'+
        (role===k?'true':'false')+'">'+esc(roles[k])+'</button>';}).join('');
    if(chips) chips='<div class="lg-wrapchips" style="margin-top:18px">'+
      '<span class="label" style="padding-right:4px">Narrow it down</span>'+chips+
      '<button class="lg-chip lg-alt" data-role="" aria-pressed="'+(role?'false':'true')+
      '">Show everything</button></div>';
    var shown=0;
    var steps=s.steps.map(function(st,i){
      var on=!role||st.r.indexOf(role)>-1; if(on)shown++;
      var badges=st.r.map(function(r){
        return '<span class="lg-roleb">'+esc(roles[r]||r)+'</span>';}).join('');
      return '<div class="lg-step" data-dim="'+(on?'0':'1')+'">'+
        '<div class="lg-step-n">'+(i<9?'0':'')+(i+1)+'</div><div>'+
        '<h4><a href="'+esc(st.ref)+'/">'+esc(st.t)+'</a></h4>'+
        '<span class="lg-ref">'+esc(st.ref_label)+'</span>'+
        '<p>'+esc(st.p)+'</p><div style="margin-top:9px">'+badges+'</div></div></div>';
    }).join('');
    var watch=s.watch?('<div class="card card-dark" style="padding:26px;margin-top:22px">'+
      '<span class="stamp" style="color:var(--riso-marigold);border-color:var(--riso-marigold)">'+
      'The one people miss</span><p style="font-size:15.5px;line-height:1.65;margin:14px 0 0">'+
      esc(s.watch)+'</p></div>'):'';
    return '<div class="card" style="padding:30px">'+
      '<span class="bar">Answer</span>'+
      '<h2 style="font-family:\'Literata\',Georgia,serif;font-size:clamp(26px,3.6vw,38px);'+
      'font-weight:normal;margin:14px 0 8px;line-height:1.15">'+esc(s.t)+'</h2>'+
      '<p class="prose" style="margin:0">'+esc(s.lede)+'</p>'+chips+
      '<p class="label" style="margin:22px 0 4px">In this order · '+
      (role?(shown+' of '+s.steps.length+' apply to you'):(s.steps.length+' steps'))+'</p>'+
      '<div style="margin-top:6px">'+steps+'</div>'+
      '<p class="label" style="margin-top:20px"><a class="ulink" href="doing/'+esc(s.id)+
      '/">Open as its own page, printable and shareable →</a></p></div>'+watch;
  }
  function renderRefine(scens,instr,matched){
    var bits=[];
    var rel=((matched&&matched.related)||[]).map(function(id){
      var f=IDX.scenarios.filter(function(x){return x.id===id;})[0];
      return f?'<button class="lg-chip lg-alt" data-try="'+esc(f.t)+'">'+esc(f.t)+'</button>':'';
    }).join('');
    var others=scens.filter(function(s){return !matched||s.id!==matched.id;}).slice(0,3)
      .map(function(s){return '<button class="lg-chip lg-alt" data-try="'+esc(s.t)+'">'+
        esc(s.t)+'</button>';}).join('');
    if(rel||others) bits.push('<div class="lg-wrapchips" style="margin-bottom:10px">'+
      '<span class="label" style="padding-right:4px">Or you might mean</span>'+rel+others+'</div>');
    var segs={};
    instr.slice(0,14).forEach(function(e){
      e.seg.forEach(function(s){segs[s]=(segs[s]||0)+1;});});
    var top=Object.keys(segs).sort(function(a,b){return segs[b]-segs[a];}).slice(0,5);
    if(top.length>1) bits.push('<div class="lg-wrapchips">'+
      '<span class="label" style="padding-right:4px">Narrow by segment</span>'+
      top.map(function(s){return '<a class="lg-chip" href="?view=instruments&seg='+
        encodeURIComponent(s)+'">'+esc(IDX.segments[s])+'</a>';}).join('')+'</div>');
    return bits.join('');
  }

  function search(raw){
    var phrase=raw.trim().toLowerCase(),tk=toks(raw);
    if(!tk.length||!IDX){results.hidden=true;browse.hidden=false;return;}
    browse.hidden=true;results.hidden=false;
    var sc=scoreScenarios(tk,phrase),ins=scoreInstruments(tk,phrase),note='';
    if(!sc.length&&!ins.length){
      var fixed=correct(tk);
      if(fixed){
        var fp=fixed.join(' ');
        sc=scoreScenarios(fixed,fp);ins=scoreInstruments(fixed,fp);
        if(sc.length||ins.length)
          note='<p class="label" style="margin-bottom:16px">Showing results for <strong>'+
            esc(fp)+'</strong></p>';
      }
    }
    /* Lead with a scenario only when it beats the best single instrument.
       "withholding tax" is the Income Tax Act, not a brush against a scenario
       that happens to list "withholding payment" as one of its aliases. */
    var scens=sc.map(function(x){return x[1];}),instr=ins.map(function(x){return x[1];});
    var matched=(sc.length&&(!ins.length||sc[0][0]>=ins[0][0]))?sc[0][1]:null;
    answer.innerHTML=note+(matched?renderAnswer(matched):'');
    if(matched){
      var inChain={};matched.steps.forEach(function(s){inChain[s.ref]=1;});
      instr=instr.filter(function(e){return !inChain[e.id];});
    }
    instrhits.innerHTML=instr.length?
      ('<div style="margin-top:'+(matched?'34px':'0')+'">'+
       '<span class="bar">'+(matched?'Also relevant':'Laws and codes')+'</span>'+
       '<div class="grid grid-3" style="margin-top:14px">'+
       instr.slice(0,12).map(instrCard).join('')+'</div></div>'):'';
    refine.innerHTML=renderRefine(scens,instr,matched);
    refine.hidden=!refine.innerHTML;

    sechits.innerHTML='';
    if(phrase.length>=3&&SECS){
      var hits=[],rx=new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'ig');
      for(var i=0;i<SECS.length&&hits.length<25;i++)
        if(SECS[i][3].toLowerCase().indexOf(phrase)>-1)hits.push(SECS[i]);
      hits.forEach(function(h){
        var a=document.createElement('a');
        a.href=h[0]+'/';a.className='lg-hit';
        a.innerHTML='<span class="lg-num">s.'+esc(h[2])+'</span> '+
          esc(h[3]).replace(rx,function(m){return '<mark>'+m+'</mark>';})+
          '<span class="label" style="display:block;margin-top:4px">'+esc(h[1])+'</span>';
        sechits.appendChild(a);
      });
      sechitswrap.hidden=hits.length===0;
    } else sechitswrap.hidden=true;

    var none=!matched&&!instr.length&&sechitswrap.hidden;
    noresult.hidden=!none;
    if(none) noresult.innerHTML='<div class="card" style="padding:30px">'+
      '<span class="bar">No match</span>'+
      '<p class="prose" style="margin:14px 0 0">Nothing in the library matches <strong>'+
      esc(raw)+'</strong>. This library is federal legislation plus the codes and treaties around '+
      'it; state entertainment enactments and council by-laws are the known gap. Try one of these, '+
      'or tell us what happened.</p><div class="lg-wrapchips" style="margin-top:18px">'+
      IDX.scenarios.slice(0,6).map(function(s){
        return '<button class="lg-chip lg-alt" data-try="'+esc(s.t)+'">'+esc(s.t)+'</button>';
      }).join('')+'</div>'+
      '<p class="label" style="margin-top:20px"><a class="ulink" href="../get-help/">'+
      'Ask ALIM directly →</a></p></div>';
  }

  function has(set,csv){ if(!set.size)return true; var p=(csv||'').split(' ');
    var it=set.values(),n;while(!(n=it.next()).done){if(p.indexOf(n.value)>-1)return true;}
    return false; }
  function paintFilters(){
    var shown=0;
    cards.forEach(function(c){
      var ok=has(active.obj,c.dataset.obj)&&has(active.seg,c.dataset.seg)&&
             has(active.tier,c.dataset.tier);
      c.hidden=!ok; if(ok)shown++;
    });
    count.textContent=shown+(shown===1?' law or code':' laws and codes');
    empty.hidden=shown>0;
    document.querySelectorAll('.lg-chip[data-filter]').forEach(function(b){
      b.setAttribute('aria-pressed',active[b.dataset.filter].has(b.dataset.value)?'true':'false');
    });
  }
  function setView(v){
    view=v;
    document.querySelectorAll('.lg-tab').forEach(function(t){
      t.setAttribute('aria-selected',t.dataset.view===v?'true':'false');});
    document.querySelectorAll('[data-panel]').forEach(function(p){
      p.hidden=p.dataset.panel!==v;});
  }

  document.addEventListener('click',function(ev){
    var t=ev.target.closest('[data-try]');
    if(t){q.value=t.dataset.try;role=null;search(q.value);sync();
      q.scrollIntoView({block:'center',behavior:'smooth'});return;}
    var r=ev.target.closest('[data-role]');
    if(r&&results.contains(r)){role=r.dataset.role||null;search(q.value);return;}
    var tab=ev.target.closest('.lg-tab');
    if(tab){setView(tab.dataset.view);sync();return;}
    var f=ev.target.closest('.lg-chip[data-filter]');
    if(f){var k=f.dataset.filter,v=f.dataset.value;
      if(active[k].has(v))active[k].delete(v);else active[k].add(v);
      paintFilters();sync();return;}
    if(ev.target.closest('#clear')){
      active={obj:new Set(),seg:new Set(),tier:new Set()};paintFilters();sync();}
  });
  var t0;q.addEventListener('input',function(){
    role=null;clearTimeout(t0);t0=setTimeout(function(){search(q.value);sync();},140);});
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();q.select();}
    if(e.key==='Escape'&&document.activeElement===q){q.value='';search('');sync();q.blur();}
  });

  function sync(){
    var p=new URLSearchParams();
    if(q.value.trim())p.set('q',q.value.trim());
    else{
      if(view!=='scenarios')p.set('view',view);
      active.obj.forEach(function(v){p.append('obj',v);});
      active.seg.forEach(function(v){p.append('seg',v);});
      active.tier.forEach(function(v){p.append('tier',v);});
    }
    var s=p.toString();
    history.replaceState(null,'',s?('?'+s):location.pathname);
  }
  function boot(){
    fetch('data/sections.json').then(function(r){return r.json();})
      .then(function(j){SECS=j;if(q.value.trim())search(q.value);});
    var p=new URLSearchParams(location.search);
    p.getAll('obj').forEach(function(v){active.obj.add(v);});
    p.getAll('seg').forEach(function(v){active.seg.add(v);});
    p.getAll('tier').forEach(function(v){active.tier.add(v);});
    paintFilters();
    setView(p.get('view')||((p.get('obj')||p.get('seg')||p.get('tier'))?'instruments':'scenarios'));
    if(p.get('q')){q.value=p.get('q');search(q.value);}
  }
})();
</script>"""

    return (head("Legislation Library · ALIM.my",
                 "Start with what you're doing. A searchable library of the Malaysian law that "
                 "reaches artists: copyright, censorship, licensing, employment and heritage, "
                 "sourced from the Attorney General's Chambers.",
                 "https://alim.my/legislation/", depth)
            + body + tail(depth, lib["generated"][:10], lib["catalogue_fetched"], js))


# ---------------------------------------------------------------------------
def main():
    lib = json.loads((DATA / "library.json").read_text("utf-8"))
    by_id = {e["id"]: e for e in lib["entries"]}
    objmeta, segmeta = lib["objectives"], lib["segments"]

    # A bad reference here would ship a dead link, so fail the build instead.
    problems, seen = [], set()
    ids = {s["id"] for s in SCENARIOS}
    for sc in SCENARIOS:
        if sc["id"] in seen:
            problems.append(f"duplicate scenario id {sc['id']}")
        seen.add(sc["id"])
        for ref, roles, _ in sc["steps"]:
            if ref not in by_id:
                problems.append(f"{sc['id']}: unknown instrument {ref!r}")
            for r in roles:
                if r not in (sc.get("roles") or {}):
                    problems.append(f"{sc['id']}: step {ref} uses undeclared role {r!r}")
        for r in (sc.get("related") or []):
            if r not in ids:
                problems.append(f"{sc['id']}: unknown related scenario {r!r}")
        for s in sc["segments"]:
            if s not in segmeta:
                problems.append(f"{sc['id']}: unknown segment {s!r}")
        for o in sc["objectives"]:
            if o not in objmeta:
                problems.append(f"{sc['id']}: unknown objective {o!r}")
    for ref in ALIASES:
        if ref not in by_id:
            problems.append(f"alias block for unknown instrument {ref!r}")
    if problems:
        for p in problems:
            print("  !", p)
        raise SystemExit("build aborted: %d bad reference(s)" % len(problems))

    def tok(s):
        return [w for w in re.split(r"[^a-z0-9]+", (s or "").lower()) if w]

    sections = []
    for e in lib["entries"]:
        for a in (e.get("arrangement") or []):
            sections.append([e["id"], e["short"], a["s"], a["t"]])
        for s in e["sections"]:
            if not s["verified"]:
                sections.append([e["id"], e["short"], "-", s["t"]])
    (DATA / "sections.json").write_text(
        json.dumps(sections, ensure_ascii=False, separators=(",", ":")), "utf-8")

    instruments = []
    for e in lib["entries"]:
        al = ALIASES.get(e["id"], [])
        asat = (dt.date(*(int(x) for x in e["as_at"].split("-"))).strftime("%b %Y")
                if e.get("as_at") else "")
        instruments.append({
            "id": e["id"], "t": e["short"], "full": e["title_en"] or "",
            "meta": " · ".join(x for x in (ref_of(e), f"as at {asat}" if asat else "") if x),
            "why": e["why"][:140], "tier": e["tier"],
            "obj": e["objectives"], "seg": e["segments"],
            "ink": obj_inks(e["objectives"], objmeta),
            "al": al,
            "tt": sorted(set(tok(e["short"]) + tok(e["title_en"]) + tok(e["title_bm"]))),
            "at": sorted(set(w for a in al for w in tok(a))),
            "wt": sorted(set(tok(e["why"]))),
            "num": (e.get("act") or "").lower(),
        })

    scen = []
    for s in SCENARIOS:
        scen.append({
            "id": s["id"], "t": s["title"], "lede": s["lede"], "al": s["aliases"],
            "seg": s["segments"], "obj": s["objectives"], "roles": s.get("roles") or {},
            "watch": s.get("watch", ""), "related": s.get("related") or [],
            "tt": sorted(set(tok(s["title"]))),
            "at": sorted(set(w for a in s["aliases"] for w in tok(a))),
            "lt": sorted(set(tok(s["lede"]))),
            "steps": [{"ref": r, "t": by_id[r]["short"], "ref_label": ref_of(by_id[r]),
                       "r": roles, "p": p} for r, roles, p in s["steps"]],
        })

    (DATA / "search.json").write_text(json.dumps(
        {"instruments": instruments, "scenarios": scen, "segments": segmeta},
        ensure_ascii=False, separators=(",", ":")), "utf-8")

    scen_for = {}
    for s in SCENARIOS:
        for ref, _, _ in s["steps"]:
            scen_for.setdefault(ref, []).append(s)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(index_page(lib), "utf-8")
    for e in lib["entries"]:
        d = OUT / e["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(act_page(e, lib, scen_for), "utf-8")
    for s in SCENARIOS:
        d = OUT / "doing" / s["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(scenario_page(s, lib, by_id), "utf-8")

    # A bare re-harvest pulls the photographic scans back; catch it here rather
    # than discovering it in an rsync.
    heavy = [(e["short"], lang, m["bytes"]) for e in lib["entries"]
             for lang, m in e["pdf"].items() if m.get("local") and m.get("bytes", 0) > 12e6]
    if heavy:
        print("  ! oversized PDFs are staged for deploy; run tools/refresh.sh instead:")
        for short, lang, b in heavy:
            print(f"    {short} [{lang}] {b/1e6:.0f} MB")

    covered = len(scen_for)
    print(f"  {len(lib['entries'])} instrument pages + {len(SCENARIOS)} scenario pages + index")
    print(f"  scenarios cover {covered}/{len(lib['entries'])} instruments, "
          f"{sum(len(s['steps']) for s in SCENARIOS)} mapped steps")
    print(f"  search.json {(DATA / 'search.json').stat().st_size/1024:.0f} KB · "
          f"sections {len(sections):,} rows "
          f"({(DATA / 'sections.json').stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
