#!/usr/bin/env python3
"""PreToolUse guard for git calls inside Bash commands.

Pushing is the user's job: in theme repos a push to main deploys to production.
Commits carry no Co-Authored-By trailer. Committing on main needs confirmation.

  git push origin main                         -> deny
  git commit -m "x" --trailer "Co-Authored-By: ..." -> deny
  git commit -m "x"        (on main)           -> ask
  git commit -m "x"        (on feature)        -> no decision

Quotes are ignored, so `bash -c "git push"` is caught. git counts only at the
start of a command (after env assignments and wrappers like sudo, env, bash -c),
so "git push" inside a commit message is not.
"""

import json
import os
import re
import subprocess
import sys

# Shell separators that start a new command: ; & | && || newline ` $( )
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;&|\n`()]|\$\(")
QUOTES = re.compile(r"[\"']")
CO_AUTHOR = re.compile(r"co-authored-by", re.IGNORECASE)
ENV_ASSIGNMENT = re.compile(r"^\w+=\S*$")

# Tokens allowed before git in a command: sudo env GIT_X=1 bash -c git ...
PREFIXES = {"sudo", "env", "command", "exec", "time", "nohup", "xargs", "bash", "sh", "zsh", "-c", "-lc"}

MAIN_BRANCH = "main"

# Global git options whose value is the next token: git -C <dir> commit.
VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
MESSAGE_FILE_OPTIONS = {"-F", "--file"}


class Decision:
    DENY = "deny"
    ASK = "ask"


def git_calls(command, cwd):
    """Yield (subcommand, args, repo_dir) for every git invocation; follows `cd <dir>`."""
    for segment in SEGMENT_SPLIT.split(command):
        tokens = QUOTES.sub("", segment).split()

        if tokens[:1] == ["cd"] and len(tokens) > 1:
            cwd = os.path.join(cwd, os.path.expanduser(tokens[1]))
            continue

        for i, token in enumerate(tokens):
            if os.path.basename(token) == "git":
                parsed = parse(tokens[i + 1 :], cwd)
                if parsed:
                    yield parsed
                break

            if token not in PREFIXES and not ENV_ASSIGNMENT.match(token):
                break


def parse(tokens, cwd):
    """Split `[-C dir] <subcommand> args...` into (subcommand, args, repo_dir)."""
    repo = cwd
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in VALUE_OPTIONS and i + 1 < len(tokens):
            if token == "-C":
                repo = os.path.join(repo, os.path.expanduser(tokens[i + 1]))
            i += 2
            continue

        if token.startswith("-"):
            i += 1
            continue

        return token, tokens[i + 1 :], repo
    return None


def current_branch(repo):
    try:
        result = subprocess.run(["git", "-C", repo, "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def message_file_has_co_author(args, repo):
    """True when `-F <file>` / `--file=<file>` points to a message with a Co-Authored-By trailer."""
    for i, arg in enumerate(args):
        path = None
        if arg in MESSAGE_FILE_OPTIONS and i + 1 < len(args):
            path = args[i + 1]
        elif arg.startswith("--file="):
            path = arg.split("=", 1)[1]

        if not path or path == "-":
            continue

        try:
            with open(os.path.join(repo, os.path.expanduser(path)), encoding="utf-8", errors="ignore") as f:
                if CO_AUTHOR.search(f.read()):
                    return True
        except OSError:
            continue
    return False


def check(subcommand, args, repo, command):
    """Return (decision, reason) for one invocation, or None."""
    if subcommand == "push":
        return Decision.DENY, "git push is blocked: the user pushes (push to main deploys to production)."

    if subcommand != "commit":
        return None

    # The message may span heredoc lines split into other segments: scan the whole command.
    if CO_AUTHOR.search(command) or message_file_has_co_author(args, repo):
        return Decision.DENY, "Commit messages must not contain a Co-Authored-By trailer."

    if current_branch(repo) == MAIN_BRANCH:
        return Decision.ASK, f"Commit on {MAIN_BRANCH}: confirm."

    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return

    command = payload.get("tool_input", {}).get("command", "")
    if "git" not in command:
        return

    cwd = payload.get("cwd") or os.getcwd()
    results = [result for call in git_calls(command, cwd) if (result := check(*call, command))]
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
