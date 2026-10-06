import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SIDE = ROOT / "side-skills" / "readme-update-skill"
SCRIPT = SIDE / "scripts" / "git_readme_delta.py"
SPEC = importlib.util.spec_from_file_location("git_readme_delta", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@unittest.skipUnless(shutil.which("git"), "Git is required for local fixture tests")
class GitDeltaChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="readme-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith("GIT_"):
                self.env.pop(key)
        self.env.update({
            "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        })
        self.git("init", "--quiet")

    def git(self, *args):
        process = subprocess.run(
            ["git", "--no-pager", "-c", "core.hooksPath=" + os.devnull, "-c", "commit.gpgSign=false", "-C", str(self.root)] + list(args),
            env=self.env, capture_output=True, check=True,
        )
        return process.stdout

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "--quiet", "-m", "Fixture snapshot")
        return self.git("rev-parse", "HEAD").decode().strip()

    def baseline(self):
        self.write("README.md", "# Tool\n\nVersion: 1.0.0\n")
        self.write("src/main.py", "value = 1\n")
        return self.commit()

    def report(self, **kwargs):
        return MODULE.collect(self.root, **kwargs)

    def paths(self, records):
        return {record["path"] for record in records}

    def test_four_layers_and_net_delta(self):
        base = self.baseline()
        self.write("src/main.py", "value = 2\n")
        self.commit()
        self.write("src/staged.py", "flag = True\n")
        self.git("add", "src/staged.py")
        self.write("src/main.py", "value = 3\n")
        self.write("src/new.py", "new = True\n")
        report = self.report(base=base)
        self.assertEqual(self.paths(report["layers"]["committed"]), {"src/main.py"})
        self.assertEqual(self.paths(report["layers"]["staged"]), {"src/staged.py"})
        self.assertEqual(self.paths(report["layers"]["unstaged"]), {"src/main.py"})
        self.assertEqual(self.paths(report["layers"]["untracked"]), {"src/new.py"})
        self.assertEqual(self.paths(report["layers"]["net_tracked"]), {"src/main.py", "src/staged.py"})

    def test_all_language_names_and_ignored_readmes(self):
        self.baseline()
        self.write(".gitignore", "docs/\n")
        self.write("README-en.md", "# Tool\n")
        self.write("assets/README-zh.md", "# 工具\n")
        self.write("README.ja.md", "# Tool\n")
        self.write("README_ko.md", "# Tool\n")
        self.write("docs/fr/README.md", "# Tool\n")
        self.write("packages/cli/README.md", "# CLI\n")
        self.write("node_modules/dependency/README.md", "# Third party\n")
        self.write("vendor/library/README.md", "# Third party\n")
        report = self.report()
        paths = {item["path"] for item in report["readmes"]}
        self.assertTrue({"README.md", "README-en.md", "assets/README-zh.md", "README.ja.md", "README_ko.md", "docs/fr/README.md", "packages/cli/README.md"}.issubset(paths))
        self.assertNotIn("node_modules/dependency/README.md", paths)
        self.assertNotIn("vendor/library/README.md", paths)
        ignored = next(item for item in report["readmes"] if item["path"] == "docs/fr/README.md")
        self.assertTrue(ignored["ignored"])
        self.assertFalse(ignored["tracked"])

    def test_rename_and_delete(self):
        base = self.baseline()
        self.git("mv", "src/main.py", "src/renamed.py")
        self.commit()
        (self.root / "src/renamed.py").unlink()
        report = self.report(base=base)
        record = report["layers"]["committed"][0]
        self.assertTrue(record["status"].startswith("R"))
        self.assertEqual(record["old_path"], "src/main.py")
        self.assertEqual(record["path"], "src/renamed.py")
        self.assertEqual(report["layers"]["unstaged"][0]["status"], "D")

    def test_nul_filename_handling(self):
        base = self.baseline()
        name = "src/空 格\tline\nname.py"
        self.write(name, "value = 2\n")
        self.git("add", "--", name)
        report = self.report(base=base)
        self.assertIn(name, self.paths(report["layers"]["staged"]))

    def test_reverted_change_excluded_from_net(self):
        base = self.baseline()
        self.write("src/main.py", "value = 2\n")
        self.commit()
        self.write("src/main.py", "value = 1\n")
        report = self.report(base=base)
        self.assertTrue(report["layers"]["committed"])
        self.assertEqual(report["layers"]["net_tracked"], [])

    def test_readme_baseline_is_labeled_heuristic(self):
        base = self.baseline()
        self.write("src/main.py", "value = 2\n")
        self.commit()
        report = self.report()
        self.assertEqual(report["baseline"]["commit"], base)
        self.assertIn("heuristic", report["baseline"]["source"])
        self.assertTrue(any("heuristic" in warning for warning in report["warnings"]))

    def test_explicit_tag_baseline(self):
        base = self.baseline()
        self.git("tag", "v1.0.0")
        report = self.report(base="v1.0.0")
        self.assertEqual(report["baseline"]["commit"], base)
        self.assertEqual(report["baseline"]["source"], "explicit")

    def test_invalid_or_option_like_ref(self):
        self.baseline()
        for ref in ("missing-version", "--output=bad", "; touch bad"):
            with self.subTest(ref=ref), self.assertRaises(MODULE.DeltaError):
                self.report(base=ref)
        self.assertFalse((self.root / "bad").exists())

    def test_no_head_reports_limitation(self):
        self.write("README.md", "# New\n")
        self.write("src/main.py", "value = 1\n")
        self.git("add", "src/main.py")
        report = self.report()
        self.assertIsNone(report["head"])
        self.assertIsNone(report["baseline"]["commit"])
        self.assertIsNone(report["layers"]["net_tracked"])
        self.assertIn("src/main.py", self.paths(report["layers"]["staged"]))
        self.assertTrue(report["warnings"])

    def test_no_committed_readme(self):
        self.write("src/main.py", "value = 1\n")
        self.commit()
        self.write("README.md", "# New\n")
        report = self.report()
        self.assertIsNone(report["baseline"]["commit"])
        self.assertTrue(any("No baseline" in warning for warning in report["warnings"]))

    def test_explicit_nested_primary(self):
        self.write("docs/README.md", "# Tool\n")
        base = self.commit()
        self.assertEqual(self.report(primary="docs/README.md")["baseline"]["commit"], base)
        with self.assertRaises(MODULE.DeltaError):
            self.report(primary="../README.md")

    def test_nested_root_rejected(self):
        self.baseline()
        with self.assertRaises(MODULE.DeltaError):
            MODULE.collect(self.root / "src")

    def test_read_only_preserves_index_config_and_files(self):
        self.baseline()
        self.write("src/main.py", "value = 2\n")
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.report()
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_symlinks_not_followed(self):
        self.baseline()
        (self.root / "external").symlink_to(ROOT, target_is_directory=True)
        (self.root / "README-zh.md").symlink_to(ROOT / "README.md")
        report = self.report()
        item = next(item for item in report["readmes"] if item["path"] == "README-zh.md")
        self.assertFalse(item["present"])
        self.assertFalse(any(item["path"].startswith("external/") for item in report["readmes"]))

    def test_missing_tracked_translation_reported(self):
        self.baseline()
        self.write("assets/README-zh.md", "# 工具\n")
        self.commit()
        (self.root / "assets/README-zh.md").unlink()
        report = self.report()
        self.assertFalse(next(item for item in report["readmes"] if item["path"] == "assets/README-zh.md")["present"])
        self.assertTrue(any("missing" in warning for warning in report["warnings"]))

    def test_file_limit_fails_instead_of_truncating(self):
        self.baseline()
        with self.assertRaises(MODULE.DeltaError):
            self.report(max_files=1)

    def test_cli_json_error_and_success(self):
        self.baseline()
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("readmes", json.loads(result.stdout))
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--base", "nonexistent"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["complete"])

    def test_nested_repository_not_scanned(self):
        self.baseline()
        self.write("child/README-zh.md", "# Child\n")
        self.write("child/.git", "gitdir: unavailable\n")
        report = self.report()
        self.assertIn("child", report["repository_boundaries"])
        self.assertNotIn("child/README-zh.md", {item["path"] for item in report["readmes"]})

    def test_scan_permission_failure_is_explicit(self):
        self.baseline()

        def denied(*args, **kwargs):
            kwargs["onerror"](PermissionError("fixture denied"))
            return iter(())

        with patch.object(MODULE.os, "walk", side_effect=denied), self.assertRaises(MODULE.DeltaError):
            self.report()

    def test_clean_filter_not_executed(self):
        base = self.baseline()
        self.write(".gitattributes", "src/*.py filter=fixture\n")
        self.write("trap.py", "from pathlib import Path\nimport sys\nPath('filter-ran').write_text('ran')\nsys.stdout.write(sys.stdin.read())\n")
        self.git("config", "filter.fixture.clean", "python3 trap.py")
        self.git("config", "filter.fixture.required", "true")
        self.write("src/main.py", "value = 98765\n")
        report = self.report(base=base)
        self.assertFalse((self.root / "filter-ran").exists())
        self.assertTrue(any("filters were disabled" in warning for warning in report["warnings"]))

    def test_submodule_dirty_not_hidden_by_config(self):
        base = self.baseline()
        child = self.root / "module"
        child.mkdir()
        self.git("-C", str(child), "init", "--quiet")
        self.write("module/README.md", "# Child\n")
        self.git("-C", str(child), "add", "README.md")
        self.git("-C", str(child), "commit", "--quiet", "-m", "Child snapshot")
        child_head = self.git("-C", str(child), "rev-parse", "HEAD").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", "160000," + child_head + ",module")
        self.write("module/README.md", "# Child changed\n")
        self.git("config", "diff.ignoreSubmodules", "all")
        report = self.report(base=base)
        self.assertIn("module", report["gitlinks"])
        self.assertIn("module", self.paths(report["layers"]["unstaged"]))
        self.assertNotIn("module/README.md", {item["path"] for item in report["readmes"]})

    def test_environment_git_overrides_are_removed(self):
        reader = MODULE.GitReader(self.root)
        self.assertNotIn("GIT_DIR", reader.env)
        self.assertEqual(reader.env["GIT_OPTIONAL_LOCKS"], "0")
        self.assertEqual(reader.env["GIT_NO_LAZY_FETCH"], "1")


class SideSkillContract(unittest.TestCase):
    def test_gate_and_reference_contract(self):
        text = (SIDE / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(text.index("Mandatory version gate"), text.index("## Workflow"))
        self.assertIn("Stop and wait", text)
        self.assertIn("VERSION_REQUIRED", text)
        self.assertIn("all four change layers", text)
        self.assertIn("complete list of language editions", text)
        self.assertIn("General delegation", text)
        self.assertIn("name: readme-update\n", text)
        self.assertIn("Place, do not append", text)
        self.assertIn("identical apart from the language", text)
        self.assertIn("Keep the flowchart present and current", text)
        self.assertTrue((SIDE / "references/placement-and-parity.md").is_file())
        self.assertTrue((SIDE / "references/git-delta.md").is_file())
        self.assertTrue((SIDE / "references/version-and-language-sync.md").is_file())
        self.assertNotIn("[TODO", text)

    def test_behavior_contract(self):
        cases = json.loads((SIDE / "tests/behavior-cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            self.assertTrue(case["must"])

    def test_main_routes_incremental_updates_first(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(text.index("Update routing"), text.index("Non-negotiable entry gate"))
        self.assertIn("readme-update", text)
        self.assertIn("side-skills/readme-update-skill/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
