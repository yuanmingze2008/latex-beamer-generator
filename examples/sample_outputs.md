# Sample Outputs

## Single File

Use single-file output for small or medium decks where editing in one place is more convenient. The generated project should contain one `main.tex` with title metadata, theme directives, and all frames inline.

## Multi File

Use multi-file output for larger or more complex decks where `main.tex` assembles section files without duplicating slide content. The generated project should contain:

- `main.tex`
- `sections/01-*.tex`
- `sections/02-*.tex`
- additional section files only when structure or slide count justifies them
