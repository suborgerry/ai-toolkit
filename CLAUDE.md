# CLAUDE.md

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. Implement
2. Verify
3. Re-check against requirements
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Commands

- `npm run dev` — Vite dev server (use `npm run host` to expose on LAN).
- `npm run build` — runs `tsc` typecheck, then `vite build`, then `node scripts/copy-assets.js`. The copy step syncs `dist/assets/**` into `wp-theme/assets/` so the built output can be dropped into a WordPress theme.
- `npm run preview` — preview the `dist/` build.
- No test runner is configured. Lint via `npx eslint .`; format via `npx prettier --write .`.

## 6. Architecture

This is a multi-page Vite site (MPA) whose final delivery target is a WordPress theme. The repo was forked from the `zen-express` starter; some root-level starter files (e.g. `index.html`) are not part of the actual build.

### Build inputs

`vite.config.js` discovers entry HTML by reading `pages/*.html` at config-load time — **only files in `pages/` become build inputs**; the root `index.html` is ignored. The TS entry is `src/scripts/main.ts`, emitted as `assets/js/script.js`. Two custom Vite plugins run during build:

1. `wrap-in-iife` — wraps the emitted `script.js` in an IIFE so it is safe to enqueue from a WordPress theme without polluting the global scope.
2. `flatten-html-output` — moves `dist/pages/*.html` up to `dist/*.html` after the bundle is written, so the final layout matches WordPress theme expectations.

Output file naming is customized in `rollupOptions.output`: JS → `assets/js/[name].js`, CSS → `assets/css/style.css` (single file), fonts → `assets/fonts/`.

### Handlebars partials

`vite-plugin-handlebars` is wired to `components/` as the `partialDirectory` with `reloadOnPartialChange: true`. Reusable HTML fragments live there and are referenced from `pages/*.html` via Handlebars partial syntax (`{{> partial-name}}`). The directory is currently empty — new shared markup should go there rather than being duplicated across pages.

### Styles

`src/styles/main.css` is the single style entry, imported by `src/scripts/main.ts`. It does:

```css
@import "tailwindcss" important;
@import "./custom.css";
```

The `important` modifier on the Tailwind v4 import means **every Tailwind utility is emitted as `!important`**. This is intentional so utilities win against WordPress theme styles when the build is embedded. Implication when authoring custom CSS: project-specific class rules in `custom.css` will *not* override Tailwind utilities applied to the same element unless they are also `!important`. Prefer adjusting the utility set on the element, or scope custom CSS to properties Tailwind isn't setting.

### Units and design source

Components are recreated from Figma. Component-scoped classes follow a BEM-ish convention (`.care-hero`, `.care-hero__title`, `.care-hero__button:hover`) alongside Tailwind utilities on the same element.

### WordPress integration

`scripts/copy-assets.js` mirrors `dist/assets/` → `wp-theme/assets/` at the end of `npm run build`. Anything that needs to ship to the theme must end up under `dist/assets/` (which is why the rollup output naming and IIFE wrapping matter). Public files in `public/images/` are copied to `dist/` as-is by Vite but are **not** propagated to `wp-theme/` by the copy script — image assets are expected to live in the theme separately.

## 7. Code style

- Prettier: `printWidth: 180`, double quotes, trailing commas (es5), `arrowParens: "avoid"`, with `prettier-plugin-tailwindcss` enabled (class lists get auto-sorted).
- ESLint: TypeScript recommended config; `@typescript-eslint/no-explicit-any` is disabled.
- TypeScript: strict mode on, `noUnusedLocals`/`noUnusedParameters` enforced — `tsc` runs as part of `build` and will fail the build on unused identifiers.