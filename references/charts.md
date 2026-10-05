# Charts

All charts are plain HTML/CSS/SVG built by `build_report.py` (no chart library).
Every mark is focusable and has a `data-tip` tooltip that states its fact.

| Chart | Placeholder | Use it for |
|---|---|---|
| Evidence bars | hand-written in the template | 4–6 metrics from one strong source; highlight the ones that make the point, gray the rest |
| Capability grid | `{{coverage}}` | products × pillars; filled dot = shipped with AI, ring = basic/manual, dash = none found |
| Scope heatmap | `{{heat}}` | scope rows (thread → workspace) × pillars; cell = product count, tooltip lists them |
| Loop coverage | `{{loopmatrix}}` | products × steps of the feedback loop; reveals the empty column |
| Loop ring | `{{loopsvg}}` | the same steps as a diagram, colored by pillar |

## Palette
Pillar hues are a validated 3-slot categorical palette. Marks use `--u/--a/--l`;
text uses the `-ink` variants so labels stay readable in dark mode.

| Token | Light | Dark (marks) | Dark (text) |
|---|---|---|---|
| Understand | `#1A5FC8` | `#5B93E8` | `#8AB4F8` |
| Act | `#B45309` | `#C97A22` | `#F0B36A` |
| Learn | `#137A4B` | `#3FA874` | `#7DD3A7` |

Light mode's amber/green pair sits in the 6–8 CVD band, so every dot also
differs by shape (filled vs ring) and every column is labelled. If you change
hues, re-validate both modes (OKLab ΔE ≥ 8 between adjacent slots, lightness
inside the band for the surface).

## Rules
- One axis, single hue per series; emphasis by highlight, not extra colors.
- Text never takes a series color on a light mark; values stay in ink.
- The headline above each chart states the takeaway in words.
- Every number in a chart is traceable to a source in the chart footer or tooltip.
