import argparse
from pathlib import Path

from PIL import Image

SCRIPT_ROOT = Path(__file__).resolve().parent
WEBSITE_ROOT = SCRIPT_ROOT.parent
REPO_ROOT = WEBSITE_ROOT.parent
DEFAULT_OUTPUT_ROOT = WEBSITE_ROOT / "public" / "images" / "archive"

ASSET_GROUPS = (
    (
        REPO_ROOT / "art" / "Map_of_Aetherhaven.png",
        "map-of-aetherhaven",
        (768, 1152, 1539),
        92,
    ),
    (
        REPO_ROOT / "art" / "Clockwork_Gardens_at_Night.png",
        "clockwork-gardens-at-night",
        (480, 767),
        89,
    ),
    (
        REPO_ROOT / "art" / "Wayfinder_Above_the_Clouds.png",
        "wayfinder-above-clouds",
        (640, 1024),
        89,
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate responsive WebP derivatives for the archive preview."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory that receives generated WebP files.",
    )
    return parser.parse_args()


def resized(image: Image.Image, width: int) -> Image.Image:
    if width == image.width:
        return image.copy()
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def generate_group(
    source_path: Path,
    output_stem: str,
    widths: tuple[int, ...],
    quality: int,
    output_root: Path,
) -> list[Path]:
    if not source_path.is_file():
        raise FileNotFoundError(f"Archive source artwork not found: {source_path}")

    generated = []
    with Image.open(source_path) as source:
        image = source.convert("RGB")
        for width in widths:
            if width > image.width:
                raise ValueError(
                    f"Requested width {width} exceeds source width {image.width}: {source_path}"
                )
            output_path = output_root / f"{output_stem}-{width}.webp"
            derivative = resized(image, width)
            derivative.save(
                output_path,
                "WEBP",
                quality=quality,
                method=6,
                exact=True,
            )
            generated.append(output_path)
    return generated


def main() -> None:
    args = parse_args()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    generated = []
    for group in ASSET_GROUPS:
        generated.extend(generate_group(*group, output_root))

    print(f"Generated {len(generated)} archive WebP derivatives in {output_root}")


if __name__ == "__main__":
    main()
