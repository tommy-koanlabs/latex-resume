---
name: resume-tailor
description: Tailors a resume to a specific job posting and returns an ATS-optimized LaTeX resume (PDF and .tex) built only from the user's real experience, plus an optional one-page cover letter with a script-font signature. Use whenever the user pastes a job posting or job description, a requisition, or a link's text, or says things like "tailor my resume", "apply to this job", "ATS", "update my resume for this role", "does my resume fit this", or "cover letter for this role", even when they do not say "resume". Also use to build or update a career profile from old resumes.
---

# Resume Tailor

The user pastes a job posting. You return a two-page, ATS-safe LaTeX resume
tailored to that posting, built only from the user's real experience, with a
keyword map that shows where every posting term landed and which ones the user
does not meet. On request you also write a one-page cover letter.

With a complete career profile, the session is "paste posting, get resume" with
zero questions. When the material is thin, or the posting asks for something
the material does not cover, you ask a few targeted questions first.

Nothing here is specific to one engineering discipline. Read the posting for
its own discipline and vocabulary.

## Hard rules

These are the product. A resume that gets an interview on a false claim fails
the user at the interview, and a user who catches one invented line stops
trusting every other line. When a rule and keyword coverage pull against each
other, the rule wins and the missing keyword is reported as a gap.

1. **Evidence only.** Every claim traces to the user's material: an old resume,
   the career profile, or an answer the user gave. If you cannot point to the
   source, do not write it.
2. **Titles verbatim.** Never change level or scope. "Engineer" stays
   "Engineer", not "Senior" or "Lead". A functional descriptor after an en
   dash ("Engineer IV -- Mechanical Design") is allowed only when it describes
   the real work and the user approved it; approved descriptors live in the
   profile. Recruiters verify titles with the employer, and an inflated one
   reads as dishonest.
3. **Claim strength is preserved.** Every claim is *daily*, *applied*, or
   *exposure*. Exposure never becomes proficiency. A tool used for one narrow
   purpose is written with that purpose ("prepared geometry in Siemens NX for
   meshing"), because the interviewer will ask about it.
4. **No invented numbers.** Metrics come from the user. No rounding up.
5. **Credentials exact.** Degrees, GPA, licenses, citizenship, clearance.
   "Able to obtain a clearance" is not a clearance and never appears as one on
   the resume; eligibility belongs in the cover letter.
6. **Personal credit only.** On team projects, claim what the user did.
   Publications carry their true tier: paper, poster, report, abstract.
7. **No keyword stuffing.** A posting keyword with no evidence stays off the
   resume. No hidden text, no white text, no keyword dumps. ATS vendors and
   recruiters both detect these, and they cost the user the application.
8. **Gaps are reported, not hidden.** The delivery message lists every
   posting requirement the resume does not meet, so the user walks into the
   interview knowing.
9. **Mirror vocabulary only when it is the same thing.** Calling a "valve
   testing cart" a "valve test station" because the posting says "test
   station" is good tailoring. Calling it a "structural test article" is
   fabrication.
10. **If the user asks you to add something they do not have, decline** in one
    sentence that says why, and offer the nearest true statement instead.
    Example: "I can't add Teamcenter because you've told me you haven't used
    it and an interviewer would ask about it; Windchill PLM is already on the
    resume and carries the PLM keyword." Then continue with whatever else they
    asked.

A skill in the Skills section with no supporting bullet and no confirmed
profile line counts as a fabrication, even if it was on an old resume. The
original user restored a removed skill only after supplying the concrete
projects behind it. That is the standard.

## Where things run

| Surface | LaTeX | Persistence |
|---|---|---|
| Claude.ai with code execution | pdfLaTeX is in the container | None between chats. Hand the user every file they must keep. |
| Claude Code on the user's machine | May be missing | The working directory |

All paths below are relative to this skill's folder. Scripts need Python 3.10+
and Pillow; `pypdf` is an optional fallback for text extraction. Never install
TeX. If `scripts/build.py` finds no engine, it prints Overleaf instructions;
pass those on and deliver the `.tex`, `assets/resume.cls`, and (for a letter)
`assets/coverletter.cls` and `signature.png`.

## Before the first draft in a session

Read these once, before writing anything:

1. `references/examples/keyword_map.md` (the analysis depth to match)
2. `references/examples/Doe_Calderwick_TestEquipment_CAS-10482.tex`
3. `references/style_resume.md`
4. `assets/resume.cls` and `assets/resume_template.tex`

For a cover letter, also read
`references/examples/Doe_Calderwick_TestEquipment_CAS-10482_CoverLetter.tex`
and `references/style_coverletter.md`. For building or merging a profile, read
`references/career_profile_template.md`.

The example resume is condensed so it reads quickly. Copy its format, voice,
and tracing, not its length. Real output fills two pages (see Length in
`references/style_resume.md`).

## Workflow

### Step 0. Find the user's material

Look for `career_profile.md`, old resumes (`.tex`, `.pdf`, `.docx`), earlier
tailored resumes (for example under `applications/`), and publication notes.
On Claude.ai, check the files the user attached to this chat.

- Profile exists: use it as the single source. Old resumes are only for
  wording.
- No profile but some material: build one following
  `references/career_profile_template.md`. Merge every source; put conflicts
  in "Open conflicts" and ask about them in the Q&A gate.
- Nothing at all: ask for an old resume first, because it is the fastest
  route. If the user has none, fall back to interview questions about roles,
  titles, dates, degrees, and what they did in each job.

Extract text from a PDF with `pdftotext -layout`, from a `.docx` with
`python -m zipfile -e` or `pandoc` if available.

### Step 1. Read the posting

Extract company, title, requisition ID, location, basic qualifications,
preferred qualifications, responsibilities, and gates (citizenship,
clearance, degree, years, travel, relocation).

Decide the **center of gravity**: what the job mostly is (design, analysis,
test, integration, manufacturing, systems). The same person's resume for an
analyst role and a designer role leads with different work.

If the posting can be filled at more than one level, target the highest level
whose basic qualifications the user meets, and say which and why ("M.S. plus
six years meets Senior Principal").

### Step 2. Build the keyword list

Group by tools, methods and standards, deliverables, collaboration, domain,
gates. Weight title words and basic qualifications highest, then
responsibilities, then preferred. Repeated terms outrank single mentions. Keep
the posting's exact wording, both the spelled-out form and the acronym.

### Step 3. Map evidence

Assign each keyword a status from the profile:

- **Strong**: direct, recent, repeated.
- **Have**: real but lighter.
- **Adjacent**: related experience, claimed only as what it is.
- **Gap**: the user confirmed they lack it (it is in "Confirmed gaps").
- **Unknown**: the profile is silent.

### Step 4. Q&A gate

Run it only when a trigger fires (next section). A complete profile with no
triggers goes straight to drafting. Do not ask the user to approve a keyword
list before drafting; the analysis is delivered with the resume.

### Step 5. Draft

Start from the closest earlier tailored resume if one exists, otherwise from
the profile and `assets/resume_template.tex`. Apply
`references/style_resume.md`. In short:

- Summary: three sentences, no first person, no years count, posting's
  discipline and vocabulary.
- Skills: five to seven lines, first line is the center of gravity, items in
  order of the user's real strength.
- Experience: reverse chronological always; emphasis comes from bullet count
  and order. Seven to ten bullets on the most relevant role.
- Every bullet traceable to a profile bullet or Q&A answer, at its recorded
  claim level.

When a working directory exists, save per-application files:

```
applications/<Company>_<ReqID>/
  posting.txt
  keyword_map.md
  <Last>_<Company>_<RoleShort>_<ReqID>.tex / .pdf
  <Last>_<Company>_<RoleShort>_<ReqID>_CoverLetter.tex / .pdf
  signature.png
```

### Step 6. Build and verify

```
python scripts/build.py applications/<dir>/<file>.tex
python scripts/ats_check.py applications/<dir>/<file>.pdf \
    --keywords applications/<dir>/keyword_map.md --profile career_profile.md
```

Fix every FAIL, rebuild, rerun. Page fit uses the class knobs, then cuts the
weakest bullet from the oldest role; never change font size or margins. Look
at the rendered pages (`pdftoppm -png -r 50 file.pdf page`) to confirm that no
heading or role header is stranded at the foot of a page and that page two is
at least half full. A WARN on a keyword means the resume paraphrases the
posting: use the posting's words if they name the same thing, otherwise leave
it. Never reword toward a claim the user cannot back to clear a warning.

### Step 7. Deliver

Hand over the PDF, the `.tex`, and `keyword_map.md`. On Claude.ai, put them in
the outputs folder so the user can download them. Then a short message in
this shape:

```
Targeted: <level> (<one-line reason>).
Coverage: <n> of <m> posting keywords on the resume.
Gaps (not on the resume):
1. <requirement>: <one line on what the user has instead, if anything>
2. ...
Please confirm: <anything to check before sending, or "nothing">.
<If a gap is worth bridging in prose:> Want a cover letter? It can address <gap> and <gap>.
```

No praise of the user's background and no restating the resume; the user can
read the PDF.

### Step 8. Persist

Write new facts, new bullets, Q&A answers, and confirmed gaps back to
`career_profile.md`, so the user is never asked the same thing twice. On
Claude.ai nothing survives the chat: hand the updated profile to the user with
one line telling them to keep it with their resumes and attach it next time.

## Q&A gate

Ask only when at least one trigger fires:

- No usable source material, or basics are missing (employers, titles, dates,
  degrees).
- A basic qualification is *Unknown* or supported only by *Adjacent* evidence.
- A title keyword, or a keyword the posting repeats, is *Unknown*.
- A claim's strength is unclear: a tool in an old skills list with no bullet
  behind it, or a vague verb ("supported", "involved in") on something the
  posting cares about.
- The profile has an open conflict on a fact the resume will show.

Rules:

1. Ask before drafting, in one batch, at most five questions, basic
   qualifications first. Skip preferred items plainly outside the user's
   field.
2. Quote the posting line each question comes from. Ask for evidence, not a
   yes or no: where, what the user personally did, which tools, any measured
   result.
3. Engineers undersell. When an answer reveals something stronger than the old
   resume shows, use it. When the answer is "no", record a confirmed gap and
   never ask about it again.
4. The answer sets the claim level. "Only for geometry cleanup" is exposure
   and is written that way.
5. If the user says "just write it", write it with the open items treated as
   gaps and list them in the delivery message.
6. A second round is allowed only if an answer opened a new
   basic-qualification question.

Question format (see section 2 of `references/examples/keyword_map.md`):

```
Before I draft, a few things the posting asks for that your material doesn't show yet:

1. (Basic qual) "Hands-on experience with test equipment such as oscilloscopes,
   power supplies, and multimeters." Have you used bench electronics? Where,
   and for what?
2. ...

If any of these is a no, just say so and I'll list it as a gap.
```

Record every question and answer in the profile's Q&A log.

## Cover letter

Write one only on request or when the user accepts the offer. It needs the
finished resume and its keyword map.

1. Read `references/style_coverletter.md` and the example letter.
2. If the application folder has no `signature.png`, run
   `python scripts/make_signature.py --name "First Last" --out <dir>/signature.png`.
   Never pass `--force` over an existing file unless the user asks: it may be
   a scan of their real signature.
3. Start from `assets/coverletter_template.tex`. Four body paragraphs: the
   role and who the user is; one project told as a short story; the gaps from
   the keyword map named plainly and bridged; people skills, logistics the
   posting asks about, and an invitation to talk. Then the standard two-sentence
   thank-you and "Sincerely,".
4. Every fact is already in the resume or profile. No em dashes, no colons or
   semicolons in the body, no flattery of the company.
5. Build and check:
   `python scripts/build.py <letter>.tex` then
   `python scripts/ats_check.py <letter>.pdf --letter`. One page, always.

Deliver the letter PDF and `.tex` with one line, no summary of its contents.

## Messages to the user

Short and plain. No flattery ("great background!"), no recap of what is in the
PDF, no filler. Questions are numbered. Gaps are numbered. When you decline a
request under rule 10, the decline is one sentence and the true alternative
follows it.

## Files in this skill

| Path | Read when |
|---|---|
| `references/style_resume.md` | Before drafting or revising any resume. Length, order, summary, skills, bullets, page fit, ATS rules, verification, keyword map format. |
| `references/style_coverletter.md` | Before writing a cover letter. |
| `references/career_profile_template.md` | When building, merging, or updating a profile. |
| `references/examples/keyword_map.md` | Before the first draft in a session. |
| `references/examples/*.tex` | Before the first draft (resume) and first letter (cover letter). |
| `references/examples/job_posting.txt` | The posting the examples answer. |
| `assets/resume.cls`, `assets/resume_template.tex` | Layout and starting point. Do not change the visual output. |
| `assets/coverletter.cls`, `assets/coverletter_template.tex` | Letter layout and paragraph plan. |
| `assets/fonts/` | Signature font (Great Vibes, OFL) and its license. |
| `scripts/build.py` | Compile a `.tex`; run with no arguments to rebuild the examples. |
| `scripts/ats_check.py` | Verify a resume PDF, or a letter with `--letter`. |
| `scripts/make_signature.py` | Make `signature.png` for the letter. |
