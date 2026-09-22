# -*- coding: utf-8 -*-
"""
Drop locally hosted PDFs that are too big to serve, and fall back to AGC.

  python3 tools/prune_oversize.py [max_mb]

Most AGC consolidations are born-digital and small. A few are photographic
scans that survive compression: the English Criminal Procedure Code is 102 MB
and still 75 MB after downsampling, which is more than the rest of the library
put together and is not something to put on a phone on a 4G connection.

For those, the page keeps the entry and the link but sends the reader to AGC
rather than serving the file. Run after tools/compress.py.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "legislation" / "data" / "library.json"
CAP = float(sys.argv[1] if len(sys.argv) > 1 else 12) * 1e6

lib = json.loads(LIB.read_text("utf-8"))
dropped, freed = [], 0

for entry in lib["entries"]:
    for lang, meta in entry["pdf"].items():
        rel = meta.get("local")
        if not rel:
            continue
        f = ROOT / rel.lstrip("/")
        if not f.exists():
            meta.pop("local", None)
            continue
        size = f.stat().st_size
        if size <= CAP:
            meta["bytes"] = size
            continue
        if not meta.get("remote"):
            print(f"  ! {entry['id']} {lang}: oversize but no AGC link to fall back to; keeping")
            continue
        f.unlink()
        meta.pop("local", None)
        meta.pop("bytes", None)
        meta["oversize"] = True
        dropped.append((entry["short"], lang, size))
        freed += size

LIB.write_text(json.dumps(lib, ensure_ascii=False, indent=1), "utf-8")

for short, lang, size in dropped:
    print(f"  not hosted: {short} [{lang}] {size/1e6:.0f} MB, links to AGC instead")
total = sum(m.get("bytes", 0) for e in lib["entries"] for m in e["pdf"].values())
print(f"\n  {len(dropped)} file(s) dropped, {freed/1e6:.0f} MB freed; "
      f"library now hosts {total/1e6:.0f} MB")
