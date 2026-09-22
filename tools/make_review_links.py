# -*- coding: utf-8 -*-
"""
Issue personal review links and write the server-side token map.

  python3 tools/make_review_links.py Fahri=L2 Nanda=L1 Karl=L3 Nick=P1 Marisa=P2

Each reviewer gets one unguessable token. Their token is the whole of their
identity as far as the endpoint is concerned, so the link is the login: no
account, no password, no form. Clicking a button on a page they were sent is
the entire interaction.

Writes
  review/_reviewers.php        the token map, to be deployed OUTSIDE public_html
  review/review-links.md       the links and the message to send each person

The token map never goes in the repo's public tree and never gets rsynced to
public_html. Deploy it to domains/alim.my/private/reviewers.php.
"""
import pathlib
import secrets
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scenarios import SCENARIOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "review"
BASE = "https://alim.my/legislation/doing"

# Two tracks, because they are two different questions and only one of them
# needs a practising lawyer.
#
#   legal  is this a correct statement of Malaysian law
#   plain  can a person who is not a lawyer actually use this
#
# A non-lawyer's tick must never produce a badge that implies legal review, so
# the two are recorded and displayed separately.

BUNDLES = {
    # ---- legal: the 19 pages split three ways, grouped by area of law ----
    "L1": ("legal", "IP, deals and selling",
           ["release-track", "sync-licence", "someone-used-my-work", "management-deal",
            "exhibit-sell-art", "merch-online"]),
    "L2": ("legal", "Speech, censorship and police",
           ["post-set-online", "arrested", "documentary", "publish-book", "busking", "mural"]),
    "L3": ("legal", "Work, money and organisations",
           ["dj-club-night", "stage-show", "unpaid", "foreign-artist", "run-organisation",
            "brand-deal", "archive"]),
    # ---- plain: the pages a frightened or skint person actually lands on ----
    "P1": ("plain", "Can you follow it: the urgent ones",
           ["arrested", "unpaid", "dj-club-night", "post-set-online", "busking"]),
    # ---- sandboxes, so Raul can see exactly what each track sees ----
    "DEMO-L": ("legal", "DEMO: what the lawyers see",
               ["dj-club-night", "arrested", "release-track"]),
    "DEMO-P": ("plain", "DEMO: what Nick and Marisa see",
               ["dj-club-night", "arrested", "release-track"]),
    "P2": ("plain", "Can you follow it: the deals and selling ones",
           ["merch-online", "someone-used-my-work", "brand-deal", "management-deal",
            "publish-book"]),
}

TITLES = {s["id"]: s["title"] for s in SCENARIOS}
WORDS = {s["id"]: len(s["lede"].split()) + len(s.get("watch", "").split())
         + sum(len(p.split()) for _, _, p in s["steps"]) for s in SCENARIOS}


def main(args):
    if not args:
        raise SystemExit(__doc__)
    assigned, reviewers = {}, {}
    for a in args:
        name, _, code = a.partition("=")
        code = code.strip().upper()
        if code not in BUNDLES:
            raise SystemExit(f"unknown bundle {code!r}; pick from {', '.join(BUNDLES)}")
        if code in assigned:
            raise SystemExit(f"bundle {code} assigned twice")
        assigned[code] = name.strip()
        reviewers[secrets.token_hex(10)] = (name.strip(), code)

    admin_key = secrets.token_hex(12)

    # ---- server-side token map, deployed outside the web root -------------
    php = ["<?php", "// Issued by tools/make_review_links.py. Keep OUTSIDE public_html.",
           "return [", "  'admin_key' => '%s'," % admin_key, "  'pages' => ["]
    for sid in TITLES:
        php.append("    '%s' => %s," % (sid, "'" + TITLES[sid].replace("'", "\\'") + "'"))
    php += ["  ],", "  'reviewers' => ["]
    for tok, (name, code) in reviewers.items():
        track, label, pages = BUNDLES[code]
        php.append("    '%s' => [" % tok)
        php.append("      'name' => '%s'," % name.replace("'", "\\'"))
        php.append("      'bundle' => '%s'," % code)
        php.append("      'track' => '%s'," % track)
        php.append("      'bundle_name' => '%s'," % label)
        php.append("      'pages' => [%s]," % ", ".join("'%s'" % p for p in pages))
        php.append("    ],")
    php += ["  ],", "];", ""]
    (OUT / "_reviewers.php").write_text("\n".join(php), "utf-8")

    # ---- the links and the messages --------------------------------------
    md = ["# Personal review links", "",
          "One link per person. The link is the identity, so do not forward them or post",
          "them in the group; send each one in a direct message. Anyone holding a link can",
          "sign off that person's pages.", "",
          f"Admin view, yours only: `https://alim.my/legislation/review.php?admin={admin_key}`",
          "", "---", ""]
    for tok, (name, code) in reviewers.items():
        track, label, pages = BUNDLES[code]
        words = sum(WORDS[p] for p in pages)
        first = pages[0]
        rate = 70 if track == "legal" else 120      # a lay read is quicker
        mins = round(words / rate) + 2
        md += [f"## {name} — {code}, {label} ({track} track)", "",
               f"{len(pages)} pages, {words:,} words, about {mins} minutes.", "",
               f"**Start here:** {BASE}/{first}/?r={tok}", "",
               "All pages, if they want to jump around:", ""]
        for p in pages:
            md.append(f"- {TITLES[p]} — {BASE}/{p}/?r={tok}")

        if track == "legal":
            body = [
                f"{name}, this is the bit I need your eyes on, as a lawyer. {label}.",
                "",
                f"{BASE}/{first}/?r={tok}",
                "",
                f"{len(pages)} pages, about {mins} minutes. Open it on your phone.",
                "Two buttons at the top of each page. Tap the tick if the page is a correct",
                "statement of the law, or the flag if it is not and type what is wrong. That is",
                "the whole job, and it walks you to the next page after each one.",
                "",
                "The Act numbers and section numbers are already machine-checked against the",
                "Attorney General's Chambers' own text, so ignore those. What needs you is the",
                "plain-English explanation of what each provision actually does.",
                "",
                "It has already been through a hard internal pass that found 86 errors, so you",
                "are the second line, not the first.",
                "",
                "One thing I want to put to you properly rather than assume. Pages that are",
                "cleared can carry the reviewer's name publicly, and I am not going to put yours",
                "on a public statement of Malaysian law without you choosing it. The first page",
                "asks you, once: your name, or just \"a lawyer on the board\" with no name, or no",
                "credit at all. Any of the three is completely fine by me, the review is the",
                "valuable part and the credit is optional, and you can change it later with one",
                "tap. Worth a thought about your firm and your own view on publicity before you",
                "pick. Nothing is published under your name unless you say so.",
            ]
        else:
            body = [
                f"{name}, I need the opposite of a legal opinion on this one. {label}.",
                "",
                f"{BASE}/{first}/?r={tok}",
                "",
                f"{len(pages)} pages, about {mins} minutes. Open it on your phone, the way",
                "someone would if this had just happened to them.",
                "",
                "The lawyers are checking whether it is legally right. What I need from you is",
                "whether it is any use: could you follow it, did you know what to do next, did",
                "anything lose you. Two buttons at the top. Tick if you could follow it, flag if",
                "it lost you, and say where.",
                "",
                "Do not worry about whether the law is correct, that is not your job here and",
                "your tick is not recorded as a legal sign-off. It is recorded separately, as a",
                "plain-English check, and the page says so in those words.",
                "",
                "The first page asks whether you want to be credited by name, as \"an ALIM",
                "director\" without your name, or not at all. Your call entirely, and you can",
                "change it later. Nothing goes up under your name unless you choose it.",
            ]
        md += ["", "**Message to send:**", "", "> " + "\n> ".join(body), "", "---", ""]
    (OUT / "review-links.md").write_text("\n".join(md), "utf-8")

    print(f"  {len(reviewers)} reviewer(s) issued")
    for tok, (name, code) in reviewers.items():
        track, label, pages = BUNDLES[code]
        print(f"    {name:<10} {code}  {track:<6} {len(pages)} pages  token {tok[:6]}…")
    unassigned = [c for c in BUNDLES if c not in assigned]
    if unassigned:
        print(f"  ! bundle(s) {', '.join(unassigned)} not assigned to anyone")
    print(f"\n  wrote {(OUT / 'review-links.md').relative_to(ROOT)}")
    print(f"  wrote {(OUT / '_reviewers.php').relative_to(ROOT)}  <- deploy OUTSIDE public_html")
    print(f"\n  admin view: https://alim.my/legislation/review.php?admin={admin_key}")


if __name__ == "__main__":
    main(sys.argv[1:])
