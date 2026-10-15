"""Run with: python3 -m unittest discover tests"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "tools"))
        os.makedirs(os.path.join(self.root, "vault", "screenshots"))
        shutil.copy(os.path.join(KIT, "tools", "board.py"), os.path.join(self.root, "tools"))
        self.board("init", "Sample")

    def tearDown(self):
        shutil.rmtree(self.root)

    def board(self, *args, ok=True):
        r = subprocess.run([sys.executable, os.path.join(self.root, "tools", "board.py"), *args],
                           capture_output=True, text=True, cwd=self.root)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def data(self):
        return json.load(open(os.path.join(self.root, "status", "board.json")))

    def test_tokens_add_up_per_task_agent_and_week(self):
        self.board("task", "add", "01", "Plant list", "--est", "40000")
        self.board("task", "set", "01", "review", "--tokens", "30000")
        self.board("agent", "coder-01", "done", "--tokens", "5000")
        b = self.data()
        self.assertEqual(b["tasks"]["01"]["actual"], 30000)
        self.assertEqual(b["agents"]["coder-01"]["tokens"], 5000)
        self.assertIn("35,000 tokens in the last 7 days", self.board("show").stdout)

    def test_budget_flags_check_in_at_cap(self):
        self.board("budget", "100000", "--cap", "50")
        self.board("tokens", "40000")
        self.assertNotIn("CHECK IN", self.board("show").stdout)
        self.board("tokens", "10000")
        self.assertIn("CHECK IN", self.board("show").stdout)

    def test_screenshot_goes_on_both_dashboards(self):
        open(os.path.join(self.root, "vault", "screenshots", "a.png"), "wb").close()
        self.board("shot", "vault/screenshots/a.png", "First screen")
        html = open(os.path.join(self.root, "dashboard", "index.html")).read()
        md = open(os.path.join(self.root, "vault", "Dashboard.md")).read()
        self.assertIn('src="../vault/screenshots/a.png"', html)
        self.assertIn("![[screenshots/a.png|360]]", md)

    def test_screenshot_outside_vault_is_refused(self):
        open(os.path.join(self.root, "elsewhere.png"), "wb").close()
        r = self.board("shot", os.path.join(self.root, "elsewhere.png"), "x", ok=False)
        self.assertNotEqual(r.returncode, 0)

    def test_milestone_phases(self):
        self.board("phase", "Design draft")
        self.assertEqual(self.data()["phase"], "Design draft")

    def test_old_board_with_old_phases_accepts_new_ones(self):
        path = os.path.join(self.root, "status", "board.json")
        b = self.data(); b["phases"] = ["Discovery", "Build", "Review", "Ship"]
        json.dump(b, open(path, "w"))
        self.board("phase", "Features draft")
        self.assertEqual(self.data()["phase"], "Features draft")

    def test_pipes_in_titles_keep_obsidian_table_intact(self):
        self.board("task", "add", "01", "A | B")
        md = open(os.path.join(self.root, "vault", "Dashboard.md")).read()
        self.assertIn("A \\| B", md)

    def test_old_board_without_new_fields_still_loads(self):
        path = os.path.join(self.root, "status", "board.json")
        b = self.data()
        for k in ("tokens", "budget", "cap", "shots"):
            b.pop(k)
        json.dump(b, open(path, "w"))
        self.board("agent", "manager", "hi")
        self.assertIn("usage:", self.board("show").stdout)


class NotifyTest(unittest.TestCase):
    def test_without_settings_it_exits_1(self):
        env = {k: v for k, v in os.environ.items() if k not in ("RESEND_API_KEY", "ALERT_EMAIL_TO", "TELEGRAM_BOT_TOKEN", "TELEGRAM_BOT_API_KEY", "TELEGRAM_CHAT_ID")}
        root = tempfile.mkdtemp()
        os.makedirs(os.path.join(root, "tools"))
        shutil.copy(os.path.join(KIT, "tools", "notify.py"), os.path.join(root, "tools"))
        r = subprocess.run([sys.executable, os.path.join(root, "tools", "notify.py"), "s", "b"],
                           capture_output=True, text=True, env=env)
        shutil.rmtree(root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("thread", r.stdout)


if __name__ == "__main__":
    unittest.main()
