# Liquid output: schema, markup, escaping, checks

## Schema Rules

- One `{% schema %}` per section, valid JSON, at the end of the file.
- `name`: readable label (`Hero: Media Split`) or a `t:` key if the theme translates schemas. With `t:` keys, add
  them to every `locales/*.schema.json` the theme ships (at least the default).
- `presets` with at least one entry, so the section appears in the theme editor. Preset blocks mirror the Figma item count.
- `enabled_on` / `disabled_on` per theme convention (e.g. exclude section groups for page sections).
- Every setting has `type`, `id`, `label`. Add `default` only where the theme does; content lives in the template JSON.
- `select` options: `value` in `snake_case`, readable `label`.
- `range`: `min`, `max`, `step`, `unit`, `default`, within the platform's step-count limit.
- Blocks: `type` (kebab-case), `name`, `settings`; set `max_blocks` when the design caps the count.
- Do not rename existing setting ids or block types: stored content in templates references them.

## Markup Rules

Each section file:

- Assigns settings at the top, then derived values, then markup.
- Uses `section.id` for unique DOM ids; no hardcoded ids that repeat when the section is added twice.
- Renders blocks with `{{ block.shopify_attributes }}` on the block wrapper.
- Uses `{% render %}` for snippets (isolated scope; pass params explicitly). New snippets get a `{% doc %}` header.
- Maps variants to full class strings in `{% case %}`; no class names built from fragments the build cannot detect.
- Uses `{% stylesheet %}` / `{% javascript %}` or the theme's asset pattern, whichever the theme uses.
- Has no copied HTML comments from Figma exports.

Skeleton:

```liquid
{% liquid
  assign section_heading = section.settings.heading
  assign section_text = section.settings.description
  assign media_image = section.settings.image

  assign section_classes = 'hero hero--media-left'
  if section.settings.media_position == 'right'
    assign section_classes = 'hero hero--media-right'
  endif
%}

<section id="section-{{ section.id }}" class="{{ section_classes }}">
  {% if section_heading != blank %}
    <h2 class="hero__heading">{{ section_heading }}</h2>
  {% endif %}

  {% if section_text != blank %}
    <p class="hero__text">{{ section_text | escape }}</p>
  {% endif %}

  <div class="hero__media">
    {% if media_image != blank %}
      {{ media_image | image_url: width: 1920 | image_tag: loading: 'lazy', widths: '480, 960, 1440, 1920', sizes: '(min-width: 990px) 50vw, 100vw' }}
    {% else %}
      {% render 'image-placeholder' %}
    {% endif %}
  </div>
</section>

{% schema %}
{
  "name": "Hero: Media Split",
  "settings": [
    { "type": "inline_richtext", "id": "heading", "label": "Heading" },
    { "type": "textarea", "id": "description", "label": "Description" },
    { "type": "image_picker", "id": "image", "label": "Image" },
    { "type": "select", "id": "media_position", "label": "Media position", "default": "left",
      "options": [{ "value": "left", "label": "Left" }, { "value": "right", "label": "Right" }] }
  ],
  "presets": [{ "name": "Hero: Media Split" }]
}
{% endschema %}
```

The `else` branch renders the placeholder only. Never a theme asset exported from Figma (see `SKILL.md` → "Images").

## Escaping And Output

| Setting | Output |
|---|---|
| `text`, `textarea` | `{{ value \| escape }}` |
| `inline_richtext`, `richtext` | `{{ value }}` (Shopify sanitizes) |
| `url` | `href="{{ value }}"`; check `!= blank` first |
| Attribute value from text | `{{ value \| escape }}` |
| `html` (trusted embed) | `{{ value }}` |

Do not wrap `textarea` in `newline_to_br` unless the design shows hard line breaks; use `richtext` for real formatting.

### Images

- Render with `image_url` + `image_tag`; set `widths` and `sizes` from the slot's rendered width.
- Alt text comes from the file's alt in Shopify; pass `alt:` only for a deliberate override.
- Above the fold: `loading: 'eager'`, `fetchpriority: 'high'` for the first section only.
- No manual `<img src="{{ … | asset_url }}">` for content. No editable `background-image: url(...)`; render a
  positioned image element instead.
- An empty `image_picker` renders the placeholder in the same slot, with the slot's aspect ratio, so layout is unchanged.

### Links

```liquid
{% if section.settings.button_label != blank and section.settings.button_link != blank %}
  <a href="{{ section.settings.button_link }}" class="button">{{ section.settings.button_label | escape }}</a>
{% endif %}
```

### Blocks

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'card' %}
      <div class="card" {{ block.shopify_attributes }}>
        <h3 class="card__heading">{{ block.settings.heading | escape }}</h3>
      </div>
  {% endcase %}
{% endfor %}
```

Use `forloop.index` for display numbers and `block.id` for ARIA relationships.

## Template JSON

- `templates/page.<name>-dev.json`: `sections` keyed by stable ids (`hero`, `faq`), `order` in Figma page order.
- `type` equals the section file name. Block entries go in `blocks` with `block_order`.
- Settings hold the exact Figma copy. `image_picker` values are `shopify://shop_images/<filename>` of uploaded files,
  or omitted.
- `richtext` values are HTML strings (`"<p>Text</p>"`); `inline_richtext` allows inline tags only.

## Static Markup And Interaction

- Preserve the theme's existing JS hooks, custom elements, `data-*` attributes, and ARIA patterns when reusing parts.
- Do not add `aria-label` to every `<section>`; no `aria-hidden` on wrappers or meaningful images.
- `aria-hidden="true"` only for decorative SVGs and the placeholder.
- Tabs, accordions, sliders, modals, menus: keyboard and state behavior per the theme's existing components.
- Re-initialize JS on `shopify:section:load` if the theme does for similar sections.

## Validation And Verification

After each section or batch:

- `shopify theme check` passes for changed files.
- Schema JSON parses; every setting has `type`, `id`, `label`; ids unique per section and block type.
- Each new section has `presets`; `t:` keys exist in locale schema files.
- Template JSON parses; every `type` has a matching file; every `order` id exists in `sections`.
- No hardcoded DOM ids without `section.id`; `block.shopify_attributes` present on every block wrapper.

Scan changed files for forbidden patterns:

```txt
asset_url used for content images or in an image_picker else branch
assets referenced by hardcoded path, CDN URL, or CSS url() instead of asset_url / inline_asset_content
Figma, MCP, or other temporary asset URLs
manual <img> for image_picker settings
editable CSS background-image URLs
unescaped text / textarea output
```

Run project checks when available: `shopify theme check`, `npm run build`, `npm run lint`.

Do not claim completion until checks pass or remaining issues are clearly reported.
