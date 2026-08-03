#!/usr/bin/env python3
"""Rename the medical network to the Order of the Mended Hand.

This migration preserves the established moral ambiguity and distributed
Halls/Houses/Clinics structure while making the owner-approved formal name and
common shorthand authoritative across active canon and build scripts.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_PATH = ROOT / "organizations" / "The_Institute_of_Vital_Mechanics.md"
NEW_PATH = ROOT / "organizations" / "The_Order_of_the_Mended_Hand.md"

PATH_REPLACEMENTS = {
    "organizations/The_Institute_of_Vital_Mechanics.md": "organizations/The_Order_of_the_Mended_Hand.md",
    "The_Institute_of_Vital_Mechanics.md": "The_Order_of_the_Mended_Hand.md",
}

TEXT_REPLACEMENTS = [
    ("The Institute of Vital Mechanics", "The Order of the Mended Hand"),
    ("the Institute of Vital Mechanics", "the Order of the Mended Hand"),
    ("Institute of Vital Mechanics", "Order of the Mended Hand"),
    ("The Vital Institute", "The Hand"),
    ("the Vital Institute", "the Hand"),
    ("IVM, provisional abbreviation", "The Hand"),
]


def transform(text: str) -> str:
    for old, new in PATH_REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)

    # Once the formal name has been replaced, remaining capitalized references
    # to the former institution become references to the Order.
    text = re.sub(r"\bInstitute's\b", "Order's", text)
    text = re.sub(r"\bInstitute\b", "Order", text)
    return text


def rewrite_active_files() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "unused" in path.parts:
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in {".md", ".py", ".yml", ".yaml"}:
            continue

        original = path.read_text(encoding="utf-8")
        updated = transform(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


def migrate_profile_path() -> None:
    if OLD_PATH.exists():
        content = transform(OLD_PATH.read_text(encoding="utf-8"))
        NEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        NEW_PATH.write_text(content, encoding="utf-8")
        OLD_PATH.unlink()
    elif NEW_PATH.exists():
        content = transform(NEW_PATH.read_text(encoding="utf-8"))
        NEW_PATH.write_text(content, encoding="utf-8")
    else:
        raise RuntimeError("Medical order profile not found at old or new path")


def refine_order_profile() -> None:
    text = NEW_PATH.read_text(encoding="utf-8")

    text = re.sub(
        r"^name: .*?$",
        "name: The Order of the Mended Hand",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^type: .*?$",
        "type: Chartered hospitaller medical order, surgical network, rehabilitation authority, prosthetics service, and field-response organization",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^aliases:\n(?:  - .*\n)+",
        "aliases:\n  - The Mended Hand\n  - The Hand\n  - The Order\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    text = text.replace(
        "Its exact final name, leadership, internal ranks, branch names, and historical role remain open for later development.",
        "Its formal name and common shorthand are canonical. Its leadership, internal ranks, branch names, founding history, and full historical role remain open for later development.",
    )

    heading = "## Name and Common Usage"
    if heading not in text:
        marker = "## Public Role\n"
        block = """## Name and Common Usage

The formal name is **The Order of the Mended Hand**.

In ordinary speech, citizens call it **the Hand**.

The shorthand carries both reassurance and threat. A person may say, *Take them to the Hand*, when an injury has passed beyond household remedies. Another may answer, *Not unless there is no other choice.*

The word **Order** reflects its age, chartered privileges, dispersed houses, field service, internal loyalties, and semi-autonomous authority. It does not make every member a knight, soldier, or moral exemplar. Exact ranks, vows, chapter titles, and the Order's founding Rule remain unresolved.

"""
        if marker not in text:
            raise RuntimeError("Public Role heading not found in Mended Hand profile")
        text = text.replace(marker, block + marker, 1)

    text = text.replace(
        "1. Is **The Order of the Mended Hand** the final name?",
        "1. What event founded the Order and established its chartered privileges?",
    )
    text = text.replace(
        "- [ ] Approve the final organization name.",
        "- [x] Formal name approved: **The Order of the Mended Hand**; common shorthand approved: **the Hand**.",
    )

    # The Hall is a facility belonging to a hospitaller order, not itself a
    # medical institute. Its final proper name remains unresolved.
    text = text.replace(
        "Unlisted civic hospital, medical order, and emergency-coordination center",
        "Unlisted civic hospital, central order hall, and emergency-coordination center",
    )

    NEW_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    # Move the canonical profile first, then update every inbound reference and
    # the scripts that regenerate those references.
    migrate_profile_path()
    rewrite_active_files()
    refine_order_profile()
    rewrite_active_files()
    print("Renamed the medical network to the Order of the Mended Hand (the Hand).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
