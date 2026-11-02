// Per-page critical CSS, run after `vite build`.
// Serves dist/ with `vite preview` (JS runs, assets resolve), renders each page at
// mobile and desktop viewports and writes the CSS painted above the fold to
// dist/assets/css/critical/<page>.css. The theme inlines that file in <head>.
//
//   dist/index.html ─► vite preview ─► critical (render, 375 + 1440) ─► critical/index.css
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { preview } from "vite";
import { critical } from "critical";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const DIST_DIR = path.join(root, "dist");
const OUT_DIR = path.join(DIST_DIR, "assets/css/critical");

// Both folds are unioned: one file covers phones and desktops.
const VIEWPORTS = [
  { width: 375, height: 812 },
  { width: 1440, height: 900 },
];

// Rules for states JS removes before extraction runs, so the renderer never sees them.
// Example: Alpine drops [x-cloak] on init; without this rule cloaked menus flash on load.
const FORCED_CSS = "[x-cloak]{display:none!important}";

const server = await preview({ root, logLevel: "warn" });
const origin = new URL(server.resolvedUrls.local[0]).origin;

try {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const pages = fs.readdirSync(DIST_DIR).filter(f => f.endsWith(".html"));
  for (const file of pages) {
    const { css, report } = await critical({ src: `${origin}/${file}`, engine: "render", dimensions: VIEWPORTS });

    // url() comes back absolute to the preview server; keep it root-relative like style.css.
    const out = FORCED_CSS + css.replaceAll(origin, "");

    const name = path.parse(file).name;
    fs.writeFileSync(path.join(OUT_DIR, `${name}.css`), out);
    console.log(`critical-css: ${file} -> assets/css/critical/${name}.css (${out.length} B of ${report.bytes.stylesheets} B)`);

    for (const warning of report.warnings) {
      console.warn(`critical-css: ${file}: ${warning}`);
    }
  }
} finally {
  await server.close();
}
