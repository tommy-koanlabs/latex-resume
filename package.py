#!/usr/bin/env python3
"""Package skill/ into resume-tailor.skill (a zip whose top folder is resume-tailor/).

Usage:  python package.py [--out DIR]

The repo keeps the skill in skill/, but an installed skill's folder name must
match its `name`, so files are written under resume-tailor/ inside the zip.
Python caches and build leftovers are skipped. Entries are sorted and
timestamped at a fixed date so the same source gives the same file.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skill"
NAME = "resume-tailor"
SKIP_DIRS = {"__pycache__"}
SKIP_SUFFIX = {".pyc", ".aux", ".log", ".out"}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT)
    args = ap.parse_args()

    md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m or not re.search(rf"^name:\s*{NAME}\s*$", m.group(1), re.M):
        print(f"FAIL: skill/SKILL.md frontmatter must say name: {NAME}")
        return 1
    lines = md.count("\n") + 1
    if lines >= 500:
        print(f"FAIL: SKILL.md is {lines} lines; keep it under 500.")
        return 1

    files = sorted(p for p in SKILL.rglob("*") if p.is_file()
                   and not SKIP_DIRS.intersection(p.parts)
                   and p.suffix not in SKIP_SUFFIX and p.name not in SKIP_NAMES)
    args.out.mkdir(parents=True, exist_ok=True)
    dest = args.out / f"{NAME}.skill"
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(f"{NAME}/{p.relative_to(SKILL).as_posix()}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if p.suffix == ".py" else 0o644) << 16
            z.writestr(info, p.read_bytes())
    print(f"OK    {dest}  ({len(files)} files, SKILL.md {lines} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
