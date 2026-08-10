import { defineCollection } from "astro:content";

import { canonFrontmatterLoader } from "./loaders/canon-frontmatter-loader";

const repositoryRoot = new URL("../../", import.meta.url);

const canon = defineCollection({
  loader: canonFrontmatterLoader(repositoryRoot),
});

export const collections = { canon };
