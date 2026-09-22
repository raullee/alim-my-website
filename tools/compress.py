# -*- coding: utf-8 -*-
"""Downsample the handful of AGC files that are high-DPI scans.

AGC's consolidated PDFs are small and born-digital, but a few Acts are only
available as CamScanner scans: Act 135 ships at 13.8 MB for 20 pages. Those
pages are images, so re-encoding them at screen resolution costs nothing a
reader will notice and keeps the deployment light.
"""
import pathlib
import sys

import fitz

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = float(sys.argv[1]) if len(sys.argv) > 1 else 4e6
TARGET_DPI = 150

total_before = total_after = 0
for pdf in sorted((ROOT / "legislation" / "pdf").glob("*.pdf")):
    size = pdf.stat().st_size
    if size < LIMIT:
        continue
    doc = fitz.open(pdf)
    if sum(len(doc.load_page(i).get_text()) for i in range(min(doc.page_count, 10))) > 500:
        doc.close()
        continue                      # has real text; leave it alone
    out = fitz.open()
    for i in range(doc.page_count):
        page = doc.load_page(i)
        scale = min(1.0, TARGET_DPI / 300.0)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale * 2, scale * 2))
        np = out.new_page(width=page.rect.width, height=page.rect.height)
        np.insert_image(np.rect, stream=pix.tobytes("jpeg", jpg_quality=72))
    tmp = pdf.with_suffix(".tmp.pdf")
    out.save(tmp, deflate=True, garbage=4)
    out.close(); doc.close()
    new = tmp.stat().st_size
    if new < size:
        tmp.replace(pdf)
        print(f"  {pdf.name}: {size/1e6:.1f} -> {new/1e6:.1f} MB")
        total_before += size; total_after += new
    else:
        tmp.unlink()
        print(f"  {pdf.name}: no gain, kept original")
if total_before:
    print(f"  saved {(total_before-total_after)/1e6:.1f} MB")
