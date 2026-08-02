#!/usr/bin/env python3
"""Update PROJECT_INDEX.md after generating the placeholder profile library."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "PROJECT_INDEX.md"

SNAPSHOT = """The repository currently contains:

- **9** completed canonical character profiles and **19** source-grounded character placeholders
- **12** completed canonical organization profiles and **23** source-grounded organization placeholders
- **5** completed canonical location profiles and **48** source-grounded location placeholders
- **5** long-range or hidden story-arc profiles
- **64** artifact image-slate records
- **5** profile templates and development standards
- **2** compiled manuscript exports (`DOCX` and `PDF`)
- an active artwork library in `art/`
- a complete [placeholder profile index](PLACEHOLDER_PROFILE_INDEX.md)
"""

BACKLOG = """## Placeholder Expansion Backlog

Every currently identified person, organization, and location now has a dedicated Markdown record. Completed profiles remain authoritative. Files marked **Source-grounded placeholder** preserve the supplied PDF/DOCX material and current Markdown references until they receive full development.

The central protagonists now have dedicated placeholders:

- [Professor Elias Hawthorne](characters/Professor_Elias_Hawthorne.md)
- [Amelia Hawthorne](characters/Amelia_Hawthorne.md)

Their placeholders deliberately preserve unresolved source details instead of forcing a premature final synthesis.

Other character placeholders include:

- [Doctor Elara Quill](characters/Doctor_Elara_Quill.md)
- [Master Gideon Brasswell](characters/Master_Gideon_Brasswell.md)
- [Orin Flint](characters/Orin_Flint.md)
- [Lucian Wren](characters/Lucian_Wren.md)
- [Barnaby Wren](characters/Barnaby_Wren.md)
- [Madame Celestine Mirrow](characters/Madame_Celestine_Mirrow.md)
- [Keeper Thirteen](characters/Keeper_Thirteen.md)
- [The First Mechanist](characters/The_First_Mechanist.md)
- [The Lady in the Water](characters/The_Lady_in_the_Water.md)
- [The Ashen Cartographer](characters/The_Ashen_Cartographer.md)
- [The Null Shepherd](characters/The_Null_Shepherd.md)
- [The Bellmaker](characters/The_Bellmaker.md)

Organization and location placeholders—including all missing numbered and restricted map locations—are catalogued in [PLACEHOLDER_PROFILE_INDEX.md](PLACEHOLDER_PROFILE_INDEX.md).

The next development phase is to replace placeholders with complete profiles as each subject becomes story-relevant. Expansion should preserve source notes, explicitly resolve contradictions, and retain existing file paths so inbound links remain stable.

"""


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")

    text = re.sub(
        r"The repository currently contains:\n\n.*?\n\n## Canon Authority",
        SNAPSHOT.rstrip() + "\n\n## Canon Authority",
        text,
        flags=re.DOTALL,
    )

    if "[PLACEHOLDER_PROFILE_INDEX.md](PLACEHOLDER_PROFILE_INDEX.md)" not in text:
        marker = "| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Internal project inventory, canon index, audit notes, and development backlog |\n"
        addition = marker + "| [PLACEHOLDER_PROFILE_INDEX.md](PLACEHOLDER_PROFILE_INDEX.md) | Index of source-grounded placeholder records awaiting full development |\n"
        text = text.replace(marker, addition)

    text = re.sub(
        r"## Development Backlog\n.*?(?=## Audit Findings)",
        BACKLOG,
        text,
        flags=re.DOTALL,
    )

    text = text.replace(
        "8. [Amelia](characters/Amelia_Hawthorne.md) and [Elias Hawthorne](characters/Professor_Elias_Hawthorne.md) are intentionally deferred until the surrounding canon is substantially complete.",
        "8. Amelia and Elias Hawthorne now have source-grounded placeholder profiles. Their full synthesis remains intentionally deferred until the surrounding canon is substantially complete.",
    )

    INDEX.write_text(text, encoding="utf-8")
    print("Updated PROJECT_INDEX.md for the placeholder profile library.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
