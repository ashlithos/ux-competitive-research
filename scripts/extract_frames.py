#!/usr/bin/env python3
"""Pull still frames from a GIF or video. Help-center GIFs and launch videos
often show the exact interaction that no static screenshot does (for example
a comment summary appearing, or a review agent's suggestion feed).

Usage:
  python3 scripts/extract_frames.py input.(gif|mp4|webm) outdir [--at 0.2 0.5 0.8]

--at takes fractions of the duration. Motion blur is common mid-transition,
so take several frames and keep the sharpest one. MP4/WebM needs ffmpeg.
"""
import argparse
import os
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("outdir")
    ap.add_argument("--at", type=float, nargs="+", default=[0.2, 0.35, 0.5, 0.65, 0.8, 0.95])
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.input))[0]
    if a.input.lower().endswith(".gif"):
        from PIL import Image
        im = Image.open(a.input)
        n = getattr(im, "n_frames", 1)
        for f in a.at:
            k = min(n - 1, int(n * f))
            im.seek(k)
            out = os.path.join(a.outdir, f"{base}_{f:.2f}.png")
            im.convert("RGB").save(out)
            print(out)
        return
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.input]).strip())
    for f in a.at:
        out = os.path.join(a.outdir, f"{base}_{f:.2f}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(dur * f), "-i", a.input,
                        "-frames:v", "1", out], check=True)
        print(out)


if __name__ == "__main__":
    main()
