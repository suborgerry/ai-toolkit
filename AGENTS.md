# AGENTS.md

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

## 6. Code style

- Prettier: `printWidth: 180`, double quotes, trailing commas (es5), `arrowParens: "avoid"`, with `prettier-plugin-tailwindcss` enabled (class lists get auto-sorted).
- ESLint: TypeScript recommended config; `@typescript-eslint/no-explicit-any` is disabled.
- TypeScript: strict mode on, `noUnusedLocals`/`noUnusedParameters` enforced — `tsc` runs as part of `build` and will fail the build on unused identifiers.

## 7. Code for humar read

- When writing something intended for human consumption, (comment, commit message, reply to prompt) use as few words as possible. Pick every word meticulously to reduce the volume to a strict minimum. Be down to the point. Less is more.

- Avoid superlatives and praise. Stop telling me I am absolutely right. Give me the cold hard truth.

- Avoid magic numbers and strings by extracting recurring or meaningful values into descriptive constants (const) or enums. Keep self-explanatory, one-off values inline to avoid clutter. If a value comes from a spec (e.g. HTTP 200 OK), use a constant regardless.

- Reduce code indentation. Avoid Arrow Anti-Pattern. Leverage early return and continue.

- Keep function names short. Less than 30 characters.

- Use enums instead of booleans for function parameters.

- Let the reader of the code breathe. Add empty lines between logical blocks of code.

- Add a small, to the point, comment to explain *what* the block does and *why*. Use examples when possible. Propose ASCII drawings to explain complete systems.

- Treat member visibility changes as a breaking design shift. Keep all fields and functions private unless external access is strictly required by the design. Prompt the user for explicit approval before changing any access modifier from private to internal or public.

- Program to levels of abstraction. Lower-level mechanics (e.g., raw hardware I/O, sector parsing, direct socket streams) must be encapsulated in a dedicated driver/abstraction layer. Expose clean, high-level APIs to the rest of the application so calling code works with domain concepts, not raw implementation details.

- Don't touch blocks of code unrelated to the feature you implement. e.g. Don't add comments to a block of code if you did not create it or modify it. As much as possible try to minimize the number of changed lines when implementing a feature.

- Strictly adhere to the layered boundary hierarchy: each layer may only communicate with its immediate neighbor directly below it. Never "punch holes" through layers (e.g., controllers or UI components must never directly call database queries, raw hardware drivers, or low-level network clients; always route through the intermediate service/abstraction layer).

- Always use {}, even on a one-line "if" statement.

- If the prompt indicates that a bug is being fixed, don't write the fix right away. First write the test. Observe it failing. Then write the fix. And observe the test passing.

## 8. Interaction tool. 
- Priority #1 for chromedevtools-mcp. If unavailable, check whether it is installed and not currently in use by another agent.
- Priority #2 for browser-skill and other tools.
