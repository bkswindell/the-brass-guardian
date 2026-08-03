#!/usr/bin/env python3
"""Validate media-reaction Markdown without altering immutable source formatting.

Markdown hard line breaks use two trailing spaces. Those spaces are allowed
inside the immutable public-reaction source block because the transcript's
source formatting must be preserved exactly. Editorial metadata and analysis
outside the source block must remain free of trailing whitespace.

The closing source marker may immediately follow the final transcript sentence;
that pre-existing layout is recognized without rewriting the source block.
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
        in_source = False
        start_count = 0
        end_count = 0

        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8").splitlines(keepends=True), start=1
        ):
            line = raw_line.rstrip("\r\n")
            line_started_in_source = in_source

            if START in line:
                start_count += line.count(START)
                in_source = True

            if END in line:
                end_count += line.count(END)
                in_source = False

            # Marker-bearing lines may contain source text before or after the
            # marker. Do not apply editorial whitespace rules to those lines.
            if START in line or END in line:
                continue

            if not line_started_in_source and not in_source:
                if line != line.rstrip(" \t"):
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
