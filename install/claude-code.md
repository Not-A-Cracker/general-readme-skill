# Installation — Claude Code

## Quick Setup

Copy the skill files to your project:

```bash
mkdir -p .claude/skills/general-readme
cp SKILL.md .claude/skills/general-readme/
cp -r references/ scripts/ .claude/skills/general-readme/
```

## Global Installation

To make the skill available across all your projects:

```bash
mkdir -p ~/.claude/skills/general-readme
cp SKILL.md ~/.claude/skills/general-readme/
cp -r references/ scripts/ ~/.claude/skills/general-readme/
```

## Usage

Say "generate readme" in a session where the installed skill is available. `/readme` is a trigger phrase; verify slash-command registration/skill invocation behavior in the actual host.

## How It Works

Keep the entry point and companion resources together under `.claude/skills/`. When the host loads this skill for a README task, its 2.0 workflow first asks a bundled question about unresolved language, reader, depth and design preferences, then waits. Explicit delegation can skip that question. Verify actual loading in the host; file placement alone is not a host-level test.
