%% coverletter.cls -- one-page cover letter that pairs with resume.cls
%%
%% Compile with pdfLaTeX (TeX Live, MiKTeX, or Overleaf).
%%
%% Document-level API (see coverletter_template.tex):
%%   \name{..}                 printed in bold caps, top left
%%   \letterdate{..}           optional; defaults to \today, bold, top right
%%   \contactline{..}          repeat once per line (address, email, phone)
%%   \recipient{a \\ b \\ c}   company, location, position
%%   \signaturefile{..}        optional; defaults to signature.png
%%   \makeheader
%%   \opening{Dear Hiring Manager:}
%%   ...paragraphs separated by blank lines...
%%   \closing{Sincerely,}
%%
%% Class option  typedname  prints the typed name under the signature image.
%% Without a signature image the typed name is always printed, so the letter
%% is never unsigned.
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coverletter}[2026/10/04 v1.0 one-page cover letter]

\newif\if@cltypedname \@cltypednamefalse
\DeclareOption{typedname}{\@cltypednametrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass[11pt,letterpaper]{article}

% ---------- page ----------
\RequirePackage[letterpaper,top=0.75in,bottom=0.75in,left=0.9in,right=0.9in]{geometry}

% ---------- fonts / encoding ----------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{palatino}
\RequirePackage{microtype}          % provides \textls for the spaced contact lines

% ---------- machine-readable text layer (pdfTeX only) ----------
\RequirePackage{iftex}
\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi

\RequirePackage{graphicx}
\RequirePackage[hidelinks]{hyperref}

% ---------- global text behavior ----------
\raggedright
\hyphenpenalty=10000
\exhyphenpenalty=10000
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}           % one blank line in the source = one 8pt gap

% ---------- knobs ----------
\newlength{\clsigheight} \setlength{\clsigheight}{1.2cm}  % signature image height
\newlength{\clblockgap}  \setlength{\clblockgap}{10pt}    % header / recipient / salutation gaps

% ---------- data ----------
\newcommand{\name}[1]{\gdef\@clname{#1}}
\newcommand{\letterdate}[1]{\gdef\@cldate{#1}}
\newcommand{\recipient}[1]{\gdef\@clrecipient{#1}}
\newcommand{\signaturefile}[1]{\gdef\@clsigfile{#1}}
\name{}\letterdate{\today}\recipient{}\signaturefile{signature.png}

% \contactline may be used any number of times; lines print in order.
\newtoks\@clcontact
\newcommand{\contactline}[1]{%
  \global\@clcontact=\expandafter{\the\@clcontact\@clcontactfmt{#1}}}
\newcommand{\@clcontactfmt}[1]{\par\vspace{1pt}\textit{\textls[80]{#1}}}

\AtBeginDocument{\hypersetup{pdfauthor={\@clname},pdftitle={\@clname\space Cover Letter}}}

% ---------- header ----------
\newcommand{\makeheader}{%
  {\setlength{\parskip}{0pt}%
   \textbf{\Large\MakeUppercase{\@clname}} \hfill \textbf{\@cldate}\par
   \vspace{4pt}%
   \the\@clcontact\par
   \vspace{\clblockgap}%
   \@clrecipient\par
   \vspace{\clblockgap}}}

% ---------- salutation ----------
\newcommand{\opening}[1]{{\setlength{\parskip}{0pt}#1\par}}

% ---------- sign-off ----------
% Signature image if the file exists, typed name otherwise.
\newcommand{\closing}[1]{%
  \par\vspace{6pt}#1\par
  \IfFileExists{\@clsigfile}{%
    \vspace{-2pt}\includegraphics[height=\clsigheight]{\@clsigfile}%
    \if@cltypedname\par\vspace{-4pt}\@clname\fi
  }{%
    \vspace{22pt}\@clname
  }\par}

\endinput
