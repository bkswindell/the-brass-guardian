# The Brass Guardian Website

This directory contains the Astro site for **The Brass Guardian**.

It currently renders a public-safe Coming Soon page with Vercel Web Analytics, Speed Insights, responsive derivatives of the approved cover artwork, and an accessible cover reader. It does not yet publish stories, character profiles, or internal canon files.

## Local Verification

From the `website/` directory:

```bash
npm install
npm run dev
```

To verify the production build:

```bash
npm run build
npm run preview
```

Run the complete publication, test, build, metadata, and static-route acceptance checks with:

```bash
npm run verify
```

The verification command runs the publication-boundary contract tests, validates the explicit public manifest, builds the site, and checks the generated metadata, favicon links, social image, web manifest, and custom 404 route.

## World Entrance branch preview

The World Entrance work keeps proposal content outside the approved public manifest. Proposal routes are enabled only for an explicit local preview or a Vercel branch Preview:

```bash
PUBLICATION_PREVIEW=1 npm run dev -- --host 0.0.0.0
npm run verify:archive-preview
```

Vercel sets `VERCEL_ENV=preview` automatically for branch deployments. Production builds do not load the proposal records. The dedicated preview branch may be committed and pushed iteratively, but merging to `main` and production publication remain explicit author approval gates.

Responsive archive derivatives are reproducible from the unchanged active artwork:

```bash
npm run assets:archive
```

## Curated Publication Boundary

`content/public/manifest.json` is the website's explicit publication allowlist. It currently contains no entries. Internal canon, stories, proposals, and artwork are never imported into public routes merely because they exist in the repository.

Every future public record must have an existing canonical source, a deliberately written public title and summary, an `approved` publication status, a `public` or author-selected `teaser` classification, and a dated author approval record. The prebuild validator rejects restricted classifications, missing sources or images, undeclared internal fields, duplicate identifiers, and cross-references to unpublished records.

See [`docs/PUBLICATION_BOUNDARY.md`](docs/PUBLICATION_BOUNDARY.md) for the complete field contract and approval workflow.

## Initial Vercel Project Settings

When importing `bkswindell/the-brass-guardian` into Vercel, use:

| Setting | Value |
|---|---|
| Framework Preset | `Astro` |
| Root Directory | `website` |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | `npm install` |
| Production Branch | `main` |

With the GitHub integration enabled, pushes to non-production branches create preview deployments. Pushes or merges to `main` create production deployments after the project has been imported.

The production page is reviewed on the generated `vercel.app` deployment before `thebrassguardian.com` and `www.thebrassguardian.com` are connected.

## Cover Artwork

The source cover remains unchanged at `art/The_Brass_Guardian_Cover.png`. Web delivery uses optimized 480px and 767px WebP derivatives under `public/images/`; the root page renders the full composition without cropping and opens it in an accessible native dialog.

The approved cover also appears uncropped in the 1200×630 social preview at `public/images/the-brass-guardian-social.jpg`. The derivative and 180×180 touch icon are generated files and are committed to the repository.

### Regenerating brand assets

From the `website/` directory, create an isolated generator environment and install the pinned dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-generator.txt
```

Then regenerate and verify the committed assets:

```bash
.venv/bin/python scripts/generate-brand-assets.py
npm run verify
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. The generator uses the vendored DejaVu Serif files under `scripts/fonts/`; their license is included there as `LICENSE.txt`, so no system fonts are required.

Pillow is intentionally a local, generator-only dependency. It is not listed in `package.json`, and neither the Vercel install command (`npm install`) nor build command (`npm run build`) installs or invokes it.

## Sharing and Utility Routes

`src/layouts/SiteLayout.astro` owns the shared HTML shell, Vercel instrumentation, and `SiteMeta` integration. `src/components/SiteMeta.astro` owns canonical, Open Graph, Twitter/X card, favicon, manifest, and indexing metadata. The Coming Soon page remains deliberately `noindex, nofollow`. `src/pages/404.astro` provides a public-safe archive-themed error route with an obvious return to the archive entrance.

## Web Analytics

The shared site layout imports the official Astro component from `@vercel/analytics/astro` and renders `<Analytics />`. Analytics begins collecting page views after the integration is deployed and the deployed site is visited.

## Speed Insights

The shared site layout imports the official Astro component from `@vercel/speed-insights/astro` and renders `<SpeedInsights />`. Performance data begins collecting after the integration is deployed and the deployed site is visited.

## References

- [Import an existing project into Vercel](https://vercel.com/docs/getting-started-with-vercel/import)
- [Configure Vercel builds and the project root directory](https://vercel.com/docs/deployments/configure-a-build)
- [Vercel for GitHub](https://vercel.com/docs/git/vercel-for-github)
- [Vercel Web Analytics quickstart](https://vercel.com/docs/analytics/quickstart)
- [Vercel Speed Insights quickstart](https://vercel.com/docs/speed-insights/quickstart)
