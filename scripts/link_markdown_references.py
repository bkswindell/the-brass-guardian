#!/usr/bin/env python3
"""Add relative links between canonical Markdown records.

The script discovers documented characters, organizations, locations, and artifacts,
then links unlinked name references across Markdown files. It intentionally avoids
YAML front matter, headings, fenced code, existing links/images, inline code,
reference definitions, and exact visual-transcription sections.
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
EXCLUDED_FILES = {
    ROOT / "README2.md",  # legacy duplicate, intentionally not maintained as canon
}
VISUAL_EVIDENCE_HEADINGS = {
    "plate text transcription — visual evidence only",
    "plate text transcription - visual evidence only",
    "complete plate description — visual evidence only",
    "complete plate description - visual evidence only",
}

# Markdown regions protected from substitutions.
PROTECTED_RE = re.compile(
    r"(!?\[[^\]\n]*\]\([^\)\n]+\)|"  # inline links and images
    r"!?\[[^\]\n]*\]\[[^\]\n]*\]|"  # reference links and images
    r"`[^`\n]+`|"                         # inline code
    r"https?://[^\s<>)\]]+|"             # URLs
    r"<[^>\n]+>)"                          # HTML tags
)


@dataclass(frozen=True)
class Entity:
    kind: str
    path: Path
    display_name: str
    aliases: tuple[str, ...]


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.strip()


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    end += len("\n---\n")
    return text[:end], text[end:]


def parse_simple_yaml(front_matter: str) -> dict[str, object]:
    """Parse the small YAML subset used in this repository without dependencies."""
    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in front_matter.splitlines():
        if raw in {"---", ""} or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s+-\s+", raw) and current_list:
            item = clean_scalar(re.sub(r"^\s+-\s+", "", raw))
            if item and item.lower() != "null":
                cast = data.setdefault(current_list, [])
                if isinstance(cast, list):
                    cast.append(item)
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
            heading = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", match.group(1))
            return heading.strip()
    return None


def filename_alias(path: Path) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    return stem.replace("_", " ").strip()


def normalized_aliases(kind: str, path: Path, metadata: dict[str, object], heading: str | None) -> list[str]:
    aliases: list[str] = []

    def add(value: str | None) -> None:
        if not value:
            return
        value = value.strip()
        if not value or value.lower() in {"unassigned", "none", "null"}:
            return
        if value not in aliases:
            aliases.append(value)

    name = metadata.get("name")
    if isinstance(name, str):
        add(name)
    title = metadata.get("title")
    if isinstance(title, str):
        add(title)
    elif isinstance(title, list):
        for item in title:
            if isinstance(item, str):
                add(item)
    formal_title = metadata.get("formal_title")
    if isinstance(formal_title, str):
        add(formal_title)
    elif isinstance(formal_title, list):
        for item in formal_title:
            if isinstance(item, str):
                add(item)
    declared_aliases = metadata.get("aliases")
    if isinstance(declared_aliases, list):
        for item in declared_aliases:
            if isinstance(item, str):
                add(item)
    add(heading)
    add(filename_alias(path))

    # Article-free aliases for names that begin with "The".
    for alias in list(aliases):
        if alias.lower().startswith("the ") and len(alias) > 4:
            add(alias[4:])

    if kind == "character":
        # Derive short personal-name aliases only from the primary name field.
        # Never split titles or epithets such as "The Man Between Ticks" into
        # common words that would create false links.
        primary_name = metadata.get("name") if isinstance(metadata.get("name"), str) else None
        if primary_name and primary_name.casefold() not in {"unassigned", "none", "null"}:
            plain = re.sub(r"\([^)]*\)", "", primary_name)
            plain = re.sub(
                r"^(Captain|Chancellor|Chief Inspector|Inspector|Professor|Doctor|Dr\.|Master|Madame|Harbormaster)\s+",
                "",
                plain,
                flags=re.IGNORECASE,
            ).strip()
            if not plain.casefold().startswith("the "):
                words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'’.-]*", plain)
                if 1 < len(words) <= 3:
                    for word in words:
                        if len(word) >= 4 or word == "Pip":
                            add(word)

    # Avoid auto-linking generic terms by themselves.
    generic = {
        "guild", "council", "order", "watch", "union", "gardens", "garden",
        "district", "passenger", "keeper", "prototype", "archive", "archives",
        "society", "conservancy", "underclock", "unwound", "artifact", "seal",
        "mark", "key", "ticket", "crest", "wayfinder", "morningstar",
    }
    aliases = [a for a in aliases if a.casefold() not in generic]
    return aliases


def discover_entities() -> list[Entity]:
    provisional: list[tuple[str, Path, str, list[str]]] = []
    for kind, directory in ENTITY_DIRS.items():
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            text = path.read_text(encoding="utf-8")
            front, body = split_front_matter(text)
            metadata = parse_simple_yaml(front)
            heading = first_h1(body)
            display = metadata.get("name") if isinstance(metadata.get("name"), str) else heading
            if not display:
                display = filename_alias(path)
            aliases = normalized_aliases(kind, path, metadata, heading)
            provisional.append((kind, path, str(display), aliases))

    # Remove aliases that resolve to more than one entity. Full display names remain.
    alias_owners: dict[str, set[Path]] = {}
    for _, path, _, aliases in provisional:
        for alias in aliases:
            alias_owners.setdefault(alias.casefold(), set()).add(path)

    entities: list[Entity] = []
    for kind, path, display, aliases in provisional:
        filtered: list[str] = []
        for alias in aliases:
            owners = alias_owners.get(alias.casefold(), set())
            if len(owners) == 1 or alias.casefold() == display.casefold():
                filtered.append(alias)
        # Longer aliases first prevents partial replacements.
        filtered = sorted(set(filtered), key=lambda a: (-len(a), a.casefold()))
        entities.append(Entity(kind, path, display, tuple(filtered)))
    return entities


def markdown_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.md"):
        if path in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_DIR_NAMES for part in path.relative_to(ROOT).parts):
            continue
        yield path


def relative_target(source: Path, target: Path) -> str:
    rel = os.path.relpath(target, source.parent).replace(os.sep, "/")
    return rel


def alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias)
    # Treat spaces as flexible whitespace and accept straight/curly apostrophe variants.
    escaped = escaped.replace(r"\ ", r"\s+")
    escaped = escaped.replace("’", "['’]").replace(r"\'", "['’]")
    return re.compile(rf"(?<![\w]){escaped}(?![\w])", re.IGNORECASE)


def link_plain_segment(segment: str, source: Path, entities: list[Entity]) -> str:
    # Find every candidate against the original plain segment, then render once.
    # This prevents later substitutions from matching text or paths inside links
    # inserted earlier in the same pass.
    candidates: list[tuple[int, int, Entity, str]] = []
    for entity in entities:
        if entity.path == source:
            continue
        for alias in entity.aliases:
            for match in alias_pattern(alias).finditer(segment):
                candidates.append((match.start(), match.end(), entity, match.group(0)))

    if not candidates:
        return segment

    # At a shared start position, prefer the longest available canonical name.
    candidates.sort(key=lambda item: (item[0], -(item[1] - item[0]), item[2].display_name.casefold()))
    selected: list[tuple[int, int, Entity, str]] = []
    cursor = -1
    for candidate in candidates:
        start, end, _, _ = candidate
        if start < cursor:
            continue
        selected.append(candidate)
        cursor = end

    rendered: list[str] = []
    cursor = 0
    for start, end, entity, matched_text in selected:
        rendered.append(segment[cursor:start])
        rendered.append(f"[{matched_text}]({relative_target(source, entity.path)})")
        cursor = end
    rendered.append(segment[cursor:])
    return "".join(rendered)


def link_line(line: str, source: Path, entities: list[Entity]) -> str:
    # Do not alter headings; linked headings create unstable anchors.
    if re.match(r"^\s{0,3}#{1,6}\s", line):
        return line
    # Reference definitions and horizontal structures should remain intact.
    if re.match(r"^\s*\[[^\]]+\]:\s", line):
        return line
    if re.match(r"^\s*<!--", line):
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
    fence_token = ""
    skip_visual_section = False
    output: list[str] = []

    for line in lines:
        stripped = line.rstrip("\r\n")
        fence = re.match(r"^\s*(```+|~~~+)", stripped)
        if fence:
            token = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token[0]
            elif token.startswith(fence_token):
                in_fence = False
                fence_token = ""
            output.append(line)
            continue

        h2 = re.match(r"^##\s+(.+?)\s*$", stripped)
        if h2:
            heading = h2.group(1).strip().casefold()
            skip_visual_section = heading in VISUAL_EVIDENCE_HEADINGS

        if in_fence or skip_visual_section:
            output.append(line)
            continue

        linked = link_line(line, path, entities)
        if linked != line:
            # Existing Markdown hard-break spaces become newly added whitespace
            # after a link insertion and fail `git diff --check`. Preserve the
            # newline while removing only trailing horizontal whitespace.
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
            destination = (path.parent / clean).resolve()
            if not destination.exists():
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
