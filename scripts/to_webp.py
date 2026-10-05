#!/usr/bin/env python3
"""Convert chosen screenshots to web-sized WebP files named by key.

Usage:
  python3 scripts/to_webp.py shots/ key1=path/to/img1.png key2=raw/img2.bin ...

Resizes to at most 1800px wide (quality 84). Animated GIFs keep frame 0;
crop or pick a frame first with extract_frames.py. Keys become the ids used
in spec.json and in {{shots:...}} placeholders, e.g. "confluence-summary".
"""
import os
import sys

from PIL import Image


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    total = 0
    for pair in sys.argv[2:]:
        key, path = pair.split("=", 1)
        im = Image.open(path)
        im.seek(0)
        im = im.convert("RGB")
        if im.width > 1800:
            im = im.resize((1800, int(im.height * 1800 / im.width)), Image.LANCZOS)
        out = os.path.join(outdir, f"{key}.webp")
        im.save(out, "WEBP", quality=84, method=6)
        size = os.path.getsize(out)
        total += size
        print(f"{key}: {im.size} {size // 1024} KB")
    print(f"total {total // 1024} KB")


if __name__ == "__main__":
    main()
