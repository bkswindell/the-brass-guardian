#!/usr/bin/env python3
"""Disambiguate shorthand for Aetherhaven's two organizations named Order.

Canonical usage:
- The Order of the Mended Hand is normally shortened to "the Hand."
- The Order of the Closed Eye is normally called by its full name or
  "the Closed Eye" in canon prose.
- Bare "the Order" is reserved for clearly established Closed Eye internal
  speech or restricted records and is never the default name for the Hand.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENDED = ROOT / "organizations" / "The_Order_of_the_Mended_Hand.md"
CLOSED = ROOT / "organizations" / "The_Order_of_the_Closed_Eye.md"
STANDARD = ROOT / "docs/standards/docs/standards/CANON_MARKDOWN_STANDARD.md"


def save(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_section(text: str, heading: str, body: str) -> str:
    block = f"## {heading}\n\n{body.strip()}\n\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text)
    raise RuntimeError(f"Missing section: {heading}")


def insert_before(text: str, marker_heading: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = f"## {marker_heading}\n"
    if marker not in text:
        raise RuntimeError(f"Missing insertion heading: {marker_heading}")
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def hand_shorthand(text: str) -> str:
    """Replace bare Order shorthand while preserving formal organization names."""
    tokens = {
        "The Order of the Mended Hand": "__FORMAL_MENDED_HAND__",
        "the Order of the Mended Hand": "__LOWER_FORMAL_MENDED_HAND__",
        "Order of the Mended Hand": "__NO_ARTICLE_MENDED_HAND__",
        "The Order of the Closed Eye": "__FORMAL_CLOSED_EYE__",
        "the Order of the Closed Eye": "__LOWER_FORMAL_CLOSED_EYE__",
        "Order of the Closed Eye": "__NO_ARTICLE_CLOSED_EYE__",
    }
    for phrase, token in tokens.items():
        text = text.replace(phrase, token)

    text = re.sub(r"\bThe Order's\b", "The Hand's", text)
    text = re.sub(r"\bthe Order's\b", "the Hand's", text)
    text = re.sub(r"\bOrder's\b", "Hand's", text)
    text = re.sub(r"\bThe Order\b", "The Hand", text)
    text = re.sub(r"\bthe Order\b", "the Hand", text)
    text = re.sub(r"\bOrder\b", "Hand", text)

    for phrase, token in tokens.items():
        text = text.replace(token, phrase)
    return text


def closed_eye_shorthand(text: str) -> str:
    """Prefer Closed Eye wording while preserving the formal name."""
    tokens = {
        "The Order of the Closed Eye": "__FORMAL_CLOSED_EYE__",
        "the Order of the Closed Eye": "__LOWER_FORMAL_CLOSED_EYE__",
        "Order of the Closed Eye": "__NO_ARTICLE_CLOSED_EYE__",
        "The Order of the Mended Hand": "__FORMAL_MENDED_HAND__",
        "the Order of the Mended Hand": "__LOWER_FORMAL_MENDED_HAND__",
        "Order of the Mended Hand": "__NO_ARTICLE_MENDED_HAND__",
    }
    for phrase, token in tokens.items():
        text = text.replace(phrase, token)

    text = re.sub(r"\bThe Order's\b", "The Closed Eye's", text)
    text = re.sub(r"\bthe Order's\b", "the Closed Eye's", text)
    text = re.sub(r"\bOrder's\b", "Closed Eye's", text)
    text = re.sub(r"\bThe Order\b", "The Closed Eye", text)
    text = re.sub(r"\bthe Order\b", "the Closed Eye", text)
    text = re.sub(r"\bOrder\b", "Closed Eye", text)

    for phrase, token in tokens.items():
        text = text.replace(token, phrase)
    return text


def refine_mended_hand() -> None:
    text = MENDED.read_text(encoding="utf-8")
    text = hand_shorthand(text)

    text = re.sub(
        r"^aliases:\n(?:  - .*\n)+",
        "aliases:\n  - The Mended Hand\n  - The Hand\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    body = """
The formal name is **The Order of the Mended Hand**.

Its normal public and conversational shorthand is **the Hand**.

Typical usage:

- Formal documents, introductions, charters, and the first clear reference use **the Order of the Mended Hand**.
- Ordinary citizens, patients, Watch officers, explorers, and most members usually say **the Hand**.
- Facilities may be described as Hand halls, Hand houses, Hand clinics, or houses and clinics operated by the Hand until their individual names are established.
- **The Order** is not the preferred standalone shorthand for the Mended Hand in narration, repository prose, or ordinary dialogue.

The distinction is necessary because [the Order of the Closed Eye](The_Order_of_the_Closed_Eye.md) is a separate secret organization. Using **the Hand** keeps the public hospitaller order distinct from the hidden Closed Eye.

A person may say:

> **Take them to the Hand.**

Another may answer:

> **Not unless there is no other choice.**

The word **Order** in the formal name reflects the Mended Hand's age, chartered privileges, dispersed houses, field service, internal loyalties, and semi-autonomous authority. It does not make every member a knight, soldier, or moral exemplar. Exact ranks, vows, chapters, and the founding Rule remain unresolved.
"""
    text = replace_section(text, "Name and Common Usage", body)
    save(MENDED, text)


def refine_closed_eye() -> None:
    text = CLOSED.read_text(encoding="utf-8")
    text = closed_eye_shorthand(text)

    text = re.sub(
        r"^aliases:\n(?:  - .*\n)+",
        "aliases:\n  - The Closed Eye\n  - The Order, internal or restricted shorthand only\n  - The Keepers of Closure\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    body = """
The formal name is **The Order of the Closed Eye**.

In canon narration, summaries, and cross-organization references, use either the full name or **the Closed Eye**.

Bare **the Order** is permitted only when:

- members of the Closed Eye are speaking among themselves;
- a restricted record has already established the subject unmistakably;
- or a scene deliberately uses the vague title to conceal the organization's identity.

Bare **the Order** must not be used in a passage that also discusses [the Order of the Mended Hand](The_Order_of_the_Mended_Hand.md) unless the intended organization is explicitly restated. The public medical organization is normally called **the Hand**.

Ordinary citizens do not generally recognize **the Order** as a reference to the Closed Eye because the Closed Eye is officially unacknowledged.
"""
    block = f"## Naming and Reference Convention\n\n{body.strip()}\n"
    if "## Naming and Reference Convention" in text:
        text = replace_section(text, "Naming and Reference Convention", body)
    else:
        text = insert_before(text, "Core Doctrine", block)

    save(CLOSED, text)


def refine_linked_sections() -> None:
    """Use Hand shorthand inside sections specifically about the Mended Hand."""
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "unused" in path.parts:
            continue
        if path in {MENDED, CLOSED, STANDARD}:
            continue

        text = path.read_text(encoding="utf-8")
        pattern = re.compile(
            r"(^##[^\n]*(?:Order of the Mended Hand|Mended Hand)[^\n]*\n.*?)(?=^##\s+|\Z)",
            re.MULTILINE | re.DOTALL,
        )

        updated = pattern.sub(lambda m: hand_shorthand(m.group(1)), text)
        if updated != text:
            save(path, updated)


def refine_standard() -> None:
    text = STANDARD.read_text(encoding="utf-8")
    heading = "## Organization Naming Collision Rule"
    body = """
Aetherhaven contains two distinct organizations whose formal names begin with **Order**:

- [The Order of the Mended Hand](organizations/The_Order_of_the_Mended_Hand.md) is a public, highly visible hospitaller and medical organization. Its normal shorthand is **the Hand**.
- [The Order of the Closed Eye](organizations/The_Order_of_the_Closed_Eye.md) is a secret containment organization. Canon prose normally uses **the Closed Eye** or its full name.

Do not use bare **the Order** as shorthand for the Mended Hand.

Bare **the Order** may refer to the Closed Eye only in clearly established internal speech, restricted records, or deliberately obscured dialogue. Never use bare **the Order** where both organizations appear in the same passage.

On first meaningful reference in a file or scene, use the appropriate full formal name before using its approved shorthand.
"""
    block = f"{heading}\n\n{body.strip()}\n"

    if heading in text:
        text = replace_section(text, "Organization Naming Collision Rule", body)
    else:
        text = insert_before(text, "Hyperlinking Rule", block)

    save(STANDARD, text)


def main() -> int:
    refine_mended_hand()
    refine_closed_eye()
    refine_linked_sections()
    refine_standard()
    print("Clarified shorthand for the Mended Hand and Closed Eye.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
