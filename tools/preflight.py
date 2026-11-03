#!/usr/bin/env python3
"""Setup check: are the keys and settings this product needs actually in place?

Reads env.manifest (the product's list of settings, names only, never values) and
checks the variables this session can see: the process environment plus .env.

  preflight.py           before /orchestrate and whenever the owner says "done, I added it"
  preflight.py --live    before go-live: also fails if a data-source setting still
                         points at fixtures, mocks, samples or seed data

env.manifest, one setting per line:
  NAME  where=session,hosting  [also=OTHER_NAME]  [pattern=REGEX]  [optional]  [live]  # note

  where     session = agents need it here (cloud environment or .env); anything else
            (hosting, supabase, google, ...) can't be seen from here, so it is listed
            for the owner to confirm by hand.
  also      other accepted names for the same setting (comma-separated)
  pattern   a regex the value must match, e.g. pattern=^https:// or pattern=^\\d+$
  optional  missing is a warning, not a failure
  live      the setting decides where real data comes from; --live rejects
            values like "fixture", "mock", "sample", "seed", "test", "demo" or "fake"

Values are never printed. Exits 1 if anything fails.
"""
import argparse
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOT_LIVE = re.compile(r"fixture|mock|sample|seed|stub|test|demo|fake|dummy|placeholder", re.I)


def parse_manifest(path):
    items = []
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line, _, note = raw.partition("#")
        parts = line.split()
        if not parts:
            continue
        item = {"name": parts[0], "where": ["session"], "also": [], "pattern": None,
                "optional": False, "live": False, "note": note.strip(), "line": n}
        for p in parts[1:]:
            if p.startswith("where="):
                item["where"] = [w for w in p[6:].split(",") if w]
            elif p.startswith("also="):
                item["also"] = [x for x in p[5:].split(",") if x]
            elif p.startswith("pattern="):
                item["pattern"] = p[8:]
            elif p == "optional":
                item["optional"] = True
            elif p == "live":
                item["live"] = True
            else:
                sys.exit(f"env.manifest line {n}: unknown word {p!r}")
        items.append(item)
    return items


def read_dotenv(path):
    values = {}
    if not os.path.exists(path):
        return values
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip().removeprefix("export ").strip()] = v.strip().strip('"').strip("'")
    return values


def near_misses(name, available):
    """Names that look like a typo of `name` (SUPABASE_BE_URL for SUPABASE_DB_URL)."""
    close = difflib.get_close_matches(name, available, n=3, cutoff=0.75)
    stem = name.rsplit("_", 1)[0]
    close += [k for k in available if k != name and k.startswith(stem + "_") and k not in close]
    return close[:3]


def check(items, env, live=False):
    fails, warns, by_hand = [], [], []
    names = sorted(env)
    for it in items:
        where = ", ".join(it["where"])
        if "session" not in it["where"]:
            if live or not it["live"]:
                extra = " (must point at real data, not fixtures)" if it["live"] else ""
                by_hand.append(f"{it['name']} in {where}{extra}" + (f": {it['note']}" if it["note"] else ""))
            continue
        value = next((env[n] for n in [it["name"], *it["also"]] if env.get(n)), "")
        if not value:
            hint = [h for h in near_misses(it["name"], names) if h not in it["also"]]
            msg = f"{it['name']} is missing" + (f"; did you mean {' or '.join(hint)}?" if hint else "")
            msg += f" ({it['note']})" if it["note"] else ""
            (warns if it["optional"] else fails).append(msg)
            continue
        if it["pattern"] and not re.search(it["pattern"], value):
            fails.append(f"{it['name']} is set but doesn't look right (expected to match {it['pattern']})")
        if live and it["live"] and NOT_LIVE.search(value):
            fails.append(f"{it['name']} still points at test data; set it to the live source before go-live")
    return fails, warns, by_hand


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check this product's keys and settings.")
    ap.add_argument("--live", action="store_true", help="also reject fixture/mock/seed data sources")
    ap.add_argument("--manifest", default=os.path.join(ROOT, "env.manifest"))
    a = ap.parse_args(argv)
    if not os.path.exists(a.manifest):
        print("No env.manifest yet. /kickoff writes it from the master plan's integrations; "
              "copy vault/templates/env.manifest to start one.")
        return 0
    env = {**read_dotenv(os.path.join(ROOT, ".env")),
           **{k: v for k, v in os.environ.items() if v}}
    fails, warns, by_hand = check(parse_manifest(a.manifest), env, live=a.live)
    for f in fails:
        print(f"FAIL  {f}")
    for w in warns:
        print(f"WARN  {w}")
    if by_hand:
        print("Confirm by hand (not visible from this session):")
        for b in by_hand:
            print(f"  - {b}")
    if not fails:
        print("Preflight OK" + (" for go-live" if a.live else ""))
    print("Note: in cloud sessions, settings added after the session started only appear in a new session.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
