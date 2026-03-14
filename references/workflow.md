# Workflow

## Summary

This skill turns an academic slide request into a Beamer project through a fixed pipeline:

1. detect that the request is academic slide work
2. ask whether Beamer should be used if the user only asked for PPT/PDF
3. gather missing planning details
4. normalize the request into a deck spec
5. generate the Beamer project
6. optionally compile

## Deck Spec Expectations

The agent should stabilize a spec before invoking generation.

Suggested fields:

- `mode`: `topic` or `source_material`
- `topic`
- `source_paths`
- `source_text`
- `agent_derived_descriptions`
- `context`
- `audience`
- `duration_minutes`
- `target_slide_count`
- `slide_count_source`
- `language`
- `theme`
- `tone`
- `has_math`
- `has_tables`
- `has_bibliography`
- `visual_requirements`
- `content_outline`
- `output_layout_mode`

Normalization may fill in `mode`, `target_slide_count`, `slide_count_source`, and `output_layout_mode` when the incoming spec omitted them.

## Layout Strategy

Use `single_file` when:

- the deck is roughly 15 slides or fewer
- the user did not ask for modular output
- the structure is straightforward

Use `multi_file` when:

- the deck is larger than roughly 15 slides
- the content spans clearly separable modules
- the user wants a more maintainable project layout

## Agent Responsibility

The agent is responsible for:

- deciding when to ask questions
- deciding whether Beamer is appropriate
- deriving structured visual descriptions from non-text files
- determining when the output should be single-file or multi-file

The scripts are responsible for deterministic project generation, not product-level decisions.
