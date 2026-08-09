from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCRIPT_ROOT = Path(__file__).resolve().parent
WEBSITE_ROOT = SCRIPT_ROOT.parent
REPO_ROOT = WEBSITE_ROOT.parent
PUBLIC_ROOT = WEBSITE_ROOT / "public"
COVER_PATH = REPO_ROOT / "art" / "The_Brass_Guardian_Cover.png"
FONT_ROOT = SCRIPT_ROOT / "fonts"
SERIF = FONT_ROOT / "DejaVuSerif.ttf"
SERIF_BOLD = FONT_ROOT / "DejaVuSerif-Bold.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: str,
    spacing: int = 4,
) -> None:
    left, top, right, bottom = draw.multiline_textbbox(
        (0, 0), text, font=text_font, spacing=spacing, align="center"
    )
    width = right - left
    height = bottom - top
    box_left, box_top, box_right, box_bottom = box
    x = box_left + (box_right - box_left - width) / 2
    y = box_top + (box_bottom - box_top - height) / 2
    draw.multiline_text(
        (x, y),
        text,
        font=text_font,
        fill=fill,
        spacing=spacing,
        align="center",
    )


def create_touch_icon() -> None:
    size = 180
    image = Image.new("RGB", (size, size), "#07111f")
    draw = ImageDraw.Draw(image)
    draw.ellipse((24, 24, 156, 156), outline="#b67a26", width=6)
    draw.ellipse((34, 34, 146, 146), outline="#d6c291", width=2)
    draw_centered_text(
        draw,
        (34, 34, 146, 146),
        "AH",
        font(SERIF, 52),
        "#f3e3bb",
    )
    image.save(PUBLIC_ROOT / "apple-touch-icon.png", optimize=True)


def create_social_preview() -> None:
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), "#050c16")
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            radial = max(0.0, 1.0 - (((x - 760) / 760) ** 2 + ((y - 300) / 520) ** 2))
            vertical = y / height
            pixels[x, y] = (
                int(5 + 7 * radial),
                int(12 + 27 * radial + 3 * vertical),
                int(22 + 38 * radial + 7 * vertical),
            )

    draw = ImageDraw.Draw(image, "RGBA")
    for x in range(0, width, 60):
        draw.line((x, 0, x, height), fill=(126, 210, 236, 8), width=1)
    for y in range(0, height, 60):
        draw.line((0, y, width, y), fill=(126, 210, 236, 8), width=1)

    draw.rectangle((24, 24, width - 24, height - 24), outline=(182, 122, 38, 145), width=2)
    draw.rectangle((34, 34, width - 34, height - 34), outline=(214, 194, 145, 65), width=1)

    with Image.open(COVER_PATH) as source:
        cover = source.convert("RGB")
    cover.thumbnail((360, 540), Image.Resampling.LANCZOS)

    shadow = Image.new("RGBA", (cover.width + 50, cover.height + 50), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle((25, 18, 25 + cover.width, 18 + cover.height), fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    cover_x = 790
    cover_y = (height - cover.height) // 2
    image.paste(shadow, (cover_x - 25, cover_y - 18), shadow)
    image.paste(cover, (cover_x, cover_y))
    draw.rectangle(
        (cover_x - 2, cover_y - 2, cover_x + cover.width + 2, cover_y + cover.height + 2),
        outline=(182, 122, 38, 220),
        width=2,
    )

    draw.text((92, 84), "AETHERHAVEN ARCHIVES", font=font(SERIF_BOLD, 22), fill="#d8a34b")
    draw.line((92, 126, 660, 126), fill=(182, 122, 38, 165), width=2)
    draw.multiline_text(
        (88, 174),
        "THE BRASS\nGUARDIAN",
        font=font(SERIF_BOLD, 62),
        fill="#f3e3bb",
        spacing=-2,
    )
    draw.text((94, 364), "ENTER ARCHIVE", font=font(SERIF, 30), fill="#d8a34b")
    draw.multiline_text(
        (94, 424),
        "Follow the curator's route—or open the\ncatalog and follow your own thread.",
        font=font(SERIF, 22),
        fill="#c9dfe5",
        spacing=10,
    )
    draw.text((94, 552), "TheBrassGuardian.com", font=font(SERIF_BOLD, 18), fill="#8db9c7")

    output = PUBLIC_ROOT / "images" / "the-brass-guardian-social.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=90, optimize=True, progressive=True, subsampling="4:4:4")


def main() -> None:
    PUBLIC_ROOT.mkdir(parents=True, exist_ok=True)
    create_touch_icon()
    create_social_preview()
    print("Generated apple-touch-icon.png and 1200x630 social preview.")


if __name__ == "__main__":
    main()
