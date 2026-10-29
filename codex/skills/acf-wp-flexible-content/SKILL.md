---
name: acf-wp-flexible-content
description: Use when converting static HTML sections, frontend components, or existing page markup into WordPress theme integration with ACF Pro Flexible Content, ACF Local JSON field groups, PHP template parts, CMS-editable fields, safe WordPress output, and structural header/footer/theme settings wiring. Trigger for HTML-to-WordPress, ACF flexible layouts, template-parts/flexible, ACF JSON updates, WordPress theme partials, options pages, and replacing hardcoded section content with editable ACF fields. Do not use for pixel-perfect frontend-only work, Gutenberg blocks, or plugin/page-builder architecture unless explicitly requested.
---

# ACF WP Flexible Content

Convert static HTML sections or frontend components into a maintainable WordPress theme implementation using **ACF Pro Flexible Content**, **ACF Local JSON**, and **safe PHP template parts**.

This skill is for CMS integration work after, or alongside, frontend implementation. The goal is not to rebuild the design from scratch; the goal is to preserve the approved markup and make the correct content editable in WordPress.

## Source Of Truth

- The current project is the source of truth for theme paths, coding style, helper functions, Tailwind/CSS conventions, asset handling, ACF JSON structure, field key naming, menu registration, and rendering patterns.
- The provided HTML, components, screenshots, or existing templates are the source of truth for structure, classes, attributes, Alpine/JS hooks, visual hierarchy, and content relationships.
- Existing ACF JSON field groups are the source of truth for group settings, field naming patterns, layout conventions, and key style.
- When project conventions conflict with this skill, inspect the project first and follow the project if the convention is intentional and safe.

## Default Project Paths

Use project equivalents when paths differ:

```txt
wp-theme/templates/flexible.php
wp-theme/template-parts/flexible/[layout_name].php
wp-theme/acf-json/group_flexible_content.json
wp-theme/acf-json/group_theme_settings.json
wp-theme/template-parts/header.php
wp-theme/template-parts/footer.php
wp-theme/functions.php
wp-theme/inc/
```

Never assume these paths are final. First inspect the repository and follow the existing theme structure.

## Required Discovery

Before editing, inspect enough context to answer:

- Where is the active WordPress theme?
- How does the project render Flexible Content?
- Which ACF JSON groups already exist?
- What is the flexible field name: `content`, `page_sections`, `sections`, or another name?
- How are layout PHP files named and loaded?
- Are existing layout names structural and reusable?
- Are header, footer, menus, forms, and site-wide values already handled elsewhere?
- Which helpers, button partials, image helpers, menu walkers, or theme settings already exist?
- Which build/lint/PHP checks are available?

For large batches, report the detected sections, structural components, duplicates, and proposed layout names before implementation when doing so prevents rework.

## Core Workflow

1. Audit source HTML/components and identify section boundaries.
2. Classify each item as a flexible section, structural component, form placeholder, archive/listing, or global setting.
3. Check existing flexible layouts before creating new ones.
4. Merge duplicate structures into one reusable layout with a controlled variant only when justified.
5. Choose layout names using the naming standard in this skill.
6. Model fields from the source markup.
7. Update ACF JSON without breaking existing keys, group settings, or field order.
8. Create or update the PHP template part.
9. Integrate structural components outside Flexible Content.
10. Validate JSON, scan PHP for forbidden patterns, and run project checks.
11. Report changed files, layouts, fields, assumptions, checks, and any skipped work.

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

## ACF JSON Rules

Flexible layouts should live in the project’s main Flexible Content field group, usually:

```txt
wp-theme/acf-json/group_flexible_content.json
```

Do not split layouts into separate `layout_*.json` files unless the project already uses a custom generation system.

Default keys when creating a new group from scratch:

```txt
Field group key:       group_flexible_content
Flexible field key:    field_content
Flexible field name:   content
Layout key:            layout_[layout_name]
Layout name:           [layout_name]
Template file:         [layout_name].php
```

Hard rules:

- Preserve existing field group settings: `location`, `menu_order`, `position`, `style`, `label_placement`, `instruction_placement`, `hide_on_screen`, `show_in_rest`, `active`, and project-specific properties.
- Do not regenerate existing field keys.
- Do not reuse field keys across layouts or field groups.
- The layout object key in `layouts` must match the layout `key` value.
- Layout `name` must exactly match the PHP file name without `.php`.
- The first sub-field in every layout must be `section_id` unless the existing project intentionally uses another standard.
- Every field must include at least `key`, `label`, `name`, and `type`.
- Do not add `instructions`, `placeholder`, or `required` unless the user or existing project convention requires it.
- Every `textarea` must include `rows` and `new_lines: ""`.
- Every `image` should use `return_format: "id"` and `preview_size: "medium"`.
- Every `link` should use `return_format: "array"`.
- Every `repeater` should include `layout` and `button_label`.
- Repeater sub-fields should include `parent_repeater` when the existing JSON format uses it. The value must exactly match the parent repeater field key.

Standard first field:

```json
{
  "key": "field_[layout_name]_section_id",
  "label": "Section ID",
  "name": "section_id",
  "type": "text"
}
```

When creating a new group, create only real layouts and real fields. Do not leave placeholder layouts or sample fields in committed JSON.

## PHP Template Rules

Each flexible template should:

- Start with a short docblock: `Flexible layout: [Label]`.
- Fetch all ACF fields at the top.
- Avoid inline `get_sub_field()` calls inside HTML attributes.
- Use `section_id` on the outer `<section>` when present.
- Preserve source classes, data attributes, Alpine directives, AOS attributes, ARIA states, and JS hooks unless they are unsafe or obsolete.
- Use `!empty()` checks for optional fields.
- Avoid copied HTML comments from static source markup.
- Keep the template readable and close to the original approved markup.

Skeleton:

```php
<?php
/**
 * Flexible layout: Hero: Media Split
 *
 * Fields:
 * - section_id (text)
 * - heading (textarea)
 * - description (textarea)
 * - image (image)
 * - cta_link (link)
 */
$section_id  = get_sub_field('section_id');
$heading     = get_sub_field('heading');
$description = get_sub_field('description');
$image       = get_sub_field('image');
$cta_link    = get_sub_field('cta_link');
?>

<section <?= !empty($section_id) ? 'id="' . esc_attr($section_id) . '"' : '' ?> class="...">
  <?php if (!empty($heading)): ?>
    <h2 class="..."><?= esc_html($heading) ?></h2>
  <?php endif; ?>
</section>
```

## Escaping And Output Rules

Escape on output by context:

| Context | Function |
|---|---|
| Visible plain text | `esc_html()` |
| Attribute value | `esc_attr()` |
| URL | `esc_url()` |
| WYSIWYG/rich HTML | `wp_kses_post()` |
| Trusted admin embed code | raw echo with `phpcs:ignore WordPress.Security.EscapeOutput` |

Do not use `the_field()` or `the_sub_field()` inside flexible templates. Use `get_sub_field()` and explicit context-aware escaping.

Do not wrap textareas in `nl2br()`. If line breaks or rich formatting are required, use a WYSIWYG field instead.

Do not add `__()`, `_e()`, text domains, or translation wrappers around ACF content unless multilingual implementation is explicitly requested.

### Image Output

Use attachment IDs and `wp_get_attachment_image()`:

```php
<?php if (!empty($image)): ?>
  <?= wp_get_attachment_image($image, 'full', false, [
    'class' => '...',
    'loading' => 'lazy',
  ]) ?>
<?php endif; ?>
```

For above-the-fold images, use `loading => 'eager'` and `fetchpriority => 'high'` when appropriate.

Never write manual `<img>` tags for ACF image fields unless the project has a helper that intentionally does so. Avoid editable `background-image: url(...)`; render editable images as positioned image elements where possible.

### Link Output

```php
<?php if (!empty($cta_link)): ?>
  <?php
  $cta_url    = $cta_link['url'] ?? '';
  $cta_title  = $cta_link['title'] ?? '';
  $cta_target = $cta_link['target'] ?? '';
  ?>

  <?php if (!empty($cta_url) && !empty($cta_title)): ?>
    <a
      href="<?= esc_url($cta_url) ?>"
      <?= !empty($cta_target) ? 'target="' . esc_attr($cta_target) . '"' : '' ?>
      <?= $cta_target === '_blank' ? 'rel="noopener noreferrer"' : '' ?>
      class="..."
    ><?= esc_html($cta_title) ?></a>
  <?php endif; ?>
<?php endif; ?>
```

### Repeater Output

Prefer array-based repeater output for flexible templates:

```php
<?php $items = get_sub_field('items'); ?>

<?php if (!empty($items)): ?>
  <?php foreach ($items as $i => $item): ?>
    <?php
    $title = $item['title'] ?? '';
    $text  = $item['text'] ?? '';
    ?>
  <?php endforeach; ?>
<?php endif; ?>
```

Use `foreach ($items as $i => $item)` so indexes are available for numbers, IDs, animation delays, and ARIA relationships. `$i` is zero-based; display numbers as `$i + 1`.

Avoid `have_rows()` / `the_row()` inside repeater output unless the existing project explicitly uses that pattern and changing it would be inconsistent.

### Embed Output

```php
<?= $embed_code // phpcs:ignore WordPress.Security.EscapeOutput ?>
```

Only output raw embed fields when the field is intended for trusted admin-entered iframe/script snippets.

## Flexible Template Loop

Use the project’s existing loop if present. Otherwise use the project equivalent of:

```php
<?php if (have_rows('content')): ?>
  <?php while (have_rows('content')): the_row(); ?>
    <?php get_template_part('template-parts/flexible/' . get_row_layout()); ?>
  <?php endwhile; ?>
<?php endif; ?>
```

The field name must match the flexible content field in ACF JSON.

If a layout file might be missing during migration, use the project’s existing fallback pattern. Do not add noisy front-end errors unless the project already does.

## Static Markup And Interaction Rules

- Preserve existing classes, IDs required by scripts, `data-*` attributes, Alpine directives, AOS attributes, Swiper hooks, animation classes, and ARIA relationships.
- Do not change frontend behavior unless the CMS integration requires it.
- Do not add `aria-label` to every `<section>` by default.
- Do not add `aria-hidden` to section wrappers or meaningful images.
- Use `aria-hidden="true"` only for decorative inline SVGs or clearly decorative elements.
- Keep semantic heading order from the source unless the source is clearly incorrect.
- For tabs, accordions, sliders, modals, and menus, preserve keyboard and state behavior.

## Styling Integration

- Preserve approved utility classes and scoped classes from the source markup.
- Avoid class names composed dynamically in PHP that the build cannot detect; map variants to full class strings.
- Do not refactor styling architecture while converting ACF sections.

## Structural Components And Theme Settings

Header, footer, navigation, and global UI are not Flexible Content layouts.

Use theme partials and existing WordPress systems:

- Include structural partials with `get_template_part()`.
- Replace static nav lists with `wp_nav_menu()` when appropriate.
- Use existing menu walkers from `inc/` before creating new ones.
- Register nav menus only if missing.
- Preserve mobile menu, Alpine state, and JS hooks.
- Move editable global content into Theme Settings fields.

Theme Settings should be a separate field group, commonly:

```txt
wp-theme/acf-json/group_theme_settings.json
group_theme_settings
options_page == theme-settings
```

Use Theme Settings for:

```txt
logo
header_cta
footer_cta
phone
email
address
socials
footer_columns
copyright
```

Read option fields with:

```php
get_field('field_name', 'option')
```

Register an ACF options page only if one does not already exist:

```php
add_action('acf/init', function () {
    if (function_exists('acf_add_options_page')) {
        acf_add_options_page([
            'page_title' => 'Theme Settings',
            'menu_title' => 'Theme Settings',
            'menu_slug'  => 'theme-settings',
            'capability' => 'edit_posts',
            'redirect'   => false,
        ]);
    }
});
```

Follow existing capability, slug, and menu placement conventions if present.

## Accessibility And Editor UX

CMS editability must not break accessible output.

- Keep meaningful images editable and output with appropriate alt handling through WordPress attachment data.
- Keep decorative SVGs static and hidden from assistive tech when appropriate.
- Do not make editors choose from confusing technical variants.
- Labels should be readable in wp-admin.
- Fields should appear in the same logical order as the front-end section.
- Avoid over-modeling tiny decorative differences as editor fields.

## Validation And Verification

After each layout or batch, run the strongest available checks.

Required JSON checks:

```bash
python3 -m json.tool wp-theme/acf-json/group_flexible_content.json
python3 -m json.tool wp-theme/acf-json/group_theme_settings.json
```

Adjust paths to the project.

Verify:

- JSON is valid.
- No duplicate field keys were introduced.
- Layout object keys match layout `key` values.
- Layout names use lowercase `snake_case` only.
- PHP file names match layout names exactly.
- `section_id` is the first sub-field in each new layout.
- Textareas include `rows` and `new_lines: ""`.
- Images use attachment ID return format.
- Links use array return format.
- Repeater sub-fields include correct `parent_repeater` when used by the project JSON.
- Existing group settings were preserved.

Scan PHP for forbidden or suspicious patterns:

```txt
the_field(
the_sub_field(
nl2br(
@package
required HTML comments copied from source
manual <img> output for ACF image fields
editable CSS background-image URLs
translation wrappers around ACF content
unescaped plain ACF output
```

Run project checks when available:

```txt
composer lint / phpcs / php -l
npm run build
npm run lint
npm run typecheck
```

Do not claim completion until checks pass or remaining issues are clearly reported.

## Final Response

Include:

- Converted sections/components
- Files changed
- ACF field groups and layouts updated
- Layout names and PHP templates created/updated
- Structural components or Theme Settings touched
- JSON/PHP/build/lint checks run and results
- Important assumptions
- Skipped items or unresolved blockers
- Any manual WordPress admin sync steps required
