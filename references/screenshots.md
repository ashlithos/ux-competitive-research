# Finding real product screenshots

## Where they are
| Source | Notes |
|---|---|
| Official docs / help centers | Best captions (alt text is often a full description). Docusaurus sites use unquoted `src=`; Atlassian embeds Contentful URLs as `src='//images.ctfassets.net/…'` inside JSON; Intercom help centers sign URLs, so download right away. |
| Changelogs | Usually one crisp hero screenshot per feature (Cursor, GitHub, Vercel). |
| Product / solution pages | Marketing renders, still real UI (Figma, Hex). |
| Help-center GIFs | Show interactions no still does. Pull frames with `extract_frames.py`. |
| Blog videos (MP4) | Hex-style launch posts often hold the most important flow; extract several frames, keep the sharpest. |
| YouTube | `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`. Often a title card; only keep it if it shows UI. |
| Press | Android Authority, Office Watch, Tom's Guide have real screenshots of new launches. Label as press. |

Some docs render images client-side only (e.g. Snowflake). If nothing turns up,
say so in chapter 4 rather than substituting a mockup.

## Review loop
1. Download all candidates into `raw/`.
2. `contact_sheet.py sheet.jpg raw/*` in batches of 12, read each sheet once.
3. Drop logos, title cards, illustrations and blurry frames.
4. For GIFs/videos, extract 5–6 frames, sheet them, crop the best one.
5. Keep shots that show the actual interaction the pattern describes.

## Captions
- `short`: 3–6 words, what the screen shows ("Comment summary with citation chips").
- `caption`: one sentence describing the UI, verified against the image.
- `detail`: one factual observation a designer would notice ("Every bullet ends
  in numbered citation chips"). No advice, no "this is the best example of".
- `source_type`: "Docs screenshot", "Changelog image", "Frame from blog video",
  "Press screenshot · <outlet>".
- Re-read any number or label in the image before quoting it.
