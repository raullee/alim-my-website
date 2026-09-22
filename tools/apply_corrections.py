# -*- coding: utf-8 -*-
"""
Apply panel corrections to tools/scenarios.py.

  python3 tools/apply_corrections.py review/panel-ip.md [more panels...]
  python3 tools/apply_corrections.py --dry-run review/panel-*.md

Each panel report lists corrections in a fixed shape:

    ### [claim-id]
    - WRONG: the phrase that is wrong
    - WHY: the reasoning
    - REPLACE WITH: the drop-in replacement, publication ready

`claim-id` is either `scenario-id#NN` for a step, or `scenario-id — WATCH-CLAIM`
/ `scenario-id — LEDE` for the scenario's own prose.

Rewriting is done through the AST rather than by find and replace: each step's
point is a run of adjacent string literals across several lines, and a textual
replace on that is how you silently corrupt the file. We locate the exact source
span of the literal and swap it, so anything the panel did not touch is left
byte-identical.
"""
import argparse
import ast
import pathlib
import re
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "tools" / "scenarios.py"

# Panels write headings three different ways, so accept all of them:
#   ### [dj-club-night#13] and [busking#03] and [stage-show#12]
#   ### [management-deal#03] and [unpaid#06]: Stamp Act curability stated backwards
#   ### `tools/scenarios.py` :: `arrested` step06 (act-15)
#   ### `tools/scenarios.py` :: `documentary`.watch
HEADING = re.compile(r"^###[ \t]+(.+?)[ \t]*$", re.M)
BRACKET = re.compile(r"\[([a-z][a-z0-9-]*)\s*(?:#(\d+)|[\u2014-]{1,2}\s*(WATCH-CLAIM|LEDE))\]", re.I)
BACKTICK = re.compile(r"`([a-z][a-z0-9-]*)`\s*(?:step\s*(\d+)|\.(watch|lede))", re.I)
# "- REPLACE WITH:" / "- **BETTER:**" / "- REPLACE WITH (2):" and, where one
# block corrects several claims differently, "- REPLACE WITH (management-deal#01):"
REPL = re.compile(r"^[-*]\s*(?:\*\*)?(?:REPLACE WITH|BETTER)(?:\s*\(([^)]*)\))?(?:\*\*)?\s*:\s*(.*?)"
                  r"(?=\n[-*]\s*(?:\*\*)?(?:REPLACE WITH|BETTER|WRONG|WHY|RISK|PROBLEM|"
                  r"NOW|CLAIM|NOTE|FIX|STRUCTURAL)\b|\n###|\n##|\Z)",
                  re.S | re.M)


def claims_in(heading, valid):
    """Every scenario claim a heading refers to, in either notation."""
    out = []
    for m in BRACKET.finditer(heading):
        sid = m.group(1).lower()
        if sid in valid:
            out.append((sid, int(m.group(2)) if m.group(2) else (m.group(3) or "").upper()))
    for m in BACKTICK.finditer(heading):
        sid = m.group(1).lower()
        if sid not in valid:
            continue
        if m.group(2):
            out.append((sid, int(m.group(2))))
        else:
            out.append((sid, "WATCH-CLAIM" if m.group(3).lower() == "watch" else "LEDE"))
    return out


def parse_panel(path, valid=None):
    """Pull (scenario_id, step_no|kind, replacement) out of one panel report."""
    if valid is None:
        import scenarios
        valid = {s["id"] for s in scenarios.SCENARIOS}
    text = pathlib.Path(path).read_text("utf-8")
    # Advisory sections are not applied; only sections that ask for a change are.
    blocks = []
    for name in ("## CORRECTIONS REQUIRED", "## SENTENCES TO SIMPLIFY",
                 "## MISLEADING TO A LAY READER"):
        i = text.find(name)
        if i < 0:
            continue
        j = len(text)
        for m in re.finditer(r"^## ", text[i + 4:], re.M):
            j = min(j, i + 4 + m.start())
        blocks.append(text[i:j])
    if not blocks:
        return []

    out, unlabelled = [], []
    for body in blocks:
        heads = list(HEADING.finditer(body))
        for i, h in enumerate(heads):
            seg = body[h.end():(heads[i + 1].start() if i + 1 < len(heads) else len(body))]
            targets = claims_in(h.group(1), valid)
            if not targets:
                continue
            reps = REPL.findall(seg)
            if not reps:
                continue

            def clean(t):
                t = " ".join(t.split()).strip().strip("`").strip().strip('"').strip()
                # an instruction to a human, not text to paste
                if not t or re.match(r"^(hold|see |as above|same as)\b", t, re.I):
                    return None
                return t

            # a block may carry one replacement per claim, tagged in brackets
            tagged = {}
            for label, body_text in reps:
                for m in BRACKET.finditer("[%s]" % label.strip()) if label else []:
                    tagged[(m.group(1).lower(),
                            int(m.group(2)) if m.group(2) else (m.group(3) or "").upper())] = body_text
            for sid, key in targets:
                if tagged:
                    if (sid, key) not in tagged:
                        unlabelled.append(f"{sid}#{key} ({pathlib.Path(path).name})")
                        continue
                    t = clean(tagged[(sid, key)])
                else:
                    t = clean(reps[-1][1])
                if t:
                    out.append((sid, key, t, pathlib.Path(path).name))
    if unlabelled:
        print(f"  ~ {pathlib.Path(path).name}: no replacement text supplied for "
              + ", ".join(unlabelled))
    return out


def literal_span(node):
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def find_targets(src):
    """Map (scenario_id, key) -> source span of the string literal to replace."""
    tree = ast.parse(src)
    spans = {}
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign)
                and any(getattr(t, "id", None) == "SCENARIOS" for t in node.targets)):
            continue
        for call in node.value.elts:                      # each dict(...) call
            kw = {k.arg: k.value for k in call.keywords}
            sid = ast.literal_eval(kw["id"])
            for kind in ("watch", "lede"):
                if kind in kw:
                    spans[(sid, kind.upper() + ("-CLAIM" if kind == "watch" else ""))] = \
                        literal_span(kw[kind])
            spans[(sid, "WATCH-CLAIM")] = spans.get((sid, "WATCH-CLAIM"))
            for i, step in enumerate(kw["steps"].elts, 1):
                spans[(sid, i)] = literal_span(step.elts[2])
    return {k: v for k, v in spans.items() if v}


def as_literal(text, indent):
    """Re-emit as adjacent string literals wrapped to the file's column style."""
    body = text.replace("\\", "\\\\").replace('"', '\\"')
    lines = textwrap.wrap(body, width=max(40, 96 - indent - 2),
                          break_long_words=False, break_on_hyphens=False)
    pad = " " * indent
    return ("\n" + pad).join(f'"{l}{" " if n < len(lines) - 1 else ""}"'
                             for n, l in enumerate(lines))


def apply(corrections, dry_run=False):
    src = TARGET.read_text("utf-8")
    spans = find_targets(src)
    lines = src.split("\n")

    # offsets into the flat text, so replacements can be made back to front
    starts = []
    pos = 0
    for l in lines:
        starts.append(pos)
        pos += len(l) + 1

    edits, missing = [], []
    for sid, key, new, panel in corrections:
        span = spans.get((sid, key))
        if not span:
            missing.append(f"{sid}#{key} ({panel})")
            continue
        l1, c1, l2, c2 = span
        a = starts[l1 - 1] + c1
        b = starts[l2 - 1] + c2
        edits.append((a, b, as_literal(new, c1), f"{sid}#{key}", panel))

    edits.sort(key=lambda e: -e[0])
    seen = set()
    applied = []
    for a, b, lit, label, panel in edits:
        if label in seen:            # two panels touching one claim: first wins
            print(f"  ! {label}: already corrected by an earlier panel, skipped")
            continue
        seen.add(label)
        old = src[a:b]
        if not dry_run:
            src = src[:a] + lit + src[b:]
        applied.append((label, panel, len(old), len(lit)))

    if not dry_run:
        ast.parse(src)               # refuse to write a file that will not import
        TARGET.write_text(src, "utf-8")

    for label, panel, o, n in sorted(applied):
        print(f"  {'would fix' if dry_run else 'fixed'}  {label:<28} {panel}")
    if missing:
        print("\n  UNMATCHED claim ids (check the panel report wording):")
        for m in missing:
            print("   !", m)
    print(f"\n  {len(applied)} correction(s) {'previewed' if dry_run else 'applied'}, "
          f"{len(missing)} unmatched")
    return len(missing)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("panels", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    all_c = []
    for p in args.panels:
        c = parse_panel(p)
        print(f"{pathlib.Path(p).name}: {len(c)} correction(s)")
        all_c += c
    print()
    sys.exit(1 if apply(all_c, args.dry_run) else 0)
