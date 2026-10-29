---
name: skill-creator
description: Create or update a skill in the ai-toolkit repository, producing both the Claude Code plugin variant and the Codex variant. Use when asked to write, add, port, split, rename, or improve a toolkit skill, its description, or its triggering. Not for general coding guidelines or one-off prompts.
---

# Create or update a toolkit skill

## Layout

```txt
claude/skills/<name>/SKILL.md            Claude Code plugin "ai-toolkit"
codex/skills/<name>/SKILL.md             Codex
codex/skills/<name>/agents/openai.yaml   Codex UI metadata, policy, MCP dependencies
<platform>/skills/<name>/references/     Long specs, read on demand
<platform>/skills/<name>/scripts/        Deterministic code, executed not loaded
```

Both variants share one body. Only the lines listed in "Platform differences" may differ.

## 1. Think before writing

- One job per skill. State its trigger (what the user says), inputs, output, and what is out of scope.
- Search both `skills/` directories and installed third-party skills (e.g. the Figma plugin) for overlap.
  Extend an existing skill instead of adding a competing one.
- If scope, trigger, or output format is ambiguous, ask. Do not pick an interpretation silently.

## 2. Write the minimum

- `name`: lowercase-hyphen, equal to the directory name, at most 64 characters.
- `description`: first clause says what it does with the main trigger words; then `Use when …`;
  then `Not for …` when a neighbouring skill is confusable. Third person, at most 1024 characters.
  Front-load: Claude truncates long listings and Codex shortens descriptions first.
- Body: imperative steps with explicit inputs and outputs, plus the output format with an example.
  Write only what the model would not do correctly by default.
- Do not repeat the description in the body (no "Use this skill for" lists).
- Do not include generic coding principles; they live in the user's `AGENTS.md` / `CLAUDE.md`.
- Keep `SKILL.md` under 500 lines. Move long tables or specs to `references/<topic>.md`, linked with
  "read when …". Move scripts and validators to `scripts/`.
- No `README.md`, changelog, or other extra docs inside the skill directory.
- No options, modes, or variants nobody asked for.

## 3. Platform differences

| Concern | Claude variant | Codex variant |
|---|---|---|
| Reference another skill | `ai-toolkit:<name>` skill | `$<name>` |
| Bundled file in a command | `${CLAUDE_SKILL_DIR}/scripts/x` | path relative to the skill directory |
| Questions to the user | `AskUserQuestion` for choices; plain text for links and free text | one plain-text message |
| MCP setup snippet | `claude mcp add <name> -- <command>` or `.mcp.json` | `[mcp_servers.<name>]` in `~/.codex/config.toml` |
| Extra metadata | frontmatter only when needed: `allowed-tools`, `disable-model-invocation`, `argument-hint` | `agents/openai.yaml` |
| Explicit-only skills (side effects) | `disable-model-invocation: true` | `policy.allow_implicit_invocation: false` |

Codex `agents/openai.yaml`:

```yaml
interface:
  display_name: "Human Name"
  short_description: "One line for the skill picker"
  default_prompt: "Use $<name> to …"
dependencies:            # only for MCP servers the skill cannot work without
  tools:
    - type: "mcp"
      value: "figma"
      description: "Figma MCP server"
      transport: "streamable_http"
      url: "https://mcp.figma.com/mcp"
```

## 4. Change surgically

- When updating, touch only what the request needs. Do not reformat or reword unrelated sections.
- Apply the same change to both variants in the same task.
- Update the skill list in the root `README.md` when adding, renaming, or removing a skill.

## 5. Verify

1. `diff -r claude/skills/<name> codex/skills/<name>`: only platform lines and `agents/` differ.
2. `claude plugin validate ./claude` and `claude plugin validate .` pass.
3. Frontmatter and `openai.yaml` parse as YAML.
4. Trigger check: write 3 prompts that must trigger the skill and 2 that must not. Run each in a fresh
   session (`claude -p "<prompt>" --plugin-dir ./claude`; `codex exec "<prompt>"` with the skill
   installed) and confirm which skill loaded.
5. Run the skill on one realistic task. Fix what the model got wrong, then re-run.

Report changed files, trigger prompts with results, and checks that could not be run.
