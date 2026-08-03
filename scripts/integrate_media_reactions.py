#!/usr/bin/env python3
"""Integrate non-canonical public reaction records without altering source content.

The media_reactions directory is evidence of audience interpretation, not canon.
This migration adds editorial metadata around each source transcript, records an
immutable checksum for the source block, builds an audience-response synthesis,
and connects the folder to the wider project.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media_reactions"
PROJECT_INDEX = ROOT / "PROJECT_INDEX.md"
STANDARD = ROOT / "CANON_MARKDOWN_STANDARD.md"
STORY_DRAFT_INDEX = ROOT / "story_drafts" / "README.md"

SOURCE_START = "<!-- SOURCE CONTENT START: IMMUTABLE PUBLIC REACTION -->"
SOURCE_END = "<!-- SOURCE CONTENT END: IMMUTABLE PUBLIC REACTION -->"
TODAY = "2026-08-03"

REACTIONS = {
    "An_Introduction_to_Aetherhaven.md": {
        "id": "AH-REACTION-001",
        "title": "An Introduction to Aetherhaven",
        "media_type": "Audio podcast dialogue transcript",
        "source_file": "An_Introduction_to_Aetherhaven.m4a",
        "overall_sentiment": "Highly enthusiastic, intellectually curious, and mystery-driven",
        "alignment": "Mixed: strong thematic understanding with several literalized or outdated lore claims",
        "summary": (
            "The reaction understands Aetherhaven as a living, shifting city whose institutions are built around "
            "technology they do not fully control. Amelia is recognized as central to the mystery, but the response "
            "frequently converts unresolved titles, metaphors, and speculative possibilities into settled mechanics."
        ),
        "lands": [
            "The Heart Engine and the Lost Seconds are immediately memorable hooks.",
            "The living-machine ecology of the Clockwork Gardens is understood as a core theme rather than decoration.",
            "The political conflict between knowledge, secrecy, dependence, and reform is legible.",
            "Amelia is perceived as the emotional and mechanical center of the larger mystery.",
        ],
        "aligned": [
            "Aetherhaven feels alive and capable of reacting to its inhabitants.",
            "The city depends on ancient systems no modern institution completely understands.",
            "The Closed Eye, Ninth Guild, Unwound, and Severed Coil are read as competing philosophies rather than interchangeable villains.",
        ],
        "flags": [
            "The transcript repeatedly uses Hawthorn and Thorn instead of Hawthorne and Thorne.",
            "It calls Amelia the Clockwork Prodigy rather than her canonical primary title, the Clockwork Explorer.",
            "It treats Amelia's exact age as nine even though opening chronology remains unresolved.",
            "It treats kindness as the literal technical fuel of the Aether Heart; current canon preserves that wording as bedtime-story framing.",
            "It presents the Six Keys, Prototype II linkage, and Amelia's arm as a literal key component with more certainty than active canon supports.",
            "It risks reducing Amelia from a person making choices to a component required by the city.",
        ],
        "development": [
            "Keep the Heart Engine, Lost Seconds, and living-city premise prominent in public-facing summaries.",
            "Strengthen person-first language whenever Amelia is described as a Bearer or Living Key.",
            "Label metaphor, rumor, and unresolved theory more clearly in material shared with test readers.",
        ],
        "connections": [
            "../locations/Aetherhaven.md",
            "../locations/The_Aetherium.md",
            "../characters/Amelia_Hawthorne.md",
            "../organizations/The_High_Council_of_Aetherhaven.md",
            "../organizations/The_Order_of_the_Closed_Eye.md",
        ],
    },
    "How_Kindness_Powers_Aetherhaven’s_Heart_Engine.md": {
        "id": "AH-REACTION-002",
        "title": "How Kindness Powers Aetherhaven's Heart Engine",
        "media_type": "Audio podcast dialogue transcript",
        "source_file": "How_Kindness_Powers_Aetherhaven’s_Heart_Engine.m4a",
        "overall_sentiment": "Warm, delighted, accessible, and strongly attached to Amelia's everyday life",
        "alignment": "Emotionally strong; technically over-literal",
        "summary": (
            "This is the clearest evidence that the light opening stories are creating affection. Pip, the Wayfinder as home, "
            "Amelia's competence, and kindness as heroic action all land immediately. The main interpretive problem is that "
            "the bedtime-story metaphor is treated as literal citywide engineering law."
        ),
        "lands": [
            "Pip dropping a wrench on Amelia's pillow is highly memorable and charming.",
            "The Wayfinder is understood as home, family member, and adventure partner rather than transportation.",
            "Amelia is read as a capable young mechanic, not merely someone with a magical arm.",
            "Kindness and attention to small suffering are understood as the moral center of the bedtime adventure.",
        ],
        "aligned": [
            "The intended emotional lesson of the Moon Garden story is understood correctly.",
            "The quiet domestic relationship among Amelia, Elias, Pip, and the Wayfinder is resonating.",
            "The reaction sees caring for others as a form of courage rather than a secondary trait.",
        ],
        "flags": [
            "It states that the Aether Heart is literally powered by kindness rather than recognizing the fairy-tale framing.",
            "It expands one compassionate act into a citywide energy pulse and concludes that all machinery requires empathy to grow.",
            "It treats Amelia's age as definitively nine.",
            "It uses Hawthorn instead of Hawthorne.",
        ],
        "development": [
            "The opening strategy is working: warmth makes Amelia and her household immediately likable.",
            "Retain the kindness theme, but add a subtle cue that the narrator's explanation is poetic or storybook language.",
            "Use this reaction as evidence that Book One should establish the family before introducing institutional trauma.",
        ],
        "connections": [
            "../story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md",
            "../story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md",
            "../characters/Amelia_Hawthorne.md",
            "../characters/Pip.md",
            "../story_arcs/The_Keeper_of_Dreams.md",
        ],
    },
    "Aetherhaven_and_the_Heart_Engine.md": {
        "id": "AH-REACTION-003",
        "title": "Traveler's Guide to Aetherhaven",
        "media_type": "Audio podcast dialogue transcript",
        "source_file": "Aetherhaven_and_the_Heart_Engine.m4a",
        "overall_sentiment": "Fascinated, unsettled, and eager to explore the city's systems",
        "alignment": "Strong thematic reading; mixed factual precision",
        "summary": (
            "The reaction treats Aetherhaven itself as the main attraction: a city whose geography, time, infrastructure, "
            "and government cannot be separated. It is especially engaged by working-class knowledge, institutional hypocrisy, "
            "Dock Zero, the Cauldron, and Amelia's ability to listen. It also invents confident technical explanations for mysteries intentionally left open."
        ),
        "lands": [
            "Temporal displacement at the Aerial Docks is an excellent entry hook.",
            "Living charts and working-class expertise are perceived as more trustworthy than official abstractions.",
            "Dock Zero and the future-dated ticket produce sympathy as well as mystery.",
            "The Cauldron reads as structural hypocrisy, not merely a dangerous neighborhood.",
            "Amelia is understood as someone who listens to the city rather than conquers it.",
        ],
        "aligned": [
            "Modern institutions are trying to govern systems older than their authority.",
            "The Council, unions, Watch, Cauldron, Unwound, and Coil are connected by dependence rather than simple good-versus-evil roles.",
            "The city's mutable geography and missing time feel purposeful rather than random spectacle.",
        ],
        "flags": [
            "It supplies unconfirmed physics for condensed aether and describes the Aetherium as a miniature black hole.",
            "It claims the Wayfinder surfs temporal waves through a specific ancient conduit mechanism not established as settled canon.",
            "It describes Mara Voss as entirely ignoring Council mandates, which is more absolute than her canonical practical independence.",
            "It treats Prototype I as a full-scale Heart Engine iteration loose in the undercity; active canon does not establish that description.",
            "It makes several interpretations of Thorne, the Council, and Amelia's Living Key status sound like confirmed facts.",
            "It uses Hawthorn, Thorn, Ether, and Morning Star where current canon uses Hawthorne, Thorne, Aether, and Morningstar.",
        ],
        "development": [
            "The city has enough identity to function as a character and a reason to keep reading.",
            "Public-facing files need clearer separation among observed evidence, institutional belief, and audience theory.",
            "Preserve the working-class and infrastructure perspective; it makes the world feel inhabited rather than merely ornate.",
        ],
        "connections": [
            "../locations/Aetherhaven.md",
            "../locations/The_Aerial_Docks.md",
            "../locations/The_Cauldron.md",
            "../characters/Amelia_Hawthorne.md",
            "../organizations/The_Aerial_Mariners_Union.md",
        ],
    },
    "Who_Rules_Aetherhaven_s_Heart_Engine.md": {
        "id": "AH-REACTION-004",
        "title": "Who Rules Aetherhaven's Heart Engine?",
        "media_type": "Audio debate transcript",
        "source_file": "Who_Rules_Aetherhaven_s_Heart_Engine.m4a",
        "overall_sentiment": "Deeply engaged and genuinely divided rather than seeking a simple villain",
        "alignment": "Thematically strong with several institutional claims stated too confidently",
        "summary": (
            "The debate understands the central political question correctly: protection and oppression may be produced by the same machinery. "
            "Neither speaker can dismiss the need for Continuance or the cost of secrecy. That moral tension is one of the strongest audience responses in the folder."
        ),
        "lands": [
            "The Doctrine of Continuance works as both a credible survival principle and a possible instrument of control.",
            "The distinction between the peaceful Unwound and violent Severed Coil is understood and defended.",
            "The Cauldron is interpreted as the hidden cost of upper-city stability.",
            "The Council is not reduced to a cartoon villain; its necessity remains arguable.",
        ],
        "aligned": [
            "Aetherhaven's government is morally compromised without being functionally unnecessary.",
            "Information control can be protective in motive and oppressive in effect.",
            "The central conflict invites readers to decide rather than supplying a single approved political answer.",
        ],
        "flags": [
            "It describes the Closed Eye as a conventional deep-state intelligence agency, which flattens its stranger containment doctrine.",
            "It presents retroactive clock editing and specific committees as settled mechanisms rather than interpretations requiring source verification.",
            "It interprets the Thirteenth Chair as either proof of limits or authoritarian theater; both are useful readings, not established truth.",
            "It describes the Cauldron as an unregulated toxic sweatshop in language more absolute than active canon.",
            "It uses Thorn instead of Thorne.",
        ],
        "development": [
            "The Council's ambiguity is landing exactly as intended and should not be simplified.",
            "Future stories should show individual Council decisions and consequences rather than resolving the institution as wholly protective or wholly corrupt.",
            "The Unwound/Severed Coil distinction is clear enough to support nuanced political storytelling.",
        ],
        "connections": [
            "../organizations/The_High_Council_of_Aetherhaven.md",
            "../organizations/The_Unwound.md",
            "../organizations/The_Severed_Coil.md",
            "../locations/The_Cauldron.md",
            "../organizations/The_Order_of_the_Closed_Eye.md",
        ],
    },
    "Policing_the_Lost_Seconds_of_Aetherhaven.md": {
        "id": "AH-REACTION-005",
        "title": "Policing the Lost Seconds of Aetherhaven",
        "media_type": "Audio podcast dialogue transcript",
        "source_file": "Policing_the_Lost_Seconds_of_Aetherhaven.m4a",
        "overall_sentiment": "Highly engaged with procedure, moral injury, institutional limits, and local expertise",
        "alignment": "Strong institutional themes; significant invented or conflicting event detail",
        "summary": (
            "The reaction sees the Brass Watch as honorable people operating inside a deliberately incomplete information system. "
            "Thorne's conflict, the value of physical evidence, and the need for Hawthorne expertise all resonate. The Gearbreaker retelling, however, "
            "adds actions and motivations that should not be imported back into canon."
        ),
        "lands": [
            "The Watch's containment-first mentality feels practical, understandable, and insufficient.",
            "Thorne is perceived as a strong character caught between truth, safety, and political command.",
            "The distinction between honorable officers and a compromised information system is clear.",
            "The Gearbreaker Standoff communicates the importance of local expertise and disciplined refusal.",
            "A Watch/Hawthorne partnership feels narratively productive because each side supplies what the other lacks.",
        ],
        "aligned": [
            "The Watch should be capable of bravery and institutional harm at the same time.",
            "Gearbreaker is understood as a lesson against blind obedience and dismissal of workers' knowledge.",
            "Thorne's value comes from recognizing that procedure can preserve safety without revealing truth.",
        ],
        "flags": [
            "It introduces detailed divisions, protocols, witness technology, and Sentinel behavior that may be audience extrapolation rather than settled canon.",
            "The Gearbreaker account invents a shove, raised weapons, specific command actions, and a later career for the young constable.",
            "It frames Vale as knowingly compelling miners into danger and Thorne as resolving consequences in ways that exceed active canon; Vale did not intend violence and Thorne did not order it.",
            "The exact Gearbreaker choreography must remain the canonical disciplined, defensive standoff with no blood or blows.",
            "It uses Oren, Hawthorne inconsistently, Thorn, Ether Gauntlet, and Ether Heart instead of Orin, Thorne, Aether Gauntlet, and Aether Heart.",
            "The final temporal-bomb theory is an effective hook but remains audience speculation.",
        ],
        "development": [
            "The emotional meaning of Gearbreaker is landing, but the exact event needs a protected public-facing summary to prevent drift.",
            "Keep Thorne morally serious and capable of opposing misuse without turning her into a simple rebel against the Council.",
            "Procedural details are appealing; future canon can selectively formalize them without accepting the entire reaction account.",
        ],
        "connections": [
            "../organizations/The_Brass_Watch.md",
            "../characters/Chief_Inspector_Beatrice_Thorne.md",
            "../historical_events/The_Gearbreaker_Standoff.md",
            "../characters/Orin_Flint.md",
            "../story_arcs/The_Watchmans_Regret.md",
        ],
    },
    "Who_Really_Drives_Your_Mechanical_Hand.md": {
        "id": "AH-REACTION-006",
        "title": "Who Really Drives Your Mechanical Hand?",
        "media_type": "Audio podcast dialogue transcript",
        "source_file": "Who_Really_Drives_Your_Mechanical_Hand.m4a",
        "overall_sentiment": "Powerfully affected, disturbed, and philosophically engaged",
        "alignment": "Excellent thematic resonance; major overstatement of unresolved medical history",
        "summary": (
            "This reaction strongly understands the intended bodily-autonomy theme. The Hand is perceived as necessary, skilled, feared, "
            "and capable of treating a successful mechanism as more important than the person. Mechanical limbs also read as interfaces with memory and power. "
            "However, the transcript converts many deliberately unresolved possibilities about Amelia's treatment and the Recovery House into confirmed abuse."
        ),
        "lands": [
            "The Hand's public shorthand is understood without confusion with the Closed Eye.",
            "The necessary-evil medical model produces exactly the intended discomfort.",
            "Replacement versus preservation is perceived as an ethical philosophy, not merely a visual detail.",
            "Bodily autonomy, consent, institutional ownership, and mechanical memory generate strong adult-level thematic engagement.",
            "Amelia's personhood is understood as threatened by institutions that may value the Aether Heart more than her choices.",
        ],
        "aligned": [
            "Medical ability does not automatically confer moral authority.",
            "Individual practitioners may save lives while the wider institution remains dangerous.",
            "A prosthetic can be part of embodied identity while still raising questions about memory, control, and outside access.",
        ],
        "flags": [
            "It treats aggressive amputation as the Hand's universal default rather than one possible bias among branches and practitioners.",
            "It portrays the Cauldron Recovery House as a trusted safer alternative, conflicting with current canon that it may exploit vulnerable patients and conceal deaths or disappearances.",
            "It states that the Closed Eye uses wards as holding cells and that Academy researchers experiment on anesthetized patients as confirmed institutional practice; active canon leaves exact abuses unresolved.",
            "It invents a settled Amelia recovery sequence in which the Hand demanded higher amputation, surrender of the Aether Heart, confinement, and Elias smuggled her out. Those decisions remain open canon questions.",
            "It repeatedly shifts from the possibility that Amelia could be treated as property to stating that she was civic property; canon requires person-first framing.",
            "It uses Ether rather than Aether in several names.",
        ],
        "development": [
            "The Hand concept is resonating strongly and can sustain serious story material.",
            "Revise shared summaries of the Recovery House so its weak oversight, disappearances, and possible exploitation are unmistakable.",
            "Keep Amelia's medical history unresolved until the story earns those revelations; do not let reaction material become accidental canon.",
            "Balance institutional horror with compassionate Hand practitioners so the organization remains dangerous rather than uniformly evil.",
        ],
        "connections": [
            "../organizations/The_Order_of_the_Mended_Hand.md",
            "../locations/The_Cauldron_Recovery_House.md",
            "../characters/Amelia_Hawthorne.md",
            "../characters/Professor_Elias_Hawthorne.md",
            "../historical_events/The_Clockwork_Jungle_Expedition.md",
            "../characters/Master_Gideon_Brasswell.md",
        ],
    },
}


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(name: str, values: list[str]) -> list[str]:
    lines = [f"{name}:"]
    lines.extend(f"  - {q(value)}" for value in values)
    return lines


def source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def extract_source(text: str) -> tuple[str, str | None]:
    if SOURCE_START not in text:
        return text, None

    start_token = SOURCE_START + "\n"
    if start_token not in text or SOURCE_END not in text:
        raise RuntimeError("Malformed immutable source markers")

    prefix, remainder = text.split(start_token, 1)
    source, _ = remainder.split(SOURCE_END, 1)
    match = re.search(r'^source_sha256:\s*["\']?([0-9a-f]{64})', prefix, re.MULTILINE)
    previous_hash = match.group(1) if match else None
    return source, previous_hash


def link_list(paths: list[str]) -> str:
    items = []
    for path in paths:
        label = Path(path).stem.replace("_", " ")
        items.append(f"- [{label}]({path})")
    return "\n".join(items)


def bullet_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def render_record(filename: str, data: dict[str, object], source: str) -> str:
    digest = source_hash(source)
    front = [
        "---",
        f"reaction_id: {data['id']}",
        f"title: {q(str(data['title']))}",
        "record_type: Non-canonical public reaction",
        "canon_status: Non-canonical audience evidence",
        f"media_type: {q(str(data['media_type']))}",
        f"source_file: {q(str(data['source_file']))}",
        "source_content_policy: Immutable",
        f"source_sha256: {digest}",
        "audience_scope: Limited test audience",
        f"overall_sentiment: {q(str(data['overall_sentiment']))}",
        f"canon_alignment: {q(str(data['alignment']))}",
        f"last_metadata_review: {TODAY}",
    ]
    front.extend(yaml_list("primary_connections", list(data["connections"])))
    front.append("---")

    editorial = dedent(
        f"""
        # Public Reaction Record: {data['title']}

        > **Non-canonical audience evidence.** The editorial metadata and interpretation audit may be updated as canon develops. The source transcript below is preserved exactly and must not be edited, corrected, normalized, or silently incorporated into canon.

        ## Editorial Reaction Summary

        {data['summary']}

        **Overall sentiment:** {data['overall_sentiment']}  
        **Canon alignment:** {data['alignment']}

        ## What Appears to Be Landing

        {bullet_list(list(data['lands']))}

        ## Interpretation Audit

        ### Aligned with Current Canonical Intent

        {bullet_list(list(data['aligned']))}

        ### Misinterpretations, Overreach, or Continuity Risks

        {bullet_list(list(data['flags']))}

        ## Development Use

        {bullet_list(list(data['development']))}

        ## Primary Canon Connections

        {link_list(list(data['connections']))}

        ## Immutable Source Transcript

        **Source integrity:** SHA-256 `{digest}`  
        **Editing rule:** Do not alter anything between the source markers. Corrections belong in the editorial metadata above.
        """
    ).strip()

    return "\n".join(front) + "\n\n" + editorial + "\n\n" + SOURCE_START + "\n" + source + SOURCE_END + "\n"


def integrate_reaction_files() -> None:
    for filename, data in REACTIONS.items():
        path = MEDIA / filename
        if not path.exists():
            raise RuntimeError(f"Missing media reaction source: {filename}")

        original = path.read_text(encoding="utf-8")
        source, previous_hash = extract_source(original)
        digest = source_hash(source)
        if previous_hash and previous_hash != digest:
            raise RuntimeError(
                f"Immutable source content changed in {filename}: expected {previous_hash}, found {digest}"
            )

        rendered = render_record(filename, data, source)
        if rendered != original:
            path.write_text(rendered, encoding="utf-8")


def render_media_readme() -> str:
    rows = []
    for filename, data in REACTIONS.items():
        rows.append(
            f"| [{data['title']}]({filename}) | {data['media_type']} | {data['overall_sentiment']} | {data['alignment']} |"
        )

    return dedent(
        f"""
        # Public Reactions to The Brass Guardian

        > **Non-Canonical Public Reactions:** This folder contains reactions from a limited test audience. These records are evidence of how the work is being understood, felt, remembered, and reinterpreted. They are not sources of canon and cannot resolve an open canon question.

        ## Purpose

        The folder exists to help determine:

        - whether characters and settings are creating emotional attachment;
        - which mysteries generate curiosity;
        - whether moral and institutional ambiguity is being understood;
        - where terminology or chronology is confusing;
        - where metaphor is being mistaken for literal mechanics;
        - and where audience interpretation is drifting away from established canon.

        ## Source-Integrity Rule

        Each reaction file contains two distinct layers:

        1. **Editorial metadata and analysis**, which may be corrected and updated.
        2. **Immutable source content**, enclosed by explicit source markers and protected by a SHA-256 checksum.

        Do not edit, spell-correct, normalize, or rewrite the source transcript, blog, article, or review. Name errors and inaccurate interpretations are themselves useful audience evidence. Record corrections only in the editorial metadata.

        ## Current Reaction Records

        | Reaction | Media type | Audience response | Canon alignment |
        |---|---|---|---|
        {chr(10).join(rows)}

        ## Current Cross-Reaction Synthesis

        See [Audience Response Synthesis](AUDIENCE_RESPONSE_SYNTHESIS.md) for the aggregate interpretation audit and development recommendations.

        ## Canon Separation

        Material in this directory may inspire a question, reveal a communication problem, or identify a successful theme. It must never be copied into a canonical profile merely because a listener stated it confidently.

        When a reaction conflicts with canon:

        - preserve the reaction exactly;
        - document the conflict in metadata;
        - link to the authoritative active Markdown;
        - and decide separately whether the reaction reveals a problem in the story, the shared source package, or the audience's inference.
        """
    ).strip() + "\n"


def render_synthesis() -> str:
    return dedent(
        """
        ---
        analysis_id: AH-AUDIENCE-SYNTHESIS-001
        title: Limited Test Audience Response Synthesis
        record_type: Non-canonical audience analysis
        canon_status: Non-canonical development evidence
        source_records: 6
        last_updated: 2026-08-03
        ---

        # Limited Test Audience Response Synthesis

        > This document analyzes the reaction records in `media_reactions/`. It is not canon. It should be revised as new reactions arrive, but it must never replace the immutable source transcripts.

        ## Executive Assessment

        The material is resonating strongly. The audience is not merely noticing the steampunk appearance; it is identifying the deeper design of the project: a living city, inherited systems no one fully controls, institutions that can protect and exploit at the same time, and a child protagonist whose attention and empathy matter as much as technical power.

        The reactions also show a consistent failure mode: unresolved possibilities are being converted into factual exposition. Listeners repeatedly explain the physics, assign motives, complete Amelia's medical history, and settle institutional conspiracies that active canon intentionally leaves open. The enthusiasm is valuable, but it demonstrates that the current shared materials do not always distinguish **observed fact**, **institutional claim**, **legend**, **metaphor**, and **development possibility** clearly enough.

        The sample is small—six reaction records—and should not be treated as market research. It is nevertheless coherent enough to identify several strong signals.

        ## What Is Resonating Most Strongly

        ### Aetherhaven Feels Alive

        Every reaction treats the city as more than scenery. Shifting streets, lost seconds, living charts, self-directed machines, and responsive gardens are being interpreted as parts of one living system. This is one of the clearest successes in the project.

        ### The Central Mysteries Are Memorable

        The Heart Engine, the Lost Seconds, the Thirteenth Chair, Dock Zero, the Morningstar ticket, and the question of what the city is waiting for repeatedly become closing hooks. The audience is generating its own questions rather than merely repeating summaries.

        ### Amelia Is Compelling in Two Different Modes

        The lighter reaction responds to Amelia as a child, mechanic, daughter, friend to Pip, and member of the Wayfinder household. The darker reactions respond to her as the person whose agency is threatened by institutions and ancient systems. Both are useful, but the first mode needs to come earlier so the second mode has emotional weight.

        ### Institutional Ambiguity Is Working

        The High Council, Brass Watch, Closed Eye, Hand, Unwound, Severed Coil, and Cauldron are not being read as a simple hero-and-villain chart. The strongest reactions debate necessity against oppression and competence against moral authority. That is the intended response.

        ### Working-Class Knowledge Is Visible

        The Aerial Mariners, Lamplighters, miners, Cauldron residents, and practical field workers are consistently recognized as people who understand reality better than distant officials. This makes Aetherhaven feel socially inhabited and supports the theme that expertise is distributed.

        ### Bodily Autonomy Has Significant Power

        The Hand reaction shows that the medical and prosthetic material can support serious emotional and philosophical engagement. The question is not merely whether a mechanical arm works; it is who gets to decide what a repaired body is for.

        ## Where Audience Understanding Is Drifting

        ### Metaphor Is Becoming Mechanics

        The bedtime statement that the Aether Heart is powered by kindness is being treated as a literal energy specification. The emotional message is landing, but the framing is not sufficiently clear.

        ### Amelia Is Too Easily Reduced to a Key

        Several reactions describe Amelia as a component, civic property, required interface, or potential puppet. Some of that is a legitimate threat within the story, but the reactions sometimes adopt the institutions' dehumanizing frame as objective truth. Future public-facing language should emphasize that machines react to Amelia; they do not define or own her.

        ### The Recovery House Is Being Misread as Safe

        One reaction treats the Cauldron Recovery House as the trustworthy, autonomy-preserving alternative to the Hall. Current canon is more dangerous: weak oversight creates room for community protection **and** exploitation, missing patients, unexplained deaths, and off-book experiments. The shared material should communicate that risk more clearly.

        ### Amelia's Recovery Is Being Written by the Audience

        The reaction material invents a complete sequence in which the Hand demands amputation and surrender of the Aether Heart, Elias rejects them, and then smuggles Amelia away. The actual sequence, practitioners, procedures, and choices remain unresolved. This is the most important accidental-canon risk in the folder.

        ### Gearbreaker's Meaning Is Correct, but Its Events Are Drifting

        The audience understands disciplined resistance, local expertise, and the danger of lawful orders issued without context. The policing reaction nevertheless invents a shove, weapon movements, command decisions, and later career outcomes. The exact historical choreography needs stronger protection in any public summary.

        ### Naming and Terminology Are Not Stable in Memory

        Hawthorn/Hawthorne, Thorn/Thorne, Oren/Orin, Ether/Aether, Morning Star/Morningstar, Clockwork Prodigy/Clockwork Explorer, and Aether Gauntlet/Ether Gauntlet all vary. This is a clear case for a concise public naming glossary.

        ### The Two Heart Engines Create Confusion

        The Wayfinder draft and several reactions use Heart Engine language close to the Aetherium's Heart Engine. The reactions reinforce the existing development concern that the Wayfinder's central mechanism should receive a distinct final term.

        ## Are These the Reactions We Want?

        Largely, yes.

        We want readers to feel wonder, unease, affection, curiosity, and moral uncertainty. We want them to ask whether systems can be alive, whether protection can become control, whether inherited technology can ever truly be owned, and whether kindness and attention are forms of technical intelligence. All of those responses are present.

        The main imbalance is tonal. Five of the six reactions gravitate quickly toward conspiracy, authoritarian systems, temporal horror, bodily control, and civic collapse. Only the kindness-focused reaction spends substantial time with Amelia, Elias, Pip, and the Wayfinder as a family. That supports the current Book One strategy: begin with the warm, wondrous present-day characters before asking the reader to carry the heavier history.

        The reactions also suggest a crossover tone. The world can engage children through adventure and living machines while giving older readers institutional, ethical, and political material to discuss. That breadth is a strength as long as the opening remains emotionally accessible.

        ## Recommended Development Actions

        1. Preserve the planned light opening sequence: bedtime teaser followed by ordinary life aboard the Wayfinder.
        2. Complete the Volume One opening baseline, especially Amelia's age, what she knows, and what the public knows.
        3. Rename or distinguish the Wayfinder's internal Heart Engine from the Aetherium's Heart Engine.
        4. Add a public-facing terminology sheet covering canonical spellings, titles, and approved shorthand.
        5. Present claims in shared lore as **known**, **reported**, **believed**, **restricted**, or **unresolved**.
        6. Strengthen person-first wording around Amelia's Bearer and Living Key material.
        7. Clarify that the Cauldron Recovery House can protect patients and exploit them; neither the House nor the Hall is automatically safe.
        8. Protect the exact Gearbreaker Standoff summary from embellishment.
        9. Keep the High Council and Brass Watch morally contested rather than resolving them into villains or heroes.
        10. Continue gathering reactions, but tag the audience segment and the specific source package they received so later responses can be compared meaningfully.

        ## Useful Measures for Future Reactions

        Future metadata should record, when known:

        - audience age range;
        - prior familiarity with the project;
        - exact files or stories shared;
        - whether the response was spontaneous or prompted;
        - favorite character, place, image, and mystery;
        - points of confusion;
        - desire to continue reading;
        - and which statements the audience believed were confirmed canon.
        """
    ).strip() + "\n"


def insert_before_heading(text: str, heading: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = f"## {heading}\n"
    if marker not in text:
        raise RuntimeError(f"Missing heading in integration target: {heading}")
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def update_project_index() -> None:
    text = PROJECT_INDEX.read_text(encoding="utf-8")

    snapshot = "- **6** non-canonical public reaction records in `media_reactions/`"
    if snapshot not in text:
        marker = "- **2** canonical prose story drafts in `story_drafts/`"
        if marker not in text:
            raise RuntimeError("Project snapshot story-draft marker not found")
        text = text.replace(marker, marker + "\n" + snapshot, 1)

    authority_note = (
        "6. `media_reactions/` contains non-canonical evidence of audience interpretation. "
        "It may identify communication problems but cannot establish or resolve canon."
    )
    if authority_note not in text:
        marker = "5. The `unused/` directory is outside the project canon and must never be used as a story, art, continuity, or reference source unless the project owner explicitly restores a specific item to active canon."
        if marker not in text:
            raise RuntimeError("Project canon authority marker not found")
        text = text.replace(marker, marker + "\n" + authority_note, 1)

    root_row = "| [media_reactions/README.md](media_reactions/README.md) | Non-canonical limited-audience reactions, immutable source records, and interpretation audits |"
    if root_row not in text:
        marker = "| [story_drafts/README.md](story_drafts/README.md) | Index, canon rules, and Book One placement strategy for active prose story drafts |"
        if marker not in text:
            raise RuntimeError("Project root-file story draft row not found")
        text = text.replace(marker, marker + "\n" + root_row, 1)

    section = dedent(
        """
        ## Non-Canonical Public Reactions

        Limited-audience reactions are preserved in [`media_reactions/`](media_reactions/README.md). They are development evidence, not canon.

        The source transcripts are immutable. Editorial metadata may identify enthusiasm, confusion, factual drift, or useful audience theories without correcting the source text.

        See the current [Audience Response Synthesis](media_reactions/AUDIENCE_RESPONSE_SYNTHESIS.md).
        """
    ).strip()
    text = insert_before_heading(text, "Canonical Story Drafts", section)
    PROJECT_INDEX.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_standard() -> None:
    text = STANDARD.read_text(encoding="utf-8")

    source_note = "6. `media_reactions/` is non-canonical audience evidence and cannot override active canon."
    if source_note not in text:
        marker = "5. `unused/` is excluded and must never be consulted unless the project owner explicitly restores a named item."
        if marker not in text:
            raise RuntimeError("Canon standard source priority marker not found")
        text = text.replace(marker, marker + "\n" + source_note, 1)

    section = dedent(
        f"""
        ## Public Reaction Records

        Files in `media_reactions/` are non-canonical development evidence.

        - Preserve source transcripts, articles, blogs, and reviews exactly between `{SOURCE_START}` and `{SOURCE_END}`.
        - Store a SHA-256 checksum for each immutable source block.
        - Editorial metadata, interpretation audits, summaries, tags, and canon links may be updated.
        - Do not silently correct misspelled names, inaccurate claims, or speculative statements inside source content; those errors are useful evidence of audience understanding.
        - Never promote a reaction theory into canon without a separate explicit canon decision.
        - When a reaction conflicts with canon, link to the authoritative active Markdown and describe the conflict outside the source block.
        - Aggregate conclusions must identify the sample size and avoid treating a limited test audience as broad market evidence.
        """
    ).strip()
    text = insert_before_heading(text, "Organization Naming Collision Rule", section)
    STANDARD.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_story_draft_index() -> None:
    text = STORY_DRAFT_INDEX.read_text(encoding="utf-8")
    section = dedent(
        """
        ## Limited Audience Testing

        Selected story and canon materials are being shared with a limited test audience. Reactions are preserved in the non-canonical [`media_reactions/`](../media_reactions/README.md) directory.

        The current [Audience Response Synthesis](../media_reactions/AUDIENCE_RESPONSE_SYNTHESIS.md) supports the decision to introduce Amelia, Elias, Pip, and the Wayfinder through warmth and ordinary life before revealing the heavier Clockwork Jungle and institutional history.

        Audience reactions may guide clarity, pacing, terminology, and emphasis. They do not determine canon.
        """
    ).strip()
    text = insert_before_heading(text, "Placement Decision Still Open", section)
    STORY_DRAFT_INDEX.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    MEDIA.mkdir(parents=True, exist_ok=True)
    integrate_reaction_files()
    (MEDIA / "README.md").write_text(render_media_readme(), encoding="utf-8")
    (MEDIA / "AUDIENCE_RESPONSE_SYNTHESIS.md").write_text(render_synthesis(), encoding="utf-8")
    update_project_index()
    update_standard()
    update_story_draft_index()
    print("Integrated non-canonical public reactions without modifying source content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
