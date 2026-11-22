---
name: figma-to-shopify-liquid
description: Build Figma sections directly as Shopify theme sections and blocks (Liquid, schema, JSON templates) and verify each one pixel-perfect on a local `shopify theme dev` preview. Use when implementing a Figma page or section straight into a Shopify Online Store 2.0 theme with Shopify CLI available. Not for WordPress/ACF (figma-to-acf), static HTML without Shopify (figma-pixel-perfect-frontend), apps, checkout extensions, or Hydrogen.
---

# Figma to Shopify Liquid

Figma is the source of truth for output. The theme is the source of truth for structure, conventions, and build.
No intermediate static HTML: every section is written as a Liquid section with schema and checked on the dev theme.

```txt
Figma section ─► schema (settings, blocks) ─► Liquid markup ─► assets ─► template JSON ─► render on theme dev ─► compare ─► fix
                                                                                                    └──── next section ◄┘
```

## Preconditions

Stop and tell the user if any is missing:

- Figma URL or frame for each section. Without a visual reference, do not start.
- Theme source locally and a store the user named for `shopify theme dev --store <store>`.
- Shopify CLI authenticated; `shopify theme dev` serves a preview URL.
- Browser screenshot tooling (chrome-devtools-mcp preferred).

## Shopify CLI safety

1. **Development theme only.** Work through `shopify theme dev`; it uploads to a development theme, never the live one.
2. **Forbidden:** `theme publish`, `theme delete`, `theme push` (any form), `--live`, `--allow-live`, `theme share`,
   `theme rename`, `theme pull` over local files, `--theme-editor-sync`. If the task seems to need one, stop and ask.
3. **Own files only.** Create or change only the sections, blocks, snippets, assets, locale keys, and the dev template
   this task needs. Do not edit `templates/index.json`, existing page templates, `config/settings_data.json`, or
   section groups unless the user names them.
4. **No store writes.** Do not change products, pages, files, menus, or settings in the admin, by API or browser,
   unless the user gives access for that exact step (see "Images").
5. **No secrets.** Do not read or print tokens, `.env`, or CLI credentials.

## Discovery

Inspect once per task:

- Theme architecture: sections only, or theme blocks in `blocks/` (`{% content_for 'blocks' %}`); section groups for
  header and footer; existing sections and naming.
- Schema conventions: plain labels or `t:` keys in `locales/*.schema.json`; `presets`, `enabled_on`, color schemes.
- Styling: `{% stylesheet %}`, asset CSS files, or a build (Tailwind, Vite). If a build exists, run its watch during
  work and the full build at the end; confirm its sources cover `sections/`, `blocks/`, `snippets/`.
- Fonts, tokens (`config/settings_schema.json`, CSS variables), icon snippets, image and button snippets.
- **Image placeholder**: `snippets/*placeholder*`, or how existing sections render an empty `image_picker`
  (e.g. `placeholder_svg_tag`). Record what you find; it is used in "Images".

## Plan and approve

1. Split the Figma page into sections. Classify each: section, structural (header, footer, menu → section groups and
   theme settings), form, or global setting.
2. Reuse existing sections where the structure matches. Propose names for new ones.
3. Ask the user to approve the section list and names (AskUserQuestion) before writing code.

Read `references/shopify-modeling.md` for classification, naming, duplicate rules, and settings modeling.

## Dev template

Create `templates/page.<figma-page-handle>-dev.json`. Preview it on any existing page with the alternate-template
parameter: `<preview-url>/pages/<handle>?view=<figma-page-handle>-dev`. Ask the user which page handle to use.
Assigning the template to a page in the admin happens only after the user agrees.

## Per-section loop

For each section, in page order:

1. **Read Figma.** Extract the values listed in `references/figma-fidelity.md` → "Design Data Extraction".
2. **Schema.** Write settings, blocks, and presets per `references/liquid-output.md` → "Schema Rules".
3. **Markup.** Write `sections/<section-name>.liquid` from Figma, per `references/liquid-output.md`
   (assign settings at the top, escape on output, full class strings for variants).
4. **Assets.** See "Assets" and "Images" below.
5. **Content.** Add the section to the dev template with the exact Figma copy:

   ```json
   { "sections": { "hero": { "type": "hero-media-split",
       "settings": { "heading": "Text from Figma", "image": "shopify://shop_images/hero.jpg" } } },
     "order": ["hero"] }
   ```

   Omit `image` when no uploaded file exists; the section then renders the placeholder.
6. **Verify.** Render the preview, screenshot the section at the Figma frame width, compare, fix, repeat per
   `references/figma-fidelity.md` → "Visual Verification". Then check the responsive widths.
   Placeholder areas are compared for size, ratio, and position only.
7. Move to the next section only when no critical or medium differences remain.

## Assets

| Asset | Route |
|---|---|
| Decoration (raster or SVG) the merchant does not change | File in `assets/`, see below |
| Content image, or anything the merchant must be able to replace | `image_picker` setting; see "Images" |

Decorations in `assets/` are output only through Liquid filters:

- SVG: `{{ 'decor-wave.svg' | inline_asset_content }}`, inside a wrapper with `aria-hidden="true"`.
- Raster: `{{ 'decor-texture.png' | asset_url | image_tag: alt: '', loading: 'lazy' }}`.

No hardcoded asset paths, no CDN URLs, no CSS `url()` to assets. Name files `decor-<role>.<ext>`.

Clean SVG exports: remove fixed IDs that can collide, keep `viewBox`, use `currentColor` where the color follows text.

## Images

**Figma images never enter the theme as fallbacks.** Forbidden:

- Figma exports in `assets/` used for content images or as the `else` branch of an empty `image_picker`
  (decorations from "Assets" are the only Figma files allowed in `assets/`).
- `{% if section.settings.image %}…{% else %}<img src="{{ 'figma-hero.jpg' | asset_url }}">{% endif %}`.
- Figma MCP or other temporary URLs anywhere in Liquid, CSS, or JSON.

Every content image is an `image_picker` (or `image` block). Fill it one of two ways:

1. **Admin access.** Ask the user for access to upload to Content → Files, or ask them to upload the files themselves.
   Export from Figma at the rendered size × 2 into the task directory (not the theme), check with the
   `check-figma-assets` skill, write alt text with `generate-alt-text`. After upload, reference each file in the
   template as `shopify://shop_images/<filename>`.
2. **Placeholder.** Without access, leave the setting empty and render the placeholder:
   - the theme's existing placeholder (snippet or `placeholder_svg_tag` pattern found in Discovery), reused as is;
   - if the theme has none, create `snippets/image-placeholder.liquid`: a single neutral SVG (rect + simple glyph,
     `currentColor`, `aria-hidden="true"`), sized by the slot's aspect ratio. Reuse it in every section.

List every image slot left on a placeholder in the final response, with its Figma node.

## Finish

1. Run `shopify theme check` on changed files and the full build if one exists.
2. Run the checks in `references/liquid-output.md` → "Validation And Verification".
3. Screenshot the full dev template once at desktop and 375 px.
4. Full QA is out of scope; suggest `web-page-qa` on the preview URL.

## Final response

- Sections → names, new or reused
- Files changed (sections, blocks, snippets, assets, locales, template)
- Preview URL with `?view=`, development theme ID
- Images: uploaded files with `shopify://` references, slots left on placeholder
- Verification passes per section and widths checked; remaining differences
- Theme check and build results
- Assumptions, skipped items, manual steps (assign template to a page, upload images)
