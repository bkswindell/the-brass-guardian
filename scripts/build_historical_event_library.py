#!/usr/bin/env python3
"""Build the historical-event canon layer and the Gearbreaker story records.

This migration adds the `historical_events/` information class, records the
Gearbreaker Standoff as a canonical historical event, creates the future
Watchman's Regret story arc, expands Orin Flint, and creates conservative
placeholders for other already identified historical events.
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


def replace_section(path: str, heading: str, content: str, before: str = "## Continuity Constraints") -> None:
    target = ROOT / path
    if not target.exists():
        return
    text = target.read_text(encoding="utf-8")
    block = f"## {heading}\n\n{content.strip()}\n\n"
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        text = pattern.sub(block.rstrip() + "\n\n", text)
    elif before in text:
        text = text.replace(before, block + before, 1)
    else:
        text = text.rstrip() + "\n\n" + block
    target.write_text(text, encoding="utf-8")


def historical_template() -> str:
    return """
---
historical_event_id: AH-HIST-UNASSIGNED
name:
aliases: []
type:
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Draft historical event
canonical_scope: Aetherhaven volumes
last_updated:
date_status: unresolved
chronology: []
locations: []
participants: []
organizations: []
related_artifacts: []
related_story_arcs: []
public_record_status: incomplete
restricted_record_status: unknown
order_interest: unknown
source_basis: []
---

# Historical Event Name

> **Historical-event record.** This file owns the objective in-world event. Story arcs own how Amelia and the reader discover, interpret, or experience its consequences.

## Canonical Historical Summary

## Public Record

## Restricted Record

## Known Participants

## Timeline

## Institutional Responses

## Conflicting Accounts

## Physical Evidence

## Related Artifacts

## Story Connections

## Continuity Constraints

## Unresolved Historical Questions

## Development Checklist

- [ ] Public and restricted accounts separated.
- [ ] Known participants and institutions linked.
- [ ] Timeline limited to established facts.
- [ ] Conflicting accounts preserved rather than silently reconciled.
- [ ] Physical evidence and artifact records linked.
- [ ] Relevant story arcs linked.
- [ ] Canonical or representative image linked, or exception documented.
- [ ] Backlinks added from directly related profiles.

## Archival Status

### Public Record

### Restricted Record

### Order Interest

### Primary Sources

### Outstanding Historical Questions

- [ ]
"""


def historical_readme() -> str:
    return """
# Aetherhaven Historical Events

> **Development reference and spoiler warning:** Historical-event records describe events that objectively occurred within Aetherhaven's world, even when dates, motives, memories, and official accounts remain disputed.

## Information Ownership

A **historical event** owns what happened, the known timeline, participants, institutional consequences, conflicting accounts, and surviving evidence.

A **story arc** owns how Amelia and the reader uncover or become involved with that history.

Character, organization, location, and artifact profiles should link to the historical event rather than repeat its full chronology.

```text
Historical Event
        ▲
        │ discovered or revisited through
        │
     Story Arc
        ▲
        │ experienced by
        │
Characters · Organizations · Locations · Artifacts
```

## Canonical Working Events

| Event | Status | Primary connections |
|---|---|---|
| [The Gearbreaker Standoff](The_Gearbreaker_Standoff.md) | Canonical historical event | Orin Flint, High Council, Brass Watch, Gearbreaker Mines |
| [The Disappearance of Prototype I](The_Disappearance_of_Prototype_I.md) | Canonical historical event | Prototype I, Order of the Closed Eye, Ninth Guild, Underclock |
| [The Resolute Incident](The_Resolute_Incident.md) | Canonical historical event | Mara Voss, *Resolute*, Aerial Docks |
| [The Revision of the Society of Explorers Charter](The_Revision_of_the_Society_of_Explorers_Charter.md) | Canonical working history | Society of Explorers and both seal variants |

## Historical Placeholders

| Event | Status |
|---|---|
| [The Rising](The_Rising.md) | Historical placeholder |
| [The First Continuance](The_First_Continuance.md) | Historical placeholder |
| [The Closing of Dock Zero](The_Closing_of_Dock_Zero.md) | Historical placeholder |
| [The Founding of the Conservancy](The_Founding_of_the_Conservancy.md) | Historical placeholder |
| [The Ash Compact](The_Ash_Compact.md) | Historical placeholder |
| [The Founding of the Eight Guilds](The_Founding_of_the_Eight_Guilds.md) | Historical placeholder |
| [The Opening of the Aerial Docks](The_Opening_of_the_Aerial_Docks.md) | Historical placeholder |
| [The First Dream Bloom](The_First_Dream_Bloom.md) | Historical placeholder |
| [The Great Garden Rearrangement](The_Great_Garden_Rearrangement.md) | Historical placeholder |
| [The Night of Silent Clocks](The_Night_of_Silent_Clocks.md) | Historical placeholder |
| [The Last Morningstar Manifest](The_Last_Morningstar_Manifest.md) | Historical placeholder |

## Historical-Record Rules

- Do not convert rumor into objective history.
- Preserve contradictory witness accounts.
- Separate public history from restricted evidence.
- Record uncertainty explicitly in `date_status`, `canon_status`, and unresolved questions.
- Do not reveal a story-arc solution merely because the underlying event has its own record.
- Artifacts should record provenance and historical significance through links to these files.
- `unused/` remains outside canon and must never be consulted.
"""


def event_file(event_id: str, name: str, summary: str, *, status: str = "Historical event placeholder", locations: list[str] | None = None, participants: list[str] | None = None, organizations: list[str] | None = None, arcs: list[str] | None = None, constraints: list[str] | None = None, questions: list[str] | None = None, public: str = "The public record is incomplete and may reduce the event to a simplified civic account.", restricted: str = "Restricted records remain incomplete, sealed, contradictory, or not yet assigned.", order_interest: str = "Unknown.") -> str:
    locations = locations or []
    participants = participants or []
    organizations = organizations or []
    arcs = arcs or []
    constraints = constraints or []
    questions = questions or []

    def links(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None yet assigned."

    return f"""
---
historical_event_id: {event_id}
name: {name}
aliases: []
type: Historical event
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: {status}
canonical_scope: Aetherhaven volumes
last_updated: {TODAY}
date_status: unresolved
chronology: []
locations: []
participants: []
organizations: []
related_artifacts: []
related_story_arcs: []
public_record_status: incomplete
restricted_record_status: incomplete
order_interest: unresolved
source_basis:
  - Current canonical Markdown
  - Aetherhaven compiled manuscript where Markdown leaves gaps
---

# {name}

> **Historical-event record.** This file owns the objective event. It does not decide how Amelia learns the history or resolve mysteries not established by current canon.

## Canonical Historical Summary

{summary}

## Public Record

{public}

## Restricted Record

{restricted}

## Known Participants

{links(participants)}

## Timeline

- Exact dates and sequence remain unresolved unless stated in the canonical summary.

## Institutional Responses

{links(organizations)}

## Conflicting Accounts

- Preserve contradictory dates, records, memories, and witness statements until a later canon decision resolves them.

## Physical Evidence

- Link surviving artifacts here as they are identified.

## Related Artifacts

- No dedicated artifact backlink has yet been confirmed unless linked below.

## Story Connections

{links(arcs)}

## Continuity Constraints

{links(constraints)}

## Unresolved Historical Questions

{links(questions)}

## Development Checklist

- [ ] Expand the public account.
- [ ] Separate restricted evidence.
- [ ] Confirm participants and institutions.
- [ ] Establish or preserve date uncertainty.
- [ ] Link related artifacts.
- [ ] Link story arcs and profile backlinks.
- [ ] Add representative historical imagery or document why none should exist.

## Archival Status

### Public Record

{public}

### Restricted Record

{restricted}

### Order Interest

{order_interest}

### Primary Sources

- Current canonical Markdown
- Compiled manuscript only where active Markdown leaves a gap

### Outstanding Historical Questions

{links(questions)}
"""


def gearbreaker_standoff() -> str:
    return """
---
historical_event_id: AH-HIST-001
name: The Gearbreaker Standoff
aliases:
  - Gearbreaker Standoff
  - The Day the Mountain Refused
  - The Mine Gate Standoff
type: Civic and labor confrontation
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Canonical historical event
canonical_scope: Aetherhaven volumes
last_updated: 2026-08-02
date_status: exact date unresolved
chronology:
  - pre-Amelia main storyline
locations:
  - Gearbreaker Mines
participants:
  - Orin Flint
  - Chancellor Octavia Vale
  - Chief Inspector Beatrice Thorne
  - unnamed young Brass Watch constable
  - Gearbreaker mining crews
organizations:
  - High Council of Aetherhaven
  - Brass Watch
  - Miners' Guild
related_artifacts: []
related_story_arcs:
  - The Watchman's Regret
public_record_status: publicly known but rarely discussed
restricted_record_status: official accounts incomplete and politically sensitive
order_interest: no confirmed direct involvement
source_basis:
  - Canon decisions recorded August 2, 2026
  - Current canonical Markdown
---

# The Gearbreaker Standoff

> **Canonical historical event.** This file owns the objective chronology, institutional consequences, conflicting accounts, and surviving evidence. [The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md) owns Amelia's future discovery of the event through a former constable's account.

## Canonical Historical Summary

Years before Amelia's main adventures, [Orin Flint](../characters/Orin_Flint.md) closed the [Gearbreaker Mines](../locations/The_Gearbreaker_Mines.md) after determining that an unstable section of the mountain could not be entered safely.

Ore shipments stopped. Foundries slowed. Merchants, industrial leaders, and Council delegates demanded that production resume. Orin submitted a report containing a single sentence:

> **The mountain is not finished speaking.**

Believing the shutdown could be a labor refusal rather than an imminent structural emergency, [Chancellor Octavia Vale](../characters/Chancellor_Octavia_Vale.md) authorized the [Brass Watch](../organizations/The_Brass_Watch.md) to restore lawful operation. She did not intend violence. [Chief Inspector Beatrice Thorne](../characters/Chief_Inspector_Beatrice_Thorne.md) did not instruct officers to assault or endanger miners.

At the mine entrance, the crews stood silent with tools lowered and lamps extinguished. Orin refused the order to return underground.

A young and inexperienced Watch constable crossed the line that Orin would not permit anyone to cross. The constable shoved, seized, or attempted to physically force one crew member toward the mine entrance. Witnesses disagree about the exact contact. They agree that the miner was touched against his will and placed at risk.

Orin moved for the first time.

He picked up his rock hammer and raised it into a controlled half-ready defensive guard. The miners did not look toward him or wait for another order. Picks, hammers, drilling bars, and crowbars rose throughout the line almost at once.

Then the entire mining line took exactly one step forward.

They did not charge. They did not retreat. They did not threaten to attack. They held their tools at a posture that was defensive but unmistakably capable of becoming offensive if the Watch attempted to force entry or seize another miner.

The Watch had expected reluctant workers. It was woefully unprepared for a disciplined wall of people whose daily labor made them physically formidable and whose loyalty to Orin had been earned over years of safe decisions.

Some younger officers continued escalating verbally and called for arrests. Veteran and more experienced officers understood what the formation meant. Disagreement broke out within the Watch ranks, preventing any unified order to advance.

No one was physically injured.

The same cannot be said for institutional pride.

Neither side could safely de-escalate without outside help. An as-yet-unidentified mediator eventually secured a stand-down. The miners lowered their tools only after receiving credible assurance that no one would be forced underground. The Watch withdrew without arrests.

Several days later, the tunnel that the Council had sought to reopen collapsed. Had Orin obeyed, dozens of miners could have died.

## Public Record

The incident is publicly known but rarely discussed in formal civic settings. Most citizens know only that the Council attempted to reopen the mines, a confrontation followed, and the subsequent collapse proved Orin's safety judgment correct.

The miners' oral account emphasizes the one step forward and the fact that no miner looked toward Orin before following his movement.

Watch veterans remember the internal disagreement that prevented a disastrous advance.

Council summaries tend to describe the event as a failed compliance action resolved without injury.

## Restricted Record

The full Council authorization, Watch deployment instructions, officer statements, mediator communications, and post-incident inquiry are incomplete, missing, sealed, politically embarrassing, or distributed across separate records.

No official account conclusively identifies the mediator.

No official account fully agrees on whether the young constable shoved the miner, seized his clothing, grabbed his shoulder, or attempted to drag him toward the shaft.

## Known Participants

- [Orin Flint](../characters/Orin_Flint.md), Foreman of the Gearbreaker Mines
- [Chancellor Octavia Vale](../characters/Chancellor_Octavia_Vale.md), who authorized lawful compliance but did not intend violence
- [Chief Inspector Beatrice Thorne](../characters/Chief_Inspector_Beatrice_Thorne.md), whose exact location and direct involvement during the decisive moments remain unresolved
- an unnamed young Brass Watch constable whose action triggered Orin's defensive response
- senior and veteran Watch officers who resisted further escalation
- the assembled Gearbreaker crews
- an unresolved outside mediator

## Timeline

1. Orin closes an unsafe mine section and walks the crews off site.
2. Ore shortages create political, merchant, trade, and industrial pressure.
3. The High Council orders work restored.
4. Vale authorizes a Brass Watch compliance action based on incomplete information.
5. Miners assemble silently outside the main shaft.
6. Orin refuses the return-to-work order.
7. A young constable physically attempts to force a miner toward the mine.
8. Orin raises his hammer into a defensive guard.
9. The miners follow without waiting for another instruction.
10. The mining line takes exactly one step forward and locks in place.
11. The Watch divides internally between escalation and restraint.
12. An unresolved mediator secures a stand-down.
13. The mine remains closed.
14. The disputed tunnel collapses several days later.

## Institutional Responses

### High Council

The standoff became a public embarrassment and an enduring lesson in the limits of authority exercised without local knowledge. The Council did not issue a public apology, and Orin did not demand one.

### Brass Watch

The Watch incorporated the event into informal institutional memory. Veteran officers understand that a lawful order can become dangerous when officers misunderstand the environment, the people, or the practical authority of a specialist responsible for lives.

### Gearbreaker Crews

The miners' loyalty to Orin became unquestionable. The standoff did not create that loyalty; it revealed how completely he had already earned it.

### Orin Flint

Orin has no interest in using the incident to humiliate Vale, Thorne, the Watch, or the Council. He considers the matter closed as long as no institution again disrespects his crews or attempts to force them into danger.

## Conflicting Accounts

- The young constable's exact physical action remains disputed.
- Thorne's exact role during the confrontation remains unresolved.
- Vale may have intervened directly, remotely, or only after the immediate crisis.
- The mediator's identity remains deliberately unassigned.
- Some accounts describe the miners' tools as defensive; hostile political accounts call them weapons.
- The precise duration of the locked standoff differs between accounts.

## Physical Evidence

Potential surviving evidence includes:

- Orin's one-line closure report
- the original Council directive
- Brass Watch deployment instructions
- individual officer statements
- mining-shift rosters
- mine safety readings
- survey diagrams of the collapsed tunnel
- newspaper accounts shaped by different political interests
- an eventual recorded testimony from the Watchman in *The Watchman's Regret*

No dedicated artifact records for these documents have yet been created.

## Related Artifacts

- [Gearbreaker Excavation Photograph](../artifacts/033_Gearbreaker_Excavation_Photograph.md), related to the broader mine mystery rather than direct proof of the standoff
- [Orin Flint's Depth Log](../artifacts/035_Orin_Flints_Depth_Log.md), potentially useful context for Orin's safety judgment
- Future artifact concepts: Orin's closure report, Council compliance order, Watch incident report, and post-collapse survey

## Story Connections

### [The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md)

The standoff appears as a flashback narrated by the former young constable who crossed the line. He shares the account when Amelia faces a well-intentioned mistake caused by certainty without sufficient understanding.

### Six-Key and Heart Engine arcs

The later six-socket wall and machinery beneath the mountain may cause Amelia and others to re-examine whether the earlier instability was purely geological. The standoff itself does not prove a Six-Key or Heart Engine connection.

## Continuity Constraints

- Orin remained passive until a Watch member physically endangered or attempted to force a miner.
- Orin initiated the raising of tools.
- The crews followed his lead without waiting for a further order.
- The miners took exactly one step forward.
- The miners did not charge, pursue, or attack.
- Their posture was massively defensive and only half-offensive as an unmistakable warning.
- No one was physically injured.
- The Watch was internally divided, and that division prevented further escalation.
- Vale did not intend violence.
- Thorne did not order officers to assault miners.
- A mediator was required, but the mediator's identity remains unresolved.
- The tunnel later collapsed and vindicated Orin's safety judgment.
- Orin does not exploit the incident for political power or public humiliation.
- The event must not be simplified into miners good, Watch bad. Multiple good people acted on incomplete information, while one inexperienced officer made the decisive mistake.

## Unresolved Historical Questions

1. Who was the mediator?
2. Where were Vale and Thorne during the one-step advance?
3. What exactly did the young constable do to the miner?
4. Who supplied the Council with the incomplete or misleading safety assessment?
5. Did merchant or industrial interests knowingly minimize the danger?
6. Why are portions of the official inquiry missing or separated?
7. Which miner was physically forced, and does that person wish to be identified?
8. Did the mountain shift during the standoff itself?
9. Was the later collapse natural, mechanical, or connected to deeper systems?
10. Why did the miners move with such immediate coordination without looking toward Orin?

## Development Checklist

- [x] Core chronology established.
- [x] Orin's decisive trigger established.
- [x] Miners' one-step defensive formation established.
- [x] No physical injuries established.
- [x] Institutional consequences established.
- [x] Mediator identity preserved as unresolved.
- [x] Watchman's Regret story connection established.
- [ ] Create historical evidence artifact records.
- [ ] Generate a canonical historical illustration or evidence collage.
- [ ] Define the future Watchman's name only when required by the story.
- [ ] Add the final story appearance after *The Watchman's Regret* is drafted.

## Archival Status

### Public Record

Publicly known, politically embarrassing, and commonly simplified.

### Restricted Record

Incomplete and distributed among Council, Watch, mine, and private testimony records.

### Order Interest

No direct Order of the Closed Eye involvement is established. Missing records may be ordinary institutional self-protection unless later evidence proves otherwise.

### Primary Sources

- [Orin Flint](../characters/Orin_Flint.md)
- [Chancellor Octavia Vale](../characters/Chancellor_Octavia_Vale.md)
- [Chief Inspector Beatrice Thorne](../characters/Chief_Inspector_Beatrice_Thorne.md)
- [The Brass Watch](../organizations/The_Brass_Watch.md)
- [The High Council of Aetherhaven](../organizations/The_High_Council_of_Aetherhaven.md)
- [The Gearbreaker Mines](../locations/The_Gearbreaker_Mines.md)
- [The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md)

### Outstanding Historical Questions

- [ ] Identify or deliberately preserve the mediator.
- [ ] Determine the future Watchman's identity.
- [ ] Establish the provenance of Orin's closure report.
- [ ] Decide how much of the inquiry was sealed, lost, altered, or merely dispersed.
"""


def orin_profile() -> str:
    return """
---
character_id: AH-CHAR-005
name: Orin Flint
title: Foreman of the Gearbreaker Mines
aliases:
  - Orin
  - Foreman Flint
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Canonical working profile
canonical_scope: Aetherhaven volumes
last_updated: 2026-08-02
primary_locations:
  - Gearbreaker Mines
affiliations:
  - Gearbreaker mining crews
  - Miners' Guild, formal status unresolved
key_connections:
  - Master Gideon Brasswell
  - Professor Elias Hawthorne
  - Amelia Hawthorne
  - Chancellor Octavia Vale
  - Chief Inspector Beatrice Thorne
  - Gearbreaker Standoff
temporal_relevance: High
source_basis:
  - Current canonical Markdown
  - Aetherhaven compiled manuscripts where Markdown previously left gaps
---

# Orin Flint

## Canonical Summary

[Orin Flint](Orin_Flint.md) is the veteran Foreman of the [Gearbreaker Mines](../locations/The_Gearbreaker_Mines.md) and one of the most respected working leaders in [Aetherhaven](../locations/Aetherhaven.md). Gruff, obstinate, and nearly impossible to move once he has made a safety judgment, Orin places the lives of his crews and the integrity of the mountain above profit, politics, production, or civic urgency.

He knows the mines and tunnels better than any outside authority. He can identify chambers by their echoes, notices changes in the mountain before instruments confirm them, and treats long experience as evidence rather than superstition.

Orin does not negotiate over safety.

If he closes a tunnel, it remains closed. If ordered to endanger a crew, he will walk every miner off the site. His workers will follow because he has spent decades proving that he will never sacrifice one of them to preserve a contract, satisfy a politician, or protect his own position.

He rarely raises his voice. He acts.

> **The hell with your politics. I know these mines and tunnels. I will not put anyone at risk, and I will not offend the mountain.**

Orin's defining public history is [the Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md), when a failed Brass Watch compliance action came dangerously close to civil violence. After a young constable physically attempted to force one of Orin's crew toward a closed mine, Orin raised his hammer. The miners followed without waiting for another instruction, took exactly one step forward, and formed a disciplined defensive wall that neither advanced nor retreated.

No one was physically injured.

The tunnel later collapsed, proving Orin had been right.

## Character Core

Orin represents stewardship through responsibility.

He believes:

- every worker who enters the mountain must be given every reasonable chance to return home;
- authority belongs to the person willing to carry the consequences of a decision;
- a careless worker is not merely risking one life but weakening the chain that protects the whole crew;
- the mountain is not property to be conquered but a reality to be respected;
- hesitation can kill, but so can ambition disguised as courage.

His central principle is simple:

> **Nothing is more valuable than bringing every worker home.**

## Personality

Orin is:

- gruff,
- immovable,
- brutally practical,
- disciplined,
- fiercely loyal,
- quietly generous,
- intolerant of carelessness,
- suspicious of outside control,
- willing to use force when restraint has genuinely failed,
- and exceptionally difficult to frighten or intimidate.

Stubborn is an understatement.

Once Orin concludes that safety requires a course of action, persuasion becomes nearly impossible. He does not argue for the pleasure of winning. He stops discussing the matter because, in his judgment, the point at which discussion was useful has already passed.

He is not a pacifist. He understands violence more clearly than many people who speak casually about using it. That understanding makes him slow to initiate it and decisive when a line has been crossed.

## Leadership Underground

Leadership beneath the mountain is different from leadership in a council chamber.

There are no speeches during a collapse.

No votes during a pressure failure.

No second chances after someone ignores a cracked support.

Orin leads through precise decisions and immediate action. He will not ask a miner to perform work he would refuse himself, and he expects every member of a crew to give full effort.

Mining is backbreaking work and not for the faint of heart. Orin does not romanticize it.

He has little tolerance for careless mistakes because one weak link can compromise the safety of everyone in the tunnel.

When a new apprentice lacks the strength, discipline, or nerve for the work, Orin does not humiliate them. He may pay the apprentice a day's wages from his own pocket and say:

> **Stay home tomorrow. Come back when you're ready. The mountain will still be here.**

If a miner is injured or a shutdown leaves families without wages, Orin has quietly surrendered his own pay to the crew. He makes no speech and expects no gratitude.

The miners always discover what he did.

## The Gearbreaker Crews

Orin's crews are fiercely loyal because he earned their loyalty one safe decision at a time.

They know that:

- he will be the last person to leave a dangerous site;
- he will stop production regardless of financial pressure;
- he will confront any person who physically endangers a miner;
- he will accept the political and professional consequences of protecting them;
- he will also dismiss or remove anyone whose carelessness threatens the crew.

During the Gearbreaker Standoff, the miners did not look toward Orin after he raised his hammer.

They already knew what he stood for.

## Public Reputation

Across Aetherhaven, workers say:

> **If Orin turns a crew around, you turn around.**

Merchants, councillors, and industrial leaders use different language.

One frustrated official summarized the problem:

> **If Gideon won't move, then we might have better luck moving the mountain.**

## Relationship with Master Gideon Brasswell

[Gideon Brasswell](Master_Gideon_Brasswell.md) understands machines. Orin understands mountains.

Their trust is old, practical, and nearly wordless.

If Gideon says the pressure is wrong, Orin begins evacuating before asking for a full explanation.

If Orin says a tunnel is closed, Gideon checks his instruments instead of questioning Orin's authority.

They may disagree about causes, but neither embarrasses the other professionally or treats uncertainty as weakness.

## Relationship with Professor Elias Hawthorne

Orin respects [Elias Hawthorne](Professor_Elias_Hawthorne.md) because Elias listens to miners before explaining what they must have misunderstood.

Their tension comes from curiosity. Elias sometimes presses toward an answer after Orin believes the safe limit has been reached.

Orin will stand in his path if necessary.

> **You'll get your answers after my people get home.**

## Relationship with Amelia Hawthorne

Orin speaks to [Amelia Hawthorne](Amelia_Hawthorne.md) honestly. He does not soften danger for her, dismiss her because of her age, or treat her as a mechanism that belongs in the mines.

The mountain and its oldest machinery appear to respond differently around her. Orin does not pretend to know why.

His protection of Amelia comes from the same principle that governs his crews: no one gets to use a person as an expendable tool.

## Relationship with Chancellor Octavia Vale

[Octavia Vale](Chancellor_Octavia_Vale.md) learned how immovable Orin could be during the [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md).

Vale did not intend the confrontation to approach violence. She authorized lawful compliance using incomplete information and underestimated both Orin's responsibility to his crews and the loyalty he had earned.

Since the standoff, Vale no longer assumes that civic authority alone can resolve a mine-safety dispute. She still challenges Orin, and he still refuses her when necessary, but she asks for his reasoning before choosing a response.

Orin has no intention of using the event to humiliate her, provided the Council never again attempts to force his crew into danger.

## Relationship with Chief Inspector Beatrice Thorne

[Beatrice Thorne](Chief_Inspector_Beatrice_Thorne.md) and Orin are not friends, but they understand one another.

The Gearbreaker Standoff taught Thorne that authority without situational understanding can become dangerous. It taught Orin that disciplined officers may resist a reckless escalation even when doing so creates conflict inside their own ranks.

When Orin now says no one goes underground, Thorne's first useful question is:

> **Show me.**

## Relationship with the High Council

The [High Council](../organizations/The_High_Council_of_Aetherhaven.md) depends on ore, production, and infrastructure supplied through the mines. That dependence repeatedly creates tension with Orin.

He does not recognize political urgency as a substitute for geological reality.

> **The mountain doesn't care who signed the order.**

The Council can remove his title in theory. In practice, experienced crews may walk with him.

## Relationship with Merchants, Trade, and Industry

Mine closures cost merchants money, delay contracts, slow foundries, and disrupt industries across the city.

Orin understands those consequences and does not enjoy causing them.

He simply ranks funerals as more expensive.

> **Better lost coin than lost people.**

## Relationship with the Brass Watch

Orin respects the [Brass Watch](../organizations/The_Brass_Watch.md) when it protects people and works within its competence.

He does not respect a badge used as a substitute for understanding.

The Gearbreaker Standoff remains a scar between the mines and the Watch, but not an active feud. Veteran officers know what happened. Orin knows that experienced Watch members prevented the younger officers from escalating further.

Neither side seeks another test.

## Relationship with the Miners' Guild

Orin's exact formal office within the [Miners' Guild](../organizations/The_Miners_Guild.md) remains unresolved.

He is unquestionably the operational authority at Gearbreaker and an influential voice among miners. Whether he formally leads the full Guild, rejects the administrative position, or allows another person to handle civic representation remains open.

## Relationship with the Underclock

Officially, Orin has no relationship with the [Underclock](../organizations/The_Underclock.md).

He knows that some passages were not cut by miners and that frightened people occasionally pass through places the official city does not acknowledge.

When those routes do not threaten his crews or the mountain, Orin may mark them:

> **Not ours.**

That is not the same as granting the Underclock control of the mines.

## Relationship with the Quiet Choir

Orin has heard rhythmic vibrations travel through abandoned pipes beneath the mines.

He has learned not to answer.

He does not know whether the [Quiet Choir](../organizations/The_Quiet_Choir.md) is a network of people, a machine intelligence, or something between them. He may not even know its accepted name early in the series.

## Relationship with Juniper Bell

Orin and [Juniper Bell](Juniper_Bell.md) do not currently know one another personally.

Their worlds do not ordinarily intersect geographically, professionally, or politically. Orin knows the Keeper of the Clockwork Gardens by name and reputation. Juniper has heard of the foreman who brings his crews home.

A future story may force them to meet. Any eventual respect or friendship must grow from that encounter rather than pre-existing connection.

Their contrasting personalities and parallel roles as reluctant stewards may become meaningful later, but no present relationship should be assumed.

## Relationship with the Mountain

Most citizens say Orin knows the mountain.

Orin says:

> **Mostly, I try not to offend it.**

Whether this is humor, hard-earned metaphor, or literal belief remains unresolved.

## The Six-Socket Wall

Orin's crews discovered a perfectly smooth metallic wall beneath the Gearbreaker Mines. It has no visible seam and contains six empty sockets.

Machinery can be heard beyond it.

Orin halted excavation.

He has no desire to open the wall merely because it exists.

Every attempt to drill or cut the wall has failed or transferred dangerous stress into the surrounding stone. Orin treats that response as the mountain refusing the work.

## Main Story Connections

### Six-Key Arc

The six sockets may be one of the oldest surviving access points associated with the Six Keys. Orin protects the site without knowing its full purpose.

The connection remains strongly suggested rather than mechanically resolved.

### Heart Engine and Living Key Arc

Sounds and movement beyond the wall may change when the Heart Engine's rhythm changes or when Amelia enters deeper mine systems.

Orin is likely to identify the pattern before anyone can explain it.

### Quiet Choir

The mine vibrations may become early evidence that communication is traveling through Aetherhaven's oldest infrastructure. Orin hears the pattern but refuses to answer without understanding the risk.

### The Watchman's Regret

[The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md) reveals the Gearbreaker Standoff through the testimony of the former young constable whose action forced Orin to raise his hammer.

Orin is central to the flashback but not the emotional protagonist of the story.

## Side-Story Opportunities

### The Apprentice

A frightened apprentice disappears before the first shift. Orin quietly searches for the young person rather than allowing the crew to turn the absence into ridicule.

### The Last Shift

A retired miner asks to work one final day underground. Orin refuses for a reason that initially appears cruel and later proves protective.

### Tunnel Twenty-Seven

An abandoned tunnel repeatedly appears on official maps despite no living miner remembering its excavation.

### The Quiet Lunch

Amelia spends a day eating with the crews and learns that courage includes admitting when one is not ready.

### The Stone That Floats

Miners recover a stone that refuses to fall. Gideon insists that it cannot exist. Orin considers the result additional evidence that the mountain is strange.

### The Broken Chain

A young miner causes a dangerous accident through carelessness. Orin makes the miner rebuild every damaged safety chain by hand and earn the crew's trust again.

### The Day the Mountain Refused

Different participants tell Amelia contradictory versions of the Gearbreaker Standoff before the former Watch constable gives his own account.

## Visual Continuity

Orin should appear:

- broad-shouldered and physically formidable;
- older and weathered by decades underground;
- dressed in practical mining clothes with no ceremonial excess;
- marked by dust, old scars, and heavy work;
- carrying a battered helmet and an old rock hammer;
- calm rather than visibly angry during confrontation;
- capable of becoming deeply intimidating through posture alone.

His rock hammer is a working tool, not a decorative weapon.

His previously mentioned metal-seeking compass remains provisional until its function and origin are developed.

## Continuity Constraints

- Orin is Foreman of the Gearbreaker Mines.
- His formal Miners' Guild leadership remains unresolved.
- Worker safety always comes before production.
- He will walk a crew off site rather than obey an unsafe order.
- He is gruff, obstinate, and nearly impossible to persuade after making a safety decision.
- He is stubborn but not irrational; his judgments consistently arise from evidence, experience, and responsibility.
- He rarely raises his voice.
- He acts decisively and does not continue negotiating once immediate danger requires action.
- He is not afraid of violence, but understands it well enough not to use it casually.
- He initiated the miners' defensive posture during the Gearbreaker Standoff only after a Watch officer physically endangered a miner.
- The miners took exactly one step forward and did not attack.
- His crews are fiercely loyal because he has earned their loyalty.
- He quietly supports struggling miners and families.
- He has little tolerance for carelessness that endangers a crew.
- He protects both the workers and the mountain.
- He and Juniper Bell know one another only by name and reputation at present.
- He must never become merely a grumpy miner or anti-government caricature.

## Unresolved Canon Questions

1. Does Orin formally lead the Miners' Guild or reject its administrative leadership?
2. Who ordered excavation to resume at the six-socket wall?
3. What lies beyond the wall?
4. Who constructed the oldest tunnels?
5. Why are there exactly six sockets?
6. Why does the mountain react differently around Amelia?
7. What produces the Quiet Choir vibrations beneath the mines?
8. Has Orin unknowingly crossed Underclock routes?
9. What happened to Tunnel Twenty-Seven?
10. Why do survey marks resemble First Mechanist symbols?
11. Is the metal-seeking compass canonical, and where did it come from?
12. What does Orin believe the mountain is protecting?
13. Why do some tunnels disappear from memory while remaining physically present?
14. Has Orin encountered a hidden garden below the city without recognizing it?
15. Who mediated the Gearbreaker Standoff?
16. Which miner was physically forced by the Watch constable?
17. Did merchant or industrial pressure deliberately distort the mine-safety report?
18. What would happen if all six sockets were filled?

## Development Checklist

- [x] Two supplied source descriptions reconciled.
- [x] Foreman role established.
- [x] Leadership style established.
- [x] Crew loyalty and quiet generosity established.
- [x] Gearbreaker Standoff linked as historical event.
- [x] Relationships defined without forcing future alliances.
- [x] Main story connections defined.
- [x] Side-story hooks recorded.
- [x] Unresolved canon questions retained.
- [ ] Resolve formal Miners' Guild office.
- [ ] Generate canonical portrait.
- [ ] Create artifact record for his hammer, compass, or closure report when story-relevant.
- [ ] Draft *The Watchman's Regret*.
"""


def watchmans_regret() -> str:
    return """
---
story_arc_id: AH-ARC-006
name: The Watchman's Regret
aliases: []
type: Coming-of-age story concept
series: The Brass Guardian / The Aetherhaven Chronicles
canon_status: Canonical future story concept
canonical_scope: Volume 2 or later; exact placement unresolved
last_updated: 2026-08-02
primary_characters:
  - Amelia Hawthorne
  - unnamed veteran Brass Watch officer
  - Orin Flint
supporting_characters:
  - Chief Inspector Beatrice Thorne
  - Professor Elias Hawthorne
primary_locations: []
related_historical_events:
  - The Gearbreaker Standoff
related_artifacts: []
central_themes:
  - certainty versus understanding
  - good people on opposing sides
  - responsibility and authority
  - mentorship after failure
---

# The Watchman's Regret

## Canonical Story Purpose

*The Watchman's Regret* is a future coming-of-age story in which [Amelia Hawthorne](../characters/Amelia_Hawthorne.md) learns that good people can stand on opposite sides of the same line while each believes they are protecting someone.

The story uses the [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) as a flashback narrated by the former young constable whose physical attempt to force a miner toward the closed mine triggered [Orin Flint](../characters/Orin_Flint.md)'s defensive action.

The story is emotionally about Amelia, not Orin.

## Amelia's Inciting Mistake

Amelia makes a well-intentioned decision while convinced that she understands a complex situation.

She does not act maliciously. Her intervention may even solve part of the immediate problem. However, she acts without understanding every person, risk, or institutional responsibility involved and places herself or others close enough to danger that the Brass Watch must intervene.

The exact mistake remains unassigned so it can arise naturally from the volume's active plot.

Possible structures include:

- Amelia enters a restricted area to help someone before learning why it was sealed;
- she moves or activates evidence during an emergency;
- she protects a frightened person whom the Watch has lawful reason to contain;
- she interferes with a Watch operation because she recognizes a mechanical danger but not the human danger;
- she seeks out the veteran officer afterward because Thorne's official explanation does not answer the moral question troubling her.

The mistake should place Amelia in the Watch's crosshairs without making her reckless, selfish, or unrecognizable.

## The Watchman

The Watchman is the unnamed former young constable from the Gearbreaker Standoff.

By the time Amelia meets him, he is an older and respected officer, investigator, trainer, evidence custodian, or recently retired veteran. His exact current role remains open.

He does not tell Amelia the story to confess dramatically or obtain forgiveness.

He recognizes in her the same dangerous certainty he once carried.

> **I thought I understood the situation. Turns out I understood the order. Those aren't always the same thing.**

## Natural Connection to Amelia

The final story should choose one natural connection:

1. **Assigned contact:** Thorne places Amelia under the veteran's supervision while she repairs, catalogs, or assists with work connected to her mistake.
2. **Evidence encounter:** Amelia finds his name or partial testimony in an old file and seeks him out.
3. **Repeated patrol contact:** He has encountered Amelia during prior Watch incidents and recognizes that she is struggling after this one.
4. **Voluntary mentorship:** He approaches Amelia because he sees the Watch treating her as a problem rather than a young person needing context.
5. **Community consequence:** Amelia must help restore something damaged or disrupted by her decision, and he is responsible for overseeing the work.

The meeting must feel earned rather than arranged only to deliver exposition.

## Flashback Structure

The Standoff is shown primarily through the Watchman's memory.

His account should include:

- the Watch expecting reluctant workers rather than disciplined resistance;
- the miners' silence;
- Orin's refusal;
- the Watchman's physical attempt to force a miner;
- Orin's deliberate raising of the hammer;
- the miners following without looking toward Orin;
- exactly one step forward;
- the horrifying realization that the Watch was unprepared;
- younger officers continuing to escalate verbally;
- experienced officers dividing the Watch ranks by refusing a reckless advance;
- the unresolved mediator;
- the later tunnel collapse;
- the long delay before the Watchman understood the full meaning of his mistake.

His account is a primary source, not guaranteed omniscience. Other participants may remember details differently.

## Core Lesson

Amelia begins with a simpler moral assumption: good people should make good choices, and a correct intention should identify the correct side.

She leaves understanding that:

- Vale believed she was protecting the city;
- Thorne believed lawful order protected everyone;
- the young constable believed obedience was responsibility;
- Orin believed protecting his crew required refusal;
- people may share good intentions while lacking the same information;
- certainty can be more dangerous than fear.

The question Amelia begins carrying into later political arcs is:

> **What does each person believe they are protecting?**

## Key Dialogue

The Watchman:

> **I thought I understood the situation. Turns out I understood the order. Those aren't always the same thing.**

Amelia:

> **Were you afraid?**

The Watchman:

> **No. I was absolutely certain. That frightened me much later.**

Amelia:

> **Who was right?**

The Watchman:

> **The mountain. We were lucky enough to learn that before it buried us.**

## Relationship with Chief Inspector Beatrice Thorne

Thorne may explain that the young constable became one of her finest officers not despite the event, but because he learned from it.

> **Because of what happened.**

This should demonstrate that Thorne values disciplined growth rather than permanent condemnation.

## Relationship with Orin Flint

The Watchman and Orin have not needed a dramatic reconciliation.

The apology may have occurred through years of changed behavior, safer Watch practice, and the officer's willingness to teach younger members what he learned.

Whether they ever spoke privately after the Standoff remains unresolved.

## Story Beats

1. Amelia makes a well-intentioned but insufficiently informed decision.
2. The Brass Watch intervenes, and Amelia feels misunderstood or unfairly judged.
3. Consequences place her in contact with the veteran Watchman.
4. He recognizes certainty rather than malice.
5. He tells the Gearbreaker story in fragments rather than one uninterrupted lecture.
6. Amelia initially searches for the single person who was right.
7. The Watchman's account reveals competing duties and incomplete information.
8. Amelia applies the lesson to the present problem rather than merely apologizing.
9. Thorne acknowledges the Watchman's growth.
10. Amelia asks who was right and receives the answer: the mountain.

## Continuity Constraints

- The story is a coming-of-age lesson for Amelia.
- Amelia's mistake is well intentioned and plausible.
- The Watchman is the young constable who crossed the line at Gearbreaker.
- He has grown into a respected veteran or equivalent mature figure.
- The story does not portray Orin as bloodthirsty or the Watch as uniformly abusive.
- The flashback preserves the one-step advance and absence of physical injury.
- The mediator remains unresolved unless a later canon decision deliberately reveals the identity.
- The Watchman's account may be incomplete or subjective without being dishonest.
- Amelia must apply the lesson to the active story problem.
- The emotional resolution is understanding, not merely punishment or absolution.

## Unresolved Story Questions

1. What present-day decision places Amelia in conflict with the Watch?
2. Does Thorne assign Amelia to the Watchman, or does Amelia seek him out?
3. What is the Watchman's name and present role?
4. Which miner did he attempt to force?
5. Has he ever apologized directly to Orin?
6. Does Orin appear in the present-day story or only in flashback?
7. What active problem allows Amelia to demonstrate that she learned the lesson?
8. At what point in the larger series does Amelia need this moral framework?
9. Does the story expose missing official records or remain centered on personal testimony?
10. What artifact anchors the flashback: Orin's report, a Watch badge, a damaged helmet, or another object?

## Development Checklist

- [x] Historical event linked.
- [x] Coming-of-age purpose established.
- [x] Watchman identity function established but name preserved.
- [x] Key dialogue preserved.
- [x] Flashback constraints preserved.
- [ ] Select Amelia's inciting mistake.
- [ ] Choose the natural meeting structure.
- [ ] Define the Watchman's current role and name.
- [ ] Create or select the anchoring artifact.
- [ ] Outline the present-day plot.
- [ ] Draft the complete story.
"""


def build_events() -> None:
    write("templates/Historical_Event_Profile_Template.md", historical_template())
    write("historical_events/README.md", historical_readme())
    write("historical_events/The_Gearbreaker_Standoff.md", gearbreaker_standoff())

    write("historical_events/The_Rising.md", event_file(
        "AH-HIST-002", "The Rising",
        "The Rising is the unresolved event that transformed the Clockwork Gardens and portions of Aetherhaven's waterways into their present configuration. Surviving surveys disagree about dates, elevations, canals, and whether the Gardens rose, the water fell, or civic chronology adjusted around both.",
        locations=["[The Clockwork Gardens](../locations/The_Clockwork_Gardens.md)", "[The Reflection Canals](../locations/The_Reflection_Canals.md)"],
        arcs=["Future Gardens history arc, not yet assigned"],
        constraints=["Current floating-garden geography and earlier water-filled surveys must both remain valid evidence.", "Do not define one complete cause until temporal and Garden canon is ready."],
        questions=["What physically rose?", "Why do records preserve different water levels?", "Did the event occur once or across several adjusted chronologies?"]
    ))

    write("historical_events/The_First_Continuance.md", event_file(
        "AH-HIST-003", "The First Continuance",
        "The First Continuance is the earliest event cited as precedent for the Doctrine of Continuance and the extraordinary powers later claimed by the High Council during threats to Aetherhaven's survival. The event's date, crisis, participants, and original legal meaning remain sealed or contradictory.",
        organizations=["[The High Council of Aetherhaven](../organizations/The_High_Council_of_Aetherhaven.md)"],
        arcs=["[The Thirteenth Chair](../story_arcs/The_Thirteenth_Chair.md)"],
        constraints=["Do not assume the modern Council's interpretation matches the original event.", "Do not identify the First Mechanist who may have participated."],
        questions=["What crisis required the First Continuance?", "Was the Thirteenth Chair occupied?", "Which modern emergency powers were added later?"]
    ))

    write("historical_events/The_Disappearance_of_Prototype_I.md", event_file(
        "AH-HIST-004", "The Disappearance of Prototype I",
        "Prototype I displayed alarming autonomy, memory, or Bearer-responsive behavior. The Order of the Closed Eye issued Closure, altered records and witnesses, and attempted a Quiet Transfer. A Ninth Guild front deceived an Underclock crew into extracting what they believed was a conscious captive being moved for erasure. The handoff failed. The Order lost custody, the Ninth Guild never completed accession, and Prototype I's location remains unresolved.",
        status="Canonical historical event",
        participants=["Prototype I"],
        organizations=["[The Order of the Closed Eye](../organizations/The_Order_of_the_Closed_Eye.md)", "[The Ninth Guild](../organizations/The_Ninth_Guild.md)", "[The Underclock](../organizations/The_Underclock.md)"],
        arcs=["[The Disappearance of Prototype I](../story_arcs/The_Disappearance_of_Prototype_I.md)", "[The Black Catalogue Arc](../story_arcs/The_Black_Catalogue_Arc.md)"],
        constraints=["The broader Unwound movement was not responsible.", "The Underclock was manipulated rather than knowingly serving the Ninth Guild.", "Prototype I may have agency."],
        questions=["Where did Prototype I go?", "Did it decline transfer under its own power?", "Who designed the false rescue story?"]
    ))

    write("historical_events/The_Resolute_Incident.md", event_file(
        "AH-HIST-005", "The Resolute Incident",
        "The airship *Resolute*, captained by Mara Voss, disappeared for seven civic months while only nineteen days passed aboard. It returned with clocks running backward and records that identify Mara as sole passenger despite her role as captain and the existence of conflicting crew manifests.",
        status="Canonical historical event",
        locations=["[The Aerial Docks](../locations/The_Aerial_Docks.md)", "[The Quiet Hangar](../locations/The_Quiet_Hangar.md)"],
        participants=["[Captain Mara Voss](../characters/Captain_Mara_Voss.md)", "[Silas Rook](../characters/Silas_Rook_The_Stillmaker.md)"],
        organizations=["[The Aerial Mariners' Union](../organizations/The_Aerial_Mariners_Union.md)", "[The Brass Watch](../organizations/The_Brass_Watch.md)"],
        arcs=["Future Resolute and Stillmaker revelations"],
        constraints=["Seven civic months and nineteen aboard-days remain canonical.", "Mara's sole-passenger record remains contradictory rather than corrected.", "Silas returned out of sequence."],
        questions=["Where did the Resolute travel?", "What happened to the crew?", "Why do the clocks count backward toward the Morningstar date?"]
    ))

    write("historical_events/The_Closing_of_Dock_Zero.md", event_file(
        "AH-HIST-006", "The Closing of Dock Zero",
        "Dock Zero was sealed, restricted, or removed from ordinary port use despite predating the modern Aerial Docks. The exact incident that caused the closure, the authority that ordered it, and the relationship between Dock Zero and the Morningstar berth remain unresolved.",
        locations=["[Dock Zero](../locations/Dock_Zero.md)", "[The Aerial Docks](../locations/The_Aerial_Docks.md)", "[The Morningstar Berth](../locations/The_Morningstar_Berth.md)"],
        participants=["[The Passenger of Dock Zero](../characters/The_Passenger_of_Dock_Zero.md)"],
        arcs=["Future Passenger and Morningstar story"],
        constraints=["Do not assume the Passenger caused the closure.", "Dock Zero predates the recognized port."],
        questions=["Who closed Dock Zero?", "Was it ever open in the current chronology?", "Why do its lights activate during storms?"]
    ))

    write("historical_events/The_Revision_of_the_Society_of_Explorers_Charter.md", event_file(
        "AH-HIST-007", "The Revision of the Society of Explorers Charter",
        "The Society of Explorers underwent a major institutional change that produced a revised seal and likely a revised charter. Both active seal variants are valid historical evidence. The older lantern-centered seal reflects the Society's original grounded identity as explorers carrying light into unknown places and creates a symbolic connection to the Lamplighters' Fellowship. The later world-centered seal suggests broader navigation, global reach, celestial or temporal investigation, and the Society's changing understanding of exploration.",
        status="Canonical working historical event",
        organizations=["[The Society of Explorers](../organizations/The_Society_of_Explorers.md)", "[The Lamplighters' Fellowship](../organizations/The_Lamplighters_Fellowship.md)"],
        arcs=["Future Society history and temporal-exploration arc"],
        constraints=["Both seal variants remain valid.", "Do not choose one seal as a correction of the other.", "The cause and date of the institutional change remain unresolved."],
        questions=["What event forced the charter revision?", "Did the Society expand into temporal work before or after the seal changed?", "What formal or symbolic relationship exists with the Lamplighters?"]
    ))

    write("historical_events/The_Founding_of_the_Conservancy.md", event_file(
        "AH-HIST-008", "The Founding of the Conservancy",
        "The Conservancy of Living Mechanisms formed to tend, heal, advocate for, and protect the Clockwork Gardens and other living machinery. Its modern hierarchy may be younger than the Keeper title held by Juniper Bell.",
        organizations=["[The Conservancy of Living Mechanisms](../organizations/The_Conservancy_of_Living_Mechanisms.md)"],
        participants=["[Juniper Bell](../characters/Juniper_Bell.md)", "[The First Tender](../characters/The_First_Tender.md)"],
        constraints=["Juniper is not automatically the founder.", "The Keeper title predates or exists outside modern hierarchy."],
        questions=["Who formally founded the Conservancy?", "Did the Gardens request its creation?", "What relationship did early Verdant Mechanists have to it?"]
    ))

    write("historical_events/The_Ash_Compact.md", event_file(
        "AH-HIST-009", "The Ash Compact",
        "The Ash Compact is the practical accommodation that allows the Cauldron and Aetherhaven's outside authorities to coexist despite incompatible claims of law, representation, refuge, trade, and enforcement. Its exact terms, signatories, date, and legal status remain unresolved.",
        locations=["[The Cauldron](../locations/The_Cauldron.md)"],
        organizations=["[The High Council of Aetherhaven](../organizations/The_High_Council_of_Aetherhaven.md)", "[The Brass Watch](../organizations/The_Brass_Watch.md)", "[The Furnace Court](../organizations/The_Furnace_Court.md)", "[The Cinder Wardens](../organizations/The_Cinder_Wardens.md)"],
        participants=["[The Cinder Regent](../characters/The_Cinder_Regent.md)"],
        constraints=["The Compact does not place the Cauldron under ordinary Council control.", "The identity of the Cinder Regent remains unassigned."],
        questions=["Who negotiated the Compact?", "Is it written, spoken, or enforced through precedent?", "What action would break it?"]
    ))

    write("historical_events/The_Founding_of_the_Eight_Guilds.md", event_file(
        "AH-HIST-010", "The Founding of the Eight Guilds",
        "The Eight Founding Engineering Guilds organized the human civic and technical systems that made early Aetherhaven livable. Their creation established the Conclave of Eight and the enduring distinction between eightfold civic order and the older sixfold mechanisms beneath the city.",
        organizations=["[The Eight Founding Engineering Guilds](../organizations/The_Eight_Founding_Engineering_Guilds.md)", "[The Conclave of Eight](../organizations/The_Conclave_of_Eight.md)"],
        locations=["[The Octagonal Hall](../locations/The_Octagonal_Hall.md)"],
        constraints=["Eight represents human civic order; six represents the older Keys and Heart systems.", "Do not retroactively make the Ninth Guild one of the publicly founded eight."],
        questions=["Were the guilds founded simultaneously?", "What knowledge did they inherit rather than invent?", "Did the First Mechanist oversee the founding?"]
    ))

    write("historical_events/The_Opening_of_the_Aerial_Docks.md", event_file(
        "AH-HIST-011", "The Opening of the Aerial Docks",
        "The modern Aerial Docks opened as Aetherhaven's primary commercial airship port around older structures, including Dock Zero. The event formalized customs, mooring, freight, passenger, and safety systems without explaining everything already present at the site.",
        locations=["[The Aerial Docks](../locations/The_Aerial_Docks.md)", "[Dock Zero](../locations/Dock_Zero.md)"],
        organizations=["[The Aerial Mariners' Union](../organizations/The_Aerial_Mariners_Union.md)"],
        constraints=["Dock Zero predates the modern port.", "Do not assume the opening marks the first aerial arrival at the site."],
        questions=["Who designed the modern docks?", "Why was Dock Zero incorporated rather than demolished?", "When did the Quiet Hangar receive its present function?"]
    ))

    write("historical_events/The_First_Dream_Bloom.md", event_file(
        "AH-HIST-012", "The First Dream Bloom",
        "The First Dream Bloom is the earliest remembered or recorded flowering associated with the Dream Engine, the Moon Garden, or dream-bearing silver blossoms. Accounts may describe a physical botanical event, a shared dream, a memory preserved by the Gardens, or several overlapping experiences.",
        locations=["[The Moon Garden](../locations/The_Moon_Garden.md)", "[The Clockwork Gardens](../locations/The_Clockwork_Gardens.md)"],
        participants=["[Juniper Bell](../characters/Juniper_Bell.md)"],
        arcs=["[The Keeper of Dreams](../story_arcs/The_Keeper_of_Dreams.md)"],
        constraints=["Dream, memory, and physical travel may overlap.", "Do not define Juniper's age or nature through this event alone."],
        questions=["Was it truly the first bloom?", "Who witnessed it?", "Did the Dream Engine awaken or merely become visible?"]
    ))

    write("historical_events/The_Great_Garden_Rearrangement.md", event_file(
        "AH-HIST-013", "The Great Garden Rearrangement",
        "The Great Garden Rearrangement is a proposed name for a major reordering of the Clockwork Gardens' paths, waterways, elevations, and hidden layers. It may be distinct from the Rising, one phase of it, or a later civic attempt to describe changes that occurred across more than one chronology.",
        locations=["[The Clockwork Gardens](../locations/The_Clockwork_Gardens.md)"],
        participants=["[Juniper Bell](../characters/Juniper_Bell.md)"],
        constraints=["Do not merge this event with the Rising until their relationship is decided.", "The Gardens are active participants rather than passive landscaping."],
        questions=["Was the Rearrangement intentional?", "Did Juniper witness or negotiate it?", "Which paths disappeared from official memory?"]
    ))

    write("historical_events/The_Night_of_Silent_Clocks.md", event_file(
        "AH-HIST-014", "The Night of Silent Clocks",
        "The Night of Silent Clocks is a proposed historical event during which synchronized clocks across part or all of Aetherhaven stopped, lost agreement, or failed to record a shared interval. The exact event is not yet supported by a complete canonical account.",
        locations=["[The Clocktower Spire](../locations/The_Clocktower_Spire.md)"],
        organizations=["[The Keepers of Time](../organizations/The_Keepers_of_Time.md)", "[The Guild of Clockwrights](../organizations/The_Guild_of_Clockwrights.md)"],
        constraints=["Do not confuse this proposed event with every ordinary Lost Second.", "Do not establish a date or cause without further canon."],
        questions=["Did every clock stop?", "What continued moving?", "Who remembers the missing interval?"]
    ))

    write("historical_events/The_Last_Morningstar_Manifest.md", event_file(
        "AH-HIST-015", "The Last Morningstar Manifest",
        "The Last Morningstar Manifest is the proposed final known cargo or passenger record associated with the Morningstar Company before its offices, employees, and ships disappeared from ordinary registries. Whether it is truly the last manifest, a future document, or a record from another chronology remains unresolved.",
        locations=["[The Southern Docks](../locations/The_Southern_Docks.md)", "[The Morningstar Berth](../locations/The_Morningstar_Berth.md)"],
        participants=["[The Passenger of Dock Zero](../characters/The_Passenger_of_Dock_Zero.md)"],
        arcs=["Future Morningstar and Passenger story"],
        constraints=["Morningstar has no current registered offices, employees, or ships.", "Do not assume the manifest belongs to the current chronology."],
        questions=["What cargo was listed?", "Who signed it?", "Was it created before or after the Passenger's ticket date?"]
    ))


def patch_existing_profiles() -> None:
    replace_section("characters/Chancellor_Octavia_Vale.md", "The Gearbreaker Standoff", """
[The Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) is one of the defining failures and lessons of Octavia Vale's public career.

Vale authorized a lawful compliance action after receiving incomplete information and intense pressure to restore mine production. She did not intend violence, but underestimated Orin Flint's practical authority, the loyalty of his crews, and the danger of using the Brass Watch to resolve a specialized safety dispute.

After the standoff and the later tunnel collapse, Vale stopped assuming that a lawful order could substitute for local knowledge. She still challenges Orin, but now asks why before deciding how civic authority should respond.

The incident remains a public embarrassment. Orin does not exploit it, and Vale does not pretend it never happened.
""")

    replace_section("characters/Chief_Inspector_Beatrice_Thorne.md", "The Gearbreaker Standoff", """
[The Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) permanently changed Thorne's understanding of operational authority.

She did not order officers to assault miners. Nevertheless, an inexperienced constable crossed the line, and the Watch's internal disagreement became the only thing preventing further escalation before a mediator arrived.

Thorne learned that authority without situational understanding can become dangerous. When Orin now closes a tunnel, her first useful response is not to demand his legal authority but to say:

> **Show me.**

The exact extent of Thorne's direct presence during the decisive moments remains unresolved.
""")

    replace_section("organizations/The_Brass_Watch.md", "Institutional Memory: The Gearbreaker Standoff", """
[The Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) is an informal but powerful lesson within the Brass Watch.

A young constable's attempt to physically force a miner toward a closed shaft triggered a disciplined defensive response from Orin Flint and the assembled crews. Veteran officers recognized that the Watch was unprepared for the confrontation and resisted further escalation inside their own ranks.

No formal regulation says never force Orin Flint into the mountain.

No formal regulation is needed.

The future story [The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md) follows the constable who caused the defining moment and later became a respected veteran shaped by what he learned.
""")

    replace_section("organizations/The_High_Council_of_Aetherhaven.md", "Institutional Memory: The Gearbreaker Standoff", """
The [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) exposed the limits of Council authority when civic urgency, merchant pressure, and incomplete technical information combine.

The Council's attempt to compel mine production nearly produced bloodshed and was later discredited by the collapse of the tunnel Orin Flint had refused to reopen.

The event remains politically embarrassing and is rarely discussed in formal session. It nevertheless shapes modern Council treatment of mine closures, specialist authority, and Brass Watch compliance actions.
""")

    replace_section("locations/The_Gearbreaker_Mines.md", "Historical Event: The Gearbreaker Standoff", """
The mine entrance was the site of the [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md), when Orin Flint and the mining crews resisted a failed Brass Watch attempt to force a return to unsafe work.

The miners raised tools only after a Watch constable physically attempted to force one crew member toward the shaft. They took exactly one step forward and held position. No one was physically injured. The disputed tunnel collapsed several days later.

The incident established the modern unwritten rule that when Orin closes the mountain, outside authorities proceed by evidence and negotiation rather than force.
""")

    replace_section("organizations/The_Miners_Guild.md", "The Gearbreaker Standoff", """
The [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) demonstrated the practical solidarity of the Gearbreaker crews and Orin Flint's authority among miners.

The event does not yet prove that Orin formally leads the entire Miners' Guild. It does establish that experienced Gearbreaker crews would walk off site with him rather than accept an unsafe external order.
""")

    replace_section("organizations/The_Quiet_Choir.md", "Relationship to the Gearbreaker Mines", """
Rhythmic vibrations associated with the Quiet Choir have been reported in abandoned pipe systems beneath the [Gearbreaker Mines](../locations/The_Gearbreaker_Mines.md).

[Orin Flint](../characters/Orin_Flint.md) has learned not to answer them. He may not know the network's accepted name or nature during early stories.

This connection remains exploratory and does not establish that the Quiet Choir caused the [Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md), the later tunnel collapse, or the six-socket wall.
""")


def patch_artifact_history_links() -> None:
    mappings = {
        "artifacts/002_Seal_of_the_Society_of_Explorers.md": "- [The Revision of the Society of Explorers Charter](../historical_events/The_Revision_of_the_Society_of_Explorers_Charter.md)\n\nBoth active seal variants remain valid evidence from different periods or functions of the Society.",
        "artifacts/011_Prototype_II_Cabinet_Photograph.md": "- [The Disappearance of Prototype I](../historical_events/The_Disappearance_of_Prototype_I.md)",
        "artifacts/012_The_Missing_Prototype_I_Catalog_Card.md": "- [The Disappearance of Prototype I](../historical_events/The_Disappearance_of_Prototype_I.md)",
        "artifacts/015_Botanical_Plate_of_the_Dream_Blossom.md": "- [The First Dream Bloom](../historical_events/The_First_Dream_Bloom.md)",
        "artifacts/018_The_Changing_Paths_of_the_Gardens.md": "- [The Rising](../historical_events/The_Rising.md)\n- [The Great Garden Rearrangement](../historical_events/The_Great_Garden_Rearrangement.md)",
        "artifacts/025_The_Passengers_Future_Dated_Ticket.md": "- [The Closing of Dock Zero](../historical_events/The_Closing_of_Dock_Zero.md)\n- [The Last Morningstar Manifest](../historical_events/The_Last_Morningstar_Manifest.md)",
        "artifacts/027_The_Morningstar_Company_Manifest.md": "- [The Last Morningstar Manifest](../historical_events/The_Last_Morningstar_Manifest.md)",
        "artifacts/028_Captain_Mara_Vosss_Backward_Clock.md": "- [The Resolute Incident](../historical_events/The_Resolute_Incident.md)",
        "artifacts/056_High_Council_Thirteenth_Seat_Record.md": "- [The First Continuance](../historical_events/The_First_Continuance.md)",
    }
    for path, content in mappings.items():
        replace_section(path, "Related Historical Events", content, before="## Continuity Notes")


def patch_standards_and_indexes() -> None:
    standard = ROOT / "docs/standards/CANON_MARKDOWN_STANDARD.md"
    if standard.exists():
        text = standard.read_text(encoding="utf-8")
        section = """
## Historical-Event Records

Historical events belong in `historical_events/` and use [templates/Historical_Event_Profile_Template.md](templates/Historical_Event_Profile_Template.md).

A historical-event file owns:

- the objective event,
- public and restricted accounts,
- participants and institutions,
- the known timeline,
- conflicting testimony,
- physical evidence and provenance,
- institutional consequences,
- continuity constraints,
- and unresolved historical questions.

A story arc owns how Amelia and the reader discover, experience, or interpret that history.

Profiles and artifacts should link to the event rather than repeat its full chronology. Historical records must preserve uncertainty and must not convert rumor into fact.

Every historical event ends with an **Archival Status** section containing:

- Public Record,
- Restricted Record,
- Order Interest,
- Primary Sources,
- and Outstanding Historical Questions.

Artifacts should link to relevant historical events through a **Related Historical Events** section. Provenance belongs in the artifact record; the complete event chronology belongs in the historical-event record.

"""
        if "## Historical-Event Records" not in text:
            marker = "## Source Priority"
            if marker in text:
                text = text.replace(marker, section + marker, 1)
            else:
                text = text.rstrip() + "\n\n" + section
            standard.write_text(text, encoding="utf-8")

    project = ROOT / "docs/PROJECT_INDEX.md"
    if project.exists():
        text = project.read_text(encoding="utf-8")
        if "templates/Historical_Event_Profile_Template.md" not in text:
            marker = "| [templates/Story_Arc_Profile_Template.md](templates/Story_Arc_Profile_Template.md) | Standard structure for story-arc records |\n"
            text = text.replace(marker, marker + "| [templates/Historical_Event_Profile_Template.md](templates/Historical_Event_Profile_Template.md) | Standard structure for objective in-world historical-event records |\n")
        section = """
## Historical Events

Historical-event records own objective in-world events, while story arcs own how Amelia and the reader discover or experience them.

See the [Historical Events Index](historical_events/README.md).

| Event | Canon status | File |
|---|---|---|
| The Gearbreaker Standoff | Canonical historical event | [The_Gearbreaker_Standoff.md](historical_events/The_Gearbreaker_Standoff.md) |
| The Rising | Historical placeholder | [The_Rising.md](historical_events/The_Rising.md) |
| The First Continuance | Historical placeholder | [The_First_Continuance.md](historical_events/The_First_Continuance.md) |
| The Disappearance of Prototype I | Canonical historical event | [The_Disappearance_of_Prototype_I.md](historical_events/The_Disappearance_of_Prototype_I.md) |
| The Resolute Incident | Canonical historical event | [The_Resolute_Incident.md](historical_events/The_Resolute_Incident.md) |
| The Closing of Dock Zero | Historical placeholder | [The_Closing_of_Dock_Zero.md](historical_events/The_Closing_of_Dock_Zero.md) |
| Revision of the Society of Explorers Charter | Canonical working history | [The_Revision_of_the_Society_of_Explorers_Charter.md](historical_events/The_Revision_of_the_Society_of_Explorers_Charter.md) |
| The Founding of the Conservancy | Historical placeholder | [The_Founding_of_the_Conservancy.md](historical_events/The_Founding_of_the_Conservancy.md) |
| The Ash Compact | Historical placeholder | [The_Ash_Compact.md](historical_events/The_Ash_Compact.md) |
| The Founding of the Eight Guilds | Historical placeholder | [The_Founding_of_the_Eight_Guilds.md](historical_events/The_Founding_of_the_Eight_Guilds.md) |
| The Opening of the Aerial Docks | Historical placeholder | [The_Opening_of_the_Aerial_Docks.md](historical_events/The_Opening_of_the_Aerial_Docks.md) |
| The First Dream Bloom | Historical placeholder | [The_First_Dream_Bloom.md](historical_events/The_First_Dream_Bloom.md) |
| The Great Garden Rearrangement | Historical placeholder | [The_Great_Garden_Rearrangement.md](historical_events/The_Great_Garden_Rearrangement.md) |
| The Night of Silent Clocks | Historical placeholder | [The_Night_of_Silent_Clocks.md](historical_events/The_Night_of_Silent_Clocks.md) |
| The Last Morningstar Manifest | Historical placeholder | [The_Last_Morningstar_Manifest.md](historical_events/The_Last_Morningstar_Manifest.md) |

"""
        if "## Historical Events" not in text:
            marker = "## Artifact Image Slate"
            text = text.replace(marker, section + marker, 1)
        text = text.replace("- **5** long-range or hidden story-arc profiles", "- **6** long-range or hidden story-arc profiles\n- **15** historical-event records")
        project.write_text(text, encoding="utf-8")

    linker = ROOT / "scripts/link_markdown_references.py"
    if linker.exists():
        text = linker.read_text(encoding="utf-8")
        old = '    "artifact": ROOT / "artifacts",\n}'
        new = '    "artifact": ROOT / "artifacts",\n    "story_arc": ROOT / "story_arcs",\n    "historical_event": ROOT / "historical_events",\n}'
        if old in text:
            text = text.replace(old, new, 1)
            linker.write_text(text, encoding="utf-8")

    todo = ROOT / "scripts/build_canon_development_todo.py"
    if todo.exists():
        text = todo.read_text(encoding="utf-8")
        old = '    "Location": ROOT / "locations",\n}'
        new = '    "Location": ROOT / "locations",\n    "Historical Event": ROOT / "historical_events",\n}'
        if old in text:
            text = text.replace(old, new, 1)
        old_visual = '    elif record.kind == "Location":\n        action = "Add a labeled Aetherhaven map callout and generate or select at least one canonical establishing image; embed both under `Map Reference` and `Visual Reference`."\n    else:'
        new_visual = '    elif record.kind == "Location":\n        action = "Add a labeled Aetherhaven map callout and generate or select at least one canonical establishing image; embed both under `Map Reference` and `Visual Reference`."\n    elif record.kind == "Historical Event":\n        action = "Create or link a canonical historical illustration, evidence collage, photograph, document, or artifact set; preserve conflicting accounts and avoid depicting unresolved facts as certain."\n    else:'
        if old_visual in text:
            text = text.replace(old_visual, new_visual, 1)
        todo.write_text(text, encoding="utf-8")


def main() -> int:
    build_events()
    write("characters/Orin_Flint.md", orin_profile())
    write("story_arcs/The_Watchmans_Regret.md", watchmans_regret())
    patch_existing_profiles()
    patch_artifact_history_links()
    patch_standards_and_indexes()
    print("Historical-event architecture, Gearbreaker canon, and Watchman's Regret records generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
