# Local Git Delta Protocol

## Safety and scope

Inspect Git locally without changing repository state. Disable pagers, optional index writes, external diff/textconv, fsmonitor hooks, configured clean/process filters, and lazy/network fetching. The script reads filter configuration and overrides clean/process/required settings only for its commands; it does not write Git config. Report transformed-file comparison limits. Use `--ignore-submodules=none` so configured ignore policies cannot hide gitlink/dirty changes. Stop inventory recursion at gitlinks/nested Git repositories and report their boundaries; do not read child source without authorization. Treat directory traversal errors as incomplete inventory, not successful coverage. Never run commit hooks, fetch/pull, checkout, stash, reset, clean, add, commit, tag, config writes, or project commands. Do not read commit author/email fields, credential files, or whole sensitive patches.

Resolve the explicit target root and check it is the intended repository. When invoking the bundled script, pass the Git repository root as `--root`; the script rejects a nested directory instead of silently broadening scope. For a package request, collect the authorized repository report but filter impact to that package and shared interfaces before editing. Do not inspect a child submodule without permission to include its code scope.

Use argument arrays, never shell interpolation of paths or refs. Use literal pathspecs and `--` before paths. NUL-delimit filename records; filenames may contain spaces, Unicode, tabs, newlines or leading hyphens. Validate refs with `rev-parse --verify --end-of-options <ref>^{commit}` before diffing the resolved commit hash. Reject invalid refs and do not fall back silently.

## Baseline policy

Choose in this order:

1. The user-provided local commit/tag or range start.
2. A previously confirmed baseline in this conversation, if still valid for the same project.
3. Propose the last commit touching the primary README as a **heuristic**; announce it and its limits.

Do not blindly use the newest tag, `HEAD~1`, or a tag named like the requested version. The newest tag may belong to another package. A README formatting commit may be newer than its actual semantic coverage, and translations may lag behind the primary.

When using the heuristic, inspect the last-touch commits of other language editions and audit their affected facts against current source. Older edition touch commits are a lag signal, not proof of staleness. Do not use a README-only working-tree edit to conclude code documentation is current. If the heuristic misses obviously stale facts, inspect older history for the relevant files or ask for an intended release baseline.

Report shallow history and missing ancestors. If there is no committed primary README, no HEAD, or no Git repository, do not invent a baseline. Show available working-tree information and request an explicit baseline/current-state audit. A `--base` error is a blocker, not a reason to silently generate using partial evidence.

## Include every change layer

| Layer | Local Git source | Meaning |
|---|---|---|
| committed | `git diff --name-status -z -M BASE HEAD --` | Committed changes after the baseline |
| staged | `git diff --cached --name-status -z -M --` | Index relative to HEAD (or empty tree in a new repo) |
| unstaged | `git diff --name-status -z -M --` | Working tree relative to index |
| untracked | `git ls-files --others --exclude-standard -z` | New files not in the index |
| net tracked | `git diff --name-status -z -M BASE --` | Current working tree relative to baseline |

Add `--no-ext-diff --no-textconv` to all diff commands. Read `git ls-files -u -z` to identify conflicts. The script emits paths/statuses only, never code or raw patches. Use native tools to inspect relevant public source and tests afterward. Preserve the distinction between committed release content and local uncommitted work.

A reverted addition can appear in committed/staged layers but disappear from the net current-state delta. Do not document removed/reverted features as present. Retain rename source and destination; deletion must remove stale reader-facing documentation, not create a new description for a nonexistent file. A gitlink change means a submodule pointer changed, not that its actual public API has been inspected.

## Script interface

```bash
python3 /installed/readme-update/scripts/git_readme_delta.py --root /absolute/repository
python3 /installed/readme-update/scripts/git_readme_delta.py --root /absolute/repository --base v1.2.0
```

Optional `--primary docs/README.md` selects the baseline document when root README is not the primary guide. Optional `--max-files 20000` changes the inventory limit. The default limit is 10,000 candidates/files per change list. Overflow raises an error rather than silently dropping editions. The script requires Python 3.9+ and a local Git binary; it creates no state/report files, reads no code contents and performs no network operations.

JSON contains `head`, `baseline`, `shallow`, `layers`, `readmes`, `conflicts`, and `warnings`. Every README candidate has a path, present/missing status, tracked/ignored classification and last-touch commit where available. Inventory includes ignored first-party READMEs because translated docs may be under a ignored `docs/` directory. It does not scan skipped dependency/build/vendor directories or follow symlinks. Filename candidates are not semantic translation families; the agent must classify them from content/switchers.

Exit `0`: report created, possibly with limitations requiring a question. Exit `1`: Git/scope/ref/limit failure, JSON error; no update should proceed automatically. A no-baseline or unborn report is not evidence of a complete committed delta. Check `warnings` and `baseline.commit`, not only the exit status.

## Native-tool fallback

If Python is unavailable but Git can run, use the same read-only commands through approved native command tools. If command permissions are denied, do not bypass denial using a script or subagent. Report that Git inspection is blocked and ask for an explicit diff or authorized static audit.

If Git itself is missing, request a user-provided diff/range or permission for current-state comparison. Do not call static file discovery “Git delta analysis”. For relevant source changes, inspect entry points, tests and consumers to map actual behavior—not commit subjects or dependency names—to README facts.
