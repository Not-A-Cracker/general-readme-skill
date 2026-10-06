# Version Consent and Complete Language Synchronization

## Target-project version, not tool version

Read the selected project's public version fields and current-version README statements as candidates. A root monorepo can contain several package versions; an installed skill's own metadata is not the target application version. Do not infer a release number from the latest Git tag, a branch name or conventional commit type.

Ask for one of:

- An exact target version (including a supported prerelease/custom version scheme).
- Explicitly keep the version unchanged; if no version exists, do not introduce one.

Do not choose patch/minor/major without a user decision. If the user already said “更新到 2.3.0” or “版本不变”, record it and proceed; do not ask again. “你决定/默认即可/不要问” without a version decision does not satisfy the gate. In that case ask only the version question, not a full redesign questionnaire.

Read-only preflight can precede the question; writes cannot. Bundle genuine baseline/package/release-scope ambiguity with the version question to avoid multiple menus. Keep the actual user reply in conversation state. A metadata file alone is not consent. `VERSION_REQUIRED` is the unattended failure mode.

## Decision contract

Keep this internal record without creating a file by default:

```json
{
  "project_root": "/absolute/target/project",
  "version_action": "set",
  "target_version": "2.3.0",
  "version_scope": "readme",
  "source": "explicit_user_reply",
  "preserve_existing_design": true,
  "all_language_editions": true
}
```

For `keep`, omit `target_version`. Validate the exact value against the actual project's version scheme when known. If the supplied value would be unsafe in Markdown, HTML, URLs or shell examples, escape it appropriately; never interpolate it into shell commands. Ask if a semantic ambiguity prevents a reliable update.

Version acceptance authorizes narrow evidence-based changes to affected unmarked README facts and current-version occurrences, not whole-document rewrite. Preserve design choices and explicit manual blocks. If a correction is inside a manual block, request targeted permission. Follow the main skill's paired managed regions when available; do not blanket-convert unmarked documents to managed regions.

## Occurrence classification

Classify version-like strings before editing:

| Occurrence | `set` action | `keep` action |
|---|---|---|
| Current project version statement | Replace with exact chosen version in every edition | Leave unchanged |
| Static current-project version badge | Update label/value safely; preserve style | Leave unchanged |
| Current install command pinned to project release | Update only if it actually targets this project and the target distribution is valid; disclose unpublished assumptions | Leave version pin unchanged |
| Existing current release link | Update only when the selected release/artifact is verified or user provided its destination | Leave unchanged |
| Dynamic registry/version badge | Preserve true endpoint; add text if necessary, never fake live release status | Preserve endpoint |
| Runtime/dependency/package-other-than-target | Do not change | Do not change |
| API protocol version such as `/api/v1` | Do not change unless code actually changed it | Update protocol only when code actually changed it; not a release-version bump |
| Historical changelog / migration example | Preserve history unless specifically requested | Preserve |
| Main/side skill metadata in another installed tool | Never substitute target project's version | Preserve |

Do not perform global replacement of `1.2.3`. A chosen release version does not prove publication. When a version pin/link cannot be updated honestly, report it as unresolved, propose a valid source-build/unpinned alternative and ask if needed. Do not claim complete version synchronization with unresolved current pins or links.

For `set` when a family has no version statement, add one short native-language line near the introduction or existing release information, consistently across that family's editions. Do not duplicate it on a later run. For `keep`, leave inconsistent existing version literals unchanged and report the mismatch; never silently align them with manifests. Content changes can still be synchronized.

Default to README-only scope. Explicit manifest/lockfile/tag requests are separate release operations; clarify selected package(s) and actual release tooling. Do not stage, commit, create tags or publish releases without a corresponding request. The side skill's metadata is not a project-release manifest.

## Discover every language edition

Start with tracked paths, untracked paths and a bounded first-party file walk so ignored translation files are not missed. Match README names case-insensitively, including `README.md`, `README-zh.md`, `README.zh-CN.md`, `README_ja.md`, `docs/zh/README.md`, `assets/README-ko.md`, and existing extensionless/RST/text editions. Skip `.git`, dependencies, build output, caches and vendored third-party trees. Do not follow symlinks outside the authorized root. A deleted tracked README is a candidate needing explicit disposition, not a new file to recreate silently.

Classify into families using:

1. Language-switcher links and explicit primary/translated headings.
2. Same project/package identity and equivalent document purpose.
3. Locale filenames/directories as supporting evidence only.

Separate a monorepo package README, a dependency README, a tutorial sample and an actual translation. Include every edition of each impacted family. For a workspace-wide update, evaluate every first-party family for impact; mark unrelated package guides no-change rather than translating root content into them.

For unsupported-format or unreadable editions, report and resolve the limitation. Do not say “all README files updated” while silently skipping RST, a missing file, a nested language directory, or a protected manual region. Never fabricate a missing translation language file. If the user explicitly excludes a language, respect it and report the resulting incomplete synchronization scope.

## Synchronization matrix

Keep an internal per-file matrix:

| File / language / family | Existing state | Affected facts | Version action | Result |
|---|---|---|---|---|
| Primary | Read and scoped | Canonical fact delta | set/keep | updated/no-change/unresolved |
| Every edition | Read and compared | Same fact delta localized | same decision | updated/no-change/excluded with reason/unresolved |

Do not equate identical section IDs with semantic parity. Legacy translations can have older structure or missing sections. All editions must end up identical to the primary apart from the language (see `placement-and-parity.md`): bring a diverged edition to the canonical structure built from the verified union of facts, placing each fact at the same natural position, and report the repair. Request a focused insertion/correction when ambiguity or manual protection blocks it; an unresolved edition means the set is not synchronized.

Use one canonical verified change set. Translate prose naturally into every existing edition. Keep executable code, commands, options, variable names, target-version literals, API paths and public export names equivalent. Translate headings where appropriate and recompute fragment links. Compute each image/license/docs/switcher path from the destination file's parent, never reuse `LICENSE` blindly for `assets/README-zh.md`.

## Before claiming completion

- Compare candidate inventory with the synchronization matrix; every candidate has a disposition.
- Verify every included family member received the same applicable facts and version decision.
- Preserve dependencies, history, manual notes, layout and uncommitted maintainer edits.
- Inspect a final narrow diff for each edited file; verify no unrelated manifest/tag/config changes.
- Run local link/fence/marker checks for all included Markdown editions with the main checker when available.
- Report no-change files as checked, not edited. Keep unresolved editions/version targets explicit.
- Do not claim runtime, remote publication, native-speaker review or GitHub rendering checks without performing them.

For no public code delta + `keep`, return a verified no-op. For version-only `set`, update current-version documentation across all editions without inventing feature changes or a changelog.
