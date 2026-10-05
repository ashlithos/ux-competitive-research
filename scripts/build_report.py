#!/usr/bin/env python3
"""Build a competitive research report from a template + spec.json.

Usage:
  python3 scripts/build_report.py <report_dir> [--out index.html]

<report_dir> must contain:
  template.html  page with {{placeholders}} (start from templates/report.html)
  spec.json      data for screenshots, charts, sketches and sources
  shots/         screenshots as <key>.webp (see scripts/to_webp.py)

Placeholders the template may use:
  {{shots:key1,key2,...}}  a gallery of screenshot cards (click opens a lightbox)
  {{coverage}}             capability dot grid: products x pillars
  {{heat}}                 heatmap: scope rows x pillars, value = product count
  {{loopmatrix}}           dot matrix: products x loop steps
  {{loopsvg}}              ring diagram of the loop steps
  {{sketch:N}}             the Nth HTML sketch from spec["sketches"]
  {{sourcelist}}           spec["sources_html"]

Cell values in coverage / loop: "f" = shipped (filled dot), "h" = partial or
manual (ring), "n" = none found (dash). Every non-"n" cell needs a tooltip
string that states the fact behind it.
"""
import argparse, collections, html, json, math, os, re, sys

E = html.escape
PILLAR_CLASS = {"u": "cu", "a": "ca", "l": "cl"}


def img_size(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return (1600, 1000)


def card(key, shot, shots_dir):
    w, h = img_size(os.path.join(shots_dir, f"{key}.webp"))
    return (
        f'<figure class="shot" id="s-{key}"><button class="shot-img" type="button" data-full="shots/{key}.webp" '
        f'data-prod="{E(shot["product"])}" data-cap="{E(shot["caption"])}" data-detail="{E(shot.get("detail", ""))}" '
        f'data-src="{E(shot["src"])}" data-stype="{E(shot["source_type"])}" aria-label="Enlarge: {E(shot["product"])}, {E(shot["short"])}">'
        f'<img src="shots/{key}.webp" width="{w}" height="{h}" loading="lazy" alt="{E(shot["caption"])}"></button>'
        f'<figcaption><b>{E(shot["product"])}</b><span class="t">{E(shot["short"])}</span></figcaption></figure>'
    )


def dot_cell(pclass, value, tip, label, tag="td", center=True):
    c = ' class="c"' if center else ""
    if value == "n":
        return f'<{tag}{c}><span class="dot n" aria-label="{label}: none found"></span></{tag}>'
    return (f'<{tag}{c}><span class="dot {value} {pclass} tip" tabindex="0" data-tip="{E(tip)}" '
            f'aria-label="{label}: {E(tip)}"></span></{tag}>')


def build_coverage(spec):
    pillars = spec["pillars"]
    head = "".join(f'<th class="c {p["key"]}-ink">{E(p["name"])}</th>' for p in pillars)
    out = [f'<div class="cov-wrap"><table class="cov"><thead><tr><th>Product</th>{head}</tr></thead><tbody>']
    for g in spec["coverage"]:
        out.append(f'<tr class="grp"><td colspan="{len(pillars) + 1}">{E(g["group"])}</td></tr>')
        for row in g["rows"]:
            cells = "".join(dot_cell(PILLAR_CLASS[p["key"]], v, tip, p["name"])
                            for p, (v, tip) in zip(pillars, row["cells"]))
            out.append(f'<tr><td>{E(row["product"])}</td>{cells}</tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def build_heat(spec):
    pillars = spec["pillars"]
    out = ['<div class="heat" role="table" aria-label="Products by pillar and scope"><div></div>']
    out += [f'<div class="hh {PILLAR_CLASS[p["key"]]}"><i></i>{E(p["name"])}</div>' for p in pillars]
    for name, sub in spec["heat"]["rows"]:
        out.append(f'<div class="rh">{E(name)}<small>{E(sub)}</small></div>')
        for p, products in zip(pillars, spec["heat"]["cells"][name]):
            n = len(products)
            tip = ", ".join(products) if products else "None found"
            out.append(f'<div class="cell {PILLAR_CLASS[p["key"]]} v{min(n, 5)} tip" tabindex="0" data-tip="{E(tip)}" '
                       f'aria-label="{E(name)}, {E(p["name"])}: {n} products. {E(tip)}">{n if n else "—"}</div>')
    out.append("</div>")
    return "".join(out)


def build_loopmatrix(spec):
    names = {p["key"]: p["name"] for p in spec["pillars"]}
    steps = spec["loop"]["steps"]
    out = ['<table class="lm"><thead><tr><th>Product</th>']
    out += [f'<th><small class="{k}-ink">{E(names[k])}</small>{E(s)}</th>' for s, k in steps]
    out.append("</tr></thead><tbody>")
    for row in spec["loop"]["rows"]:
        out.append(f'<tr class="{"ref" if row.get("ref") else ""}"><td>{E(row["name"])}</td>')
        out += [dot_cell(PILLAR_CLASS[k], v, tip, s, center=False) for (v, tip), (s, k) in zip(row["cells"], steps)]
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def build_loopsvg(spec):
    steps = spec["loop"]["steps"]
    n = len(steps)
    cx = cy = 190
    r = 118
    out = [f'<svg viewBox="0 0 380 380" role="img" aria-label="{n}-step loop: {E(", ".join(s for s, _ in steps))}">'
           f'<circle class="lp-ring" cx="{cx}" cy="{cy}" r="{r}"/>']
    step = 360 / n
    for i in range(n):
        a = math.radians(-90 + step * i + step / 2)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        out.append(f'<polygon class="lp-arrow" points="-5,-6 5,0 -5,6" transform="translate({x:.1f},{y:.1f}) rotate({math.degrees(a) + 90:.1f})"/>')
    for i, (s, k) in enumerate(steps):
        a = math.radians(-90 + step * i)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if abs(math.cos(a)) < 0.3:
            anchor, lx = "middle", cx + (r + 40) * math.cos(a)
        else:
            anchor, lx = ("start" if math.cos(a) > 0 else "end"), cx + (r + 30) * math.cos(a)
        ly = cy + (r + 40) * math.sin(a)
        out.append(f'<g class="lp-node {k}"><circle cx="{x:.1f}" cy="{y:.1f}" r="20"/><text x="{x:.1f}" y="{y:.1f}">{i + 1}</text></g>')
        out.append(f'<text class="lp-lab" x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="{anchor}">{E(s)}</text>')
    center = spec["loop"].get("center", ["Feedback", "→ shared context"])
    out.append(f'<text class="lp-c1" x="{cx}" y="{cy - 4}">{E(center[0])}</text><text class="lp-c2" x="{cx}" y="{cy + 16}">{E(center[1])}</text></svg>')
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report_dir")
    ap.add_argument("--out", default="index.html")
    args = ap.parse_args()
    d = args.report_dir
    spec = json.load(open(os.path.join(d, "spec.json"), encoding="utf-8"))
    t = open(os.path.join(d, "template.html"), encoding="utf-8").read()
    shots_dir = os.path.join(d, "shots")

    used = []

    def gallery(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        missing = [k for k in keys if k not in spec["shots"]]
        if missing:
            sys.exit(f"Unknown screenshot keys: {missing}")
        used.extend(keys)
        return '<div class="gal">' + "".join(card(k, spec["shots"][k], shots_dir) for k in keys) + "</div>"

    t = re.sub(r"\{\{shots:([^}]+)\}\}", gallery, t)
    t = re.sub(r"\{\{sketch:(\d+)\}\}", lambda m: spec["sketches"][int(m.group(1))], t)
    if "coverage" in spec: t = t.replace("{{coverage}}", build_coverage(spec))
    if "heat" in spec: t = t.replace("{{heat}}", build_heat(spec))
    if "loop" in spec:
        t = t.replace("{{loopmatrix}}", build_loopmatrix(spec)).replace("{{loopsvg}}", build_loopsvg(spec))
    t = t.replace("{{sourcelist}}", spec.get("sources_html", ""))

    out_path = os.path.join(d, args.out)
    open(out_path, "w", encoding="utf-8").write(t)

    # checks
    ids = re.findall(r'id="([^"]+)"', t)
    dups = [i for i, c in collections.Counter(ids).items() if c > 1]
    broken = sorted(h for h in set(re.findall(r'href="#([^"]+)"', t)) if h not in ids)
    left = re.findall(r"\{\{[^}]+\}\}", t)
    unused = sorted(set(spec["shots"]) - set(used))
    print(f"wrote {out_path} ({len(t) // 1024} KB) · {len(used)} screenshots")
    for label, val in [("duplicate ids", dups), ("broken #anchors", broken), ("unfilled placeholders", left), ("unused screenshots", unused)]:
        if val:
            print(f"WARN {label}: {val}")


if __name__ == "__main__":
    main()
