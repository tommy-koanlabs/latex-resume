#!/usr/bin/env python3
"""Verify a built resume (or cover letter) PDF the way an ATS will read it.

Usage:
    python scripts/ats_check.py <resume.pdf> [--keywords keyword_map.md]
                                [--profile career_profile.md] [--pages 2]
    python scripts/ats_check.py <letter.pdf> --letter

Resume checks (references/style_resume.md, "Verification pass"):
  1. page count
  2. text layer: reading order, no ligature / private-use / replacement
     characters, no em dashes, no clearance-eligibility line
  3. email and phone in the first two extracted lines
  4. keyword map: Strong/Have/Adjacent found, Gap absent   (needs --keywords)
  5. every Skills item backed by a bullet or a profile line (stronger with --profile)
  6. titles, employers, dates identical to the profile      (needs --profile)
  7. no <placeholder> text
Letter checks: one page, clean text layer, no em dash, no colon or semicolon
in the body, signature image present, no placeholder text.

Text comes from pdftotext (poppler), else pypdf. With neither, the script says
extraction could not be verified and exits non-zero.

Each line is PASS, WARN, FAIL or SKIP. Exit status is 1 if any line FAILs.
WARN lines need a human look but do not fail the build: they are the cases
where forcing a fix could push the resume toward a claim the user cannot back.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
DATE_RANGE = rf"(?:{MONTHS}) \d{{4}} [–-] (?:Present|(?:{MONTHS}) \d{{4}})"
ROLE_LINE = re.compile(rf"^(\S.*?\S)\s{{2,}}({DATE_RANGE})\s*$")
REQUIRED_HEADINGS = ["Professional Summary", "Technical Skills",
                     "Professional Experience", "Education"]
OPTIONAL_HEADINGS = ["Publications", "Publications & Presentations", "Projects",
                     "Certifications", "Licenses & Certifications"]
ALL_HEADINGS = REQUIRED_HEADINGS + OPTIONAL_HEADINGS
STOPWORDS = {"a", "an", "the", "of", "in", "and", "or", "for", "with", "to",
             "per", "on", "at", "by", "as", "including"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?:\+\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
PLACEHOLDER = re.compile(r"<[^<>\n]{1,80}>")
BAD_CHARS = [
    (re.compile("[ﬀ-ﭏ]"), "ligature"),
    (re.compile("[-]"), "private-use"),
    (re.compile("�"), "replacement"),
    (re.compile("[\x00-\x08\x0b\x0e-\x1f]"), "control"),
]
EM_DASH = "—"


# ---------------------------------------------------------------- output
class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, list[str]]] = []

    def add(self, status: str, label: str, details: list[str] | None = None) -> None:
        self.rows.append((status, label, details or []))

    def print(self, title: str) -> int:
        print(title)
        for status, label, details in self.rows:
            print(f"[{status}] {label}")
            for d in details[:25]:
                print(f"         {d}")
            if len(details) > 25:
                print(f"         ... and {len(details) - 25} more")
        fails = sum(1 for s, _, _ in self.rows if s == "FAIL")
        warns = sum(1 for s, _, _ in self.rows if s == "WARN")
        verdict = "FAIL" if fails else "PASS"
        print(f"Result: {verdict} ({fails} failed, {warns} warning{'s' if warns != 1 else ''})")
        return 1 if fails else 0


# ---------------------------------------------------------------- extraction
def extract(pdf: Path) -> tuple[str | None, str]:
    if shutil.which("pdftotext"):
        p = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                           capture_output=True, text=True, encoding="utf-8")
        if p.returncode == 0:
            return p.stdout, "pdftotext"
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text(extraction_mode="layout"))
            except TypeError:  # older pypdf
                pages.append(page.extract_text())
        return "\f".join(pages), "pypdf"
    except ImportError:
        return None, ""


def page_count(pdf: Path, text: str) -> int:
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            return int(m.group(1))
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        return len(text.rstrip("\f").split("\f"))


# ---------------------------------------------------------------- matching
def _stem(w: str) -> str:
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 4 and w.endswith("sses"):
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        w = w[:-1]
    for suf in ("ing", "ed"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def tokens(s: str) -> list[str]:
    s = s.lower().replace("&", " and ").replace("’", "'")
    s = re.sub(r"\(s\)", "", s)               # test station(s) -> test station
    s = re.sub(r"(?<=\w)\.(?=\w)", "", s)     # m.s. -> ms, y14.5 -> y145
    s = s.replace(".", " ")
    words = re.findall(r"[a-z0-9]+", s)
    return [_stem(w) for w in words if w not in STOPWORDS]


def contains_seq(hay: list[str], needle: list[str]) -> bool:
    if not needle:
        return False
    n = len(needle)
    first = needle[0]
    for i, w in enumerate(hay):
        if w == first and hay[i:i + n] == needle:
            return True
    return False


def split_top(s: str, seps: str = ",;:") -> list[str]:
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch in seps and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def forms(term: str) -> tuple[str, str | None]:
    """'Bill of Materials (BOM)' -> ('Bill of Materials', 'BOM')."""
    m = re.match(r"^(.*?)\s*\(([^()]+)\)\s*$", term)
    if m and m.group(1).strip():
        return m.group(1).strip(), m.group(2).strip()
    return term.strip(), None


# ---------------------------------------------------------------- resume parsing
def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"_header": []}
    cur = "_header"
    for line in lines:
        s = line.strip().lstrip("\f")
        if s in ALL_HEADINGS:
            cur = s
            sections.setdefault(cur, [])
            continue
        sections[cur].append(line.replace("\f", ""))
    return sections


def units(lines: list[str]) -> list[str]:
    """Group lines into bullets / entry lines (a bullet's continuation lines are indented)."""
    out: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        stripped = line.lstrip()
        if line.startswith((" ", "\t")) and out and not stripped.startswith("–"):
            out[-1] += " " + stripped
        else:
            out.append(stripped)
    return out


def skill_items(lines: list[str]) -> list[tuple[str, str]]:
    joined: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r"^[^,:]{1,60}:\s", s) or not joined:
            joined.append(s)
        else:
            joined[-1] += " " + s
    items = []
    for row in joined:
        label, _, rest = row.partition(":")
        for item in split_top(rest, ","):
            items.append((label.strip(), item))
    return items


# ---------------------------------------------------------------- profile parsing
def md_tables(text: str) -> list[list[list[str]]]:
    tables, cur = [], []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            cur.append(cells)
        elif cur:
            tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    return tables


def section_text(md: str, heading: str) -> str:
    m = re.search(rf"^##\s+{re.escape(heading)}\b.*?$(.*?)(?=^##\s|\Z)", md, re.M | re.S | re.I)
    return m.group(1) if m else ""


def norm_dash(s: str) -> str:
    return re.sub(r"\s*(?:--|–)\s*", " – ", s.replace("\\&", "&")).strip()


def profile_roles(md: str) -> list[dict]:
    roles = []
    body = section_text(md, "Roles")
    for block in re.split(r"^###\s+", body, flags=re.M)[1:]:
        title, _, rest = block.partition("\n")
        role = {"title": title.strip().strip("*").replace("\\&", "&")}
        for key in ("Employer", "Context", "City", "Dates", "Approved descriptors"):
            m = re.search(rf"^\s*[-*]\s*{key}:\s*(.+)$", rest, re.M | re.I)
            role[key.lower()] = m.group(1).strip().replace("\\&", "&") if m else ""
        descs = role["approved descriptors"]
        role["descriptors"] = [] if descs.lower() in ("", "none", "n/a", "-") else \
            [d.strip().strip('"') for d in descs.split(";") if d.strip()]
        role["dates"] = norm_dash(role["dates"])
        roles.append(role)
    return roles


def profile_tools(md: str) -> list[tuple[str, str]]:
    body = section_text(md, "Tools and skills")
    rows = []
    for table in md_tables(body):
        header = [h.lower() for h in table[0]]
        if "item" not in header[0]:
            continue
        lvl = next((i for i, h in enumerate(header) if "level" in h), 1)
        for r in table[1:]:
            if len(r) > lvl:
                rows.append((r[0].replace("\\&", "&"), r[lvl].lower().strip("* ")))
    return rows


def profile_gaps(md: str) -> list[str]:
    body = section_text(md, "Confirmed gaps")
    gaps = re.findall(r"^\s*[-*]\s*\*\*(.+?)\*\*", body, re.M)
    return [g.strip() for g in gaps]


# ---------------------------------------------------------------- checks
def check_text_layer(rep: Report, text: str, lines: list[str], sections: dict,
                     letter: bool) -> None:
    bad = []
    for i, line in enumerate(lines, 1):
        for rx, kind in BAD_CHARS:
            for m in rx.finditer(line):
                bad.append(f"line {i}: {kind} U+{ord(m.group()):04X} in {line.strip()[:70]!r}")
    order = []
    if not letter:
        found = [h for h in REQUIRED_HEADINGS if h in sections]
        missing = [h for h in REQUIRED_HEADINGS if h not in sections]
        if missing:
            order.append(f"missing section heading(s): {', '.join(missing)}")
        heads_in_text = [l.strip().lstrip("\f") for l in lines if l.strip().lstrip("\f") in ALL_HEADINGS]
        req_seq = [h for h in heads_in_text if h in REQUIRED_HEADINGS]
        if req_seq != found:
            order.append(f"headings out of order: {' > '.join(heads_in_text)}")
        edu = heads_in_text.index("Education") if "Education" in heads_in_text else None
        for h in heads_in_text:
            if h in OPTIONAL_HEADINGS and edu is not None and heads_in_text.index(h) < edu:
                order.append(f"'{h}' comes before Education")
        for i, line in enumerate(lines, 1):
            ranges = re.findall(DATE_RANGE, line)
            if len(ranges) > 1:
                order.append(f"line {i}: two date ranges on one line (column bleed): {line.strip()[:80]!r}")
            elif ranges and not ROLE_LINE.match(line.replace("\f", "")):
                order.append(f"line {i}: date range not on a title line: {line.strip()[:80]!r}")
    if bad or order:
        rep.add("FAIL", "2. Text layer reads in order with clean characters", bad + order)
    else:
        rep.add("PASS", "2. Text layer reads in order with clean characters")

    dashes = [f"line {i}: {l.strip()[:80]!r}" for i, l in enumerate(lines, 1) if EM_DASH in l]
    rep.add("FAIL" if dashes else "PASS", "2b. No em dashes (style rule)", dashes)

    if not letter:
        clr = [l.strip() for l in lines
               if re.search(r"\b(?:able to obtain|eligible|eligibility|obtainable|clearable)\b.*clearance|"
                            r"clearance.*\b(?:eligible|eligibility|obtain)", l, re.I)]
        rep.add("FAIL" if clr else "PASS",
                "2c. No clearance-eligibility line (eligibility is not a clearance)", clr)


def check_fonts(rep: Report, pdf: Path) -> None:
    if not shutil.which("pdffonts"):
        rep.add("SKIP", "2d. Fonts embedded with Unicode maps (pdffonts not installed)")
        return
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()
    bad = []
    for line in out[2:]:
        parts = line.split()
        if len(parts) >= 5 and (parts[-5] != "yes" or parts[-3] != "yes"):
            bad.append(line.strip())
    rep.add("FAIL" if bad else "PASS", "2d. Fonts embedded with Unicode maps", bad)


def check_contact(rep: Report, lines: list[str]) -> None:
    first = [l.strip() for l in lines if l.strip()][:2]
    joined = " ".join(first)
    miss = []
    if not EMAIL.search(joined):
        miss.append("no email address")
    if not PHONE.search(joined):
        miss.append("no phone number")
    rep.add("FAIL" if miss else "PASS", "3. Email and phone in the first two lines",
            miss + ([f"first lines: {first}"] if miss else []))


def parse_keyword_map(md: str) -> list[dict]:
    for table in md_tables(md):
        header = [h.lower() for h in table[0]]
        if not any("status" in h for h in header):
            continue
        k = next((i for i, h in enumerate(header) if "keyword" in h), 0)
        s = next(i for i, h in enumerate(header) if "status" in h)
        w = next((i for i, h in enumerate(header) if "where" in h), None)
        rows = []
        for r in table[1:]:
            if len(r) <= s:
                continue
            rows.append({
                "keyword": r[k].strip("`* "),
                "status": re.sub(r"[^a-z]", "", r[s].lower().split()[0]) if r[s].split() else "",
                "where": r[w] if w is not None and len(r) > w else "",
            })
        return rows
    return []


def check_keywords(rep: Report, rows: list[dict], text: str, profile_md: str | None) -> None:
    hay = tokens(text)
    hay_set = set(hay)
    fails, warns, skips, found, total = [], [], [], 0, 0

    def present(term: str) -> bool:
        return contains_seq(hay, tokens(term))

    for row in rows:
        kw, status = row["keyword"], row["status"]
        if status not in ("strong", "have", "adjacent", "gap"):
            if status:
                skips.append(f"{kw!r}: status '{status}' not checked")
            continue
        total += 1
        terms = split_top(kw)
        if status == "gap":
            hits = []
            for t in terms:
                spelled, acr = forms(t)
                for f in (spelled, acr):
                    if f and present(f):
                        hits.append(f)
            if hits:
                fails.append(f"Gap keyword appears on the resume: {', '.join(hits)}  (row {kw!r})")
            else:
                found += 1
            continue
        if re.match(r"\s*not on (the )?resume", row["where"], re.I):
            skips.append(f"{kw!r}: map says not on resume ({row['where'][:60]})")
            total -= 1
            continue
        missing, partial = [], []
        for t in terms:
            spelled, acr = forms(t)
            has_sp, has_acr = present(spelled), (present(acr) if acr else True)
            if has_sp and has_acr:
                continue
            if acr and (has_sp or has_acr):
                partial.append(f"{t} (only {'spelled-out form' if has_sp else 'acronym'} found)")
                continue
            toks = tokens(spelled)
            share = sum(1 for x in toks if x in hay_set) / max(1, len(toks))
            (partial if share >= 0.5 else missing).append(t)
        if missing:
            fails.append(f"[{status}] {kw!r}: not found: {', '.join(missing)}")
        elif partial:
            warns.append(f"[{status}] {kw!r}: not verbatim: {', '.join(partial)}")
        else:
            found += 1

    if profile_md:
        for g in profile_gaps(profile_md):
            if present(g):
                fails.append(f"confirmed gap from the profile appears on the resume: {g!r}")

    label = f"4. Keywords: {found} of {total} rows as mapped"
    if fails:
        rep.add("FAIL", label, fails + warns)
    elif warns:
        rep.add("WARN", label + " (check wording; reword only when it is the same thing)", warns)
    else:
        rep.add("PASS", label)
    if skips:
        rep.add("SKIP", "4b. Keyword rows not checked against the resume", skips)


def check_skills(rep: Report, sections: dict, profile_md: str | None) -> None:
    skills = skill_items(sections.get("Technical Skills", []))
    if not skills:
        rep.add("FAIL", "5. Skills items backed by evidence", ["no Technical Skills items found"])
        return
    body = []
    for h in ("Professional Experience", "Projects", "Publications",
              "Publications & Presentations", "Education", "Certifications",
              "Licenses & Certifications"):
        body += units(sections.get(h, []))
    body_tokens = [set(tokens(u)) for u in body]
    tools = profile_tools(profile_md) if profile_md else []
    gaps = profile_gaps(profile_md) if profile_md else []

    def in_bullet(term: str) -> bool:
        t = set(tokens(term))
        return bool(t) and any(t <= u for u in body_tokens)

    def profile_level(term: str) -> str | None:
        t = tokens(term)
        for item, level in tools:
            for f in (item, *[x for x in forms(item) if x]):
                if t and set(t) <= set(tokens(f)):
                    return level
        return None

    fails, warns = [], []
    for label, item in skills:
        spelled, acr = forms(item)
        cands = [item, spelled] + ([acr] if acr else [])
        if any(set(tokens(g)) and set(tokens(g)) <= set(tokens(item)) for g in gaps):
            fails.append(f"{label}: {item} -- listed as a confirmed gap in the profile")
            continue
        bullet = any(in_bullet(c) for c in cands)
        level = next((lv for c in cands if (lv := profile_level(c))), None)
        if profile_md is not None:
            if level and "gap" in level:
                fails.append(f"{label}: {item} -- profile marks it a gap")
            elif level and "exposure" in level and not bullet:
                fails.append(f"{label}: {item} -- exposure-level; needs a bullet stating its narrow use")
            elif not bullet and not level:
                fails.append(f"{label}: {item} -- no bullet and no Tools and skills row")
        elif not bullet:
            warns.append(f"{label}: {item} -- no bullet; confirm a profile line (pass --profile)")

    n = len(skills)
    if fails:
        rep.add("FAIL", f"5. Skills items backed by evidence ({n} items)", fails + warns)
    elif warns:
        rep.add("WARN", f"5. Skills items backed by evidence ({n} items)", warns)
    else:
        rep.add("PASS", f"5. Skills items backed by evidence ({n} items)")


def check_roles(rep: Report, sections: dict, profile_md: str | None) -> None:
    exp = [l.replace("\f", "") for l in sections.get("Professional Experience", [])]
    found = []
    for i, line in enumerate(exp):
        m = ROLE_LINE.match(line)
        if m:
            nxt = next((l.strip() for l in exp[i + 1:] if l.strip()), "")
            found.append((m.group(1).strip(), m.group(2).strip(), nxt))
    if not found:
        rep.add("FAIL", "6. Titles, employers, dates match the profile", ["no role lines found"])
        return
    if profile_md is None:
        rep.add("SKIP", f"6. Titles, employers, dates match the profile ({len(found)} roles; pass --profile)")
        return
    roles = profile_roles(profile_md)
    if not roles:
        rep.add("FAIL", "6. Titles, employers, dates match the profile",
                ["no roles parsed from the profile (expected '### <Official title>' under '## Roles')"])
        return
    fails = []
    for title, dates, emp_line in found:
        match = None
        for r in roles:
            allowed = [r["title"]] + [f"{r['title']} – {d}" for d in r["descriptors"]]
            if title in allowed:
                match = r
                if r["dates"] == dates and emp_line.startswith(r["employer"]):
                    break
        if not match:
            fails.append(f"title not in profile (verbatim or with an approved descriptor): {title!r}")
            continue
        if match["dates"] != dates:
            fails.append(f"{title!r}: dates {dates!r} != profile {match['dates']!r}")
        if not match["employer"] or not emp_line.startswith(match["employer"]):
            fails.append(f"{title!r}: employer line {emp_line!r} does not start with {match['employer']!r}")
        if match["city"] and not emp_line.endswith(match["city"]):
            fails.append(f"{title!r}: employer line {emp_line!r} does not end with {match['city']!r}")
    rep.add("FAIL" if fails else "PASS",
            f"6. Titles, employers, dates match the profile ({len(found)} roles)", fails)


def check_placeholders(rep: Report, lines: list[str], label: str) -> None:
    hits = [f"line {i}: {m.group()}" for i, l in enumerate(lines, 1) for m in PLACEHOLDER.finditer(l)]
    rep.add("FAIL" if hits else "PASS", label, hits)


def check_letter(rep: Report, pdf: Path, lines: list[str]) -> None:
    start = next((i for i, l in enumerate(lines) if l.strip().startswith("Dear ")), None)
    end = next((i for i, l in enumerate(lines) if l.strip().rstrip(",") in
                ("Sincerely", "Respectfully", "Best regards", "Regards")), None)
    if start is None or end is None or end <= start:
        rep.add("FAIL", "8. Body found between salutation and sign-off",
                ["could not find a 'Dear ...' line and a 'Sincerely,' line"])
        return
    body = lines[start + 1:end]
    punct = [f"{l.strip()[:90]!r}" for l in body if re.search(r"[:;]", l)]
    rep.add("FAIL" if punct else "PASS", "8. No colon or semicolon in the body", punct)
    if shutil.which("pdfimages"):
        out = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True).stdout
        n = sum(1 for l in out.splitlines()[2:] if l.split()[2:3] == ["image"])
        rep.add("PASS" if n else "WARN", f"8b. Signature image present ({n} image{'s' if n != 1 else ''})",
                [] if n else ["no image found; the class printed the typed name instead"])
    else:
        rep.add("SKIP", "8b. Signature image present (pdfimages not installed)")


# ---------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--keywords", type=Path, help="keyword_map.md with a coverage table")
    ap.add_argument("--profile", type=Path, help="career_profile.md")
    ap.add_argument("--pages", type=int, help="expected page count (default 2; 1 with --letter)")
    ap.add_argument("--letter", action="store_true", help="check a cover letter instead of a resume")
    args = ap.parse_args(argv)

    rep = Report()
    if not args.pdf.exists():
        print(f"FAIL: {args.pdf} not found")
        return 1
    text, tool = extract(args.pdf)
    if text is None:
        print("FAIL: text extraction could not be verified. Install poppler (pdftotext) "
              "or `pip install pypdf`, then rerun.")
        return 1
    lines = text.splitlines()
    want = args.pages or (1 if args.letter else 2)
    pages = page_count(args.pdf, text)
    rep.add("PASS" if pages == want else "FAIL", f"1. Page count: {pages} (expected {want})")

    if args.letter:
        check_text_layer(rep, text, lines, {}, letter=True)
        check_fonts(rep, args.pdf)
        check_letter(rep, args.pdf, lines)
        check_placeholders(rep, lines, "7. No <placeholder> text")
        return rep.print(f"Cover letter check: {args.pdf} (text via {tool})")

    profile_md = args.profile.read_text(encoding="utf-8") if args.profile else None
    sections = split_sections(lines)
    check_text_layer(rep, text, lines, sections, letter=False)
    check_fonts(rep, args.pdf)
    check_contact(rep, lines)
    if args.keywords:
        rows = parse_keyword_map(args.keywords.read_text(encoding="utf-8"))
        if rows:
            check_keywords(rep, rows, text, profile_md)
        else:
            rep.add("FAIL", "4. Keywords", [f"no coverage table with a Status column in {args.keywords}"])
    else:
        rep.add("SKIP", "4. Keywords (pass --keywords keyword_map.md)")
    check_skills(rep, sections, profile_md)
    check_roles(rep, sections, profile_md)
    check_placeholders(rep, lines, "7. No <placeholder> text")
    return rep.print(f"ATS check: {args.pdf} (text via {tool})")


if __name__ == "__main__":
    sys.exit(main())
