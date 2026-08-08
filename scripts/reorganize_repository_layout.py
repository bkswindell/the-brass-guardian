#!/usr/bin/env python3
"""One-time migration to clean the repository root and centralize templates/docs.

Moves project templates into /templates, development/reference documents into /docs,
and rewrites Markdown links plus hard-coded path references to the moved files.
The companion workflow removes this script and itself after a successful migration.
"""

from __future__ import annotations

import os
import posixpath
import re
import shutil
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

ROOT_MD_ALLOWLIST = {
    "README.md",
    "AGENTS.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
}

EXCLUDED_TEMPLATE_ROOTS = {".git", ".github", "agents", "unused", "templates"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json", ".toml", ".txt", ".ps1", ".sh"}

EXPLICIT_MOVES = {
    "PROJECT_INDEX.md": "docs/PROJECT_INDEX.md",
    "CANON_MARKDOWN_STANDARD.md": "docs/standards/CANON_MARKDOWN_STANDARD.md",
    "Map_Location_Reference_Style_Guide.md": "docs/standards/Map_Location_Reference_Style_Guide.md",
    "PLACEHOLDER_PROFILE_INDEX.md": "docs/development/PLACEHOLDER_PROFILE_INDEX.md",
    "CANON_DEVELOPMENT_TODO.md": "docs/development/CANON_DEVELOPMENT_TODO.md",
}

TEMP_SCRIPT = "scripts/reorganize_repository_layout.py"
TEMP_WORKFLOW = ".github/workflows/reorganize-repository-layout.yml"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_project_template(path: Path) -> bool:
    rp = path.relative_to(ROOT)
    if not path.is_file() or path.suffix.lower() != ".md":
        return False
    if rp.parts and rp.parts[0] in EXCLUDED_TEMPLATE_ROOTS:
        return False
    return "template" in path.name.lower()


def choose_root_doc_destination(name: str) -> str:
    if name in EXPLICIT_MOVES:
        return EXPLICIT_MOVES[name]
    low = name.lower()
    if "template" in low:
        return f"templates/{name}"
    if low.endswith("_todo.md") or low.endswith("_index.md"):
        return f"docs/development/{name}"
    if "standard" in low or "style_guide" in low or "style-guide" in low or "guide" in low:
        return f"docs/standards/{name}"
    return f"docs/reference/{name}"


def build_move_map() -> dict[str, str]:
    moves: dict[str, str] = {}

    # Centralize all project Markdown templates outside excluded system/agent areas.
    for path in ROOT.rglob("*.md"):
        if is_project_template(path):
            old = rel(path)
            new = f"templates/{path.name}"
            if old != new:
                moves[old] = new

    # Clean the remaining project Markdown from repository root.
    for path in ROOT.glob("*.md"):
        if path.name in ROOT_MD_ALLOWLIST:
            continue
        moves.setdefault(path.name, choose_root_doc_destination(path.name))

    return moves


def normalize_repo_path(parent: PurePosixPath, target: str) -> str:
    joined = posixpath.normpath(posixpath.join(parent.as_posix(), target))
    if joined.startswith("./"):
        joined = joined[2:]
    return joined


def split_suffix(target: str) -> tuple[str, str]:
    cut = len(target)
    for marker in ("?", "#"):
        i = target.find(marker)
        if i != -1:
            cut = min(cut, i)
    return target[:cut], target[cut:]


def rewrite_local_target(target: str, original_file: str, current_file: str, moves: dict[str, str]) -> str:
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
        return target

    angle = target.startswith("<") and target.endswith(">")
    raw = target[1:-1] if angle else target
    path_part, suffix = split_suffix(raw)
    if not path_part or path_part.startswith("/"):
        return target

    old_parent = PurePosixPath(original_file).parent
    new_parent = PurePosixPath(current_file).parent
    old_repo_target = normalize_repo_path(old_parent, path_part)
    new_repo_target = moves.get(old_repo_target, old_repo_target)

    start = new_parent.as_posix() if new_parent.as_posix() != "." else "."
    new_relative = posixpath.relpath(new_repo_target, start=start)
    result = new_relative + suffix
    return f"<{result}>" if angle else result


INLINE_LINK_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]*\]\()(?P<target><[^>]+>|[^)\s]+)(?P<suffix>(?:\s+[\"'][^\"']*[\"'])?\))"
)
REF_LINK_RE = re.compile(r"^(?P<prefix>\s*\[[^\]]+\]:\s*)(?P<target><[^>]+>|\S+)(?P<suffix>.*)$")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")


def rewrite_markdown(text: str, original_file: str, current_file: str, moves: dict[str, str]) -> str:
    def inline_sub(match: re.Match[str]) -> str:
        target = rewrite_local_target(match.group("target"), original_file, current_file, moves)
        return match.group("prefix") + target + match.group("suffix")

    text = INLINE_LINK_RE.sub(inline_sub, text)

    out_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        ending = "\n" if line.endswith("\n") else ""
        body = line[:-1] if ending else line
        m = REF_LINK_RE.match(body)
        if m:
            target = rewrite_local_target(m.group("target"), original_file, current_file, moves)
            body = m.group("prefix") + target + m.group("suffix")
        out_lines.append(body + ending)
    text = "".join(out_lines)

    # Agent/project instructions often use repository-root file paths in inline code.
    def code_sub(match: re.Match[str]) -> str:
        inner = match.group(1)
        if inner in moves:
            return f"`{moves[inner]}`"
        if inner.startswith("/") and inner[1:] in moves:
            return f"`/{moves[inner[1:]]}`"
        return match.group(0)

    return CODE_SPAN_RE.sub(code_sub, text)


def rewrite_non_markdown(text: str, moves: dict[str, str]) -> str:
    # Source code/workflows generally use repository-root paths.
    for old, new in sorted(moves.items(), key=lambda kv: len(kv[0]), reverse=True):
        escaped = re.escape(old)
        text = re.sub(rf"(?<![/A-Za-z0-9_.-]){escaped}(?![A-Za-z0-9_.-])", new, text)
        text = text.replace(f"/{old}", f"/{new}")
    return text


def move_files(moves: dict[str, str]) -> None:
    for old, new in sorted(moves.items()):
        src = ROOT / old
        dst = ROOT / new
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            if src.read_bytes() == dst.read_bytes():
                src.unlink()
                continue
            raise RuntimeError(f"Destination collision: {old} -> {new}")
        shutil.move(str(src), str(dst))
        print(f"MOVE {old} -> {new}")


def write_navigation_files() -> None:
    templates_readme = ROOT / "templates/README.md"
    templates_readme.parent.mkdir(parents=True, exist_ok=True)
    templates_readme.write_text(
        "# Canon and Development Templates\n\n"
        "This directory contains the reusable Markdown templates for *The Brass Guardian / Aetherhaven* project.\n\n"
        "Templates are structural starting points, not canonical content. Creating or filling a template does not establish canon; creative changes remain subject to the author's approval rules in [`../agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`](../agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md).\n\n"
        "## Available Templates\n\n"
        "- [Character Profile](Character_Profile_Template.md)\n"
        "- [Organization Profile](Organization_Profile_Template.md)\n"
        "- [Location Profile](Location_Profile_Template.md)\n"
        "- [Artifact Profile](Artifact_Profile_Template.md)\n"
        "- [Story Arc Profile](Story_Arc_Profile_Template.md)\n"
        "- [Historical Event Profile](Historical_Event_Profile_Template.md)\n\n"
        "Use the repository's [Canon Markdown Standard](../docs/standards/CANON_MARKDOWN_STANDARD.md) when creating or revising canonical Markdown.\n",
        encoding="utf-8",
    )

    docs_readme = ROOT / "docs/README.md"
    docs_readme.parent.mkdir(parents=True, exist_ok=True)
    docs_readme.write_text(
        "# Project Documentation\n\n"
        "This directory contains project-wide development indexes, standards, and working documentation that do not need to live at repository root.\n\n"
        "## Project Index\n\n"
        "- [Project Index](PROJECT_INDEX.md) — internal canon inventory, audit notes, and repository map.\n\n"
        "## Standards\n\n"
        "- [Canon Markdown and Visual Integration Standard](standards/CANON_MARKDOWN_STANDARD.md)\n"
        "- [Aetherhaven Map-Location Reference Style Guide](standards/Map_Location_Reference_Style_Guide.md)\n\n"
        "## Development\n\n"
        "- [Canon Development TODO](development/CANON_DEVELOPMENT_TODO.md)\n"
        "- [Placeholder Profile Index](development/PLACEHOLDER_PROFILE_INDEX.md)\n\n"
        "Reusable profile structures live in [`../templates/`](../templates/README.md). AI collaboration and durable memory live in [`../agents/`](../agents/README.md).\n",
        encoding="utf-8",
    )


def update_project_index_heading() -> None:
    path = ROOT / "docs/PROJECT_INDEX.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace("## Root Project Files", "## Core Project and Development Files")
        path.write_text(text, encoding="utf-8")


def rewrite_references(moves: dict[str, str]) -> None:
    inverse = {new: old for old, new in moves.items()}

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rp = rel(path)
        if rp in {TEMP_SCRIPT, TEMP_WORKFLOW}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if path.suffix.lower() == ".md":
            original = inverse.get(rp, rp)
            new_text = rewrite_markdown(text, original, rp, moves)
        else:
            new_text = rewrite_non_markdown(text, moves)

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"REWRITE {rp}")


def check_root() -> None:
    remaining = sorted(p.name for p in ROOT.glob("*.md") if p.name not in ROOT_MD_ALLOWLIST)
    if remaining:
        raise RuntimeError(f"Unexpected Markdown files remain at repository root: {remaining}")

    print("\nRepository root Markdown:")
    for p in sorted(ROOT.glob("*.md")):
        print(f"  {p.name}")


def report_old_paths(moves: dict[str, str]) -> None:
    stale: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rp = rel(path)
        if rp in {TEMP_SCRIPT, TEMP_WORKFLOW}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for old in moves:
            if f"]({old}" in text or f"`{old}`" in text or f"`/{old}`" in text:
                stale.append(f"{rp}: {old}")
    if stale:
        print("\nWARNING: possible stale references:")
        for item in stale:
            print(f"  {item}")


def remove_temporary_migration_files() -> None:
    for rp in (TEMP_SCRIPT, TEMP_WORKFLOW):
        p = ROOT / rp
        if p.exists():
            p.unlink()
            print(f"REMOVE temporary migration file {rp}")


def main() -> None:
    os.chdir(ROOT)
    moves = build_move_map()
    if not moves:
        print("No files require relocation.")
        return

    print("Planned relocations:")
    for old, new in sorted(moves.items()):
        print(f"  {old} -> {new}")

    move_files(moves)
    rewrite_references(moves)
    write_navigation_files()
    update_project_index_heading()
    check_root()
    report_old_paths(moves)
    remove_temporary_migration_files()

    print("\nRepository layout migration complete.")


if __name__ == "__main__":
    main()
