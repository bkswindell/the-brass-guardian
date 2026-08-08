#!/usr/bin/env python3
"""Finalize Elias and Amelia profiles and their Clockwork Jungle canon links."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def insert_before_heading(text: str, heading: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = f"## {heading}\n"
    if marker not in text:
        raise RuntimeError(f"Missing heading: {heading}")
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def normalize_profile_links() -> None:
    replacements = {
        "characters/Professor_Elias_Hawthorne.md": {
            "[Aether Heart](../artifacts/008_The_Aether_Heart.md)": "[Aether Heart](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)",
        },
        "characters/Amelia_Hawthorne.md": {
            "../art/AH-1-008_Aether_Gauntlet_Exterior_Study.png": "../art/AH-1-004_The_Aether_Gauntlet-Exterior_Study.png",
            "../art/AH-1-010_Prototype_II_Cabinet_Photograph.png": "../art/AH-1-005_Prototype_II.png",
            "[Aether Heart](../artifacts/008_The_Aether_Heart.md)": "[Aether Heart](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)",
        },
        "historical_events/The_Clockwork_Jungle_Expedition.md": {
            "[Aether Heart](../artifacts/008_The_Aether_Heart.md)": "[Aether Heart](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)",
            "- [The Aether Heart](../artifacts/008_The_Aether_Heart.md), path and final catalog identity require repository review\n": "- The Aether Heart, currently documented visually within [The Aether Gauntlet: Exterior Study](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md); a dedicated artifact record may be created later\n",
        },
        "characters/Master_Gideon_Brasswell.md": {
            "[Aether Heart](../artifacts/008_The_Aether_Heart.md)": "[Aether Heart](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)",
        },
    }

    for path, mapping in replacements.items():
        target = ROOT / path
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        for old, new in mapping.items():
            text = text.replace(old, new)
        write(path, text)


def update_clockwork_jungle() -> None:
    path = "locations/The_Clockwork_Jungle.md"
    text = read(path)

    text = text.replace(
        "primary_connections: []",
        "primary_connections:\n  - Professor Elias Hawthorne\n  - Amelia Hawthorne\n  - The Clockwork Jungle Expedition\n  - Return to the Clockwork Jungle",
    )

    old_summary = (
        "The expedition region where [Amelia](../characters/Amelia_Hawthorne.md)'s arm was injured according to the supplied source. "
        "It contains living and mechanical wilderness, ancient structures, and dangers not yet fully reconciled with current canon."
    )
    new_summary = (
        "The Clockwork Jungle is the distant expedition region where living wilderness, mechanical growth, and Ancient structures exist together. "
        "It is the site of [the Clockwork Jungle Expedition](../historical_events/The_Clockwork_Jungle_Expedition.md), during which a dormant machine awakened, much of the expedition was destroyed, and [Amelia Hawthorne](../characters/Amelia_Hawthorne.md)'s right arm was catastrophically injured. "
        "The location remains a source-grounded placeholder because its geography, peoples, ecology, access rules, and full visual identity have not yet received a dedicated canon review."
    )
    text = text.replace(old_summary, new_summary)

    block = """## Historical and Narrative Connections

The series begins after the expedition disaster rather than opening with a complete depiction of it.

The location's history is owned by [The Clockwork Jungle Expedition](../historical_events/The_Clockwork_Jungle_Expedition.md). The future story that revisits the site is owned by [Return to the Clockwork Jungle](../story_arcs/The_Return_to_the_Clockwork_Jungle.md).

Earlier volumes should reveal the Jungle through aftermath, field records, damaged artifacts, incomplete memories, Ancient systems found in Aetherhaven, and [Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md)'s protective behavior.

The eventual return should show that the Jungle has not remained a static ruin waiting unchanged for the Hawthornes. Exact changes remain unresolved.
"""
    text = insert_before_heading(text, "Visual Continuity", block)

    if "- Preserve the aftermath-first narrative strategy" not in text:
        text = text.replace(
            "- Replace or expand this file rather than creating a duplicate profile later.",
            "- Replace or expand this file rather than creating a duplicate profile later.\n- Preserve the aftermath-first narrative strategy; do not use this location profile to reveal the complete expedition before the story earns it.\n- A later return may revise the accepted account without erasing the real harm suffered by Amelia and Elias.",
        )

    write(path, text)


def update_placeholder_index() -> None:
    path = "docs/development/docs/development/PLACEHOLDER_PROFILE_INDEX.md"
    lines = []
    for line in read(path).splitlines():
        if "characters/Professor_Elias_Hawthorne.md" in line:
            continue
        if "characters/Amelia_Hawthorne.md" in line:
            continue
        lines.append(line)
    write(path, "\n".join(lines))


def update_historical_index() -> None:
    path = "historical_events/README.md"
    text = read(path)
    row = "| [The Clockwork Jungle Expedition](The_Clockwork_Jungle_Expedition.md) | Canonical historical event | Elias Hawthorne, Amelia Hawthorne, Aether Gauntlet, Clockwork Jungle |"
    if row not in text:
        marker = "| [The Gearbreaker Standoff](The_Gearbreaker_Standoff.md) | Canonical historical event | Orin Flint, High Council, Brass Watch, Gearbreaker Mines |"
        if marker not in text:
            raise RuntimeError("Historical index insertion marker not found")
        text = text.replace(marker, marker + "\n" + row, 1)
    write(path, text)


def update_project_index() -> None:
    path = "docs/docs/PROJECT_INDEX.md"
    text = read(path)

    text = re.sub(
        r"- \*\*\d+\*\* completed canonical character profiles and \*\*\d+\*\* source-grounded character placeholders",
        "- **13** completed canonical character profiles and **15** source-grounded character placeholders",
        text,
        count=1,
    )
    text = re.sub(
        r"- \*\*\d+\*\* long-range or hidden story-arc profiles",
        "- **7** long-range or hidden story-arc profiles",
        text,
        count=1,
    )
    text = re.sub(
        r"- \*\*\d+\*\* historical-event records",
        "- **16** historical-event records",
        text,
        count=1,
    )

    character_rows = (
        "| [Professor Elias Hawthorne](characters/Professor_Elias_Hawthorne.md) | Engineer, explorer, father, keeper of the Wayfinder, and the Brass Guardian | Canonical working profile | [Professor_Elias_Hawthorne.md](characters/Professor_Elias_Hawthorne.md) |\n"
        "| [Amelia Hawthorne](characters/Amelia_Hawthorne.md) | The Clockwork Explorer, bearer of the Aether Gauntlet, and central protagonist | Canonical working profile | [Amelia_Hawthorne.md](characters/Amelia_Hawthorne.md) |\n"
    )
    if character_rows.strip() not in text:
        marker = "| [Orin Flint](characters/Orin_Flint.md) | Foreman of the Gearbreaker Mines and protector of its crews | Canonical working profile | [Orin_Flint.md](characters/Orin_Flint.md) |\n"
        if marker not in text:
            raise RuntimeError("Character index insertion marker not found")
        text = text.replace(marker, marker + character_rows, 1)

    arc_row = "| Return to the Clockwork Jungle | Amelia and Elias revisit the site of the expedition disaster and confront memory, evidence, guilt, and agency | Canonical future story arc concept | [The_Return_to_the_Clockwork_Jungle.md](story_arcs/The_Return_to_the_Clockwork_Jungle.md) |"
    if arc_row not in text:
        marker = "| The Watchman's Regret | Amelia's coming-of-age lesson through a veteran Watchman's account of the Gearbreaker Standoff | Canonical future story concept | [The_Watchmans_Regret.md](story_arcs/The_Watchmans_Regret.md) |"
        if marker not in text:
            raise RuntimeError("Story arc insertion marker not found")
        text = text.replace(marker, marker + "\n" + arc_row, 1)

    event_row = "| The Clockwork Jungle Expedition | Canonical historical event with restricted chronology | [The_Clockwork_Jungle_Expedition.md](historical_events/The_Clockwork_Jungle_Expedition.md) |"
    if event_row not in text:
        marker = "| The Gearbreaker Standoff | Canonical historical event | [The_Gearbreaker_Standoff.md](historical_events/The_Gearbreaker_Standoff.md) |"
        if marker not in text:
            raise RuntimeError("Historical event insertion marker not found")
        text = text.replace(marker, marker + "\n" + event_row, 1)

    # Remove stale placeholder-backlog bullets if present.
    lines = []
    for line in text.splitlines():
        if line.strip() in {
            "- [Professor Elias Hawthorne](characters/Professor_Elias_Hawthorne.md)",
            "- [Amelia Hawthorne](characters/Amelia_Hawthorne.md)",
        }:
            continue
        lines.append(line)
    write(path, "\n".join(lines))


def main() -> int:
    normalize_profile_links()
    update_clockwork_jungle()
    update_placeholder_index()
    update_historical_index()
    update_project_index()
    print("Finalized Elias and Amelia core profiles and Clockwork Jungle canon integration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
