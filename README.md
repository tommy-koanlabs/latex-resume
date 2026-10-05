# resume-tailor

A Claude Skill that turns a job posting into a tailored, ATS-friendly resume
(PDF plus the LaTeX source), built only from your real experience. It can also
write a matching one-page cover letter with a script-font signature.

It never invents experience, numbers, credentials, or job titles. When your
material does not cover something the posting asks for, it asks you a few
short questions first. Anything you do not have is listed as a gap instead of
being written onto the resume.

Everything in this repository is fictional sample data. "John Doe" is not a
real person.

## What you need

- A Claude account with code execution turned on (Claude.ai), or Claude Code.
- One old resume, in any format. PDF, Word, or LaTeX all work.

## Install on Claude.ai

1. Download `resume-tailor.skill` from this repository's releases, or build it
   yourself (see "Build the package" below).
2. In Claude.ai, open **Settings > Capabilities** and make sure code
   execution is on.
3. In the same Capabilities area, find **Skills**, choose to upload a skill,
   and pick `resume-tailor.skill`. (Menu names on Claude.ai change from time
   to time; if you cannot find it, search the Claude help center for
   "upload a skill".)
4. Start a new chat. The skill turns on by itself when you paste a job posting.

## Install in Claude Code

1. Unzip `resume-tailor.skill`. It contains one folder, `resume-tailor`.
2. Move that folder to `~/.claude/skills/` (for all your projects) or to
   `.claude/skills/` inside one project folder.
3. Install Pillow once, for the signature: `pip install pillow`.
4. Optional: install a LaTeX system to make PDFs on your own machine
   (MacTeX on Mac, MiKTeX on Windows, TeX Live on Linux). Without it the skill
   still writes the `.tex` file and tells you how to make the PDF on Overleaf.

## First run

1. Start a chat and attach your old resume.
2. Paste the job posting and say "tailor my resume for this".
3. Answer the questions it asks. There are at most five, and each one quotes
   the line in the posting it is about. "No" is a fine answer. It will list
   that item as a gap and never ask again.
4. You get back:
   - the resume PDF and its `.tex` source,
   - `keyword_map.md`, which shows where each posting keyword landed and why,
   - a short message with the level it targeted, how many posting keywords are
     covered, and the list of gaps,
   - `career_profile.md`, your evidence bank.
5. Say "write the cover letter" if you want one.

The second time, attach `career_profile.md` with the new posting. With a
complete profile there are usually no questions at all.

## Where your files go

**Claude.ai.** Nothing is saved between chats. Download every file you want
to keep, especially `career_profile.md`. Attach it next time.

**Claude Code.** Files are written to the folder you are working in:

```
career_profile.md
applications/<Company>_<ReqID>/
    posting.txt
    keyword_map.md
    <Last>_<Company>_<Role>_<ReqID>.tex and .pdf
    <Last>_<Company>_<Role>_<ReqID>_CoverLetter.tex and .pdf
    signature.png
```

If you have a scan of your real signature, save it as `signature.png` in the
application folder. The skill will use it and never overwrite it.

## Edit and recompile on Overleaf

1. Go to [overleaf.com](https://www.overleaf.com) and create a **Blank
   Project**.
2. Upload your `.tex` file and the class file it uses: `resume.cls` for a
   resume, `coverletter.cls` plus `signature.png` for a letter. The class files
   are in the skill's `assets/` folder.
3. Open **Menu** and set **Compiler** to **pdfLaTeX**.
4. Edit the text and press **Recompile**. Download the PDF from the button
   above the preview.

Keep the layout as it is. The single column, plain section names, and real
text layer are what let applicant tracking systems read the resume.

## For developers

```
python skill/scripts/build.py                     # rebuild both example PDFs
python skill/scripts/ats_check.py skill/references/examples/Doe_Calderwick_TestEquipment_CAS-10482.pdf
python skill/scripts/make_signature.py --name "John Doe" --out /tmp/signature.png
python evals/check_outputs.py <eval id> <outputs folder>
```

### Build the package

```
python package.py
```

This writes `resume-tailor.skill` in the repository folder.

`CLAUDE.md` is the build brief, `DECISIONS.md` records the judgment calls made
while building, and `evals/` holds the eval prompts and fictional fixtures.

The bundled signature font is Great Vibes, licensed under the SIL Open Font
License (`skill/assets/fonts/OFL.txt`).
