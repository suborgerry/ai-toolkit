// Per-page critical CSS from the local WordPress site, run after the theme build.
// Renders each page at mobile and desktop viewports and writes the CSS painted
// above the fold to <theme>/<OUT_DIR>/<key>.css. The theme inlines that file in <head>.
//
//   node scripts/critical-css.mjs https://theme.local / /about/
//   https://theme.local/       ─► critical (render, 375 + 1440) ─► critical/index.css
//   https://theme.local/about/ ─►                                ─► critical/about.css
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { critical } from "critical";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));

// Theme-relative, tracked in git and shipped in the release package.
const OUT_DIR = path.join(root, "assets/css/critical");

// Front page key; other pages use the last path segment (WordPress slug).
const FRONT_KEY = "index";

// Both folds are unioned: one file covers phones and desktops.
const VIEWPORTS = [
  { width: 375, height: 812 },
  { width: 1440, height: 900 },
];

// Rules for states JS removes before extraction runs, so the renderer never sees them.
// Example: Alpine drops [x-cloak] on init; without this rule cloaked menus flash on load.
const FORCED_CSS = "[x-cloak]{display:none!important}";

const [site, ...paths] = process.argv.slice(2);
if (!site) {
  console.error("usage: node scripts/critical-css.mjs <local-site-url> [/path/ ...]");
  process.exit(1);
}

const origin = new URL(site).origin;
const keyOf = p => p.split("/").filter(Boolean).at(-1) ?? FRONT_KEY;

fs.mkdirSync(OUT_DIR, { recursive: true });

for (const p of paths.length ? paths : ["/"]) {
  const url = new URL(p, origin).href;
  const { css, report } = await critical({ src: url, engine: "render", dimensions: VIEWPORTS });

  // url() comes back absolute to the local site; keep it root-relative so it works on production.
  const out = FORCED_CSS + css.replaceAll(origin, "");

  const key = keyOf(new URL(url).pathname);
  fs.writeFileSync(path.join(OUT_DIR, `${key}.css`), out);
  console.log(`critical-css: ${url} -> ${path.relative(root, OUT_DIR)}/${key}.css (${out.length} B of ${report.bytes.stylesheets} B)`);

  for (const warning of report.warnings) {
    console.warn(`critical-css: ${url}: ${warning}`);
  }
}
