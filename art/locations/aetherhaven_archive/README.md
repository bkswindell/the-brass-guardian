# Aetherhaven Archive Active Art

This directory contains the creator-approved active environment image for the Aetherhaven Archives.

## Approval and publication status

- **Active image:** `AA-2.png`
- **Creative status:** creator-approved active art
- **Website use:** selected for the World Entrance feature Preview
- **Production publication:** not yet approved

Brad Swindell accepted the corrected `AA-2.png` on August 9, 2026 and directed that it become the permanent Archive environment image. The remaining `AA-*` variants were moved to `unused/aetherhaven_archive/`, which is outside canon and must not be consulted or reused unless the author explicitly restores a named file.

## `AA-2.png`

`AA-2.png` is a source-preserving correction of `unused/aetherhaven_archive/AA-1.png`, created and accepted on 2026-08-09.

### Provenance

- Source: `unused/aetherhaven_archive/AA-1.png`
- Source SHA-256: `6c3af24dd86096becb9edf11905c5d864a4fc9c570f7c8842262f8d39e8517a5`
- Output: `AA-2.png`
- Output SHA-256: `1b40b14d384c5580ab6249d790ec9df16293398125b0469210029a615c5bc91c`
- Output dimensions: `1672 × 941`
- Method: local source-preserving inpainting using IOPaint `1.6.0` with the CPU-hosted LaMa `big-lama` model
- LaMa model download MD5 reported by IOPaint: `e3aa4aaa15225a33ec84f9f4bc47e500`
- Whole-scene text-to-image regeneration: none used in the retained result

### Approved corrective scope

The retained correction:

1. removes the malformed pseudo-lettering from the foreground brass plate and reconstructs it as an unlettered, worn brass surface;
2. removes three redundant side clocks while retaining the distant central civic chronometer;
3. removes six oversized decorative gallery wheels while preserving the surrounding Archive architecture;
4. removes the remaining right foreground desk clock to reduce mirrored repetition;
5. preserves the original left task lamps after a rejected experimental removal introduced less convincing detail;
6. preserves the central aisle, glazed roof, catalog drawers, reading desks, warm task lighting, cool ambient light, and original resolution.

### Verification

Compared with `AA-1.png`:

- pixels changed by more than five channel values: `2.374%`;
- changed pixels in the central website-overlay region: `0.550%`;
- mean source luminance: `28.847`;
- mean corrected luminance: `28.451`.

The correction preserves the reviewed composition and overlay clearance while addressing the most visible generated-image defects. Acceptance establishes `AA-2.png` as the active artwork; production publication remains subject to the separate `main` merge and production approval gate.
