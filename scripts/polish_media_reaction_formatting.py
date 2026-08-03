#!/usr/bin/env python3
"""Normalize generated media-reaction metadata without touching immutable sources."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media_reactions"
SOURCE_START = "<!-- SOURCE CONTENT START: IMMUTABLE PUBLIC REACTION -->"

REACTION_FILES = [
    "An_Introduction_to_Aetherhaven.md",
    "How_Kindness_Powers_Aetherhaven’s_Heart_Engine.md",
    "Aetherhaven_and_the_Heart_Engine.md",
    "Who_Rules_Aetherhaven_s_Heart_Engine.md",
    "Policing_the_Lost_Seconds_of_Aetherhaven.md",
    "Who_Really_Drives_Your_Mechanical_Hand.md",
]


def clean_generated_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("        "):
            line = line[8:]
        lines.append(line.rstrip())
    return "\n".join(lines)


def clean_reaction(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    marker = SOURCE_START + "\n"
    if marker not in text:
        raise RuntimeError(f"Missing immutable source marker in {path.name}")

    prefix, source = text.split(marker, 1)
    cleaned = clean_generated_lines(prefix).rstrip() + "\n\n" + marker + source
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")


def clean_generated_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    cleaned = clean_generated_lines(text).rstrip() + "\n"
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")


def main() -> int:
    for filename in REACTION_FILES:
        clean_reaction(MEDIA / filename)

    clean_generated_file(MEDIA / "README.md")
    clean_generated_file(MEDIA / "AUDIENCE_RESPONSE_SYNTHESIS.md")
    print("Polished generated media-reaction formatting without changing source transcripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
