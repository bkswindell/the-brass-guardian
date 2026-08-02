#!/usr/bin/env python3
"""Refine the Institute of Vital Mechanics as a necessary but morally risky institution.

The base placeholder builder establishes the distributed medical network. This
pass preserves that infrastructure while removing modern assumptions of safety,
universal ethics, clinical sophistication, and institutional neutrality.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8")


def add_yaml_item(text: str, key: str, item: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\n(?P<body>(?:  - .*\n)*)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return text
    body = match.group("body")
    line = f"  - {item}\n"
    if line in body:
        return text
    replacement = f"{key}:\n{body}{line}"
    return text[: match.start()] + replacement + text[match.end() :]


def replace_section(text: str, heading: str, content: str) -> str:
    block = f"## {heading}\n\n{content.strip()}\n\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Missing section: {heading}")
    return pattern.sub(block, text)


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


def insert_or_append_relation(path: str, heading: str, content: str) -> None:
    target = ROOT / path
    if not target.exists():
        return
    text = target.read_text(encoding="utf-8")
    for before in ("Continuity Constraints", "Continuity Notes", "Open Canon Questions", "Visual Language"):
        if f"## {before}\n" in text:
            text = insert_section_before(text, heading, content, before)
            write(path, text)
            return
    text = insert_section_before(text, heading, content, "__missing__")
    write(path, text)


def update_institute() -> None:
    path = "organizations/The_Institute_of_Vital_Mechanics.md"
    text = read(path)

    for item in (
        "The Unwound",
        "The Order of the Closed Eye",
        "The Conservancy of Living Mechanisms, occasional resource exchange only",
    ):
        text = add_yaml_item(text, "primary_connections", item)

    text = replace_section(
        text,
        "Canonical Summary",
        """
The Institute of Vital Mechanics is Aetherhaven's principal civic institution for severe medicine, emergency surgery, trauma care, rehabilitation, prosthetics, implants, mechanobiology, and the forced cooperation of living bodies with mechanical technology.

It is necessary.

It is not automatically safe.

The Institute exists because there are injuries, infections, aetheric exposures, industrial accidents, and mechanical integrations that neighborhood healers cannot reliably treat. Its practitioners can preserve lives that would otherwise be lost, replace function that cannot be restored, and keep explorers or workers alive long enough to return home.

They can also recommend treatments more dangerous than the illness, value a successful mechanism above the person attached to it, and mistake the ability to perform a procedure for proof that the procedure should be performed.

The Institute is not a separate medical district and does not replace private physicians, apothecaries, midwives, household remedies, workshop medics, herbalists, or community healers. Most citizens prefer those alternatives for ordinary ailments and approach the Institute only when the risk of avoiding it has become greater than the risk of submitting to its care.

The Institute operates as a distributed network with:

- a central hospital and administrative institution in [the Government District](../locations/The_Government_District.md);
- clinical and research staff embedded within [the Academy of Invention](The_Academy_of_Invention.md);
- prosthetics, implant, and rehabilitation engineering facilities connected to [the Great Workshops](../locations/The_Great_Workshops.md);
- a semi-autonomous recovery house inside [the Cauldron](../locations/The_Cauldron.md);
- field medics and emergency liaisons working beside [the Brass Watch](The_Brass_Watch.md);
- and expeditionary practitioners who may accompany accredited explorers.

The Institute supports biology with technology, but its understanding of biology is incomplete and uneven. Its mechanical skill often exceeds its knowledge of infection, rejection, pain, recovery, and the long-term consequences of intervention.

It can save a life.

It may change that life permanently while doing so.
""",
    )

    text = replace_section(
        text,
        "Public Role",
        """
The Institute's public responsibilities include catastrophic injury response, surgery, prosthetics, implants, rehabilitation, expedition medicine, industrial medicine, and the treatment of aetheric or mechanical trauma.

It is not where most citizens willingly go for a cough, fever, rash, infected cut, difficult pregnancy, or ordinary broken bone.

For common ailments, many residents first seek:

- family remedies;
- an apothecary;
- a neighborhood healer;
- a trusted midwife;
- a workshop medic;
- a Cauldron practitioner;
- or an herbal treatment passed through generations.

Some of those remedies are ineffective or dangerous. Some are better suited to the problem than the Institute's aggressive interventions.

The Institute is most trusted when the alternative is death, loss of a limb, irreversible aether exposure, or a condition no ordinary practitioner understands.

Its public reputation can be summarized as:

> **They may save you. They may also decide that saving you requires becoming someone different.**

Institute advice is respected, feared, questioned, and often taken only after a second opinion from someone the patient personally trusts.
""",
    )

    text = replace_section(
        text,
        "Distributed Presence",
        """
### The Hall of Vital Mechanics

[The Hall of Vital Mechanics](../locations/The_Hall_of_Vital_Mechanics.md) is the Institute's central hospital, training center, records office, research authority, and emergency-coordination headquarters in the Government District.

It is both the best-equipped medical facility in Aetherhaven and the place many citizens most fear being taken.

Public wards coexist with restricted theatres, implant laboratories, anatomical collections, sealed treatment records, and research rooms whose practices are not widely understood.

### Academy Clinical and Research Annex

The Institute maintains a presence within or beside the Academy of Invention for anatomy, physiology, mechanobiology, implant testing, medical-device development, and experimental treatment.

The annex has produced important discoveries and unethical recommendations.

Its practitioners may disagree over whether a procedure is treatment, research, or both. Patients with unusual conditions can attract academic attention that is not always in their interests.

The final formal name and oversight of the annex remain unresolved.

### Great Workshops Prosthetics and Implant Annex

Institute surgeons, prosthetists, rehabilitation staff, and mechanobiologists work with certified engineers in the Great Workshops to create replacement limbs, braces, sensory aids, stabilization frames, adaptive tools, and interfaces between tissue and machinery.

The annex is often excellent at replacing damaged function.

It is not always patient about preserving injured flesh when a mechanical replacement appears faster, more reliable, professionally interesting, or easier to certify.

One practitioner may spend weeks finding the correct herb, drainage method, or rest regimen to clear an infection.

Another may recommend amputation and a proven brass replacement before the infection has been fully understood.

Neither recommendation is automatically foolish. Neither is automatically right.

### The Cauldron Recovery House

[The Cauldron Recovery House](../locations/The_Cauldron_Recovery_House.md) provides rehabilitation, adaptive-device care, industrial-injury treatment, and community medicine inside the Cauldron.

It is affiliated with the Institute but survives through local trust and partial independence. Residents may trust a particular healer or prosthetist there while distrusting the Institute as a whole.

The House may use salvaged devices, household remedies, herbs, unlicensed methods, and practical knowledge rejected by the central Hall. Some of those practices work. Some carry their own risks.

### Brass Watch Medical Liaison

The Institute trains or seconds field medics for fires, collapses, canal disasters, industrial explosions, hazardous machinery incidents, aetheric exposure, temporal disorientation, and mass-casualty evacuation.

Field medics are often more trusted than central Institute officials because they work where people are injured rather than where research is conducted.

That trust is not universal. Some medics are Watch officers. Some share information with investigators. Some answer first to the Institute, the Council, or another organization.

### Expeditionary Medical Service

Accredited expeditions may include an Institute surgeon, medic, prosthetics specialist, or expedition-certified practitioner.

Expedition medics may carry broad emergency authority because delay can kill. The same isolation that makes decisive treatment necessary can also make oversight, consent, and later verification difficult.

An expeditionary practitioner may save a life through an improvised procedure that would never be approved in the city.

Another may collect samples, test a device, or recommend a permanent intervention because no one present has the authority or knowledge to challenge them.

The exact size, rules, and history of this service remain unresolved.
""",
    )

    text = replace_section(
        text,
        "Fields of Practice",
        """
The Institute's disciplines may include surgery, emergency medicine, field medicine, prosthetics, rehabilitation, mechanobiology, implant medicine, industrial medicine, aetheric trauma, environmental medicine, and the treatment of unusual biological-mechanical conditions.

Its capabilities should not be equated with a modern medical system.

Institute practitioners may possess advanced mechanical techniques while lacking reliable answers about:

- infection and contamination;
- internal disease;
- tissue rejection;
- nerve damage;
- anesthesia and pain;
- blood loss and replacement;
- long-term implant effects;
- psychological trauma;
- and interactions between Ancient components and living bodies.

Knowledge varies dramatically between practitioners and branches.

A brilliant prosthetist may be a poor diagnostician. A skilled field surgeon may distrust herbs that a Cauldron healer understands. An Academy researcher may know more about aetheric tissue response than how to help a patient live comfortably afterward.

Final period-appropriate professional titles remain unresolved. Physician, surgeon, medic, healer, prosthetist, chirurgeon, mechanobiologist, and vital mechanist may coexist.
""",
    )

    text = insert_section_before(
        text,
        "Public Reputation and Avoidance",
        """
The Institute is respected as a last resort rather than loved as a public service.

Citizens may delay seeking care because they fear:

- amputation;
- compulsory observation;
- experimental treatment;
- permanent implants;
- loss of privacy;
- debt or service obligations;
- being transferred to a restricted ward;
- having an unusual condition reported to the Council or Watch;
- or becoming more interesting to researchers than to caregivers.

Families often ask who is on duty before deciding whether to enter the Hall. Trust attaches to individual practitioners more readily than to the institution.

Some people die because they waited too long.

Others survive because they refused an Institute recommendation and sought a less invasive treatment elsewhere.

The risk runs in both directions.
""",
        "Relationship with the Mechanists' Guild",
    )

    text = insert_section_before(
        text,
        "Experiments and Institutional Abuse",
        """
Experiments have been performed under Institute authority.

Not every experiment was cruel, and some produced treatments that later saved lives. The institution nevertheless possesses a history of practices that may include:

- procedures performed without meaningful consent;
- experimental implants offered when no ordinary care was available;
- treatment made conditional on observation or research access;
- aggressive amputation and replacement;
- testing on people with limited civic standing;
- retention of tissue, devices, or records after recovery;
- recommendations shaped by patents, prestige, or institutional rivalry;
- and sealed wards where the distinction between patient and subject became deliberately unclear.

The exact scandals, dates, victims, and reforms remain unresolved.

These abuses do not make every practitioner malicious. They do mean that an Institute seal is not proof of moral authority.
""",
        "Relationship with the Mechanists' Guild",
    )

    text = insert_section_before(
        text,
        "Internal Factions and Outside Allegiances",
        """
The Institute is too large and politically valuable to remain ideologically neutral.

Individual practitioners, administrators, researchers, or record keepers may have loyalties to:

- [the Unwound](The_Unwound.md), especially those who oppose dependency on implants or the Heart Engine;
- [the Order of the Closed Eye](The_Order_of_the_Closed_Eye.md), especially those who classify anomalous patients and suppress dangerous knowledge;
- the Academy of Invention;
- the Mechanists' Guild;
- the High Council;
- the Brass Watch;
- Cauldron neighborhood compacts;
- merchant patrons;
- or private research circles.

No single outside organization is established as controlling the Institute.

Affiliations may create genuine reform, quiet protection, divided loyalties, corruption, information leaks, concealed treatment, or deliberate harm.

A physician's badge identifies training and access.

It does not reveal whom that physician ultimately serves.
""",
        "Relationship with the Mechanists' Guild",
    )

    text = replace_section(
        text,
        "Relationship with the Mechanists' Guild",
        """
The Institute and [the Mechanists' Guild](The_Mechanists_Guild.md) share responsibility wherever machinery becomes medically necessary.

Their cooperation has saved lives and accelerated the development of prosthetics, braces, implants, and adaptive tools.

It has also created a powerful bias toward mechanical solutions.

A damaged limb can become an engineering opportunity. A difficult recovery can look inefficient beside a certified replacement. A rare implant can become professional prestige for the surgeon, mechanist, institution, or patron who claims it.

Conflicts include:

- whether injured tissue should be preserved or replaced;
- whether a device is equipment or part of a person's body;
- who may inspect or alter an implant;
- whether a patient's refusal can block certification, research, or public-safety review;
- ownership of experimental designs;
- responsibility when an implant behaves unpredictably;
- and whether Ancient components can be understood through modern standards.

Patient autonomy is an important argument within this relationship.

It is not a universally enforced rule.
""",
    )

    text = replace_section(
        text,
        "Relationship with the Academy of Invention",
        """
The Institute and [the Academy of Invention](The_Academy_of_Invention.md) collaborate on anatomy, mechanobiology, adaptive technology, implants, and experimental procedures.

The Academy supplies theories, laboratories, instruments, and ambitious researchers.

The Institute supplies injuries, clinical access, treatment records, and living cases that theory alone cannot provide.

At their best, the institutions combine knowledge and practical care.

At their worst, a patient becomes the place where an academic hypothesis is tested.

The boundary between treatment and experiment is especially unstable when:

- no accepted treatment exists;
- the patient is dying;
- an Ancient component is involved;
- a child cannot fully participate in the decision;
- or institutional prestige depends on success.
""",
    )

    text = replace_section(
        text,
        "Relationship with the Brass Watch",
        """
The Institute supports [the Brass Watch](The_Brass_Watch.md) during disasters, dangerous investigations, and anomalous incidents.

Care, custody, and evidence can overlap.

An Institute medic may protect a patient's privacy, record details for the Watch, identify an implant as dangerous evidence, or recommend confinement in a restricted ward.

Different practitioners make different choices.

The Watch may genuinely need medical information to protect the city. It may also use medical authority to hold a person who has not committed a crime.

No automatic rule makes Institute staff independent from Watch or Council pressure.
""",
    )

    text = replace_section(
        text,
        "Relationship with the Society of Explorers",
        """
The Institute may certify expedition readiness, train field medics, review evacuation plans, and maintain records of unusual injuries encountered beyond Aetherhaven.

Explorers often view medical restrictions as obstacles imposed by people who have never entered the field.

Institute practitioners often view explorers as people who rename preventable risk as courage.

Both criticisms can be true.

Expeditionary medicine creates special danger because isolation gives a medic enormous authority, while sponsors may pressure that medic to keep an expedition moving, preserve a discovery, or collect samples before evacuation.

Whether an Institute practitioner accompanied the original Clockwork Jungle expedition remains unresolved.
""",
    )

    text = replace_section(
        text,
        "Relationship with the Cauldron",
        """
The Institute's presence in the Cauldron exists because industrial injury, chemical exposure, disability, poverty, and lack of civic documentation do not remove a person's need for care.

The central Institute is also one of the institutions Cauldron residents have reason to distrust.

The [Cauldron Recovery House](../locations/The_Cauldron_Recovery_House.md) may depend on local healers, herbal knowledge, neighborhood compacts, former Institute staff, salvaged equipment, and practitioners whose credentials are not recognized by the upper city.

Central administrators may call those methods unsafe.

Local residents may answer that the Hall's methods are merely dangerous in cleaner rooms.

The Recovery House is not automatically morally superior. Its protection comes from local accountability, and that protection can fail.
""",
    )

    text = insert_section_before(
        text,
        "Relationship with the Conservancy of Living Mechanisms",
        """
The Institute has no standing alliance with [the Conservancy of Living Mechanisms](The_Conservancy_of_Living_Mechanisms.md).

From time to time, individual practitioners or branches obtain:

- medicinal herbs;
- responsive mosses;
- resins;
- antifungal growths;
- living fibers;
- calming pollens;
- or other rare materials from the Clockwork Gardens.

The exchange is practical and often cautious.

Conservancy members may distrust an institution inclined to cut, replace, classify, and experiment. Institute practitioners may dismiss Conservancy remedies as unmeasured, inconsistent, or superstitious.

Neither side possesses complete knowledge.

A resource obtained from the Conservancy may save a patient whom Institute surgery could not. An invasive Institute procedure may save someone no herb can reach.

No regular partnership, shared governance, or ideological closeness should be assumed.
""",
        "Relationship with Elias and Amelia Hawthorne",
    )

    text = replace_section(
        text,
        "Relationship with Elias and Amelia Hawthorne",
        """
[Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) has engineering knowledge, field experience, and personal responsibility connected to Amelia's survival.

His emergency actions may have been essential. Trained medical intervention was also necessary.

The Institute may have contributed through an expedition medic, evacuation, surgery, infection control, pain management, rehabilitation, prosthetic fitting, implant monitoring, or collaboration while Elias built the mechanical framework of Amelia's arm.

It may also have recommended procedures Elias rejected.

Possible unresolved recommendations include:

- complete amputation at a higher point;
- a standardized prosthetic rather than Elias's custom design;
- removal or isolation of the Aether Heart;
- prolonged confinement for observation;
- experimental integration;
- or compulsory study because the Ancient component was considered a civic hazard.

None of these is yet established as the exact historical choice.

Elias may owe individual Institute practitioners Amelia's life while distrusting the institution that employed them.

[Amelia Hawthorne](../characters/Amelia_Hawthorne.md) may remember kindness, pain, frightening procedures, missing time, or adults debating her future while she could not meaningfully participate.

The Institute is not entitled to her trust merely because it helped keep her alive.
""",
    )

    text = replace_section(
        text,
        "Medical Ethics",
        """
There is no universal Hippocratic oath in the modern sense.

Different schools, wards, guild traditions, and practitioners follow different codes. Some promise to preserve life. Some prioritize function. Some serve the city. Some serve knowledge. Some place loyalty to a patron, institution, or cause above the wishes of a patient.

Common ethical arguments may include:

- whether survival justifies permanent alteration;
- whether emergency authority continues after the emergency;
- whether a child, prisoner, undocumented resident, injured worker, or unconscious explorer can meaningfully refuse;
- whether dangerous knowledge should be recorded or destroyed;
- whether a rare patient owes access to the people who saved them;
- and whether one person's risk is justified by a treatment that may later save many.

Individual practitioners can be principled, compassionate, and courageous.

Institutional ethics are inconsistent, contested, and vulnerable to pressure.

No reader or character should assume that an Institute recommendation is morally correct simply because it is medical.
""",
    )

    text = replace_section(
        text,
        "Political and Institutional Tensions",
        """
The Institute is a necessary civic power with weakly bounded authority.

It faces pressure from the High Council, Academy, Mechanists' Guild, Brass Watch, Society of Explorers, merchants, patrons, the Cauldron, the Unwound, and hidden interests connected to the Order of the Closed Eye.

Corruption may take several forms:

- payment for preferred access;
- research priorities shaped by patrons;
- sealed treatment records;
- altered causes of death;
- devices recommended because a workshop profits from them;
- patients transferred for political reasons;
- dangerous discoveries concealed;
- or practitioners using institutional access to serve another organization.

The Institute should not be portrayed as uniformly benevolent or uniformly evil.

It contains healers who take extraordinary risks for patients, researchers who justify cruelty as progress, exhausted field medics, brilliant prosthetists, frightened administrators, political operatives, reformers, and people who move between those categories over time.

Its necessity protects it from easy abolition.

Its necessity also makes its abuses harder to confront.
""",
    )

    text = replace_section(
        text,
        "Visual Language",
        """
The Institute's visual language should combine medicine, workshop engineering, and civic authority without resembling a modern hospital.

Possible elements include:

- brass, enamel, dark wood, glass, linen, leather straps, and stone;
- articulated braces and intimidating stabilization frames;
- anatomical diagrams beside mechanical cutaways;
- surgical instruments maintained like precision tools;
- herbal drawers beside chemical bottles;
- locked specimen cabinets;
- field cases scarred by expedition use;
- prosthetics displayed as both practical work and institutional achievement;
- public wards that are crowded and worn;
- and restricted rooms cleaner, quieter, and more frightening than the spaces outside them.

The Hall should feel capable rather than comforting.

Avoid modern visual shorthand such as perfect sterility, effortless diagnostics, disposable supplies, universal privacy, or uniformly gentle bedside care.
""",
    )

    text = replace_section(
        text,
        "Continuity Constraints",
        """
- The Institute exists as a distributed medical network rather than a separate map district.
- Its central institution is in the Government District.
- It maintains Academy, Great Workshops, Cauldron, Brass Watch, and expeditionary presences.
- It combines incomplete biological medicine with comparatively advanced mechanical intervention.
- It is necessary for catastrophic and unusual cases but is not assumed safe, trustworthy, or morally neutral.
- Ordinary citizens commonly prefer home remedies, apothecaries, midwives, neighborhood healers, or trusted local practitioners for ordinary ailments.
- Institute advice may be questioned, refused, or balanced against another form of care.
- No universal Hippocratic oath or consistently enforced consent code exists.
- Experiments and unethical treatments have occurred under Institute authority.
- Some practitioners may be connected to the Unwound, Order of the Closed Eye, Council, Watch, Academy, Guild, Cauldron factions, or private patrons.
- The Institute has no standing alliance with the Conservancy, though herbs and other resources may occasionally pass between individual practitioners.
- Mechanical replacement may be favored over slower biological treatment, including amputation and prosthetic replacement where another healer might attempt to preserve the limb.
- The Institute is less medically sophisticated than a modern health system; diagnosis, infection control, anesthesia, recovery, and long-term implant knowledge remain incomplete.
- Elias's actions were important to Amelia's survival, but trained medical care was also required.
- The Institute may have helped save Amelia while also frightening, studying, pressuring, or making contested recommendations about her.
- The exact final name, leadership, ranks, scandals, and Clockwork Jungle personnel remain unresolved.
""",
    )

    text = replace_section(
        text,
        "Open Canon Questions",
        """
1. Is **The Institute of Vital Mechanics** the final name?
2. Who leads it, and whom do they truly answer to?
3. Is it Council-chartered, professionally self-governing, privately patronized, or a mixture?
4. What competing medical schools or traditions exist inside it?
5. What codes do individual practitioners swear, if any?
6. Which services are public, charitable, fee-based, guild-funded, patron-funded, or debt-based?
7. What treatments do ordinary citizens most fear?
8. What historical experiment or scandal is publicly known?
9. What worse scandal remains sealed?
10. Which patients were treated as subjects without meaningful consent?
11. How common is amputation and mechanical replacement compared with preservation and herbal treatment?
12. Which Institute branch is considered most trustworthy?
13. Which is considered most dangerous?
14. Which members are connected to the Unwound?
15. Which members are connected to the Order of the Closed Eye?
16. What information is routinely shared with the Brass Watch or Council?
17. What exact relationship exists with the Cauldron Recovery House?
18. What resources are occasionally obtained from the Conservancy?
19. Was an Institute medic present during the Clockwork Jungle expedition?
20. Who stabilized Amelia first?
21. What procedures were performed during Amelia's survival and recovery?
22. What recommendations did Elias accept or refuse?
23. When did the Institute first encounter the Aether Heart?
24. Did anyone claim research, custody, or public-safety authority over Amelia?
25. Which recurring physician, medic, healer, prosthetist, or researcher eventually represents the Institute in the story?
""",
    )

    text = replace_section(
        text,
        "Development Checklist",
        """
- [x] Distributed institutional role established.
- [x] Government District, Academy, Workshops, Cauldron, Watch, Guild, and Society connections established.
- [x] Necessary-but-risky moral position established.
- [x] Public distrust and preference for ordinary home or local care established.
- [x] Limited medical sophistication and mechanical replacement bias established.
- [x] Experimental abuse and inconsistent ethics established.
- [x] Possible Unwound, Order, and other outside allegiances preserved.
- [x] Limited, non-allied Conservancy resource exchange established.
- [x] Medical support for Amelia's survival established as necessary but unresolved.
- [ ] Approve the final organization name.
- [ ] Define governance, leadership, schools, and practitioner ranks.
- [ ] Define at least one public scandal and one sealed scandal.
- [ ] Select a recurring compassionate practitioner and a recurring morally compromised practitioner when stories require them.
- [ ] Create the Institute seal and field-medical visual language.
- [ ] Resolve the exact Clockwork Jungle medical-response sequence only when the arc requires it.
""",
    )

    write(path, text)


def update_hall() -> None:
    path = "locations/The_Hall_of_Vital_Mechanics.md"
    text = read(path)

    text = replace_section(
        text,
        "Public Map Reference",
        """
A respected and feared civic hospital where Aetherhaven sends catastrophic injuries, failed prosthetics, dangerous infections, aetheric trauma, and patients whose conditions ordinary healers cannot treat.
""",
    )

    text = replace_section(
        text,
        "Canonical Summary",
        """
The Hall of Vital Mechanics is the central headquarters, principal hospital, teaching center, records authority, and research institution of [the Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md).

It is the best-equipped place in Aetherhaven for injuries that cross the boundaries between flesh, machinery, aether, and public safety.

It is not the place most citizens choose for ordinary care.

People enter because a limb cannot be saved at home, a fever has survived every trusted remedy, an implant is failing, a worker has been crushed, an expedition has returned with an impossible injury, or the Watch has ordered transport.

The Hall can save patients no one else can.

It can also expose them to intervention, observation, and institutional authority they would never willingly accept while healthy.
""",
    )

    text = insert_section_before(
        text,
        "Public Reputation",
        """
The Hall is commonly regarded as a place of last resort.

Families may delay entry while consulting an apothecary, midwife, household healer, workshop medic, or trusted elder. Some ask the name of the attending surgeon before allowing a patient through the doors.

Common fears include:

- unnecessary amputation;
- experimental treatment;
- confinement in a restricted ward;
- loss of privacy;
- debt;
- compulsory observation;
- and having an unusual condition reported to the Council, Watch, Academy, or Guild.

The Hall's reputation is not wholly fair.

It is also not wholly undeserved.
""",
        "Civic and Narrative Role",
    )

    text = replace_section(
        text,
        "Civic and Narrative Role",
        """
The Hall may contain emergency wards, surgical theatres, recovery rooms, prosthetics rooms, rehabilitation halls, anatomy classrooms, record vaults, field-medic training spaces, implant laboratories, specimen collections, and restricted facilities for aetheric or temporal injuries.

The distinction between ward, laboratory, and holding room is not always obvious to a patient.

Some departments are known for compassionate care.

Others are known for technical success purchased at severe personal cost.

Exact departments, practices, and rival schools remain unresolved.
""",
    )

    text = insert_section_before(
        text,
        "Restricted Wards and Experimentation",
        """
The Hall contains restricted wards where unusual injuries, Ancient implants, contagious conditions, failed integrations, and politically sensitive patients may be isolated.

Some isolation is medically necessary.

Some has been used to conceal experimentation, protect institutional reputation, preserve access to a rare case, or delay outside scrutiny.

Sealed records may document procedures performed under emergency authority that would not have been accepted under ordinary circumstances.

The Hall should never be assumed to be a neutral refuge merely because it is a hospital.
""",
        "Relationship with the Government District",
    )

    text = replace_section(
        text,
        "Relationship with the Government District",
        """
The Hall's Government District location gives it funding, emergency communication, legal privilege, and direct access to the High Council and Brass Watch.

It also makes political influence unavoidable.

Council officials may pressure the Hall to contain a patient, alter a record, prioritize a public figure, conceal an outbreak, or classify an unusual implant as a civic-security concern.

Some administrators resist.

Some cooperate.

Some are themselves connected to outside organizations.
""",
    )

    text = replace_section(
        text,
        "Relationship with Amelia Hawthorne",
        """
Amelia may have received surgery, stabilization, rehabilitation, fitting, monitoring, or experimental treatment through the Hall after the Clockwork Jungle disaster.

The exact sequence remains unresolved.

She may owe her survival to individual practitioners who worked there while still having valid reasons to fear the institution, distrust its records, or resent decisions made while she could not meaningfully participate.

The Hall may regard the Aether Heart as a medical danger, research opportunity, civic threat, or impossible implant.

None of those classifications grants it moral authority over Amelia.
""",
    )

    text = replace_section(
        text,
        "Visual Continuity",
        """
The Hall should feel capable, busy, old, and intimidating rather than modern, sterile, or uniformly comforting.

Potential visual elements include:

- tall windows and hard daylight;
- enamel, stone, dark wood, brass, glass, and linen;
- crowded public wards;
- articulated braces and stabilization frames;
- surgical instruments beside precision engineering tools;
- herbal drawers beside chemical cabinets;
- straps, lifts, pulleys, and mechanical tables designed for procedures;
- pneumatic message tubes;
- locked specimen and record rooms;
- worn floors from constant use;
- and restricted corridors that are quieter and cleaner than the public wards.

Avoid a gothic asylum caricature, but do not make the Hall reassuring by default.
""",
    )

    text = replace_section(
        text,
        "Continuity Constraints",
        """
- The Hall is an unnumbered point of interest within the Government District.
- It is the central institution of the Institute of Vital Mechanics.
- It is a last-resort hospital and research authority, not the ordinary first choice for common ailments.
- Citizens may fear unnecessary amputation, experimentation, confinement, debt, or institutional reporting.
- Public wards, training, administration, surgery, prosthetics, rehabilitation, records, and restricted research coexist.
- The Hall is medically capable but not equivalent to a modern hospital.
- Individual practitioners vary sharply in skill, ethics, loyalties, and preferred methods.
- The Hall may have participated in Amelia's recovery, but exact details remain unresolved.
- Past care does not make the Hall's later claims morally correct or trustworthy.
""",
    )

    text = replace_section(
        text,
        "Open Canon Questions",
        """
1. Is **The Hall of Vital Mechanics** the final name?
2. Where precisely does it stand within the Government District?
3. Which wards are publicly trusted?
4. Which wards are feared?
5. What rival medical schools operate inside it?
6. Who directs the Hall, and what outside loyalties do they hold?
7. What treatments are most commonly refused?
8. What experiment or scandal is hidden in its sealed records?
9. How are ordinary patients charged or indebted?
10. Which part of Amelia's care occurred here?
11. Was Amelia ever confined, observed, or treated experimentally?
12. Has the Hall surrendered patients or records to the Council, Watch, Order, or Academy?
13. Which recurring medical characters work here?
""",
    )

    write(path, text)


def update_recovery_house() -> None:
    path = "locations/The_Cauldron_Recovery_House.md"
    text = read(path)

    text = replace_section(
        text,
        "Canonical Summary",
        """
The Cauldron Recovery House provides rehabilitation, adaptive-device care, industrial-injury treatment, long-term recovery, prosthetics maintenance, and community medicine within the Cauldron.

It is affiliated with [the Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md), but it cannot function as a simple branch of Government District authority.

Residents often trust individual House practitioners more than the central Institute because those practitioners live with the consequences of their recommendations.

That does not make the House automatically safe or medically correct.

Its care may combine salvaged devices, household remedies, local herbs, rough surgery, unlicensed prosthetics, practical experience, and limited supplies. Some methods are more humane and effective than upper-city treatment. Others survive because no better option is available.
""",
    )

    text = replace_section(
        text,
        "Neutrality and Trust",
        """
The Recovery House claims customary neutrality, not guaranteed legal protection.

It is expected not to function as a Brass Watch observation post, Council registry, debt office, confiscation point, or pipeline sending unusual patients to upper-city researchers.

Those expectations have likely been tested and may have been violated in the past.

Trust is attached to people, neighborhood compacts, and repeated conduct rather than the Institute seal on the door.

A practitioner who shares a patient's name or accepts an outside payment may make the entire House unsafe until the community answers the breach.
""",
    )

    text = replace_section(
        text,
        "Services",
        """
Possible services include rehabilitation after industrial accidents, burn recovery, mobility training, prosthetics adjustment, pain management, adaptive-work retraining, community nursing, temporary shelter, and treatment using local herbs or household methods.

The House is more likely than the central Hall to attempt preservation before replacement when time and supplies permit.

It is also more likely to use an untested remedy because no certified treatment is affordable or accessible.

Patients may be transferred to the Hall for surgery or advanced intervention only after local options have failed—or when delay has made the situation worse.
""",
    )

    text = replace_section(
        text,
        "Relationship with the Institute of Vital Mechanics",
        """
The central Institute may provide supplies, specialist rotations, difficult surgery, training, prosthetic components, and emergency transport.

It may also demand records, impose licensing requirements, reject local methods, recruit unusual patients, or threaten to withdraw support.

The Recovery House may conceal information from the central Hall to protect residents.

It may also depend on that Hall when a patient needs care no Cauldron practitioner can provide.

Their relationship is one of dependency, resentment, cooperation, and recurring negotiation.
""",
    )

    text = replace_section(
        text,
        "Visual Continuity",
        """
The Recovery House should look repaired, practical, crowded, and protected by its community rather than polished or idealized.

Possible visual elements include:

- salvaged braces and mobility devices adapted to individual bodies;
- clean linens maintained despite soot and limited water;
- drying herbs beside mechanical tools;
- locked medicine cabinets;
- workshop-made ramps and lifts;
- shared kitchens and recovery courtyards;
- worn wood, patched tile, brass rails, and repurposed machinery;
- hand-painted warnings about privacy and Watch access;
- and visible evidence of both successful adaptation and failed treatment.

Avoid portraying it as morally pure merely because it opposes upper-city control.
""",
    )

    text = replace_section(
        text,
        "Continuity Constraints",
        """
- A rehabilitation and community-care facility exists in the Cauldron.
- It is affiliated with the Institute but depends on local trust and partial autonomy.
- It serves people neglected, priced out, undocumented, or endangered by ordinary civic systems.
- It is not a disguised Watch or Council outpost, though its neutrality may be breached.
- It may use herbs, household remedies, salvaged devices, unlicensed methods, and uncertified technology.
- Local methods are neither automatically superior nor automatically negligent.
- Individual trust matters more than institutional affiliation.
- Transfer to the central Hall may be necessary even when the Hall is feared.
- Exact leadership, legal status, scandals, and final name remain unresolved.
""",
    )

    text = replace_section(
        text,
        "Open Canon Questions",
        """
1. Is **The Cauldron Recovery House** the final name?
2. Who founded it?
3. Is it locally governed, Institute controlled, or jointly chartered?
4. What customary protection guards patient identity?
5. When was that protection last broken?
6. Which neighborhood compact protects the House?
7. What herbs or remedies are unavailable in the upper city?
8. Which local practices genuinely outperform Institute methods?
9. Which local practice has caused preventable harm?
10. How are supplies moved across the Ash Line?
11. Which services require transfer to the central Hall?
12. Does the Mechanists' Guild recognize devices maintained here?
13. Which recurring healer, therapist, prosthetist, or morally compromised practitioner works here?
""",
    )

    write(path, text)


def update_character_relationships() -> None:
    path = "characters/Amelia_Hawthorne.md"
    text = read(path)
    text = replace_section(
        text,
        "Relationship with the Institute of Vital Mechanics",
        """
[The Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md) may have participated in Amelia's emergency treatment, surgery, rehabilitation, prosthetic fitting, implant monitoring, or experimental care after the Clockwork Jungle disaster.

The exact clinicians and sequence remain unresolved.

Amelia may remember individual caregivers with gratitude while distrusting the institution that employed them. She may also remember pain, frightening apparatus, missing time, adults arguing over amputation or replacement, or recommendations she was too young and injured to understand.

The Institute's involvement does not make its later advice trustworthy by default.

Some practitioners may want to preserve the gauntlet. Others may recommend removing the Aether Heart, replacing Elias's design, confining Amelia for observation, or studying her as a unique interface.

Amelia's developing ability to question medical authority, seek another opinion, and participate in decisions about her own body should become part of her growth.
""",
    )
    write(path, text)

    path = "characters/Professor_Elias_Hawthorne.md"
    text = read(path)
    text = replace_section(
        text,
        "Relationship with the Institute of Vital Mechanics",
        """
Elias has a complicated relationship with [the Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md).

His field engineering and emergency actions may have been essential to keeping Amelia alive. They did not replace trained surgery, infection control, rehabilitation, or prosthetic care.

He may owe particular Institute practitioners an unpayable debt while distrusting the institution as a whole.

The Institute may have recommended interventions Elias accepted because Amelia would otherwise die. It may also have recommended amputation, standardized replacement, removal of the Aether Heart, prolonged observation, or experimental procedures he refused.

The exact choices remain unresolved.

Elias respects genuine expertise but does not accept an Institute title as proof of wisdom or morality. His guilt can make him too willing to accept dangerous recommendations—or too determined to oppose practitioners who may be correct.

The Institute is one of the institutions capable of challenging Elias's belief that he alone must decide Amelia's care, while also giving him valid reasons to fear surrendering control.
""",
    )
    write(path, text)


def update_historical_event() -> None:
    path = "historical_events/The_Clockwork_Jungle_Expedition.md"
    text = read(path)

    old = "The [Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md) may have supported the expedition, the recovery, Amelia's surgery, rehabilitation, prosthetic integration, or later monitoring.\n\nThe exact role remains unresolved.\n\nThe historical record must not imply that Elias single-handedly provided every form of medical care required to keep Amelia alive. His emergency engineering and stabilization may have been essential, while trained medical practitioners provided other critical care.\n\nWhether an Institute medic accompanied the expedition or became involved only after evacuation remains an open question."
    new = """The [Institute of Vital Mechanics](../organizations/The_Institute_of_Vital_Mechanics.md) may have supported the expedition, recovery, surgery, rehabilitation, prosthetic integration, experimental treatment, or later monitoring.

The exact role remains unresolved.

The historical record must not imply that Elias single-handedly provided every form of care required to keep Amelia alive. His emergency engineering and stabilization may have been essential, while trained practitioners provided other critical treatment.

It must also not assume that every Institute recommendation was safe, ethical, or accepted.

The recovery may have involved disputed decisions concerning amputation, replacement, observation, the Aether Heart, or experimental integration. Elias may have accepted some measures under desperate circumstances and refused others.

Whether an Institute medic accompanied the expedition or became involved only after evacuation remains open."""
    if old not in text:
        raise RuntimeError("Expected Institute historical-event section text not found")
    text = text.replace(old, new, 1)

    if "What procedures or experiments were performed during Amelia's recovery?" not in text:
        text = text.replace(
            "21. What exact medical personnel, field support, surgery, and rehabilitation kept Amelia alive?",
            "21. What exact medical personnel, field support, surgery, and rehabilitation kept Amelia alive?\n22. What procedures or experiments were performed during Amelia's recovery?\n23. Which Institute recommendations did Elias accept or refuse?",
            1,
        )

    write(path, text)


def update_connected_organizations() -> None:
    insert_or_append_relation(
        "organizations/The_Conservancy_of_Living_Mechanisms.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Conservancy has no standing alliance with [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md).

Individual Tenders may occasionally provide herbs, responsive mosses, resins, living fibers, calming pollens, antifungal growths, or other rare materials when a particular patient requires them.

The Conservancy distrusts an institution that may classify a living body as a failed mechanism and recommend cutting or replacement before understanding the relationship being damaged.

Institute practitioners may distrust Conservancy remedies because dosage, growth, and response can vary between specimens.

The exchange is practical, irregular, and often mediated through trusted individuals rather than formal offices.
""",
    )

    insert_or_append_relation(
        "organizations/The_Unwound.md",
        "Relationship with the Institute of Vital Mechanics",
        """
Some Institute practitioners may sympathize with or belong to [the Unwound](The_Unwound.md), particularly those who oppose dependence on permanent implants, the Heart Engine, or mechanized solutions imposed as medical necessity.

Other Unwound members may view the Institute as proof that Aetherhaven replaces living bodies rather than caring for them.

No formal organizational alliance is established. Individual affiliation may support reform, leak records, influence treatment, or create divided loyalty.
""",
    )

    insert_or_append_relation(
        "organizations/The_Order_of_the_Closed_Eye.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Order of the Closed Eye may maintain individual contacts within [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md).

Medical records, anomalous implants, altered memories, unidentified patients, and Ancient biological-mechanical interfaces would all be valuable to the Order's containment work.

Possible influence includes sealed wards, altered records, restricted diagnoses, concealed deaths, or treatment recommendations shaped by containment rather than recovery.

No institution-wide control is established.
""",
    )

    insert_or_append_relation(
        "organizations/The_Academy_of_Invention.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Academy collaborates with [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md) on mechanobiology, implants, adaptive devices, and experimental treatment.

The relationship produces real advances and creates access to vulnerable patients whose conditions can become academic opportunities.

Neither Academy review nor Institute approval guarantees that an experiment is safe, consensual, or morally justified.
""",
    )

    insert_or_append_relation(
        "organizations/The_Brass_Watch.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Brass Watch relies on [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md) for field medics, disaster response, aetheric trauma, and injuries involving implants or unusual mechanisms.

Institute personnel do not possess uniform independence from Watch authority. Some protect patients, some share records, and some treat containment as part of care.

The boundary between medical transport and custody should remain a recurring institutional tension.
""",
    )

    insert_or_append_relation(
        "organizations/The_Mechanists_Guild.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Guild collaborates with [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md) on prosthetics, braces, implants, and adaptive machinery.

This collaboration saves lives but can favor replacement over biological recovery. A damaged limb may be treated as an engineering problem before every medical or herbal option has been exhausted.

Guild certification does not guarantee that an intervention is the best choice for the patient.
""",
    )

    insert_or_append_relation(
        "organizations/The_Society_of_Explorers.md",
        "Relationship with the Institute of Vital Mechanics",
        """
The Society may rely on [the Institute of Vital Mechanics](The_Institute_of_Vital_Mechanics.md) for expedition medics, readiness review, medical equipment, and evacuation planning.

Field isolation gives expeditionary practitioners broad authority and weak oversight. A medic may save a life through necessary improvisation or perform a procedure that could not have been justified in the city.

Whether an Institute practitioner accompanied the Clockwork Jungle expedition remains unresolved.
""",
    )


def main() -> int:
    update_institute()
    update_hall()
    update_recovery_house()
    update_character_relationships()
    update_historical_event()
    update_connected_organizations()
    print("Refined Vital Mechanics as a necessary, limited, and morally risky institution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
