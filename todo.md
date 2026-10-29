# TODO

## Agents

- [ ] `page-qa` agent from `web-page-qa`: read-only, report output, keeps screenshots out of main context. Tools: chrome-devtools, Figma read.
- [ ] `media-prep` agent merging `check-figma-assets` + `generate-alt-text`: one image pass, JSON output, batchable, cheaper model.
- [ ] `visual-verifier` agent for the verification step of `figma-pixel-perfect-frontend`: compares one block with Figma, returns differences.
- [ ] Claude: `claude/agents/*.md`. Codex: equivalent subagent config.
- [ ] `new-page-by-existing` delegates to `media-prep`, then `page-qa`.

## Structure

- [ ] Split `acf-wp-flexible-content` (652 lines > 500): move naming vocabulary, field tables, PHP snippets to `references/`.
- [ ] Move `web-page-qa` inline JS (scroll prep, freeze, section map, overflow, link check) to `scripts/*.js`.
- [ ] Unify viewport sets: `figma-pixel-perfect-frontend` 1440/1024/768/375 vs `web-page-qa` 1920…320.
- [ ] Resolve overlap with Figma plugin skill `figma:figma-design-to-code` (mandatory before `get_design_context`); reference it from `figma-pixel-perfect-frontend`.
- [ ] `web-page-qa` hard-stops without chrome-devtools; `AGENTS.md` §8 allows a fallback. Pick one rule.
- [ ] Rename toolkit `skill-creator` if collision with Codex built-in / `anthropic-skills:skill-creator` causes wrong triggering.
- [ ] Add LICENSE (required by Claude plugin directory) and plugin icon if publishing.
- [ ] Verify Codex `openai.yaml` dependency schema for stdio MCP (`web-page-qa` → chrome-devtools).
- [ ] `AGENTS.md` §5–6 describe a Vite/WordPress project that is not in this repo; move to a template or drop.

## acf-wp-flexible-content

- [ ] Fix contradiction: forbids `$title`, `$text`, `$image`, but skeleton and repeater examples use them.
- [ ] Field names (`heading`) vs variable rule (`$section_heading`): align.
- [ ] Add: bump ACF JSON `modified` timestamp so wp-admin offers sync.
- [ ] Replace prose JSON checks with `scripts/validate-acf-json.py` (duplicate keys, `parent_repeater`, `section_id` first, layout name = PHP file).
- [ ] Add rendered-page check in WordPress.
- [ ] Explain or drop the `@package` ban.

## figma-pixel-perfect-frontend

- [ ] Replace "at least 3 passes" with a stop criterion (diff threshold or zero critical/medium issues).
- [ ] Define comparison tooling (overlay / pixel diff).
- [ ] Use `check-figma-assets` and `generate-alt-text` for assets.

## web-page-qa

- [ ] Link check: parallel `fetch` with timeout.
- [ ] Extend `unsafe` regex: `checkout`, `cart/clear`, similar.
- [ ] Section map and `stillHidden`: add WOW.js and other builders.
- [ ] Optional numeric diff for design comparison.

## new-page-by-existing

- [ ] Concrete snapshot/rollback: where to store values, how to restore.

## check-figma-assets

- [ ] Say where references come from (Figma `get_screenshot`).
- [ ] Optional objective metric (SSIM / diff).
- [ ] Output: add severity and matched reference.

## generate-alt-text

- [ ] Length guidance (~125 chars).
- [ ] Safer default keys than base filename.
