#!/usr/bin/env python3
"""Cross-link canonical names throughout the repository's Markdown files.

The linker discovers documented characters, organizations, locations, and artifacts
from their YAML front matter. It adds relative Markdown links to unlinked references
while preserving YAML, existing links and images, headings, code, URLs, and exact
artifact visual-evidence transcriptions.
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

# These phrases are legitimate conversational shorthand, but they are too
# context-dependent to auto-link safely. Full canonical names and distinctive
# aliases remain linkable.
AMBIGUOUS_SHORTHAND = {
    "the architect",
    "the archives",
    "the conservancy",
    "the council",
    "the eight",
    "the gardens",
    "the guild",
    "the keeper",
    "the order",
    "the passenger",
    "the union",
    "the watch",
}
GENERIC_SINGLE_WORDS = {
    "archive", "archives", "architect", "artifact", "bell", "conservancy",
    "council", "crest", "district", "eight", "garden", "gardens", "guild",
    "key", "keeper", "mark", "order", "passenger", "prototype", "seal",
    "society", "ticket", "union", "watch",
}
AMBIGUOUS_SURNAMES = {"Bell", "Pike", "Rook", "Vale"}
HONORIFIC_RE = re.compile(
    r"^(Captain|Chancellor|Chief Inspector|Inspector|Professor|Doctor|Dr\.|Master|Madame|Harbormaster)\s+",
    flags=re.IGNORECASE,
)


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
    """Parse the small YAML subset used by the canon records."""
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


def is_safe_article_free_alias(remainder: str) -> bool:
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9'’.-]+", remainder)
    if not words:
        return False
    return not (len(words) == 1 and words[0].casefold() in GENERIC_SINGLE_WORDS)


def is_distinctive_epithet(title: str) -> bool:
    if not title.startswith("The ") or " of " in title.casefold():
        return False
    return 2 <= len(title.split()) <= 5 and is_safe_article_free_alias(title[4:])


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

    def add(text: str | None, *, case_sensitive: bool = False) -> None:
        if not text:
            return
        text = text.strip()
        if not text or text.casefold() in AMBIGUOUS_SHORTHAND:
            return
        key = (text.casefold(), case_sensitive)
        if any((item.text.casefold(), item.case_sensitive) == key for item in aliases):
            return
        aliases.append(Alias(text=text, case_sensitive=case_sensitive))

    display_is_single_character_name = kind == "character" and len(display.split()) == 1
    add(display, case_sensitive=display_is_single_character_name)
    if name and name.casefold() != display.casefold():
        add(name, case_sensitive=kind == "character" and len(name.split()) == 1)

    declared = metadata.get("aliases")
    if isinstance(declared, list):
        for item in declared:
            if isinstance(item, str):
                add(item, case_sensitive=kind == "character" and len(item.split()) == 1)

    # The eight named founding guilds share the umbrella organization's file.
    if kind == "organization":
        member_guilds = metadata.get("member_guilds")
        if isinstance(member_guilds, list):
            for item in member_guilds:
                if isinstance(item, str):
                    add(item)

    if kind == "character" and title and is_distinctive_epithet(title):
        add(title)

    for alias in list(aliases):
        if alias.text.casefold().startswith("the "):
            remainder = alias.text[4:].strip()
            if is_safe_article_free_alias(remainder):
                add(remainder, case_sensitive=alias.case_sensitive)

    if kind == "character" and name:
        plain = HONORIFIC_RE.sub("", re.sub(r"\([^)]*\)", "", name)).strip()
        if not plain.casefold().startswith("the "):
            words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'’.-]*", plain)
            if 2 <= len(words) <= 3:
                add(words[0], case_sensitive=True)
                surname = words[-1]
                if surname not in AMBIGUOUS_SURNAMES:
                    add(surname, case_sensitive=True)

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
    # Preserve headings so their generated anchors remain stable.
    if re.match(r"^\s{0,3}#{1,6}\s", line):
        return line
    if re.match(r"^\s*\[[^\]]+\]:\s", line) or re.match(r"^\s*<!--", line):
        return line

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
