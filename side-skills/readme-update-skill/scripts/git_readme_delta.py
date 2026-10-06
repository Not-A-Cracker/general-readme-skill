#!/usr/bin/env python3
"""Report local Git change layers and README paths without changing the repo."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "third_party", "third-party", "build",
    "dist", "__pycache__", ".venv", "venv", ".next", "coverage", "logs",
    ".cache", "target", ".tox", "site-packages", "bower_components",
}
README_NAME = re.compile(r"^readme(?:(?:[-_.][^.]+)*\.(?:md|markdown|mdown|rst|txt)|[-_][^.]+)?$", re.I)


class DeltaError(Exception):
    pass


def decode(value):
    return value.decode("utf-8", errors="surrogateescape")


def is_readme(path):
    return bool(README_NAME.fullmatch(Path(path).name))


def first_party(path):
    return not any(part.casefold() in SKIP_DIRS for part in Path(path).parts[:-1])


class GitReader:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith("GIT_"):
                self.env.pop(key)
        self.env.update({
            "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
            "GIT_NO_LAZY_FETCH": "1", "GIT_PAGER": "cat", "PAGER": "cat",
            "GIT_LITERAL_PATHSPECS": "1", "LC_ALL": "C",
        })

        self.filter_overrides = []
        filters = self.run("config", "--null", "--get-regexp", r"^filter\..*\.(clean|process|required)$", optional=True)
        drivers = set()
        for item in (filters or b"").split(b"\0"):
            key = decode(item.partition(b"\n")[0])
            match = re.fullmatch(r"filter\.(.+)\.(?:clean|process|required)", key)
            if match:
                drivers.add(match[1])
        for driver in sorted(drivers):
            self.filter_overrides.extend([
                "-c", "filter." + driver + ".clean=", "-c", "filter." + driver + ".process=",
                "-c", "filter." + driver + ".required=false",
            ])

    def run(self, *args, optional=False):
        command = [
            "git", "--no-pager", "-c", "core.fsmonitor=false", "-c",
            "diff.external=", "-c", "core.quotePath=false", "-c", "protocol.allow=never",
            "-C", str(self.root),
        ] + self.filter_overrides + list(args)
        env = self.env.copy()
        if args and args[0] == "check-ignore":
            env.pop("GIT_LITERAL_PATHSPECS", None)
        try:
            result = subprocess.run(command, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=60, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise DeltaError("Git is unavailable or timed out: " + str(exc)) from exc
        if result.returncode:
            if optional:
                return None
            raise DeltaError("Local Git inspection failed: " + " ".join(args[:2]))
        return result.stdout

    def diff(self, *revisions, cached=False):
        args = ["diff", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none", "--name-status", "-z", "-M"]
        if cached:
            args.append("--cached")
        return parse_changes(self.run(*(args + list(revisions) + ["--"])))


def parse_changes(data):
    tokens = data.split(b"\0")
    if tokens and not tokens[-1]:
        tokens.pop()
    records = []
    index = 0
    while index < len(tokens):
        status = decode(tokens[index])
        index += 1
        count = 2 if status[:1] in {"R", "C"} else 1
        if not re.fullmatch(r"[ACDMRTUXB][0-9]*", status) or index + count > len(tokens):
            raise DeltaError("Malformed NUL-delimited Git change record.")
        paths = [decode(value) for value in tokens[index:index + count]]
        index += count
        record = {"status": status, "path": paths[-1]}
        if count == 2:
            record["old_path"] = paths[0]
        records.append(record)
    return records


def split_paths(data):
    return [decode(item) for item in data.split(b"\0") if item]


def walk_readmes(root, max_files, gitlinks=()):
    found = set()
    boundaries = set(gitlinks)
    visited = 0

    def scan_error(error):
        raise DeltaError("README inventory is incomplete: a first-party directory could not be scanned.") from error

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=scan_error):
        kept = []
        for name in sorted(dirs):
            child = Path(directory) / name
            relative = child.relative_to(root).as_posix()
            if name.casefold() in SKIP_DIRS or child.is_symlink():
                continue
            if relative in boundaries or (child / ".git").exists():
                boundaries.add(relative)
                continue
            kept.append(name)
        dirs[:] = kept
        for name in files:
            visited += 1
            if visited > max_files:
                raise DeltaError("First-party file inventory limit exceeded; increase --max-files or narrow scope.")
            path = Path(directory) / name
            if is_readme(name) and not path.is_symlink():
                found.add(path.relative_to(root).as_posix())
    return found, boundaries


def last_touch(git, path):
    result = git.run("log", "-1", "--format=%H", "--", path, optional=True)
    return decode(result).strip() if result else None


def choose_primary(readmes, selected=None):
    if selected is not None:
        if selected not in readmes:
            raise DeltaError("--primary must identify a discovered README inside the repository.")
        return selected
    for name in ("README.md", "readme.md", "README.markdown", "README.rst", "README", "README.txt"):
        if name in readmes:
            return name
    root_candidates = sorted(path for path in readmes if "/" not in path and Path(path).name.casefold() in {"readme.md", "readme.markdown", "readme.rst", "readme", "readme.txt"})
    return root_candidates[0] if root_candidates else None


def collect(root, base=None, primary=None, max_files=10000):
    root = Path(root).resolve()
    if not root.is_dir():
        raise DeltaError("--root must be an existing repository directory.")
    if max_files < 1:
        raise DeltaError("--max-files must be positive.")
    git = GitReader(root)
    actual = Path(decode(git.run("rev-parse", "--show-toplevel")).strip()).resolve()
    if actual != root:
        raise DeltaError("--root must be the Git repository root; refusing to broaden nested scope.")
    head_data = git.run("rev-parse", "--verify", "HEAD^{commit}", optional=True)
    head = decode(head_data).strip() if head_data else None
    shallow = decode(git.run("rev-parse", "--is-shallow-repository")).strip() == "true"
    tracked = set(split_paths(git.run("ls-files", "-z")))
    gitlinks = set()
    for item in git.run("ls-files", "--stage", "-z").split(b"\0"):
        metadata, separator, filename = item.partition(b"\t")
        if separator and metadata.startswith(b"160000 "):
            gitlinks.add(decode(filename))
    untracked = split_paths(git.run("ls-files", "--others", "--exclude-standard", "-z"))
    if len(tracked) > max_files or len(untracked) > max_files:
        raise DeltaError("Git file inventory limit exceeded; increase --max-files or narrow scope.")
    candidates = {path for path in tracked | set(untracked) if is_readme(path) and first_party(path)}
    walked, boundaries = walk_readmes(root, max_files, gitlinks)
    candidates |= walked
    candidates = {path for path in candidates if not any(path == boundary or path.startswith(boundary + "/") for boundary in boundaries)}
    present_candidates = {path for path in candidates if (root / path).is_file() and not (root / path).is_symlink()}
    if primary:
        primary_path = Path(primary)
        candidate = (root / primary_path).resolve()
        try:
            primary = candidate.relative_to(root).as_posix()
        except ValueError as exc:
            raise DeltaError("--primary resolves outside the repository.") from exc
    primary = choose_primary(present_candidates, primary)
    warnings = []
    if boundaries:
        warnings.append("Nested Git/submodule boundaries were not traversed; request scope before inspecting child repository content.")
    if git.filter_overrides:
        warnings.append("Clean/process filters were disabled for safety; transformed files may require manual semantic comparison.")
    if shallow:
        warnings.append("Shallow history: earlier README/code changes may be unavailable.")
    if not head:
        warnings.append("Unborn repository: no committed delta or historical baseline is available.")
    baseline = {"commit": None, "source": "unavailable", "primary_readme": primary}
    if base is not None:
        resolved = git.run("rev-parse", "--verify", "--end-of-options", base + "^{commit}", optional=True)
        if not resolved:
            raise DeltaError("Requested baseline is not a locally available commit/tag.")
        baseline.update(commit=decode(resolved).strip(), source="explicit")
    elif head and primary:
        baseline.update(commit=last_touch(git, primary), source="last-primary-readme-touch-heuristic")
        warnings.append("Last README touch is a heuristic, not proof of semantic coverage; audit older translations against current code.")
    if not baseline["commit"]:
        warnings.append("No baseline found: request a local baseline or explicit current-state audit before claiming a complete sync.")
    layers = {
        "committed": git.diff(baseline["commit"], head) if baseline["commit"] and head else [],
        "staged": git.diff(cached=True),
        "unstaged": git.diff(),
        "untracked": [{"status": "?", "path": path} for path in sorted(untracked)],
        "net_tracked": git.diff(baseline["commit"]) if baseline["commit"] else None,
    }
    if any(records is not None and len(records) > max_files for records in layers.values()):
        raise DeltaError("Change inventory limit exceeded; increase --max-files.")
    conflicts = set()
    for item in git.run("ls-files", "-u", "-z").split(b"\0"):
        if item:
            metadata, separator, filename = item.partition(b"\t")
            if not separator:
                raise DeltaError("Malformed conflict record.")
            conflicts.add(decode(filename))
    missing_or_unsafe = []
    readmes = []
    for path in sorted(candidates):
        absolute = root / path
        try:
            absolute.resolve().relative_to(root)
            safe = not absolute.is_symlink()
        except (ValueError, OSError):
            safe = False
        exists = safe and absolute.is_file()
        if not exists:
            missing_or_unsafe.append(path)
        ignored = False
        if path not in tracked and exists:
            ignored = git.run("check-ignore", "-q", "--", path, optional=True) is not None
        readmes.append({
            "path": path, "present": exists, "tracked": path in tracked,
            "ignored": ignored, "last_touch": last_touch(git, path) if head and path in tracked else None,
            "format": absolute.suffix.lower() or "extensionless",
        })
    if missing_or_unsafe:
        warnings.append("Some tracked README candidates are missing or symlinks; resolve their disposition before claiming complete language coverage.")
    if conflicts:
        warnings.append("Unmerged files exist: do not automatically resolve or update affected documentation.")
    return {
        "root": str(root), "head": head, "baseline": baseline, "shallow": shallow,
        "layers": layers, "readmes": readmes, "conflicts": sorted(conflicts),
        "repository_boundaries": sorted(boundaries), "gitlinks": sorted(gitlinks),
        "warnings": warnings,
        "limitations": ["path-level local report only", "no source contents or patches read", "translation families require semantic classification", "no proof of version consent or runtime/rendering validity"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--base", help="User-selected local commit/tag baseline")
    parser.add_argument("--primary", help="Primary README path relative to the root")
    parser.add_argument("--max-files", type=int, default=10000)
    args = parser.parse_args(argv)
    try:
        report = collect(args.root, args.base, args.primary, args.max_files)
    except (DeltaError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "complete": False}, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
