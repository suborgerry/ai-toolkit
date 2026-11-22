# Shopify modeling: sections, blocks, settings

## Section Classification

Treat most non-global parts of the page as sections in a JSON template.

Treat these as structural/global, not page sections:

- Header, footer, announcement bar → section groups (`sections/header-group.json`, `footer-group.json`)
- Navigation, mobile menu → `link_list` setting rendered from a Shopify menu
- Logo, socials, contact details, global CTA → `config/settings_schema.json` (theme settings)
- Product, collection, cart, search, blog templates → dynamic sources (`product`, `collection` objects), not copy

Forms: use the theme's existing `{% form %}` sections (contact, newsletter). Do not build new form handling unless asked.

## Section Naming Standard

Use **lowercase kebab-case** for section and block files; the `type` in template JSON equals the file name.

```txt
Schema name:  Hero: Media Split
File:         sections/hero-media-split.liquid
Type:         hero-media-split
```

Formula:

```txt
[family]-[visual-pattern]-[optional-structural-variant]
```

Name by **visual structure and reusable pattern**, not by page copy, colors, decoration, or page location.
Follow the theme's prefix convention if it has one.

Good: `hero-media-split`, `content-cards-grid`, `cta-centered`, `faq-accordion`, `testimonials-slider`, `stats-grid`, `logos-strip`

Avoid: `homepage-banner`, `about-us-section`, `why-choose-us`, `blue-section`, `hero-v1`, `hero-new`, `custom-section`

### Preferred Families

```txt
hero, intro, content, cards, features, benefits, services, team,
testimonials, case-studies, faq, cta, stats, logos, gallery,
pricing, form, map, posts, resources, process, showcase, campaign,
featured-product, featured-collection
```

### Preferred Pattern Terms

```txt
centered, split, media-split, grid, cards-grid, list, accordion,
slider, tabs, strip, band, featured, masonry, timeline, steps,
table, comparison, collage, overlap, sticky, stacked
```

## Duplicate Structure Rule

Before adding a section, compare it with existing and pending sections.

One section with a `select` setting when sections share content model and markup but differ by:

- Color scheme or background
- Image side left/right
- Spacing density
- Minor decorative elements
- Optional eyebrow, badge, icon, or CTA
- Column count that CSS handles safely

Separate section when markup hierarchy, settings model, or JS behavior differs meaningfully.

## Blocks Or Settings

- Repeating items (cards, stats, logos, FAQ rows, slides) → blocks with `max_blocks` matching the design's intent.
- Elements the merchant may reorder or remove (heading, text, buttons) → blocks only when the theme already composes
  sections from blocks (theme blocks in `blocks/`). Otherwise section settings.
- Theme blocks in `blocks/` only if the theme already uses them; otherwise section-local blocks in the schema.

## Settings Modeling

Never hardcode content merchants reasonably need to change. Do not make decorative details editable.

| Content | Setting type |
|---|---|
| Eyebrow, label, heading | `inline_richtext` if the theme uses it for headings, else `text` |
| Short description | `textarea` or `inline_richtext` |
| Rich content, several paragraphs | `richtext` |
| Image | `image_picker` |
| Video | `video` (uploaded) or `video_url` (YouTube/Vimeo) |
| Single CTA | `text` label + `url` link |
| Multiple CTAs, cards, stats, rows | blocks |
| Layout modifier | `select` with `id` `variant`, `media_position`, or `layout` |
| Color scheme | `color_scheme` if the theme has schemes; otherwise `select` mapped to theme classes |
| Show/hide | `checkbox` |
| Spacing, column count | `range` (only if the design shows variation) |
| Product / collection / menu reference | `product`, `collection`, `link_list` |
| Trusted embed code | `html` setting named `embed_code` |

Do not convert decorative inline SVGs into `image_picker`. Do not ask merchants to enter HTML for normal content.

## Setting Naming Rules

Concise `snake_case` ids, unique within the section and within each block type.

Good: `heading`, `description`, `image`, `button_label`, `button_link`, `variant`, `color_scheme`, `show_divider`

Avoid: `main_section_heading_text`, `homepage_button_url`, `about_us_image`, `blue_bg`, `image_2`

## Liquid Variable Naming

- `snake_case`, named by role: `section_heading`, `media_image`, `primary_link`, `card_heading`.
- Plural for collections, singular for loop items: `section.blocks` → `block`, filtered `cards` → `card`.
- Boolean intent: `has_cta`, `is_reversed`, `show_intro`.
- Assign raw settings first, then derived values (`section_classes`, `image_ratio`), then markup.
