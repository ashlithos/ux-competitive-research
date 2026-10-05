---
name: ux-competitive-research
description: Turn a UX or product question into a sourced competitive research report, published as one HTML page with real product screenshots, charts, design principles, sketches and open questions. Use when a designer or PM asks "how are other products solving X", wants a competitive landscape, interaction patterns, CUJs, or screenshots of competitors' workflows.
---

# UX competitive research report

Produces a five-chapter HTML page that a designer can scan in minutes and
share with a team:

1. **Overview** – the framework, short answers, the evidence chart, a capability grid
2. **Competitive landscape** – facts only, split by framework pillar: CUJs, patterns, who ships what, real screenshots
3. **Principles & explorations** – interpretation: principles, a loop/framework diagram, sketches, opportunities
4. **Open questions** – decisions ahead + what the research couldn't verify
5. **Sources**

The worked example in `examples/comments-at-scale/` is the reference output.
Open `examples/comments-at-scale/index.html` before starting.

## Rules that shaped this format

These came from real review rounds. Follow them unless the user says otherwise.

- **Organize by the user's framework.** Ask for it, or propose 3 pillars (e.g.
  Understand / Act / Learn) and confirm. Every pattern, chart column and
  opportunity is tagged with a pillar and keeps that pillar's color.
- **Facts and interpretation never mix.** Chapter 2 holds only sourced facts and
  screenshots. Design notes, principles, sketches and opinions live in chapter 3.
  Caption lines describe what is on screen, not what it means.
- **Real screenshots over mockups.** A designer wants to see the product. Pull
  them from docs, changelogs, blogs, help-center GIFs, launch videos and press.
  Label anything that isn't the vendor's own docs (press, video frame).
- **Less text, more charts, more space.** One line per product fact. Screenshot
  cards show product + a 3–6 word title; the full caption, a factual "Detail"
  line and the source live in the lightbox. Sections get ~56px vertical padding
  and a ~640px reading measure.
- **Charts carry the argument** (see `references/charts.md`): an evidence bar
  chart, a product × pillar capability grid, a scope × pillar heatmap, and a
  loop-coverage dot matrix. Every mark has a hover tooltip stating its fact.
- **Typography:** Google Sans / Google Sans Text / Google Sans Code from Google
  Fonts (all three are served there), unless the user names another face.
- **Navigation:** sticky numbered chapter tabs; chapter 2 has a segmented
  control per pillar; every hash (`#learn`, `#s-hex-diff`) deep-links.
- **Honesty:** say which dots are your reading of public docs; list what you
  couldn't find in chapter 4 instead of filling gaps.

## Procedure

1. **Frame (ask first).** Confirm the question, the framework pillars, the
   audience, and the special lens (e.g. "data analytics"). Ask 1–3 sharp
   questions if any are unclear; don't start the build before the framing is
   settled.
2. **Research.** Web search for: evidence the problem is real (metrics, forum
   requests, launches), then each candidate product's docs/changelog. Record
   every claim with its URL. Aim for 15–25 products across 4–6 categories.
3. **Map.** For each product decide per pillar: shipped with AI (`f`), basic or
   manual (`h`), none found (`n`), with a one-line fact as the tooltip. Group
   features into 2–3 patterns per pillar and write one CUJ per pattern in the
   user's voice ("40 comments. What's unresolved?").
4. **Collect screenshots** (`references/screenshots.md`):
   `scripts/scrape_images.py URL...` → download candidates →
   `scripts/extract_frames.py` for GIFs/videos → review with
   `scripts/contact_sheet.py` (one image read per 12 candidates) → keep shots that
   show the actual interaction → `scripts/to_webp.py`.
5. **Write spec.json** in a new report folder: `shots` (product, scope,
   caption, detail, short, src, source_type), `pillars`, `coverage`, `heat`,
   `loop`, `sketches`, `sources_html`. Copy the example's spec as a starting shape.
6. **Write template.html** by copying `templates/report.html` and replacing the
   text content: chapter heroes, CUJs, one-line "who" facts, principles,
   opportunities, questions. Keep the `{{placeholders}}` and the CSS tokens.
   See `references/report-structure.md` for text budgets.
7. **Build:** `python3 scripts/build_report.py <report_dir>`; fix any WARN lines
   (broken anchors, unused shots, unfilled placeholders).
8. **Check once:** render at 1280px and 400px (Playwright), confirm no
   horizontal scroll, charts readable in light and dark, then publish or hand
   over the folder (index.html + shots/).

## Files

| Path | What |
|---|---|
| `templates/report.html` | Page template: CSS tokens (light/dark), tabs, chart styles, lightbox, router |
| `scripts/build_report.py` | Fills placeholders from spec.json; prints integrity warnings |
| `scripts/scrape_images.py` | Lists screenshot candidates on any docs/blog page |
| `scripts/extract_frames.py` | Frames from GIF/MP4 for interactions only shown in motion |
| `scripts/contact_sheet.py` | Tiles candidates into one image for fast visual review |
| `scripts/to_webp.py` | Resizes and converts chosen shots to `shots/<key>.webp` |
| `references/report-structure.md` | Chapter-by-chapter content and text budgets |
| `references/screenshots.md` | Where screenshots hide, and caption rules |
| `references/charts.md` | The four chart types, palette, tooltips |
| `examples/comments-at-scale/` | Full worked example (spec, template, built page, 49 shots) |
