#!/usr/bin/env python3
"""Create missing placeholder profiles for named canon entities.

The source material for these placeholders is Aetherhaven v3.pdf together with
existing canonical Markdown already present in this repository. Placeholders are
intentionally concise and must not silently resolve contradictions or open canon.
Existing files are never overwritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-02"
SERIES = "The Brass Guardian / The Aetherhaven Chronicles"


@dataclass(frozen=True)
class Profile:
    path: str
    name: str
    summary: str
    source_basis: str = "Aetherhaven v3.pdf"
    aliases: tuple[str, ...] = ()
    title: str = ""
    map_number: str = ""
    map_category: str = "unlisted"
    parent_location: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)


def yaml_list(values: Iterable[str], indent: int = 0) -> str:
    values = tuple(v for v in values if v)
    if not values:
        return "[]"
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}  - {value}" for value in values)


def character_text(profile: Profile, index: int) -> str:
    notes = "\n".join(f"- {note}" for note in profile.notes) or "- Expand from later canon review."
    return f"""---
character_id: AH-CHAR-PLACEHOLDER-{index:03d}
name: {profile.name}
title: {profile.title}
aliases:{yaml_list(profile.aliases)}
series: {SERIES}
canon_status: Source-grounded placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
primary_locations: []
affiliations: []
key_connections: []
temporal_relevance: Unresolved
source_basis:
  - {profile.source_basis}
---

# {profile.name}

> **Placeholder profile.** This file exists so references can resolve to one authoritative record. It records only what the cited source currently supports and does not supersede more developed canon elsewhere in the repository.

## Canonical Summary

{profile.summary}

## Source Notes

{notes}

## Public Role

Pending expansion. Preserve the source description without adding unsupported biography, motives, affiliations, or chronology.

## Relationships

Relationships explicitly named in the source may be linked here during later expansion. No unassigned relationship should be treated as established merely because this placeholder exists.

## Hidden History

Unassigned. Do not infer a hidden identity, allegiance, or temporal origin from the placeholder.

## Visual Continuity

Use only source-supported details until a dedicated visual profile is approved.

## Continuity Constraints

- This is a placeholder, not a completed character profile.
- Source contradictions remain visible and unresolved.
- Unknown identity, age, allegiance, chronology, and motive must not be invented.
- Replace or expand this file rather than creating a duplicate profile later.

## Open Canon Questions

1. Which source details remain authoritative after full canon review?
2. What relationships, visual elements, and staged revelations require confirmation?
3. Does this character need a full long-form profile or a deliberately limited mystery record?
"""


def organization_text(profile: Profile, index: int) -> str:
    notes = "\n".join(f"- {note}" for note in profile.notes) or "- Expand from later canon review."
    return f"""---
organization_id: AH-ORG-PLACEHOLDER-{index:03d}
name: {profile.name}
type: Placeholder organization profile
aliases:{yaml_list(profile.aliases)}
series: {SERIES}
canon_status: Source-grounded placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
headquarters: []
known_leadership: []
primary_connections: []
temporal_relevance: Unresolved
source_basis:
  - {profile.source_basis}
---

# {profile.name}

> **Placeholder profile.** This file provides a stable link target while the organization awaits full development. It does not expand beyond the cited source.

## Canonical Summary

{profile.summary}

## Source Notes

{notes}

## Public Role

Pending expansion from source-supported material.

## Structure and Membership

Unresolved unless explicitly stated in the source. Do not invent leadership, ranks, membership rules, headquarters, or jurisdiction.

## Relationships

Add only relationships already established in the source or current canonical Markdown.

## Continuity Constraints

- This is a placeholder, not a completed organization profile.
- Do not promote a subgroup, office, rumor, or title into a larger institution without confirmation.
- Do not merge this organization with another merely because their purposes overlap.
- Replace or expand this file rather than creating a duplicate profile later.

## Open Canon Questions

1. Is this organization independent, subordinate, informal, historical, or partly mythical?
2. Who leads it, and what authority does it actually possess?
3. Which current relationships and conflicts require a full profile?
"""


def location_text(profile: Profile, index: int) -> str:
    notes = "\n".join(f"- {note}" for note in profile.notes) or "- Expand from later canon review."
    map_number = profile.map_number or ""
    return f"""---
location_id: AH-LOC-PLACEHOLDER-{index:03d}
name: {profile.name}
type: Placeholder location profile
aliases:{yaml_list(profile.aliases)}
series: {SERIES}
canon_status: Source-grounded placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
jurisdiction: []
access_status: []
map_reference_category: {profile.map_category}
map_number: {map_number}
parent_location: {profile.parent_location}
primary_connections: []
points_of_interest: []
temporal_relevance: Unresolved
source_basis:
  - {profile.source_basis}
---

# {profile.name}

> **Placeholder profile.** This record provides a stable link target and preserves the source description until the location receives a complete profile.

## Map Reference

{('Canonical map reference: ' + profile.map_number + '.') if profile.map_number else 'No numbered or lettered map reference is currently assigned.'}

## Public Map Reference

{profile.summary}

## Canonical Summary

{profile.summary}

## Source Notes

{notes}

## Civic, Social, or Narrative Role

Pending expansion. Do not add hidden history, governing organizations, or access rules unless they are supported by the source or existing canon.

## Relationships

Link parent districts, organizations, recurring characters, and artifacts only when established.

## Visual Continuity

Use the source description as the temporary visual baseline. No generated image becomes canonical merely because this placeholder exists.

## Continuity Constraints

- This is a placeholder, not a completed location profile.
- Public map language must remain spoiler-light for numbered locations.
- Restricted locations must remain cautionary without resolving their central mystery.
- Do not merge this location with a similarly named institution, office, vessel, or artifact.
- Replace or expand this file rather than creating a duplicate profile later.

## Open Canon Questions

1. What are the confirmed boundaries, jurisdiction, and access rules?
2. Which points of interest deserve separate profiles?
3. What hidden or temporal details should remain restricted?
"""


CHARACTERS = (
    Profile("characters/Professor_Elias_Hawthorne.md", "Professor Elias Hawthorne", "A brilliant engineer and explorer known as the Brass Guardian. The source describes him as Amelia Hawthorne's father and as the builder of her mechanical arm after the Clockwork Jungle accident.", aliases=("Elias Hawthorne", "Elias", "The Brass Guardian"), title="The Brass Guardian", notes=("The source's description of the gauntlet being powered by Amelia's courage and compassion must be reconciled later with the established Aether Heart canon.",)),
    Profile("characters/Amelia_Hawthorne.md", "Amelia Hawthorne", "The young Clockwork Explorer and central Bearer figure of the series. The source describes her as nine years old, highly observant, mechanically gifted, and equipped with a brass mechanical right arm created after an expedition accident.", aliases=("Amelia", "The Clockwork Explorer"), title="The Clockwork Explorer", notes=("The source gives Amelia an age of nine; later canon review must determine whether this remains current.", "Amelia must always be treated as a person, never as a component, device, or civic property.")),
    Profile("characters/Doctor_Elara_Quill.md", "Doctor Elara Quill", "Chancellor of the Academy of Invention and one of Aetherhaven's most brilliant scholars. She becomes Amelia's informal mentor, discovered Prototype II in the Hall of Unfinished Ideas, and removed its original records because another party had begun searching for them.", aliases=("Elara Quill", "Elara", "Dr. Elara Quill"), title="Chancellor of the Academy of Invention"),
    Profile("characters/Master_Gideon_Brasswell.md", "Master Gideon Brasswell", "A highly respected engineer who maintains the oldest machinery beneath Aetherhaven. He has two mechanical hands, trained Elias as an apprentice, and carries an old guild medallion matching symbols found inside the Heart Engine.", aliases=("Gideon Brasswell", "Gideon"), title="Master Engineer"),
    Profile("characters/Orin_Flint.md", "Orin Flint", "Leader of the Miners' Guild and a veteran of the Gearbreaker Mines. He believes the tunnels are alive and carries a compass that points toward nearby metal rather than north.", aliases=("Orin",), title="Leader of the Miners' Guild"),
    Profile("characters/Lucian_Wren.md", "Lucian Wren", "A brilliant, elegant, and ambitious inventor who serves as Elias Hawthorne's professional rival. He seeks public acclaim, repeatedly fails to copy Elias's work, and unknowingly possesses a machine created by the First Mechanist.", aliases=("Lucian",), title="Inventor and professional rival"),
    Profile("characters/Barnaby_Wren.md", "Barnaby Wren", "A retired explorer and storyteller who owns the Last Lantern. His walls are covered in impossible maps, and his records indicate that he vanished for two years despite remembering only a few weeks.", aliases=("Barnaby",), title="Retired explorer and proprietor of the Last Lantern"),
    Profile("characters/Madame_Celestine_Mirrow.md", "Madame Celestine Mirrow", "The elegant and enigmatic mistress of the Theatre of Impossible Things. Her productions sometimes depict events before they happen, and she stages warnings rather than predicting the future directly.", aliases=("Celestine Mirrow", "Celestine", "Madame Mirrow"), title="Mistress of the Theatre of Impossible Things"),
    Profile("characters/Keeper_Thirteen.md", "Keeper Thirteen", "A planned character profile named in the supplied project material, but no descriptive entry for this figure was located in Aetherhaven v3.pdf.", title="Unresolved keeper designation", notes=("Do not infer that Keeper Thirteen is the First Mechanist, Keeper of Dreams, Juniper Bell, or the sealed Thirteenth Chair.",)),
    Profile("characters/The_First_Mechanist.md", "The First Mechanist", "An ancient office or person associated with the founding guilds, the Heart Engine, and the sealed Thirteenth Chair. Current source material does not establish how the First Mechanist is selected, whether the title belongs to one person, or who last held it.", aliases=("First Mechanist",), title="Ancient civic and engineering authority", source_basis="Aetherhaven v3.pdf and current canonical Markdown"),
    Profile("characters/The_Lady_in_the_Water.md", "The Lady in the Water", "A woman seen only in the reflections of the Reflection Canals. She resembles an older Amelia with a silver-white mechanical arm and has warned, 'Do not let him open the sixth door.'", aliases=("Lady in the Water",), title="Unidentified reflected woman"),
    Profile("characters/The_Ashen_Cartographer.md", "The Ashen Cartographer", "A masked traveler who leaves indelible ash maps in abandoned rooms, sealed vaults, and unexplored places. The newest known map depicts the interior of Amelia's mechanical arm with a room at its center.", aliases=("Ashen Cartographer", "The Cartographer"), title="Masked mapmaker"),
    Profile("characters/The_Null_Shepherd.md", "The Null Shepherd", "A child-sized figure seen in the Null Zone among silent mechanical animals that continue moving where other machines fail. After Amelia entered the region, the Shepherd began constructing the Hawthorne crest from black stones.", aliases=("Null Shepherd", "The Shepherd"), title="Unidentified figure of the Null Zone"),
    Profile("characters/The_Bellmaker.md", "The Bellmaker", "An elderly artisan whom no one remembers meeting, though bells bearing his mark appear throughout Aetherhaven. His bells ring for events rather than hours, and a tiny bell appeared in Amelia's satchel after her first visit to the Grand Atrium.", aliases=("Bellmaker",), title="Unremembered artisan"),
    Profile("characters/The_Cinder_Regent.md", "The Cinder Regent", "The currently unassigned civic authority associated with the Cauldron, Furnace Court, Ash Law, and enforcement of the Ash Compact.", aliases=("Cinder Regent",), title="Unassigned ruler of the Cauldron", source_basis="Current canonical Markdown", notes=("The identity remains deliberately unassigned.",)),
    Profile("characters/The_Curator.md", "The Curator", "The unidentified leader or central preserving authority of the Ninth Guild and Black Catalogue. The Curator is explicitly distinct from the Hidden Architect.", aliases=("Curator",), title="Leader of the Ninth Guild", source_basis="Aetherhaven v3.pdf and current canonical Markdown", notes=("The identity remains deliberately unassigned.",)),
    Profile("characters/The_First_Tender.md", "The First Tender", "The unassigned administrative leader of the Conservancy of Living Mechanisms. The office coordinates the Conservancy but is distinct from Juniper Bell's older title as Keeper of the Clockwork Gardens.", aliases=("First Tender",), title="Administrative leader of the Conservancy", source_basis="Current canonical Markdown", notes=("The identity remains deliberately unassigned.",)),
    Profile("characters/Euphemia_Pike.md", "Euphemia Pike", "A Pike family name visible on the canonical plate for Tamsin Pike's brass key. No further biography is established by the supplied source.", title="Pike family figure", source_basis="Canonical artifact plate and current Markdown"),
    Profile("characters/Beatrice_Pike.md", "Beatrice Pike", "A Pike family name visible on the canonical plate for Tamsin Pike's brass key. No further biography is established by the supplied source.", title="Pike family figure", source_basis="Canonical artifact plate and current Markdown"),
)


ORGANIZATIONS = (
    Profile("organizations/The_Academy_of_Invention.md", "The Academy of Invention", "Aetherhaven's principal institution for invention, engineering education, experimental research, and preservation of unfinished ideas. Doctor Elara Quill serves as its Chancellor.", aliases=("Academy of Invention", "the Academy")),
    Profile("organizations/The_Society_of_Explorers.md", "The Society of Explorers", "A chartered exploration society associated with expedition credentials, maps, field reports, and the Hawthornes. Existing source material suggests respectable public authority while leaving parts of its history and inner leadership unresolved.", aliases=("Society of Explorers", "Explorers' Society")),
    Profile("organizations/The_Quiet_Choir.md", "The Quiet Choir", "An underground network communicating through vibrations carried in Aetherhaven's pipes. Its leaders are unseen, and the source leaves unresolved whether it consists of workers and dissidents or a collective intelligence formed by ancient machines.", aliases=("Quiet Choir", "the Choir")),
    Profile("organizations/The_Aetherhaven_Archives.md", "The Aetherhaven Archives", "The civic archival institution responsible for restricted records, transit documents, artifact custody, and official history. Current canon repeatedly shows that its records may be incomplete, altered, redacted, or temporally unstable.", aliases=("Aetherhaven Archives", "civic Archives"), source_basis="Aetherhaven v3.pdf and current canonical Markdown"),
    Profile("organizations/The_Conclave_of_Eight.md", "The Conclave of Eight", "The assembly of the eight founding guildmasters, meeting in the Octagonal Hall to coordinate technical standards and advise Aetherhaven's government.", aliases=("Conclave of Eight", "the Conclave"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Furnace_Court.md", "The Furnace Court", "The Cauldron's governing court under Ash Law and the Cinder Regent. Its exact membership, procedures, and authority remain unresolved.", aliases=("Furnace Court",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Keepers_of_Time.md", "The Keepers of Time", "The mysterious order described as maintaining the great astronomical clock within Clocktower Spire. Their relationship to civic timekeeping and temporal anomalies remains unresolved.", aliases=("Keepers of Time",)),
    Profile("organizations/The_Handwright_Circles.md", "The Handwright Circles", "Practical local circles within the wider Unwound movement that preserve handcraft, repair knowledge, and manual alternatives to automated systems.", aliases=("Handwright Circles",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Free_Spring_Assembly.md", "The Free Spring Assembly", "A public political and reform wing within the wider Unwound movement, associated with petitions, broadsides, debate, transparency, and accountable infrastructure.", aliases=("Free Spring Assembly",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Clockkeepers_Without_Hours.md", "The Clockkeepers Without Hours", "An informal Unwound network preserving unsynchronized clocks, family ledgers, and contradictory calendars that may survive official chronological adjustment.", aliases=("Clockkeepers Without Hours",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Inner_Compass.md", "The Inner Compass", "A name associated with the concealed or senior leadership of the Society of Explorers. The supplied source does not establish its membership, authority, or current activity.", aliases=("Inner Compass",), source_basis="Aetherhaven v3.pdf and current canonical Markdown"),
    Profile("organizations/The_Cinder_Wardens.md", "The Cinder Wardens", "The enforcement body associated with Cauldron authority, Ash Law, the Furnace Court, and the Cinder Regent.", aliases=("Cinder Wardens",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Ash_Detail.md", "The Ash Detail", "An informal Brass Watch intelligence detail focused on the Cauldron, Ash Line, Entertainment District, and related criminal or political activity.", aliases=("Ash Detail",), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Miners_Guild.md", "The Miners' Guild", "The organization led by Orin Flint and associated with the Gearbreaker Mines, tunnel safety, extraction work, and knowledge of the mountain beneath Aetherhaven.", aliases=("Miners' Guild", "Miner's Guild")),
    Profile("organizations/The_Guild_of_Framewrights.md", "The Guild of Framewrights", "One of the Eight Founding Engineering Guilds, responsible for structures, architecture, foundations, and the physical frames upon which Aetherhaven rests.", aliases=("Guild of Framewrights", "Framewrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Enginewrights.md", "The Guild of Enginewrights", "One of the Eight Founding Engineering Guilds, responsible for steam, pressure, turbines, heavy machinery, and engine systems.", aliases=("Guild of Enginewrights", "Enginewrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Aetherwrights.md", "The Guild of Aetherwrights", "One of the Eight Founding Engineering Guilds, responsible for aetherstone, conduits, Golden Veins, and the controlled movement of aetheric power.", aliases=("Guild of Aetherwrights", "Aetherwrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Canalwrights.md", "The Guild of Canalwrights", "One of the Eight Founding Engineering Guilds, responsible for canals, locks, water systems, drainage, and sanitation.", aliases=("Guild of Canalwrights", "Canalwrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Skywrights.md", "The Guild of Skywrights", "One of the Eight Founding Engineering Guilds, responsible for airship design, lift systems, mooring towers, and aerial engineering.", aliases=("Guild of Skywrights", "Skywrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Clockwrights.md", "The Guild of Clockwrights", "One of the Eight Founding Engineering Guilds, responsible for clocks, synchronization, calendars, and civic measurement of time.", aliases=("Guild of Clockwrights", "Clockwrights"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Artificers.md", "The Guild of Artificers", "One of the Eight Founding Engineering Guilds, responsible for automata, prosthetics, optics, precision devices, and advanced mechanical craft.", aliases=("Guild of Artificers", "Artificers"), source_basis="Current canonical Markdown"),
    Profile("organizations/The_Guild_of_Verdant_Mechanists.md", "The Guild of Verdant Mechanists", "One of the Eight Founding Engineering Guilds, responsible for living machinery, botanical engineering, agricultural mechanisms, and systems joining growth with craft.", aliases=("Guild of Verdant Mechanists", "Verdant Mechanists"), source_basis="Current canonical Markdown"),
)


LOCATIONS = (
    Profile("locations/Aetherhaven.md", "Aetherhaven", "The City of Gears, Dreams and Discovery, built outward from the ancient Aetherium beneath the mountain. Its districts, gardens, canals, workshops, and aerial ports depend upon machinery whose full purpose remains unknown.", aliases=("City of Aetherhaven",)),
    Profile("locations/The_Aetherium.md", "The Aetherium", "At the center of Aetherhaven stands an enormous brass armillary surrounding a radiant sphere of condensed aether. Citizens call it the Heart Engine, and its rhythm changes are accompanied by every city clock losing exactly one second.", aliases=("Aetherium", "The Heart Engine", "Heart Engine"), map_number="1", map_category="numbered"),
    Profile("locations/The_Clockwork_Gardens.md", "The Clockwork Gardens", "The living and mechanical inner ring surrounding the Aetherium, filled with brass vines, clockwork pollinators, changing paths, and sealed mechanisms that respond to Amelia's arm.", aliases=("Clockwork Gardens",), map_number="2", map_category="numbered"),
    Profile("locations/The_Grand_Atrium.md", "The Grand Atrium", "A glass-domed conservatory containing tropical forests, rare flowers, indoor waterfalls, mechanical trees, and an orrery that tracks celestial bodies unknown to Aetherhaven's astronomers.", aliases=("Grand Atrium",), map_number="3", map_category="numbered"),
    Profile("locations/The_Clocktower_Spire.md", "The Clocktower Spire", "A towering civic clock containing thousands of visible gears and a great astronomical mechanism maintained by the Keepers of Time. Its deepest chamber contains a door that opens only when every clock in the city stops.", aliases=("Clocktower Spire",), map_number="4", map_category="numbered"),
    Profile("locations/The_Waterfall_Cascades.md", "The Waterfall Cascades", "A chain of waterfalls descending through terraced gardens, canal machinery, and public walks, combining civic waterworks with one of Aetherhaven's most celebrated views.", aliases=("Waterfall Cascades",), map_number="5", map_category="numbered"),
    Profile("locations/The_Reflection_Canals.md", "The Reflection Canals", "Mirror-like canals running through the inner city. Their waters sometimes reflect scenes, people, or skies that are not present above them.", aliases=("Reflection Canals",), map_number="6", map_category="numbered"),
    Profile("locations/The_Starlight_Walkways.md", "The Starlight Walkways", "Elevated illuminated paths and bridges that glow after dark, offering public views across the gardens, canals, and central districts.", aliases=("Starlight Walkways", "Starlight Walk"), map_number="7", map_category="numbered"),
    Profile("locations/The_Southern_Docks.md", "The Southern Docks", "The city's principal waterborne trade district, handling canal freight, river craft, warehouses, market traffic, and arrivals that do not come by air.", aliases=("Southern Docks",), map_number="9", map_category="numbered"),
    Profile("locations/The_Brass_Gate.md", "The Brass Gate", "A monumental civic entrance and defensive gateway whose great mechanisms regulate passage into the older central city.", aliases=("Brass Gate",), map_number="10", map_category="numbered"),
    Profile("locations/The_Government_District.md", "The Government District", "The formal civic quarter containing the High Chamber, council offices, courts, public petition spaces, and institutions responsible for Aetherhaven's laws and administration.", aliases=("Government District",), map_number="11", map_category="numbered"),
    Profile("locations/The_Merchant_District.md", "The Merchant District", "A busy commercial quarter of exchanges, counting houses, shops, warehouses, guild offices, and markets serving citizens and visiting traders.", aliases=("Merchant District",), map_number="12", map_category="numbered"),
    Profile("locations/The_Inventors_District.md", "The Inventors' District", "A neighborhood of workshops, laboratories, prototype halls, rented attics, lecture rooms, and experimental machinery surrounding the Academy of Invention.", aliases=("Inventors' District", "Inventors District"), map_number="13", map_category="numbered"),
    Profile("locations/The_Industrial_District.md", "The Industrial District", "A working district of factories, foundries, pressure lines, rail spurs, repair yards, and heavy machinery supporting the city's public systems.", aliases=("Industrial District",), map_number="14", map_category="numbered"),
    Profile("locations/The_Old_City.md", "The Old City", "The oldest inhabited streets of Aetherhaven, where modern buildings stand over foundations, passages, and command systems predating accepted civic history.", aliases=("Old City",), map_number="15", map_category="numbered"),
    Profile("locations/The_Canal_District.md", "The Canal District", "A dense district shaped by locks, bridges, water stairs, workshops, homes, markets, and the hidden routes used by canal guides and the Underclock.", aliases=("Canal District",), map_number="16", map_category="numbered"),
    Profile("locations/The_Workers_Dormitories.md", "The Workers' Dormitories", "A large residential district for miners, engineers, foundry workers, and their families, with strong community kitchens, schools, meeting halls, rooftop gardens, and old service tunnels.", aliases=("Workers' Dormitories", "Workers Dormitories"), map_number="18", map_category="numbered"),
    Profile("locations/The_Great_Workshops.md", "The Great Workshops", "Sprawling halls where mechanists construct locomotives, airships, automata, and experimental engines. Elias maintains a private workspace in the eastern hall.", aliases=("Great Workshops",), map_number="20", map_category="numbered"),
    Profile("locations/The_Engine_Complex.md", "The Engine Complex", "A fortified industrial facility regulating the transfer of power from the Aetherium into Aetherhaven's public systems through pressure chambers, turbines, and distribution regulators.", aliases=("Engine Complex",), map_number="21", map_category="numbered"),
    Profile("locations/The_Gearbreaker_Mines.md", "The Gearbreaker Mines", "Ancient mines descending through the mountain beneath Aetherhaven. Their tunnels produce ore, expose forgotten mechanisms, and sometimes appear to change or respond to those who enter.", aliases=("Gearbreaker Mines",), map_number="22", map_category="numbered"),
    Profile("locations/The_Observatory.md", "The Observatory", "A public astronomical observatory studying Aetherhaven's skies, distant bodies, and unusual celestial events from the city's upper reaches.", aliases=("Observatory",), map_number="23", map_category="numbered"),
    Profile("locations/The_Academy_of_Invention_Campus.md", "The Academy of Invention Campus", "The map location occupied by the Academy's lecture halls, laboratories, collections, prototype rooms, and Hall of Unfinished Ideas.", aliases=("Academy campus", "Academy of Invention campus"), map_number="24", map_category="numbered"),
    Profile("locations/The_Obsidian_Spire.md", "The Obsidian Spire", "Restricted Area A, a dark and heavily controlled spire whose origin, access systems, and present purpose remain unresolved.", aliases=("Obsidian Spire",), map_number="A", map_category="restricted"),
    Profile("locations/The_Shrouded_Vaults.md", "The Shrouded Vaults", "Restricted Area B, a sealed complex of ancient chambers associated with denied expeditions, altered records, and mechanisms whose recognition may itself be dangerous.", aliases=("Shrouded Vaults",), map_number="B", map_category="restricted"),
    Profile("locations/The_Echoing_Depths.md", "The Echoing Depths", "Restricted Area C, a deep subterranean region where sound, machinery, and distance behave unreliably and where official maps remain incomplete.", aliases=("Echoing Depths",), map_number="C", map_category="restricted"),
    Profile("locations/The_Silent_Observatory.md", "The Silent Observatory", "Restricted Area D, an isolated observatory whose instruments, records, and silence distinguish it from the public Observatory.", aliases=("Silent Observatory",), map_number="D", map_category="restricted"),
    Profile("locations/The_Null_Zone.md", "The Null Zone", "Restricted Area F, a region where ordinary machines fail. The Null Shepherd and silent mechanical animals have nevertheless been observed moving within it.", aliases=("Null Zone",), map_number="F", map_category="restricted"),
    Profile("locations/The_Clockwork_Jungle.md", "The Clockwork Jungle", "The expedition region where Amelia's arm was injured according to the supplied source. It contains living and mechanical wilderness, ancient structures, and dangers not yet fully reconciled with current canon.", aliases=("Clockwork Jungle",)),
    Profile("locations/The_Skyward_Cliffs.md", "The Skyward Cliffs", "The high cliff region associated with the Wayfinder's exterior view, aerial approaches, and Amelia's sleeping quarters in the supplied source.", aliases=("Skyward Cliffs",)),
    Profile("locations/The_Skyward_Isles.md", "The Skyward Isles", "A distant aerial region reached by airship from Aetherhaven, known through routes, travelers, and expedition stories rather than sustained early-volume exploration.", aliases=("Skyward Isles",)),
    Profile("locations/Cloudspire.md", "Cloudspire", "A distant settlement or region served by aerial routes from Aetherhaven. Its complete geography and political status remain undeveloped.", aliases=()),
    Profile("locations/The_Southern_Seas.md", "The Southern Seas", "A distant maritime region referenced through trade, navigation, and expedition accounts. It remains outside the main early-volume setting.", aliases=("Southern Seas",)),
    Profile("locations/The_Shattered_Lands.md", "The Shattered Lands", "A distant region associated with the Returning Star and dangerous aerial routes. Its full geography and chronology remain unresolved.", aliases=("Shattered Lands",)),
    Profile("locations/The_Verdant_Wilds.md", "The Verdant Wilds", "A distant living wilderness referenced through explorers, plants, cargo, and stories while the main volumes remain centered on Aetherhaven.", aliases=("Verdant Wilds",)),
    Profile("locations/The_Thirteenth_Canal.md", "The Thirteenth Canal", "An old or unofficial canal route associated with Tamsin Pike, inherited keys, Underclock passage, and waterways the recognized city does not fully acknowledge.", aliases=("Thirteenth Canal",), source_basis="Current canonical Markdown"),
    Profile("locations/Pike_Bridge.md", "Pike Bridge", "A named canal bridge associated with the Pike family, an old lock inscription, and Tamsin Pike's inherited route history.", aliases=(), source_basis="Canonical artifact slate and current Markdown"),
    Profile("locations/The_Last_Lantern.md", "The Last Lantern", "Barnaby Wren's shop and gathering place, filled with impossible maps, explorer stories, old objects, and records of journeys that do not fit official time.", aliases=("Last Lantern",)),
    Profile("locations/The_Theatre_of_Impossible_Things.md", "The Theatre of Impossible Things", "Aetherhaven's celebrated theatre owned by Madame Celestine Mirrow, where performances sometimes portray events before they occur.", aliases=("Theatre of Impossible Things",), parent_location="The Entertainment District"),
    Profile("locations/The_Hall_of_Unfinished_Ideas.md", "The Hall of Unfinished Ideas", "An Academy chamber containing abandoned, incomplete, or unresolved inventions. Doctor Elara Quill found the mechanical arm marked Prototype II there.", aliases=("Hall of Unfinished Ideas",), parent_location="The Academy of Invention Campus"),
    Profile("locations/The_High_Chamber.md", "The High Chamber", "The circular council chamber in the Government District containing the Twelve Seats, Chancellor's dais, Petition Floor, Continuance Dial, and sealed Thirteenth Chair.", aliases=("High Chamber",), parent_location="The Government District", source_basis="Current canonical Markdown"),
    Profile("locations/The_Octagonal_Hall.md", "The Octagonal Hall", "The meeting place of the Conclave of Eight, designed around the symbols and technical traditions of the founding engineering guilds.", aliases=("Octagonal Hall",), source_basis="Current canonical Markdown"),
    Profile("locations/The_Pulse_Chamber.md", "The Pulse Chamber", "The deepest control room named by Engine Complex operators, restricted to senior personnel and connected to the regulation of power from the Aetherium.", aliases=("Pulse Chamber",), parent_location="The Engine Complex"),
    Profile("locations/Dock_Zero.md", "Dock Zero", "A sealed hangar and mooring complex at the Aerial Docks that predates the recognized port. Its lights activate during storms, and the Passenger repeatedly waits nearby for the Morningstar.", aliases=(), parent_location="The Aerial Docks", source_basis="Aetherhaven v3.pdf and current canonical Markdown"),
    Profile("locations/The_Quiet_Hangar.md", "The Quiet Hangar", "A restricted quarantine and evidence hangar at the Aerial Docks where the Resolute is believed to remain sealed. Its clocks are isolated from the civic synchronization network.", aliases=("Quiet Hangar",), parent_location="The Aerial Docks", source_basis="Current canonical Markdown"),
    Profile("locations/The_Morningstar_Berth.md", "The Morningstar Berth", "A permanently reserved berth at the Gardens Airship Landing for a vessel absent from current registries. Its reservation survives administrative changes and may function as a chronal anchor.", aliases=("Morningstar Berth",), parent_location="The Gardens Airship Landing", source_basis="Current canonical Markdown"),
    Profile("locations/The_Wayfinder_Berth.md", "The Wayfinder Berth", "The familiar berth at the Gardens Airship Landing used by Elias and Amelia Hawthorne's vessel, the Wayfinder.", aliases=("Wayfinder Berth",), parent_location="The Gardens Airship Landing", source_basis="Current canonical Markdown"),
    Profile("locations/Lamplighters_Hall.md", "Lamplighters' Hall", "The headquarters and meeting hall of the Lamplighters' Fellowship, containing the Homecoming Flame that recently changed from gold to blue.", aliases=("Lamplighters Hall",), source_basis="Aetherhaven v3.pdf and current canonical Markdown"),
    Profile("locations/Mariners_Hall.md", "Mariners' Hall", "The Aerial Mariners' Union headquarters at the Aerial Docks, containing meeting spaces, the Weather Loft, Chart Vault, Memorial Rigging, and Starless Room.", aliases=("Mariners Hall",), parent_location="The Aerial Docks", source_basis="Current canonical Markdown"),
    Profile("locations/Rootglass_Cloister.md", "Rootglass Cloister", "The Conservancy of Living Mechanisms' headquarters and sanctuary, including communal, healing, listening, archival, and introduction spaces.", aliases=("The Rootglass Cloister",), parent_location="The Clockwork Gardens", source_basis="Current canonical Markdown"),
)


def write_profile(profile: Profile, kind: str, index: int) -> bool:
    target = ROOT / profile.path
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    if kind == "character":
        text = character_text(profile, index)
    elif kind == "organization":
        text = organization_text(profile, index)
    else:
        text = location_text(profile, index)
    target.write_text(text, encoding="utf-8")
    return True


def write_index() -> None:
    target = ROOT / "docs/development/PLACEHOLDER_PROFILE_INDEX.md"
    sections = [
        ("Character Placeholders", CHARACTERS),
        ("Organization Placeholders", ORGANIZATIONS),
        ("Location Placeholders", LOCATIONS),
    ]
    lines = [
        "# Source-Grounded Placeholder Profile Index",
        "",
        "> Generated from **Aetherhaven v3.pdf** and existing canonical Markdown on 2026-08-02. These files provide stable link targets and preserve source-supported information until each entity receives a full review.",
        "",
        "A placeholder does not resolve contradictions, assign unknown identities, or supersede a completed canonical profile.",
        "",
    ]
    for heading, profiles in sections:
        lines.extend([f"## {heading}", "", "| Entity | File |", "|---|---|"])
        for profile in profiles:
            rel = Path(profile.path)
            lines.append(f"| {profile.name} | [{rel.name}]({rel.as_posix()}) |")
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    created: list[str] = []
    for index, profile in enumerate(CHARACTERS, start=1):
        if write_profile(profile, "character", index):
            created.append(profile.path)
    for index, profile in enumerate(ORGANIZATIONS, start=1):
        if write_profile(profile, "organization", index):
            created.append(profile.path)
    for index, profile in enumerate(LOCATIONS, start=1):
        if write_profile(profile, "location", index):
            created.append(profile.path)
    write_index()
    print(f"Created {len(created)} missing placeholder profiles.")
    for path in created:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
