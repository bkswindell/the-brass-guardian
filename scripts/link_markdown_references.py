#!/usr/bin/env python3
"""Cross-link canonical entity names throughout the Markdown library.

The linker discovers documented characters, organizations, locations, and artifacts
from YAML front matter. It adds relative Markdown links while preserving YAML,
existing links and images, code, URLs, HTML, and exact artifact transcription
sections. It also repairs a small class of malformed links created by older passes.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
ENTITY_DIRS = {
    "character": ROOT / "characters",
    "organization": ROOT / "organizations",
    "location": ROOT / "locations",
    "artifact": ROOT / "artifacts",
    "story_arc": ROOT / "story_arcs",
    "historical_event": ROOT / "historical_events",
}
EXCLUDED_DIR_NAMES = {".git", ".github", "unused", "node_modules", "vendor"}
VISUAL_EVIDENCE_HEADINGS = {
    "plate text transcription — visual evidence only",
    "plate text transcription - visual evidence only",
    "complete plate description — visual evidence only",
    "complete plate description - visual evidence only",
}

PROTECTED_RE = re.compile(
    r"(!?\[[^\]\n]*\]\([^\)\n]+\)|"  # inline links and images
    r"!?\[[^\]\n]*\]\[[^\]\n]*\]|"  # reference links and images
    r"`[^`\n]+`|"                         # inline code
    r"https?://[^\s<>)\]]+|"             # URLs
    r"<[^>\n]+>)"                          # HTML tags
)
INLINE_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+\.md(?:#[^)\n]+)?)\)")

AMBIGUOUS_SHORTHAND = {
    "architect",
    "archives",
    "the archives",
    "conservancy",
    "the conservancy",
    "council",
    "the council",
    "eight",
    "the eight",
    "fellowship",
    "the fellowship",
    "gardens",
    "the gardens",
    "guild",
    "the guild",
    "keeper",
    "the keeper",
    "order",
    "the order",
    "passenger",
    "the passenger",
    "twelve",
    "the twelve",
    "union",
    "the union",
    "watch",
    "the watch",
}

HONORIFIC_RE = re.compile(
    r"^(Captain|Chancellor|Chief Inspector|Inspector|Professor|Doctor|Dr\.|Master|Madame|Harbormaster)\s+",
    flags=re.IGNORECASE,
)

# Safe short forms used repeatedly in canon. They are deliberately curated rather
# than derived from every first name, which avoids false links such as Beatrice Pike
# being linked to Beatrice Thorne.
CURATED_SHORT_ALIASES: dict[str, tuple[str, ...]] = {
    "Captain_Mara_Voss.md": ("Mara",),
    "Chancellor_Octavia_Vale.md": ("Octavia",),
    "Chief_Inspector_Beatrice_Thorne.md": ("Thorne",),
    "Juniper_Bell.md": ("Juniper",),
    "Pip.md": ("Pip",),
    "Silas_Rook_The_Stillmaker.md": ("Silas", "Rook"),
    "Tamsin_Pike.md": ("Tamsin",),
    "Professor_Elias_Hawthorne.md": ("Elias",),
    "Amelia_Hawthorne.md": ("Amelia",),
    "Doctor_Elara_Quill.md": ("Elara",),
    "Master_Gideon_Brasswell.md": ("Gideon",),
    "Orin_Flint.md": ("Orin",),
    "Lucian_Wren.md": ("Lucian",),
    "Barnaby_Wren.md": ("Barnaby",),
    "Madame_Celestine_Mirrow.md": ("Celestine",),
}


@dataclass(frozen=True)
class Alias:
    text: str
    case_sensitive: bool = False


@dataclass(frozen=True)
class Entity:
    kind: str
    path: Path
    display_name: str
    aliases: tuple[Alias, ...]


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.strip()


def valid_value(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or value.casefold() in {"unassigned", "none", "null"}:
        return None
    return value


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    end += len("\n---\n")
    return text[:end], text[end:]


def parse_simple_yaml(front_matter: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in front_matter.splitlines():
        if raw in {"---", ""} or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s+-\s+", raw) and current_list:
            item = clean_scalar(re.sub(r"^\s+-\s+", "", raw))
            if item and item.casefold() != "null":
                values = data.setdefault(current_list, [])
                if isinstance(values, list):
                    values.append(item)
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not match:
            continue
        key, value = match.groups()
        if value == "":
            data[key] = []
            current_list = key
        else:
            data[key] = clean_scalar(value)
            current_list = None
    return data


def first_h1(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", match.group(1)).strip()
    return None


def filename_alias(path: Path) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    return stem.replace("_", " ").strip()


def default_case_sensitive(text: str) -> bool:
    return len(text.split()) == 1


def build_aliases(
    kind: str,
    metadata: dict[str, object],
    heading: str | None,
    path: Path,
) -> tuple[str, list[Alias]]:
    name = valid_value(metadata.get("name"))
    title = valid_value(metadata.get("title"))
    display = name or (title if kind == "character" and title else None) or heading or filename_alias(path)
    aliases: list[Alias] = []

    def add(text: str | None, *, case_sensitive: bool | None = None) -> None:
        if not text:
            return
        text = text.strip()
        if not text or text.casefold() in AMBIGUOUS_SHORTHAND:
            return
        if case_sensitive is None:
            case_sensitive = default_case_sensitive(text)
        key = (text.casefold(), case_sensitive)
        if any((item.text.casefold(), item.case_sensitive) == key for item in aliases):
            return
        aliases.append(Alias(text=text, case_sensitive=case_sensitive))

    add(display)
    if name and name.casefold() != display.casefold():
        add(name)

    declared = metadata.get("aliases")
    if isinstance(declared, list):
        for item in declared:
            if isinstance(item, str):
                add(item)

    # Link article-free variants only when they remain distinctive. Multiword
    # official names are safe; single-word proper nouns remain case-sensitive.
    for alias in list(aliases):
        if alias.text.casefold().startswith("the "):
            remainder = alias.text[4:].strip()
            if len(remainder.split()) >= 2 or remainder in {"Cauldron", "Stillmaker", "Underclock", "Unwound"}:
                add(remainder, case_sensitive=default_case_sensitive(remainder))

    if kind == "character" and name:
        plain = HONORIFIC_RE.sub("", re.sub(r"\([^)]*\)", "", name)).strip()
        if plain and not plain.casefold().startswith("the "):
            add(plain)
        for short in CURATED_SHORT_ALIASES.get(path.name, ()):
            add(short, case_sensitive=True)

    # The umbrella founding-guild profile historically listed member_guilds. When
    # dedicated guild files exist, duplicate alias filtering below gives ownership
    # to the dedicated profile rather than the umbrella record.
    if kind == "organization":
        member_guilds = metadata.get("member_guilds")
        if isinstance(member_guilds, list):
            for item in member_guilds:
                if isinstance(item, str):
                    add(item)

    return display, aliases


def discover_entities() -> list[Entity]:
    provisional: list[tuple[str, Path, str, list[Alias]]] = []
    for kind, directory in ENTITY_DIRS.items():
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.casefold() == "readme.md":
                continue
            text = path.read_text(encoding="utf-8")
            front, body = split_front_matter(text)
            metadata = parse_simple_yaml(front)
            display, aliases = build_aliases(kind, metadata, first_h1(body), path)
            provisional.append((kind, path, display, aliases))

    owners: dict[str, set[Path]] = {}
    for _, path, _, aliases in provisional:
        for alias in aliases:
            owners.setdefault(alias.text.casefold(), set()).add(path)

    entities: list[Entity] = []
    for kind, path, display, aliases in provisional:
        filtered = [
            alias
            for alias in aliases
            if len(owners.get(alias.text.casefold(), set())) == 1
            or alias.text.casefold() == display.casefold()
        ]
        filtered.sort(key=lambda item: (-len(item.text), item.text.casefold()))
        entities.append(Entity(kind, path, display, tuple(filtered)))
    return entities


def markdown_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIR_NAMES for part in path.relative_to(ROOT).parts):
            continue
        yield path


def relative_target(source: Path, target: Path) -> str:
    return os.path.relpath(target, source.parent).replace(os.sep, "/")


def alias_pattern(alias: Alias) -> re.Pattern[str]:
    escaped = re.escape(alias.text)
    escaped = escaped.replace(r"\ ", r"\s+")
    escaped = escaped.replace("’", "['’]").replace(r"\'", "['’]")
    flags = 0 if alias.case_sensitive else re.IGNORECASE
    return re.compile(rf"(?<![\w]){escaped}(?![\w])", flags)


def entity_for_target(source: Path, target: str, by_path: dict[Path, Entity]) -> Entity | None:
    clean = target.split("#", 1)[0]
    try:
        resolved = (source.parent / clean).resolve()
    except OSError:
        return None
    return by_path.get(resolved)


def alias_owner(text: str, entities: list[Entity]) -> Entity | None:
    matches: list[Entity] = []
    for entity in entities:
        if any(alias.text.casefold() == text.casefold() for alias in entity.aliases):
            matches.append(entity)
    unique = {entity.path: entity for entity in matches}
    return next(iter(unique.values())) if len(unique) == 1 else None


def repair_existing_links(line: str, source: Path, entities: list[Entity]) -> str:
    by_path = {entity.path.resolve(): entity for entity in entities}

    # Combine adjacent links to the same target, such as [Mara](...) [Voss](...).
    adjacent = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)\s+\[([^\]]+)\]\(\2\)")
    while True:
        updated = adjacent.sub(lambda m: f"[{m.group(1)} {m.group(3)}]({m.group(2)})", line)
        if updated == line:
            break
        line = updated

    # Repair a linked first name followed by an unlinked surname. The combined
    # name may belong to the same entity or a different one, as with Beatrice Pike.
    partial = re.compile(r"\[([A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)\]\(([^)]+\.md)\)\s+([A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)")

    def repair_partial(match: re.Match[str]) -> str:
        combined = f"{match.group(1)} {match.group(3)}"
        owner = alias_owner(combined, entities)
        if not owner:
            return match.group(0)
        return f"[{combined}]({relative_target(source, owner.path)})"

    line = partial.sub(repair_partial, line)

    # Remove clearly ambiguous or lowercase auto-links created by older passes.
    def clean_link(match: re.Match[str]) -> str:
        anchor, target = match.groups()
        entity = entity_for_target(source, target, by_path)
        if not entity:
            return match.group(0)
        stripped = re.sub(r"[*_`]", "", anchor).strip()
        if stripped.casefold() in AMBIGUOUS_SHORTHAND:
            return anchor
        if stripped and stripped == stripped.casefold() and entity.kind in {"character", "organization", "location"}:
            return anchor
        return match.group(0)

    return INLINE_LINK_RE.sub(clean_link, line)


def link_plain_segment(segment: str, source: Path, entities: list[Entity]) -> str:
    candidates: list[tuple[int, int, Entity, str]] = []
    for entity in entities:
        if entity.path == source:
            continue
        for alias in entity.aliases:
            for match in alias_pattern(alias).finditer(segment):
                candidates.append((match.start(), match.end(), entity, match.group(0)))

    if not candidates:
        return segment

    candidates.sort(key=lambda item: (item[0], -(item[1] - item[0]), item[2].display_name.casefold()))
    selected: list[tuple[int, int, Entity, str]] = []
    occupied_until = -1
    for candidate in candidates:
        start, end, _, _ = candidate
        if start < occupied_until:
            continue
        selected.append(candidate)
        occupied_until = end

    rendered: list[str] = []
    cursor = 0
    for start, end, entity, matched_text in selected:
        rendered.append(segment[cursor:start])
        rendered.append(f"[{matched_text}]({relative_target(source, entity.path)})")
        cursor = end
    rendered.append(segment[cursor:])
    return "".join(rendered)


def link_line(line: str, source: Path, entities: list[Entity]) -> str:
    if re.match(r"^\s*\[[^\]]+\]:\s", line) or re.match(r"^\s*<!--", line):
        return line

    line = repair_existing_links(line, source, entities)
    pieces: list[str] = []
    cursor = 0
    for match in PROTECTED_RE.finditer(line):
        if match.start() > cursor:
            pieces.append(link_plain_segment(line[cursor:match.start()], source, entities))
        pieces.append(match.group(0))
        cursor = match.end()
    if cursor < len(line):
        pieces.append(link_plain_segment(line[cursor:], source, entities))
    return "".join(pieces)


def process_file(path: Path, entities: list[Entity]) -> tuple[str, int]:
    original = path.read_text(encoding="utf-8")
    front, body = split_front_matter(original)
    lines = body.splitlines(keepends=True)
    changed = 0
    in_fence = False
    fence_character = ""
    skip_visual_section = False
    output: list[str] = []

    for line in lines:
        stripped = line.rstrip("\r\n")
        fence = re.match(r"^\s*(```+|~~~+)", stripped)
        if fence:
            token = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_character = token[0]
            elif token.startswith(fence_character):
                in_fence = False
                fence_character = ""
            output.append(line)
            continue

        h2 = re.match(r"^##\s+(.+?)\s*$", stripped)
        if h2:
            skip_visual_section = h2.group(1).strip().casefold() in VISUAL_EVIDENCE_HEADINGS

        if in_fence or skip_visual_section:
            output.append(line)
            continue

        linked = link_line(line, path, entities)
        if linked != line:
            newline = "\r\n" if linked.endswith("\r\n") else "\n" if linked.endswith("\n") else ""
            core = linked[:-len(newline)] if newline else linked
            linked = core.rstrip(" \t") + newline
            changed += 1
        output.append(linked)

    return front + "".join(output), changed


def validate_links(paths: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+\.md(?:#[^)]+)?)\)")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            clean = target.split("#", 1)[0]
            if re.match(r"^[a-z]+://", clean, re.IGNORECASE):
                continue
            if not (path.parent / clean).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)} -> {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Report changes without writing files")
    args = parser.parse_args()

    entities = discover_entities()
    files = sorted(markdown_files())
    changed_files: list[tuple[Path, int]] = []

    for path in files:
        updated, changed_lines = process_file(path, entities)
        current = path.read_text(encoding="utf-8")
        if updated != current:
            changed_files.append((path, changed_lines))
            if not args.check:
                path.write_text(updated, encoding="utf-8")

    if not args.check:
        broken = validate_links(files)
        if broken:
            print("Broken Markdown links detected:", file=sys.stderr)
            for item in broken:
                print(f"  {item}", file=sys.stderr)
            return 2

    print(f"Discovered {len(entities)} canonical entities.")
    print(f"Scanned {len(files)} Markdown files.")
    print(f"Changed {len(changed_files)} files.")
    for path, count in changed_files:
        print(f"  {path.relative_to(ROOT)} ({count} lines)")
    return 1 if args.check and changed_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
