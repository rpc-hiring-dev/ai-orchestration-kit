"""Run with: python3 -m unittest discover tests"""
import os
import subprocess
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "tools"))
import preflight  # noqa: E402

MANIFEST = """\
# sample manifest
SUPABASE_URL     where=session,hosting pattern=^https://   # project URL
SUPABASE_DB_URL  where=session also=DATABASE_URL           # database connection string
TELEGRAM_CHAT_ID where=session pattern=^-?\\d+$ optional
DATA_SOURCE      where=session live                        # sheets in production
GMAIL_CLIENT_ID  where=hosting                              # Google OAuth client
SHEET_SOURCE     where=hosting live
"""


class PreflightTest(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write(MANIFEST)
        self.items = preflight.parse_manifest(self.path)

    def tearDown(self):
        os.remove(self.path)

    def good_env(self, **over):
        env = {"SUPABASE_URL": "https://abc.supabase.co", "SUPABASE_DB_URL": "postgres://x",
               "TELEGRAM_CHAT_ID": "12345", "DATA_SOURCE": "sheets"}
        env.update(over)
        return {k: v for k, v in env.items() if v is not None}

    def test_all_present_passes_and_lists_hosting_settings_for_the_owner(self):
        fails, warns, by_hand = preflight.check(self.items, self.good_env())
        self.assertEqual((fails, warns), ([], []))
        self.assertTrue(any("GMAIL_CLIENT_ID in hosting" in b for b in by_hand))

    def test_typo_in_a_name_is_suggested(self):
        env = self.good_env(SUPABASE_DB_URL=None, SUPABASE_BE_URL="postgres://x")
        fails, _, _ = preflight.check(self.items, env)
        self.assertEqual(len(fails), 1)
        self.assertIn("did you mean SUPABASE_BE_URL", fails[0])

    def test_an_accepted_other_name_counts(self):
        env = self.good_env(SUPABASE_DB_URL=None, DATABASE_URL="postgres://x")
        self.assertEqual(preflight.check(self.items, env)[0], [])

    def test_bad_format_fails_without_printing_the_value(self):
        fails, _, _ = preflight.check(self.items, self.good_env(SUPABASE_URL="secret-value"))
        self.assertEqual(len(fails), 1)
        self.assertNotIn("secret-value", fails[0])

    def test_optional_missing_is_only_a_warning(self):
        fails, warns, _ = preflight.check(self.items, self.good_env(TELEGRAM_CHAT_ID=None))
        self.assertEqual(fails, [])
        self.assertEqual(len(warns), 1)

    def test_live_rejects_a_data_source_left_on_fixtures(self):
        env = self.good_env(DATA_SOURCE="fixture")
        self.assertEqual(preflight.check(self.items, env)[0], [])
        fails, _, by_hand = preflight.check(self.items, env, live=True)
        self.assertIn("DATA_SOURCE still points at test data", fails[0])
        self.assertTrue(any("SHEET_SOURCE" in b and "real data" in b for b in by_hand))

    def test_unknown_word_in_manifest_is_an_error(self):
        with open(self.path, "a") as f:
            f.write("X where=session requird\n")
        with self.assertRaises(SystemExit):
            preflight.parse_manifest(self.path)

    def test_command_exits_1_on_failure_and_0_without_a_manifest(self):
        script = os.path.join(KIT, "tools", "preflight.py")
        env = {"PATH": os.environ.get("PATH", "")}
        r = subprocess.run([sys.executable, script, "--manifest", self.path],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL  SUPABASE_URL is missing", r.stdout)
        r = subprocess.run([sys.executable, script, "--manifest", self.path + ".none"],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
