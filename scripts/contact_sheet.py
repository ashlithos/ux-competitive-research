#!/usr/bin/env python3
"""Tile many images into one labelled contact sheet so an agent can review
dozens of screenshot candidates in a single image read.

Usage:
  python3 scripts/contact_sheet.py out.jpg img1 img2 ... [--cols 3]

Each tile shows the file name and original pixel size. Animated GIFs show
frame 0; use extract_frames.py to pull later frames.
"""
import argparse
import os

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--tile", type=int, nargs=2, default=(520, 340))
    a = ap.parse_args()
    w, h = a.tile
    rows = (len(a.images) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * w, rows * (h + 24)), "white")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(a.images):
        try:
            im = Image.open(path)
            size = im.size
            im.seek(0)
            im = im.convert("RGB")
        except Exception:  # noqa: BLE001
            continue
        im.thumbnail((w - 10, h - 10))
        x, y = (i % a.cols) * w, (i // a.cols) * (h + 24)
        sheet.paste(im, (x + 5, y + 5))
        draw.text((x + 5, y + h + 4), f"{os.path.basename(path)}  {size}", fill="black")
    sheet.save(a.out, quality=80)
    print("wrote", a.out, sheet.size)


if __name__ == "__main__":
    main()
