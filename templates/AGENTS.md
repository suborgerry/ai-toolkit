# AGENTS.md

## Project

Fill in when copying into a theme. If a value is still `<...>`, ask the user for it before relying on it.

- Local site: `<local-url>`
- Production: `<prod-url>`
- Asset budget: `<asset-budget>`

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

Use `pnpm`, not `npm` or `yarn`.

- `pnpm dev`, `pnpm build`, `pnpm lint`, `pnpm check`.
- `scripts/package-theme.mjs` packages the theme into `release/`. Agent files never ship: `AGENTS.md`, `CLAUDE.md`, `.mcp.json`, `.claude/`, `.claude-plugin/`, `.agents/`. Add any missing one to its exclusions.
- `templates/` holds the theme PHP templates, e.g. `templates/flexible.php`.

Scripts differ between themes: read `package.json` and `scripts/` before the first build. Don't guess what a script does.

## 6. Code style

- Prettier: `printWidth: 180`, double quotes, trailing commas (es5), `arrowParens: "avoid"`, with `prettier-plugin-tailwindcss` enabled (class lists get auto-sorted).
- ESLint: TypeScript recommended config; `@typescript-eslint/no-explicit-any` is disabled.
- TypeScript: strict mode on, `noUnusedLocals`/`noUnusedParameters` enforced — `tsc` runs as part of `build` and will fail the build on unused identifiers.

## 7. Code for humar read

- Replies and questions to the user: in the language the user writes in. Code, commits, comments: English.

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
- Run tests in a separate isolated tab, never in the window the user is viewing.
- Never close the user's Chrome or its profile without asking.

## 9. Git and deploy

- The theme has its own git repository.
- Main branch: `main`. Push to `main` deploys to production.
- Before every commit, check the branch: `git branch --show-current`.
- No `Co-Authored-By` trailers.
- Never commit or push without an explicit request. Strictly forbidden.

## 10. Environments

- Local site and production URLs: see Project.
- ACF content, menus and image crops live in the database, not in git. Deploy does not carry them.
- At the end of a task, list what must be repeated on production by hand: page, field / menu / image, value.
- Agent files on production: check read-only via chrome-devtools or safari MCP. Ask the user for the production URL each time; take the theme slug from the page source (`/wp-content/themes/<slug>/`). Open `<prod-url>/wp-content/themes/<slug>/<file>` for each agent file from §5 (for folders, a known file inside, e.g. `.claude-plugin/plugin.json`, `.claude/settings.json`): 200 = leaked, report it; 404 = absent; 403 = unknown, ask for a file listing (SFTP or hosting file manager).

## 11. Performance

- Before handing over animations and heavy blocks, measure with 4× CPU and GPU off: `lighthouse <url> --throttling.cpuSlowdownMultiplier=4 --chrome-flags="--disable-gpu"`.
- Check asset weight against the asset budget (see Project).
- Never promise a PageSpeed score you have not measured.

## 12. Shared styles

Before changing a shared rule (e.g. the accent heading in `templates/flexible.php`), check it against every Figma frame where it applies.
