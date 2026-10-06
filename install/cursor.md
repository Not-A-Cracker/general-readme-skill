# Installation — Cursor

## Setup

1. Create the rules directory:

```bash
mkdir -p .cursor/rules
```

2. Copy the skill file:

```bash
cp SKILL.md .cursor/rules/readme-write.mdc
```

3. Copy reference files:

```bash
cp -r references/ scripts/ .cursor/rules/
```

## Update companion

Keep the complete updater under the main rule's companion directory:

```bash
mkdir -p .cursor/rules/side-skills/readme-update-skill
cp side-skills/readme-update-skill/SKILL.md .cursor/rules/side-skills/readme-update-skill/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .cursor/rules/side-skills/readme-update-skill/
```

The main rule resolves Git-driven updates to this `SKILL.md`. Version confirmation or an explicit unchanged decision precedes edits; every existing language edition is inventoried. Verify actual rule loading in the host rather than assuming copied files prove integration.

## Usage

Open Cursor's AI chat (Cmd+L / Ctrl+L) and say "generate readme" or "write a README for this project".

## How It Works

Cursor loads `.mdc` files from `.cursor/rules/` as context for the AI. The reference files must be in the project so Cursor can read them when needed. The skill content is injected into the AI's context for README-related conversations.
