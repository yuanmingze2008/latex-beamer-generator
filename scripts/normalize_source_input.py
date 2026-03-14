from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TEXT_SUFFIXES = {".txt", ".md", ".tex", ".rst"}
ACADEMIC_DURATION_GUIDE = {
    5: (5, 7),
    10: (8, 12),
    15: (12, 16),
    20: (15, 20),
}
DEFAULT_THEME = "Berlin"


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def choose_mode(spec: dict[str, Any]) -> str:
    mode = str(spec.get("mode", "") or "").strip().lower()
    if mode in {"topic", "source_material"}:
        return mode
    has_sources = bool(spec.get("source_paths") or spec.get("source_text") or spec.get("agent_derived_descriptions"))
    return "source_material" if has_sources else "topic"


def suggest_slide_count(duration_minutes: int) -> tuple[int, str]:
    if duration_minutes <= 0:
        return 0, "unspecified"
    nearest = min(ACADEMIC_DURATION_GUIDE, key=lambda item: abs(item - duration_minutes))
    low, high = ACADEMIC_DURATION_GUIDE[nearest]
    return ((low + high) // 2), "agent_suggested"


def infer_layout(target_slide_count: int, explicit_mode: str) -> str:
    if explicit_mode in {"single_file", "multi_file"}:
        return explicit_mode
    return "multi_file" if target_slide_count > 15 else "single_file"


def normalize_descriptions(raw: list[Any]) -> list[dict[str, Any]]:
    descriptions: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if isinstance(item, dict):
            normalized = dict(item)
            normalized.setdefault("id", f"derived-{index}")
            normalized.setdefault("kind", "agent_description")
            normalized.setdefault("summary", "")
            descriptions.append(normalized)
        else:
            descriptions.append(
                {
                    "id": f"derived-{index}",
                    "kind": "agent_description",
                    "summary": str(item),
                }
            )
    return descriptions


def normalize(spec: dict[str, Any]) -> dict[str, Any]:
    mode = choose_mode(spec)
    source_paths = [Path(p) for p in spec.get("source_paths", [])]
    source_text = str(spec.get("source_text", "") or "").strip()
    derived = normalize_descriptions(list(spec.get("agent_derived_descriptions", []) or []))

    extracted_texts: list[dict[str, str]] = []
    ignored_paths: list[str] = []
    missing_paths: list[str] = []

    for path in source_paths:
        if not path.exists():
            missing_paths.append(str(path))
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            extracted_texts.append({"path": str(path), "text": read_text_file(path)})
        else:
            ignored_paths.append(str(path))

    duration_minutes = int(spec.get("duration_minutes", 0) or 0)
    target_slide_count = int(spec.get("target_slide_count", 0) or 0)
    slide_count_source = str(spec.get("slide_count_source", "") or "").strip() or "unspecified"
    if target_slide_count <= 0:
        target_slide_count, slide_count_source = suggest_slide_count(duration_minutes)

    output_layout_mode = infer_layout(
        target_slide_count=target_slide_count,
        explicit_mode=str(spec.get("output_layout_mode", "") or "").strip().lower(),
    )

    combined_source_text = "\n\n".join(
        part for part in [source_text, *[item["text"].strip() for item in extracted_texts if item["text"].strip()]] if part
    )

    return {
        **spec,
        "mode": mode,
        "theme": spec.get("theme") or DEFAULT_THEME,
        "source_text": source_text,
        "combined_source_text": combined_source_text,
        "extracted_texts": extracted_texts,
        "ignored_source_paths": ignored_paths,
        "missing_source_paths": missing_paths,
        "agent_derived_descriptions": derived,
        "target_slide_count": target_slide_count,
        "slide_count_source": slide_count_source,
        "output_layout_mode": output_layout_mode,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize source inputs for the beamer skill.")
    parser.add_argument("--spec", required=True, help="Path to an input JSON spec.")
    parser.add_argument("--output", required=True, help="Path to the normalized JSON spec.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    output_path = Path(args.output)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    normalized = normalize(spec)
    output_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
