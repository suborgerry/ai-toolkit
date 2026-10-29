---
name: check-figma-assets
description: Visually compare prepared website images with Figma section or component references. Use to check crops, orientation, backgrounds, content assignment, transparency, and rendering artifacts before delivery or media import.
---

# Check prepared assets against Figma

Match each supplied asset to its reference using the supplied mapping or design context.
Do not guess ambiguous matches; report them as errors or request the missing reference.

For each pair:

1. Inspect the asset and reference with an available image-viewing tool. Create temporary
   previews when needed, but keep enough resolution to judge the relevant details.
2. Compare orientation and mirroring, crop, subject placement, edge bars, frames, neighboring
   fragments, background color, component assignment, blur, broken pixels, and transparency.
3. Distinguish defects in the file from cropping or backgrounds supplied by the page's CSS.
   Compare the intended rendered result when that context is available.
4. For edge, alpha, or pixel-level doubts, inspect the original at full resolution and use
   available image metadata or image-processing tools. Do not require a particular OS or converter.
5. Remove only temporary previews created for this check. Do not modify source assets unless asked.

Unless the user requests another format, return one JSON object keyed by the supplied asset
identifier (use relative paths if filenames collide):

```json
{
  "images/example.webp": {
    "verdict": "ok",
    "issues": []
  }
}
```

Use `mismatch` with concise issue strings for discrepancies, or `error` when an asset or
reference cannot be inspected. Do not report an uninspected pair as `ok`.
