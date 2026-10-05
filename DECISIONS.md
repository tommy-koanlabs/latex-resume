# Decisions

One line per judgment call made while building the skill, with the reason.
Where the brief was silent, the choice that best protects rule 3.1 (never
fabricate) won.

- `build.py` with no arguments rebuilds the two shipped examples, so the definition-of-done command works as written.
- `build.py` sets `SOURCE_DATE_EPOCH` only for the shipped examples, so rebuilding them gives identical bytes; user builds keep real timestamps, and `\today` is never frozen.
- `build.py` fails a resume over two pages and a cover letter over one page even without `--pages`, because those limits are hard rules in the brief.
- `build.py` exposes the classes through `TEXINPUTS` for pdfLaTeX and `-Z search-path` for tectonic instead of copying them, so a user's folder never collects stale class copies.
- `ats_check.py` matches keywords on normalized tokens (case, punctuation, `&`/and, plurals, `(s)`, small stopwords) rather than raw bytes, so "Bills of Materials (BOMs)" satisfies "Bill of Materials (BOM)"; byte-exact matching would fail honest resumes on grammar alone.
- A mapped keyword that is only partly present is a WARN, not a FAIL. Forcing every posting phrase verbatim would push the drafter to reword real work into the posting's words even when it is not the same thing (rule 3.9); the example itself says "frames" where the posting says "fixtures", because that is what John analyzed.
- A keyword row whose "Where it lands" cell starts with "Not on resume" is skipped, which is how the example map handles citizenship (stated in the cover letter, not the resume).
- Without `--profile`, a Skills item with no bullet behind it is a WARN, because the script cannot see the confirming profile line; with `--profile` it is a FAIL. An exposure-level tool must also have a bullet stating its narrow use, which enforces rule 3.3.
- `ats_check.py` adds checks the brief implies but does not list: no em dashes, no clearance-eligibility wording on the resume (rule 3.5), fonts embedded with Unicode maps (the example map lists it), and any confirmed gap from the profile appearing on the resume.
- Allowed section headings are the template's plus "Certifications" and "Licenses & Certifications", because a licensed engineer (PE) needs somewhere exact to put the license.
- `ats_check.py --letter` implements verification step 8 for cover letters and confirms a signature image is embedded.
- Bundled Great Vibes (OFL) as the one signature font, because the stand-in example already used it and switching would change the example letter's look.
- `make_signature.py` checks glyph coverage by reading the font's `cmap` table with `struct`, since Pillow cannot report missing glyphs and fontTools is outside the allowed dependencies.
- `make_signature.py` renders with Pillow's BASIC layout engine so the PNG is byte-identical whether or not libraqm is installed; Great Vibes connects letters without OpenType shaping.
- `make_signature.py` rejects `--height` below 300 px instead of silently raising it, so the user sees why.
- The keyword map's coverage table is the machine-readable contract between the drafter and `ats_check.py`; `style_resume.md` fixes its column shape instead of inventing a second format.
- The profile template fixes simple Markdown shapes (`### Title` + `- Dates:` lines, a `| Item | Level |` table, bold gap bullets) so `ats_check.py --profile` can verify titles, dates, and skills without a YAML dependency.
- Profile conflicts between two old resumes go to an "Open conflicts" section and a question, never a silent pick, per section 7.
- `evals/evals.json` uses the skill-creator field `expectations`, adds a `name` per eval, and gives file paths relative to the repo root because the fixtures live outside `skill/` so they never ship in the package.
- Multi-turn evals (3, 4, 5) carry the simulated user's replies inside the prompt, so a runner can answer the skill's questions without a human.
- The thin profile for eval 3 keeps the old vague "Co-author test procedures" bullet at level `?` instead of deleting it, which is how real old resumes look and is what should trigger the ATP question.
- Eval 4 uses a second fictional person (Jane Roe, electrical I&T) to prove the workflow is not mechanical-engineering specific. Her old resume carries deliberate flaws (vague verbs, unbacked skills, a years count, a 3.40 GPA) that the skill must drop or ask about.
- `.gitignore` now allows `career_profile.md` and PDFs under `evals/fixtures/` only, since those are fictional fixtures; the blanket rules still protect a user's real files everywhere else.
- Evals 1 and 5 were run in this session by the author following SKILL.md, not by an independent agent; they prove the scripts and fixtures work end to end but are biased as a test of the instructions. Evals 2 to 4 still need independent runs.
- During eval 5 the draft letter gained an invented detail ("no drawing changes"). No script can catch that, so SKILL.md and style_coverletter.md now require a sentence-by-sentence source check before building a letter (fix the skill, not the evals).
- README describes the Claude.ai upload path loosely and points to the help center, because menu names change faster than this repo.
- `package.py` lives at the repo root (not in `skill/`) and writes the zip with `resume-tailor/` as its top folder, since the repo folder is named `skill/` but the installed folder must match the skill name. Output validated with skill-creator's `quick_validate`.
