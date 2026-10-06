# README Design System

Compose content and visual hierarchy together after preference confirmation. Do not run an automatic HTML transformation or ask for beautification after writing. Treat `BEAUTIFIED` as a legacy marker, not a reason to skip checks.

## Layout presets

| Preset | Hero | Navigation | Visuals | Badge budget |
|---|---|---|---|---|
| compact | Markdown H1 + one sentence | Usually unnecessary | No decorative images; the mandatory flowchart only | 0–2 |
| balanced | Markdown H1 + short description | Plain text links when the document is long | Mandatory flowchart plus one real screenshot when useful | 0–4 |
| showcase | Optional centered HTML title/description | 1–2 plain-text action links | Mandatory flowchart plus one real product/demo image | 0–4 |

Apply `renderer=portable` as Markdown-only, even with showcase spacing. Keep tone independent: professional does not mean centered, and energetic does not mean emoji. Use no emoji unless requested.

## First screen

Make purpose and next action visible without scrolling through badge walls:

1. One project title; no duplicate H1.
2. One concrete sentence: outcome + intended reader/context.
3. A small row of relevant status/identity badges, or none.
4. One obvious next step: Quick Start, install/use, or docs navigation.
5. A real image only if it conveys the product better than text.

Prefer text action links over badges that masquerade as buttons. Do not add a keyword subtitle that repeats the description. Put longer API/config/package references after the first successful use path. Add a table of contents only when navigation genuinely benefits; do not duplicate the Hero action links and a short document's entire section list.

## Compact and balanced pattern

```markdown
# Project Name

One concrete sentence describing the outcome and intended reader.

[Quick Start](#quick-start) · [Usage](#usage)

## Quick Start

Verified commands and a first useful example.
```

Use this as a structural pattern only; replace sample text with project evidence. Do not copy links for sections that do not exist. Compute heading fragments for the actual language. Keep prose and code readable in the raw file.

## Showcase pattern

```html
<h1 align="center">Project Name</h1>
<p align="center">One concrete, evidence-based description.</p>
<p align="center">
  <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a>
</p>
```

Escape text in HTML. Use Markdown for the body, with blank lines after HTML blocks. Do not wrap the entire README in a `<div>` because Markdown rendering can change. Do not insert Markdown syntax inside raw HTML paragraphs. Use only GitHub-supported simple HTML; no CSS, scripts, forms, iframes, fixed-width multi-column grids, or base64 images.

## Image policy

- Prefer existing screenshots, terminal captures, or diagrams tied to the real project.
- Inspect an asset before using it. A generic marketing poster is not proof of a functioning UI.
- Use descriptive alt text explaining what is shown. Do not use "image" or "screenshot" alone.
- Keep one Hero image; avoid huge screenshots with unreadable text. Prefer a responsive image with no fixed pixel width in Markdown.
- Use an existing `<picture>` dark/light pair only when both assets exist and are appropriate.
- Do not create images/assets unless requested. Do not fabricate a product screenshot or workflow result.
- Mention image size concerns in delivery; do not silently rewrite or compress existing binaries.

## Whitespace, hierarchy and density

Use one H1, H2 for primary sections, H3 for steps; do not skip levels. Keep paragraphs short. Use lists for capabilities, tables for comparison/configuration, and fenced blocks for commands. Do not force every feature into a table. Avoid horizontal rules between every section.

Keep install and first-use instructions visible, not inside `<details>`. Collapse only long optional output/advanced references for GitHub rendering, never for portable mode. Avoid wide tables, giant directory trees, and line-wrapped diagrams. Use depth-2/3 trees only when readers need navigation; link to folders when clearer.

Use one consistent badge style. Keep identity badges in the Hero; put secondary technology details in prose or a concise table. Add AI IDE/platform badges only for real target-project integrations. Prefer the project's existing brand colors for approved visuals; never enforce white text on every colored background.

## Diagrams

Every layout, including compact, contains at least one flowchart of the real primary flow (see `diagram-templates.md`); no image preference removes it. Other diagram types are optional extras that need verified relationships. Prefer 3–8 nodes, top-down flow on narrow screens, and short source-backed labels. Never derive edges solely from a directory tree, and keep node IDs and edges identical across language editions.

Use Mermaid's diagram-specific syntax: flowcharts may use `classDef`; sequence diagrams should use native participant/message styling or theme defaults, not flowchart classes. Default themes are acceptable. Use dark fills with light text or light fills with dark text, checking contrast. Split/group a large graph or link existing detailed docs; do not automatically create SVG files because a node count threshold was crossed.

## Design review

Check the first screen, narrow-screen plausibility, badge count, image usefulness, code visibility, heading hierarchy, and maintenance readability. Respect compact/none/portable choices before aesthetic preferences. If no browser/GitHub render was performed, describe this as a source-level design review, not a screenshot-verified result.
