#!/usr/bin/env python3
"""Finalize indexes and minor link cleanup after the historical-event migration."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update_orin() -> None:
    path = ROOT / "characters/Orin_Flint.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("[Orin Flint](Orin_Flint.md) is the veteran", "Orin Flint is the veteran")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_placeholder_index() -> None:
    path = ROOT / "PLACEHOLDER_PROFILE_INDEX.md"
    text = path.read_text(encoding="utf-8")
    lines = [
        line for line in text.splitlines()
        if "characters/Master_Gideon_Brasswell.md" not in line
        and "characters/Orin_Flint.md" not in line
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_project_index() -> None:
    path = ROOT / "PROJECT_INDEX.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- **9** completed canonical character profiles and **19** source-grounded character placeholders",
        "- **11** completed canonical character profiles and **17** source-grounded character placeholders",
    )
    text = text.replace(
        "- **5** profile templates and development standards",
        "- **6** profile templates and development standards",
    )
    text = text.replace(
        "Canonical Markdown profiles in `characters/`, `organizations/`, `locations/`, and `story_arcs/`.",
        "Canonical Markdown profiles in `characters/`, `organizations/`, `locations/`, `historical_events/`, and `story_arcs/`.",
    )

    character_marker = "| [The Passenger of Dock Zero](characters/The_Passenger_of_Dock_Zero.md) | [Unverified Morningstar passenger](characters/The_Passenger_of_Dock_Zero.md) | Canonical working profile | [The_Passenger_of_Dock_Zero.md](characters/The_Passenger_of_Dock_Zero.md) |\n"
    character_rows = (
        "| [Master Gideon Brasswell](characters/Master_Gideon_Brasswell.md) | Keeper of the Engine Complex and former master to Elias Hawthorne | Canonical working profile | [Master_Gideon_Brasswell.md](characters/Master_Gideon_Brasswell.md) |\n"
        "| [Orin Flint](characters/Orin_Flint.md) | Foreman of the Gearbreaker Mines and protector of its crews | Canonical working profile | [Orin_Flint.md](characters/Orin_Flint.md) |\n"
    )
    if character_rows not in text and character_marker in text:
        text = text.replace(character_marker, character_marker + character_rows)

    arc_marker = "| The Thirteenth Chair | [High Council](organizations/The_High_Council_of_Aetherhaven.md), [First Mechanist](characters/The_First_Mechanist.md), Continuance, and constitutional authority | Canonical long-range arc | [The_Thirteenth_Chair.md](story_arcs/The_Thirteenth_Chair.md) |\n"
    arc_row = "| The Watchman's Regret | Amelia's coming-of-age lesson through a veteran Watchman's account of the Gearbreaker Standoff | Canonical future story concept | [The_Watchmans_Regret.md](story_arcs/The_Watchmans_Regret.md) |\n"
    if arc_row not in text and arc_marker in text:
        text = text.replace(arc_marker, arc_marker + arc_row)

    text = "\n".join(
        line for line in text.splitlines()
        if "[Master Gideon Brasswell](characters/Master_Gideon_Brasswell.md)" not in line
        or "Canonical working profile" in line
        if True
    )
    # The comprehension above preserves the canonical row and removes stale backlog
    # bullets only when they do not identify a canonical table entry.
    lines = []
    for line in text.splitlines():
        if line.strip() == "- [Master Gideon Brasswell](characters/Master_Gideon_Brasswell.md)":
            continue
        if line.strip() == "- [Orin Flint](characters/Orin_Flint.md)":
            continue
        lines.append(line)
    text = "\n".join(lines)

    text = text.replace(
        "The artifact Markdown file owns the artifact concept. Broader history remains in the linked canon profiles.",
        "The artifact Markdown file owns the artifact concept and provenance. Historical-event records own complete event chronology; character, organization, location, and story-arc files link to that history rather than duplicating it.",
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    marker = "- canonical character, organization, location, and story-arc profiles,\n"
    replacement = "- canonical character, organization, location, historical-event, and story-arc profiles,\n"
    text = text.replace(marker, replacement)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    update_orin()
    update_placeholder_index()
    update_project_index()
    update_readme()
    print("Finalized historical-event migration indexes and links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
