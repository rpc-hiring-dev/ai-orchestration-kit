#!/usr/bin/env python3
"""Email the owner. Used only for milestone drafts, anything that costs money,
stuck agents and the weekly usage check-in.

Settings come from .env (git-ignored) or the environment:
  RESEND_API_KEY     free key from resend.com
  ALERT_EMAIL_TO     the owner's address (kept per product, never in the kit)
  ALERT_EMAIL_FROM   optional, defaults to Resend's test sender

Usage:
  notify.py "<subject>" "<body>" [--dry-run]

Exits 1 if email isn't set up, so the caller falls back to asking in the thread.
"""
import argparse
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env():
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path):
            k, sep, v = line.strip().partition("=")
            if sep and not k.startswith("#"):
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def main(argv):
    p = argparse.ArgumentParser(description="Email the owner")
    p.add_argument("subject"); p.add_argument("body"); p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)
    load_env()
    key, to = os.environ.get("RESEND_API_KEY"), os.environ.get("ALERT_EMAIL_TO")
    sender = os.environ.get("ALERT_EMAIL_FROM", "Agent team <onboarding@resend.dev>")
    msg = {"from": sender, "to": [to], "subject": a.subject, "text": a.body}
    if a.dry_run:
        print(json.dumps({**msg, "to": [to or "<ALERT_EMAIL_TO not set>"]}, indent=2))
        return 0
    if not key or not to:
        print("Email isn't set up (RESEND_API_KEY and ALERT_EMAIL_TO in .env). Tell the owner in the thread instead.")
        return 1
    req = urllib.request.Request("https://api.resend.com/emails", data=json.dumps(msg).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                          "User-Agent": "ai-orchestration-kit"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"Sent: {a.subject} ({r.status})")
            return 0
    except Exception as err:  # report and let the caller fall back to the thread
        print(f"Email failed: {err}. Tell the owner in the thread instead.")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
