# Website Deployment Scaffold

This directory contains the temporary static site used to verify the GitHub-to-Vercel deployment workflow for **The Brass Guardian**.

It is intentionally limited to a single `index.html` page. It does not yet publish repository canon, stories, profiles, or artwork.

## Local Verification

From the repository root:

```bash
python3 -m http.server 4173 --directory website
```

Then open <http://localhost:4173>.

## Initial Vercel Project Settings

When importing `bkswindell/the-brass-guardian` into Vercel, use:

| Setting | Value |
|---|---|
| Framework Preset | `Other` |
| Root Directory | `website` |
| Build Command | Leave empty |
| Output Directory | Leave empty |
| Install Command | Leave empty |
| Production Branch | `main` |

With the GitHub integration enabled, pushes to non-production branches create preview deployments. Pushes or merges to `main` create production deployments after the project has been imported.

Do not connect `thebrassguardian.com` or `www.thebrassguardian.com` during this initial scaffolding test. Review the generated `vercel.app` deployment first.

## References

- [Import an existing project into Vercel](https://vercel.com/docs/getting-started-with-vercel/import)
- [Configure Vercel builds and the project root directory](https://vercel.com/docs/deployments/configure-a-build)
- [Vercel for GitHub](https://vercel.com/docs/git/vercel-for-github)
