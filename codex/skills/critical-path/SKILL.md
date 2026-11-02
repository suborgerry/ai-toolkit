---
name: critical-path
description: Speed up first render of a Vite + WordPress theme page - per-page critical CSS generated with `critical` (inlined in head, full bundle deferred) and non-blocking JS (defer, delayed third-party scripts), measured before and after with chrome-devtools-mcp traces. Use when asked about critical CSS or JS, render-blocking CSS or scripts, deferring theme or third-party scripts, critical rendering path, FCP/LCP, or PageSpeed on such a project. Not for visual QA against Figma (web-page-qa).
---

# Critical rendering path

Goal: the first screen paints from HTML plus a small inlined CSS file; everything else loads without blocking it.
Measure first: if nothing blocks render noticeably, report and stop.

```txt
discover ─► baseline trace ─► plan (approve) ─► CSS ─► JS ─► verify trace ─► report
                  └─ nothing to gain ─► report, stop
```

Write the report in the language the user writes in.

## Preconditions

Stop and tell the user if any is missing:

- Vite project that builds pages from `pages/*.html` into `dist/` and copies `dist/assets` into a WordPress theme.
- Node ≥ 22.13 (`critical` 9).
- Local WordPress serving the theme, reachable in the browser. Never measure or change production.
- chrome-devtools-mcp.

## 1. Discover

Inspect once, change nothing:

- `package.json` `build` script, `vite.config.*` (`base`, output names), `scripts/copy-assets.*` (which dist files go where in the theme).
- Theme: `wp_enqueue_style` / `wp_enqueue_script` calls — handles, `in_footer`, `strategy`, dependencies, inline scripts attached to them.
- Head of each WordPress page (via `evaluate_script`): every `link[rel=stylesheet]` and `script[src]` with position, `async`/`defer`/`type`, and origin. Mark third-party ones.
- Page mapping: dist page name = WordPress slug, front page = `index`. List mismatches.
- Performance plugins (WP Rocket, LiteSpeed Cache, Autoptimize, Perfmatters, SiteGround Optimizer). If one already does critical CSS or delays JS, stop and ask: two systems on the same page conflict.

## 2. Baseline

For each mapped page on local WordPress, record a performance trace (`performance_start_trace`, `reload: true`, `ignoreCache: true`):

- mobile: `emulate` viewport `375x812x2,mobile,touch`, network `Fast 4G`, CPU `4`;
- desktop: viewport `1440x900x1`, no throttling.

Collect FCP, LCP, CLS and the `RenderBlocking`, `LCPBreakdown`, `CLSCulprits`, `ThirdParties` insights (`performance_analyze_insight`).
Note sizes of the theme CSS and JS bundles.

Stop and report if `RenderBlocking` does not list theme CSS or JS and no third-party script blocks render, unless the user asks to proceed.

## 3. Plan and approve

Present the planned changes as a list: dependencies, new files, `package.json` build order, `copy-assets` mapping, theme PHP edits, each JS change.
Ask for approval in one message before touching anything. Approval of the CSS part does not cover the JS part.

## 4. Critical CSS

1. `npm i -D critical@^9 playwright`, then `npx playwright install chromium` (use the project's package manager).
2. Copy `<skill-dir>/scripts/critical-css.mjs` into the project's `scripts/`. It serves `dist/` with `vite preview`,
   renders every `dist/*.html` at 375×812 and 1440×900 with JS running, and writes `dist/assets/css/critical/<page>.css`.
3. Build order: `tsc && vite build && node scripts/critical-css.mjs && node scripts/copy-assets.js`.
4. Make `copy-assets` copy `dist/assets/css/critical/` into the theme. Follow the file's existing style.
5. `FORCED_CSS` in the script: add rules for states the project's JS removes on init (search `src/` for `x-cloak`,
   `no-js`, `classList.remove` at startup). The renderer extracts after JS ran and never sees those states.
6. Theme PHP: read `references/wp-integration.md` and adapt the CSS part (handle, paths, page map).

Pages without a critical file keep the normal render-blocking bundle. That is the safe fallback, not an error.

## 5. JS

Apply only the approved items:

- Theme bundle: enqueue with `['in_footer' => true, 'strategy' => 'defer']` (WordPress ≥ 6.3). See `references/wp-integration.md`.
- Third-party scripts: propose per script — keep, `defer`, or load on first interaction. Delaying analytics loses
  short sessions; say so. Never delay consent managers or anything the first screen needs.
- First screen must look right before JS runs: menus, sliders, accordions in their initial state, no layout shift
  when JS initialises (`CLSCulprits`). Fix with CSS in the component, not with more inline JS.
- Code splitting (dynamic `import()`) is out of scope: the IIFE `script.js` is a classic script. If the bundle is large and
  `LCPBreakdown` or main-thread time points at it, recommend moving to ES modules in the report; do not do it.

## 6. Verify

1. `npm run build` passes; every expected `critical/<page>.css` exists in the theme and is smaller than the full bundle.
2. On each WordPress page: `<style id="critical-css">` comes before any stylesheet in `<head>`, the bundle is a
   `preload` in `<head>` and a stylesheet at the end of `<body>`. A page without a critical file still has the normal blocking link.
3. `list_network_requests`: no 404 for fonts or images referenced by the critical CSS.
4. First-screen check at both viewports: screenshot, then disable the full bundle with
   `evaluate_script` (`document.querySelectorAll('link[rel=stylesheet][href*="<bundle>"]').forEach(l => l.disabled = true)`),
   then screenshot again without reloading. The first screen must be identical; below the fold may differ.
5. Repeat the baseline traces with the same settings.

If a check fails, fix and re-run it. Do not report success with a failing check.

## Report

```md
## Critical path: <site>

| Page | Viewport | FCP before → after | LCP before → after | CLS before → after | Render-blocking before → after |
|---|---|---|---|---|---|
| index | mobile | 2.1 s → 1.3 s | 3.4 s → 2.6 s | 0.02 → 0.02 | style.css, script.js → — |

Critical CSS: index 18 KB of 64 KB, …
JS: script.js deferred; GTM kept; chat widget loads on first interaction.
Changed files: …
Not done / recommendations: …
```
