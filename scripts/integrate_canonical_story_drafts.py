#!/usr/bin/env python3
"""Integrate canonical prose drafts into the active canon index and standards."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_INDEX = ROOT / "docs/docs/PROJECT_INDEX.md"
STANDARD = ROOT / "docs/standards/docs/standards/CANON_MARKDOWN_STANDARD.md"
KEEPER_ARC = ROOT / "story_arcs" / "The_Keeper_of_Dreams.md"

PRINCESS_PATH = "story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md"
EXPLORER_PATH = "story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md"


def save(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def insert_before(text: str, heading: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = f"## {heading}\n"
    if marker not in text:
        raise RuntimeError(f"Missing heading: {heading}")
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def update_project_index() -> None:
    text = PROJECT_INDEX.read_text(encoding="utf-8")

    snapshot_line = "- **2** canonical prose story drafts in `story_drafts/`"
    if snapshot_line not in text:
        marker = "- **7** long-range or hidden story-arc profiles"
        if marker not in text:
            raise RuntimeError("Story arc snapshot marker not found")
        text = text.replace(marker, snapshot_line + "\n" + marker, 1)

    text = text.replace(
        "Canonical Markdown profiles in `characters/`, `organizations/`, `locations/`, `historical_events/`, and `story_arcs/`.",
        "Canonical Markdown profiles and prose drafts in `characters/`, `organizations/`, `locations/`, `historical_events/`, `story_arcs/`, and `story_drafts/`.",
    )

    root_row = "| [story_drafts/README.md](story_drafts/README.md) | Index, canon rules, and Book One placement strategy for active prose story drafts |"
    if root_row not in text:
        marker = "| [templates/templates/Story_Arc_Profile_Template.md](templates/templates/Story_Arc_Profile_Template.md) | Standard structure for story-arc records |"
        if marker not in text:
            raise RuntimeError("Root project file marker not found")
        text = text.replace(marker, root_row + "\n" + marker, 1)

    block = """## Canonical Story Drafts

Story drafts contain active narrative prose. Their working titles and wording may be revised, but their canonical character relationships, events, emotional truths, and opening-role decisions remain authoritative unless explicitly changed.

See the [Canonical Story Drafts Index](story_drafts/README.md).

| Working title | Intended role | Canon status | File |
|---|---|---|---|
| *The Brass Guardian and the Clockwork Princess — A Bedtime Adventure for Amelia* | Preface, illustrated teaser, or short opening vignette introducing wonder, kindness, and the Hawthornes' bond | Canonical story draft; working title | [The_Brass_Guardian_and_the_Clockwork_Princess.md](story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md) |
| *The Brass Guardian and the Clockwork Explorer — A Day Aboard the Wayfinder* | Potential opening story or first full chapter establishing ordinary life aboard the *Wayfinder* | Canonical story draft; working title | [The_Brass_Guardian_and_the_Clockwork_Explorer.md](story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md) |
"""
    text = insert_before(text, "Canonical Story Arcs", block)
    save(PROJECT_INDEX, text)


def update_standard() -> None:
    text = STANDARD.read_text(encoding="utf-8")

    text = text.replace(
        "2. Canonical Markdown profiles and artifact files.",
        "2. Canonical Markdown profiles, story drafts, and artifact files.",
    )

    block = """### Story Drafts

- Story prose belongs in `story_drafts/`; long-range plotting and reveal planning belong in `story_arcs/`.
- A file marked **Canonical story draft** is authoritative for its character relationships, events, emotional truth, and explicitly stated continuity even while the title and wording remain under revision.
- Preserve the current full prose before making structural revisions.
- Separate exact draft text from editorial notes, continuity notes, placement options, and unresolved terminology.
- Working titles may change without changing the story's canonical status.
- Do not treat every fairy-tale explanation, metaphor, remembered detail, or narrator simplification as settled technical lore when the draft explicitly preserves that ambiguity.
- Opening stories should avoid premature exposition when their purpose is to establish present-day character attachment, wonder, domestic life, or tone.
- Link the draft to the character, location, artifact, historical-event, and story-arc records that own its deeper continuity.
"""
    text = insert_before(text, "Story Arcs", block)
    save(STANDARD, text)


def update_keeper_arc() -> None:
    text = KEEPER_ARC.read_text(encoding="utf-8")

    if "related_story_drafts:" not in text:
        marker = "primary_artifacts:\n"
        if marker not in text:
            raise RuntimeError("Keeper arc primary_artifacts marker not found")
        insertion = "related_story_drafts:\n  - ../story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md\n"
        text = text.replace(marker, insertion + marker, 1)

    old = "The early bedtime adventure presents the Keeper of Dreams as a luminous figure who asks [Amelia](../characters/Amelia_Hawthorne.md) and [Elias](../characters/Professor_Elias_Hawthorne.md) to restore [the Moon Garden](../locations/The_Moon_Garden.md) and Dream Engine."
    new = "The canonical story draft [*The Brass Guardian and the Clockwork Princess — A Bedtime Adventure for Amelia*](../story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md) presents the Keeper of Dreams as a luminous figure who asks [Amelia](../characters/Amelia_Hawthorne.md) and [Elias](../characters/Professor_Elias_Hawthorne.md) to restore [the Moon Garden](../locations/The_Moon_Garden.md) and Dream Engine."
    text = text.replace(old, new)

    save(KEEPER_ARC, text)


def update_existing_title_references() -> None:
    link = "[*The Brass Guardian and the Clockwork Princess*](../story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md)"
    for path in (ROOT / "characters").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = text.replace("*The Brass Guardian and the Clockwork Princess*", link)
        if updated != text:
            save(path, updated)


def main() -> int:
    for required in (ROOT / PRINCESS_PATH, ROOT / EXPLORER_PATH):
        if not required.exists():
            raise RuntimeError(f"Missing canonical story draft: {required}")

    update_project_index()
    update_standard()
    update_keeper_arc()
    update_existing_title_references()
    print("Integrated two canonical story drafts into project indexes and continuity standards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
