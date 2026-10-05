#!/usr/bin/env python3
"""Scripted checks for the resume-tailor evals (evals/evals.json).

Usage:
    python evals/check_outputs.py <eval_id> <outputs_dir> [--baseline <eval-1 outputs_dir>]

<outputs_dir> holds what one eval run produced: the resume (and letter) PDF
and .tex, keyword_map.md, any updated career_profile.md, and transcript.md.
transcript.md is every message in order, each preceded by a line
`--- skill ---` or `--- user ---`.

Covers the expectations marked "(scripted)". The rest need a human or a
grader reading the outputs. Prints PASS/FAIL per check; exits 1 on any FAIL.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skill" / "scripts"
FIX = ROOT / "evals" / "fixtures"
sys.path.insert(0, str(SCRIPTS))
import ats_check  # noqa: E402

PROFILE_FULL = FIX / "john_doe" / "career_profile.md"
PROFILE_THIN = FIX / "john_doe_thin" / "career_profile.md"


class Checks:
    def __init__(self) -> None:
        self.fails = 0

    def __call__(self, ok: bool, label: str, detail: str = "") -> bool:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail and not ok else ""))
        self.fails += not ok
        return ok


def text_of(pdf: Path) -> str:
    t, _ = ats_check.extract(pdf)
    return t or ""


def find(out: Path, letter: bool = False) -> Path | None:
    pdfs = sorted(p for p in out.rglob("*.pdf") if ("CoverLetter" in p.name) == letter)
    return pdfs[0] if pdfs else None


def skill_messages(out: Path) -> list[str]:
    tr = out / "transcript.md"
    if not tr.exists():
        return []
    parts = re.split(r"^--- (skill|user) ---\s*$", tr.read_text(encoding="utf-8"), flags=re.M)
    return [parts[i + 1] for i in range(1, len(parts) - 1, 2) if parts[i] == "skill"]


def numbered_questions(msg: str) -> int:
    return len(re.findall(r"^\s*\d+[.)]\s", msg, re.M))


def question_items(msg: str) -> str:
    """Text of the numbered items only (a closing note that names settled gaps is not a question)."""
    items = re.findall(r"^\s*\d+[.)]\s.*?(?=^\s*\d+[.)]\s|^\s*$|\Z)", msg, re.M | re.S)
    return "\n".join(items)


def run_ats(c: Checks, pdf: Path, *extra: str, label: str) -> None:
    p = subprocess.run([sys.executable, str(SCRIPTS / "ats_check.py"), str(pdf), *extra],
                       capture_output=True, text=True)
    fails = [l for l in p.stdout.splitlines() if l.startswith("[FAIL]")]
    c(p.returncode == 0, label, "; ".join(fails))


def absent(c: Checks, text: str, words: list[str], label: str) -> None:
    hits = [w for w in words if re.search(w, text, re.I)]
    c(not hits, label, f"found: {hits}")


def sections(pdf: Path) -> dict:
    return ats_check.split_sections(text_of(pdf).splitlines())


def role_titles(pdf: Path) -> list[str]:
    exp = sections(pdf).get("Professional Experience", [])
    return [m.group(1).strip() for l in exp if (m := ats_check.ROLE_LINE.match(l))]


def first_skill_line(pdf: Path) -> str:
    lines = [l.strip() for l in sections(pdf).get("Technical Skills", []) if l.strip()]
    return lines[0] if lines else ""


def summary(pdf: Path) -> str:
    return " ".join(l.strip() for l in sections(pdf).get("Professional Summary", []))


def common_resume(c: Checks, out: Path, profile: Path, pages: int | None = 2) -> Path | None:
    pdf = find(out)
    if not c(pdf is not None, "resume PDF present"):
        return None
    c(pdf.with_suffix(".tex").exists(), "resume .tex present")
    km = out / "keyword_map.md"
    args = ["--profile", str(profile)]
    if km.exists():
        args += ["--keywords", str(km)]
    if pages is None:
        pages = ats_check.page_count(pdf, "")
        c(pages in (1, 2), f"resume is one or two pages ({pages})")
    run_ats(c, pdf, *args, "--pages", str(pages), label=f"ats_check passes ({pages} pages, profile"
            + (", keyword map)" if km.exists() else ")"))
    s = summary(pdf)
    absent(c, s, [r"\b(I|my|me)\b", r"\d+\+?\s*years"], "summary has no first person and no years count")
    return pdf


def eval1(c: Checks, out: Path, _b) -> None:
    pdf = common_resume(c, out, PROFILE_FULL)
    c((out / "keyword_map.md").exists(), "keyword_map.md present")
    if pdf:
        absent(c, text_of(pdf), ["Teamcenter", "LabVIEW", "clearance"], "resume has no gap keywords")
    msgs = skill_messages(out)
    if c(bool(msgs), "transcript.md present"):
        c(numbered_questions(msgs[0]) == 0 or "Targeted" in msgs[0], "no question batch before delivery")
        last = msgs[-1]
        for g in ["NX", "Teamcenter", "LabVIEW", "clearance"]:
            c(re.search(g, last, re.I) is not None, f"delivery message lists gap: {g}")


def eval2(c: Checks, out: Path, base: Path | None) -> None:
    pdf = common_resume(c, out, PROFILE_FULL)
    if not pdf:
        return
    absent(c, text_of(pdf), ["HyperMesh", "Patran", "NASGRO", "composite", "Teamcenter",
                             "LabVIEW", "clearance"], "resume has no gap keywords")
    first = first_skill_line(pdf)
    c(re.search(r"analysis|FEA|Nastran|ANSYS|stress", first, re.I) is not None,
      "first skills line is about analysis", first)
    if base and (b := find(base)):
        c(role_titles(pdf) == role_titles(b), "role order and titles identical to eval 1",
          f"{role_titles(pdf)} vs {role_titles(b)}")
        c(summary(pdf) != summary(b), "summary differs from eval 1")
        c(first != first_skill_line(b), "first skills line differs from eval 1")
    else:
        c(role_titles(pdf)[:1] == ["Senior Mechanical Design Engineer"],
          "newest role first (pass --baseline for the full comparison)")


def eval3(c: Checks, out: Path, _b) -> None:
    msgs = skill_messages(out)
    if c(bool(msgs), "transcript.md present"):
        q = msgs[0]
        n = numbered_questions(q)
        c(1 <= n <= 5, f"first message is one batch of 1 to 5 questions ({n})")
        c(re.search(r"oscilloscopes, power\s+supplies, and\s+multimeters", q, re.I) is not None,
          "a question quotes the bench test equipment line")
        c(re.search(r"Acceptance Test Procedures|ATPs", q) is not None, "a question quotes the ATP line")
        absent(c, question_items(q), ["Teamcenter", "LabVIEW"], "no question about already confirmed gaps")
    pdf = common_resume(c, out, PROFILE_THIN)
    if pdf:
        absent(c, text_of(pdf), [r"oscilloscope", r"multimeter", r"power suppl", r"acceptance test procedure",
                                 r"\bATPs?\b"], "resume has none of the denied keywords")
    prof = out / "career_profile.md"
    if c(prof.exists(), "updated career_profile.md present"):
        gaps = " ".join(ats_check.profile_gaps(prof.read_text(encoding="utf-8")))
        c(re.search(r"oscilloscope|bench|test equipment", gaps, re.I) is not None,
          "profile confirms the test equipment gap", gaps)
        c(re.search(r"ATP|acceptance", gaps, re.I) is not None, "profile confirms the ATP gap", gaps)


def eval4(c: Checks, out: Path, _b) -> None:
    msgs = skill_messages(out)
    if c(bool(msgs), "transcript.md present"):
        n = numbered_questions(msgs[0])
        c(1 <= n <= 5, f"first message is one batch of 1 to 5 questions ({n})")
    prof = out / "career_profile.md"
    if not c(prof.exists(), "career_profile.md built and returned"):
        return
    md = prof.read_text(encoding="utf-8")
    for h in ["Contact", "Status", "Roles", "Tools and skills", "Education", "Confirmed gaps", "Q&A log"]:
        c(re.search(rf"^##\s+{re.escape(h)}", md, re.M) is not None, f"profile has section: {h}")
    lv = [lvl for item, lvl in ats_check.profile_tools(md) if "labview" in item.lower()]
    in_gaps = any("labview" in g.lower() for g in ats_check.profile_gaps(md))
    c(in_gaps or (bool(lv) and all(("daily" not in x and "applied" not in x) for x in lv)),
      "LabVIEW recorded as exposure or a gap", str(lv))
    pdf = common_resume(c, out, prof, pages=None)
    if pdf:
        t = text_of(pdf)
        c("Test Engineer I" in t, "title 'Test Engineer I' kept verbatim")
        absent(c, t, ["LabVIEW", r"3\.40", r"2\+\s*years", "passionate"], "resume drops unbacked or stale items")


STOCK = [r"thrilled", r"groundbreaking", r"cutting[- ]edge", r"passionate", r"align(s)? perfectly",
         r"proven track record", r"\bleverag", r"world[- ]class", r"industry[- ]leading", "—"]


def eval5(c: Checks, out: Path, _b) -> None:
    msgs = skill_messages(out)
    if c(bool(msgs), "transcript.md present"):
        c("Windchill" in msgs[0], "turn 1 reply offers Windchill PLM")
    for pdf in out.rglob("*.pdf"):
        if "CoverLetter" not in pdf.name:
            absent(c, text_of(pdf), ["Teamcenter"], f"{pdf.name} has no Teamcenter")
    letter = find(out, letter=True)
    if not c(letter is not None, "cover letter PDF present"):
        return
    run_ats(c, letter, "--letter", label="ats_check --letter passes")
    t = text_of(letter)
    c(re.search(r"\bNX\b", t) is not None, "letter names the NX gap")
    c(re.search(r"clearance", t, re.I) is not None, "letter names the clearance gap")
    absent(c, t, STOCK, "letter has no stock flattery or em dash")
    c(any(p.name == "signature.png" for p in out.rglob("signature.png")), "signature.png in outputs")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("eval_id", type=int, choices=range(1, 6))
    ap.add_argument("outputs", type=Path)
    ap.add_argument("--baseline", type=Path, help="eval 1 outputs, for eval 2's comparisons")
    a = ap.parse_args()
    c = Checks()
    print(f"Eval {a.eval_id}: {a.outputs}")
    [eval1, eval2, eval3, eval4, eval5][a.eval_id - 1](c, a.outputs, a.baseline)
    print(f"Result: {'FAIL' if c.fails else 'PASS'} ({c.fails} failed)")
    return 1 if c.fails else 0


if __name__ == "__main__":
    sys.exit(main())
