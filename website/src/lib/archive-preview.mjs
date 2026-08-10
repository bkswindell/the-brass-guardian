import {
  hiddenArchiveEntries,
  hiddenMapEntries,
  publicCharacterEntries,
  publicMapEntries,
  publicOrganizationEntries,
} from "./archive-catalog.mjs";

const featuredWorldEntranceEntries = [
  {
    id: "location-aetherhaven",
    slug: "aetherhaven",
    entityType: "location",
    canonicalName: "Aetherhaven",
    publicTitle: "Aetherhaven",
    publicSummary:
      "Aetherhaven is the City of Gears, Dreams and Discovery: a mountain city of brass streets, glass conservatories, canal bridges, workshops, crowded markets, and airship towers. Its people build, repair, teach, trade, argue, and explore among mechanisms older than the city’s best records. Some machines are understood. Others are maintained because they have always worked.",
    previewStatus: "proposal",
    spoilerClassification: "teaser",
    sourcePaths: ["locations/Aetherhaven.md"],
    image: {
      src: "/images/archive/map-of-aetherhaven-1539.webp",
      alt: "Illustrated map of Aetherhaven showing a circular brass-and-canal city with twenty-four numbered points of interest, six lettered restricted areas, airship routes, rail lines, bridges, waterways, and surrounding mountains.",
      width: 1539,
      height: 1152,
    },
    relatedEntryIds: [
      "location-clockwork-gardens",
      "location-gardens-airship-landing",
      "district-merchant",
      "district-inventors",
      "location-aerial-docks",
      "vessel-wayfinder",
    ],
    tags: ["city", "map", "public-cartography"],
  },
  {
    id: "location-clockwork-gardens",
    slug: "clockwork-gardens",
    entityType: "location",
    canonicalName: "The Clockwork Gardens",
    publicTitle: "The Clockwork Gardens",
    publicSummary:
      "The Clockwork Gardens form a living and mechanical ring near Aetherhaven’s center. Brass vines climb glasshouses, clockwork pollinators move among luminous flowers, and waterways pass beneath paths that do not always remain where gardeners left them. The Gardens are tended through care, observation, and cooperation—not command. Visitors may follow the public walks, but hidden paths reveal themselves on terms no mapmaker has mastered.",
    previewStatus: "proposal",
    spoilerClassification: "teaser",
    sourcePaths: ["locations/The_Clockwork_Gardens.md"],
    image: {
      src: "/images/archive/clockwork-gardens-at-night-767.webp",
      alt: "Night view of the Clockwork Gardens, with glass conservatories, brass walkways, luminous mechanical flowers, canals, clocks, and airships beneath a full moon.",
      width: 767,
      height: 1151,
    },
    mapMarker: "2",
    mapPosition: { x: 50, y: 51 },
    relatedEntryIds: [
      "location-aetherhaven",
      "location-gardens-airship-landing",
    ],
    tags: ["gardens", "living-mechanisms", "map-location"],
  },
  {
    id: "location-gardens-airship-landing",
    slug: "gardens-airship-landing",
    entityType: "location",
    canonicalName: "The Gardens Airship Landing",
    publicTitle: "The Gardens Airship Landing",
    publicSummary:
      "The Gardens Airship Landing is a quiet elevated platform for explorers, couriers, official visitors, and vessels needing urgent assistance. Brass walkways, flowering terraces, and luminous guide lamps overlook the Reflection Canals, while the Wayfinder rests at her familiar berth between expeditions. One polished berth remains reserved for a vessel called the Morningstar. No such ship appears in the current registry. The gardeners polish the nameplate anyway.",
    previewStatus: "proposal",
    spoilerClassification: "teaser",
    sourcePaths: ["locations/The_Gardens_Airship_Landing.md"],
    mapMarker: "8",
    mapPosition: { x: 28, y: 59 },
    relatedEntryIds: [
      "location-aetherhaven",
      "location-clockwork-gardens",
      "vessel-wayfinder",
    ],
    tags: ["airships", "clockwork-gardens", "map-location"],
  },
  {
    id: "district-merchant",
    slug: "merchant-district",
    entityType: "district",
    canonicalName: "The Merchant District",
    publicTitle: "The Merchant District",
    publicSummary:
      "The Merchant District is a busy quarter of exchanges, counting houses, shops, warehouses, guild offices, and markets serving citizens and visiting traders. Goods arrive by canal and airship, prices change with weather and rumor, and every street seems to specialize in something different. It is one of the easiest places to hear how large Aetherhaven really is: listen long enough, and nearly every district passes through its stalls.",
    previewStatus: "proposal",
    spoilerClassification: "public",
    sourcePaths: ["locations/The_Merchant_District.md"],
    mapMarker: "12",
    mapPosition: { x: 29.3, y: 29.2 },
    relatedEntryIds: ["location-aetherhaven"],
    tags: ["commerce", "markets", "map-location"],
  },
  {
    id: "district-inventors",
    slug: "inventors-district",
    entityType: "district",
    canonicalName: "The Inventors' District",
    publicTitle: "The Inventors’ District",
    publicSummary:
      "The Inventors’ District gathers workshops, laboratories, lecture rooms, prototype halls, and rented attics around the Academy of Invention. Students hurry between demonstrations, mechanists test ideas in narrow courtyards, and shop windows display devices whose purposes are not always immediately obvious. The district values curiosity, practical skill, and the courage to admit when an invention needs one more revision—preferably before it reaches the street.",
    previewStatus: "proposal",
    spoilerClassification: "public",
    sourcePaths: ["locations/The_Inventors_District.md"],
    mapMarker: "13",
    mapPosition: { x: 57, y: 23.4 },
    relatedEntryIds: ["location-aetherhaven"],
    tags: ["invention", "workshops", "map-location"],
  },
  {
    id: "location-aerial-docks",
    slug: "aerial-docks",
    entityType: "location",
    canonicalName: "The Aerial Docks",
    publicTitle: "The Aerial Docks",
    publicSummary:
      "The Aerial Docks are Aetherhaven’s great gateway to the skies. Mooring towers, cargo cranes, customs platforms, and immense dirigible hangars rise above a constant bustle of crews, merchants, couriers, and travelers. From the Mooring Crown, vessels depart for distant settlements and the Skyward Isles. At the far end of Hangar Row stands Dock Zero, a locked structure older than the port around it. On stormy nights, its lights sometimes wake to guide a ship no one can see.",
    previewStatus: "proposal",
    spoilerClassification: "teaser",
    sourcePaths: ["locations/The_Aerial_Docks.md"],
    mapMarker: "19",
    mapPosition: { x: 22, y: 24.2 },
    relatedEntryIds: ["location-aetherhaven"],
    tags: ["airships", "port", "map-location"],
  },
  {
    id: "vessel-wayfinder",
    slug: "wayfinder",
    entityType: "vessel",
    canonicalName: "The Wayfinder",
    publicTitle: "The Wayfinder",
    publicSummary:
      "The Wayfinder is Elias and Amelia Hawthorne’s exploration airship: part vessel, part workshop, and part home above the clouds. She is frequently moored at the Gardens Airship Landing, where expedition equipment, repairs, and questions collect between journeys. Her hull shows the care of many voyages, and her systems combine practical engineering with older mechanisms that do not surrender their secrets easily. The Hawthornes trust her not merely as a machine, but as a companion.",
    previewStatus: "proposal",
    spoilerClassification: "public",
    sourcePaths: [
      "artifacts/007_The_Wayfinder_Technical_Plate.md",
      "locations/The_Gardens_Airship_Landing.md",
    ],
    image: {
      src: "/images/archive/wayfinder-above-clouds-1024.webp",
      alt: "The Wayfinder, a brass explorer airship with a silver envelope, sailing above sunlit clouds and mountain peaks.",
      width: 1024,
      height: 1536,
    },
    relatedEntryIds: [
      "location-aetherhaven",
      "location-gardens-airship-landing",
    ],
    tags: ["airship", "exploration", "hawthorne"],
  },
];

const worldEntranceMapEntries = publicMapEntries.map((entry) => {
  const featured = featuredWorldEntranceEntries.find(
    (candidate) => candidate.mapMarker === entry.mapMarker,
  );

  return featured
    ? {
        ...entry,
        ...featured,
        archiveSection: "public",
        mapRegion: entry.mapRegion,
        mapLabel: entry.mapLabel,
      }
    : entry;
});

const worldEntranceEntries = [
  ...featuredWorldEntranceEntries.filter((entry) => !entry.mapMarker),
  ...worldEntranceMapEntries,
  ...publicCharacterEntries,
  ...publicOrganizationEntries,
];

const curatorRouteDefinition = [
  {
    id: "location-aetherhaven",
    label: "Orientation record",
    note: "Begin with the city as a whole before opening its individual cabinets.",
  },
  {
    id: "map-room",
    kind: "room",
    title: "The Map Room",
    href: "/archive/map/",
    label: "Cartographic table",
    note: "Set the records beside their numbered places, then choose whether to follow or wander.",
  },
  {
    id: "location-clockwork-gardens",
    label: "Living systems",
    note: "Enter by the public walks, where mechanisms grow as often as they are built.",
  },
  {
    id: "location-gardens-airship-landing",
    label: "Threshold record",
    note: "Move from the Gardens to the landing where journeys begin and return.",
  },
  {
    id: "vessel-wayfinder",
    label: "Explorer vessel",
    note: "Meet the airship that carries the Hawthornes beyond Aetherhaven and home again.",
  },
  {
    id: "location-aerial-docks",
    label: "Civic gateway",
    note: "Compare one familiar berth with the city’s vast and crowded aerial port.",
  },
  {
    id: "district-merchant",
    label: "City life",
    note: "Follow the goods, arguments, and rumors that move between every quarter.",
  },
  {
    id: "district-inventors",
    label: "Working knowledge",
    note: "Finish among the workshops where Aetherhaven tests what it may become next.",
  },
];

const entryHref = (entry) =>
  `/archive/${entry.entityType}/${entry.slug}/`;

const worldEntranceCuratorRoute = curatorRouteDefinition.map((step) => {
  if (step.kind === "room") return step;

  const entry = worldEntranceEntries.find((candidate) => candidate.id === step.id);
  if (!entry) throw new Error(`Unknown curator route entry: ${step.id}`);

  return {
    ...step,
    kind: "record",
    title: entry.publicTitle,
    href: entryHref(entry),
    entityType: entry.entityType,
  };
});

export const isArchivePreviewEnabled = (env = process.env) => {
  if (env.VERCEL_ENV === "production") return false;
  return env.PUBLICATION_PREVIEW === "1" || env.VERCEL_ENV === "preview";
};

export const getWorldEntrancePreview = (env = process.env) => {
  const enabled = isArchivePreviewEnabled(env);
  return {
    enabled,
    entries: enabled ? worldEntranceEntries : [],
    mapEntries: enabled ? worldEntranceMapEntries : [],
    hiddenEntries: enabled ? hiddenArchiveEntries : [],
    hiddenMapEntries: enabled ? hiddenMapEntries : [],
    curatorRoute: enabled ? worldEntranceCuratorRoute : [],
  };
};
