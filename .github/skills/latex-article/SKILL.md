---
name: latex-article
description: 'Generate a LaTeX article for a given subject using the IS&T two-column article template. Use when: writing a new technical article, engineering paper, or academic report; creating a new .tex file from scratch; need a structured document with abstract, sections, math equations, figures, and bibliography. Produces a compilable .tex file matching the template in templates/article.tex.'
argument-hint: 'Subject or topic for the article (e.g., "Newton-Cotes integration methods")'
---

# LaTeX Article Generator

## When to Use
- Writing a new technical or academic article on an engineering/math topic
- Starting a new `.tex` file from the IS&T two-column article template
- Any request to "create a LaTeX article", "write a paper", or "draft a technical report"

## Template Overview

The template lives at [templates/article.tex](../../../templates/article.tex) and uses [templates/ist.sty](../../../templates/ist.sty).

**Document class:**
```latex
\documentclass[letterpaper,twocolumn,fleqn]{article}
```

**Standard packages** (always include):
```latex
\usepackage{ist}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{physics}
\usepackage{siunitx}
```

**Author format:**
```
Firstname Lastname; Institution Name; City, State
```

## Procedure

### 1. Gather Requirements
Ask (or infer from context) the following:
- **Subject / topic** — what the article is about
- **Author name and affiliation** — ask for the author's name; institution defaults to `California Polytechnic University Pomona; Pomona, California`
- **Target output path** — e.g., `unit04/article.tex`
- **Key sections needed** — default set listed below

### 2. Plan the Article Structure
Use the standard section order:
1. Abstract (concise summary, 100–200 words)
2. Introduction — motivation, context, problem statement
3. Theory / Method — define the method with equations
4. Application / Analysis — apply the method to the specific problem
5. Error Analysis (if numerical) — derive or bound the error
6. Numerical Comparison / Results — concrete numbers and figures
7. Discussion — interpretation, limitations, tradeoffs
8. Conclusion — restate key findings in 1–2 paragraphs
9. References / Bibliography

Omit or merge sections that do not apply to the subject.

### 3. Write the LaTeX File

Follow these conventions from the template:

**Math:** Use `\[...\]` for displayed equations, `$...$` for inline. Use `physics` package macros (`\dd`, `\dv`, `\pdv`, `\norm`, etc.) and `siunitx` (`\SI{9.81}{\meter\per\second\squared}`) where appropriate.

**Section headers with labels:**
```latex
\section{Introduction}
\label{sec:intro}
```

**Figures:**
```latex
\begin{figure}[h!]
    \centering
    \includegraphics[width=1\linewidth]{path/to/image.png}
    \caption{Caption text.}
    \label{fig:label}
\end{figure}
```

**Bibliography:**
```latex
\small
\begin{thebibliography}{9}
\bibitem{bib1}
Author, \emph{Title}, Publisher, Year.
\end{thebibliography}
```

**Section comment blocks** (keep consistent with template style):
```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Section name
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

### 4. Quality Checklist
Before finalizing, verify:
- [ ] `\documentclass`, all five standard packages, and `\usepackage{ist}` are present
- [ ] `\pagestyle{empty}` appears after package declarations
- [ ] Title, author (correct format), and `\date{}` are set
- [ ] `\maketitle` and `\thispagestyle{empty}` follow `\begin{document}`
- [ ] Abstract is present and self-contained
- [ ] All equations are numbered or displayed correctly (no raw `$$`)
- [ ] At least one bibliography entry exists
- [ ] Document ends with `\end{document}`
- [ ] Output path matches the requested location

### 5. Copy `ist.sty`
Copy `templates/ist.sty` into the same directory as the new `.tex` file so the document compiles without any path configuration.

Example: if the output is `unit04/article.tex`, copy `templates/ist.sty` → `unit04/ist.sty`.

### 6. Output
Create the `.tex` file at the requested path. Remind the user that images referenced with `\includegraphics` must exist at the specified relative paths.
