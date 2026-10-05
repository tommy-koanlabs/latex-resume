#!/usr/bin/env python3
"""Compile a resume or cover letter .tex with the skill's LaTeX classes.

Usage:
    python scripts/build.py <file.tex> [<file.tex> ...] [--out DIR] [--pages N]
    python scripts/build.py              # rebuild both shipped examples

Finds resume.cls / coverletter.cls in ../assets and exposes them through
TEXINPUTS, so the .tex never needs a copy of the class beside it. Runs
pdfLaTeX twice, reports page count and overfull boxes, and removes aux files.
Falls back to tectonic. Never installs TeX: if no engine exists it says how
to compile on Overleaf instead.

Exit status is non-zero on any LaTeX error, on a missing engine, on a resume
over two pages, on a cover letter over one page, or when --pages is given and
the page count differs.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
EXAMPLES = SKILL_DIR / "references" / "examples"
EXAMPLE_FILES = [
    (EXAMPLES / "Doe_Calderwick_TestEquipment_CAS-10482.tex", 2),
    (EXAMPLES / "Doe_Calderwick_TestEquipment_CAS-10482_CoverLetter.tex", 1),
]
AUX_EXT = (".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz")
# Fixed timestamp for the shipped examples so rebuilding them does not change
# the PDF bytes. Does not affect \today (that needs FORCE_SOURCE_DATE).
EXAMPLE_EPOCH = "1791072000"  # 2026-10-04 00:00 UTC

OVERLEAF_MSG = """No LaTeX engine found (looked for pdflatex and tectonic).
To compile without installing anything:
  1. Go to https://www.overleaf.com and create a blank project.
  2. Upload {tex} and {cls}{sig}.
  3. Menu > Compiler: pdfLaTeX. Then Recompile and download the PDF."""


def doc_class(tex: Path) -> str:
    m = re.search(r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}", tex.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def page_count(pdf: Path, log_text: str = "") -> int | None:
    m = re.search(r"Output written on .*?\((\d+) pages?", log_text, re.S)
    if m:
        return int(m.group(1))
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            return int(m.group(1))
    try:
        from pypdf import PdfReader  # optional
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        pass
    data = pdf.read_bytes()
    n = len(re.findall(rb"/Type\s*/Page(?!s)", data))
    return n or None


def run_pdflatex(tex: Path, outdir: Path, env: dict) -> tuple[bool, str]:
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
           f"-output-directory={outdir}", tex.name]
    log = ""
    for _ in range(2):
        proc = subprocess.run(cmd, cwd=tex.parent, env=env, capture_output=True,
                              text=True, errors="replace")
        logfile = outdir / (tex.stem + ".log")
        log = logfile.read_text(errors="replace") if logfile.exists() else proc.stdout
        if proc.returncode != 0:
            return False, log
    return True, log


def run_tectonic(tex: Path, outdir: Path, env: dict) -> tuple[bool, str]:
    cmd = ["tectonic", "--keep-logs", "--outdir", str(outdir),
           "-Z", f"search-path={ASSETS}", tex.name]
    proc = subprocess.run(cmd, cwd=tex.parent, env=env, capture_output=True,
                          text=True, errors="replace")
    logfile = outdir / (tex.stem + ".log")
    log = logfile.read_text(errors="replace") if logfile.exists() else ""
    return proc.returncode == 0, log + proc.stdout + proc.stderr


def errors_from(log: str) -> list[str]:
    lines = log.splitlines()
    out = []
    for i, line in enumerate(lines):
        if line.startswith("! ") or line.startswith("error:"):
            out.append(" ".join(l.strip() for l in lines[i:i + 3] if l.strip()))
    return out


def overfull_from(log: str) -> list[str]:
    return [l.strip() for l in log.splitlines() if l.startswith("Overfull \\")]


def clean(outdir: Path, stem: str) -> None:
    for ext in AUX_EXT:
        p = outdir / (stem + ext)
        if p.exists():
            p.unlink()


def build(tex: Path, outdir: Path | None, want_pages: int | None,
          reproducible: bool = False) -> bool:
    tex = tex.resolve()
    if not tex.exists():
        print(f"FAIL  {tex}: file not found")
        return False
    outdir = (outdir or tex.parent).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    cls = doc_class(tex)

    env = os.environ.copy()
    # Trailing separator keeps the TeX distribution's own search path.
    env["TEXINPUTS"] = os.pathsep.join([str(ASSETS), str(tex.parent), env.get("TEXINPUTS", "")])
    if reproducible:
        env["SOURCE_DATE_EPOCH"] = EXAMPLE_EPOCH

    if shutil.which("pdflatex"):
        engine, runner = "pdflatex", run_pdflatex
    elif shutil.which("tectonic"):
        engine, runner = "tectonic", run_tectonic
    else:
        sig = " and signature.png" if cls == "coverletter" else ""
        print(OVERLEAF_MSG.format(tex=tex.name, cls=ASSETS / f"{cls or 'resume'}.cls", sig=sig))
        return False

    ok, log = runner(tex, outdir, env)
    pdf = outdir / (tex.stem + ".pdf")
    errs = errors_from(log)
    overfull = overfull_from(log)
    clean(outdir, tex.stem)

    if not ok or not pdf.exists():
        print(f"FAIL  {tex.name}: {engine} stopped with errors")
        for e in errs or ["(no error line found; rerun pdflatex by hand to see the log)"]:
            print(f"      {e}")
        return False

    pages = page_count(pdf, log)
    good = True
    notes = []
    limit = {"resume": 2, "coverletter": 1}.get(cls)
    if want_pages is not None and pages != want_pages:
        good = False
        notes.append(f"expected {want_pages} page(s)")
    elif limit is not None and pages is not None and pages > limit:
        good = False
        notes.append(f"a {cls} may not exceed {limit} page(s)")
    if errs:
        good = False
        notes.append(f"{len(errs)} LaTeX error(s)")

    status = "OK  " if good else "FAIL"
    print(f"{status}  {pdf}  ({pages} page{'s' if pages != 1 else ''}, {engine})"
          + (f"  -- {'; '.join(notes)}" if notes else ""))
    for e in errs:
        print(f"      error: {e}")
    for o in overfull:
        print(f"      warning: {o}")
    return good


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex", nargs="*", type=Path, help=".tex file(s); none = rebuild the examples")
    ap.add_argument("--out", type=Path, help="output directory (default: beside each .tex)")
    ap.add_argument("--pages", type=int, help="fail unless the PDF has exactly this many pages")
    args = ap.parse_args(argv)

    if args.tex:
        jobs = [(t, args.pages, False) for t in args.tex]
    else:
        jobs = [(t, n, True) for t, n in EXAMPLE_FILES]
    results = [build(t, args.out, n, repro) for t, n, repro in jobs]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
