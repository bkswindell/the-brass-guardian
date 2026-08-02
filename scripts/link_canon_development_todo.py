#!/usr/bin/env python3
"""Link the generated canon development queue from PROJECT_INDEX.md."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "PROJECT_INDEX.md"

ROW = "| [CANON_DEVELOPMENT_TODO.md](CANON_DEVELOPMENT_TODO.md) | Prioritized operational queue for profile expansion, image generation, artifact production, and repository QA |\n"
PARAGRAPH = "The complete prioritized work order, including status and direct links to every affected file, is maintained in [CANON_DEVELOPMENT_TODO.md](CANON_DEVELOPMENT_TODO.md).\n\n"


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")

    if ROW not in text:
        marker = "| [PLACEHOLDER_PROFILE_INDEX.md](PLACEHOLDER_PROFILE_INDEX.md) | Index of source-grounded placeholder records awaiting full development |\n"
        if marker in text:
            text = text.replace(marker, marker + ROW)
        else:
            marker = "| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Internal project inventory, canon index, audit notes, and development backlog |\n"
            text = text.replace(marker, marker + ROW)

    if PARAGRAPH not in text:
        marker = "## Placeholder Expansion Backlog\n\n"
        if marker in text:
            text = text.replace(marker, marker + PARAGRAPH)

    INDEX.write_text(text, encoding="utf-8")
    print("Linked CANON_DEVELOPMENT_TODO.md from PROJECT_INDEX.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
