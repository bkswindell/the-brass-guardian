#!/usr/bin/env python3
"""Create and integrate the Order of the Mended Hand placeholder network.

This migration establishes a distributed civic medical institution without
prematurely defining its leadership, every branch, or the exact medical team
involved in Amelia Hawthorne's survival after the Clockwork Jungle disaster.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-02"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized = content.strip() + "\n"
    if not target.exists() or target.read_text(encoding="utf-8") != normalized:
        target.write_text(normalized, encoding="utf-8")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def save(path: str, text: str) -> None:
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8")


def add_yaml_item(text: str, key: str, item: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\n(?P<body>(?:  - .*\n)*)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return text
    body = match.group("body")
    if f"  - {item}\n" in body:
        return text
    replacement = f"{key}:\n{body}  - {item}\n"
    return text[: match.start()] + replacement + text[match.end() :]


def replace_empty_yaml_list(text: str, key: str, items: list[str]) -> str:
    old = f"{key}: []"
    if old not in text:
        for item in items:
            text = add_yaml_item(text, key, item)
        return text
    replacement = key + ":\n" + "".join(f"  - {item}\n" for item in items).rstrip()
    return text.replace(old, replacement, 1)


def insert_section_before(text: str, heading: str, content: str, before: str) -> str:
    block = f"## {heading}\n\n{content.strip()}\n\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text)

    marker = f"## {before}\n"
    if marker in text:
        return text.replace(marker, block + marker, 1)

    return text.rstrip() + "\n\n" + block


def organization_profile() -> str:
    return f"""
---
organization_id: AH-ORG-PLACEHOLDER-024
name: The Order of the Mended Hand
type: Distributed civic medical, surgical, rehabilitation, prosthetics, and field-response institution
aliases:
  - The Hand
  - Order of the Mended Hand
  - The Hand
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Owner-directed canonical placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
headquarters:
  - The Hall of Vital Mechanics, Government District
known_leadership: []
primary_connections:
  - The Government District
  - The Academy of Invention
  - The Great Workshops
  - The Cauldron
  - The Brass Watch
  - The Mechanists' Guild
  - The Society of Explorers
  - Professor Elias Hawthorne
  - Amelia Hawthorne
  - The Clockwork Jungle Expedition
temporal_relevance: High
source_basis:
  - Owner canon decision recorded August 2, 2026
---

# The Order of the Mended Hand

> **Canonical working placeholder.** This institution exists throughout Aetherhaven and its expeditionary networks. Its exact final name, leadership, internal ranks, branch names, and historical role remain open for later development.

## Canonical Summary

The Order of the Mended Hand is Aetherhaven's principal civic institution for advanced medicine, emergency surgery, trauma care, rehabilitation, prosthetics, implants, mechanobiology, and the safe integration of living bodies with mechanical technology.

It is not a separate medical district and does not replace every neighborhood healer, private physician, apothecary, midwife, workshop medic, or community clinic.

Instead, the Order operates as a distributed medical network with:

- a central hospital and administrative institution in [the Government District](../locations/The_Government_District.md);
- clinical and research staff embedded within [the Academy of Invention](The_Academy_of_Invention.md);
- prosthetics, implant, and rehabilitation engineering facilities connected to [the Great Workshops](../locations/The_Great_Workshops.md);
- a protected recovery and rehabilitation house inside [the Cauldron](../locations/The_Cauldron.md);
- field medics and emergency liaisons who work alongside [the Brass Watch](The_Brass_Watch.md);
- and expeditionary medical staff who may accompany accredited explorers into remote or anomalous regions.

The Order supports biology with technology.

Its practitioners treat illness and injury, design braces and replacement limbs, develop implants, restore function, teach adaptation, study unusual biological-mechanical interfaces, and coordinate with certified mechanists when a medical device becomes part of a person's daily body.

The Order must never treat a patient as secondary to the mechanism keeping that patient alive.

## Public Role

The Order's public responsibilities may include:

- emergency and surgical care;
- severe industrial-injury response;
- treatment of burns, pressure injuries, aether exposure, chemical exposure, and crush trauma;
- prosthetic design and fitting;
- implant monitoring and repair;
- long-term rehabilitation;
- physical and occupational retraining;
- field-medic education;
- expedition medical certification;
- disaster-response coordination;
- medical ethics and consent review for experimental procedures;
- and research into the boundary between living tissue and mechanical systems.

Most citizens encounter the Order through an emergency ward, specialist clinic, rehabilitation program, workplace medical station, or field responder rather than its central administration.

## Distributed Presence

### The Hall of Vital Mechanics

[The Hall of Vital Mechanics](../locations/The_Hall_of_Vital_Mechanics.md) is the Order's central hospital, training center, records office, and emergency-coordination headquarters in the Government District.

Its exact internal departments remain unresolved.

### Academy Clinical and Research Annex

The Order maintains a presence within or beside the Academy of Invention for:

- anatomy and physiology education;
- mechanobiology research;
- implant testing;
- clinical review of experimental devices;
- medical instruction for inventors;
- and ethical oversight where invention directly affects living bodies.

The final formal name of this annex remains unresolved.

### Great Workshops Prosthetics and Implant Annex

Order surgeons, prosthetists, therapists, and mechanobiologists work with certified engineers in the Great Workshops to create and maintain:

- replacement limbs;
- braces and mobility supports;
- sensory aids;
- pressure-regulation implants;
- adaptive tools;
- and custom interfaces between tissue and machinery.

The Order governs the patient's medical care and consent.

The Mechanists' Guild governs mechanical certification and engineering responsibility.

Neither institution owns the patient or the device once it becomes part of the patient's embodied life.

### The Cauldron Recovery House

[The Cauldron Recovery House](../locations/The_Cauldron_Recovery_House.md) provides rehabilitation, long-term recovery, industrial-injury care, adaptive-device support, and community medicine inside the Cauldron.

Its presence is politically sensitive.

The facility cannot function as a disguised Brass Watch post, Council registry, or mechanism for identifying undocumented residents. Its safety depends on negotiated neutrality, local staff, and trust earned within the district.

### Brass Watch Medical Liaison

The Order trains or seconds field medics to support:

- fires;
- collapses;
- canal disasters;
- industrial explosions;
- hazardous machinery incidents;
- aetheric exposure;
- temporal disorientation;
- and mass-casualty evacuation.

Some medics may be Watch officers with medical certification. Others remain Order staff operating beside the Watch while retaining independent responsibility to patients.

### Expeditionary Medical Service

Accredited expeditions may include an Order field physician, surgeon, medic, prosthetics specialist, or expedition-certified practitioner.

The Order may also provide:

- portable surgical kits;
- stabilization frames;
- aether-burn treatments;
- pressure and altitude medicine;
- biological sample protocols;
- airship infirmary standards;
- evacuation plans;
- and post-expedition rehabilitation.

The exact size and authority of this service remain unresolved.

## Fields of Practice

The Order's working disciplines may include:

- general medicine;
- surgery;
- emergency medicine;
- field medicine;
- prosthetics;
- orthotics and mobility support;
- rehabilitation;
- pain management;
- mechanobiology;
- implant medicine;
- aetheric trauma;
- environmental and expedition medicine;
- industrial medicine;
- and psychological recovery after catastrophic injury or anomalous events.

Final period-appropriate professional titles remain to be selected.

Terms such as physician, surgeon, medic, therapist, prosthetist, mechanobiologist, chirurgeon, and vital mechanist may coexist or later be reconciled.

## Relationship with the Mechanists' Guild

The Order and [the Mechanists' Guild](The_Mechanists_Guild.md) share responsibility wherever machinery becomes medically necessary.

The relationship is cooperative but not simple.

Potential areas of agreement include:

- device safety;
- material standards;
- pressure tolerance;
- maintenance documentation;
- implant certification;
- and training for prosthetics engineers.

Potential conflicts include:

- whether a device should be treated primarily as machinery or part of a person's body;
- who may inspect an implant;
- whether a Guild certification can override a patient's refusal;
- ownership of experimental designs;
- responsibility when an implant behaves unpredictably;
- and whether Ancient components can be certified under modern standards.

Medical consent takes priority over professional curiosity.

## Relationship with the Academy of Invention

The Order supports Academy research involving biology, healing, adaptive technology, and medical devices.

The Academy provides theoretical knowledge, laboratories, and experimental designs.

The Order provides clinical reality, patient care, ethics, and the reminder that a successful mechanism can still harm the person using it.

The institutions may disagree sharply over experimental procedures, access to rare cases, publication, and whether knowledge should be pursued before a safe clinical use exists.

## Relationship with the Brass Watch

The Order supports the Brass Watch during disasters and dangerous investigations.

Its medics do not become evidence officers merely because they enter a secured scene. Their primary duty remains care.

This creates useful tension when:

- clothing, implants, or biological material may also be evidence;
- a patient refuses to answer questions;
- a temporal incident creates conflicting medical records;
- or the Watch wants access to a device integrated into a person's body.

The Order can cooperate with Watch authority without surrendering patient autonomy.

## Relationship with the Society of Explorers

The Order may certify expedition medical readiness, train field medics, review evacuation plans, and maintain records of unusual injuries encountered beyond Aetherhaven.

Whether an Order medic accompanied the original Clockwork Jungle expedition remains unresolved.

The Society may sometimes view medical restrictions as barriers to discovery.

The Order may view explorers as people who describe preventable risk as unavoidable adventure.

## Relationship with the Cauldron

The Order's official presence in the Cauldron exists because industrial injury, chemical exposure, poverty, disability, and lack of civic documentation do not remove a person's need for care.

The Recovery House may depend on:

- local healers;
- neighborhood compacts;
- former Order staff;
- donated or salvaged equipment;
- and negotiated supply routes.

The central Order may not fully control the facility in practice.

That tension should remain available for later stories.

## Relationship with Elias and Amelia Hawthorne

[Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) has engineering knowledge, field experience, and personal responsibility connected to Amelia's survival.

He should not be portrayed as having single-handedly performed every medical, surgical, rehabilitative, and prosthetic task required after the Clockwork Jungle disaster.

His emergency actions may have been essential. Trained medical care was also necessary.

The Order may have contributed through:

- an expedition medic;
- emergency evacuation;
- surgical stabilization;
- infection control;
- pain management;
- rehabilitation;
- prosthetic fitting;
- implant monitoring;
- and collaboration while Elias built the mechanical framework of Amelia's arm.

The exact practitioners, sequence, and institutional role remain unresolved.

[Amelia Hawthorne](../characters/Amelia_Hawthorne.md) is a patient and person with authority over her own body. She is not a unique specimen owned by the Order.

Any Order interest in the Aether Heart or Aether Gauntlet must be governed by Amelia's consent, safety, and age-appropriate participation in decisions.

## Medical Ethics

The Order's strongest canonical principles should include:

- treat the person before the mechanism;
- obtain meaningful consent whenever circumstances permit;
- do not make necessary care conditional on research participation;
- do not allow the Council, Academy, Guild, Watch, or Society to claim a patient as institutional property;
- distinguish emergency stabilization from permanent authority over future treatment;
- preserve medical confidentiality while recognizing legitimate public-safety risks;
- and ensure adaptive technology serves the patient's life rather than forcing the patient to serve the technology.

The final official oath, code, and enforcement process remain unresolved.

## Political and Institutional Tensions

The Order may face pressure from:

- the High Council during public-health or civic emergencies;
- the Mechanists' Guild over device certification;
- the Academy over research access;
- the Brass Watch over evidence and custody;
- the Society of Explorers over expedition restrictions;
- merchants over expensive treatment and patents;
- and the Cauldron over surveillance, unequal access, and civic neglect.

The Order should not be portrayed as uniformly benevolent or corrupt.

It is a large institution containing skilled caregivers, cautious administrators, ambitious researchers, exhausted field medics, ethical conflicts, political compromise, and people capable of both extraordinary compassion and institutional failure.

## Visual Language

The Order's visual language should combine medicine and precise engineering without resembling the Mechanists' Guild.

Possible elements include:

- clean enamel, brass, glass, linen, and dark wood;
- articulated braces and anatomical diagrams;
- medical instruments arranged beside precision tools;
- white, cream, blue-gray, or muted green fabrics;
- a symbol combining a pulse line, open hand, leaf, or articulated joint;
- field cases designed to survive airship travel;
- and prosthetics displayed as personal adaptive work rather than trophies.

The final crest, uniforms, color system, and seal remain unresolved.

## Continuity Constraints

- The Order exists as a distributed medical network rather than a separate map district.
- Its central institution is in the Government District.
- It maintains a clinical and research presence at the Academy.
- It maintains prosthetics and implant collaboration in the Great Workshops.
- It supports a rehabilitation and community-care facility in the Cauldron.
- It provides or trains field medics connected with the Brass Watch.
- It may support expeditions with medical staff, equipment, and evacuation planning.
- It combines biological medicine with technology, implants, prosthetics, and rehabilitation.
- It collaborates with the Mechanists' Guild without surrendering medical authority or patient autonomy.
- Elias's actions were important to Amelia's survival, but he did not necessarily provide all required medical care alone.
- Amelia must never be treated as an Order asset, specimen, device platform, or compulsory research subject.
- The exact final name, leadership, branch names, ranks, and Clockwork Jungle personnel remain unresolved.

## Open Canon Questions

1. Is **The Order of the Mended Hand** the final name?
2. What is the central building's official name?
3. Who leads the Order?
4. Is it governed by the Council, independently chartered, or professionally self-governing?
5. What are its staff ranks and period-appropriate titles?
6. Which services are public, charitable, fee-based, guild-funded, or Council-funded?
7. How does it handle patients without civic records?
8. What is the exact relationship between the central Order and the Cauldron Recovery House?
9. Does the Recovery House trust the central administration?
10. What medical authority do Order field medics possess during Watch operations?
11. Does the Society of Explorers require an Order-certified medic on dangerous expeditions?
12. Was an Order medic present during the Clockwork Jungle expedition?
13. Who stabilized Amelia first?
14. Who performed the surgery that allowed the Aether Gauntlet to be integrated safely?
15. When did the Order first encounter the Aether Heart?
16. Did anyone attempt to claim research authority over Amelia?
17. What ethical failure or historical scandal shaped the Order's current consent rules?
18. Which Order practitioner eventually becomes a recurring character?
19. What is the Order's seal, oath, and visual identity?
20. How does the Order respond when an implant appears conscious or refuses repair?

## Development Checklist

- [x] Distributed institutional role established.
- [x] Government District headquarters established.
- [x] Academy, Workshops, Cauldron, Watch, Guild, and Society connections established.
- [x] Medical support for Amelia's survival established as necessary but unresolved.
- [x] Patient-autonomy constraints established.
- [ ] Approve the final organization name.
- [ ] Define governance and leadership.
- [ ] Define staff ranks and medical terminology.
- [ ] Select a recurring physician, medic, therapist, or prosthetist when a story requires one.
- [ ] Create the Order seal and field-medical visual language.
- [ ] Resolve the exact Clockwork Jungle medical-response sequence only when the arc requires it.
"""


def central_hall_profile() -> str:
    return f"""
---
location_id: AH-LOC-PLACEHOLDER-049
name: The Hall of Vital Mechanics
type: Unlisted civic hospital, medical institute, and emergency-coordination center
aliases:
  - Vital Hall
  - The Central Order, provisional
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Owner-directed canonical placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
jurisdiction:
  - The Order of the Mended Hand
  - Civic medical regulation and emergency coordination, exact authority unresolved
access_status:
  - Public clinical areas
  - Restricted surgical, research, records, and implant laboratories
map_reference_category: unlisted
map_number:
parent_location: The Government District
primary_connections:
  - The Order of the Mended Hand
  - The High Council of Aetherhaven
  - The Brass Watch
  - The Academy of Invention
  - The Mechanists' Guild
points_of_interest: []
temporal_relevance: Moderate
source_basis:
  - Owner canon decision recorded August 2, 2026
---

# The Hall of Vital Mechanics

> **Canonical working placeholder.** This unnumbered institution exists within the Government District. Its exact architecture, departments, leadership, and final public name remain unresolved.

## Map Reference

No separate numbered map location is required.

The Hall is a significant point of interest within [the Government District](The_Government_District.md).

## Public Map Reference

A major civic hospital and teaching institution where physicians, surgeons, medics, therapists, and prosthetics specialists work beside carefully regulated mechanical technology.

## Canonical Summary

The Hall of Vital Mechanics is the central headquarters, principal hospital, training center, medical-records authority, and emergency-coordination site of [the Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md).

It serves ordinary citizens as well as severe industrial, aetheric, mechanical, expeditionary, and anomalous injuries requiring specialized care.

The Hall is not the only place medicine is practiced in Aetherhaven. It is the city's primary referral and coordination center for cases that cross the boundaries between biology, machinery, public safety, and civic responsibility.

## Civic and Narrative Role

The Hall may contain:

- emergency wards;
- surgical theatres;
- recovery rooms;
- rehabilitation halls;
- prosthetics fitting rooms;
- implant monitoring laboratories;
- anatomy and mechanobiology classrooms;
- medical archives;
- field-medic training spaces;
- disaster-coordination rooms;
- and restricted facilities for unusual aetheric or temporal injuries.

Exact departments remain unresolved.

## Relationship with the Government District

The Hall's placement in the Government District gives it access to civic funding, emergency communication, legal authority, and coordination with the High Council and Brass Watch.

It also exposes the Order to political pressure.

The Hall must not become a facility where the government can quietly seize unusual patients or integrated devices without due process and consent.

## Relationship with Amelia Hawthorne

Amelia may have received surgery, rehabilitation, fitting, monitoring, or later consultation through the Hall after the Clockwork Jungle disaster.

The exact sequence remains unresolved.

No later story may treat her previous care as granting the Hall ownership over the Aether Gauntlet, Aether Heart, her records, or her future decisions.

## Visual Continuity

The Hall should feel like an active medical institution shaped by both care and precision.

Potential visual elements include:

- tall windows and clean daylight;
- brass-framed glass partitions;
- washable enamel and stone;
- articulated rehabilitation devices;
- quiet mechanical lifts;
- pneumatic medical-message tubes;
- surgical instruments beside precision engineering tools;
- patient spaces designed for dignity rather than spectacle;
- and visible wear from constant civic use.

Avoid making the Hall a cold laboratory, gothic asylum, or fantastical machine factory.

## Continuity Constraints

- The Hall is an unnumbered point of interest within the Government District.
- It is the central institution of the Order of the Mended Hand.
- It supports ordinary medicine as well as advanced mechanomedical care.
- Public, clinical, administrative, training, and restricted research functions coexist.
- The Hall may have participated in Amelia's post-accident treatment, but exact details remain unresolved.
- Medical care does not confer institutional ownership over a patient or implant.

## Open Canon Questions

1. Is **The Hall of Vital Mechanics** the final name?
2. Where precisely does it stand within the Government District?
3. What are its major departments and wards?
4. Who directs the Hall?
5. What public symbolism appears on its facade?
6. How are emergency patients transported from docks, mines, workshops, and canals?
7. What restricted records concerning Ancient implants are stored here?
8. Which part of Amelia's care occurred here?
9. Has the Hall ever been pressured to surrender a patient to the Council or Watch?
10. Which recurring medical character works here?

## Development Checklist

- [x] Institutional purpose established.
- [x] Government District placement established.
- [x] Relationship to the Order established.
- [ ] Approve final name and architecture.
- [ ] Define departments and leadership.
- [ ] Create representative art or an architectural artifact.
- [ ] Link recurring medical staff when created.
"""


def recovery_house_profile() -> str:
    return f"""
---
location_id: AH-LOC-PLACEHOLDER-050
name: The Cauldron Recovery House
type: Unlisted rehabilitation, adaptive-care, and community medical facility
aliases:
  - The Recovery House
  - Cauldron Rehabilitation House
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Owner-directed canonical placeholder
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
jurisdiction:
  - Local Cauldron compact and Order affiliation, exact balance unresolved
access_status:
  - Community medical access
  - Neutral-care protections expected but not formally defined
map_reference_category: unlisted
map_number:
parent_location: The Cauldron
primary_connections:
  - The Order of the Mended Hand
  - The Cauldron
  - Neighborhood Compacts
  - The Mechanists' Guild, limited technical support
  - The Brass Watch, restricted emergency coordination
points_of_interest: []
temporal_relevance: Moderate
source_basis:
  - Owner canon decision recorded August 2, 2026
---

# The Cauldron Recovery House

> **Canonical working placeholder.** A rehabilitation and community-care facility exists within the Cauldron. Its final name, exact founders, governance, staff, and relationship with the central Order remain unresolved.

## Map Reference

No separate numbered or restricted-letter map location is required.

The Recovery House is a significant interior location within [the Cauldron](The_Cauldron.md).

## Public Map Reference

A hard-won place of recovery inside the Cauldron, serving workers, families, disabled residents, burn survivors, and people whose injuries or lack of records make ordinary civic care difficult to obtain.

## Canonical Summary

The Cauldron Recovery House provides rehabilitation, adaptive-device care, industrial-injury treatment, long-term recovery, prosthetics maintenance, and community medicine within the Cauldron.

It is affiliated with [the Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md), but it cannot function as a simple branch of Government District authority.

Its survival depends on local trust.

The facility may be staffed by a mixture of:

- Order physicians and therapists;
- Cauldron healers;
- former workshop medics;
- prosthetists;
- volunteer caregivers;
- neighborhood compact members;
- and practitioners whose credentials are unrecognized by the upper city but whose skill is real.

## Neutrality and Trust

The Recovery House must not serve as:

- a Brass Watch observation post;
- a Council registry for undocumented residents;
- a debt-collection office;
- a mechanism for confiscating unlicensed prosthetics;
- or a research pipeline extracting unusual cases from vulnerable people.

Emergency coordination with the Watch may occur at the Ash Line or during major disasters, but patient information and local access remain sensitive.

The House's neutral status may be customary rather than legally guaranteed.

## Services

Possible services include:

- rehabilitation after industrial accidents;
- burn and chemical-exposure recovery;
- mobility training;
- prosthetics adjustment and maintenance;
- pain management;
- adaptive-work retraining;
- community nursing;
- trauma recovery;
- support for conscious automata or hybrid beings whose medical status is disputed;
- and temporary shelter during recovery.

Exact services and technology remain open.

## Relationship with the Order of the Mended Hand

The central Order may provide:

- supplies;
- specialist rotations;
- difficult surgeries;
- training;
- prosthetics components;
- and emergency transport.

The Recovery House may distrust:

- official records;
- upper-city research interests;
- licensing requirements;
- Council oversight;
- and any demand that treatment reveal a patient's identity or legal status.

Their relationship should contain both genuine cooperation and recurring tension.

## Visual Continuity

The Recovery House should look repaired, practical, crowded, and cared for rather than polished.

Possible visual elements include:

- salvaged braces and mobility devices adapted for individual patients;
- clean linens maintained despite soot and limited resources;
- workshop-made ramps and lifts;
- locally painted signs;
- locked medicine cabinets;
- shared kitchens and recovery courtyards;
- worn wood, patched tile, brass rails, and repurposed machinery;
- and visible evidence that the community protects the building.

Avoid portraying it as filthy, hopeless, or secretly sinister merely because it is in the Cauldron.

## Continuity Constraints

- A rehabilitation and community-care facility exists in the Cauldron.
- It is affiliated with the Order but depends on local trust and partial autonomy.
- It serves people neglected or excluded by ordinary civic systems.
- It is not a disguised Watch or Council outpost.
- It may use salvaged, unofficial, or uncertified technology without being inherently negligent.
- Exact leadership, legal status, and final name remain unresolved.

## Open Canon Questions

1. Is **The Cauldron Recovery House** the final name?
2. Who founded it?
3. Is it controlled by the Order, locally governed, or jointly chartered?
4. What neutral-care custom protects patients?
5. Which neighborhood compact protects it?
6. How are supplies moved across the Ash Line?
7. Which services require transfer to the central Hall?
8. Does the Mechanists' Guild recognize devices maintained here?
9. Which recurring healer, therapist, or prosthetist works here?
10. What past breach of trust shaped its current rules?

## Development Checklist

- [x] Cauldron rehabilitation role established.
- [x] Order affiliation and local autonomy established.
- [x] Neutral-care constraints established.
- [ ] Approve final name and governance.
- [ ] Define staff and neighborhood relationships.
- [ ] Create representative art when the location enters a story.
"""


def update_government_district() -> None:
    path = "locations/The_Government_District.md"
    text = read(path)
    text = replace_empty_yaml_list(
        text,
        "primary_connections",
        ["The Hall of Vital Mechanics", "The Order of the Mended Hand"],
    )
    text = replace_empty_yaml_list(text, "points_of_interest", ["The Hall of Vital Mechanics"])

    sentence = " The district also contains [the Hall of Vital Mechanics](The_Hall_of_Vital_Mechanics.md), Aetherhaven's central civic hospital and headquarters for advanced medical and rehabilitative care."
    for heading in ("## Public Map Reference", "## Canonical Summary"):
        pattern = re.compile(rf"({re.escape(heading)}\n\n.*?)(?=\n\n##)", re.DOTALL)
        match = pattern.search(text)
        if match and "Hall of Vital Mechanics" not in match.group(1):
            text = text[: match.end(1)] + sentence + text[match.end(1) :]

    save(path, text)


def update_great_workshops() -> None:
    path = "locations/The_Great_Workshops.md"
    text = read(path)
    text = replace_empty_yaml_list(
        text,
        "primary_connections",
        ["The Order of the Mended Hand", "The Mechanists' Guild"],
    )
    text = replace_empty_yaml_list(
        text,
        "points_of_interest",
        ["Order prosthetics and implant annex, final name unresolved"],
    )

    block = """
The Great Workshops include an Order-supported prosthetics and implant annex where surgeons, prosthetists, therapists, and certified mechanists collaborate on adaptive devices, replacement limbs, braces, and medically integrated machinery.

The exact location, name, governance, and relationship to Elias's private workspace remain unresolved.
"""
    text = insert_section_before(
        text,
        "Medical, Prosthetics, and Implant Work",
        block,
        "Visual Continuity",
    )
    save(path, text)


def update_academy() -> None:
    path = "organizations/The_Academy_of_Invention.md"
    text = read(path)
    text = replace_empty_yaml_list(
        text,
        "primary_connections",
        ["The Order of the Mended Hand", "Doctor Elara Quill"],
    )
    text = replace_empty_yaml_list(text, "headquarters", ["The Academy of Invention Campus"])
    text = replace_empty_yaml_list(text, "known_leadership", ["Doctor Elara Quill"])

    content = """
The Academy hosts or works beside an Order clinical and research annex supporting anatomy, physiology, mechanobiology, implants, adaptive devices, and ethical review of inventions that directly affect living bodies.

The Academy provides laboratories and theoretical research. [The Order of the Mended Hand](The_Order_of_the_Mended_Hand.md) provides clinical care, patient consent standards, rehabilitation knowledge, and medical responsibility.

The final boundaries between Academy research and Order authority remain unresolved.
"""
    text = insert_section_before(text, "Medical and Mechanobiology Collaboration", content, "Continuity Constraints")
    save(path, text)


def update_brass_watch() -> None:
    path = "organizations/The_Brass_Watch.md"
    text = read(path)
    text = add_yaml_item(text, "key_relationships", "The Order of the Mended Hand")

    content = """
The Brass Watch coordinates with [the Order of the Mended Hand](The_Order_of_the_Mended_Hand.md) during fires, collapses, explosions, industrial disasters, aetheric exposure, temporal disorientation, and mass-casualty incidents.

Medical support may come from Order field medics, Watch officers with medical certification, or mixed emergency teams.

Field medics remain responsible first to patient care. Watch authority does not automatically convert medical treatment into evidence collection, nor does it permit officers to inspect or seize an implant integrated into a person's body without lawful and ethical justification.

The exact structure of the Watch medical liaison remains unresolved.
"""
    text = insert_section_before(text, "Medical Response and Field Medics", content, "Continuity Constraints")
    save(path, text)


def update_mechanists_guild() -> None:
    path = "organizations/The_Mechanists_Guild.md"
    text = read(path)
    text = add_yaml_item(text, "key_relationships", "The Order of the Mended Hand")

    content = """
The Guild works with [the Order of the Mended Hand](The_Order_of_the_Mended_Hand.md) wherever a certified machine becomes part of medical treatment, rehabilitation, mobility, sensory support, or a person's embodied life.

The Guild governs engineering standards and professional mechanical responsibility. The Order governs medical care, consent, and biological safety.

Neither institution may claim ownership of a patient or assert that certification grants authority over a device after it becomes integrated with that person's body.

Ancient components such as Amelia's Aether Heart create an unresolved conflict because they cannot be certified under known standards and cannot be separated from the patient merely to satisfy professional review.
"""
    text = insert_section_before(text, "Medical Devices, Prosthetics, and Implants", content, "Continuity Constraints")
    save(path, text)


def update_society() -> None:
    path = "organizations/The_Society_of_Explorers.md"
    text = read(path)
    text = replace_empty_yaml_list(
        text,
        "primary_connections",
        ["The Order of the Mended Hand", "Professor Elias Hawthorne"],
    )

    content = """
Dangerous expeditions may require Order-certified medical planning, field kits, evacuation procedures, or a medical practitioner capable of treating trauma far from Aetherhaven.

Whether [the Order of the Mended Hand](The_Order_of_the_Mended_Hand.md) supplied or certified a medic for the Clockwork Jungle expedition remains unresolved.

The Society and Order may disagree over when medical caution becomes an unreasonable barrier to exploration and when an explorer's confidence becomes preventable risk.
"""
    text = insert_section_before(text, "Expedition Medical Support", content, "Continuity Constraints")
    save(path, text)


def update_cauldron() -> None:
    path = "locations/The_Cauldron.md"
    text = read(path)
    text = add_yaml_item(text, "primary_connections", "The Order of the Mended Hand")
    text = add_yaml_item(text, "primary_connections", "The Cauldron Recovery House")

    content = """
[The Cauldron Recovery House](The_Cauldron_Recovery_House.md) provides rehabilitation, adaptive-device care, industrial-injury treatment, and community medicine inside the district.

The facility is affiliated with [the Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md) but depends on local trust and partial autonomy. It cannot operate as a disguised Watch post, Council registry, or route for identifying undocumented residents.

Its staff may include Order practitioners, Cauldron healers, workshop medics, prosthetists, therapists, and caregivers whose skill is recognized locally even when the upper city does not recognize their credentials.
"""
    text = insert_section_before(text, "The Cauldron Recovery House", content, "Relationship with the High Council")
    save(path, text)


def update_elias() -> None:
    path = "characters/Professor_Elias_Hawthorne.md"
    text = read(path)
    text = add_yaml_item(text, "key_connections", "The Order of the Mended Hand")

    content = """
Elias has a complicated relationship with [the Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md).

His field engineering and emergency actions may have been essential to keeping Amelia alive after the Clockwork Jungle disaster. They did not replace the need for trained medical, surgical, rehabilitative, and prosthetic care.

The Order may have provided an expedition medic, recovery team, surgery, infection control, rehabilitation, implant monitoring, or collaboration while Elias built the mechanical framework of the Aether Gauntlet. The exact sequence and practitioners remain unresolved.

Elias respects medical expertise but may resist institutional caution when it delays a repair or investigation he considers necessary. He becomes especially protective when researchers discuss Amelia's arm as a rare interface rather than part of his daughter's body.

The Order should be capable of challenging Elias when guilt convinces him that he alone must make every decision about Amelia's care.
"""
    text = insert_section_before(text, "Relationship with the Order of the Mended Hand", content, "The Clockwork Jungle Expedition")

    old = "Elias later constructed the mechanical structure that became Amelia's [Aether Gauntlet](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)."
    new = "After emergency stabilization and later medical care whose exact participants remain unresolved, Elias constructed the mechanical structure that became Amelia's [Aether Gauntlet](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)."
    text = text.replace(old, new)
    save(path, text)


def update_amelia() -> None:
    path = "characters/Amelia_Hawthorne.md"
    text = read(path)
    text = add_yaml_item(text, "key_connections", "The Order of the Mended Hand")

    content = """
[The Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md) may have participated in Amelia's emergency treatment, surgery, rehabilitation, prosthetic fitting, implant monitoring, and long-term care after the Clockwork Jungle disaster.

The exact clinicians and sequence remain unresolved.

Amelia may feel gratitude toward individual caregivers while remaining wary of institutional researchers interested in the Aether Heart. Previous medical care does not grant the Order ownership of her records, gauntlet, body, or future choices.

This relationship can support stories about:

- rehabilitation and adaptation;
- ordinary maintenance and physical limits;
- informed consent;
- medical privacy;
- disagreement between Elias and clinicians;
- and Amelia learning to speak for herself in decisions adults once made during an emergency.

The Order must include compassionate practitioners and institutional tensions rather than functioning only as a threat or exposition source.
"""
    text = insert_section_before(text, "Relationship with the Order of the Mended Hand", content, "The Clockwork Jungle Expedition")

    old = "Elias later constructed the mechanical framework that became Amelia's [Aether Gauntlet](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)."
    new = "After emergency stabilization and later medical care whose exact participants remain unresolved, Elias constructed the mechanical framework that became Amelia's [Aether Gauntlet](../artifacts/009_The_Aether_Gauntlet_Exterior_Study.md)."
    text = text.replace(old, new)
    save(path, text)


def update_expedition() -> None:
    path = "historical_events/The_Clockwork_Jungle_Expedition.md"
    text = read(path)
    text = add_yaml_item(text, "organizations", "The Order of the Mended Hand, possible medical support")

    known = "- possible recovery personnel or rescuers not yet identified"
    addition = "- an Order field medic, expedition-certified practitioner, or later recovery team whose exact role remains unresolved"
    if addition not in text and known in text:
        text = text.replace(known, known + "\n" + addition, 1)

    timeline_old = "7. Elias and Amelia are recovered or escape; the exact method remains unresolved.\n8. Elias constructs the mechanical framework of Amelia's new arm."
    timeline_new = "7. Elias performs or assists with emergency stabilization, but the exact medical personnel and methods remain unresolved.\n8. Elias and Amelia are recovered or escape; the exact method remains unresolved.\n9. Trained medical, surgical, rehabilitative, and prosthetic care supports Amelia's survival and recovery.\n10. Elias constructs the mechanical framework of Amelia's new arm."
    if timeline_old in text:
        text = text.replace(timeline_old, timeline_new, 1)
        text = text.replace("9. The Aether Heart", "11. The Aether Heart", 1)
        text = text.replace("10. Elias spends", "12. Elias spends", 1)
        text = text.replace("11. The main series", "13. The main series", 1)
        text = text.replace("12. Clues discovered", "14. Clues discovered", 1)
        text = text.replace("13. A later story", "15. A later story", 1)

    institution_section = """
The [Order of the Mended Hand](../organizations/The_Order_of_the_Mended_Hand.md) may have supported the expedition, the recovery, Amelia's surgery, rehabilitation, prosthetic integration, or later monitoring.

The exact role remains unresolved.

The historical record must not imply that Elias single-handedly provided every form of medical care required to keep Amelia alive. His emergency engineering and stabilization may have been essential, while trained medical practitioners provided other critical care.

Whether an Order medic accompanied the expedition or became involved only after evacuation remains an open question.
"""
    text = insert_section_before(text, "Order of the Mended Hand", institution_section, "Conflicting Accounts")

    constraint = "- Elias's emergency actions were important, but Amelia's survival and recovery also required medical expertise whose personnel and sequence remain unresolved."
    if constraint not in text:
        marker = "- Elias sincerely blames himself, but final responsibility remains unresolved."
        text = text.replace(marker, marker + "\n" + constraint, 1)

    question = "21. What exact medical personnel, field support, surgery, and rehabilitation kept Amelia alive?"
    if question not in text:
        marker = "20. What will the site reveal when Amelia returns?"
        text = text.replace(marker, marker + "\n" + question, 1)

    save(path, text)


def update_indexes() -> None:
    # Placeholder index
    path = "docs/development/PLACEHOLDER_PROFILE_INDEX.md"
    text = read(path)
    note = "\nSome entries are owner-directed canonical placeholders created from explicit canon decisions rather than compiled-source extraction.\n"
    marker = "A placeholder does not resolve contradictions, assign unknown identities, or supersede a completed canonical profile.\n"
    if note.strip() not in text:
        text = text.replace(marker, marker + note, 1)

    org_row = "| [The Order of the Mended Hand](organizations/The_Order_of_the_Mended_Hand.md) | [The_Order_of_the_Mended_Hand.md](organizations/The_Order_of_the_Mended_Hand.md) |"
    if org_row not in text:
        marker = "| [The Guild of Verdant Mechanists](organizations/The_Guild_of_Verdant_Mechanists.md) | [The_Guild_of_Verdant_Mechanists.md](organizations/The_Guild_of_Verdant_Mechanists.md) |"
        text = text.replace(marker, marker + "\n" + org_row, 1)

    loc_rows = (
        "| [The Hall of Vital Mechanics](locations/The_Hall_of_Vital_Mechanics.md) | [The_Hall_of_Vital_Mechanics.md](locations/The_Hall_of_Vital_Mechanics.md) |\n"
        "| [The Cauldron Recovery House](locations/The_Cauldron_Recovery_House.md) | [The_Cauldron_Recovery_House.md](locations/The_Cauldron_Recovery_House.md) |"
    )
    if loc_rows.splitlines()[0] not in text:
        marker = "| [Rootglass Cloister](locations/Rootglass_Cloister.md) | [Rootglass_Cloister.md](locations/Rootglass_Cloister.md) |"
        text = text.replace(marker, marker + "\n" + loc_rows, 1)
    save(path, text)

    # Project index snapshot and placeholder summary
    path = "docs/PROJECT_INDEX.md"
    text = read(path)
    text = text.replace(
        "- **12** completed canonical organization profiles and **23** source-grounded organization placeholders",
        "- **12** completed canonical organization profiles and **24** organization placeholders",
    )
    text = text.replace(
        "- **5** completed canonical location profiles and **48** source-grounded location placeholders",
        "- **5** completed canonical location profiles and **50** location placeholders",
    )

    section = """
## Distributed Medical Infrastructure

Aetherhaven's medical, surgical, rehabilitative, prosthetic, implant, and field-response infrastructure is represented by [the Order of the Mended Hand](organizations/The_Order_of_the_Mended_Hand.md).

The Order is not a separate map district. Its known presence includes:

- [the Hall of Vital Mechanics](locations/The_Hall_of_Vital_Mechanics.md) in the Government District;
- clinical and research collaboration at the Academy of Invention;
- prosthetics and implant work in the Great Workshops;
- [the Cauldron Recovery House](locations/The_Cauldron_Recovery_House.md);
- field medics supporting Brass Watch emergencies;
- and possible expeditionary medical support.

The institution is intentionally a placeholder. Its final name, leadership, staffing, and exact role in Amelia Hawthorne's survival remain unresolved.
"""
    if "## Distributed Medical Infrastructure" not in text:
        marker = "## Artifact Image Slate\n"
        text = text.replace(marker, section.strip() + "\n\n" + marker, 1)
    save(path, text)


def main() -> int:
    write("organizations/The_Order_of_the_Mended_Hand.md", organization_profile())
    write("locations/The_Hall_of_Vital_Mechanics.md", central_hall_profile())
    write("locations/The_Cauldron_Recovery_House.md", recovery_house_profile())

    update_government_district()
    update_great_workshops()
    update_academy()
    update_brass_watch()
    update_mechanists_guild()
    update_society()
    update_cauldron()
    update_elias()
    update_amelia()
    update_expedition()
    update_indexes()

    print("Created and integrated the Order of the Mended Hand placeholder network.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
