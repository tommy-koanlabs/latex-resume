%% resume.cls -- ATS-safe engineering resume
%%
%% Compile with pdfLaTeX (TeX Live, MiKTeX, or Overleaf). Single column, no
%% tables, no graphics, real text layer. Every visual choice here is a house
%% style decision documented in references/style_resume.md. Change the knobs,
%% not the structure.
%%
%% Document-level API (see resume_template.tex):
%%   \name{..}  \contact{a \sep b \sep c}  \makeheader
%%   \section*{..}
%%   \skill{Label}{items}
%%   \role{Title}{Dates}{Organization -- City, ST}   then an itemize
%%   \degree{Degree, GPA}{Date}{School}{detail line or empty}
%%   \publication{Title}{Venue, Year (Type)}
%%   \project{Title}{Context}                        then text or an itemize
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/10/04 v1.0 ATS-safe engineering resume]

\LoadClass[11pt,letterpaper]{article}

% ---------- page ----------
\RequirePackage[letterpaper,top=0.5in,bottom=0.5in,left=0.5in,right=0.5in]{geometry}

% ---------- fonts / encoding ----------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{palatino}

% ---------- machine-readable text layer (pdfTeX only) ----------
% Maps every glyph, including fi/fl ligatures and en dashes, back to Unicode
% so that ATS parsers and copy/paste get clean text.
\RequirePackage{iftex}
\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\else
  \ClassWarningNoLine{resume}{Not running pdfLaTeX. The Unicode text-layer
    mapping is pdfTeX-specific; verify text extraction with pdftotext}
\fi

\RequirePackage{enumitem}
\RequirePackage{titlesec}
\RequirePackage[hidelinks]{hyperref}

% ---------- global text behavior ----------
\raggedright                 % no justification: even word spacing, no rivers
\hyphenpenalty=10000         % never hyphenate: keywords must stay whole words
\exhyphenpenalty=10000
\pagestyle{empty}            % no page numbers
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\@beginparpenalty=\@M        % never break between a heading line and its list

% ---------- spacing knobs (tune these for page fit) ----------
\newlength{\resitemsep}   \setlength{\resitemsep}{2pt}     % between bullets
\newlength{\ressecbefore} \setlength{\ressecbefore}{10pt}   % above a section heading
\newlength{\ressecafter}  \setlength{\ressecafter}{10.9pt}  % below a section rule
\newlength{\resrolegap}   \setlength{\resrolegap}{7pt}     % between roles / degrees
\newlength{\resentrygap}  \setlength{\resentrygap}{4pt}    % between publications / projects

% ---------- section headings: bold, large, full-width rule ----------
% (the flag lets the first entry under a heading skip its leading gap)
\newif\if@resfirst \@resfirstfalse
\titleformat{\section}{\bfseries\large}{}{0pt}{}%
  [\vspace{1pt}\titlerule\vspace{-2pt}\global\@resfirsttrue]
\titlespacing*{\section}{0pt}{\ressecbefore}{\ressecafter}

% ---------- bullets: en dash label, tight, shallow indent ----------
\renewcommand\labelitemi{--}
\setlist[itemize]{itemsep=\resitemsep, leftmargin=12pt, topsep=1pt,
                  partopsep=0pt, parsep=0pt}

% ---------- header ----------
\newcommand{\sep}{\hspace{0.45em}\textbar\hspace{0.45em}}  % contact / inline separator
\newcommand{\name}[1]{\gdef\@resname{#1}}
\newcommand{\contact}[1]{\gdef\@rescontact{#1}}
\name{}\contact{}
\newcommand{\makeheader}{%
  \centerline{\LARGE \@resname}%
  \vspace{5pt}%
  \centerline{\@rescontact}%
  \vspace{1.5pt}}

% PDF metadata (some ATS and all recruiters' file previews read this)
\AtBeginDocument{\hypersetup{pdfauthor={\@resname},pdftitle={\@resname\space Resume}}}

% ---------- entries ----------
% Lines inside one entry are joined with \\* so a page break can never fall
% between a title line and the line under it.
% Leading gap before an entry, suppressed directly under a section heading.
\newcommand{\res@gap}[1]{%
  \par\if@resfirst\global\@resfirstfalse\else\addvspace{#1}\fi}

% \skill{Label}{comma separated items}
\newcommand{\skill}[2]{\textbf{#1:} #2\par}

% \role{Title}{Dates}{Organization -- City, ST}
\newcommand{\role}[3]{%
  \res@gap{\resrolegap}%
  \textbf{#1} \hfill \textbf{#2}\\*
  \textit{#3}\par\nobreak\vspace{1pt}}

% \degree{Degree, GPA}{Date}{School}{detail line (thesis, honors) or empty}
\newcommand{\degree}[4]{%
  \res@gap{\resrolegap}%
  \textbf{#1} \hfill \textbf{#2}\\*
  \textit{#3}%
  \if\relax\detokenize{#4}\relax\else\\*[1pt]#4\fi\par}

% \publication{Title}{Venue, Year (Type)}
\newcommand{\publication}[2]{%
  \res@gap{\resentrygap}%
  \textbf{#1}\\*
  \textit{#2}\par}

% \project{Title}{Context}  -- follow with one plain description line or an
% itemize. Pick one form and use it for every project in the section.
\newcommand{\project}[2]{%
  \res@gap{\resentrygap}%
  \textbf{#1}\sep\textit{#2}\par\nobreak\vspace{1pt}}

\endinput
