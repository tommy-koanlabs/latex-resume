# Eval results: iteration 1

Run on 2026-10-05. Outputs live in `resume-tailor-workspace/iteration-1/` (gitignored).
Scripted checks: `python evals/check_outputs.py <id> <outputs>`. Every resume was also read against its profile by hand.

| # | Eval | Runner | Scripted checks | Read-through |
|---|---|---|---|---|
| 1 | Complete profile, example posting | Author (biased) | PASS 12/12 | Every bullet traces to the profile. 2 pages, page 2 about half full. |
| 2 | Same profile, structural analyst posting | Independent agent | PASS 9/9 | Summary, skills, bullet order lead with analysis. Job order and titles unchanged. "Structural" mirrored as "stress" analysis (same work). Buckling kept as checks, not FE runs. Asked 5 questions first (Patran/HyperMesh and NASGRO each repeated in the posting), then wrote with them as gaps. |
| 3 | Thin profile, example posting | Independent agent, 2 turns | PASS 13/13 | Asked exactly 2 questions (bench equipment, ATPs), quoting the posting. "No" answers kept off the resume, listed as gaps, saved to the profile. |
| 4 | Old resume only, I&T posting | Independent agent, 2 turns | PASS 18/18 | Built the profile, 5 questions, 1-page resume (not padded). Dropped LabVIEW, GPA 3.40, "2+ years", "passionate", the NCR bullet. TVAC written as setup and monitoring. |
| 5 | Decline Teamcenter, then cover letter | Author (biased) | PASS 9/9 | Declined in one sentence, offered Windchill PLM. Letter 1 page, signed, names NX and clearance gaps. The first draft contained an invented detail, which was caught and removed. |

## Findings and fixes

1. **Invented story detail in a cover letter** (eval 5). Added a sentence-by-sentence source check to SKILL.md and style_coverletter.md.
2. **Bundled questions** (eval 4). Five numbered questions held about eight topics. SKILL.md now asks one topic per question, plus a one-line list of anything that will be treated as a gap.
3. **Wrapped Skills lines** (evals 1, 2, 3). style_resume.md now requires each Skills line to fit one printed line.
4. **Padding Skills to reach five lines** (eval 4). style_resume.md now forbids inventing soft categories to hit the count.
5. **Checker bug** (eval 3). The "no question about confirmed gaps" check also matched a closing note that said those gaps would not be asked about. It now reads only the numbered questions.

## Not yet done

- Fixes 2 to 4 are instruction changes made after the runs. Evals 2 to 4 have not been rerun against them.
- No baseline (without the skill) runs were made.
- Evals 1 and 5 should be rerun by an independent agent.
