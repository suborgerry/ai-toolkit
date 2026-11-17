---
name: new-page-by-existing
description: Adapt an existing or cloned WordPress page to supplied Figma designs and content using the site's existing templates and fields. Use when populating a specific page while preserving its WordPress and ACF conventions.
---

# Adapt an existing WordPress page from Figma

## Establish scope and access

Identify the target site, existing page ID or URL, design frames, supplied content, and requested
changes. Confirm the target if multiple sites or pages match. Ask only for missing inputs that
block the requested work; continue independent inspection where possible.

Treat page title, slug, SEO, FAQ, and publication status as separate requested changes, not
mandatory inputs for every task. Preserve existing values when they are outside scope. Do not
invent missing copy; ask for it when required, or use placeholders only when authorized.

Use the site's available WordPress connector, authenticated admin interface, or WP-CLI.
Discover the actual document root, runtime, and credentials through the environment's supported
configuration. Do not assume a local host, OS, theme name, database socket, or PHP version.
For Local, containers, or remote hosts, use that environment's configured shell or CLI entrypoint.
Investigate runtime warnings when they affect command success or output; do not silently discard them.

## Inspect the page and schema

1. Read the target page, status, template, content, metadata, and relevant media before editing.
   With WP-CLI, `wp post get <ID> --format=json` and `wp post meta list <ID> --format=json`
   can provide this context. Keep a recoverable snapshot of values being changed.
2. Determine whether the page uses ACF, blocks, another builder, or ordinary post content.
   Follow the existing mechanism; do not assume a flexible-content field named `content`.
3. For ACF, inspect field-group definitions, field keys, layout names, nested repeaters, and
   template rendering. Derive column options, conditional fields, and hover behavior from
   the actual schema and implementation rather than copying another project's conventions.
4. Reuse existing sections and templates where they support the design. Identify any layout
   that cannot be represented and resolve that limitation before writing incompatible data.

## Read the design

Use an available Figma integration or supplied exports. Follow integration guidance when provided.
Request the main frame and inspect dense components or variants separately when necessary.
Confirm section order, card order, responsive states, and hover content against screenshots.
Preserve intentional line breaks only in a form supported by the target field and renderer.
If the design cannot be accessed, request the missing reference rather than claiming fidelity.

## Prepare media

- Reuse identical existing library assets and icons when appropriate.
- Choose the export that reproduces the intended result: a raw asset when the template supplies
  its crop and effects, or a composed node when those effects belong in the exported image.
- Select raster dimensions, format, and compression based on rendered size, display density,
  transparency, and site conventions. Preserve SVGs where supported and appropriate.
- Use existing conversion tooling when available; do not assume a `Converter/` directory,
  package manager, or fixed export scale. Keep temporary files in a task-specific directory.
- Compare prepared images with the design, including crop, orientation, edges, and backgrounds.
  If available, the `ai-toolkit:check-figma-assets` skill supports this check; otherwise perform it directly.
- Generate alt text from the visible image, page language, and usage context. If available,
  use the `ai-toolkit:generate-alt-text` skill; otherwise apply contextual accessibility guidance directly.
- Import through the supported media workflow and record attachment IDs. With WP-CLI,
  `wp media import <file> --porcelain` returns the ID; set the title and alt text as needed.
- Do not delete replaced attachments unless deletion is in scope and their reuse has been checked.
  Remove only temporary files created for this task.

## Update the page

- Use the site's supported content APIs. For ACF, prefer `update_field` with verified field
  keys for new values and structured arrays for repeaters and flexible content so ACF manages
  references and row counts. If direct metadata changes are necessary, preserve the verified
  schema and remove only obsolete values belonging to the requested update.
- For scripted bulk updates, put structured content in a file and use an appropriate API or
  `wp eval-file`; avoid interpolating quoted or multiline copy into shell commands.
- Update title, slug, FAQ, and SEO only as requested. Discover the active SEO plugin and its
  supported storage or API; do not assume Yoast. Preserve supplied copy exactly.
- Preserve publication and indexing status unless changing them is requested. A content update
  alone does not authorize publishing a draft or removing `noindex`.

## Verify

Read back saved values and inspect the rendered target page, using an authenticated preview
for drafts or private pages. Check:

1. The intended URL loads successfully, and redirects or canonical URLs match the requested slug.
2. Changed headings, cards, FAQ, and other content match the supplied material.
3. New media load with the intended crops, orientation, and contextual alt attributes.
4. Layout and relevant responsive or interactive states match the available design references.
5. Changed SEO fields render correctly, while publication and indexing settings match scope.
6. Replaced sections contain no unintended donor-page copy.

### Compare each clone with its own frames

A clone inherits the donor's styles and settings, so it can look right and still be wrong. For
every cloned page, take its own desktop and mobile frames (not the donor's) and compare computed
styles at the frame widths with the script below (`evaluate_script` in chrome-devtools):

1. Heading accents: accented words, their color, weight and font.
2. H1 and H2: font size, line height, weight.
3. FAQ headings: set the script's `sel` default to the question selector.
4. Elements that exist only on this page: present and styled per the frame, not replaced by donor equivalents.
5. Donor leftovers in settings: compare `wp post meta list <ID>` of the clone and the donor. Equal
   SEO title and description, OG image, canonical, schema, page-level ACF options, CTA links and
   form IDs are candidates: fix them within scope or list them as questions.

```js
// Headings with their size and accent children (color, weight, style or font differing from the heading).
(sel = "h1, h2") => {
  const key = s => `${s.color} ${s.fontWeight} ${s.fontStyle} ${s.fontFamily}`;
  const visible = [...document.querySelectorAll(sel)].filter(el => el.getClientRects().length);

  return visible.map(el => {
    const s = getComputedStyle(el);
    const accents = [...el.querySelectorAll("*")]
      .filter(c => key(getComputedStyle(c)) !== key(s))
      .map(c => {
        const cs = getComputedStyle(c);
        return { text: c.innerText.trim().slice(0, 40), color: cs.color, weight: cs.fontWeight, font: cs.fontFamily };
      });
    return { tag: el.tagName.toLowerCase(), text: el.innerText.trim().slice(0, 60), size: s.fontSize, lineHeight: s.lineHeight, weight: s.fontWeight, color: s.color, accents };
  });
}
```

### Run web-page-qa

Finish by running the `ai-toolkit:web-page-qa` skill on every changed page against its own frames.
This step is mandatory. If it cannot run, say so in the report.

Report changed sections, imported media IDs, verification results, web-page-qa findings, and
unresolved inputs or checks that could not be performed. Do not claim visual verification from
metadata checks alone.
