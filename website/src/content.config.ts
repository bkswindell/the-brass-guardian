import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";

const repositoryRoot = new URL("../../", import.meta.url);

const canon = defineCollection({
  loader: glob({
    base: repositoryRoot,
    pattern: [
      "characters/!(README).md",
      "locations/!(README).md",
      "organizations/!(README).md",
      "artifacts/!(README).md",
      "vessels/!(README).md",
      "historical_events/!(README).md",
      "story_drafts/!(README).md",
      "story_arcs/!(README).md",
    ],
    generateId: ({ data }) => {
      if (typeof data?.id !== "string" || data.id.length === 0) {
        throw new Error("Canonical Markdown entry is missing its Schema v1 stable id.");
      }
      return data.id;
    },
    retainBody: false,
  }),
});

export const collections = { canon };
