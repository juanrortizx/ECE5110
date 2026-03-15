---
name: latex-slides
description: Generate a LaTeX slide presentation for a unit by summarizing that unit's article.
argument-hint: Unit folder, for example "unit03"
---

# Latex Slides Skill

## Purpose
Create a short presentation for a course unit based on that unit's LaTeX article.

This skill reads the article, extracts the main ideas, and generates a slide deck for presentation. The article is the main source of truth.

## Expected Project Structure
Each unit should follow this layout:

- `unitXX/article/article.tex`
- `unitXX/slides/slides.tex`
- `unitXX/results/` for generated figures or result files
- `unitXX/tests/` for unit-specific tests

Shared numerical code may live outside the unit folder, for example in `lib/tool.py`.

## Inputs
Primary input:
- `unitXX/article/article.tex`

Optional supporting inputs:
- images or plots in `unitXX/results/`
- other LaTeX files in `unitXX/article/`

## Output
Create or update:

- `unitXX/slides/slides.tex`

## Rules
- Base the slides on the article.
- Do not invent results that are not present in the article.
- Summarize instead of copying large blocks of text.
- Keep slides short and presentation-focused.
- Prefer bullet points over paragraphs.
- Preserve important formulas when needed for understanding.
- Put the authors' names and the article title on the first slide.
- If the article references figures from `unitXX/results/`, reuse those same files with relative paths.
- Do not copy images into the slides folder unless explicitly requested.
- end presentation with a slide prompting for questions.

## Typical Slide Flow
Use a structure like this when appropriate:

1. Title
2. Problem overview
3. Method or algorithm
4. Key formulas or ideas
5. Implementation summary
6. Example or results
7. Conclusion

Adjust the structure to fit the article.

## Length
Target about 5 to 10 slides unless the user asks for something different.

## Workflow
1. Read `unitXX/article/article.tex`.
2. Identify the main problem, methods, formulas, and conclusions.
3. Build a short slide outline.
4. Write `unitXX/slides/slides.tex`.
5. Reuse figures from `unitXX/results/` by referencing them with relative paths when needed.

## Figure Path Guidance
If a figure exists at:

- `unit03/results/plot1.png`

then `unit03/slides/slides.tex` should reference it like:

```latex
\includegraphics[width=\linewidth]{../results/plot1.png}