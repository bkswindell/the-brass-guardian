import { readFile, readdir, stat } from "node:fs/promises";

const root = new URL("../dist/", import.meta.url);
const failures = [];
const canonicalUrl = "https://thebrassguardian.com/";
const socialImageUrl =
  "https://thebrassguardian.com/images/the-brass-guardian-social.jpg";
const socialImageAlt =
  "The Brass Guardian cover displayed beside an invitation to enter the Aetherhaven Archives.";

const expect = (condition, message) => {
  if (!condition) failures.push(message);
};

const readText = async (path) =>
  readFile(new URL(path, root), "utf8").catch(() => "");

const exists = async (path) =>
  stat(new URL(path, root))
    .then((entry) => entry.isFile())
    .catch(() => false);

const pathExists = async (path) =>
  stat(new URL(path, root))
    .then(() => true)
    .catch(() => false);

const sofMarkers = new Set([
  0xc0,
  0xc1,
  0xc2,
  0xc3,
  0xc5,
  0xc6,
  0xc7,
  0xc9,
  0xca,
  0xcb,
  0xcd,
  0xce,
  0xcf,
]);

const readJpegDimensions = (image) => {
  if (image.length < 4 || image[0] !== 0xff || image[1] !== 0xd8) {
    return null;
  }

  let offset = 2;
  while (offset < image.length) {
    if (image[offset] !== 0xff) {
      offset += 1;
      continue;
    }

    while (offset < image.length && image[offset] === 0xff) offset += 1;
    if (offset >= image.length) return null;

    const marker = image[offset];
    offset += 1;

    if (marker === 0x00 || marker === 0xd8) continue;
    if (marker === 0xd9 || marker === 0xda) return null;
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue;
    if (offset + 2 > image.length) return null;

    const segmentLength = image.readUInt16BE(offset);
    if (segmentLength < 2 || offset + segmentLength > image.length) return null;

    if (sofMarkers.has(marker)) {
      if (segmentLength < 7) return null;
      return {
        height: image.readUInt16BE(offset + 3),
        width: image.readUInt16BE(offset + 5),
      };
    }

    offset += segmentLength;
  }

  return null;
};

const indexHtml = await readText("index.html");
const notFoundHtml = await readText("404.html");
const robotsText = await readText("robots.txt");
const manifestText = await readText("site.webmanifest");

expect(
  indexHtml.includes(`<link rel="canonical" href="${canonicalUrl}">`),
  "Home page must declare the canonical URL.",
);
expect(
  indexHtml.includes(`<meta property="og:url" content="${canonicalUrl}">`),
  "Home page must declare the canonical Open Graph URL.",
);
expect(
  indexHtml.includes(
    `<meta property="og:image" content="${socialImageUrl}">`,
  ),
  "Home page must declare the canonical Open Graph image.",
);
expect(
  indexHtml.includes('<meta property="og:image:width" content="1200">') &&
    indexHtml.includes('<meta property="og:image:height" content="630">'),
  "Home page must declare 1200x630 Open Graph dimensions.",
);
expect(
  indexHtml.includes('<meta name="twitter:card" content="summary_large_image">'),
  "Home page must declare a large Twitter/X sharing card.",
);
expect(
  indexHtml.includes(
    `<meta name="twitter:image" content="${socialImageUrl}">`,
  ) &&
    indexHtml.includes(
      `<meta name="twitter:image:alt" content="${socialImageAlt}">`,
    ),
  "Home page must declare the canonical Twitter/X image and alt text.",
);
expect(
  indexHtml.includes('<link rel="icon" href="/favicon.svg" type="image/svg+xml">') &&
    indexHtml.includes('<link rel="apple-touch-icon" href="/apple-touch-icon.png">'),
  "Home page must link the SVG favicon and Apple touch icon.",
);
expect(
  indexHtml.includes('<link rel="manifest" href="/site.webmanifest">'),
  "Home page must link the web manifest.",
);
expect(
  indexHtml.includes("Enter Archive") &&
    indexHtml.includes('href="/archive/"') &&
    !indexHtml.includes("Coming Soon") &&
    !indexHtml.includes('data-renderer="react-three-fiber"') &&
    indexHtml.includes("aetherhaven-archive-threshold"),
  "Published production builds must open the approved Archive entrance without the rejected 3D implementation.",
);
expect(
  indexHtml.includes('<meta name="robots" content="index, follow">'),
  "Published home page must allow indexing.",
);

expect(await exists("favicon.svg"), "The SVG favicon must be emitted.");
expect(
  await exists("apple-touch-icon.png"),
  "The Apple touch icon must be emitted.",
);
expect(
  await exists("images/the-brass-guardian-social.jpg"),
  "The social preview image must be emitted.",
);
expect(await exists("robots.txt"), "robots.txt must be emitted.");
expect(await exists("site.webmanifest"), "The web manifest must be emitted.");
expect(
  await pathExists("images/archive"),
  "Published production builds must emit approved Archive artwork.",
);
expect(
  await pathExists("archive"),
  "Published production builds must emit Archive routes.",
);

const emittedTextFiles = (await readdir(root, { recursive: true })).filter((path) =>
  /\.(?:css|html|js|json|txt)$/u.test(path),
);
const emittedText = (
  await Promise.all(emittedTextFiles.map((path) => readText(path)))
).join("\n");
expect(
  !emittedText.includes("archive-lock-experience") &&
    !emittedText.includes("react-three-fiber") &&
    !emittedText.includes("Archive opening") &&
    !emittedText.includes("Proposal preview.") &&
    !emittedText.includes("Preview only") &&
    !emittedText.includes("Not canonical publication") &&
    !emittedTextFiles.some((path) => path.includes("ArchiveLockExperience")),
  "Production output must not retain Preview labels or rejected island implementation artifacts.",
);

expect(
  robotsText.replace(/\r\n/g, "\n").trimEnd() ===
    "User-agent: *\nDisallow:",
  "robots.txt must allow crawlers to read the page-level noindex directive.",
);

let manifest;
let manifestIsObject = false;
try {
  manifest = JSON.parse(manifestText);
  manifestIsObject =
    manifest !== null && typeof manifest === "object" && !Array.isArray(manifest);
  expect(manifestIsObject, "The web manifest must contain a JSON object.");
} catch {
  expect(false, "The web manifest must contain valid JSON.");
}

if (manifestIsObject) {
  expect(
    manifest.name === "The Brass Guardian" &&
      manifest.short_name === "Brass Guardian" &&
      manifest.description ===
        "An entrance to The Brass Guardian and the Aetherhaven Archives." &&
      manifest.start_url === "/" &&
      manifest.display === "standalone" &&
      manifest.background_color === "#050c16" &&
      manifest.theme_color === "#07111f",
    "The web manifest must preserve the expected app identity and display fields.",
  );

  const expectedIcons = [
    {
      src: "/favicon.svg",
      sizes: "any",
      type: "image/svg+xml",
      purpose: "any",
    },
    {
      src: "/apple-touch-icon.png",
      sizes: "180x180",
      type: "image/png",
      purpose: "any",
    },
  ];
  expect(
    Array.isArray(manifest.icons) &&
      manifest.icons.length === expectedIcons.length &&
      expectedIcons.every((expectedIcon, index) =>
        Object.entries(expectedIcon).every(
          ([key, value]) => manifest.icons[index]?.[key] === value,
        ),
      ),
    "The web manifest must declare the expected SVG and 180x180 PNG icons.",
  );
}

expect(Boolean(notFoundHtml), "A static 404 page must be generated.");
expect(
  notFoundHtml.includes("Archive record not found"),
  "The 404 page must provide a clear archive-themed error heading.",
);
expect(
  notFoundHtml.includes('href="/"'),
  "The 404 page must provide an obvious route home.",
);
expect(
  notFoundHtml.includes('<meta name="robots" content="noindex, nofollow">'),
  "The 404 page must not be indexed.",
);

if (await exists("apple-touch-icon.png")) {
  const icon = await readFile(new URL("apple-touch-icon.png", root));
  expect(
    icon.length >= 24 && icon.toString("ascii", 1, 4) === "PNG",
    "The Apple touch icon must be a valid PNG.",
  );
  expect(
    icon.readUInt32BE(16) === 180 && icon.readUInt32BE(20) === 180,
    "The Apple touch icon must be 180x180.",
  );
}

if (await exists("images/the-brass-guardian-social.jpg")) {
  const socialImage = await readFile(
    new URL("images/the-brass-guardian-social.jpg", root),
  );
  const dimensions = readJpegDimensions(socialImage);
  expect(
    socialImage.length >= 4 &&
      socialImage[0] === 0xff &&
      socialImage[1] === 0xd8 &&
      socialImage.at(-2) === 0xff &&
      socialImage.at(-1) === 0xd9,
    "The social preview image must be a valid JPEG.",
  );
  expect(
    dimensions?.width === 1200 && dimensions?.height === 630,
    "The social preview image must actually be 1200x630.",
  );
}

if (failures.length > 0) {
  console.error(`Site verification failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  "Site verification passed: canonical and sharing metadata, robots, icons, 1200x630 JPEG, manifest, and 404.",
);
