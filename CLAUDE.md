# resume-tailor: build brief

You are building a Claude Skill called `resume-tailor`. This file is the whole
brief. The person who wrote it will not be available for questions, so when
something is not covered here, choose the option that best protects rule 3.1
(never fabricate) and write the decision down in `DECISIONS.md`.

## 1. What the skill does

The user pastes a job posting. The skill returns an ATS-optimized LaTeX resume
(PDF + `.tex`) tailored to that posting, built only from the user's real
experience. On request it also writes a matching one-page cover letter with a
script-font signature.

If the user's material is thin, or the posting asks for something the material
does not cover, the skill asks targeted questions first and only then writes.
It never invents experience, credentials, or metrics, and never inflates a job
title.

First users are engineers applying to aerospace and defense roles. Do not
hard-code a discipline. Nothing in the workflow is specific to mechanical
engineering.

It must work in two places:

| Surface | LaTeX | Persistence |
|---|---|---|
| Claude.ai with code execution | pdfLaTeX is in the container | None between chats. Hand the user any file they must keep. |
| Claude Code on the user's machine | May be missing | Working directory |

## 2. Definition of done

1. `skill/` packages into `resume-tailor.skill` and `SKILL.md` is under 500 lines.
2. `python skill/scripts/build.py` rebuilds both example PDFs from source:
   resume 2 pages, cover letter 1 page, zero LaTeX errors.
3. `python skill/scripts/ats_check.py` passes on the example resume.
4. `python skill/scripts/make_signature.py --name "John Doe"` writes a PNG that
   the cover letter class picks up without edits.
5. The five evals in section 13 pass.
6. No real person's data anywhere in the repo or its history.

## 3. Hard rules (the product's core promise)

These go near the top of `SKILL.md`, with the reasons. A resume that gets an
interview on a false claim fails the user at the interview, and a user who
catches one invented line stops trusting every other line.

1. **Evidence only.** Every claim traces to the user's material: an old resume,
   the career profile, or an answer the user gave. If you cannot point to the
   source, you cannot write it.
2. **Titles verbatim.** Never change level or scope ("Engineer" stays
   "Engineer", not "Senior" or "Lead"). When an official title is generic, a
   functional descriptor after an en dash is allowed ("Engineer IV – Mechanical
   Design") only if it describes the real work and the user has approved it.
   Store approved descriptors in the profile.
3. **Claim strength is preserved.** Track three levels: *daily*, *applied*,
   *exposure*. Exposure never becomes proficiency. A tool used for one narrow
   purpose is written with that purpose ("prepared geometry in NX for
   meshing"), not as general proficiency.
4. **No invented numbers.** Metrics come from the user. No rounding up.
5. **Credentials exact.** Degrees, GPA, licenses, citizenship, clearance.
   "Able to obtain a clearance" is not a clearance and never appears as one.
6. **Personal credit only.** On team projects, claim what the user did.
   Publications carry their true tier: paper, poster, report, abstract.
7. **No keyword stuffing.** A posting keyword with no evidence stays off the
   resume. No hidden text, no white text, no keyword dumps.
8. **Gaps are reported, not hidden.** The delivery message lists every posting
   requirement the resume does not meet.
9. **Mirror vocabulary only when it is the same thing.** Calling a "valve
   testing cart" a "valve test station" because the posting says "test station"
   is good tailoring. Calling it a "structural test article" is fabrication.
10. **If the user asks you to add something they do not have, decline**, say
    why in one sentence, and offer the nearest true statement instead.

A skill listed in the Skills section with no supporting bullet and no
confirmed profile line counts as a fabrication. The original user restored a
removed skill only after supplying the concrete projects behind it. That is
the standard.

## 4. Repo map

```
CLAUDE.md                          this brief
DECISIONS.md                       you create; one line per judgment call
README.md                          you write; install + first use, for a non-developer
.gitignore                         exists
skill/
  SKILL.md                         you write (section 12)
  assets/
    resume.cls                     exists, tested
    resume_template.tex            exists, tested
    coverletter.cls                exists, tested
    coverletter_template.tex       exists, tested
    fonts/                         you add: one OFL script font + its license
  references/
    style_resume.md                you write, from section 8
    style_coverletter.md           you write, from section 9
    career_profile_template.md     you write, from section 7
    examples/                      exists; fictional; read keyword_map.md first
      job_posting.txt
      keyword_map.md
      Doe_Calderwick_TestEquipment_CAS-10482.tex / .pdf
      Doe_Calderwick_TestEquipment_CAS-10482_CoverLetter.tex / .pdf
      signature.png                stand-in; regenerate with your script
  scripts/
    build.py                       you write (section 11)
    ats_check.py                   you write (section 11)
    make_signature.py              you write (section 11)
evals/
  evals.json                       you write (section 13)
  fixtures/                        you write; fictional only
```

The examples were written by someone with access to the private source
material this skill was distilled from. They are the ground truth for look,
voice, and analysis depth. Do not restyle them. If a class change alters their
rendered output, that is a regression.

The example resume is condensed on purpose so it reads quickly as a sample:
short skills lines, seven bullets on the lead role, a light second page. Copy
its format, voice, and tracing, not its length. Real output follows the length
rules in section 8, and the source resumes ran seven to ten bullets on the
most relevant role with a second page about two thirds full.

## 5. Runtime workflow

A session with a complete profile is "paste posting, get resume" with zero
questions. Do not make the user approve a keyword list before drafting. The
analysis is delivered with the resume, not ahead of it.

**Step 0. Find the user's material.** Look for `career_profile.md`, old
resumes (`.tex`, `.pdf`, `.docx`), earlier tailored resumes, publication
notes. If there is no profile, build one from whatever exists (section 7). If
there is nothing at all, ask for an old resume first because it is the fastest
route, and fall back to interview questions.

**Step 1. Read the posting.** Extract company, title, requisition ID,
location, basic qualifications, preferred qualifications, responsibilities,
and gates (citizenship, clearance, degree, years, travel, relocation). Decide
the *center of gravity*: what the job mostly is (design, analysis, test,
integration). The same person's resume for an analyst role and a designer role
should lead with different work. If the posting can be filled at more than one
level, target the highest level whose basic qualifications the user meets, and
say which.

**Step 2. Build the keyword list.** Group by tools, methods and standards,
deliverables, collaboration, domain, gates. Weight title words and basic
qualifications highest, then responsibilities, then preferred. Repeated terms
outrank single mentions. Keep the posting's exact wording, including both the
spelled-out form and the acronym.

**Step 3. Map evidence.** For each keyword assign *Strong*, *Have*,
*Adjacent*, *Gap* (user confirmed they lack it), or *Unknown* (profile is
silent).

**Step 4. Q&A gate.** See section 6. Skip it when nothing triggers.

**Step 5. Draft.** Start from the closest earlier tailored resume if one
exists, otherwise from the profile and `assets/resume_template.tex`. Apply
section 8.

**Step 6. Build and verify.** Compile, fit to pages, run `ats_check.py`, fix,
repeat (section 10).

**Step 7. Deliver.** PDF, `.tex`, and the keyword map. The message to the user
is short: level targeted, coverage count, the list of gaps, anything to
confirm before sending. If any gap is worth bridging in prose, offer a cover
letter. No praise of the user's background and no restating the resume.

**Step 8. Persist.** Write new facts and confirmed gaps to the profile. On
Claude.ai, hand the updated profile to the user and tell them to keep it with
their materials, since nothing else survives the chat.

**Cover letter** (on request or accepted offer): needs the finished resume and
keyword map. Make `signature.png` if none exists. Apply section 9. One page.

Per-application files, when a working directory exists:

```
applications/<Company>_<ReqID>/
  posting.txt
  keyword_map.md
  <Last>_<Company>_<RoleShort>_<ReqID>.tex / .pdf
  <Last>_<Company>_<RoleShort>_<ReqID>_CoverLetter.tex / .pdf
```

## 6. The Q&A gate

Triggers, any one of:

- No usable source material, or basics are missing (employers, titles, dates,
  degrees).
- A basic qualification is *Unknown* or supported only by *Adjacent* evidence.
- A title keyword or a keyword repeated in the posting is *Unknown*.
- A claim's strength is unclear: a tool in an old skills list with no bullet
  behind it, or a vague verb ("supported", "involved in") on something the
  posting cares about.

Rules:

1. Ask before drafting, in one batch, at most five questions, basic
   qualifications first. Skip preferred items that are plainly outside the
   user's field.
2. Quote the posting line each question comes from. Ask for evidence, not a
   yes or no: where, what they personally did, which tools, any measured
   result.
3. Engineers undersell. When the answer reveals something stronger than the
   old resume shows, use it. When the answer is "no", record a confirmed gap
   and never ask about it again.
4. An answer sets the claim level. "Only for geometry cleanup" is exposure
   and is written that way.
5. If the user says "just write it", write it with the open items treated as
   gaps and listed in the delivery message.
6. A second round is allowed only if an answer opened a new basic-qualification
   question.

`references/examples/keyword_map.md` section 2 is a worked example.

## 7. Career profile (the evidence bank)

One Markdown file per user, `career_profile.md`. It is the single source the
skill writes from, and the reason the user is never asked the same thing
twice. The practice it replaces was an annotated notes file where every
project carried two lines: what the user personally did, and how it may be
used on a resume. Keep both ideas.

Required sections:

```
# Career profile: <Name>
## Contact          name, email, phone, city/state, mailing address (cover letter only)
## Status           citizenship, clearance (exact wording), relocation, travel
## Preferences      e.g. show city on resume: yes/no; show citizenship on resume: yes/no;
                    years-of-experience count: never
## Roles            newest first. For each:
                    official title (verbatim), approved descriptors, employer, context, city, dates
                    bullet bank: every true bullet ever used, each tagged
                      [level: daily|applied|exposure] [tags: ...] [metric source: ...]
## Tools and skills table: item | level | evidence (role/bullet) | notes on scope
## Education        degree, field, school, date, GPA, honors, thesis
## Publications     title | venue | year | tier (paper/poster/report/abstract)
                    | personal role | resume status (use / use with tag / do not use)
## Projects         title | context | what the user did | awards
## Confirmed gaps   things the user has said they do not have
## Q&A log          date | posting | question | answer
```

Build it by reading every resume the user provides and merging: union of
bullets, conflicts flagged for the user rather than silently resolved. Never
store government ID numbers or anything the resume itself would not show.

## 8. Resume style

Layout is fixed by `resume.cls`. Read the class and the example before
writing. These are the content and judgment rules.

**Length.** Two pages for experienced candidates. The guidance this is built
on: large contractors screen with ATS first, so keyword coverage beats
brevity, and a second page is worth it when it carries real keywords. Never
three pages. One page only when the user's real content does not fill a page
and a half. Never pad.

**Order.** Summary, Technical Skills, Professional Experience, Education, then
Publications and Projects in whichever order suits the posting. Experience is
always reverse chronological. Ordering jobs by relevance was tried once and
reverted because parsers and recruiters both expect dates to descend. Shift
emphasis with bullet count and bullet order instead: the most relevant role
gets the most bullets, even when it is not the newest.

**Header.** Name centered, not bold. One contact line: optional city, email,
phone. No street address. Citizenship is off by default and is added only when
the profile preference says to show it, which is worth offering to a user
applying to clearance roles. An active clearance goes here only if the user
actually holds one.

**Summary.** Three sentences, no first person. Sentence one is an identity
noun phrase that mirrors the posting's discipline. Sentence two is what the
user delivers, in the posting's vocabulary. Sentence three is the
differentiator. No years-of-experience count: it goes stale, it was once
submitted out of date, and it undercounts people with graduate degrees. Let
the reader work it out from the dates.

**Technical Skills.** Five to seven lines, bold category label then a comma
list. Name a tool once at the level a recruiter searches for ("PTC Creo"), and
list its modules only when the posting names them. Rename and reorder categories for every posting so the first line is the
posting's center of gravity. Give each important term once spelled out with
its acronym: "Bill of Materials (BOM)". Order items inside a line by the
user's real strength, not the posting's preference: the daily tool goes first
even when the posting prefers another. Standards may be listed here when the
user has genuinely worked to them. Cite a standard inside an experience bullet
only when the user is comfortable being questioned on it.

**Bullets.**

- Action verb first. Present tense for ongoing duties in the current role,
  past tense for finished projects and earlier roles.
- One to three lines. Shape: what, how (tools, standards), result. A semicolon
  may join two related clauses.
- Use the posting's exact noun phrases where rule 3.9 allows.
- Most posting-relevant bullets first within each role.
- Metrics only from the profile.
- No em dashes and no parenthetical asides. En dashes appear only in date
  ranges, title descriptors, and the employer and location line.
- When a publication title does not show what the user did, put the
  contribution in an experience bullet too. A poster titled after the science
  will not tell a recruiter that the user designed the test hardware behind
  it.

**Education.** Degree and GPA bold with the date at right, school in italics,
then one line for thesis title or honors. GPA only at 3.5 or above.

**Publications.** Title the section "Publications" only if every entry is a
paper. Otherwise "Publications & Presentations", with each non-paper tagged:
"(Poster)". Drop abstract-only items and anything the profile marks "do not
use".

**Projects.** One format for the whole section: every project followed by a
plain line, or every project followed by bullets. Never mixed. For senior
candidates keep school projects to a line, or a title alone. Keep a project
when it carries an award the target employer would recognize or is the only
honest evidence for a basic qualification (a personal electronics project
backing a "hands-on with oscilloscopes" requirement).

**Page fit.** Use the class knobs in the order given in
`resume_template.tex`, then cut the weakest bullet from the oldest role. Never
change font size or margins. Place `\pagebreak` between roles so no role is
split when that can be avoided, and never leave a role header or section heading as the
last thing on a page. Page two should be at least half full. If it is not,
either relevant bullets are still sitting unused in the profile or the resume
belongs on one page.

**File names.** `<Last>_<Company>_<RoleShort>_<ReqID>.tex`.

## 9. Cover letter style

Layout is fixed by `coverletter.cls`: name in bold caps at top left, bold date
at top right on the same line, contact lines in letter-spaced italics,
recipient block, salutation, body, sign-off with signature image.

The original user's standing complaints about drafts, which are now rules:

1. **Do not sound like an AI.** No em dashes. No colons or semicolons inside
   body sentences. The salutation "Dear Hiring Manager:" keeps its colon.
   Slightly plain is better than polished.
2. **Do not flatter the company.** No echo of their mission statement, no
   "groundbreaking", no "I am thrilled". The first rejected draft "sounded
   like sucking up".
3. **Hard facts live in the resume.** The letter is light and personable. Pick
   one project and tell it as a short story. Do not re-list the skills
   section.
4. **Concise.** Four body paragraphs plus a two-sentence thank-you. One page
   with room to spare.
5. **Name the gap, then bridge it.** This is the main job of the letter. If
   the posting wants a tool or a domain the user lacks, say so plainly and
   give the honest reason the transfer is short.
6. **Insider candor is welcome** when it is true and specific. An engineer
   calling a notorious certification process "byzantine" builds rapport with a
   reader who has lived it.
7. **Nothing new.** Every fact is already in the resume or the profile.
8. First person, contractions avoided, sentences of ordinary length. A human
   sentence about pride in the work or being easy to work with is in voice.

Paragraph plan is in `coverletter_template.tex`. Standard close: "Thank you
for your consideration. Please do not hesitate to contact me if you have any
questions." Then "Sincerely," and the signature.

Logistics the posting asks about (citizenship, clearance eligibility, travel,
relocation, site access already held) go in the last body paragraph as plain
statements.

## 10. ATS rules and the verification pass

Why each rule exists: a parser reads the PDF's text layer top to bottom. Any
text it cannot extract, or extracts out of order, is experience the user does
not get credit for.

- pdfLaTeX only. The classes load `glyphtounicode` so ligatures and dashes map
  to plain Unicode. Verified with `pdftotext`.
- Single column. No tables, text boxes, images, icons, headers, or footers.
- Standard section names exactly as in the template.
- Dates as "Month YYYY – Month YYYY" (typed `--` in the source), right-aligned
  on the title line.
- Contact details as plain text in the first two lines.
- Hyphenation is off so keywords are never split across lines.
- The header separator is `\sep`, a real vertical bar. Background: the source
  resumes typed `|`, which the old OT1 font encoding silently printed as an em
  dash. The class now uses T1 and makes the character explicit. Change the one
  `\sep` definition if a user prefers a dash or bullet.
- PDF title and author metadata are set by the class.

Verification pass after every build:

1. Page count is as intended.
2. `pdftotext -layout` output reads in visual order and contains no ligature,
   private-use, or replacement characters.
3. Email and phone appear in the first two extracted lines.
4. Every keyword marked Strong, Have, or Adjacent appears verbatim at least
   once. Every keyword marked Gap appears zero times.
5. Every Skills item has a bullet or a confirmed profile line behind it.
6. Titles, employers, and dates are character-identical to the profile.
7. No `<placeholder>` text remains.
8. Cover letter only: one page, no em dash, no colon or semicolon in the body.

## 11. Scripts to write

Python 3.10+, standard library plus Pillow (and `pypdf` as an optional
fallback). No network access at runtime.
Each script prints a short human-readable result and exits non-zero on
failure.

**`build.py <file.tex> [--out DIR]`**
Finds `resume.cls` / `coverletter.cls` in `../assets` and exposes them via
`TEXINPUTS` or by copying beside the source. Runs `pdflatex
-interaction=nonstopmode -halt-on-error` twice. Reports page count and any
overfull boxes. Cleans aux files. If `pdflatex` is missing, tries `tectonic`,
and otherwise exits with a message telling the user to upload the `.tex` and
the `.cls` to Overleaf. Never installs TeX.

**`ats_check.py <resume.pdf> [--keywords keyword_map.md] [--profile career_profile.md] [--pages 2]`**
Implements verification steps 1 to 7 above. Extracts text with `pdftotext`
(poppler) when available, then `pypdf` if importable. If neither exists it
says extraction could not be verified and exits non-zero. Output is a
checklist with pass or fail per line and the offending text for each failure.

**`make_signature.py --name "First Last" [--out signature.png] [--font PATH] [--ink "#14183a"] [--height 300]`**
Renders the name in a script font to a transparent PNG.

- Bundle exactly one OFL-licensed script font in `skill/assets/fonts/` with
  its license file. The stand-in example used Great Vibes. Allura and Alex
  Brush were the alternatives considered. Do not depend on system fonts.
- Transparent background, dark blue-black ink, tight crop with a small
  margin, at least 300 px tall so it stays sharp at the 1.2 cm print height
  the class uses.
- Check that the font has a glyph for every character in the name. If not,
  stop with a clear message rather than drawing boxes.
- Never overwrite an existing `signature.png` without `--force`. A user may
  have put a scan of their real signature there, and that always wins.
- Deterministic output for the same inputs.

The class looks for `signature.png` beside the `.tex` file and falls back to
the typed name when it is absent, so a letter is never unsigned.

## 12. SKILL.md authoring notes

- Frontmatter: `name: resume-tailor` and a `description` that says what it
  does and when to use it. Skills under-trigger, so name the cues: a pasted
  job posting or job description, "tailor my resume", "ATS", "apply to this
  job", "cover letter for this role", even when the user does not say
  "resume".
- Body order: hard rules, workflow, Q&A gate, delivery format, then pointers.
  Keep it under 500 lines by moving sections 8 and 9 into `references/` and
  telling the model when to read each file.
- Explain reasons instead of shouting. The model follows a rule better when it
  knows what breaks without it.
- Tell the model to read `references/examples/keyword_map.md` and the example
  `.tex` files before its first draft in a session.
- Imperative voice. Paths relative to the skill folder.
- The skill's messages to the user are short and plain. No flattery, no
  recap of what the user can already see in the PDF.

## 13. Evals

Write `evals/evals.json` in the skill-creator schema, with fictional fixtures
only. Derive the John Doe profile fixture from the example resume and the Q&A
answers in the example keyword map, then extend it with more fictional bullets
per role. The example resume is condensed, and a profile is meant to hold more
than any one resume uses, so the fixture needs enough material to fill two
pages.

| # | Prompt shape | Must happen |
|---|---|---|
| 1 | Complete profile + the example posting | Resume delivered with no questions. Two pages. `ats_check` passes. Gaps listed: NX depth, Teamcenter, LabVIEW, clearance. |
| 2 | Same profile + a new posting with a different center of gravity (structural analyst) | Summary, skills order, and bullet emphasis change. Job order and titles do not. Nothing appears that is absent from the profile. |
| 3 | Profile with the test-equipment and ATP facts removed + the example posting | Skill asks before drafting, quoting the posting lines. Given "no" answers, those keywords do not appear and are reported as gaps. |
| 4 | No profile, one old resume attached + a posting | Skill builds a profile, asks at most five questions, returns the profile along with the resume. |
| 5 | After eval 1: "Add Teamcenter to my skills, everyone lists it" then "write the cover letter" | Declines in one sentence and offers "Windchill PLM". Letter is one page, has a signature image, contains no em dash, and names the NX and clearance gaps. |

Checks that can be scripted (page count, forbidden strings, title equality,
keyword presence) should be scripted.

## 14. Build order

1. Read `skill/references/examples/keyword_map.md`, both example `.tex` files,
   and both `.cls` files.
2. Write `build.py`. Rebuild both examples. Confirm 2 pages and 1 page.
3. Write `ats_check.py`. Confirm the example resume passes.
4. Add the font and license. Write `make_signature.py`. Regenerate
   `examples/signature.png`. Rebuild the example letter.
5. Write `references/career_profile_template.md`, `style_resume.md`,
   `style_coverletter.md`.
6. Write `SKILL.md`.
7. Write fixtures and `evals/evals.json`. Run the evals. Fix the skill, not
   the evals.
8. Write `README.md` for a non-developer: install on Claude.ai, install in
   Claude Code, first run, where files go, how to recompile on Overleaf.
9. Package `resume-tailor.skill`.

## 15. Conventions

- Fictional data only, everywhere. `.gitignore` already excludes the folders
  where a user's real material would sit during local testing. Check `git
  status` before every commit.
- Do not change the visual output of the classes. New options are fine.
  Rebuild the examples after any class edit and compare page counts and
  extracted text.
- Small commits, imperative subject lines.
- Record judgment calls in `DECISIONS.md` as you make them.
