# Installation — Claude Code

The skill is named `readme-write`; the source directory keeps its historical name `general-readme-skill`. Install the destination directory as `readme-write`.

## Quick Setup

Copy the skill files to your project:

```bash
mkdir -p .claude/skills/readme-write
cp SKILL.md .claude/skills/readme-write/
cp -r references/ scripts/ .claude/skills/readme-write/
```

## Global Installation

To make the skill available across all your projects:

```bash
mkdir -p ~/.claude/skills/readme-write
cp SKILL.md ~/.claude/skills/readme-write/
cp -r references/ scripts/ ~/.claude/skills/readme-write/
```

## Update companion

From this repository's root, install the updater alongside the main skill. Its skill name is `readme-update` (the source directory is `side-skills/readme-update-skill`):

```bash
mkdir -p .claude/skills/readme-update
cp side-skills/readme-update-skill/SKILL.md .claude/skills/readme-update/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .claude/skills/readme-update/
```

For global installation, use `~/.claude/skills/readme-update/` as the destination. Say “update README”; the updater asks for the target project version or unchanged, then checks local Git deltas, places each change in its natural section of every existing language edition, keeps all editions identical apart from language, and keeps the flowchart current. It does not modify manifests/tags by default. Keep both skills' reference directories separate.

## Usage

Say "generate readme" in a session where the installed skill is available. `/readme-write` and `/readme` are trigger phrases; verify slash-command registration/skill invocation behavior in the actual host.

## How It Works

Keep the entry point and companion resources together under `.claude/skills/`. When the host loads this skill for a README task, its 2.0 workflow first asks a bundled question about unresolved language, reader, depth and design preferences, then waits. Explicit delegation can skip that question. Every README it writes contains a flowchart, and all language editions are identical apart from the language. Verify actual loading in the host; file placement alone is not a host-level test.
