---
name: figma-to-acf
description: Build Figma sections directly as WordPress ACF Flexible Content layouts (Local JSON, PHP templates, seeded content) and verify each one pixel-perfect on a local WordPress page. Use when implementing a Figma page or section straight into a WordPress theme with ACF, with WP-CLI and Local running. Not for static HTML without WordPress (figma-pixel-perfect-frontend), converting existing HTML to ACF (acf-wp-flexible-content), or filling an existing page (new-page-by-existing).
---

# Figma to ACF Flexible Content

Figma is the source of truth for output. The theme is the source of truth for structure, conventions, and build.
No intermediate static HTML: every section is written as an ACF layout plus PHP template and checked on WordPress.

```txt
Figma section ─► fields (acf-json) ─► PHP template ─► assets ─► seed ─► render on Local ─► compare ─► fix
                                                                                   └──── next section ◄┘
```

## Preconditions

Stop and tell the user if any is missing:

- Figma URL or frame for each section. Without a visual reference, do not start.
- Local site running and reachable in the browser.
- WP-CLI working against that site (`wp option get siteurl` succeeds).
- Browser screenshot tooling (chrome-devtools-mcp preferred).

## WP-CLI safety

These rules apply even when a guard hook is installed; the hook is a backstop, not permission.

1. **Local only.** Before the first write, run `wp option get siteurl`. Continue only if the host is local
   (`localhost`, `127.0.0.1`, `*.local`, `*.test`). Never use aliases (`@prod`), `--ssh`, `--http`, or another `--path`.
2. **Snapshot first.** Before the first write, `wp db export <task-dir>/before.sql`. Rollback is manual:
   give the user the path; do not import it yourself.
3. **Own objects only.** Write only to the dev page and attachments this task created or the user named.
   Record their IDs. Never change other posts, options, users, plugins, themes, core, or `wp-config.php`.
4. **No publishing.** Do not set `post_status=publish`, remove `noindex`, or change slugs unless the user asks.
5. **Content in files, never in the shell.** Page content goes into a seed JSON file and is loaded only with
   `wp eval-file ${CLAUDE_SKILL_DIR}/scripts/seed-page.php <seed.json>`. Do not write ad-hoc PHP for `eval` or `eval-file`.
6. **Forbidden:** `db drop|reset|import|clean|query|cli`, `site empty|delete`, `search-replace` without `--dry-run`,
   `plugin|theme|core` changes, `user`, `config`, `cron event run`, `shell`, `post delete`, `option update|delete`.
   If the task seems to need one, stop and ask.
7. **No secrets.** Do not read or print DB credentials, salts, user emails, or API keys.
8. **Side effects.** Saving posts can trigger plugin hooks (mail, webhooks). If a write produces unexpected
   output or errors, stop and report; do not retry blindly.

## Discovery

Inspect once per task:

- Active theme, Flexible Content loop, flexible field key, `acf-json` path, existing layouts and naming.
- Page template that renders Flexible Content.
- Build: how CSS/JS reach the theme. Run the project's watch build during work; run the full build at the end.
  If the watch build does not update theme assets, say so and ask how to proceed.
- Tailwind: confirm the sources cover PHP templates (e.g. `@source "../../wp-theme/**/*.php"` in the CSS entry).
  Without it, classes used only in PHP are missing from the CSS. Report and ask before changing build config.
- Fonts, tokens, icon set, image helpers, existing partials (buttons, images, menus).

## Plan and approve

1. Split the Figma page into sections. Classify each: flexible layout, structural (header, footer, menu → partials
   and Theme Settings), form, or global setting.
2. Reuse existing layouts where the structure matches. Propose names for new ones.
3. Ask the user to approve the section list and layout names (AskUserQuestion) before writing JSON.

Read `references/acf-modeling.md` for classification, naming, duplicate rules, and field modeling.

## Dev page

Use the page the user named, or create one: `wp post create --post_type=page --post_status=draft
--post_title="<Figma page name> (dev)" --page_template=<flexible template> --porcelain`. Record the ID.

Drafts need a logged-in browser. Before screenshots, remove the admin bar so it does not shift the layout:
`document.getElementById('wpadminbar')?.remove(); document.documentElement.style.setProperty('margin-top', '0', 'important');`.
Publishing the dev page on Local is allowed only after the user agrees.

## Per-section loop

For each section, in page order:

1. **Read Figma.** Extract the values listed in `references/figma-fidelity.md` → "Design Data Extraction".
2. **Fields.** Add the layout to `acf-json` per `references/acf-output.md` → "ACF JSON Rules".
3. **Template.** Write `template-parts/flexible/<layout_name>.php` from Figma, per `references/acf-output.md`
   (fetch fields at the top, escape on output, full class strings for variants).
4. **Assets.** See "Assets" below.
5. **Seed.** Append the section row to the seed JSON with the exact Figma copy and attachment IDs, then run the
   seed script. Format is in the script header:

   ```json
   { "post_id": 123, "field_key": "field_flexible_content",
     "rows": [{ "acf_fc_layout": "hero_media_split", "section_id": "hero", "heading": "Text from Figma", "image": 456 }] }
   ```

6. **Verify.** Render the dev page, screenshot the section at the Figma frame width, compare, fix, repeat per
   `references/figma-fidelity.md` → "Visual Verification". Then check the responsive widths.
7. Move to the next section only when no critical or medium differences remain.

## Assets

Pick the first route that fits:

| Asset | Route |
|---|---|
| Vector (icon, logo, decoration) the editor does not change | Inline SVG in the PHP template. Decorative: `aria-hidden="true" focusable="false"` |
| Raster or vector the editor must be able to replace | ACF `image` field, file imported to the media library |
| Raster that is part of the design, not content | Theme asset, output with `get_theme_file_uri()` |

For media-library files:

1. Export from Figma at the rendered size × 2, in the format the site uses.
2. Check with the `ai-toolkit:check-figma-assets` skill; write alt text with `ai-toolkit:generate-alt-text`.
3. `wp media import <file> --porcelain --title="..." --alt="..."`; record the ID for the seed.

Never use temporary Figma asset URLs. Clean SVG exports: remove fixed IDs that can collide, keep `viewBox`,
use `currentColor` where the color follows text.

## Finish

1. Run the full build and project checks (`php -l` on changed templates, lint, typecheck).
2. Validate changed JSON (`python3 -m json.tool <file>`) and run the checks in `references/acf-output.md` →
   "Validation And Verification".
3. Read back the seed (`wp post meta list <ID>`) and screenshot the full page once at desktop and 375 px.
4. Full QA is out of scope; suggest `ai-toolkit:web-page-qa` on the dev page.

## Final response

- Sections → layout names, new or reused
- Files changed (JSON, PHP, CSS, assets)
- Dev page ID and URL, imported attachment IDs, snapshot path
- Verification passes per section and widths checked; remaining differences
- Build and check results
- Assumptions, skipped items, manual steps (ACF sync in wp-admin, build config changes)
