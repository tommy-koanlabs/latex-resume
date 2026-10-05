# Resume style

Read this before drafting any resume. Layout is fixed by `assets/resume.cls`;
these are the content and judgment rules that sit on top of it. Read the class
and `references/examples/Doe_Calderwick_TestEquipment_CAS-10482.tex` too: the
example is the ground truth for format, voice, and tracing. It is condensed on
purpose, so copy its format and tracing, not its length.

## Contents
1. Length
2. Order
3. Header
4. Summary
5. Technical Skills
6. Bullets
7. Education, Publications, Projects
8. Page fit
9. ATS rules
10. Verification pass
11. Keyword map format
12. File names

## 1. Length

Two pages for experienced candidates. Large contractors screen with an ATS
first, so keyword coverage beats brevity, and a second page is worth it when it
carries real keywords. Never three pages. One page only when the user's real
content does not fill a page and a half. Never pad: a padded line is a line the
user must defend in an interview.

The most relevant role carries seven to ten bullets. Page two ends at least
half full, ideally about two thirds.

## 2. Order

Professional Summary, Technical Skills, Professional Experience, Education,
then Publications and Projects in whichever order suits the posting.

Experience is always reverse chronological. Ordering jobs by relevance was
tried once and reverted, because parsers and recruiters both expect dates to
descend and read a shuffled list as hiding something. Shift emphasis with
bullet count and bullet order instead: the most relevant role gets the most
bullets, even when it is not the newest.

## 3. Header

- Name centered, not bold (the class does this).
- One contact line: optional city, email, phone, separated by `\sep`. No
  street address.
- Citizenship is off by default. Add it as one more `\sep` item only when the
  profile preference says to show it. Worth offering to a user applying to
  clearance roles.
- An active clearance goes in the header only if the user holds one, in the
  profile's exact wording. "Able to obtain a clearance" is not a clearance and
  never appears on the resume. It belongs in the cover letter.

## 4. Summary

Three sentences, no first person.

1. An identity noun phrase that mirrors the posting's discipline
   ("Mechanical design engineer specializing in test stations...").
2. What the user delivers, in the posting's vocabulary.
3. The differentiator: the background that makes this person's version of the
   job better.

No years-of-experience count. It goes stale, it was once submitted out of
date, and it undercounts people with graduate degrees. The reader can work it
out from the dates.

## 5. Technical Skills

- Five to seven lines, each `\skill{Label}{item, item, item}`. Each line
  fits on one printed line; check the rendered page. A wrapped line turns a
  six-line section into nine, pushes roles across the page break, and reads
  as a keyword dump. Fix a wrap by dropping the line's weakest item or by
  splitting the category, not by shrinking anything.
- Build lines only from real tools, methods, and standards. On thin material,
  five honest lines beat a padded sixth; never invent a category of soft
  items ("Technician Training") just to reach the count.
- Rename and reorder categories for every posting so the first line is the
  posting's center of gravity.
- Name a tool once, at the level a recruiter searches for ("PTC Creo"). List
  modules only when the posting names them.
- Give each important term once spelled out with its acronym:
  "Bill of Materials (BOM)". ATS searches use either form.
- Order items inside a line by the user's real strength, not the posting's
  preference. The daily tool goes first even when the posting prefers another;
  "PTC Creo, Siemens NX" tells the truth about which one the user lives in.
- Every item needs a bullet or a confirmed profile line behind it. An
  exposure-level item needs a bullet that states its narrow use. A skill with
  neither is a fabrication, even if it was on an old resume. The original user
  restored a removed skill only after supplying the concrete projects behind
  it. That is the standard.
- Standards may be listed when the user has genuinely worked to them. Cite a
  standard inside a bullet only when the user is comfortable being questioned
  on it.

## 6. Bullets

- Action verb first. Present tense for ongoing duties in the current role,
  past tense for finished projects and earlier roles.
- One to three lines. Shape: what, how (tools, standards), result. A semicolon
  may join two related clauses.
- Use the posting's exact noun phrases when they name the same thing the user
  did. "Valve testing cart" becomes "valve test station" when the posting says
  "test station". It never becomes "structural test article".
- Most posting-relevant bullets first within each role.
- Metrics only from the profile, never rounded up.
- On team work, claim what the user personally did.
- Keep the claim level. "Prepared geometry in Siemens NX for meshing" is
  honest exposure; "Designed in Siemens NX" would not be.
- No em dashes, no parenthetical asides. En dashes appear only in date
  ranges, title descriptors, and the employer line. Acronym parentheses such
  as "(DAQ)" are not asides.
- When a publication title does not show what the user did, put the
  contribution in an experience bullet too. A poster titled after the science
  will not tell a recruiter that the user designed the test hardware behind
  it.
- No keyword stuffing. A posting keyword with no evidence stays off the
  resume. No hidden text, no white text, no keyword dumps.

Titles are verbatim from the profile. A functional descriptor after an en dash
is allowed only if it is stored in the profile as approved
(`Engineer IV -- Mechanical Design`). Never change level or scope.

## 7. Education, Publications, Projects

**Education.** `\degree{Degree, GPA}{Date}{School}{detail}`. Degree and GPA
bold with the date at right, school in italics, then one line for thesis title
or honors. Show GPA only at 3.5 or above. Credentials exactly as in the
profile.

**Publications.** Title the section "Publications" only if every entry is a
paper. Otherwise "Publications \& Presentations", and tag each non-paper:
"(Poster)", "(Report)". Drop abstract-only items and anything the profile
marks "do not use".

**Projects.** One format for the whole section: every project followed by a
plain line, or every project followed by bullets, never mixed. For senior
candidates keep school projects to a line or a title alone. Keep a project
when it carries an award the target employer would recognize, or when it is
the only honest evidence for a basic qualification (a personal electronics
project backing "hands-on with oscilloscopes").

## 8. Page fit

1. Use the class knobs in the order given in `assets/resume_template.tex`:
   `\resitemsep` 2pt to 1pt to 0pt, then `\resrolegap` 7pt to 5pt, then
   `\ressecbefore` 10pt to 8pt.
2. Then cut the weakest bullet from the oldest role.
3. Never change font size or margins.
4. Place `\pagebreak` between roles so no role splits across pages when that
   can be avoided. Never leave a role header or section heading as the last
   thing on a page. The class keeps a heading with its first line, but check
   the PDF.
5. Page two must be at least half full. If it is not, relevant bullets are
   still sitting unused in the profile, or the resume belongs on one page.

Check fit by looking at the rendered pages (`pdftoppm -png -r 50`), not only at
the page count.

## 9. ATS rules

A parser reads the PDF's text layer top to bottom. Any text it cannot extract,
or extracts out of order, is experience the user gets no credit for.

- pdfLaTeX only. The class loads `glyphtounicode`, so ligatures and dashes
  extract as plain Unicode.
- Single column. No tables, text boxes, images, icons, headers, or footers.
- Section names exactly as in the template.
- Dates as "Month YYYY -- Month YYYY" in the source (an en dash in the PDF),
  right-aligned on the title line.
- Contact details as plain text in the first two lines.
- Hyphenation is off, so keywords never split across lines.
- The header separator is `\sep`, a real vertical bar. The source resumes once
  typed `|`, which the old OT1 encoding silently printed as an em dash. Change
  the one `\sep` definition if a user prefers a dash or bullet.
- PDF title and author metadata come from the class.
- Escape LaTeX specials in content: `\&`, `\%`, `\$`, `\#`, `\_`.

## 10. Verification pass

Run after every build:

```
python scripts/build.py <resume>.tex
python scripts/ats_check.py <resume>.pdf --keywords keyword_map.md --profile career_profile.md
```

`ats_check.py` covers:

1. Page count is as intended (`--pages 1` for a one-page resume).
2. `pdftotext -layout` reads in visual order with no ligature, private-use,
   or replacement characters, and no em dashes.
3. Email and phone are in the first two extracted lines.
4. Every keyword marked Strong, Have, or Adjacent appears; every Gap appears
   zero times; no confirmed profile gap appears.
5. Every Skills item has a bullet or a confirmed profile line behind it.
6. Titles, employers, and dates are character-identical to the profile.
7. No `<placeholder>` text remains.

Any FAIL is fixed before delivery. A WARN gets a look: under check 4 it
usually means the resume paraphrases a posting phrase. Switch to the posting's
words if they describe the same thing; if they do not, leave it and note it in
the keyword map. Never reword toward a claim the user cannot back to clear a
warning.

## 11. Keyword map format

Write `keyword_map.md` beside the resume, modeled on
`references/examples/keyword_map.md`: posting read, Q&A (if any), coverage
table, gaps, checks. The coverage table is machine-read by `ats_check.py`, so
keep its shape:

```
| Posting keyword or phrase | Source in posting | Status | Where it lands in the resume |
|---|---|---|---|
| test station(s) | Title, resp. | Strong | Summary; Skills 1; Role 1 bullets 1, 3 |
| Teamcenter | Resp., preferred | Gap | Not on resume. "Windchill PLM" carries the PLM keyword. |
```

- Status is one of Strong, Have, Adjacent, Gap, Unknown. Unknown should never
  survive to delivery: it was either asked about or turned into a gap.
- Put the phrase in the first column the way it should appear on the resume
  when it is honest to use it. Separate distinct terms with commas.
- A Have row that is deliberately kept off the resume (citizenship stated only
  in the letter) starts its last cell with "Not on resume".

## 12. File names

`<Last>_<Company>_<RoleShort>_<ReqID>.tex`, for example
`Doe_Calderwick_TestEquipment_CAS-10482.tex`. No spaces. The PDF takes the
same stem.
