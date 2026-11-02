# ACF output: JSON, PHP templates, escaping, checks

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

When changing a group, set its `modified` value to the current Unix time so wp-admin offers sync.

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
    $item_title       = $item['title'] ?? '';
    $item_description = $item['description'] ?? '';
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
