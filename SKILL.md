---
name: latex-beamer-generator
description: Use when the user wants an academic slide deck, research presentation, seminar deck, thesis defense, class report, or academic-style PPT/PDF and Beamer may be a better fit. The skill asks follow-up questions when planning details are missing, supports content generation from either a topic or source material, and generates an editable LaTeX Beamer project with common themes such as Berlin, Madrid, Boadilla, AnnArbor, and metropolis.
---

# Latex Beamer Generator

## Core Behavior

Treat the repository as a single agent skill, not as a standalone local application.

Follow this flow:

1. Decide whether the request is academic enough that Beamer is a good fit.
2. Ask whether to use Beamer if the user asked for an academic PPT or PDF without naming Beamer.
3. Ask follow-up questions when required planning details are missing.
4. Normalize the request into a structured deck spec.
5. Generate the Beamer project.
6. Compile only if the environment and user request make that useful.

## Required Follow-Up Questions

Before generating, confirm or infer:

- presentation context: defense, group meeting, class report, seminar, conference talk
- audience
- content mode: generate from topic, or generate from source material
- duration or target slide count
- preferred theme
- whether formulas, tables, references, and diagrams are needed
- output language

If the user cannot provide a slide count, suggest one based on academic norms and the requested duration.

Use these defaults when suggesting:

- 5 minutes: 5-7 slides
- 10 minutes: 8-12 slides
- 15 minutes: 12-16 slides
- 20 minutes: 15-20 slides

Record the result in the internal spec using `target_slide_count` and `slide_count_source`.

## Source Handling

Support two main modes:

- `topic`: the agent generates the body content from the user's topic and constraints
- `source_material`: the agent restructures source material into slides

Use `scripts/normalize_source_input.py` to:

- infer `mode` if the request omitted it
- ingest text files from `source_paths`
- preserve agent-provided descriptions for non-text sources
- suggest slide count and layout defaults when the spec omitted them

Non-text materials such as PNGs, screenshots, and rendered PDF pages should be interpreted by the agent or model first. Convert them into structured descriptions before passing them into the generation flow. Do not rely on the script layer for vision reasoning.

## Theme Selection

Support at least these themes:

- `Berlin`
- `Madrid`
- `Boadilla`
- `AnnArbor`
- `metropolis`

Default to `Berlin` unless the user specifies another academic theme.

Read [references/beamer-themes.md](references/beamer-themes.md) when theme choice matters.

## Output Strategy

Default to a single-file `main.tex` deck when the presentation is small to medium sized.

Switch to multi-file output only when one of these is true:

- the deck is large or structurally complex
- the slide count is high, typically above 15
- the user explicitly prefers modular output

Use `output_layout_mode` with these meanings:

- `single_file`: store all slide content in `main.tex`
- `multi_file`: let `main.tex` assemble section files under `sections/`

In multi-file mode, keep the actual slide content inside the included section files so the user edits each slide in exactly one place.

## Resources

Read these references as needed:

- [references/workflow.md](references/workflow.md)
- [references/content-generation.md](references/content-generation.md)
- [references/beamer-themes.md](references/beamer-themes.md)

Useful scripts:

- `scripts/normalize_source_input.py`
- `scripts/generate_beamer_project.py`
- `scripts/compile_beamer_project.py`

Theme assets live under `assets/theme-presets/`.
