# Career profile template

The career profile is the evidence bank. Every line on a resume or cover letter
must trace to it, and it is the reason the user is never asked the same
question twice. One file per user, named `career_profile.md`.

Read this file when building a profile for the first time, when merging a new
resume into an existing profile, and when writing answers back after a Q&A
gate.

## How to build it

1. Read every source the user provides: old resumes (`.tex`, `.pdf`, `.docx`),
   earlier tailored resumes, publication notes, answers in the chat.
2. Merge, never pick. The bullet bank is the union of every true bullet ever
   used. Two resumes that disagree on a date, a title, or a metric are a
   conflict: write both into **Open conflicts** and ask the user. Do not
   silently choose one.
3. Tag every bullet with a claim level. When the source does not make the
   level clear, mark it `[level: ?]` and treat it as a Q&A trigger the first
   time a posting cares about it.
4. Record where each metric came from. A metric with no source is not used.
5. Every item in an old skills list becomes a row in **Tools and skills**.
   An item with no bullet behind it gets level `?` until the user explains it.
   A skill on an old resume is not evidence by itself.
6. Never store government ID numbers, dates of birth, salary history, or
   anything the resume itself would not show.

## Format rules the scripts depend on

`scripts/ats_check.py --profile` reads this file. Keep these shapes:

- Each role is a `### <Official title, verbatim>` heading under `## Roles`,
  followed by `- Employer:`, `- Context:`, `- City:`, `- Dates:` and
  `- Approved descriptors:` lines. Dates use the resume form,
  `Month YYYY -- Month YYYY` or `Month YYYY -- Present`. Multiple approved
  descriptors are separated by `;`. Write `none` when there are none.
- The resume's employer line is `Employer (Context) -- City`, or
  `Employer -- City` when Context is empty. The check requires the line to
  start with Employer and end with City, character for character.
- **Tools and skills** is a table whose first column header contains `Item`
  and which has a `Level` column.
- Each confirmed gap is a bullet that starts with the gap in bold:
  `- **Teamcenter** ...`.

Claim levels:

| Level | Means | Written as |
|---|---|---|
| `daily` | Core, current, repeated use. | Plain claim, first in its Skills line. |
| `applied` | Real use on real work, not daily. | Plain claim, after the daily items. |
| `exposure` | Narrow or brief use. | Only with its purpose: "prepared geometry in NX for meshing". Never as general proficiency. Listed in Skills only when a bullet states the narrow use. |
| `gap` | User confirmed they do not have it. | Never written. Lives in Confirmed gaps. |

---

Copy everything below this line to start a new profile.

```markdown
# Career profile: <First Last>

Last updated: <YYYY-MM-DD>

## Contact
- Name: <First Last>
- Email: <email>
- Phone: <(000) 000-0000>
- City/State: <City, ST>
- Mailing address (cover letter only): <Street, City, ST ZIP>

## Status
- Citizenship: <exact, e.g. U.S. citizen>
- Clearance: <exact wording, e.g. "None" or "Active Secret (DoD), granted Month YYYY">
- Relocation: <yes / no / conditions>
- Travel: <limits, if any>
- Site access already held: <e.g. badge at a named government site, or none>

## Preferences
- Show city on resume: <yes/no>
- Show citizenship on resume: <yes/no>
- Years-of-experience count: never
- Cover letter signature: <generated script font / own scan in signature.png>
- Other: <anything the user has asked for, e.g. "never use the word passionate">

## Roles

### <Official title, verbatim>
- Employer: <Employer name exactly as on the resume>
- Context: <e.g. Government Test Center Contract, or empty>
- City: <City, ST>
- Dates: <Month YYYY> -- <Month YYYY or Present>
- Approved descriptors: <none, or a functional descriptor the user approved, e.g. Structural Design & Analysis>
- Notes: <scope, team size, what the job mostly was>

Bullet bank:
- [level: daily] [tags: <tag>, <tag>] [metric source: none] <Bullet text, present tense if ongoing.>
- [level: applied] [tags: <tag>] [metric source: user, <date>] <Bullet with a metric the user supplied.>
  - Personal role: <what the user did, if the bullet describes team work>

## Tools and skills

| Item | Level | Evidence | Scope notes |
|---|---|---|---|
| <PTC Creo> | daily | <Role 1 bullets 1-3> | <modules used, if any> |
| <Siemens NX> | exposure | <Role 2 bullet 2> | <only geometry cleanup for FEA> |

## Education
- <M.S. Field> | <University> | <Month YYYY> | GPA <0.00> | <honors> | Thesis: <title>

## Publications

| Title | Venue | Year | Tier | Personal role | Resume status |
|---|---|---|---|---|---|
| <title> | <venue> | <YYYY> | <paper / poster / report / abstract> | <what the user did> | <use / use with tag / do not use> |

## Projects

| Title | Context | What the user did | Awards |
|---|---|---|---|
| <title> | <personal / capstone / course> | <user's own part> | <award or none> |

## Confirmed gaps
- **<Tool or credential>** (<YYYY-MM-DD>, <posting>): <what the user said, and the nearest true statement if any>

## Open conflicts
- <Source A says X; source B says Y. Ask the user.>

## Q&A log

| Date | Posting | Question | Answer |
|---|---|---|---|
| <YYYY-MM-DD> | <Company ReqID> | <question, with the posting line quoted> | <answer, close to the user's words> |
```
