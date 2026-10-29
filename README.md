# ai-toolkit

Skills for a Figma → frontend → WordPress (ACF) workflow, kept in two variants: a Claude Code plugin and Codex skills. Both variants share one body; only platform-specific lines differ.

| Skill | Purpose |
|---|---|
| `figma-pixel-perfect-frontend` | Figma/screenshot → frontend markup with browser visual QA |
| `acf-wp-flexible-content` | Static sections → ACF Flexible Content, Local JSON, PHP templates |
| `new-page-by-existing` | Fill a cloned WordPress page from Figma and supplied content |
| `check-figma-assets` | Compare prepared images with Figma references |
| `generate-alt-text` | Context-aware alt text for images, icons, logos |
| `web-page-qa` | QA a live page against Figma via chrome-devtools-mcp |
| `skill-creator` | Create or update a skill in this repo for both platforms |

## Layout

```txt
.claude-plugin/marketplace.json   Claude marketplace → ./claude
claude/                           Claude Code plugin "ai-toolkit"
  .claude-plugin/plugin.json
  skills/<name>/SKILL.md
codex/skills/<name>/              Codex skills
  SKILL.md
  agents/openai.yaml
```

## Install: Claude Code

```txt
/plugin marketplace add suborgerry/ai-toolkit
/plugin install ai-toolkit@ai-toolkit
```

Local development: `claude --plugin-dir ./claude`. Skills are namespaced, e.g. `/ai-toolkit:web-page-qa`.

## Install: Codex

Link skills into a scanned location, per user or per repository:

```bash
for s in codex/skills/*; do ln -s "$PWD/$s" ~/.agents/skills/; done        # user
for s in codex/skills/*; do ln -s "$PWD/$s" <repo>/.agents/skills/; done   # repository
```

Invoke with `$skill-name` or `/skills`. Codex ships a built-in `skill-creator` with the same name; both appear in `/skills`.

## MCP servers

- `web-page-qa` requires chrome-devtools-mcp.
- Figma skills use the Figma MCP server when available.
