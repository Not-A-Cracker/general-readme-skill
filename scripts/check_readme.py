#!/usr/bin/env python3
"""Read-only, dependency-free README checks; not a full Markdown renderer."""

import argparse
import html
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

MAX_BYTES = 2 * 1024 * 1024
MANAGED = re.compile(r"<!--\s*readme-skill:(begin|end)\s+([a-z0-9]+(?:-[a-z0-9]+)*)\s*-->")
TEMPLATE = re.compile(
    r"\{(?:PROJECT_NAME|ONE_LINE_DESCRIPTION|SUBTITLE_WITH_KEYWORDS|KEYWORDS|"
    r"PLATFORM_BADGES|LANGUAGE_SWITCHER|QUICK_START_TEXT|LICENSE_TEXT|LICENSE_TYPE|COLOR)\}"
    r"|\b(?:YOUR_PROJECT_NAME|REPLACE_ME)\b|\{\{\s*[A-Z_]+\s*\}\}"
)
SECRET = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\bAKIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9]{36,}\b"
    r"|\bgithub_pat_[A-Za-z0-9_]{30,}\b|\bsk_live_[A-Za-z0-9]{20,}\b"
)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_LINK = re.compile(r"(!?)\[([^\]\n]*)\]\(\s*(<[^>\n]+>|(?:[^\s()\\]|\\.|\([^()\n]*\))+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
REFERENCE_DEF = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)", re.M)
REFERENCE_USE = re.compile(r"(!?)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?")
ENUMS = {
    "audience": {"users", "developers", "contributors"},
    "layout": {"compact", "balanced", "showcase"},
    "depth": {"short", "standard", "detailed"},
    "tone": {"professional", "minimal", "energetic"},
    "badge_style": {"none", "flat", "flat-square", "for-the-badge"},
    "visuals": {"none", "existing", "diagrams"},
    "update_mode": {"preserve", "rewrite"},
    "renderer": {"github", "portable"},
}
LANGUAGE = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


@dataclass
class Issue:
    severity: str
    code: str
    path: str
    line: int
    message: str


@dataclass
class Document:
    path: Path
    raw: str
    prose: str
    blocks: list
    anchors: set
    managed_ids: set


def slug(text):
    text = html.unescape(re.sub(r"<[^>]*>", "", text)).lower().strip()
    text = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").replace("~", "")
    return "".join(
        "-" if char.isspace() else char
        for char in text
        if char.isspace() or char in "-_" or unicodedata.category(char)[0] in "LN"
    )


def normalize_reference(label):
    return " ".join(label.split()).casefold()


def html_source(prose):
    return re.sub(
        r"<(?:[A-Za-z][A-Za-z0-9+.-]*:[^<>\s]*|[^<>\s@]+@[^<>\s@]+)>",
        lambda match: " " * len(match[0]),
        prose,
    )


class Elements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []
        self.anchors = set()
        self.tags = []
        self.headings = []
        self.heading = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]
        self.tags.append((tag, attrs, line))
        for key in ("id", "name" if tag == "a" else "id"):
            if attrs.get(key):
                self.anchors.add(attrs[key])
        if tag == "a" and "href" in attrs:
            self.links.append((attrs["href"] or "", line))
        if tag == "img":
            self.images.append((attrs.get("src") or "", attrs.get("alt") or "", line))
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = (tag, line, [])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if self.heading:
            self.heading[2].append(data)

    def handle_endtag(self, tag):
        if self.heading and self.heading[0] == tag:
            name, line, parts = self.heading
            self.headings.append((line, int(name[1]), "".join(parts)))
            self.heading = None


class Checker:
    def __init__(self, root, preferences=None):
        self.root = Path(root).resolve()
        self.preferences = preferences
        self.issues = []
        self.documents = {}
        self.checked = []

    def add(self, severity, code, path, line, message):
        self.issues.append(Issue(severity, code, str(path), line, message))

    def confined(self, path):
        path = Path(path).resolve()
        try:
            path.relative_to(self.root)
        except ValueError:
            return None
        return path

    def validate_preferences(self):
        prefs = self.preferences
        if prefs is None:
            return
        if not isinstance(prefs, dict):
            self.add("error", "preferences", self.root, 0, "Preferences must be an object.")
            self.preferences = None
            return
        status, source = prefs.get("status"), prefs.get("source")
        valid = isinstance(status, str) and isinstance(source, str) and (
            (status == "delegated" and source == "explicit_delegation") or (
                status == "confirmed" and source in {
                    "explicit_choices", "accepted_recommendation", "current_conversation"
                }
            )
        )
        if not valid:
            self.add("error", "preference-gate", self.root, 0, "A confirmed/delegated preference record is required; the script cannot prove consent.")
        for key, values in ENUMS.items():
            value = prefs.get(key)
            if not isinstance(value, str) or value not in values:
                self.add("error", "preferences", self.root, 0, "Invalid or missing setting: " + key)
        primary = prefs.get("primary_language")
        secondaries = prefs.get("secondary_languages")
        if not isinstance(primary, str) or not LANGUAGE.fullmatch(primary):
            self.add("error", "preferences", self.root, 0, "Invalid primary_language.")
        if not isinstance(secondaries, list) or any(
            not isinstance(code, str) or not LANGUAGE.fullmatch(code) for code in secondaries
        ):
            self.add("error", "preferences", self.root, 0, "Invalid secondary_languages.")
        elif len({code.casefold() for code in secondaries}) != len(secondaries) or (
            isinstance(primary, str) and primary.casefold() in {code.casefold() for code in secondaries}
        ):
            self.add("error", "preferences", self.root, 0, "Duplicate primary/secondary languages.")
        if not isinstance(prefs.get("emoji"), bool):
            self.add("error", "preferences", self.root, 0, "emoji must be a boolean.")
        project = prefs.get("project_root")
        if not isinstance(project, str) or not Path(project).is_absolute() or Path(project).resolve() != self.root:
            self.add("error", "preference-scope", self.root, 0, "Preference project_root must match the checked root.")
        self.preferences = dict(prefs)
        for key, values in ENUMS.items():
            value = prefs.get(key)
            if not isinstance(value, str) or value not in values:
                self.preferences.pop(key, None)
        if not isinstance(secondaries, list) or any(not isinstance(code, str) for code in secondaries):
            self.preferences.pop("secondary_languages", None)

    def load(self, path):
        resolved = self.confined(path)
        if resolved is None:
            self.add("error", "path-escape", path, 0, "Document resolves outside the project root.")
            return None
        if resolved in self.documents:
            return self.documents[resolved]
        try:
            if resolved.stat().st_size > MAX_BYTES:
                raise ValueError("Document exceeds the 2 MiB limit.")
            raw = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeError, ValueError) as exc:
            self.add("error", "read-failure", resolved, 0, str(exc))
            return None
        lines = raw.splitlines(keepends=True)
        visible = []
        blocks = []
        opened = None
        body = []
        for number, line in enumerate(lines, 1):
            match = FENCE.match(line.rstrip("\r\n"))
            if opened:
                visible.append("\n" if line.endswith("\n") else "")
                if match and match[1][0] == opened[0][0] and len(match[1]) >= len(opened[0]) and not match[2].strip():
                    blocks.append((opened[1], opened[2], "".join(body)))
                    opened, body = None, []
                else:
                    body.append(line)
            elif match:
                opened = (match[1], number, match[2].strip().split()[0] if match[2].strip() else "")
                visible.append("\n" if line.endswith("\n") else "")
            elif line.startswith("    ") or line.startswith("\t"):
                visible.append("\n" if line.endswith("\n") else "")
            else:
                visible.append(line)
        if opened:
            self.add("error", "unclosed-fence", resolved, opened[1], "Code fence is not closed.")
        prose = "".join(visible)
        parser = Elements()
        parser.feed(html_source(re.sub(r"(`+)([^`\n]*?)\1", lambda m: " " * len(m[0]), prose)))
        headings = list(parser.headings)
        prose_lines = prose.splitlines()
        for number, line in enumerate(prose_lines, 1):
            match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if match:
                headings.append((number, len(match[1]), match[2]))
            elif number > 1 and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line) and prose_lines[number - 2].strip():
                headings.append((number - 1, 1 if "=" in line else 2, prose_lines[number - 2]))
        anchors = set(parser.anchors)
        seen = Counter()
        previous_level = 0
        for number, level, title in sorted(headings):
            base = slug(title)
            anchor = base if not seen[base] else base + "-" + str(seen[base])
            while anchor in anchors:
                seen[base] += 1
                anchor = base + "-" + str(seen[base])
            seen[base] += 1
            anchors.add(anchor)
            if previous_level and level > previous_level + 1:
                self.add("warning", "heading-level", resolved, number, "Heading skips a level.")
            previous_level = level
        h1s = [item for item in headings if item[1] == 1]
        if len(h1s) != 1:
            self.add("warning", "title-count", resolved, 1, "Expected exactly one H1 title.")
        ids = self.check_markers(resolved, prose)
        doc = Document(resolved, raw, prose, blocks, anchors, ids)
        self.documents[resolved] = doc
        return doc

    def check_markers(self, path, prose):
        active = None
        ids = set()
        manual = False
        markers = re.finditer(r"<!--\s*(?:readme-skill:[^>]*|MANUAL-START|MANUAL-END)\s*-->", prose)
        for marker in markers:
            line = prose.count("\n", 0, marker.start()) + 1
            text = marker[0]
            match = MANAGED.fullmatch(text)
            if "MANUAL-START" in text:
                if manual:
                    self.add("error", "manual-markers", path, line, "Nested manual region.")
                manual = True
            elif "MANUAL-END" in text:
                if not manual:
                    self.add("error", "manual-markers", path, line, "Manual end without start.")
                manual = False
            elif not match:
                self.add("error", "managed-markers", path, line, "Malformed managed marker.")
            elif manual:
                self.add("error", "managed-markers", path, line, "Managed boundary inside a manual block.")
            elif match[1] == "begin":
                if active or match[2] in ids:
                    self.add("error", "managed-markers", path, line, "Nested or duplicate managed region.")
                ids.add(match[2])
                active = match[2]
            elif active != match[2]:
                self.add("error", "managed-markers", path, line, "Mismatched managed end.")
            else:
                active = None
        if active:
            self.add("error", "managed-markers", path, 1, "Unclosed managed region.")
        if manual:
            self.add("error", "manual-markers", path, 1, "Unclosed manual region.")
        if "<!-- AUTO-GENERATED -->" in prose or "<!-- BEAUTIFIED -->" in prose:
            self.add("warning", "legacy-marker", path, 1, "Legacy marker does not define safe update boundaries.")
        return ids

    def check_link(self, doc, target, line):
        target = html.unescape(target.strip().strip("<>"))
        if not target:
            self.add("error", "empty-link", doc.path, line, "Empty link destination.")
            return
        try:
            parts = urlsplit(target)
        except ValueError:
            self.add("error", "invalid-link", doc.path, line, "Malformed link destination.")
            return
        if parts.scheme.lower() in {"javascript", "data", "vbscript", "file"}:
            self.add("error", "unsafe-link", doc.path, line, "Unsafe or non-portable URI scheme.")
            return
        if parts.scheme or parts.netloc:
            return
        local = unquote(parts.path)
        if local.startswith("/"):
            self.add("error", "absolute-local-link", doc.path, line, "Use a relative repository link, not an absolute path.")
            return
        candidate = self.confined(doc.path.parent / local) if local else doc.path
        if candidate is None:
            self.add("error", "path-escape", doc.path, line, "Local link resolves outside the project root.")
            return
        if not candidate.exists():
            self.add("error", "missing-local-link", doc.path, line, "Local target does not exist: " + local)
            return
        if parts.fragment and (not local or candidate.suffix.lower() in {".md", ".markdown"}):
            linked = doc if candidate == doc.path else self.load(candidate)
            if linked and unquote(parts.fragment) not in linked.anchors:
                self.add("error", "missing-anchor", doc.path, line, "Heading/anchor target does not exist: " + unquote(parts.fragment))

    def check(self, path):
        doc = self.load(path)
        if not doc:
            return
        self.checked.append(doc)
        prose = re.sub(r"(`+)([^`\n]*?)\1", lambda m: " " * len(m[0]), doc.prose)
        refs = {normalize_reference(m[1]): m[2] for m in REFERENCE_DEF.finditer(prose)}
        masked = list(prose)
        images = []
        for match in INLINE_LINK.finditer(prose):
            line = prose.count("\n", 0, match.start()) + 1
            self.check_link(doc, match[3], line)
            if match[1]:
                images.append((match[3], match[2], line))
            masked[match.start():match.end()] = " " * len(match[0])
        for match in REFERENCE_DEF.finditer(prose):
            self.check_link(doc, match[2], prose.count("\n", 0, match.start()) + 1)
            masked[match.start():match.end()] = " " * len(match[0])
        for match in REFERENCE_USE.finditer("".join(masked)):
            label = normalize_reference(match[3] or match[2])
            line = prose.count("\n", 0, match.start()) + 1
            if label in refs:
                if match[1]:
                    images.append((refs[label], match[2], line))
            elif match[3] is not None:
                self.add("error", "missing-reference", doc.path, line, "Undefined reference link: " + label)
        parser = Elements()
        parser.feed(html_source(prose))
        images.extend(parser.images)
        for target, line in parser.links:
            self.check_link(doc, target, line)
        for target, alt, line in images:
            if not alt.strip():
                self.add("error", "image-alt", doc.path, line, "Image needs descriptive alt text.")
        for target, _, line in parser.images:
            self.check_link(doc, target, line)
        for tag, attrs, line in parser.tags:
            if tag in {"script", "iframe", "style", "form", "object", "embed"} or any(key.startswith("on") for key in attrs):
                self.add("error", "unsafe-html", doc.path, line, "Unsupported active HTML element or event handler.")
        for pattern, code, message in (
            (TEMPLATE, "template-token", "Unresolved template token."),
            (SECRET, "possible-secret", "Potential secret material; value suppressed."),
        ):
            for match in pattern.finditer(doc.raw):
                self.add("error", code, doc.path, doc.raw.count("\n", 0, match.start()) + 1, message)
        for line, language, body in doc.blocks:
            if language.casefold() != "mermaid":
                continue
            clean = re.sub(r"%%\{.*?\}%%", "", body, flags=re.S)
            statements = [s.strip() for s in clean.splitlines() if s.strip() and not s.lstrip().startswith("%%")]
            first = statements[0] if statements else ""
            if not re.match(r"^(?:graph|flowchart|sequenceDiagram|classDiagram|erDiagram|stateDiagram(?:-v2)?|pie|gantt|journey|gitGraph|mindmap|timeline|quadrantChart|xychart-beta|block-beta|architecture-beta|packet-beta|sankey-beta|requirementDiagram|C4Context|C4Container|C4Component)\b", first):
                self.add("error", "mermaid-type", doc.path, line, "Mermaid block lacks a supported diagram declaration.")
            if first.startswith("sequenceDiagram") and re.search(r"^\s*class(?:Def)?\s", clean, re.M):
                self.add("error", "mermaid-sequence-class", doc.path, line, "Flowchart classes are invalid in sequence diagrams.")
        badges = [(url, line) for url, _, line in images if "img.shields.io/" in url]
        first_h2 = re.search(r"^##\s", doc.prose, re.M)
        hero_line = doc.prose.count("\n", 0, first_h2.start()) + 1 if first_h2 else len(doc.prose.splitlines()) + 1
        hero_badges = [item for item in badges if item[1] < hero_line]
        prefs = self.preferences or {}
        budget = 2 if prefs.get("layout") == "compact" else 4
        if len(hero_badges) > budget:
            self.add("warning", "badge-budget", doc.path, 1, "Hero exceeds the layout's badge budget.")
        if prefs.get("badge_style") == "none" and badges:
            self.add("error", "preference-badges", doc.path, 1, "Badges conflict with badge_style=none.")
        if prefs.get("badge_style") in {"flat", "flat-square", "for-the-badge"}:
            for url, line in badges:
                try:
                    query = urlsplit(html.unescape(url.strip("<>"))).query
                except ValueError:
                    continue
                style = parse_qs(query).get("style", ["flat"])[0]
                if style != prefs["badge_style"]:
                    self.add("error", "preference-badges", doc.path, line, "Badge style differs from confirmed preferences.")
        if prefs.get("visuals") == "none" and (len(images) > len(badges) or any(language.casefold() == "mermaid" for _, language, _ in doc.blocks)):
            self.add("error", "preference-visuals", doc.path, 1, "Visuals conflict with visuals=none.")
        if prefs.get("renderer") == "portable" and (parser.tags or any(language.casefold() == "mermaid" for _, language, _ in doc.blocks)):
            self.add("error", "preference-portable", doc.path, 1, "HTML/Mermaid conflicts with portable output.")
        if prefs.get("layout") == "compact" and any(tag.startswith("h") or (attrs.get("align") == "center") for tag, attrs, _ in parser.tags):
            self.add("error", "preference-layout", doc.path, 1, "HTML Hero conflicts with compact layout.")

    def finish(self):
        prefs = self.preferences or {}
        if prefs.get("secondary_languages") and len(self.checked) > 1:
            expected = self.checked[0].managed_ids
            for doc in self.checked[1:]:
                if doc.managed_ids != expected:
                    self.add("error", "translation-regions", doc.path, 1, "Managed region IDs differ across the supplied translation set.")
        if prefs.get("secondary_languages") and len(self.checked) < 1 + len(prefs["secondary_languages"]):
            self.add("warning", "translation-coverage", self.root, 0, "Not all requested translations were supplied for checking.")
        return self.issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Target repository root")
    parser.add_argument("--preferences", type=Path, help="Optional user-authorized preference record")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable report")
    parser.add_argument("readmes", nargs="+", type=Path)
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        parser.error("--root must be an existing directory")
    prefs = None
    if args.preferences:
        try:
            if args.preferences.stat().st_size > MAX_BYTES:
                raise ValueError("Preferences exceed the size limit")
            prefs = json.loads(args.preferences.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError) as exc:
            parser.error("Cannot read preferences: " + str(exc))
    checker = Checker(args.root, prefs)
    checker.validate_preferences()
    for path in args.readmes:
        checker.check(path if path.is_absolute() else args.root / path)
    issues = checker.finish()
    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "issues": [asdict(issue) for issue in issues], "limitations": ["offline static checks only", "no command execution", "no network or rendering", "no proof of user consent"]}, ensure_ascii=False, indent=2))
    else:
        for issue in issues:
            print(f"{issue.severity.upper()} {issue.code} {issue.path}:{issue.line}: {issue.message}")
        print(f"{errors} error(s), {warnings} warning(s). Static checks only; no runtime/network/rendering verification.")
    if any(issue.code == "read-failure" for issue in issues):
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
