#!/usr/bin/env python3
"""Validate media-reaction Markdown without altering immutable source formatting.

Markdown hard line breaks use two trailing spaces. Those spaces are allowed
inside the immutable public-reaction source block because the transcript's
source formatting must be preserved exactly. Editorial metadata and analysis
outside the source block must remain free of trailing whitespace.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media_reactions"
START = "<!-- SOURCE CONTENT START: IMMUTABLE PUBLIC REACTION -->"
END = "<!-- SOURCE CONTENT END: IMMUTABLE PUBLIC REACTION -->"


def main() -> int:
    errors: list[str] = []

    for path in sorted(MEDIA.glob("*.md")):
        if path.name in {"README.md", "AUDIENCE_RESPONSE_SYNTHESIS.md"}:
            in_source = False
        else:
            in_source = False

        start_count = 0
        end_count = 0

        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8").splitlines(keepends=True), start=1
        ):
            line = raw_line.rstrip("\r\n")

            if line == START:
                start_count += 1
                in_source = True
                continue

            if line == END:
                end_count += 1
                in_source = False
                continue

            if not in_source and line != line.rstrip(" \t"):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: "
                    "trailing whitespace outside immutable source block"
                )

        if start_count != end_count:
            errors.append(
                f"{path.relative_to(ROOT)}: unbalanced immutable source markers "
                f"({start_count} start, {end_count} end)"
            )

        if start_count > 1 or end_count > 1:
            errors.append(
                f"{path.relative_to(ROOT)}: expected at most one immutable source block"
            )

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Media-reaction Markdown formatting is valid; immutable source spacing preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
