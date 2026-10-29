---
name: generate-alt-text
description: Generate context-aware alt text for website images, icons, and logos from visible assets and their usage context. Use when preparing media or updating image accessibility in any subject area.
---

# Generate image alt text

Inspect every supplied image with an available image-viewing tool. Create a temporary preview
when needed, preserving enough detail to identify the subject. Do not infer visual content
from filenames alone; request an accessible image if it cannot be inspected.

Use the requested language; otherwise use the page's language. If neither is known, ask for
the language before producing final text. Follow an established editorial style when supplied.

- Describe the information the image contributes in its actual page context, concisely.
- For linked or actionable images, describe the action or destination rather than appearance alone.
- Use an empty string for purely decorative images or images whose information is fully
  duplicated by adjacent text. Do not treat every icon as decorative.
- Include visible text when it is essential to the image's purpose. For complex charts or
  diagrams, provide a short identification and flag the need for an adjacent detailed description.
- Do not begin with redundant phrases such as “image of” or “photo of”.
- Do not invent identities, procedures, locations, brands, or unseen details. Use supplied
  context to clarify meaning, without making unsupported visual claims.
- For logos, identify the visible brand and its role; for controls, prioritize the accessible function.
- If decorative versus informative use is unclear and changes the answer, ask for usage context.

Unless the user requests another format, return one JSON object. Use each base filename
without its extension as the key; use supplied identifiers or relative paths if keys collide:

```json
{"example": "Concise contextual description", "decorative-divider": ""}
```

Remove only temporary previews created for this task.
