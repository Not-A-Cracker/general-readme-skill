# Badge Styles

Three visual styles for shields.io badges. Choose one at generation time.

---

## Style A: Flat

Parameter: `style=flat`

Clean, compact, standard. The default style. Works well for any project.

```markdown
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=node.js&logoColor=white)
```

---

## Style B: Flat-square

Parameter: `style=flat-square`

Slightly different visual weight. Sharper edges, more modern feel.

```markdown
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white)
```

---

## Style C: for-the-badge

Parameter: `style=for-the-badge`

Taller, bolder, more visual impact. Takes more horizontal space — use one badge per line or a 2-per-line grid.

```markdown
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
```

---

## Badge Grouping Rules

Apply the confirmed badge style consistently, including any requested CTA badges. `none` means no badge images. Limit the Hero to 2 badges for compact or 4 for balanced/showcase. The groups below are candidate pools, not required rows: choose only useful, verified identity badges and avoid a badge wall. Do not add AI IDE badges unless the target project actually integrates with those platforms. Keep each image tag readable in source.

### Line 1 — Identity (max 4)

These establish what the project is:
- **Build status** — dynamic badge only with the actual repository, workflow filename and branch; CI configuration alone does not establish a passing build
- **Version** — npm/crates.io/pypi badge if the project is published
- **License** — from LICENSE file
- **Primary language** — the main language badge

If fewer than 4 apply, use fewer. Don't pad.

### Line 2 — Tech Stack (max 6)

Grouped by category, ordered by importance:
1. Primary language (if not on line 1)
2. Framework
3. Database
4. Key tools (Docker, Kubernetes, etc.)

Only include technologies actually used in the project. Not devDependencies (unless they're significant like test frameworks: Jest, Pytest, etc.). If the list exceeds 6, pick the 6 most important.

### Line 3+ — Conditional (only if relevant)

These badges only appear when the data exists:
- **Downloads** — published packages only
- **Stars** — if the repo has significant stars
- **Coverage** — if test coverage is configured
- **Node/Python/Go version** — if `engines` or runtime version is specified

Never include conditional badges without actual repository/package/service identifiers. Do not infer publication, stars, downloads or coverage from a manifest or CI file. Do not claim a badge was fetched or rendered when no network/rendering check occurred. Prefer omitting optional live metrics over inventing values.

---

## Dynamic Badges

For badges that show live data (version, downloads, stars, build status), use shields.io dynamic endpoints:

```markdown
![npm version](https://img.shields.io/npm/v/package-name)
![npm downloads](https://img.shields.io/npm/dm/package-name)
![GitHub stars](https://img.shields.io/github/stars/user/repo)
![Build status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)
```

These require the actual repo/package name from the project. Never hardcode placeholder names.

---

## Static Badges

For badges that don't change (license, language, framework), use shields.io static endpoints:

```markdown
![License](https://img.shields.io/badge/license-MIT-green)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
```

The logo parameter uses Simple Icons slugs. Full list: https://simpleicons.org/
