# Content Generation

## Two Input Modes

### Topic Mode

Use topic mode when the user provides a theme or subject but not the actual slide wording.

The agent should produce:

- a high-level slide arc
- per-slide titles
- concise bullet content
- a density appropriate for the duration and audience

### Source Material Mode

Use source material mode when the user provides text, notes, summaries, papers, or agent-derived descriptions from files.

The agent should:

- extract the main claims or teaching points
- compress dense prose into presentation-friendly bullets
- avoid copying source text verbatim into slides
- convert long material into a clean speaking sequence

## Non-Text Source Inputs

PNG files, screenshots, and PDF page images can still be part of the flow, but the vision step should happen agent-side.

Expected pattern:

1. the agent interprets the non-text file
2. the agent turns it into a structured description
3. the description is inserted into the deck spec
4. generation uses that description as content or style guidance

Use `normalize_source_input.py` only after the non-text reasoning step is already complete. The script should receive those descriptions as structured input, not raw images.

## Slide Density Rules

Prefer:

- one clear point per slide
- short bullets over pasted paragraphs
- formulas only when they materially help the audience
- tables only when they can be read at presentation distance

If the user does not specify slide count, propose one using presentation duration and academic norms.
