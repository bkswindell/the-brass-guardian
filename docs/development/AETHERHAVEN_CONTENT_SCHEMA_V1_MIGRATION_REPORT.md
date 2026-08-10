# Aetherhaven Content Schema Version 1 — Migration Report

**Migration date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`  
**Branch:** `migration/content-schema-v1`

## Summary

- Schema-governed records discovered: **210**
- Legacy records migrated: **209**
- First-class records created: **1**
- Existing Version 1 records encountered: **0**
- Current C1 public projections copied into owning Markdown: **95**
- Unresolved relationship-like legacy values preserved in prose: **96**
- Other legacy fields preserved in prose: **75**
- Missing/invalid legacy asset references skipped: **0**

The migration rewrote front matter only, except when a legacy structured value could not be converted safely. Such values were appended verbatim under `Schema Migration Preservation Notes` in the owning Markdown record rather than being discarded or interpreted.

## Public Projection Preservation

The exact current C1 `publicTitle`, `publicSummary`, classification, access label, tags, related-record set, slug, and selected image context were copied from the approved Version 1 website manifest into each owning canonical record as `public_projection`. Publication approval remains in the existing website manifest until the later Version 2 ledger cutover.

## Created First-Class Records

- `vessels/The_Wayfinder.md`

## Slug Adjustments for Non-Public Records

- `story_arcs/The_Disappearance_of_Prototype_I.md`: `the-disappearance-of-prototype-i` → `the-disappearance-of-prototype-i-story-arc`

## Preserved Unresolved Legacy Relationship Values

- `characters/Amelia_Hawthorne.md` — `affiliations`: `Hawthorne exploration household and crew`
- `characters/Amelia_Hawthorne.md` — `key_connections`: `The Aether Gauntlet`
- `characters/Amelia_Hawthorne.md` — `key_connections`: `The Aether Heart`
- `characters/Amelia_Hawthorne.md` — `key_connections`: `The Six Aether Keys`
- `characters/Captain_Mara_Voss.md` — `affiliations`: `Harbormaster's Office`
- `characters/Captain_Mara_Voss.md` — `affiliations`: `Former captain of the Resolute`
- `characters/Chief_Inspector_Beatrice_Thorne.md` — `primary_locations`: `Brass Watch Headquarters`
- `characters/Chief_Inspector_Beatrice_Thorne.md` — `primary_locations`: `Active investigation sites throughout Aetherhaven`
- `characters/Chief_Inspector_Beatrice_Thorne.md` — `affiliations`: `High Council civic authority, with increasing independence`
- `characters/Master_Gideon_Brasswell.md` — `key_connections`: `Master Gideon's guild medallion`
- `characters/Orin_Flint.md` — `affiliations`: `Gearbreaker mining crews`
- `characters/Pip.md` — `primary_locations`: `The Hawthorne workshop`
- `characters/Professor_Elias_Hawthorne.md` — `affiliations`: `Academy of Invention, current status unresolved`
- `characters/Professor_Elias_Hawthorne.md` — `affiliations`: `Mechanists' Guild tradition through Gideon Brasswell`
- `characters/Professor_Elias_Hawthorne.md` — `key_connections`: `The Aether Gauntlet`
- `characters/Professor_Elias_Hawthorne.md` — `key_connections`: `The Aether Heart`
- `characters/Professor_Elias_Hawthorne.md` — `key_connections`: `The Six Aether Keys`
- `characters/Silas_Rook_The_Stillmaker.md` — `primary_locations`: `Unknown`
- `characters/Silas_Rook_The_Stillmaker.md` — `primary_locations`: `Temporal dead drops throughout Aetherhaven`
- `characters/Silas_Rook_The_Stillmaker.md` — `primary_locations`: `Abandoned chronometric stations`
- `characters/Silas_Rook_The_Stillmaker.md` — `primary_locations`: `Possible access to the Shrouded Vaults`
- `characters/Silas_Rook_The_Stillmaker.md` — `key_connections`: `The Resolute`
- `characters/Tamsin_Pike.md` — `primary_locations`: `Old City passages`
- `characters/Tamsin_Pike.md` — `primary_locations`: `Underclock routes`
- `characters/The_Passenger_of_Dock_Zero.md` — `primary_locations`: `The reserved Morningstar berth at the Gardens' Airship Landing`
- `characters/The_Passenger_of_Dock_Zero.md` — `affiliations`: `None verified`
- `characters/The_Passenger_of_Dock_Zero.md` — `affiliations`: `Possible connection to an unregistered airship line`
- `characters/The_Passenger_of_Dock_Zero.md` — `affiliations`: `Possible connection to the Morningstar`
- `characters/The_Passenger_of_Dock_Zero.md` — `key_connections`: `The Morningstar Company`
- `locations/The_Aerial_Docks.md` — `primary_connections`: `The Morningstar`
- `locations/The_Aerial_Docks.md` — `primary_connections`: `The Resolute`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `The Mooring Crown`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `Harbormaster's Tower`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `The Customs Concourse`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `The Cargo Exchange`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `Hangar Row`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `The Storm Lantern Array`
- `locations/The_Aerial_Docks.md` — `points_of_interest`: `The Navigator's Gallery`
- `locations/The_Cauldron_Recovery_House.md` — `primary_connections`: `Neighborhood Compacts`
- `locations/The_Gardens_Airship_Landing.md` — `points_of_interest`: `The Landing Terrace`
- `locations/The_Gardens_Airship_Landing.md` — `points_of_interest`: `The Emergency Repair Cradle`
- `locations/The_Gardens_Airship_Landing.md` — `points_of_interest`: `The Courier House`
- `locations/The_Gardens_Airship_Landing.md` — `points_of_interest`: `The Windglass Pavilion`
- `locations/The_Gardens_Airship_Landing.md` — `points_of_interest`: `The Garden Signal Mast`
- `locations/The_Great_Workshops.md` — `points_of_interest`: `Order prosthetics and implant annex, final name unresolved`
- `locations/The_Hall_of_Vital_Mechanics.md` — `primary_connections`: `The Academy of Invention`
- `organizations/The_Aerial_Mariners_Union.md` — `leadership`: `Elected Union Speaker, identity not yet established`
- `organizations/The_Aerial_Mariners_Union.md` — `leadership`: `Route Council`
- `organizations/The_Aetherhaven_Archives.md` — `key_relationships`: `The Academy of Invention`
- `organizations/The_Brass_Watch.md` — `headquarters`: `Brass Watch Headquarters, Government District`
- `organizations/The_Brass_Watch.md` — `key_relationships`: `Captain Mara Voss and the Harbormaster's Office`
- `organizations/The_Conservancy_of_Living_Mechanisms.md` — `leadership`: `The Circle of Seasons`
- `organizations/The_Eight_Founding_Engineering_Guilds.md` — `key_relationships`: `The Academy of Invention`
- `organizations/The_High_Council_of_Aetherhaven.md` — `key_relationships`: `The Academy of Invention`
- `organizations/The_Mechanists_Guild.md` — `key_relationships`: `The Academy of Invention`
- `organizations/The_Ninth_Guild.md` — `key_relationships`: `The Academy of Invention`
- `organizations/The_Underclock.md` — `leadership`: `No confirmed central leader`
- `artifacts/001_The_Hawthorne_Explorers_Crest.md` — `related_markdown`: `../README.md`
- `artifacts/006_Canonical_Aetherhaven_Archive_Label.md` — `related_markdown`: `../PROJECT_INDEX.md`
- `artifacts/008_Professor_Hawthornes_Field_Journal.md` — `related_markdown`: `../README.md`
- `artifacts/014_Amelias_Explorer_Journal_First_Mechanical_Sketches.md` — `related_markdown`: `../README.md`
- `artifacts/051_The_Obsidian_Covenant_Insignia.md` — `related_markdown`: `../PROJECT_INDEX.md`
- `artifacts/052_The_Quiet_Choir_Vibration_Transcript.md` — `related_markdown`: `../PROJECT_INDEX.md`
- `historical_events/The_Ash_Compact.md` — `order_interest`: `unresolved`
- `historical_events/The_Clockwork_Jungle_Expedition.md` — `participants`: `additional expedition members unresolved`
- `historical_events/The_Clockwork_Jungle_Expedition.md` — `organizations`: `Academy of Invention, possible research connection`
- `historical_events/The_Clockwork_Jungle_Expedition.md` — `related_artifacts`: `{"The Aether Gauntlet"=>"Exterior Study"}`
- `historical_events/The_Clockwork_Jungle_Expedition.md` — `related_artifacts`: `The Aether Heart`
- `historical_events/The_Clockwork_Jungle_Expedition.md` — `order_interest`: `possible but unconfirmed`
- `historical_events/The_Closing_of_Dock_Zero.md` — `order_interest`: `unresolved`
- `historical_events/The_Disappearance_of_Prototype_I.md` — `order_interest`: `unresolved`
- `historical_events/The_First_Continuance.md` — `order_interest`: `unresolved`
- `historical_events/The_First_Dream_Bloom.md` — `order_interest`: `unresolved`
- `historical_events/The_Founding_of_the_Conservancy.md` — `order_interest`: `unresolved`
- `historical_events/The_Founding_of_the_Eight_Guilds.md` — `order_interest`: `unresolved`
- `historical_events/The_Gearbreaker_Standoff.md` — `participants`: `unnamed young Brass Watch constable`
- `historical_events/The_Gearbreaker_Standoff.md` — `participants`: `Gearbreaker mining crews`
- `historical_events/The_Gearbreaker_Standoff.md` — `order_interest`: `no confirmed direct involvement`
- `historical_events/The_Great_Garden_Rearrangement.md` — `order_interest`: `unresolved`
- `historical_events/The_Last_Morningstar_Manifest.md` — `order_interest`: `unresolved`
- `historical_events/The_Night_of_Silent_Clocks.md` — `order_interest`: `unresolved`
- `historical_events/The_Opening_of_the_Aerial_Docks.md` — `order_interest`: `unresolved`
- `historical_events/The_Resolute_Incident.md` — `order_interest`: `unresolved`
- `historical_events/The_Revision_of_the_Society_of_Explorers_Charter.md` — `order_interest`: `unresolved`
- `historical_events/The_Rising.md` — `order_interest`: `unresolved`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md` — `primary_locations`: `The skies above Aetherhaven`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md` — `primary_connections`: `Wayfinder technical and domestic canon`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md` — `primary_connections`: `Amelia and Elias relationship`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md` — `primary_characters`: `Pip or a closely related brass sparrow messenger, exact identity unresolved`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md` — `primary_connections`: `The Keeper of Dreams arc`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md` — `primary_connections`: `The Dream Engine`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md` — `primary_connections`: `The silver dream flower`
- `story_arcs/The_Keeper_of_Dreams.md` — `primary_artifacts`: `Silver dream flower`
- `story_arcs/The_Keeper_of_Dreams.md` — `primary_artifacts`: `Dream Engine`
- `story_arcs/The_Keeper_of_Dreams.md` — `primary_artifacts`: `Brass sparrow with blue ribbon`
- `story_arcs/The_Watchmans_Regret.md` — `primary_characters`: `unnamed veteran Brass Watch officer`

## Other Preserved Legacy Fields

- `characters/Chancellor_Octavia_Vale.md` — `primary_location`: `["Government District"]`
- `characters/Chancellor_Octavia_Vale.md` — `public_office`: `["Chancellor of the High Council"]`
- `characters/Chancellor_Octavia_Vale.md` — `key_relationships`: `["The High Council of Aetherhaven","The Order of the Closed Eye","Chief Inspector Beatrice Thorne","Professor Elias Hawthorne","Amelia Hawthorne","Captain Mara Voss"]`
- `characters/Juniper_Bell.md` — `formal_title`: `["Keeper of the Clockwork Gardens"]`
- `characters/Juniper_Bell.md` — `possible_hidden_title`: `["Keeper of Dreams"]`
- `characters/Juniper_Bell.md` — `public_affiliation`: `["The Conservancy of Living Mechanisms"]`
- `characters/Juniper_Bell.md` — `organizational_position`: `["Public Keeper and Garden intermediary","Not the First Tender"]`
- `characters/Juniper_Bell.md` — `apparent_age`: `["Unchanged adult age across known records"]`
- `characters/Juniper_Bell.md` — `key_relationships`: `["Amelia Hawthorne","Professor Elias Hawthorne","The Conservancy of Living Mechanisms","The Guild of Verdant Mechanists","Chancellor Octavia Vale","Chief Inspector Beatrice Thorne","The Order of the Closed Eye","The Ninth Guild"]`
- `characters/Juniper_Bell.md` — `signature_objects`: `["Green many-pocketed coat","Mechanical insects","Personal Introduction Bell","Silver dream flower"]`
- `characters/Pip.md` — `affiliation`: `["Amelia Hawthorne"]`
- `characters/Pip.md` — `possible_connection`: `["Juniper Bell","The Keeper of Dreams","The Moon Garden"]`
- `characters/Tamsin_Pike.md` — `key_relationships`: `["Amelia Hawthorne","Professor Elias Hawthorne","The Underclock","Captain Mara Voss"]`
- `characters/Tamsin_Pike.md` — `signature_artifact`: `["Tamsin Pike's brass key"]`
- `characters/The_Hidden_Architect_Unassigned.md` — `true_identity`: `Deliberately undefined`
- `characters/The_Hidden_Architect_Unassigned.md` — `known_to`: `["Silas Rook"]`
- `characters/The_Hidden_Architect_Unassigned.md` — `unknown_to`: `["Amelia Hawthorne","Professor Elias Hawthorne","Captain Mara Voss","Chief Inspector Beatrice Thorne","The Brass Watch","The broader Unwound","Nearly all Severed Coil cells"]`
- `characters/The_Passenger_of_Dock_Zero.md` — `identity_status`: `Unknown`
- `locations/The_Moon_Garden.md` — `public_access`: `["Not officially acknowledged"]`
- `locations/The_Moon_Garden.md` — `actual_access`: `["Invitation or recognition by the Gardens"]`
- `locations/The_Moon_Garden.md` — `primary_guardian`: `["Juniper Bell"]`
- `locations/The_Moon_Garden.md` — `primary_mechanism`: `["The Dream Engine"]`
- `locations/The_Moon_Garden.md` — `key_connections`: `["Amelia Hawthorne","Pip","The Keeper of Dreams","The Conservancy of Living Mechanisms"]`
- `organizations/The_Academy_of_Invention.md` — `known_leadership`: `["Doctor Elara Quill"]`
- `organizations/The_Academy_of_Invention.md` — `primary_connections`: `["The Order of the Mended Hand","Doctor Elara Quill"]`
- `organizations/The_Conservancy_of_Living_Mechanisms.md` — `oldest_rule`: `["Never allow the Gardens to recognize you as an intruder."]`
- `organizations/The_Eight_Founding_Engineering_Guilds.md` — `governing_body`: `["The Conclave of Eight"]`
- `organizations/The_Eight_Founding_Engineering_Guilds.md` — `meeting_place`: `["The Octagonal Hall"]`
- `organizations/The_Eight_Founding_Engineering_Guilds.md` — `modern_federation`: `["The Mechanists' Guild"]`
- `organizations/The_Eight_Founding_Engineering_Guilds.md` — `member_guilds`: `["The Guild of Framewrights","The Guild of Enginewrights","The Guild of Aetherwrights","The Guild of Canalwrights","The Guild of Skywrights","The Guild of Clockwrights","The Guild of Artificers","The Guild of Verdant Mechanists"]`
- `organizations/The_High_Council_of_Aetherhaven.md` — `seat`: `["The High Chamber, Government District"]`
- `organizations/The_High_Council_of_Aetherhaven.md` — `presiding_officer`: `["Chancellor Octavia Vale"]`
- `organizations/The_High_Council_of_Aetherhaven.md` — `active_seats`: `["Eight Founding Guild Seats","Four Civic Quarter Seats"]`
- `organizations/The_High_Council_of_Aetherhaven.md` — `sealed_seat`: `["The Thirteenth Chair of the First Mechanist"]`
- `organizations/The_High_Council_of_Aetherhaven.md` — `founding_principle`: `["The Heart Engine must continue operating."]`
- `organizations/The_Lamplighters_Fellowship.md` — `principal_artifact`: `["The Homecoming Flame"]`
- `organizations/The_Lamplighters_Fellowship.md` — `traditional_greeting`: `["Keep a light for those still coming home."]`
- `organizations/The_Lamplighters_Fellowship.md` — `primary_duties`: `["Streetlamps","Bridge lights","Canal lights","Public stair and tunnel lamps","Aerial beacons","Emergency route lighting"]`
- `organizations/The_Mechanists_Guild.md` — `governing_body`: `["The Conclave of Eight"]`
- `organizations/The_Mechanists_Guild.md` — `member_orders`: `["The Guild of Framewrights","The Guild of Enginewrights","The Guild of Aetherwrights","The Guild of Canalwrights","The Guild of Skywrights","The Guild of Clockwrights","The Guild of Artificers","The Guild of Verdant Mechanists"]`
- `organizations/The_Ninth_Guild.md` — `primary_locations`: `["Temporary Ninth Rooms throughout Aetherhaven","The Cauldron","Hidden institutional spaces"]`
- `organizations/The_Ninth_Guild.md` — `leader_title`: `["The Curator"]`
- `organizations/The_Ninth_Guild.md` — `leader_identity`: `Unknown`
- `organizations/The_Order_of_the_Closed_Eye.md` — `public_status`: `Officially unacknowledged`
- `organizations/The_Order_of_the_Closed_Eye.md` — `hidden_leadership`: `["The Closed Council"]`
- `organizations/The_Order_of_the_Closed_Eye.md` — `institutional_reach`: `["The High Council","The Academy of Invention","The Society of Explorers","The Mechanists' Guild","The Civic Archives","Selected Brass Watch offices","The Clockwrights"]`
- `organizations/The_Order_of_the_Mended_Hand.md` — `primary_connections`: `["The Government District","The Academy of Invention","The Great Workshops","The Cauldron","The Brass Watch","The Mechanists' Guild","The Society of Explorers","Professor Elias Hawthorne","Amelia Hawthorne","The Clockwork Jungle Expedition","The Unwound","The Order of the Closed Eye","The Conservancy of Living Mechanisms, occasional resource exchange only"]`
- `organizations/The_Severed_Coil.md` — `operational_status`: `Active, deeply underground`
- `organizations/The_Severed_Coil.md` — `known_locations`: `["Hidden cells beneath the Industrial District","The Cauldron","Abandoned Golden Vein access tunnels","Unregistered workshops","Unknown safehouses throughout Aetherhaven"]`
- `organizations/The_Severed_Coil.md` — `parent_movement`: `["The Unwound"]`
- `organizations/The_Severed_Coil.md` — `public_enemy`: `["The Brass Watch"]`
- `organizations/The_Severed_Coil.md` — `suspected_connections`: `["The Ninth Guild","The Underclock, disputed and unconfirmed","Corrupt Council intermediaries, unconfirmed"]`
- `organizations/The_Severed_Coil.md` — `key_connections`: `["Chief Inspector Beatrice Thorne","Captain Mara Voss","Professor Elias Hawthorne","Amelia Hawthorne"]`
- `organizations/The_Society_of_Explorers.md` — `primary_connections`: `["The Order of the Mended Hand","Professor Elias Hawthorne"]`
- `organizations/The_Underclock.md` — `primary_locations`: `["Canal District service tunnels","Old City passages","The Cauldron","Thirteenth Canal routes","Forgotten maintenance corridors"]`
- `organizations/The_Unwound.md` — `primary_locations`: `["Workers' Dormitories","Old City","Canal District","The Cauldron","Great Workshops"]`
- `organizations/The_Unwound.md` — `public_affiliations`: `["Independent craft cooperatives","Worker mutual-aid halls","Manual infrastructure societies"]`
- `organizations/The_Unwound.md` — `suspected_affiliations`: `["The Underclock","Dissident Mechanists' Guild members","Former Academy scholars"]`
- `organizations/The_Unwound.md` — `hostile_splinter`: `["The Severed Coil"]`
- `story_arcs/The_Black_Catalogue_Arc.md` — `primary_antagonist`: `["The Ninth Guild","The Curator"]`
- `story_arcs/The_Black_Catalogue_Arc.md` — `supporting_factions`: `["The Brass Watch","The Mechanists' Guild","The Academy of Invention","The Unwound"]`
- `story_arcs/The_Black_Catalogue_Arc.md` — `primary_mysteries`: `["The Black Catalogue","Prototype I","The missing ninth discipline"]`
- `story_arcs/The_Disappearance_of_Prototype_I.md` — `primary_factions`: `["The Order of the Closed Eye","The Ninth Guild","The Underclock","The Academy of Invention"]`
- `story_arcs/The_Disappearance_of_Prototype_I.md` — `primary_mystery`: `["Prototype I"]`
- `story_arcs/The_Return_to_the_Clockwork_Jungle.md` — `related_historical_events`: `["The Clockwork Jungle Expedition"]`
- `story_arcs/The_Return_to_the_Clockwork_Jungle.md` — `related_artifacts`: `["Professor Hawthorne's Field Journal",{"The Aether Gauntlet":"Exterior Study"},"future expedition records"]`
- `story_arcs/The_Return_to_the_Clockwork_Jungle.md` — `central_themes`: `["memory and evidence","parental guilt and agency","returning to the site of trauma","inherited stories versus lived truth","recognition without ownership"]`
- `story_arcs/The_Severed_Coil_Conflict.md` — `primary_antagonist`: `["The Severed Coil"]`
- `story_arcs/The_Severed_Coil_Conflict.md` — `supporting_factions`: `["The Brass Watch","The Unwound","Harbormaster's Office","Engine Complex"]`
- `story_arcs/The_Thirteenth_Chair.md` — `primary_institutions`: `["The High Council of Aetherhaven","The Order of the Closed Eye","The Mechanists' Guild"]`
- `story_arcs/The_Thirteenth_Chair.md` — `primary_figures`: `["Chancellor Octavia Vale","Amelia Hawthorne","Professor Elias Hawthorne","Chief Inspector Beatrice Thorne"]`
- `story_arcs/The_Thirteenth_Chair.md` — `primary_mysteries`: `["The First Mechanist","The sealed Thirteenth Chair","The Doctrine of Continuance"]`
- `story_arcs/The_Watchmans_Regret.md` — `supporting_characters`: `["Chief Inspector Beatrice Thorne","Professor Elias Hawthorne"]`
- `story_arcs/The_Watchmans_Regret.md` — `related_historical_events`: `["The Gearbreaker Standoff"]`
- `story_arcs/The_Watchmans_Regret.md` — `central_themes`: `["certainty versus understanding","good people on opposing sides","responsibility and authority","mentorship after failure"]`

## Skipped Legacy Asset References

- None.

## Scope Fallbacks

The following active canonical records lacked an explicit legacy canonical scope and were assigned the repository-wide Aetherhaven scope `aetherhaven-volumes` without changing story content:
- `artifacts/001_The_Hawthorne_Explorers_Crest.md`
- `artifacts/003_The_Six_Key_Sigil.md`
- `artifacts/004_The_First_Mechanists_Mark.md`
- `artifacts/007_The_Wayfinder_Technical_Plate.md`
- `artifacts/009_The_Aether_Gauntlet_Exterior_Study.md`
- `artifacts/011_Prototype_II_Cabinet_Photograph.md`
- `artifacts/012_The_Missing_Prototype_I_Catalog_Card.md`
- `artifacts/015_Botanical_Plate_of_the_Dream_Blossom.md`
- `artifacts/017_The_Grand_Atrium_Architectural_Lithograph.md`
- `artifacts/018_The_Changing_Paths_of_the_Gardens.md`
- `artifacts/021_Tamsin_Pikes_Brass_Key.md`
- `artifacts/025_The_Passengers_Future_Dated_Ticket.md`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md`
- `story_drafts/The_Brass_Guardian_and_the_Clockwork_Princess.md`

## Validation State

- Ruby migration checks require unique IDs/slugs, resolved relationship targets, safe public relationships, and existing active asset files.
- The workflow exports every migrated metadata object and runs the repository’s locked JavaScript `validateCanonRecords()` implementation over the complete set.
- Website publication/Preview parity is **not** cut over in this migration; the existing C1 website data sources remain active until the later source-of-truth realignment passes the explicit C1 parity gate.

