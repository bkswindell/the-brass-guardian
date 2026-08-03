#!/usr/bin/env python3
"""Polish grammar introduced by deterministic Order shorthand normalization."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "an Hand": "a Hand",
    "An Hand": "A Hand",
    "an Closed Eye": "a Closed Eye",
    "An Closed Eye": "A Closed Eye",
    "Hand advice is respected": "Advice from the Hand is respected",
    "does not accept a Hand title as proof of wisdom or morality": "does not accept Hand rank or credentials as proof of wisdom or morality",
}


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "unused" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in REPLACEMENTS.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated.rstrip() + "\n", encoding="utf-8")
            changed += 1
    print(f"Polished Order shorthand grammar in {changed} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
