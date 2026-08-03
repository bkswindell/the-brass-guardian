#!/usr/bin/env python3
"""Add PDF-verified cover and inline artwork references to canonical story drafts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRINCESS = ROOT / "story_drafts" / "The_Brass_Guardian_and_the_Clockwork_Princess.md"
EXPLORER = ROOT / "story_drafts" / "The_Brass_Guardian_and_the_Clockwork_Explorer.md"


def save(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def insert_after(text: str, anchor: str, block: str) -> str:
    if block.strip() in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"Missing artwork placement anchor: {anchor!r}")
    return text.replace(anchor, anchor + "\n\n" + block.strip(), 1)


def insert_after_story_text(text: str, anchor: str, block: str) -> str:
    """Insert artwork only inside the prose section, never in YAML metadata."""
    marker = "## Current Draft Text\n"
    if marker not in text:
        raise RuntimeError("Current Draft Text heading not found")
    prefix, story = text.split(marker, 1)
    if block.strip() in story:
        return text
    if anchor not in story:
        raise RuntimeError(f"Missing story artwork placement anchor: {anchor!r}")
    story = story.replace(anchor, anchor + "\n\n" + block.strip(), 1)
    return prefix + marker + story


def set_yaml_artwork(text: str, block: str) -> str:
    """Replace or add the entire artwork block so reruns remain deterministic."""
    canonical = "\n" + block.rstrip() + "\n"
    pattern = re.compile(r"\nartwork:\n.*?(?=\n---\n)", re.DOTALL)
    if pattern.search(text):
        return pattern.sub(canonical.rstrip("\n"), text, count=1)

    marker = "last_updated: 2026-08-03\n"
    if marker not in text:
        raise RuntimeError("Story draft last_updated marker not found")
    return text.replace(marker, marker + block.rstrip() + "\n", 1)


def update_princess() -> None:
    text = PRINCESS.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "source_basis:\n  - Aetherhaven v3.pdf, pages 5-7",
        "source_basis:\n  - The_Brass_Guardian.pdf",
    )

    text = set_yaml_artwork(
        text,
        """artwork:
  cover_image: ../art/Clockwork_Gardens_at_Night.png""",
    )

    cover = "![Cover illustration for *The Brass Guardian and the Clockwork Princess*](../art/Clockwork_Gardens_at_Night.png)"
    status = "> **Canonical story draft with a working title.** The story's emotional events, character bond, and role as an early invitation into the series are canon. The final title, exact Book One placement, and some fairy-tale explanatory language remain open to revision."
    text = insert_after(text, status, cover)

    checklist_anchor = "- [x] Link the Keeper of Dreams continuity."
    checklist_item = "- [x] Add the PDF cover artwork reference."
    if checklist_item not in text:
        text = replace_once(text, checklist_anchor, checklist_anchor + "\n" + checklist_item)

    save(PRINCESS, text)


def update_explorer() -> None:
    text = EXPLORER.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "source_basis:\n  - Aetherhaven v3.pdf, pages 9-13",
        "source_basis:\n  - The_Brass_Guardian.pdf",
    )

    text = set_yaml_artwork(
        text,
        """artwork:
  cover_image: ../art/Wayfinder_Above_the_Clouds.png
  inline_images:
    - placement: after \"Professor Elias Hawthorne always woke before the sun.\"
      file: ../art/Brass Dreams Above the Clouds.png
    - placement: after \"Which somehow made Amelia love it even more.\"
      file: ../art/Clockwork Workshop in the Sky.png
    - placement: after \"Dinner was vegetable soup with warm bread.\"
      file: ../art/Steampunk Airship Galley Feast.png
    - placement: after the final Heart Engine hum
      file: ../art/Guardians Over the Brass City.png""",
    )

    cover = "![Cover illustration for *The Brass Guardian and the Clockwork Explorer*](../art/Wayfinder_Above_the_Clouds.png)"
    status = "> **Canonical story draft with a working title.** The day-to-day relationship, domestic routines, tone, and present-day characterization are canon. Final Book One placement and a small number of technical terms remain open to revision."
    text = insert_after(text, status, cover)

    # Correct the earlier mistaken mid-story assignment if it appears in any
    # generated or manually edited copy.
    text = text.replace(
        "Which somehow made Amelia love it even more.\n\n![Guardians Over the Brass City](../art/Guardians%20Over%20the%20Brass%20City.png)",
        "Which somehow made Amelia love it even more.\n\n![Clockwork Workshop in the Sky](../art/Clockwork%20Workshop%20in%20the%20Sky.png)",
    )

    text = insert_after_story_text(
        text,
        "Professor Elias Hawthorne always woke before the sun.",
        "![Brass Dreams Above the Clouds](../art/Brass%20Dreams%20Above%20the%20Clouds.png)",
    )
    text = insert_after_story_text(
        text,
        "Which somehow made Amelia love it even more.",
        "![Clockwork Workshop in the Sky](../art/Clockwork%20Workshop%20in%20the%20Sky.png)",
    )
    text = insert_after_story_text(
        text,
        "Dinner was vegetable soup with warm bread.",
        "![Steampunk Airship Galley Feast](../art/Steampunk%20Airship%20Galley%20Feast.png)",
    )
    text = insert_after_story_text(
        text,
        "The Heart Engine gave one soft, happy hum.\n\n“Hmmmm...”",
        "![Guardians Over the Brass City](../art/Guardians%20Over%20the%20Brass%20City.png)",
    )

    checklist_anchor = "- [x] Establish ordinary Wayfinder life as meaningful canon."
    checklist_item = "- [x] Add the PDF cover and four inline artwork references, including the omitted galley image."
    if checklist_item not in text:
        text = replace_once(text, checklist_anchor, checklist_anchor + "\n" + checklist_item)

    save(EXPLORER, text)


def main() -> int:
    update_princess()
    update_explorer()
    print("Added PDF-verified artwork references to both canonical story drafts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
