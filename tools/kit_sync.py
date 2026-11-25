#!/usr/bin/env python3
"""Bring a product repo up to the latest AI orchestration kit.

Every product starts as a copy of the kit, and the kit keeps improving. This
copies the kit's own files (skills, agents, hooks, tools, templates, setup traps)
into the product. Product files (master plan, tickets, decisions, handoffs, the
product's code) are never touched.

  kit_sync.py                     show what would change (nothing is written)
  kit_sync.py --apply             copy the changes and update kit.lock
  kit_sync.py --kit <path|url>    use another copy of the kit (default: the GitHub repo)

kit.lock (at the repo root, committed) records the kit commit and a hash of
each kit file as last synced. A kit file the product has edited since then is
reported as "kept (edited here)" and not overwritten, unless --force is given.
Without a kit.lock (the first sync), every file that differs is updated: run it
on a branch and read the diff before merging. Files the kit and the product
both shape (CLAUDE.md, the system plan, README) are only listed for a person to
merge by hand.

Uses only the standard library and git. Exits 1 if something failed.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT_URL = "https://github.com/rpc-hiring-dev/ai-orchestration-kit"
LOCK = "kit.lock"

# Owned by the kit: copied over (folders are copied whole, file by file).
KIT_PATHS = [
    ".claude/agents",
    ".claude/hooks",
    ".claude/skills",
    ".claude/settings.json",
    "tools/board.py",
    "tools/notify.py",
    "tools/preflight.py",
    "tools/kit_sync.py",
    "tests/test_board.py",
    "tests/test_preflight.py",
    "tests/test_kit_sync.py",
    "vault/templates",
    "vault/setup-traps.md",
    "vault/project-memory.md",
    "vault/handoffs/README.md",
    "THIRD_PARTY.md",
]

# Shaped by both: never overwritten, listed for a person to merge.
SHARED_PATHS = ["CLAUDE.md", "README.md", "vault/system-plan.md", "vault/Home.md", ".gitignore", ".env.example"]


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def kit_files(kit_root):
    """Relative paths of every kit-owned file in a kit checkout."""
    found = []
    for rel in KIT_PATHS:
        full = os.path.join(kit_root, rel)
        if os.path.isfile(full):
            found.append(rel)
        elif os.path.isdir(full):
            for d, dirs, files in os.walk(full):
                dirs[:] = [x for x in dirs if x not in ("__pycache__", "worktrees")]
                for name in files:
                    if name.endswith(".pyc"):
                        continue
                    found.append(os.path.relpath(os.path.join(d, name), kit_root).replace(os.sep, "/"))
    return sorted(found)


def read_lock(root):
    path = os.path.join(root, LOCK)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def plan(product_root, kit_root, lock, force=False):
    """Work out what to do. Returns a dict of lists of relative paths."""
    locked = (lock or {}).get("files", {})
    result = {"add": [], "update": [], "remove": [], "kept": [], "same": [], "merge_by_hand": []}
    new_files = kit_files(kit_root)
    for rel in new_files:
        src = os.path.join(kit_root, rel)
        dst = os.path.join(product_root, rel)
        if not os.path.exists(dst):
            result["add"].append(rel)
            continue
        here = file_hash(dst)
        if here == file_hash(src):
            result["same"].append(rel)
        elif lock is not None and rel in locked and locked[rel] != here and not force:
            result["kept"].append(rel)
        else:
            result["update"].append(rel)
    # Files the kit has dropped since the last sync: remove them if unedited here.
    for rel in sorted(set(locked) - set(new_files)):
        dst = os.path.join(product_root, rel)
        if not os.path.exists(dst):
            continue
        if file_hash(dst) == locked[rel] or force:
            result["remove"].append(rel)
        else:
            result["kept"].append(rel)
    for rel in SHARED_PATHS:
        src, dst = os.path.join(kit_root, rel), os.path.join(product_root, rel)
        if os.path.exists(src) and (not os.path.exists(dst) or file_hash(src) != file_hash(dst)):
            result["merge_by_hand"].append(rel)
    return result


def apply(product_root, kit_root, result, kit_commit, lock):
    for rel in result["add"] + result["update"]:
        dst = os.path.join(product_root, rel)
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(os.path.join(kit_root, rel), dst)
    for rel in result["remove"]:
        os.remove(os.path.join(product_root, rel))
    files = {}
    old = (lock or {}).get("files", {})
    for rel in result["add"] + result["update"] + result["same"]:
        files[rel] = file_hash(os.path.join(kit_root, rel))
    for rel in result["kept"]:
        if rel in old:  # keep the old hash so the edit is still noticed next time
            files[rel] = old[rel]
    with open(os.path.join(product_root, LOCK), "w", encoding="utf-8") as f:
        json.dump({"kit": KIT_URL, "kit_commit": kit_commit, "files": dict(sorted(files.items()))}, f, indent=2)
        f.write("\n")


def fetch_kit(source, dest):
    if os.path.isdir(source):
        return os.path.abspath(source)
    subprocess.run(["git", "clone", "--quiet", "--depth", "1", source, dest], check=True)
    return dest


def commit_of(path):
    try:
        out = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def report(result, applied):
    labels = [
        ("add", "new from the kit"),
        ("update", "updated from the kit"),
        ("remove", "dropped by the kit"),
        ("kept", "kept (edited here; compare by hand or rerun with --force)"),
        ("merge_by_hand", "differs from the kit; merge by hand if wanted"),
    ]
    changed = False
    for key, label in labels:
        if result[key]:
            changed = changed or key in ("add", "update", "remove")
            print(f"{label} ({len(result[key])}):")
            for rel in result[key]:
                print(f"  {rel}")
    print(f"unchanged: {len(result['same'])} files")
    if changed and not applied:
        print("Nothing written. Rerun with --apply, on a branch, to copy these changes.")
    if not changed:
        print("Kit files are up to date.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kit", default=KIT_URL, help="kit checkout folder or git URL")
    ap.add_argument("--apply", action="store_true", help="copy the changes and update kit.lock")
    ap.add_argument("--force", action="store_true", help="also overwrite kit files edited in this repo")
    ap.add_argument("--root", default=ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        try:
            kit_root = fetch_kit(args.kit, os.path.join(tmp, "kit"))
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not get the kit from {args.kit}: {e}", file=sys.stderr)
            return 1
        if os.path.abspath(kit_root) == os.path.abspath(args.root):
            print("This is the kit itself; nothing to sync.")
            return 0
        lock = read_lock(args.root)
        if lock is None:
            print("No kit.lock yet: first sync. Every kit file that differs will be updated.")
        result = plan(args.root, kit_root, lock, force=args.force)
        if args.apply:
            apply(args.root, kit_root, result, commit_of(kit_root), lock)
        report(result, args.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
