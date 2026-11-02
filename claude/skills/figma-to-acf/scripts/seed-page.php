<?php
/**
 * Seed one page's Flexible Content from a JSON file.
 *
 * Usage: wp eval-file seed-page.php <seed.json>
 *
 * Seed format:
 * {
 *   "post_id": 123,
 *   "field_key": "field_flexible_content",
 *   "rows": [
 *     { "acf_fc_layout": "hero_media_split", "section_id": "hero", "heading": "...", "image": 456 }
 *   ]
 * }
 *
 * Replaces all rows of the field. Does not touch title, slug or status.
 */

if (!function_exists('update_field') || !function_exists('acf_get_field')) {
    WP_CLI::error('ACF is not active.');
}

// Read and decode the seed file.
$seed_path = $args[0] ?? '';
if (!is_readable($seed_path)) {
    WP_CLI::error("Seed file not readable: {$seed_path}");
}

$seed = json_decode(file_get_contents($seed_path), true);
if (!is_array($seed)) {
    WP_CLI::error('Seed file is not valid JSON: ' . json_last_error_msg());
}

$post_id   = (int) ($seed['post_id'] ?? 0);
$field_key = (string) ($seed['field_key'] ?? '');
$rows      = $seed['rows'] ?? null;

// Validate the target before writing.
if (!get_post($post_id)) {
    WP_CLI::error("Post not found: {$post_id}");
}

if (!acf_get_field($field_key)) {
    WP_CLI::error("ACF field not found: {$field_key}. Check the key and the acf-json load path.");
}

if (!is_array($rows)) {
    WP_CLI::error('Seed "rows" must be an array.');
}

// ACF resolves sub-field names inside rows and stores row counts and field references.
update_field($field_key, $rows, $post_id);

$saved = get_field($field_key, $post_id, false);
$saved_count = is_array($saved) ? count($saved) : 0;

if ($saved_count !== count($rows)) {
    WP_CLI::error(sprintf('Saved %d of %d rows to post %d.', $saved_count, count($rows), $post_id));
}

WP_CLI::success(sprintf('Saved %d rows to post %d.', $saved_count, $post_id));
