# Cover letter style

Read this before writing any cover letter. Layout is fixed by
`assets/coverletter.cls`: name in bold caps top left, bold date top right on
the same line, contact lines in letter-spaced italics, recipient block,
salutation, body, sign-off with signature image. Read
`references/examples/Doe_Calderwick_TestEquipment_CAS-10482_CoverLetter.tex`
before the first letter in a session. It is the ground truth for voice.

A letter needs the finished resume and its keyword map. Write it after the
resume, never before.

## Voice rules

These come from the original user's standing complaints about drafts.

1. **Do not sound like an AI.** No em dashes. No colons or semicolons inside
   body sentences. "Dear Hiring Manager:" keeps its colon. Slightly plain is
   better than polished. Avoid stock phrases such as "I am thrilled", "align
   perfectly", "proven track record", "leverage", "passionate".
2. **Do not flatter the company.** No echo of the mission statement, no
   "groundbreaking", no "industry-leading". The first rejected draft "sounded
   like sucking up".
3. **Hard facts live in the resume.** The letter is light and personable.
   Pick one project and tell it as a short story. Do not re-list the skills
   section.
4. **Concise.** Four body paragraphs plus the two-sentence thank-you. One page
   with room to spare.
5. **Name the gap, then bridge it.** This is the main job of the letter. If
   the posting wants a tool or a domain the user lacks, say so plainly and
   give the honest reason the transfer is short. Use the gaps list from the
   keyword map.
6. **Insider candor is welcome** when it is true and specific. An engineer
   calling a notorious certification process "byzantine" builds rapport with
   a reader who has lived it.
7. **Nothing new.** Every fact is already in the resume or the profile. A
   letter is not a place to introduce a claim the resume could not carry.
8. First person, no contractions, sentences of ordinary length. A human
   sentence about pride in the work or being easy to work with is in voice.

## Paragraph plan

Follow `assets/coverletter_template.tex`:

1. **P1.** The role (title as the posting writes it), who the user is in one
   line, one human sentence about how they work.
2. **P2.** One concrete project from the resume that mirrors the posting's
   core work, told as a short story: the problem, what the user did, how it
   came out.
3. **P3.** The honest gaps against the posting, each bridged in a sentence or
   two. Drop this paragraph only when there are no real gaps, and use the
   space for a second relevant strength.
4. **P4.** People skills, then logistics the posting asks about (citizenship,
   clearance eligibility, travel, relocation, site access already held) as
   plain statements, then a plain invitation to talk.

Close with exactly: "Thank you for your consideration. Please do not hesitate
to contact me if you have any questions." Then `\closing{Sincerely,}`.

## Header and recipient

- `\name{}` is the user's name; the class uppercases it.
- `\letterdate{}` only when a fixed date is wanted; omit it for today.
- `\contactline{}` once per line: mailing address (the letter is the one
  place a street address appears), city/state/ZIP, email, phone.
- `\recipient{Company \\ City, ST \\ Position Title (ReqID)}`. When the
  posting is fillable at two levels, name the level the resume targets.

## Signature

The class looks for `signature.png` beside the `.tex` and falls back to the
typed name, so a letter is never unsigned. If there is no `signature.png` in
the application folder, run:

```
python scripts/make_signature.py --name "First Last" --out applications/<Company>_<ReqID>/signature.png
```

Never pass `--force` over an existing `signature.png` unless the user asks.
It may be a scan of their real signature, and that always wins.

## Checks

```
python scripts/build.py <letter>.tex
python scripts/ats_check.py <letter>.pdf --letter
```

One page, no em dash, no colon or semicolon in the body, signature image
present. Then reread it once for flattery and for any fact not in the resume
or profile.
