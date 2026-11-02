#!/usr/bin/env python3
"""PreToolUse guard for WP-CLI calls inside Bash commands.

Denies commands that destroy data, break the site or reach another environment.
Asks before arbitrary code, deletions and publishing. Everything else gets no
decision, so the user's normal permission rules apply.

  wp db drop                      -> deny
  wp @prod post list              -> deny
  wp eval-file fix.php            -> ask
  wp post get 12                  -> no decision

Matching is conservative: quotes are ignored, so "wp db drop" inside a string
or a `bash -c` argument is caught too.
"""

import json
import os
import re
import sys

WP_BINARIES = {"wp", "wp-cli.phar"}

# Shell separators that start a new command: ; & | && || newline ` $( )
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;&|\n`()]|\$\(")
QUOTES = re.compile(r"[\"']")

REMOTE_FLAGS = ("--ssh", "--http")
DRY_RUN_FLAG = "--dry-run"
PUBLISH_FLAG = "--post_status=publish"

# Fixed seed script shipped with figma-to-acf; running it needs no prompt.
SEED_SCRIPT = "skills/figma-to-acf/scripts/seed-page.php"

PACKAGE_WRITES = ("install", "update", "delete", "uninstall", "activate", "deactivate", "toggle")
CORE_WRITES = ("download", "install", "update", "update-db", "multisite-install", "multisite-convert")

# Positional prefixes: ("db", "drop") matches `wp --quiet db drop --yes`.
DENY_RULES = [
    *[("db", sub) for sub in ("drop", "reset", "import", "clean")],
    ("site", "empty"),
    ("site", "delete"),
    *[("core", sub) for sub in CORE_WRITES],
    *[("plugin", sub) for sub in PACKAGE_WRITES],
    *[("theme", sub) for sub in PACKAGE_WRITES],
    ("user",),
    ("config",),
]

ASK_RULES = [
    ("eval",),
    ("eval-file",),
    ("shell",),
    ("db", "query"),
    ("db", "cli"),
    ("post", "delete"),
    ("option", "update"),
    ("option", "delete"),
    ("cron", "event", "run"),
]


class Decision:
    DENY = "deny"
    ASK = "ask"


def wp_calls(command):
    """Yield the argument list of every WP-CLI invocation in the command."""
    for segment in SEGMENT_SPLIT.split(command):
        tokens = QUOTES.sub("", segment).split()

        for i, token in enumerate(tokens):
            if os.path.basename(token) in WP_BINARIES:
                yield tokens[i + 1 :]


def matches(positional, rules):
    return any(tuple(positional[: len(rule)]) == rule for rule in rules)


def is_seed_script(positional, cwd):
    """True for `wp eval-file <plugin>/skills/figma-to-acf/scripts/seed-page.php`."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root or len(positional) < 2:
        return False

    script = os.path.realpath(os.path.join(cwd, positional[1]))
    return script == os.path.realpath(os.path.join(plugin_root, SEED_SCRIPT))


def check(args, cwd):
    """Return (decision, reason) for one invocation, or None."""
    positional = [arg for arg in args if not arg.startswith("-")]
    flags = [arg for arg in args if arg.startswith("-")]

    if any(arg.startswith("@") for arg in positional) or any(flag.split("=")[0] in REMOTE_FLAGS for flag in flags):
        return Decision.DENY, "WP-CLI must run against the local install only (no aliases, --ssh, --http)."

    if matches(positional, DENY_RULES):
        return Decision.DENY, f"Blocked WP-CLI command: wp {' '.join(positional[:2])}."

    if positional[:1] == ["search-replace"] and DRY_RUN_FLAG not in flags:
        return Decision.DENY, "wp search-replace is allowed only with --dry-run."

    if positional[:1] == ["eval-file"] and is_seed_script(positional, cwd):
        return None

    if matches(positional, ASK_RULES):
        return Decision.ASK, f"WP-CLI runs code or changes site state: wp {' '.join(positional[:2])}."

    if PUBLISH_FLAG in flags:
        return Decision.ASK, "WP-CLI command publishes content."

    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return

    command = payload.get("tool_input", {}).get("command", "")
    if "wp" not in command:
        return

    cwd = payload.get("cwd") or os.getcwd()
    results = [result for args in wp_calls(command) if (result := check(args, cwd))]
    if not results:
        return

    # Deny wins over ask.
    decision, reason = next((r for r in results if r[0] == Decision.DENY), results[0])
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
