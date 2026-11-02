# WordPress integration

Adapt to the theme: put the code where the theme enqueues assets, use its prefix and existing handles.

## Critical CSS

```php
// Critical CSS: inline the page's above-the-fold CSS, load the full bundle without blocking render.
// Files: dist/assets/css/critical/<page>.css, copied into the theme by scripts/copy-assets.js.
// Pages without a file keep the normal render-blocking stylesheet.
const CRITICAL_CSS_DIR = 'assets/css/critical/';   // theme-relative
const CRITICAL_STYLE_HANDLE = 'main-style';        // handle of the enqueued Vite CSS bundle
const CRITICAL_THEME_ASSETS = 'assets/';           // theme folder mirroring dist/assets/
const CRITICAL_PAGE_MAP = [];                      // WP slug => dist page, e.g. ['home-care' => 'landing']

// Critical file of the current page or null. Example: front page → assets/css/critical/index.css.
function theme_critical_css_path(): ?string {
	$page = is_front_page() ? 'index' : '';
	if ($page === '' && is_singular()) {
		$page = get_post_field('post_name', get_queried_object_id());
	}
	if ($page === '') {
		return null;
	}

	$page = CRITICAL_PAGE_MAP[$page] ?? $page;
	$path = get_theme_file_path(CRITICAL_CSS_DIR . $page . '.css');

	return is_file($path) ? $path : null;
}

// Inline before any stylesheet (styles print at wp_head priority 8).
add_action('wp_head', function (): void {
	$path = theme_critical_css_path();
	if (!$path) {
		return;
	}

	// url() in dist CSS is root-relative (/assets/...); point it at the theme copy.
	$css = str_replace('url(/assets/', 'url(' . get_theme_file_uri(CRITICAL_THEME_ASSETS), file_get_contents($path));
	echo '<style id="critical-css">' . $css . "</style>\n";
}, 1);

// Full bundle: preload in <head>, apply at the end of <body>. No inline JS, so CSP-safe.
add_filter('style_loader_tag', function (string $tag, string $handle, string $href): string {
	if ($handle !== CRITICAL_STYLE_HANDLE || !theme_critical_css_path()) {
		return $tag;
	}

	add_action('wp_footer', function () use ($tag): void {
		echo $tag;
	}, PHP_INT_MAX);

	return '<link rel="preload" as="style" href="' . esc_url($href) . '">' . "\n";
}, 10, 3);
```

Check after adapting:

- If the Vite `base` is not `/`, url() in critical files is still root-relative (`/assets/...`): the script resolves
  them against the preview server. Keep the `str_replace`; verify fonts and images load.
- Styles that depend on the bundle handle still print in `<head>` and block. Usually fine; list them in the report.

## Theme JS bundle

```php
wp_enqueue_script('main-script', get_theme_file_uri('assets/js/script.js'), [], $version, [
	'in_footer' => true,
	'strategy' => 'defer',
]);
```

- `defer` keeps execution order among deferred scripts and runs before `DOMContentLoaded`; code waiting for
  `DOMContentLoaded` still works. Alpine recommends `defer`.
- WordPress silently falls back to a blocking tag when the strategy is unsafe, e.g. a blocking script depends
  on the handle. Check the printed tag, not only the PHP.
