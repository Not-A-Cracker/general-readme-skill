# Quality Checks and Evaluation

## Two distinct quality layers

1. **Behavioral compliance:** Did the host agent ask, stop and wait for actual preference acceptance? Did it preserve manual content and respect write scope? Evaluate with `tests/behavior-cases.json` against the actual agent/tool trace.
2. **Artifact quality:** Are the generated README's paths, headings, fences, managed regions, image alt text, placeholders and preference-dependent layout internally consistent? Use the offline checker and a human/source review.

Do not claim that a static script forces agent behavior or proves beauty, feature accuracy, executable examples, native-language quality, live links, or GitHub rendering.

## Offline checker

Use Python 3.9+ with no third-party packages. Resolve the script path relative to this installed skill, not the target repository. Supply the target root and one or more README paths explicitly:

```bash
python3 /installed/skill/scripts/check_readme.py --root /target/project /target/project/README.md
```

Optionally supply `--preferences /path/to/user-authorized-record.json` and `--json`. Never create a preferences file in the target repository just to run a check. The internal preference record can be checked manually instead.

The checker reads only explicitly supplied documents and referenced local Markdown files. It does not run commands or access the network. It rejects paths escaping the project root, including symlink escapes. Documents over 2 MiB are rejected. Its supported Markdown subset includes backtick/tilde fences, ATX/setext headings, inline and reference links/images, HTML links/images/anchors, duplicate heading fragments, and paired managed/manual regions.

Exit codes: `0` = no errors (warnings may remain); `1` = artifact/preference errors; `2` = invalid invocation/read failure. In JSON output, report the exact error and warning counts. Report warnings separately; do not describe "exit 0" as "everything verified".

Checks include:
- Missing local files/images, unresolved local heading fragments, reference destinations and root confinement.
- Missing image alt text, unclosed fences and selected unsafe HTML elements.
- Duplicate/nested/unpaired managed markers, manual blocks and legacy markers.
- Known unresolved template tokens and high-confidence secret formats, without printing the secret value.
- Mermaid block type presence and flowchart-only classes in sequence diagrams; **not full Mermaid syntax validation**.
- Excessive Hero badges, duplicate H1, heading-level jumps, and preference/layout consistency when a record is supplied.
- Equivalent managed ID sets across the supplied translation set when preferences specify translations.

GitHub fragment generation is approximated for normal text, Unicode, inline formatting and duplicates. Complex inline HTML/entities/custom rendering may need an actual GitHub review. Unrecognized URI schemes and HTML features should be reviewed manually. Do not promise complete Markdown parsing, network reachability or zero false positives.

## Source review before output

- Trace actual script/entry names and working directories; verify sibling package transitions and separately labeled terminals.
- Verify publication, runtime minimums, router prefixes/auth exceptions, public exports and configuration defaults from evidence.
- Keep quick start visible, a real first use example, and a supported observable result.
- Verify visuals describe the actual project; do not substitute a generic AI-generated screenshot.
- Diff manual/outside-managed spans; compare the same generated-region update twice to detect duplicate additions.
- Compare facts/code/region IDs across generated translations and calculate links per file directory.
- Fix new errors within scope. Report pre-existing manual issues without rewriting them silently.

## Host-agent regression protocol

For each behavioral case, provide its conversation to the actual host with the skill installed. Record the first response, tool calls before user acceptance, files touched, final document and verification claims. Check the case's `must`/`must_not` assertions. Mark a case `not_run` when no actual host execution occurred; inspecting JSON scenarios is not a behavioral pass.

The highest-priority regression is bare `/readme`: it must produce one bundled question, no implementation scan/write, and no draft before the user reply. Also test explicit delegation, partial answers, no beautification, context loss, unmarked/manual updates, monorepos and docs-only projects.

## Design acceptance rubric

Score each dimension 0 (missing), 1 (needs work), or 2 (clear):

| Dimension | Acceptance signal |
|---|---|
| First screen | Purpose, intended reader and next action are immediately clear |
| First result | Supported setup + example + observable result with no guessing |
| Hierarchy | Short paragraphs, deliberate headings, useful—not repetitive—navigation |
| Restraint | No padding, badge wall, invented diagram or duplicated tech inventory |
| Visual value | Real, readable asset or useful diagram; absence is acceptable when unnecessary |
| Maintenance | Clean Markdown body, safe updates, accurate relative links |

Aim for 10/12 or better, but never use a score to override privacy, consent, evidence, or manual preservation. A source review can assess structure; actual appearance requires a real renderer. If no browser/GitHub rendering or runtime test was performed, explicitly say so in the delivery summary.
