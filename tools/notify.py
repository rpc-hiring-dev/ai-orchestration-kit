#!/usr/bin/env python3
"""Alert the owner. Used only for milestone drafts, anything that costs money,
stuck agents and the weekly usage check-in.

Sends a phone push through a Telegram bot when TELEGRAM_BOT_TOKEN and
TELEGRAM_CHAT_ID are set, and an email through Resend when RESEND_API_KEY and
ALERT_EMAIL_TO are set.

Settings come from .env (git-ignored) or the environment:
  TELEGRAM_BOT_TOKEN token from @BotFather for the owner's private alert bot
                     (TELEGRAM_BOT_API_KEY is accepted too)
  TELEGRAM_CHAT_ID   the owner's chat with that bot (see --find-chat)
  RESEND_API_KEY     free key from resend.com
  ALERT_EMAIL_TO     the owner's address (kept per product, never in the kit)
  ALERT_EMAIL_FROM   optional, defaults to Resend's test sender

Usage:
  notify.py "<subject>" "<body>" [--dry-run]
  notify.py --find-chat    print the chat id of whoever last messaged the bot

Exits 1 if no alert was delivered, so the caller falls back to asking in the thread.
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


def send(req, label):
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"Sent by {label} ({r.status})")
            return True
    except Exception as err:
        print(f"{label} failed: {err}")
        return False


def telegram(method, payload):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/{method}"
    return urllib.request.Request(url, data=json.dumps(payload).encode(),
                                  headers={"Content-Type": "application/json",
                                           "User-Agent": "ai-orchestration-kit"})


def find_chat():
    if not os.environ.get("TELEGRAM_BOT_TOKEN"):
        print("TELEGRAM_BOT_TOKEN isn't set.")
        return 1
    with urllib.request.urlopen(telegram("getUpdates", {}), timeout=20) as r:
        updates = json.load(r).get("result", [])
    chats = [u["message"]["chat"]["id"] for u in updates if "message" in u]
    if not chats:
        print("No messages yet. Ask the owner to send the bot any message, then retry.")
        return 1
    print(chats[-1])
    return 0


def main(argv):
    load_env()
    # The cloud environment stores the bot token under this older name.
    if os.environ.get("TELEGRAM_BOT_API_KEY"):
        os.environ.setdefault("TELEGRAM_BOT_TOKEN", os.environ["TELEGRAM_BOT_API_KEY"])
    if argv == ["--find-chat"]:
        return find_chat()
    p = argparse.ArgumentParser(description="Alert the owner")
    p.add_argument("subject"); p.add_argument("body"); p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)
    bot, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    key, to = os.environ.get("RESEND_API_KEY"), os.environ.get("ALERT_EMAIL_TO")
    sender = os.environ.get("ALERT_EMAIL_FROM", "Agent team <onboarding@resend.dev>")
    msg = {"from": sender, "to": [to], "subject": a.subject, "text": a.body}
    if a.dry_run:
        print(json.dumps({"telegram": bool(bot and chat), "email": {**msg, "to": [to or "<ALERT_EMAIL_TO not set>"]}}, indent=2))
        return 0
    sent = False
    if bot and chat:
        sent |= send(telegram("sendMessage", {"chat_id": chat, "text": f"{a.subject}\n\n{a.body}"}), "push")
    if key and to:
        sent |= send(urllib.request.Request("https://api.resend.com/emails", data=json.dumps(msg).encode(),
                                            headers={"Authorization": f"Bearer {key}",
                                                     "Content-Type": "application/json",
                                                     "User-Agent": "ai-orchestration-kit"}), "email")
    if not ((bot and chat) or (key and to)):
        print("Alerts aren't set up (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID, or RESEND_API_KEY and ALERT_EMAIL_TO, in .env). Tell the owner in the thread instead.")
    elif not sent:
        print("No alert was delivered. Tell the owner in the thread instead.")
    return 0 if sent else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
