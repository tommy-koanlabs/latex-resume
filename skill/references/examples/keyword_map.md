# Keyword map: John Doe vs. CAS-10482

Worked example of the analysis the skill produces between "user pastes a
posting" and "user gets a resume". Everything here is fictional.

The example resume is condensed on purpose so it reads quickly. A real resume
for a candidate at this level carries more bullets and fills two pages. The
tracing below is the part to copy.

Files in this example:

| File | What it is |
|---|---|
| `job_posting.txt` | Input. What the user pasted. |
| `keyword_map.md` | This file. Analysis, Q&A, coverage, gaps. |
| `Doe_Calderwick_TestEquipment_CAS-10482.tex/.pdf` | Output resume. |
| `Doe_Calderwick_TestEquipment_CAS-10482_CoverLetter.tex/.pdf` | Output cover letter. |
| `signature.png` | Script-font signature used by the cover letter. |

## 1. Posting read

- **Center of gravity:** hands-on test equipment design. Station design,
  drawings, BOM, ATP, build support. Analysis and fluid systems are secondary.
- **Level:** fillable at Principal (MS + 3) or Senior Principal (MS + 6).
  John has an M.S. (Dec 2019) and related experience since June 2017, so he
  meets Senior Principal. Resume is written to that level: ownership verbs
  and a mentoring bullet.
- **Gates:** U.S. citizenship (has), ability to obtain Secret (eligible).
  Active Secret is preferred only.
- **Vocabulary to mirror:** "test station" (not cart, rig, or stand),
  "laboratory systems", "Acceptance Test Procedures (ATPs)",
  "manufacturing liaison", "multi-discipline team".

## 2. Q&A gate (what the skill asked before drafting)

John's old resumes had no evidence for one basic qualification and thin
evidence for three other posting items. The skill asked before writing.

> **Q1 (Basic qual: "hands-on experience with test equipment such as
> oscilloscopes, power supplies, and multimeters").** Nothing in your resumes
> shows this. Have you used bench electronics? Where, and for what?
>
> **A.** Yes. I check sensor signals with a scope, bench supply, and DMM when
> I bring up a DAQ on a new station. I also build microcontroller boards at
> home and debug them with a scope and logic analyzer.
>
> **Q2 (Responsibility + preferred: "develop and execute ATPs").** Your old
> resume says "co-author test procedures". Did you write and run acceptance
> procedures yourself, or contribute to someone else's?
>
> **A.** I wrote and ran them for the stations I designed. Proof, leak,
> functional.
>
> **Q3 (Basic qual: "Siemens NX or another 3D mechanical design tool").**
> Your skills line lists NX. How did you use it?
>
> **A.** Only geometry cleanup for FEA at my last job. Creo is my real tool.
>
> **Q4 (Preferred: Teamcenter, LabVIEW, active Secret).** Do you have any of
> these?
>
> **A.** No to all three. Windchill instead of Teamcenter. I log data with NI
> hardware but never wrote LabVIEW. No clearance.

Result: Q1 and Q2 became new, true bullets. Q3 set the claim level for NX.
Q4 confirmed three gaps, which were recorded in the career profile so they
are never asked again.

## 3. Coverage table

Status key: **Strong** = direct, recent, repeated. **Have** = real but
lighter. **Adjacent** = related experience, claimed only as what it is.
**Gap** = not claimed anywhere.

| Posting keyword or phrase | Source in posting | Status | Where it lands in the resume |
|---|---|---|---|
| test station(s) | Title, resp., preferred | Strong | Summary; Skills 1; Role 1 bullets 1, 3, 4, 5; publication title |
| test fixture(s) | Resp. | Strong | Summary; Skills 1; Role 1 bullet 1; Role 3; capstone project |
| laboratory systems | Resp. | Strong | Summary; Role 1 bullet 1 |
| concept through fabrication, integration, checkout | Resp. | Strong | Summary; Role 1 bullet 1 |
| solid models, assemblies, detailed engineering drawings | Resp. | Strong | Role 1 bullet 2, in the posting's exact order |
| GD&T, ASME Y14.5 | Resp., basic | Strong | Skills 3; Role 1 bullets 2, 7; Role 2 bullet 1 |
| Bill of Materials (BOM) | Resp., preferred | Strong | Skills 3; Role 1 bullet 2 (spelled out and acronym) |
| configuration management, PLM | Resp. | Strong | Skills 3; Role 1 bullet 2 |
| Acceptance Test Procedures (ATPs) | Resp., preferred | Strong | Skills 1; Role 1 bullet 4 (from Q2) |
| instrumentation, data acquisition (DAQ) | Resp. | Strong | Skills 4; Role 1 bullet 5 |
| pneumatic and fluid systems, ASME B31.3 | Resp. | Have | Role 1 bullet 3 |
| structural analysis of fixtures and support structure | Resp. | Strong | Summary; Role 2 bullet 2 |
| multi-discipline team: supply chain, operations, quality assurance | Resp. | Strong | Role 1 bullet 6 |
| manufacturing liaison; fabrication, assembly, installation | Resp., preferred | Strong | Skills 5; Role 1 bullet 6 |
| mentor less experienced engineers | Resp. | Have | Role 1 bullet 7 |
| oscilloscopes, power supplies, multimeters | Basic | Have | Skills 4; Role 1 bullet 5; personal project (from Q1) |
| test engineering concepts | Basic | Strong | Role 3 bullet 1, plus the whole of Role 1 |
| MS in Mechanical Engineering | Preferred | Strong | Education |
| U.S. citizenship | Basic | Have | Not on resume (header shows it only when the user's profile says to). Stated in the cover letter. |
| Siemens NX | Resp., basic | Adjacent | Skills 2 (listed after Creo); Role 2 bullet 2 says exactly how it was used |
| Teamcenter | Resp., preferred | Gap | Not on resume. "Windchill PLM" carries the PLM keyword. |
| LabVIEW | Preferred | Gap | Not on resume. |
| Active DoD Secret clearance | Preferred | Gap | Not on resume. Eligibility is stated in the cover letter. |

## 4. Gaps reported to the user at delivery

1. **NX depth.** NX is listed because John has used it, but only for geometry
   preparation. Creo is listed first. If asked, the honest answer is "Creo
   daily, NX occasionally". Bridged in the cover letter.
2. **Teamcenter.** Not claimed. Windchill is the equivalent tool and is named.
   Bridged in the cover letter.
3. **LabVIEW.** Not claimed. Preferred only. Left alone.
4. **Clearance.** Not claimed. The resume says nothing about clearance. The
   cover letter states citizenship and eligibility in plain words.

## 5. Checks run on the PDF

| Check | Result |
|---|---|
| Page count | 2 |
| Text layer extracts in reading order (`pdftotext -layout`) | Pass |
| No ligature or private-use characters in extracted text | Pass |
| Email and phone found as plain text in the first two lines | Pass |
| Standard section headings | Pass |
| Posting keywords found verbatim | 19 of 23 rows (3 intentional gaps; citizenship is in the cover letter only) |
| Every Skills item backed by a bullet or a confirmed profile line | Pass |
| No placeholder text (`<...>`) | Pass |
| Fonts embedded with Unicode maps (`pdffonts`) | Pass |
