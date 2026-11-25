"""Run with: python3 -m unittest discover tests"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "tools"))
import kit_sync  # noqa: E402


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


class KitSyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kit = os.path.join(self.tmp.name, "kit")
        self.product = os.path.join(self.tmp.name, "product")
        write(self.kit, ".claude/skills/feature/SKILL.md", "feature v2")
        write(self.kit, ".claude/skills/new-skill/SKILL.md", "brand new")
        write(self.kit, "vault/setup-traps.md", "traps v2")
        write(self.kit, "CLAUDE.md", "kit rules v2")
        write(self.product, ".claude/skills/feature/SKILL.md", "feature v1")
        write(self.product, "vault/setup-traps.md", "traps v2")
        write(self.product, "CLAUDE.md", "product rules")
        write(self.product, "vault/master-plan.md", "the product's plan")

    def tearDown(self):
        self.tmp.cleanup()

    def run_sync(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = kit_sync.main(["--kit", self.kit, "--root", self.product, *args])
        return code, out.getvalue()

    def test_dry_run_writes_nothing(self):
        code, out = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn(".claude/skills/new-skill/SKILL.md", out)
        self.assertIn("Nothing written", out)
        self.assertEqual(read(self.product, ".claude/skills/feature/SKILL.md"), "feature v1")
        self.assertFalse(os.path.exists(os.path.join(self.product, "kit.lock")))

    def test_first_apply_copies_kit_files_and_leaves_product_files(self):
        code, out = self.run_sync("--apply")
        self.assertEqual(code, 0)
        self.assertEqual(read(self.product, ".claude/skills/feature/SKILL.md"), "feature v2")
        self.assertEqual(read(self.product, ".claude/skills/new-skill/SKILL.md"), "brand new")
        self.assertEqual(read(self.product, "CLAUDE.md"), "product rules")
        self.assertEqual(read(self.product, "vault/master-plan.md"), "the product's plan")
        self.assertIn("CLAUDE.md", out.split("merge by hand")[1])
        lock = json.loads(read(self.product, "kit.lock"))
        self.assertIn(".claude/skills/feature/SKILL.md", lock["files"])
        self.assertNotIn("CLAUDE.md", lock["files"])

    def test_file_edited_in_product_is_kept(self):
        self.run_sync("--apply")
        write(self.product, ".claude/skills/feature/SKILL.md", "edited for this product")
        write(self.kit, ".claude/skills/feature/SKILL.md", "feature v3")
        _, out = self.run_sync("--apply")
        self.assertEqual(read(self.product, ".claude/skills/feature/SKILL.md"), "edited for this product")
        self.assertIn("kept", out)
        # Still noticed as edited on the next run.
        _, out = self.run_sync()
        self.assertIn("kept", out)
        # --force overwrites it.
        self.run_sync("--apply", "--force")
        self.assertEqual(read(self.product, ".claude/skills/feature/SKILL.md"), "feature v3")

    def test_unedited_file_is_updated_after_lock(self):
        self.run_sync("--apply")
        write(self.kit, "vault/setup-traps.md", "traps v3")
        self.run_sync("--apply")
        self.assertEqual(read(self.product, "vault/setup-traps.md"), "traps v3")

    def test_file_dropped_by_kit_is_removed_only_if_unedited(self):
        self.run_sync("--apply")
        os.remove(os.path.join(self.kit, ".claude/skills/new-skill/SKILL.md"))
        _, out = self.run_sync("--apply")
        self.assertIn("dropped by the kit", out)
        self.assertFalse(os.path.exists(os.path.join(self.product, ".claude/skills/new-skill/SKILL.md")))

    def test_up_to_date(self):
        self.run_sync("--apply")
        _, out = self.run_sync()
        self.assertIn("Kit files are up to date", out)

    def test_refuses_to_sync_the_kit_into_itself(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = kit_sync.main(["--kit", self.kit, "--root", self.kit])
        self.assertEqual(code, 0)
        self.assertIn("kit itself", out.getvalue())


if __name__ == "__main__":
    unittest.main()
