# Installation — GitHub Copilot

## Setup

1. Create the instructions directory:

```bash
mkdir -p .github
```

2. Copy the skill as Copilot instructions:

```bash
cp SKILL.md .github/copilot-instructions.md
```

3. Copy reference files:

```bash
mkdir -p .github/copilot-instructions
cp -r references/ scripts/ .github/copilot-instructions/
```

Resolve companion resources relative to `.github/copilot-instructions/`, not the workspace root. Installing only the single instructions file is insufficient. Merge into existing instructions rather than overwriting project/team conventions.

## Update companion

Keep a complete updater under the main instruction file's companion directory:

```bash
mkdir -p .github/copilot-instructions/side-skills/readme-update-skill
cp side-skills/readme-update-skill/SKILL.md .github/copilot-instructions/side-skills/readme-update-skill/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .github/copilot-instructions/side-skills/readme-update-skill/
```

The main entry resolves updates to that companion path. Version confirmation (or explicit unchanged) is required before edits; all existing language editions are included. This is a companion resource, not a claim that Copilot registers a new slash command.

## Usage

Open Copilot Chat in VS Code (Ctrl+Shift+I / Cmd+Shift+I) or JetBrains and say "generate readme" or "write a README for this project".

## How It Works

GitHub Copilot loads `.github/copilot-instructions.md` as custom instructions. These instructions are injected into all Copilot Chat conversations. The reference files must be in the repository so Copilot can read them.

## Notes

- Copilot's custom instructions are always active — the skill content will influence all conversations, not just README ones.
- If you only want the skill active for specific sessions, remove the instructions file when not needed.
