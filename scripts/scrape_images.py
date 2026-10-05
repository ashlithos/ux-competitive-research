#!/usr/bin/env python3
"""List screenshot candidates on product docs, changelogs and blog pages.

Usage:
  python3 scripts/scrape_images.py URL [URL ...]

Prints, per page: <img> sources with alt text, og:image, YouTube ids
(thumbnail: https://i.ytimg.com/vi/<id>/maxresdefault.jpg) and GIF/MP4 media.

Handles unquoted src attributes (Docusaurus/Databricks) and protocol-relative
Contentful URLs (Atlassian). Pages that render images with JavaScript only
(e.g. some Snowflake docs) show nothing; look for a blog, video or press piece.
"""
import html
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
SKIP = re.compile(r"logo|avatar|favicon|badge|gravatar|\.svg|pixel\?", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.geturl(), r.read().decode("utf-8", "ignore")


def main(urls):
    for url in urls:
        try:
            final, page = fetch(url)
        except Exception as e:  # noqa: BLE001
            print("ERR", url, e)
            continue
        print("==", url, "->", final)
        seen = set()
        for tag in re.findall(r"<img\b[^>]*>", page, re.I):
            m = re.search(r"\b(?:src|data-src)=[\"']?([^\"'\s>]+)", tag)
            if not m or m.group(1).startswith("data:"):
                continue
            src = urllib.parse.urljoin(final, html.unescape(m.group(1)))
            alt = re.search(r"\balt=\"([^\"]*)\"", tag)
            alt = html.unescape(alt.group(1)) if alt else ""
            if src in seen or (SKIP.search(src) and not alt):
                continue
            seen.add(src)
            print("  IMG", src, "|", alt[:140])
        for src in sorted(set(re.findall(r"src='(//images\.ctfassets\.net/[^']+)'", page))):
            print("  IMG", "https:" + src)
        for m in sorted(set(re.findall(r"(?:og:image|twitter:image)\"\s+content=\"([^\"]+)\"", page))):
            print("  OG ", html.unescape(m))
        for m in sorted(set(re.findall(r"(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([\w-]{11})", page))):
            print("  YT ", m, f"https://i.ytimg.com/vi/{m}/maxresdefault.jpg")
        for m in sorted(set(re.findall(r"\"(https?://[^\"]+\.(?:gif|mp4|webm))\"", page))):
            print("  MEDIA", m)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
