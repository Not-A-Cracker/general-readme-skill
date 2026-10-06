# Evidence and Safe Updates

## Evidence ledger

Keep a compact internal ledger; do not write it to the target repository without a request.

| Claim | Evidence required | Common mistake to avoid |
|---|---|---|
| Runtime / version | engines, runtime pin, manifest constraint, CI matrix with context | Latest CI version is not a supported minimum |
| Install command | packageManager/lockfile, documented distribution, build requirements | A package name does not prove publication |
| Start command | actual script/entry point plus prerequisite services | Inventing `npm start`, a port, or a Docker path |
| Framework / database | dependencies plus imports/configuration/use | Treating unused dependencies as architecture |
| Public API | actual exports, router mounts, schemas, middleware, tests | Listing a route without its prefix or auth exceptions |
| Config default | config reader/schema and documented example | Treating example values as defaults |
| Feature / performance | implementation/tests; reproducible benchmark for numerical claims | Converting adjectives in old docs into measured facts |
| Diagram edge | import, request, call, producer/consumer or configuration relation | Inferring communication from folder names |
| Platform integration | actual adapter/install instruction and compatible structure | Adding badges for the tool used to generate the README |
| License | actual LICENSE text and scope | Copying MIT from a template |

Record source path + line or manifest field, confidence (`verified`, `inferred`, `unknown`), and verification (`static`, `executed`, `rendered`). Publish verified facts. Use clearly qualified inference only when useful; omit unknown facts. Do not treat the offline checker as verification of feature claims.

Inspect real code/config when existing README prose conflicts. Do not copy secrets from `.env` or private git metadata. Use safe demonstrative values such as `YOUR_API_KEY` only when the actual interface requires a user-supplied value; explain how to obtain it. A necessary credential variable is not an unresolved template token.

## First-result contract

For each supported onboarding path, identify:

1. Starting location: repository root, package directory, or consumer project.
2. Supported prerequisites and required services.
3. Install/build/config/start sequence, using the project's package manager.
4. The smallest real invocation/example.
5. An observable result supported by tests/docs (output, UI, endpoint, or generated file).

Do not execute project commands during inspection. Statically verify script names, relative directories, flags, ports and service dependencies. Say "not runtime-tested" in delivery when applicable; never invent successful output.

Use subshells or explicit `cd ..` for sibling directories. For separate terminals, state the initial directory above each block. Do not force a monorepo or multi-service startup into four commands. Offer Docker first only when it is a verified, complete first-result path, not merely because a Dockerfile exists.

## Managed regions

For each newly generated section, use stable IDs independent of heading language:

```markdown
<!-- readme-skill:begin quick-start -->
## Quick Start

Content based on the actual project.
<!-- readme-skill:end quick-start -->
```

Use lowercase ASCII IDs with hyphens (`hero`, `quick-start`, `usage`, `configuration`, `api`). Preserve IDs when headings change or translate. Markers must be paired, uniquely identified, and never nested. Replace only the exact inclusive region. Keep the entire text outside those spans byte-for-byte when making managed updates.

Preserve explicit legacy manual regions, including their markers:

```markdown
<!-- MANUAL-START -->
Maintainer-written content.
<!-- MANUAL-END -->
```

Manual blocks inside a managed region remain intact. If a manual block contains a sensitive value or materially incorrect information, warn without reproducing it; request permission for that specific correction rather than silently changing it.

## Existing README decision table

For a Git-driven maintenance request routed to `readme-update`, actual version acceptance authorizes only narrow source-backed corrections of affected facts/current-version occurrences in unmarked sections. Preserve unrelated prose and design; do not regenerate whole sections or convert the document to managed content. Explicit manual blocks still require focused permission when a necessary correction is inside them. This exception is not whole-document rewrite authority and does not apply to general creation/redesign.

| Existing state | Action |
|---|---|
| No README | Create confirmed output paths with per-section managed markers |
| Paired managed regions | Update only selected managed regions; preserve manual blocks |
| Entirely unmarked | Treat as manual. Propose additions or ask for specific replacement scope |
| Old `AUTO-GENERATED` marker | Inspect boundaries; migrate only a clearly delimited region with consent |
| Old `BEAUTIFIED` marker | Ignore as update authorization and do not skip quality checks |
| Broken, nested, duplicate markers | Stop region replacement; name the ambiguity and request scope |
| Explicit whole-document rewrite request | Rewrite requested document, retaining explicit manual blocks |

"Use defaults" does not authorize replacing unmarked content. "Improve the Quick Start" authorizes a targeted edit of that section, not the whole README. For explicit rewrite, show a short change summary and preserve material maintainers' notes. Do not rewrite unrelated translations without a request.

## Idempotence and write scope

Before writing, find destination regions once and replace them in place. Do not append a duplicate section when its managed ID exists. Do not rely on heading string equality across languages. If a previously generated fact disappeared, remove it only inside its managed region; keep outside/manual text and report contradictions.

For additions to an unmarked README, preview which sections are being added and where. If an equivalent unmarked section exists, request focused replacement instead of appending another copy. Re-read the target region immediately before editing to preserve concurrent user edits.

Write only agreed README files and approved visual assets. Do not create preferences files, audit reports, secrets, build outputs, or a tracking directory in the target repository by default. Preserve existing translation paths and calculate local links from each file's parent directory.
