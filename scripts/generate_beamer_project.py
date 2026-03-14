from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "assets" / "templates"
PRESET_DIR = ROOT_DIR / "assets" / "theme-presets"
MAIN_TEMPLATE_NAMES = {
    "single_file": "single-file-main.tex",
    "multi_file": "multi-file-main.tex",
}
THEME_MAP = {
    "berlin": "\\usetheme{Berlin}",
    "madrid": "\\usetheme{Madrid}",
    "boadilla": "\\usetheme{Boadilla}",
    "annarbor": "\\usetheme{AnnArbor}",
    "metropolis": "\\usetheme{metropolis}",
}
SPECIAL_REPLACEMENTS = [
    ("\\", "\\textbackslash{}"),
    ("&", "\\&"),
    ("%", "\\%"),
    ("$", "\\$"),
    ("#", "\\#"),
    ("_", "\\_"),
    ("{", "\\{"),
    ("}", "\\}"),
]


def sanitize_tex(text: str) -> str:
    sanitized = text
    for src, dst in SPECIAL_REPLACEMENTS:
        sanitized = sanitized.replace(src, dst)
    return sanitized


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def infer_layout(spec: dict[str, Any]) -> str:
    chosen = str(spec.get("output_layout_mode", "") or "").strip().lower()
    if chosen in {"single_file", "multi_file"}:
        return chosen
    slide_count = int(spec.get("target_slide_count", 0) or 0)
    return "multi_file" if slide_count > 15 else "single_file"


def load_template(layout: str) -> str:
    template_name = MAIN_TEMPLATE_NAMES[layout]
    return (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")


def load_theme_metadata(theme_name: str) -> dict[str, Any]:
    preset_path = PRESET_DIR / f"{theme_name.strip().lower()}.json"
    if preset_path.exists():
        return json.loads(preset_path.read_text(encoding="utf-8"))
    return {"theme": "Berlin", "notes": "Fallback academic theme."}


def theme_directives(theme_name: str) -> str:
    metadata = load_theme_metadata(theme_name)
    theme_key = str(metadata.get("theme", theme_name) or "Berlin").strip().lower()
    lines = [THEME_MAP.get(theme_key, THEME_MAP["berlin"])]
    color_theme = metadata.get("color_theme")
    font_theme = metadata.get("font_theme")
    if color_theme:
        lines.append(f"\\usecolortheme{{{sanitize_tex(str(color_theme))}}}")
    if font_theme:
        lines.append(f"\\usefonttheme{{{sanitize_tex(str(font_theme))}}}")
    return "\n".join(lines)


def render_frame(slide: dict[str, Any]) -> str:
    title = sanitize_tex(str(slide.get("title", "Untitled Slide")))
    bullets = [sanitize_tex(str(item)) for item in list(slide.get("bullets", []) or [])]
    body_text = str(slide.get("body", "") or "").strip()
    notes = str(slide.get("speaker_notes", "") or "").strip()

    lines = [f"\\begin{{frame}}{{{title}}}"]
    if body_text:
        lines.append(sanitize_tex(body_text))
    if bullets:
        lines.append("\\begin{itemize}")
        for bullet in bullets:
            lines.append(f"  \\item {bullet}")
        lines.append("\\end{itemize}")
    if notes:
        lines.append(f"% Notes: {sanitize_tex(notes)}")
    lines.append("\\end{frame}")
    return "\n".join(lines)


def split_outline_item(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        slide = {
            "title": item.get("title", "Untitled Slide"),
            "bullets": list(item.get("bullets", []) or []),
        }
        if item.get("body"):
            slide["body"] = item["body"]
        if item.get("speaker_notes"):
            slide["speaker_notes"] = item["speaker_notes"]
        if item.get("section"):
            slide["section"] = item["section"]
        return slide
    return {"title": str(item), "bullets": []}


def build_slides(spec: dict[str, Any]) -> list[dict[str, Any]]:
    provided = [slide for slide in list(spec.get("slides", []) or []) if isinstance(slide, dict)]
    if provided:
        return provided

    outline = list(spec.get("content_outline", []) or [])
    if outline:
        return [split_outline_item(item) for item in outline]

    topic = str(spec.get("topic", "Academic Presentation"))
    audience = str(spec.get("audience", "General academic audience"))
    context = str(spec.get("context", "Academic presentation"))
    derived = list(spec.get("agent_derived_descriptions", []) or [])

    slides = [
        {
            "title": "Overview",
            "bullets": [
                f"Topic: {topic}",
                f"Context: {context}",
                f"Audience: {audience}",
            ],
            "section": "overview",
        },
        {
            "title": "Core Message",
            "bullets": [
                "State the main claim clearly.",
                "Add method or structure appropriate to the talk.",
                "Keep density aligned with the requested duration.",
            ],
            "section": "content",
        },
    ]
    if derived:
        slides.append(
            {
                "title": "Source-Derived Cues",
                "bullets": [str(item.get("summary", "")) for item in derived if str(item.get("summary", "")).strip()],
                "section": "content",
            }
        )
    slides.append(
        {
            "title": "Conclusion",
            "bullets": ["Summarize the contribution.", "End with the next question or action."],
            "section": "closing",
        }
    )
    return slides


def partition_slides(slides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current_name = ""
    current_slides: list[dict[str, Any]] = []

    for slide in slides:
        section_name = str(slide.get("section", "") or "content").strip() or "content"
        if section_name != current_name:
            if current_slides:
                sections.append({"name": current_name, "slides": current_slides})
            current_name = section_name
            current_slides = []
        current_slides.append(slide)

    if current_slides:
        sections.append({"name": current_name, "slides": current_slides})
    return sections


def render_preamble(spec: dict[str, Any], layout: str, section_inputs: str = "") -> str:
    template = load_template(layout)
    replacements = {
        "<THEME_DIRECTIVES>": theme_directives(str(spec.get("theme", "Berlin"))),
        "<TITLE>": sanitize_tex(str(spec.get("title") or spec.get("topic") or "Academic Presentation")),
        "<AUTHOR>": sanitize_tex(str(spec.get("author", "Author"))),
        "<INSTITUTE>": sanitize_tex(str(spec.get("institute", ""))),
        "<DATE>": str(spec.get("date", "\\today")),
        "<SECTIONS>": section_inputs.strip(),
    }
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    return rendered


def write_single_file(spec: dict[str, Any], output_dir: Path) -> None:
    slides = build_slides(spec)
    body = "\n\n".join(render_frame(slide) for slide in slides)
    main_tex = render_preamble(spec, layout="single_file") + "\n" + body + "\n\n\\end{document}\n"
    (output_dir / "main.tex").write_text(main_tex, encoding="utf-8")


def write_multi_file(spec: dict[str, Any], output_dir: Path) -> None:
    sections_dir = output_dir / "sections"
    sections_dir.mkdir(parents=True, exist_ok=True)
    section_inputs: list[str] = []

    for index, section in enumerate(partition_slides(build_slides(spec)), start=1):
        slug = slugify(str(section["name"]))
        filename = f"{index:02d}-{slug}.tex"
        section_body = "\n\n".join(render_frame(slide) for slide in list(section["slides"]))
        (sections_dir / filename).write_text(section_body + "\n", encoding="utf-8")
        section_inputs.append(f"\\input{{sections/{filename}}}")

    main_tex = render_preamble(spec, layout="multi_file", section_inputs="\n".join(section_inputs))
    main_tex += "\n\\end{document}\n"
    (output_dir / "main.tex").write_text(main_tex, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Beamer project from a normalized JSON spec.")
    parser.add_argument("--spec", required=True, help="Path to normalized JSON spec.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated Beamer project.")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    layout = infer_layout(spec)
    if layout == "multi_file":
        write_multi_file(spec, output_dir)
    else:
        write_single_file(spec, output_dir)


if __name__ == "__main__":
    main()
