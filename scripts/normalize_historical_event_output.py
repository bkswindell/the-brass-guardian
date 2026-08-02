#!/usr/bin/env python3
"""Normalize trailing whitespace in files touched by the historical-event migration."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    "artifacts/027_The_Morningstar_Company_Manifest.md",
    "artifacts/028_Captain_Mara_Vosss_Backward_Clock.md",
    "artifacts/056_High_Council_Thirteenth_Seat_Record.md",
)


def main() -> int:
    for relative in TARGETS:
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print("Normalized historical-event migration output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
