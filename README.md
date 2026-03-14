# latex-beamer-generator

`latex-beamer-generator` is an open skill project for agents that need to generate academic LaTeX Beamer slide decks.

The repository is designed for agent workflows rather than as a standalone end-user application. Its primary contract is [`SKILL.md`](SKILL.md). Ecosystem-specific metadata such as `agents/openai.yaml` is optional and non-authoritative.

## What The Skill Does

The skill helps an agent:

- detect when an academic PPT or PDF request should be handled as Beamer
- ask follow-up questions when planning details are missing
- generate slide content from either a topic or source material
- consume agent-derived descriptions for non-text inputs such as screenshots or rendered PDF pages
- generate editable Beamer projects in either single-file or multi-file form
- support common academic themes including `Berlin`, `Madrid`, `Boadilla`, `AnnArbor`, and `metropolis`

## Repository Structure

```text
latex-beamer-generator/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    workflow.md
    content-generation.md
    beamer-themes.md
  assets/
    templates/
    theme-presets/
  scripts/
    normalize_source_input.py
    generate_beamer_project.py
    compile_beamer_project.py
  examples/
    sample_requests.md
    sample_outputs.md
```

## Core Files

- [`SKILL.md`](SKILL.md): primary behavior contract for agent usage
- [`agents/openai.yaml`](agents/openai.yaml): optional metadata for ecosystems that support skill discovery
- [`references/workflow.md`](references/workflow.md): end-to-end request-to-output workflow
- [`references/content-generation.md`](references/content-generation.md): topic mode and source-material mode guidance
- [`references/beamer-themes.md`](references/beamer-themes.md): supported theme choices and defaults
- [`scripts/normalize_source_input.py`](scripts/normalize_source_input.py): normalize a loose spec into a more stable generation spec
- [`scripts/generate_beamer_project.py`](scripts/generate_beamer_project.py): generate a Beamer project from a normalized spec
- [`scripts/compile_beamer_project.py`](scripts/compile_beamer_project.py): compile a generated Beamer project with `latexmk`

## Runtime Requirements

For local script usage:

- Python 3.10 or newer
- A LaTeX toolchain with `latexmk` and Beamer support if you want PDF compilation

Typical environment checks:

```powershell
python --version
latexmk -v
```

## Minimal Local Flow

The helper scripts are usable directly for local verification.

```powershell
python scripts\normalize_source_input.py --spec path\to\spec.json --output generated\normalized.json
python scripts\generate_beamer_project.py --spec generated\normalized.json --output-dir generated\deck
python scripts\compile_beamer_project.py --project-dir generated\deck
```

If you only want the `.tex` output, skip the compile step.

## Open Source Positioning

This repository is intended to remain usable as a general agent skill:

- `SKILL.md` is the main specification
- helper scripts support the skill instead of replacing it
- agents that do not understand `agents/openai.yaml` can still use the repository through `SKILL.md`, `references/`, `assets/`, and `scripts/`

## Status

Version 1 focuses on:

- trigger and follow-up behavior for academic slide requests
- two content-generation modes: topic and source material
- multiple Beamer themes
- adaptive single-file versus multi-file output

Future improvements may expand outline planning, bibliography handling, visual conventions, and richer source normalization.
