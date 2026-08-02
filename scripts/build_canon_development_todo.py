#!/usr/bin/env python3
"""Build the single prioritized canon expansion and image-production queue.

The generated file is intentionally operational rather than narrative. It inventories
all source-grounded placeholders, every profile still lacking an integrated canonical
visual, unfinished artifact-image records, and repository-wide integration work.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "CANON_DEVELOPMENT_TODO.md"
TODAY = "2026-08-02"

PROFILE_DIRS = {
    "Character": ROOT / "characters",
    "Organization": ROOT / "organizations",
    "Location": ROOT / "locations",
}

EXCLUDED_NAMES = {"README.md"}

PRIORITY_LABELS = {
    "P0": "Canon blocker or production prerequisite",
    "P1": "Next active work: foundational world, core recurring cast, and central systems",
    "P2": "Primary districts, civic institutions, and recurring story infrastructure",
    "P3": "Restricted locations, hidden powers, mystery figures, and secondary institutions",
    "P4": "Distant regions, supporting families, narrow subgroups, and lower-immediacy material",
    "P5": "Artifact image production after related canon is stable",
    "P6": "Repository integration, accessibility, backlinks, and final QA",
}

STATUS_ORDER = {
    "BLOCKED": 0,
    "NEEDS DECISION": 1,
    "READY": 2,
    "PARTIAL": 3,
    "DEFERRED": 4,
}

# Full-profile synthesis for the central protagonists remains intentionally deferred,
# although their visual integration and cross-linking can proceed now.
DEFERRED_EXPANSION = {
    "characters/Amelia_Hawthorne.md",
    "characters/Professor_Elias_Hawthorne.md",
}

BLOCKED_EXPANSION = {
    "characters/Keeper_Thirteen.md": "Insufficient source material; preserve the mystery until a story or canon decision defines the figure.",
}

DECISION_REQUIRED = {
    "characters/Master_Gideon_Brasswell.md": "Reconcile the two supplied Gideon descriptions before converting the placeholder into a final profile.",
    "characters/Orin_Flint.md": "Resolve whether Orin is mine foreman, Miners' Guild leader, or both, while retaining the six-socket wall material.",
    "characters/Lucian_Wren.md": "Reconcile the anonymous-blueprint story with the earlier First Mechanist machine description.",
    "characters/Barnaby_Wren.md": "Reconcile the Last Lantern promise economy with Barnaby's missing two-year expedition history.",
}

ROLE_ONLY_EXPANSION = {
    "characters/The_Cinder_Regent.md",
    "characters/The_Curator.md",
    "characters/The_First_Tender.md",
    "characters/The_First_Mechanist.md",
    "characters/The_Hidden_Architect_Unassigned.md",
}

P1_PATHS = {
    "locations/Aetherhaven.md",
    "locations/The_Aetherium.md",
    "locations/The_Clockwork_Gardens.md",
    "locations/The_Grand_Atrium.md",
    "locations/The_Clocktower_Spire.md",
    "locations/The_Reflection_Canals.md",
    "locations/The_Government_District.md",
    "locations/The_Academy_of_Invention_Campus.md",
    "locations/The_Great_Workshops.md",
    "locations/The_Engine_Complex.md",
    "locations/The_Gearbreaker_Mines.md",
    "characters/Doctor_Elara_Quill.md",
    "characters/Master_Gideon_Brasswell.md",
    "characters/Orin_Flint.md",
    "characters/Lucian_Wren.md",
    "characters/Barnaby_Wren.md",
    "characters/Madame_Celestine_Mirrow.md",
    "organizations/The_Academy_of_Invention.md",
    "organizations/The_Society_of_Explorers.md",
    "organizations/The_Aetherhaven_Archives.md",
    "organizations/The_Conclave_of_Eight.md",
    "organizations/The_Miners_Guild.md",
}

P2_PATHS = {
    "locations/The_Waterfall_Cascades.md",
    "locations/The_Starlight_Walkways.md",
    "locations/The_Southern_Docks.md",
    "locations/The_Brass_Gate.md",
    "locations/The_Merchant_District.md",
    "locations/The_Inventors_District.md",
    "locations/The_Industrial_District.md",
    "locations/The_Old_City.md",
    "locations/The_Canal_District.md",
    "locations/The_Workers_Dormitories.md",
    "locations/The_Observatory.md",
    "locations/The_Thirteenth_Canal.md",
    "locations/Pike_Bridge.md",
    "locations/The_Last_Lantern.md",
    "locations/The_Theatre_of_Impossible_Things.md",
    "locations/The_Hall_of_Unfinished_Ideas.md",
    "locations/The_High_Chamber.md",
    "locations/The_Octagonal_Hall.md",
    "locations/The_Pulse_Chamber.md",
    "locations/Dock_Zero.md",
    "locations/The_Quiet_Hangar.md",
    "locations/The_Morningstar_Berth.md",
    "locations/The_Wayfinder_Berth.md",
    "locations/Lamplighters_Hall.md",
    "locations/Mariners_Hall.md",
    "locations/Rootglass_Cloister.md",
    "organizations/The_Keepers_of_Time.md",
    "organizations/The_Handwright_Circles.md",
    "organizations/The_Free_Spring_Assembly.md",
    "organizations/The_Clockkeepers_Without_Hours.md",
    "organizations/The_Inner_Compass.md",
    "organizations/The_Cinder_Wardens.md",
    "organizations/The_Ash_Detail.md",
    "organizations/The_Guild_of_Framewrights.md",
    "organizations/The_Guild_of_Enginewrights.md",
    "organizations/The_Guild_of_Aetherwrights.md",
    "organizations/The_Guild_of_Canalwrights.md",
    "organizations/The_Guild_of_Skywrights.md",
    "organizations/The_Guild_of_Clockwrights.md",
    "organizations/The_Guild_of_Artificers.md",
    "organizations/The_Guild_of_Verdant_Mechanists.md",
}

P3_PATHS = {
    "locations/The_Obsidian_Spire.md",
    "locations/The_Shrouded_Vaults.md",
    "locations/The_Echoing_Depths.md",
    "locations/The_Silent_Observatory.md",
    "locations/The_Null_Zone.md",
    "characters/The_First_Mechanist.md",
    "characters/The_Lady_in_the_Water.md",
    "characters/The_Ashen_Cartographer.md",
    "characters/The_Null_Shepherd.md",
    "characters/The_Bellmaker.md",
    "characters/Keeper_Thirteen.md",
    "characters/The_Cinder_Regent.md",
    "characters/The_Curator.md",
    "characters/The_First_Tender.md",
    "organizations/The_Quiet_Choir.md",
    "organizations/The_Furnace_Court.md",
}

P4_PATHS = {
    "locations/The_Clockwork_Jungle.md",
    "locations/The_Skyward_Cliffs.md",
    "locations/The_Skyward_Isles.md",
    "locations/Cloudspire.md",
    "locations/The_Southern_Seas.md",
    "locations/The_Shattered_Lands.md",
    "locations/The_Verdant_Wilds.md",
    "characters/Euphemia_Pike.md",
    "characters/Beatrice_Pike.md",
}

KNOWN_VISUALS = {
    "characters/Amelia_Hawthorne.md": ("PARTIAL", "Link `art/Amelia_Hawthorne.png`; later add a definitive full continuity portrait showing the Aether Heart and mechanical right arm."),
    "characters/Professor_Elias_Hawthorne.md": ("PARTIAL", "Link `art/Hawthornes.png` as a temporary family reference and generate a dedicated Elias portrait later."),
    "locations/Aetherhaven.md": ("PARTIAL", "Link `art/Map_of_Aetherhaven.png` and select or generate a canonical citywide establishing image."),
    "locations/The_Clockwork_Gardens.md": ("PARTIAL", "Link `art/Clockwork_Gardens_at_Night.png` and the Changing Paths artifact record; add a daytime canonical establishing view."),
    "locations/The_Grand_Atrium.md": ("READY", "Link `art/The_Grand_Atrium.png` and the Grand Atrium artifact record into the profile."),
    "organizations/The_Society_of_Explorers.md": ("PARTIAL", "Link the existing Society seal artifact and document the two active variants without forcing an early resolution."),
}

VISUAL_PRIORITY_OVERRIDES = {
    "characters/Captain_Mara_Voss.md": "P1",
    "characters/Chancellor_Octavia_Vale.md": "P1",
    "characters/Chief_Inspector_Beatrice_Thorne.md": "P1",
    "characters/Juniper_Bell.md": "P1",
    "characters/Pip.md": "P1",
    "characters/Tamsin_Pike.md": "P1",
    "characters/The_Passenger_of_Dock_Zero.md": "P1",
    "characters/Silas_Rook_The_Stillmaker.md": "P3",
    "characters/The_Hidden_Architect_Unassigned.md": "P3",
    "organizations/The_High_Council_of_Aetherhaven.md": "P1",
    "organizations/The_Brass_Watch.md": "P1",
    "organizations/The_Conservancy_of_Living_Mechanisms.md": "P1",
    "organizations/The_Mechanists_Guild.md": "P1",
    "organizations/The_Eight_Founding_Engineering_Guilds.md": "P1",
    "organizations/The_Aerial_Mariners_Union.md": "P2",
    "organizations/The_Lamplighters_Fellowship.md": "P2",
    "organizations/The_Ninth_Guild.md": "P3",
    "organizations/The_Order_of_the_Closed_Eye.md": "P3",
    "organizations/The_Severed_Coil.md": "P3",
    "organizations/The_Underclock.md": "P2",
    "organizations/The_Unwound.md": "P2",
    "locations/The_Aerial_Docks.md": "P1",
    "locations/The_Gardens_Airship_Landing.md": "P1",
    "locations/The_Moon_Garden.md": "P1",
    "locations/The_Entertainment_District.md": "P2",
    "locations/The_Cauldron.md": "P3",
}


@dataclass(frozen=True)
class Record:
    path: Path
    rel: str
    name: str
    kind: str
    metadata: dict[str, object]
    body: str


@dataclass(frozen=True)
class Task:
    task_id: str
    priority: str
    status: str
    label: str
    link: str
    kind: str
    action: str
    dependency: str = "—"


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
    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in front_matter.splitlines():
        if raw in {"---", ""} or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s*-\s+", raw) and current_list:
            item = clean_scalar(re.sub(r"^\s*-\s+", "", raw))
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


def record_from(path: Path, kind: str) -> Record:
    text = path.read_text(encoding="utf-8")
    front, body = split_front_matter(text)
    metadata = parse_simple_yaml(front)
    name = str(metadata.get("name") or metadata.get("title") or first_h1(body) or path.stem.replace("_", " "))
    return Record(path, path.relative_to(ROOT).as_posix(), name, kind, metadata, body)


def discover_profiles() -> list[Record]:
    records: list[Record] = []
    for kind, directory in PROFILE_DIRS.items():
        for path in sorted(directory.glob("*.md")):
            if path.name in EXCLUDED_NAMES:
                continue
            records.append(record_from(path, kind))
    for path in sorted((ROOT / "story_arcs").glob("*.md")):
        records.append(record_from(path, "Story Arc"))
    return records


def discover_artifacts() -> list[Record]:
    return [
        record_from(path, "Artifact")
        for path in sorted((ROOT / "artifacts").glob("*.md"))
        if path.name != "README.md"
    ]


def priority_for_profile(record: Record) -> str:
    if record.rel in DECISION_REQUIRED or record.rel in BLOCKED_EXPANSION:
        return "P0"
    if record.rel in P1_PATHS:
        return "P1"
    if record.rel in P2_PATHS:
        return "P2"
    if record.rel in P3_PATHS:
        return "P3"
    if record.rel in P4_PATHS:
        return "P4"
    if record.rel in DEFERRED_EXPANSION:
        return "P4"
    if record.kind == "Story Arc":
        return "P2"
    return "P3"


def expansion_status(record: Record) -> tuple[str, str]:
    if record.rel in BLOCKED_EXPANSION:
        return "BLOCKED", BLOCKED_EXPANSION[record.rel]
    if record.rel in DECISION_REQUIRED:
        return "NEEDS DECISION", DECISION_REQUIRED[record.rel]
    if record.rel in DEFERRED_EXPANSION:
        return "DEFERRED", "Keep the source-grounded placeholder current; perform final synthesis only after surrounding canon stabilizes."
    if record.rel in ROLE_ONLY_EXPANSION:
        return "READY", "Expand the role, public function, relationships, constraints, and visual identity without assigning the concealed officeholder or hidden identity."
    if record.kind == "Character":
        return "READY", "Replace the placeholder with a full character profile: public identity, personality, relationships, secrets, staged reveals, visual continuity, constraints, and open questions."
    if record.kind == "Organization":
        return "READY", "Replace the placeholder with a full organization profile: purpose, charter, structure, leadership, membership, jurisdiction, relationships, visual language, secrets, and constraints."
    if record.kind == "Location":
        return "READY", "Replace the placeholder with a full location profile: public map summary, map callout, boundaries, points of interest, governance, social character, visual continuity, hidden canon, and story hooks."
    return "READY", "Expand the profile while preserving established canon and avoiding duplicated history owned by linked records."


def is_placeholder(record: Record) -> bool:
    status = str(record.metadata.get("canon_status", ""))
    return "placeholder" in status.casefold()


def active_image_links(record: Record) -> list[str]:
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", record.body)
    values = record.metadata.get("canonical_images")
    if isinstance(values, list):
        links.extend(str(item) for item in values if item and str(item).casefold() != "null")
    return list(dict.fromkeys(links))


def visual_is_complete(record: Record) -> bool:
    links = active_image_links(record)
    if not links:
        return False
    if record.kind == "Location":
        meaningful = [
            link for link in links
            if "Map_of_Aetherhaven" not in link and "Background" not in link
        ]
        return bool(meaningful)
    return True


def visual_task(record: Record, sequence: int) -> Task | None:
    if visual_is_complete(record):
        return None

    priority = VISUAL_PRIORITY_OVERRIDES.get(record.rel, priority_for_profile(record))
    status, known_action = KNOWN_VISUALS.get(record.rel, ("READY", ""))

    if record.rel in BLOCKED_EXPANSION:
        status = "BLOCKED"
    elif record.rel in DECISION_REQUIRED and status == "READY":
        status = "PARTIAL"

    if known_action:
        action = known_action
    elif record.kind == "Character":
        if record.rel == "characters/The_Hidden_Architect_Unassigned.md":
            action = "Create a spoiler-safe silhouette or indirect visual motif; do not reveal or imply the eventual identity. Embed it under `Visual Reference`."
        elif record.rel in ROLE_ONLY_EXPANSION:
            action = "Create a role-based portrait, seal, silhouette, or office artifact that does not assign the concealed officeholder. Embed it under `Visual Reference`."
        else:
            action = "Generate or select a canonical portrait, photograph, or silhouette using established character continuity; embed it under `Visual Reference` and add descriptive alt text."
    elif record.kind == "Organization":
        action = "Generate or link a canonical crest, seal, badge, representative artifact, uniform element, or headquarters image; embed it under `Visual Reference`."
    elif record.kind == "Location":
        action = "Add a labeled Aetherhaven map callout and generate or select at least one canonical establishing image; embed both under `Map Reference` and `Visual Reference`."
    else:
        action = "Generate representative, spoiler-controlled arc art and embed it without duplicating character, location, or artifact canon."

    dependency = "Complete or stabilize the linked expansion task first." if is_placeholder(record) else "—"
    if status == "BLOCKED":
        dependency = BLOCKED_EXPANSION.get(record.rel, "Resolve canon blocker before visual production.")

    return Task(
        f"VIS-{sequence:03d}", priority, status, record.name,
        record.rel, record.kind, action, dependency,
    )


def section_text(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    if not match:
        return ""
    content = match.group(1).strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
    return paragraphs[0] if paragraphs else ""


def artifact_priority(record: Record) -> str:
    status = str(record.metadata.get("canon_status", ""))
    if "requires-canon-review" in status:
        return "P0"
    number = int(str(record.metadata.get("slate_number", "999")))
    if number in {2, 6}:
        return "P0"
    if 5 <= number <= 28:
        return "P1"
    if 29 <= number <= 48:
        return "P2"
    if 49 <= number <= 56:
        return "P3"
    return "P4"


def artifact_task(record: Record) -> Task | None:
    image_status = str(record.metadata.get("image_status", "")).casefold()
    if image_status == "image-linked":
        return None

    number = int(str(record.metadata.get("slate_number", "999")))
    canon_status = str(record.metadata.get("canon_status", ""))
    intended = section_text(record.body, "Intended Form")
    priority = artifact_priority(record)

    if "requires-canon-review" in canon_status:
        status = "BLOCKED"
        action = "Resolve whether the implied organization, history, and artifact belong in active canon. Only then finalize the artifact concept and generate art."
        dependency = "Explicit canon approval required."
    elif image_status == "provisional-variants":
        status = "NEEDS DECISION"
        action = "Choose one canonical seal, or document distinct in-world uses for both variants; then update the artifact record and all organization backlinks."
        dependency = "Seal-variant decision."
    elif image_status == "working-placeholder":
        status = "PARTIAL"
        action = "Select the final archive-label design, generate the production asset, then transcribe every visible field and document the completed plate."
        dependency = "Final archive-label design."
    else:
        status = "READY"
        form = f" Create it as: {intended}" if intended else ""
        action = "Generate the canonical artifact image using the archival plate standard." + form + " After approval, embed the image, transcribe all visible text, add the complete visual-only description, and separate non-visual story canon."
        dependency = "Stabilize linked profile canon before final text is placed on the image."

    return Task(
        f"ART-{number:03d}", priority, status, record.name,
        record.rel, "Artifact", action, dependency,
    )


def task_sort_key(task: Task) -> tuple[int, int, str, str]:
    p = int(task.priority[1:])
    return p, STATUS_ORDER.get(task.status, 99), task.kind, task.label.casefold()


def markdown_link(task: Task) -> str:
    return f"[{task.label}]({task.link})"


def render_table(tasks: list[Task]) -> list[str]:
    lines = [
        "| Task | Priority | Status | Element | Type | Required work | Dependency |",
        "|---|---:|---|---|---|---|---|",
    ]
    for task in tasks:
        action = task.action.replace("|", "\\|").replace("\n", " ")
        dep = task.dependency.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{task.task_id}` | **{task.priority}** | **{task.status}** | {markdown_link(task)} | {task.kind} | {action} | {dep} |"
        )
    return lines


def global_tasks() -> list[Task]:
    return [
        Task("SYS-001", "P0", "READY", "Canon authority and contradiction policy", "PROJECT_INDEX.md", "System", "For each expanded placeholder, explicitly record which PDF/DOCX details remain canonical, which are superseded, and which stay unresolved; never silently reconcile conflicts.", "Complete during every placeholder conversion."),
        Task("SYS-002", "P1", "READY", "Canonical visual integration standard", "CANON_MARKDOWN_STANDARD.md", "System", "Require every character, organization, location, story arc, and artifact record to embed its active canonical visuals with descriptive alt text and links to the authoritative image or artifact record.", "Apply during every visual task."),
        Task("SYS-003", "P2", "READY", "Location map-callout migration", "Map_Location_Reference_Style_Guide.md", "System", "Add a clear map callout to every location profile, including hidden or restricted-location handling where a public pin would be inappropriate.", "Complete alongside location visual tasks."),
        Task("SYS-004", "P5", "READY", "Artifact backlinks", "artifacts/README.md", "System", "Add backlinks from every directly related character, organization, location, and story-arc profile to its artifact records; avoid duplicating artifact descriptions in those profiles.", "Artifact and profile records must both exist."),
        Task("SYS-005", "P6", "READY", "Accessibility and AI-ingestion review", "CANON_MARKDOWN_STANDARD.md", "System", "Review headings, YAML IDs, alt text, link labels, canon-status fields, TODO checkboxes, and visual descriptions for precise AI-agent ingestion and human accessibility.", "Run after each priority wave."),
        Task("SYS-006", "P6", "READY", "Broken-link and duplicate-canon audit", "PROJECT_INDEX.md", "System", "Validate all relative Markdown links, ensure one authoritative owner for each canon fact, remove accidental duplicated summaries, and retain stable file paths when placeholders become completed profiles.", "Run after each priority wave."),
        Task("SYS-007", "P6", "READY", "Unused-art exclusion check", "CANON_MARKDOWN_STANDARD.md", "System", "Confirm no Markdown file, prompt, image reference, or generated asset uses material from `unused/` unless the project owner explicitly restores a named item.", "Continuous requirement."),
        Task("SYS-008", "P6", "READY", "Project index maintenance", "PROJECT_INDEX.md", "System", "Update completed/placeholder/image counts, remove finished work from the active queue, and keep this TODO file synchronized after every merged canon or art batch.", "Continuous requirement."),
    ]


def main() -> int:
    profiles = discover_profiles()
    artifacts = discover_artifacts()

    expansion_tasks: list[Task] = []
    exp_sequence = 1
    for record in profiles:
        if not is_placeholder(record):
            continue
        status, action = expansion_status(record)
        dependency = "—"
        if status == "BLOCKED":
            dependency = BLOCKED_EXPANSION.get(record.rel, "Canon decision required.")
        elif status == "NEEDS DECISION":
            dependency = DECISION_REQUIRED.get(record.rel, "Source reconciliation required.")
        elif status == "DEFERRED":
            dependency = "Most surrounding canon should be complete before final synthesis."
        expansion_tasks.append(Task(
            f"EXP-{exp_sequence:03d}", priority_for_profile(record), status,
            record.name, record.rel, record.kind, action, dependency,
        ))
        exp_sequence += 1

    visual_tasks: list[Task] = []
    vis_sequence = 1
    for record in profiles:
        task = visual_task(record, vis_sequence)
        if task:
            visual_tasks.append(task)
            vis_sequence += 1

    artifact_tasks = [task for record in artifacts if (task := artifact_task(record))]

    expansion_tasks.sort(key=task_sort_key)
    visual_tasks.sort(key=task_sort_key)
    artifact_tasks.sort(key=task_sort_key)
    systems = sorted(global_tasks(), key=task_sort_key)

    all_tasks = expansion_tasks + visual_tasks + artifact_tasks + systems
    status_counts: dict[str, int] = {}
    for task in all_tasks:
        status_counts[task.status] = status_counts.get(task.status, 0) + 1

    lines: list[str] = [
        "# The Brass Guardian — Canon Development TODO",
        "",
        "> **Single operational queue.** This file lists every currently identified profile requiring expansion, every canonical profile or arc still needing integrated imagery, every unfinished artifact image, and the cross-cutting work required to keep the repository coherent.",
        "",
        f"**Last generated:** {TODAY}  ",
        "**Source authority:** Active Markdown first; compiled PDF/DOCX only for gaps; `unused/` is never a source.",
        "",
        "## How to Use This Queue",
        "",
        "Work from the lowest priority number upward. Within a priority, complete blockers and source decisions before prose expansion, and complete prose stabilization before final image generation containing labels, dates, names, or story evidence.",
        "",
        "When a task is completed:",
        "",
        "1. Update the linked Markdown file and its embedded TODO checklist.",
        "2. Change the task status here to `COMPLETE` or remove it during the next generated audit.",
        "3. Preserve the file path so all inbound links remain valid.",
        "4. Update `PROJECT_INDEX.md` counts and related backlinks.",
        "",
        "## Priority Index",
        "",
        "| Priority | Meaning |",
        "|---:|---|",
    ]
    for priority, label in PRIORITY_LABELS.items():
        lines.append(f"| **{priority}** | {label} |")

    lines.extend([
        "",
        "## Status Index",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| **BLOCKED** | Cannot proceed without new canon, source material, or an explicit decision. |",
        "| **NEEDS DECISION** | Conflicting or provisional source details must be reconciled before final expansion or art. |",
        "| **READY** | Can be worked now using active Markdown and supplied source material. |",
        "| **PARTIAL** | Some content or imagery already exists, but integration or final production remains incomplete. |",
        "| **DEFERRED** | Intentionally postponed until dependent canon is more stable. |",
        "| **COMPLETE** | Finished and removed from the active generated queue on the next audit. |",
        "",
        "## Queue Summary",
        "",
        f"- **{len(expansion_tasks)}** placeholder-expansion tasks",
        f"- **{len(visual_tasks)}** profile and story-arc visual tasks",
        f"- **{len(artifact_tasks)}** artifact image/finalization tasks",
        f"- **{len(systems)}** cross-cutting integration and QA tasks",
        f"- **{len(all_tasks)} total active tasks**",
        "",
    ])
    for status in ["BLOCKED", "NEEDS DECISION", "READY", "PARTIAL", "DEFERRED"]:
        lines.append(f"- **{status}:** {status_counts.get(status, 0)}")

    lines.extend([
        "",
        "## 1. Placeholder Expansion Queue",
        "",
        "These tasks convert source-grounded placeholders into complete canon profiles. The queue is sorted by dependency and narrative usefulness rather than alphabetically.",
        "",
        *render_table(expansion_tasks),
        "",
        "## 2. Character, Organization, Location, and Story-Arc Visual Queue",
        "",
        "Every active profile should eventually embed a canonical visual. Location rows include both a map callout and a dedicated establishing image. A visual task may proceed before final prose only when the image cannot accidentally lock unresolved canon.",
        "",
        *render_table(visual_tasks),
        "",
        "## 3. Artifact Image Production and Finalization Queue",
        "",
        "Artifact art should be created only after the linked canon is stable enough to support visible names, dates, labels, seals, redactions, and recovery metadata. After each image is approved, its Markdown record must receive a full transcription and complete visual-only description.",
        "",
        *render_table(artifact_tasks),
        "",
        "## 4. Cross-Cutting Repository Tasks",
        "",
        *render_table(systems),
        "",
        "## Recommended Completion Waves",
        "",
        "### Wave 1 — Resolve blockers and stabilize the center",
        "",
        "Complete all `P0` decisions, then expand Aetherhaven, the Aetherium/Heart Engine, the Clockwork Gardens, the Grand Atrium, the Engine Complex, the Gearbreaker Mines, the Academy, the Archives, and the highest-use recurring supporting cast.",
        "",
        "### Wave 2 — Complete the public city",
        "",
        "Expand and illustrate numbered map locations, the civic institutions that govern them, and the recurring venues used by ordinary citizens and early stories.",
        "",
        "### Wave 3 — Complete the hidden city",
        "",
        "Develop restricted areas, concealed offices, mystery figures, secret organizations, and role-based visuals that preserve unresolved identities.",
        "",
        "### Wave 4 — Produce story-linked artifact sets",
        "",
        "Generate artifacts in complete narrative clusters—Gauntlet, Gardens, Thirteenth Canal, Passenger, Clocktower, Gearbreaker, Reflection, Living Key, organizations, and transitional lore—rather than isolated images with no surrounding profile support.",
        "",
        "### Wave 5 — Finish secondary regions and final protagonist synthesis",
        "",
        "Complete distant-region placeholders and, once the surrounding canon is mature, perform the final comprehensive Elias and Amelia profile synthesis without changing their established file paths.",
        "",
        "## Completion Definition",
        "",
        "A profile is not complete until it has:",
        "",
        "- stable YAML metadata and canon status,",
        "- a concise canonical summary,",
        "- linked relationships rather than duplicated biographies,",
        "- public and restricted information separated where necessary,",
        "- visual continuity and an embedded canonical image or documented exception,",
        "- continuity constraints and open canon questions,",
        "- backlinks to directly related artifacts and arcs,",
        "- and no dependency on material from `unused/`.",
        "",
        "An artifact is not complete until it has an approved active image, exact visible-text transcription, complete visual-only plate description, separated non-visual story context, descriptive alt text, and backlinks from directly related profiles.",
        "",
    ])

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(all_tasks)} active tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
