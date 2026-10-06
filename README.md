# General README Skill

Create useful, evidence-based README files with AI coding assistants—confirm the reader's preferences, show a real first result, and design for clarity rather than decoration.

![License: MIT](https://img.shields.io/badge/license-MIT-2563eb?style=flat)
![Skill version: 2.0.0](https://img.shields.io/badge/skill-2.0.0-334155?style=flat)

English · [中文](assets/README-zh.md)

[Quick Start](#quick-start) · [Preferences](#preferences) · [Quality Checks](#quality-checks)

## Quick Start

The core skill uses native agent read/search/edit tools. No runtime, third-party CLI, or network service is required for generation. The optional offline checker requires **Python 3.9+**, with no third-party packages.

### Install the complete skill

Copy `SKILL.md`, `references/`, and `scripts/` together into the host's skill location. Keep their relative paths intact; installing only `SKILL.md` leaves the workflow incomplete.

For a project-level Claude Code installation, run from this repository's root:

```bash
mkdir -p .claude/skills/general-readme
cp SKILL.md .claude/skills/general-readme/
cp -r references/ scripts/ .claude/skills/general-readme/
```

For another target project, use that project's absolute skill directory as the destination. Do not overwrite existing team instructions.

See the integration guides: [Claude Code](install/claude-code.md), [GitHub Copilot](install/copilot.md), [Cursor](install/cursor.md). These describe file placement; host loading and tool availability must be verified in the installed host. Natural-language invocation is the portable option; `/readme` is a skill trigger phrase, not a guaranteed registered slash command in every host.

### Get the first result

Ask the host agent:

> 帮我写 README

The first response should bundle the unresolved preferences and **stop until you answer**. Reply with your choices or “用推荐配置”. After acceptance, the agent inspects static project evidence, edits the agreed README paths, and reports what was checked.

To delegate choices explicitly:

> 生成 README，不用问，英文，面向开发者，均衡布局，其余你决定。

Delegation does not authorize deleting manual content or executing project installation/startup commands.

## What 2.0 Changes

| User pain | Upgrade |
|---|---|
| The agent forgets to ask preferences | An entry gate requires an actual reply or explicit delegation before scanning/generation |
| Attractive but unusable setup instructions | Commands, working directories, prerequisites and the first example must have project evidence |
| Every README looks like the same badge wall | Compact, balanced and showcase layouts; relevant badges only; visuals stay optional |
| Updating destroys maintainer-written content | Paired managed regions; unmarked text is manual; narrow replacement scope |
| Small projects get unnecessary architecture/API sections | Reader-focused routing for apps, libraries, CLIs, monorepos, skills and docs-only projects |
| Translated READMEs have broken links | Per-file relative paths, translated fragments and consistent managed IDs |
| “Generated successfully” hides untested claims | Offline checks plus an explicit distinction between static, runtime and rendering verification |

The skill is instructional, not an enforcement engine. The new gate and evaluation cases reduce omission risk; actual agent compliance still needs host-level testing.

## Preferences

Choose independently instead of accepting an all-purpose template:

| Preference | Options |
|---|---|
| Language | Primary language plus only requested translations |
| Reader | Users, developers or contributors |
| Layout | Compact, balanced or showcase |
| Depth | Short, standard or detailed |
| Tone | Professional, minimal or energetic |
| Badges | None, flat, flat-square or for-the-badge |
| Visuals | None, relevant existing assets or evidence-backed diagrams |
| Updates | Preserve by default; rewrite only within authorized scope |
| Rendering | GitHub or portable Markdown |
| Emoji | Off unless explicitly requested |

The proposed baseline is the request's language, users, balanced, standard, professional, flat, existing visuals, preserve and GitHub. **Recommendations are not consent.** “Make it beautiful” does not authorize silently choosing all defaults.

Use one reply, for example:

> 英文，面向开发者，简短，纯 Markdown，不要徽章，不要图，其余按推荐。

`--no-beautify` selects compact layout only. `--yes`, “use defaults” or “you decide” delegate unresolved preferences. A follow-up in the same project can reuse an actual confirmed conversation record; a later invocation or lost context must not infer consent from the README's appearance.

## Design That Serves the Reader

| Layout | Best fit | Presentation |
|---|---|---|
| **Compact** | Small libraries and CLIs | Left-aligned Markdown, code early, at most 2 badges, no decorative Hero |
| **Balanced** | Most repositories | Clear title and next action, at most 4 badges, one useful existing visual |
| **Showcase** | Products with a real demo | Optional centered Hero, text action links, one genuine screenshot; Markdown body |

Tone is separate from layout. Professional does not mean centered HTML. Energetic does not mean emoji. Portable rendering stays Markdown-only.

A real screenshot is useful; a fictional generated UI is not. An architecture diagram is optional and must explain source-backed relationships. The assistant used to generate the document is not automatically a supported platform badge.

## Workflow

**Confirm → Inspect → Plan → Compose → Check → Deliver**

1. **Confirm:** ask once, wait, then summarize resolved preferences.
2. **Inspect:** read manifests, entry points, examples/tests and relevant config; do not execute project code or read real credentials.
3. **Plan:** choose a first-result path and only useful sections; identify safe update boundaries.
4. **Compose:** apply content and design together; load reference material only when relevant.
5. **Check:** trace factual claims, review paths/anchors/markers and match the confirmed preferences.
6. **Deliver:** edit only agreed files and report actual checks and remaining uncertainty.

The entry point is [`SKILL.md`](SKILL.md). Detailed protocols live in [`references/`](references/).

## Safe Updates

New generated sections use stable paired markers:

```markdown
<!-- readme-skill:begin usage -->
## Usage

Project-specific content.
<!-- readme-skill:end usage -->
```

Update only the managed span; preserve text outside it and explicit `MANUAL-START` / `MANUAL-END` blocks. Unmarked existing sections are manual. Legacy `AUTO-GENERATED` or `BEAUTIFIED` comments are not blanket overwrite permission.

For an unmarked document, ask for a focused replacement scope when needed instead of rewriting it or adding a duplicate section. See [evidence and update rules](references/evidence-and-updates.md).

## Quality Checks

From this repository's root, check a target project without executing its code:

```bash
python3 scripts/check_readme.py --root /absolute/path/to/project /absolute/path/to/project/README.md
```

Add `--json` for a machine-readable report. If the user authorized a saved preference record, supply `--preferences /path/to/preferences.json`; no state file is created by default.

The checker detects missing local paths/anchors, image alt omissions, unclosed fences, broken managed/manual markers, known template remnants, high-confidence secret formats, selected Mermaid mistakes and preference-dependent layout conflicts. It rejects local links escaping the project root. Exit codes: `0` no errors, `1` validation errors, `2` invocation/read failures. Warnings are reported separately.

It **does not** prove user consent, factual accuracy, executable examples, remote-link availability, full Mermaid validity or GitHub rendering. See [quality checks and limitations](references/quality-checks.md).

### Regression suite

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Automated tests cover the checker and skill contract. [`tests/behavior-cases.json`](tests/behavior-cases.json) contains 17 scenarios for actual host-agent evaluation, including bare invocation, partial preferences, context loss, monorepos and manual preservation. These are evaluation specifications, not a claim that every host has passed.

## Development Direction

Prioritize **preference reliability → credible first use → safe maintenance → adaptive visual design**. Do not spend the next iteration primarily adding badge mappings or larger HTML templates.

Next validation work should run the behavioral scenarios on real host agents, then compare rendered READMEs from representative applications, libraries, CLIs and monorepos. Use the [design rubric](references/quality-checks.md#design-acceptance-rubric) to assess clarity, usefulness, restraint and maintainability. Prefer measured outcomes over aesthetic promises.

## Repository Map

| Path | Purpose |
|---|---|
| `SKILL.md` | Skill entry point and mandatory workflow |
| `references/preference-gate.md` | Question, state contract and recovery |
| `references/evidence-and-updates.md` | Evidence ledger and manual-safe edits |
| `references/section-guidelines.md` | Project-specific reader journeys |
| `references/beautification-rules.md` | Layout and visual design system |
| `references/quality-checks.md` | Validation scope and evaluation rubric |
| `references/badge-styles.md`, `references/badges.md` | Optional badge guidance and mappings |
| `references/diagram-templates.md`, `references/language-guide.md` | Optional diagrams and translations |
| `scripts/check_readme.py` | Read-only offline checker |
| `tests/` | Automated checks and behavioral scenarios |
| `examples/` | Legacy illustrative outputs, not source-verified golden fixtures |
| `install/` | Host integration guides |
| `assets/` | Existing artwork and translated documentation |

The Japanese, Korean and Russian documents currently retain the 1.x guide with an explicit legacy notice; use this page or the Chinese guide for the 2.0 workflow.

## Contributing

When changing workflow rules, update the relevant reference and add a behavioral scenario. When changing the checker, add a failing/passing fixture to the unit tests and run the regression suite. Do not label a scenario as host-validated without recording an actual host run.

## License

[MIT](LICENSE)
