#!/usr/bin/env python3
"""Normalize edge cases after the repository-wide Markdown link pass.

This script is intentionally conservative. It removes links from top-level file
headings, prevents source filenames and series titles from being interpreted as
entity references, and corrects known ambiguous names from earlier link passes.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIR_NAMES = {".git", ".github", "unused", "node_modules", "vendor"}
INLINE_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def markdown_files():
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIR_NAMES for part in path.relative_to(ROOT).parts):
            continue
        yield path


def rel(source: Path, target: str) -> str:
    return os.path.relpath(ROOT / target, source.parent).replace(os.sep, "/")


def normalize(path: Path, text: str) -> str:
    # These phrases are series or story titles as often as they are epithets. They
    # remain in the character profiles as titles but are removed from automatic
    # alias lists so prose titles are not mistaken for personal-name references.
    if path.as_posix().endswith("characters/Professor_Elias_Hawthorne.md"):
        text = text.replace("\n  - The Brass Guardian\n", "\n")
    if path.as_posix().endswith("characters/Amelia_Hawthorne.md"):
        text = text.replace("\n  - The Clockwork Explorer\n", "\n")

    lines = text.splitlines(keepends=True)
    output: list[str] = []

    for line in lines:
        # A file's own H1 is its identity, not a cross-reference. Removing links
        # here also prevents partial headings such as "The [Aetherhaven] Archives."
        if re.match(r"^#\s+", line):
            line = INLINE_LINK_RE.sub(lambda match: match.group(1), line)

        # Source filenames are evidence labels, not references to the city.
        line = re.sub(
            r"\[Aetherhaven\]\([^)]+/Aetherhaven\.md\)(?=(?:\s+v\d+(?:\.\d+)?)?\.pdf)",
            "Aetherhaven",
            line,
        )

        # The franchise and story titles are not references to Elias or Amelia.
        line = re.sub(
            r"\[The Brass Guardian\]\([^)]+Professor_Elias_Hawthorne\.md\)",
            "The Brass Guardian",
            line,
        )
        line = re.sub(
            r"\[The Clockwork Explorer\]\([^)]+Amelia_Hawthorne\.md\)",
            "The Clockwork Explorer",
            line,
        )

        output.append(line)

    normalized = "".join(output)

    # Earlier automatic linking matched the first name Beatrice to Inspector
    # Thorne inside the phrase "Euphemia and Beatrice Pike." Both Pike family
    # members now have dedicated placeholders, so correct the whole phrase.
    if path.as_posix().endswith("artifacts/021_Tamsin_Pikes_Brass_Key.md"):
        normalized = re.sub(
            r"(?:\[Euphemia\]\([^)]+\)|Euphemia) and \[Beatrice\]\([^)]+Chief_Inspector_Beatrice_Thorne\.md\) Pike",
            f"[Euphemia]({rel(path, 'characters/Euphemia_Pike.md')}) and [Beatrice Pike]({rel(path, 'characters/Beatrice_Pike.md')})",
            normalized,
        )

    return normalized


def main() -> int:
    changed: list[Path] = []
    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        updated = normalize(path, original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)

    print(f"Normalized {len(changed)} Markdown files.")
    for path in changed:
        print(f"  {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
