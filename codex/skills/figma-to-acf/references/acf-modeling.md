# ACF modeling: sections, layouts, fields, variables

## Section Classification

Treat most non-global sections inside `<main>` as Flexible Content layouts.

Treat these as structural/global, not flexible sections:

- Header
- Footer
- Navigation
- Mobile menu shell
- Site logo
- Global CTA repeated across templates
- Site-wide contact details
- Social links
- Tracking snippets
- Archive/query templates
- Search result templates

Structural content should usually live in theme partials, WordPress menus, Theme Settings option fields, or existing project settings.

Forms should not be rebuilt unless requested. If the form system is unknown, preserve the layout and add a clear placeholder such as:

```php
<?php // Form embed goes here. ?>
```

## Layout Naming Standard

Use **lowercase snake_case** for ACF layout names and matching PHP files.

```txt
ACF label:  Hero: Media Split
ACF name:   hero_media_split
PHP file:   hero_media_split.php
```

Formula:

```txt
[section_family]_[visual_pattern]_[optional_structural_variant]
```

Name layouts by **visual structure and reusable pattern**, not by page copy, colors, decoration, campaign text, or page location.

Good:

```txt
hero_media_split
content_media_split
content_cards_grid
benefits_cards_grid
cta_centered
faq_accordion
testimonials_slider
stats_grid
logos_strip
```

Avoid:

```txt
homepage_banner
about_us_section
why_choose_us
blue_section
section_with_circles
hero_v1
hero_new
```

Preferred label format:

```txt
[Family]: [Pattern] [Variant]
```

Examples:

```txt
Hero: Media Split
Content: Cards Grid
CTA: Centered
FAQ: Accordion
Testimonials: Slider
Stats: Grid
```

### Preferred Families

Use this vocabulary before inventing new families:

```txt
hero, intro, content, cards, features, benefits, services, team,
testimonials, case_studies, faq, cta, stats, logos, gallery,
pricing, form, map, menu, posts, resources, process, showcase,
campaign
```

### Preferred Pattern Terms

```txt
centered, split, media_split, grid, cards_grid, list, accordion,
slider, tabs, strip, band, featured, masonry, timeline, steps,
table, comparison, collage, overlap, sticky, filterable,
interactive, pinned, asymmetric, stacked
```

### Complex Layout Rule

For unusual sections, identify the dominant reusable structure.

```txt
Bad:  hero_left_text_right_image_floating_cards_gradient_background
Good: hero_media_overlap
```

Create a new layout only when the HTML hierarchy, PHP partial, field model, or front-end behavior is meaningfully different. Decoration, color, spacing, reversed columns, optional badges, and dark/light styling usually belong in the same layout as a field such as `variant`, `theme`, or `media_position`.

Avoid universal layouts like:

```txt
custom_section
content_universal
flexible_builder_section
section_builder
```

## Duplicate Structure Rule

Before adding a layout, compare it with existing and pending layouts.

Use one layout with a controlled select field when sections share the same content model and markup but differ by:

- Background color or theme
- Image side left/right
- Spacing density
- Minor decorative elements
- Optional badge, eyebrow, icon, or CTA
- Card column count that can be handled safely in CSS

Create a separate layout when:

- The markup hierarchy is different
- A different PHP partial would be clearer and safer
- The field model is substantially different
- A different JS behavior is required
- One template would need too many unrelated modes

## Field Modeling Rules

Never hardcode content that editors reasonably need to change. Do not make decorative implementation details editable.

Use these defaults unless the project has a stronger convention:

| Content | ACF field |
|---|---|
| Section anchor | `text` named `section_id`, first field in every layout |
| Eyebrow, label, short heading line | `textarea`, `rows: 2`, `new_lines: ""` |
| Heading | `textarea`, `rows: 2`, `new_lines: ""` |
| Short description | `textarea`, `rows: 3`, `new_lines: ""` |
| Body paragraph with fixed classes | `textarea`, `rows: 5`, `new_lines: ""` |
| Rich content or multiple classless paragraphs | `wysiwyg`, no media upload unless needed |
| Image | `image`, `return_format: "id"`, `preview_size: "medium"` |
| Gallery/lightbox | `gallery`, not image repeater |
| Single CTA | `link`, `return_format: "array"` |
| Multiple CTAs | repeater `buttons` with `link` and optional `button_type` |
| Cards, rows, steps, socials, stats, menu items | `repeater` |
| Layout modifier | `select` named `variant`, `theme`, `style`, or `media_position` |
| Show/hide control | `true_false` named `enabled` |
| Number, year, count | `number` |
| External URL without label | `url` |
| Trusted embed code | `textarea` named `embed_code`, `rows: 5`, `new_lines: ""` |

Do not convert decorative inline SVGs into ACF image fields. Keep decorative SVG markup static and mark it decorative when appropriate.

Do not ask editors to enter HTML for normal headings, text, images, buttons, or cards. Use WYSIWYG only when real rich text is required.

## Field Naming Rules

Use concise `snake_case` names.

Good:

```txt
section_id
heading
description
image
background_image
cta_link
buttons
items
cards
stats
variant
enabled
embed_code
```

Repeater sub-fields are relative to the row:

```txt
title
description
image
icon
link
number
label
```

Avoid redundant or page-specific names:

```txt
main_section_heading_text
service_card_service_title
homepage_button_url
about_us_image
blue_section_background
```

Use names that make sense inside the PHP template and inside wp-admin.

## PHP Variable Naming Concepts

Use these short concepts when writing variables inside `template-parts/flexible/*.php` files:

- Use lowercase `snake_case` for PHP variables.
- Name variables by their role inside the section, not by page copy, temporary content, or decoration.
- Prefer the formula `[context]_[role]_[optional_detail]`, for example `$section_heading`, `$media_image`, `$primary_link`, `$background_theme`.
- Match ACF field names and PHP variable names when practical: `section_heading` → `$section_heading`.
- Avoid vague names like `$title`, `$text`, `$image`, `$link`, `$data`, `$item_data`, `$final_data`, or `$clean_title`.
- Avoid page-specific, copy-specific, color-specific, and numbered names like `$homepage_title`, `$why_choose_us_text`, `$blue_bg`, `$image_2`.
- Use plural names for collections and singular names for loop items: `$cards` → `$card`, `$stats` → `$stat`, `$logos` → `$logo`.
- Use clear prefixes when a template has repeated concepts: `$section_heading`, `$card_heading`, `$media_image`, `$background_image`, `$primary_link`, `$secondary_link`.
- Use boolean prefixes that describe intent: `$has_cta`, `$is_reversed`, `$show_intro`, `$enable_slider`, `$should_render_section`.
- Keep raw ACF values easy to distinguish from derived values. Fetch raw values first, then create derived values such as `$section_classes`, `$heading_id`, `$image_alt`, `$primary_link_url`.
- For ACF link arrays, unpack readable parts before markup: `$primary_link_url`, `$primary_link_title`, `$primary_link_target`.
- For image values, use role-based names such as `$media_image`, `$background_image`, `$card_image`; render with project image helpers or `wp_get_attachment_image()`.
- For CSS classes, use target-specific names: `$section_classes`, `$card_classes`, `$button_classes`.
- Order variables consistently: content fields, media fields, links/CTAs, repeaters, settings/booleans, derived values, render conditions, markup.

The goal is a clear path from **ACF field name → PHP variable → derived value → escaped output**.
