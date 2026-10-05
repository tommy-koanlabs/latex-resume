# Decisions

One line per judgment call made while building the skill, with the reason.
Where the brief was silent, the choice that best protects rule 3.1 (never
fabricate) won.

- `build.py` with no arguments rebuilds the two shipped examples, so the definition-of-done command works as written.
- `build.py` sets `SOURCE_DATE_EPOCH` only for the shipped examples, so rebuilding them gives identical bytes; user builds keep real timestamps, and `\today` is never frozen.
- `build.py` fails a resume over two pages and a cover letter over one page even without `--pages`, because those limits are hard rules in the brief.
- `build.py` exposes the classes through `TEXINPUTS` for pdfLaTeX and `-Z search-path` for tectonic instead of copying them, so a user's folder never collects stale class copies.
