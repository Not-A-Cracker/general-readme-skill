# Natural Placement, Flowchart Maintenance and Language Parity

Updates are woven into the existing document where each fact belongs. They are never appended at the beginning or end because that is the easy place to write. Every edition ends up identical apart from the language, and every README keeps a current flowchart.

## 1. Place each fact at its natural position

Resolve every reader-facing fact to a home section, then to an exact position inside it:

| Fact | Home and position |
|---|---|
| Runtime / prerequisite | Quick Start prerequisites, ordered with existing prerequisites |
| Install, build or configure step | Quick Start, at its execution order between the steps it depends on |
| CLI flag / option | The options table or usage list, next to related options, following the table's existing order |
| Public export, function or class | The API/usage reference, inside the group of related items |
| HTTP endpoint | The API table, under its resource group after related routes |
| Configuration key | The configuration table, inside its group, following existing ordering |
| New or changed capability | The capabilities list, by relevance; merge with a similar item instead of adding a seventh |
| Deployment change | The deployment section, in procedure order |
| New or moved package | The package map, at the position matching dependency or startup order |
| Removed or renamed behavior | Edit or delete the existing statement in place |
| Current version | The existing version statement or badge; if none exists, beside the title/intro or existing release information |
| Flow change | The flowchart node or edge at its position in the flow |

Rules:

1. **Find the anchor first.** Pick the semantically closest existing item or section and insert adjacent to it, following the local ordering convention (alphabetical, execution order, importance or resource grouping).
2. **Edit before adding.** Prefer changing an existing sentence, row or step. Merge duplicates. Keep list and table sizes within the project's own limits by merging related items.
3. **Never default to the top or bottom.** The beginning or end is acceptable only when it is genuinely the natural position (the project description in the Hero, the last step of a sequence, License at the end). State why in the placement record.
4. **No update log inside the README.** Do not add "What's new", "Recent changes", "Update 1.5" or dated notes unless the user explicitly asks for a changelog.
5. **A missing home section is created in order.** Place it by the document's reader-journey order, adjacent to its most related section, using each language's existing heading style. Do not tack it on at the end.
6. **Match surroundings.** Keep table columns, list markers, heading levels, tone and formatting of the neighbouring content.
7. **Respect protected content.** Insert outside `MANUAL-START`/`MANUAL-END` blocks; if the natural position is inside one, ask for focused permission.

Keep an internal placement record per fact: `fact → section → anchor (previous/next sibling) → index → rationale`. The record is identical for every language edition. Do not write it to the repository.

## 2. Keep the flowchart present and current

- **Every README has a flowchart.** A Mermaid `flowchart`/`graph` block is required (a fenced `text` flowchart with arrows when the document is portable Markdown). A sequence, class, ER or state diagram does not count. If a legacy README has none, add one in its natural section, derived from evidence, in every edition; this is part of the standing requirement, not a separate request.
- **Update it in place when the flow changes.** A new stage, service, command, route or package adds a node and edges at its position in the flow; a rename edits the label; removed components lose their nodes and edges. Keep existing node IDs stable and give new nodes unique IDs.
- **Verify when the flow is unchanged.** Check that the diagram still matches the current code and leave it untouched.
- **Stay readable.** Keep 3–8 nodes by grouping related steps instead of growing the diagram indefinitely. Base edges on imports, calls, routes or configuration; when relationships cannot be proven, draw the verified install → configure → run → result workflow.
- **Same structure in every edition.** Identical node IDs and edges; only labels are translated.

## 3. Language parity

Every edition stays identical to the primary in everything except the language: section order and heading levels, tables (rows and columns), list items, code blocks and commands, flowchart nodes and edges, links and targets, images, badges, HTML structure, managed-region IDs and facts. Only prose, headings, labels, alt text and code comments are translated.

1. Treat the primary's structure as canonical. If editions have already diverged (missing sections, stale legacy content, extra edition-specific parts), build the canonical structure from the verified union of facts and bring every edition to it. Report this repair as part of the update.
2. Apply each placement at the same position in every edition.
3. Translate naturally; keep commands, flags, imports, paths, node IDs, link targets and version literals identical. Recompute relative paths and translated heading fragments per file.
4. Never leave a fact in only some editions; if one edition cannot be updated, report it as unresolved and do not call the set synchronized.

## 4. Verify

Run the main skill's checker over the primary first and then every translation:

```bash
python3 /installed/readme-write/scripts/check_readme.py --root /absolute/target --require-flowchart --parity README.md assets/README-zh.md assets/README-ja.md
```

If the checker is unavailable, compare manually: heading outline, table row/column counts, list-item counts, code blocks, flowchart node and edge lists, link targets, images and badges. Also confirm that each new fact sits at its recorded position and that nothing was appended to the beginning or end without a stated reason. A parity pass proves identical structure only; it does not prove translation accuracy, so read the translated sentences. Do not claim rendering was verified unless a real renderer was used.
