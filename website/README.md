# The Brass Guardian Website

This directory contains the Astro site for **The Brass Guardian**.

Production renders the author-approved C1 Aetherhaven Archives projection with Vercel Web Analytics, Speed Insights, an interactive city map, 67 public records, and a separately warned Hidden Archives index containing 28 closed teaser drawers. Vercel branch Previews retain proposal labels and `noindex`; production consumes only the approved manifest projection.

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

The verification command runs the publication-boundary contract tests, validates the explicit public record and presentation manifests, exercises a real isolated sealed rollback build, builds the published site, and checks the generated Archive projection, metadata, favicon links, social image, web manifest, and custom 404 route.

## Archive publication modes

The Archive has separate public and proposal modes. Production reads author-approved records from `content/public/manifest.json` and approved map/Curator Route metadata from `content/public/archive-presentation.json`; an explicit local preview or Vercel branch Preview dynamically loads the working proposal projection with `noindex`:

```bash
PUBLICATION_PREVIEW=1 npm run dev -- --host 0.0.0.0
npm run verify:archive-preview
```

Vercel sets `VERCEL_ENV=preview` automatically for branch deployments. `VERCEL_ENV=production` takes precedence over every Preview flag, including a conflicting `PUBLICATION_PREVIEW=1`, and therefore cannot load raw proposal records. `content/public/archive-release.json` is the explicit version-controlled release switch. Its `published` state enables the approved projection; changing it to `sealed` removes Archive routes and assets from the generated production artifact.

The landing threshold remains Astro-rendered and scene-first. Enabled Preview builds place a responsive, washed-back Aetherhaven Archive environment behind the existing editorial frame and expose one real `/archive/` invitation link. Hover and keyboard focus change **Invitation Waiting** to **Lock Released** with a restrained light-and-copy transition; no Canvas, WebGL, React, gears, gauges, or mechanical centerpiece is used. Reduced-motion users receive the same state without movement, and navigation works without JavaScript.

Responsive archive derivatives are reproducible from unchanged active artwork and clearly isolated candidate sources after creating the generator environment described below:

```bash
npm run assets:archive
```

The nine author-approved web derivatives—including the 768px and 1024px Archive threshold backdrop—are stored under `public/images/archive/`. Their source artwork and provenance remain separately documented; approval for website publication does not declare generated `AA-2` art to be visual canon. The output-aware build wrapper still resolves CLI or Astro-configured output directories and preserves the fail-closed pruner: if `archive-release.json` returns to `sealed`, the production build removes both `dist/archive/` and `dist/images/archive/` plus unreachable Archive-only bundles.

## Curated Publication Boundary

`content/public/manifest.json` is the website's explicit record allowlist. The approved C1 projection contains 95 entries: 67 ordinary public records and 28 Hidden Archive teasers. `content/public/archive-presentation.json` separately approves exactly 30 map geometries and eight Curator Route annotations. Production does not import the raw Preview catalog; internal canon, stories, proposals, and artwork are never imported into public routes merely because they exist in the repository.

Every public record must have an existing canonical source, a deliberately written public title and summary, an `approved` publication status, a `public` or author-selected `teaser` classification, and a dated author approval record. The prebuild validator rejects restricted safety classifications, missing sources or images, undeclared internal fields, duplicate identifiers, and cross-references to unpublished records. Hidden Archive display labels are separately approved public labels; their validated safety classification remains `teaser`, and no deeper restricted source content enters client output.

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
npm run assets:archive
npm run verify
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. The generator uses the vendored DejaVu Serif files under `scripts/fonts/`; their license is included there as `LICENSE.txt`, so no system fonts are required.

Pillow is intentionally a local, generator-only dependency. It is not listed in `package.json`, and neither the Vercel install command (`npm install`) nor build command (`npm run build`) installs or invokes it.

## Sharing and Utility Routes

`src/layouts/SiteLayout.astro` owns the shared HTML shell, Vercel instrumentation, and `SiteMeta` integration. `src/components/SiteMeta.astro` owns canonical, Open Graph, Twitter/X card, favicon, manifest, and indexing metadata. Published Archive routes declare canonical URLs and `index, follow`; proposal Preview routes remain `noindex, nofollow`. `src/pages/404.astro` provides a public-safe archive-themed error route with an obvious return to the archive entrance.

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
