# Section Guidelines

Use sections as a reader journey, not a mandatory checklist. Apply the confirmed audience, depth, layout, and update scope from `SKILL.md`. Use `beautification-rules.md` for visual patterns; do not duplicate Hero templates here.

## Global writing rules

- State what the project does, who it is for, and how to get a first result.
- Prefer specific, source-backed facts. Use performance numbers only with reproducible benchmark evidence.
- Avoid filler: "powerful", "robust", "versatile", "leverages", "seamlessly", "cutting-edge", "state-of-the-art", "game-changing", "revolutionary", "next-generation", "best-in-class", "enterprise-grade".
- Omit unsupported/empty sections. Do not fill with N/A, Coming soon, generic architecture, or assumed contribution policies.
- Keep prose natural and concise. Minimal tone needs no introductory sentence in every section.
- Use no emoji unless explicitly requested. Treat all sample content as a format example, not project facts.
- Preserve manual content and use paired managed-region markers for new generated sections.

## Project routing

| Type | Prioritize | Add only when useful |
|---|---|---|
| Application / static site | Real demo/screenshot, prerequisites, coherent local startup, first UI action | Configuration, deployment, source-backed architecture |
| Library | Verified installation/distribution, import + minimal example + result | Public exports, compatibility, advanced use |
| CLI | Installation, executable name, one real invocation, documented output | Options table, troubleshooting, shell compatibility |
| Monorepo | Package map, required services, root/package working directories | Separate package links instead of exhaustive APIs |
| Agent skill / plugin | Installation scope, actual entry point/invocation, expected interaction | Integration adapters and host limitations |
| Docs-only | Purpose, entry pages, navigation, how to use/contribute | No invented runtime; the flowchart shows how to use the material |

Order Hero → first result → capabilities/usage → workflow flowchart → reference → maintainer links by default. Every language edition uses the identical order. Move capabilities before first result when readers need context. Keep quick-start early; never move manual sections just to impose this order.

## Hero

Use one H1 with the actual name from manifest or verified existing documentation. Describe the outcome in one sentence; avoid a list of technology keywords as the main description. Use optional navigation to existing sections. Badge/image/HTML choices must match confirmed layout. Do not imply the project supports the assistant used to generate the README.

## Capabilities / Why

Select 2–6 real differentiators, or fewer if justified. Explain the benefit, not just a dependency name. Use a list for short descriptions; use a table only for genuine comparison. Omit if the introduction and minimal usage already explain the value. Do not convert test coverage, speed or security aspirations into factual claims.

## Quick Start / First Result

Document the complete smallest supported path:

1. Verified prerequisites and starting directory.
2. Installation/build using the declared package manager and actual distribution method.
3. Required configuration and services, if any.
4. Start/invoke/import and an evidence-backed observable result.

Aim for a few logical steps without a fixed command ceiling. State directory context and separate terminals explicitly. Use subshells for sibling packages. Do not assume Docker is easier; promote it only when the available files provide a complete path. Use minimum runtime versions only when declared. Do not infer package publication from a package manifest. Do not show output that was neither documented nor tested.

## Usage

Start with one real example from implementation/tests/examples and add up to three advanced cases when needed. Keep imports, options, API keys and return shape accurate. Use fenced blocks with language hints. Preserve executable code and explain necessary user-supplied values; do not use unfinished `xxx` or invented API methods.

## Workflow / Architecture (required)

Every README has this section, or places the flowchart in the section where it naturally explains the project (Usage for a library, Quick Start for a skill). The flowchart shows the real primary flow, derived from verified relationships; when relationships cannot be proven, it shows the verified install → configure → run → result workflow. Add a one-sentence lead-in only if the tone allows. A sequence diagram may supplement it for a specific interaction; a function library need not have a class diagram. Read `diagram-templates.md` for the required rules. Default Mermaid themes are acceptable; diagram-specific syntax takes priority over styling. Use a fenced text flowchart for portable rendering. Do not create an SVG asset without authorization.

## Configuration

Include actual public configuration keys even if they are read in source rather than a config file. Use a concise table: key | purpose | required | default. Distinguish a documented example from a real runtime default. Link `.env.example`/schema when present. Never read/copy real credential files; do not expose passwords, tokens, private URLs, or personal data. Explain necessary user-provided secrets without supplying real ones.

## Public API

For libraries, describe exported functions/types and supported signatures. For REST, include mounted path, method, request shape and auth rules with exceptions. Trace router prefixes and middleware. For GraphQL/gRPC, describe actual schema/service methods. Do not state that every route requires authentication when login/registration/public routes are exceptions. Link larger existing API documentation instead of duplicating everything.

## Navigation / Directory Structure / Tech Stack

Use a package map or depth-2/3 annotated tree only when it helps readers navigate. Include only existing paths; ignore generated/cache/dependency folders. Explain top-level responsibilities from evidence. Include a small tech table only when it adds useful context; do not list every dependency or repeat all Hero badges.

## Deployment and Troubleshooting

Document deployment only with a verified configuration and required setup; CI existence does not imply a passing build or deployment pipeline. Link actual workflows. Include troubleshooting for evidenced failure conditions, with a diagnosis and specific remedy; do not invent errors to fill a section.

## Contributing and License

Link existing contribution rules. Include actual development/test commands only if declared; do not invent commit conventions. Add a license name/link only after reading the actual license. Resolve links from each output file's directory. Mention missing/ambiguous licensing in delivery, not as a fabricated section or badge.

## Content budgets

Treat short (~80–150 lines), standard (~150–300), and detailed as ceilings to guide reduction, not minimum targets. Let small projects be much shorter. Prioritize first-result clarity over a line quota. Link optional long references; keep first-use code visible. Ensure headings, links, translations, and managed IDs are checked after composition.
