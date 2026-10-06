import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_readme.py"
SPEC = importlib.util.spec_from_file_location("check_readme", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ReadmeChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".readme-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def prefs(self, **overrides):
        result = {
            "status": "confirmed", "source": "accepted_recommendation",
            "project_root": str(self.root), "primary_language": "en",
            "secondary_languages": [], "audience": "users", "layout": "balanced",
            "depth": "standard", "tone": "professional", "badge_style": "flat",
            "visuals": "existing", "update_mode": "preserve", "renderer": "github",
            "emoji": False,
        }
        result.update(overrides)
        return result

    def check(self, content, preferences=None, name="README.md"):
        checker = MODULE.Checker(self.root, preferences)
        checker.validate_preferences()
        checker.check(self.write(name, content))
        return checker.finish()

    def codes(self, issues):
        return {issue.code for issue in issues}

    def test_valid_minimal(self):
        self.assertEqual(self.check("# Tool\n\n## Usage\n\nRun the tool.\n"), [])

    def test_nested_translation_links(self):
        self.write("LICENSE", "MIT")
        self.write("README.md", "# Tool\n\n## Quick Start\n")
        issues = self.check("# 工具\n\n[English](../README.md#quick-start)\n[MIT](../LICENSE)\n\n## 快速开始\n\n[开始](#快速开始)\n", name="assets/README-zh.md")
        self.assertEqual(issues, [])

    def test_missing_local_file(self):
        self.assertIn("missing-local-link", self.codes(self.check("# Tool\n[Docs](absent.md)\n")))

    def test_translated_anchor_not_english(self):
        self.assertIn("missing-anchor", self.codes(self.check("# 工具\n[开始](#quick-start)\n## 快速开始\n")))

    def test_duplicate_heading_anchors(self):
        issues = self.check("# Tool\n[Second](#usage-1)\n## Usage\n## Usage\n")
        self.assertEqual(issues, [])

    def test_setext_heading(self):
        self.assertEqual(self.check("Tool\n====\n\n[Use](#usage)\n\nUsage\n-----\n"), [])

    def test_inline_formatting_heading(self):
        self.assertEqual(self.check("# Tool\n[Use](#use-tool)\n## Use `tool`\n"), [])

    def test_percent_encoded_path(self):
        self.write("docs/first use.md", "# Guide\n")
        self.assertEqual(self.check("# Tool\n[Guide](docs/first%20use.md)\n"), [])

    def test_balanced_parentheses_path(self):
        self.write("docs/use(v2).md", "# Guide\n")
        self.assertEqual(self.check("# Tool\n[Guide](docs/use(v2).md)\n"), [])

    def test_reference_links(self):
        self.write("docs.md", "# Guide\n")
        self.assertEqual(self.check("# Tool\n[Guide][docs]\n\n[docs]: docs.md\n"), [])

    def test_undefined_reference(self):
        self.assertIn("missing-reference", self.codes(self.check("# Tool\n[Guide][missing]\n")))

    def test_ignore_code_examples(self):
        content = "# Tool\n\n```markdown\n[Fake](missing.md)\n<!-- readme-skill:begin fake -->\n```\n\n`[Fake](missing.md)`\n"
        self.assertEqual(self.check(content), [])

    def test_tilde_and_long_fences(self):
        self.assertEqual(self.check("# Tool\n\n~~~~text\n```\n[Fake](missing.md)\n~~~~\n"), [])

    def test_unclosed_fence(self):
        self.assertIn("unclosed-fence", self.codes(self.check("# Tool\n```bash\necho hello\n")))

    def test_path_escape(self):
        self.assertIn("path-escape", self.codes(self.check("# Tool\n[Outside](../LICENSE)\n")))

    def test_symlink_escape(self):
        (self.root / "outside").symlink_to(ROOT / "LICENSE")
        self.assertIn("path-escape", self.codes(self.check("# Tool\n[Outside](outside)\n")))

    def test_absolute_local_link(self):
        self.assertIn("absolute-local-link", self.codes(self.check("# Tool\n[Bad](/LICENSE)\n")))

    def test_external_links_are_not_fetched(self):
        self.assertEqual(self.check("# Tool\n[Site](https://invalid.example/path#missing)\n"), [])

    def test_html_image_alt_and_path(self):
        self.write("shot.png", "fixture")
        issues = self.check('# Tool\n<img src="shot.png" alt="" />\n')
        self.assertIn("image-alt", self.codes(issues))
        self.assertNotIn("missing-local-link", self.codes(issues))

    def test_html_boolean_image_attributes(self):
        issues = self.check('# Tool\n<img src alt>\n')
        self.assertTrue({"image-alt", "empty-link"}.issubset(self.codes(issues)))

    def test_portable_autolinks(self):
        issues = self.check('# Tool\n<https://example.com>\n<docs@example.com>\n', self.prefs(renderer="portable"))
        self.assertEqual(issues, [])

    def test_html_anchor(self):
        self.assertEqual(self.check('# Tool\n<a id="start"></a>\n[Start](#start)\n'), [])

    def test_unsafe_html_and_uri(self):
        issues = self.check('# Tool\n<script>alert(1)</script>\n<a href="javascript:alert(1)">Bad</a>\n')
        self.assertTrue({"unsafe-html", "unsafe-link"}.issubset(self.codes(issues)))

    def test_managed_with_manual_block(self):
        content = "# Tool\n<!-- readme-skill:begin usage -->\n## Usage\n<!-- MANUAL-START -->\nMaintainer note.\n<!-- MANUAL-END -->\n<!-- readme-skill:end usage -->\n"
        self.assertEqual(self.check(content), [])

    def test_duplicate_managed_regions(self):
        region = "<!-- readme-skill:begin usage -->\nText\n<!-- readme-skill:end usage -->\n"
        self.assertIn("managed-markers", self.codes(self.check("# Tool\n" + region + region)))

    def test_nested_and_mismatched_regions(self):
        content = "# Tool\n<!-- readme-skill:begin usage -->\n<!-- readme-skill:begin api -->\n<!-- readme-skill:end usage -->\n"
        self.assertIn("managed-markers", self.codes(self.check(content)))

    def test_unclosed_manual_region(self):
        self.assertIn("manual-markers", self.codes(self.check("# Tool\n<!-- MANUAL-START -->\nNote\n")))

    def test_template_token(self):
        self.assertIn("template-token", self.codes(self.check("# {PROJECT_NAME}\n")))

    def test_secret_value_not_reported(self):
        secret = "ghp_" + "x" * 36
        issues = self.check("# Tool\n" + secret + "\n")
        self.assertIn("possible-secret", self.codes(issues))
        self.assertNotIn(secret, json.dumps([MODULE.asdict(issue) for issue in issues]))

    def test_incomplete_mermaid(self):
        self.assertIn("mermaid-type", self.codes(self.check("# Tool\n```mermaid\nclassDef foo fill:red\n```\n")))

    def test_invalid_sequence_classes(self):
        issues = self.check("# Tool\n```mermaid\nsequenceDiagram\nA->>B: Hello\nclassDef foo fill:red\n```\n")
        self.assertIn("mermaid-sequence-class", self.codes(issues))

    def test_valid_mermaid_flowchart(self):
        self.assertEqual(self.check("# Tool\n```mermaid\nflowchart TD\nA --> B\n```\n"), [])

    def test_preference_gate(self):
        issues = self.check("# Tool\n", self.prefs(status="asked"))
        self.assertIn("preference-gate", self.codes(issues))

    def test_valid_delegation(self):
        self.assertEqual(self.check("# Tool\n", self.prefs(status="delegated", source="explicit_delegation")), [])

    def test_preference_scope(self):
        self.assertIn("preference-scope", self.codes(self.check("# Tool\n", self.prefs(project_root=str(ROOT)))))

    def test_invalid_preference_types(self):
        issues = self.check("# Tool\n", self.prefs(layout=[], secondary_languages=[{}]))
        self.assertIn("preferences", self.codes(issues))

    def test_invalid_confirmation_source(self):
        issues = self.check("# Tool\n", self.prefs(source=[]))
        self.assertIn("preference-gate", self.codes(issues))

    def test_invalid_badge_style_and_translation_types(self):
        issues = self.check("# Tool\n", self.prefs(badge_style=[], secondary_languages=7))
        self.assertIn("preferences", self.codes(issues))

    def test_duplicate_languages(self):
        self.assertIn("preferences", self.codes(self.check("# Tool\n", self.prefs(secondary_languages=["en"]))))

    def test_no_badges(self):
        issues = self.check("# Tool\n![MIT](https://img.shields.io/badge/license-MIT-green)\n", self.prefs(badge_style="none"))
        self.assertIn("preference-badges", self.codes(issues))

    def test_badge_style_consistency(self):
        issues = self.check("# Tool\n![MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)\n", self.prefs())
        self.assertIn("preference-badges", self.codes(issues))

    def test_malformed_badge_url(self):
        issues = self.check('# Tool\n![Badge](https://[img.shields.io/bad)\n', self.prefs())
        self.assertIn("invalid-link", self.codes(issues))

    def test_compact_and_portable(self):
        issues = self.check('<h1 align="center">Tool</h1>\n', self.prefs(layout="compact", renderer="portable"))
        self.assertTrue({"preference-layout", "preference-portable"}.issubset(self.codes(issues)))

    def test_no_visuals(self):
        self.write("shot.png", "fixture")
        self.assertIn("preference-visuals", self.codes(self.check("# Tool\n![Real demo](shot.png)\n", self.prefs(visuals="none"))))

    def test_translation_regions(self):
        checker = MODULE.Checker(self.root, self.prefs(secondary_languages=["zh"]))
        checker.validate_preferences()
        checker.check(self.write("README.md", "# Tool\n<!-- readme-skill:begin usage -->\nUse\n<!-- readme-skill:end usage -->\n"))
        checker.check(self.write("README-zh.md", "# 工具\n"))
        self.assertIn("translation-regions", self.codes(checker.finish()))

    def test_cli_json_and_exit_codes(self):
        path = self.write("README.md", "# Tool\n[Bad](missing.md)\n")
        process = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json", str(path)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 1)
        self.assertEqual(json.loads(process.stdout)["errors"], 1)

    def test_cli_read_failure(self):
        process = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json", str(self.root / "missing.md")], capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)
        self.assertIn("read-failure", {item["code"] for item in json.loads(process.stdout)["issues"]})

    def test_read_only(self):
        path = self.write("README.md", "# Tool\n\n## Usage\n")
        before = path.read_bytes()
        checker = MODULE.Checker(self.root)
        checker.check(path)
        checker.finish()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(self.root.iterdir()), [path])


class SkillContract(unittest.TestCase):
    def test_entry_gate_and_reference_paths(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version: 2.0.0", content)
        self.assertLess(content.index("Non-negotiable entry gate"), content.index("## Workflow"))
        self.assertIn("End the turn and wait", content)
        self.assertNotIn("If the user provides no configuration, use these defaults", content)
        for name in re.findall(r"`((?:references|scripts|tests)/[^`]+)`", content):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_behavior_case_contract(self):
        cases = json.loads((ROOT / "tests" / "behavior-cases.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(cases), 12)
        for case in cases:
            self.assertTrue(case["must"])
            self.assertTrue(case["conversation"])


if __name__ == "__main__":
    import re
    unittest.main()
