#!/usr/bin/env python3
"""Preserve the Amelia-Orin relationship arc within Watchman's Regret canon.

The historical-event builder owns the base Orin and Watchman's Regret files.
This deterministic refinement records the earlier-volume tension between Amelia
and Orin, the personal meaning Amelia gains from the Gearbreaker account, and
the partial reconciliation that follows without making Orin permissive or
removing the danger of the mines.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_section(path: str, heading: str, content: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    block = f"## {heading}\n\n{content.strip()}\n\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Missing section {heading!r} in {path}")
    text = pattern.sub(block, text)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def insert_section_before(path: str, heading: str, content: str, before_heading: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    block = f"## {heading}\n\n{content.strip()}\n\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        marker = f"## {before_heading}\n"
        if marker not in text:
            raise RuntimeError(f"Missing insertion marker {before_heading!r} in {path}")
        text = text.replace(marker, block + marker, 1)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_orin() -> None:
    replace_section(
        "characters/Orin_Flint.md",
        "Relationship with Amelia Hawthorne",
        """
Orin's relationship with [Amelia Hawthorne](Amelia_Hawthorne.md) is initially strained.

Across earlier volumes, Amelia and her companions repeatedly seek access to the Gearbreaker Mines or their deeper tunnels while pursuing legitimate mysteries. Orin repeatedly blocks them. Some refusals interrupt promising investigations, prevent Amelia from following evidence, or appear to protect secrets that she believes adults are withholding from her.

Amelia grows frustrated with Orin's obstinacy and begins to interpret his refusals as distrust, territorial control, or an unwillingness to take her seriously. Orin does little to correct that impression. To him, a closed tunnel is a closed tunnel, and a lengthy explanation does not make unstable stone safer.

Orin does not dislike Amelia. He recognizes her intelligence and speaks to her honestly, but he does not yet trust her judgment underground. Curiosity can become dangerous when it outruns experience, and Amelia's unusual connection to ancient machinery makes unrestricted access more dangerous rather than less.

He does not soften a safety decision merely because Amelia's questions are important.

> **You'll get your answers after my people get home.**

[The Watchman's Regret](../story_arcs/The_Watchmans_Regret.md) becomes the turning point in their relationship. Hearing the truth of [the Gearbreaker Standoff](../historical_events/The_Gearbreaker_Standoff.md) allows Amelia to understand that Orin's refusals are not primarily attempts to control her or hide the truth. They come from a man who has already stood against the Council and the Brass Watch rather than permit someone under his protection to be forced into danger.

The resolution does not make Orin permissive, grant Amelia unrestricted access, or erase their differences. Amelia begins asking what Orin sees instead of assuming that his answer is arbitrary. Orin recognizes the change in her judgment and becomes more willing to explain his concerns, hear her evidence, and consider narrowly defined, supervised access when conditions genuinely permit it.

Their trust begins there. It is not completed there.

Orin's protection of Amelia remains governed by the same principle that protects his crews: no one gets to use a person as an expendable tool, including Amelia herself.
""",
    )


def update_watchmans_regret() -> None:
    insert_section_before(
        "story_arcs/The_Watchmans_Regret.md",
        "Secondary Emotional Resolution: Amelia and Orin",
        """
Earlier volumes establish a growing strain between [Amelia Hawthorne](../characters/Amelia_Hawthorne.md) and [Orin Flint](../characters/Orin_Flint.md).

Amelia and her companions are repeatedly blocked from entering the Gearbreaker Mines or following evidence into restricted tunnels. Orin's refusals are legitimate and safety-grounded, but he explains little and refuses to negotiate. From Amelia's perspective, he repeatedly places himself between her and the truth.

That history gives the Watchman's account personal meaning. Amelia does not merely learn an abstract lesson about authority and certainty. She realizes that Orin once faced the full weight of the Council and Brass Watch rather than allow one miner to be forced into danger. His refusal to admit Amelia is the same instinct, applied to someone who does not yet understand why she is being protected.

This realization does not prove that Orin is always right, excuse poor communication, or require Amelia to stop challenging him. It changes the question she asks.

Instead of demanding:

> **Why won't you let me in?**

Amelia begins asking:

> **What do you know that I don't?**

The story should end with a brief coda in which Amelia returns to Orin after speaking with the Watchman. She does not seek unrestricted permission or offer a sentimental apology. She approaches him with a more mature understanding of the responsibility he carries.

Orin notices the difference.

The reconciliation should be restrained and characteristic of both characters. Orin does not become warm or easy. Amelia does not become obedient. He may explain a danger he previously would have dismissed with a single word, invite her to show him the evidence before he decides, or permit a narrowly controlled investigation under conditions he defines.

The reward is not access to every tunnel.

The reward is the beginning of mutual trust.
""",
        "Key Dialogue",
    )

    replace_section(
        "story_arcs/The_Watchmans_Regret.md",
        "Story Beats",
        """
1. Earlier volumes have already established repeated conflict between Amelia and Orin over access to the mines.
2. Amelia makes a well-intentioned but insufficiently informed decision in the present story.
3. The Brass Watch intervenes, and Amelia feels misunderstood or unfairly judged.
4. Consequences place her in contact with the veteran Watchman.
5. He recognizes certainty rather than malice.
6. He tells the Gearbreaker story in fragments rather than one uninterrupted lecture.
7. Amelia initially searches for the single person who was right.
8. The Watchman's account reveals competing duties and incomplete information.
9. Amelia recognizes the connection between Orin's stand at Gearbreaker and his repeated refusal to let her enter unsafe tunnels.
10. Amelia applies the lesson to the active story problem rather than merely apologizing.
11. Thorne acknowledges the Watchman's growth.
12. Amelia asks who was right and receives the answer: the mountain.
13. In a restrained coda, Amelia returns to Orin and approaches the mine dispute differently.
14. Orin recognizes her changed judgment and offers explanation, consideration, or limited supervised cooperation rather than unrestricted access.
""",
    )

    replace_section(
        "story_arcs/The_Watchmans_Regret.md",
        "Continuity Constraints",
        """
- The story is a coming-of-age lesson for Amelia.
- Amelia's mistake is well intentioned and plausible.
- Earlier volumes must establish repeated frustration between Amelia and Orin over denied mine access.
- Orin's earlier refusals are grounded in real safety concerns, even when he communicates them poorly or withholds details.
- The Watchman is the young constable who crossed the line at Gearbreaker.
- He has grown into a respected veteran or equivalent mature figure.
- The story does not portray Orin as bloodthirsty or the Watch as uniformly abusive.
- The flashback preserves the one-step advance and absence of physical injury.
- The mediator remains unresolved unless a later canon decision deliberately reveals the identity.
- The Watchman's account may be incomplete or subjective without being dishonest.
- Amelia must apply the lesson to the active story problem.
- The story must also change how Amelia interprets Orin's protection of the mines.
- The reconciliation does not make Orin permissive, remove mine danger, or grant Amelia unrestricted access.
- Orin and Amelia retain their contrasting personalities; the change is greater understanding and the beginning of earned trust.
- The emotional resolution is understanding, not merely punishment, absolution, obedience, or easy friendship.
""",
    )

    replace_section(
        "story_arcs/The_Watchmans_Regret.md",
        "Unresolved Story Questions",
        """
1. Which earlier-volume incidents most effectively establish Amelia's frustration with Orin?
2. What present-day decision places Amelia in conflict with the Watch?
3. Does Thorne assign Amelia to the Watchman, or does Amelia seek him out?
4. What is the Watchman's name and present role?
5. Which miner did he attempt to force?
6. Has he ever apologized directly to Orin?
7. Does Orin appear throughout the present-day story or only in the closing coda and flashback?
8. What active problem allows Amelia to demonstrate that she learned the lesson?
9. At what point in the larger series does Amelia need this moral framework?
10. Does the story expose missing official records or remain centered on personal testimony?
11. What artifact anchors the flashback: Orin's report, a Watch badge, a damaged helmet, or another object?
12. What specific question does Amelia finally ask Orin after hearing the Watchman's account?
13. What limited explanation, cooperation, or supervised access shows that Orin recognizes her growth?
14. Does Orin acknowledge that his refusal was correct but his communication was not?
""",
    )

    replace_section(
        "story_arcs/The_Watchmans_Regret.md",
        "Development Checklist",
        """
- [x] Historical event linked.
- [x] Coming-of-age purpose established.
- [x] Watchman identity function established but name preserved.
- [x] Key dialogue preserved.
- [x] Flashback constraints preserved.
- [x] Earlier Amelia-Orin tension established as required setup.
- [x] Partial Amelia-Orin reconciliation established as the secondary resolution.
- [ ] Select the earlier mine-access conflicts that build the strain.
- [ ] Select Amelia's inciting mistake.
- [ ] Choose the natural meeting structure.
- [ ] Define the Watchman's current role and name.
- [ ] Create or select the anchoring artifact.
- [ ] Decide the restrained Orin-Amelia coda.
- [ ] Outline the present-day plot.
- [ ] Draft the complete story.
""",
    )


def update_historical_event() -> None:
    path = "historical_events/The_Gearbreaker_Standoff.md"
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    old = """The standoff appears as a flashback narrated by the former young constable who crossed the line. He shares the account when Amelia faces a well-intentioned mistake caused by certainty without sufficient understanding.
"""
    new = """The standoff appears as a flashback narrated by the former young constable who crossed the line. He shares the account when Amelia faces a well-intentioned mistake caused by certainty without sufficient understanding.

The account also gives Amelia the context to reinterpret her earlier conflicts with Orin. Across prior volumes, Orin repeatedly blocks her from entering unsafe or restricted mine passages, creating genuine frustration and a strained relationship. Learning how far he once went to prevent a single miner from being forced into danger helps Amelia understand that his refusals are rooted in responsibility rather than casual obstruction. The historical event does not resolve their relationship by itself; the story arc owns that personal reconciliation.
"""
    if old not in text:
        raise RuntimeError(f"Expected Watchman's Regret paragraph not found in {path}")
    text = text.replace(old, new, 1)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    update_orin()
    update_watchmans_regret()
    update_historical_event()
    print("Refined the Amelia-Orin relationship arc in Watchman's Regret canon.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
