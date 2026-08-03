#!/usr/bin/env python3
"""One-time checksum refresh for owner-approved source formatting edits.

The source transcript wording was not changed. The owner added Markdown hard
line-break spacing inside the immutable source blocks in commit
906cfb932e35f62fa73d01512d389972e7e5b8ea. Because source integrity hashes are
byte-sensitive, this script updates only the two checksum markers in each
reaction record before the normal integration validator runs.

Remove this script and its workflow invocation after the refreshed hashes have
been committed.
"""

from __future__ import annotations

import re

from integrate_media_reactions import MEDIA, REACTIONS, extract_source, source_hash


FRONT_HASH = re.compile(
    r"^source_sha256:\s*[0-9a-f]{64}\s*$", re.MULTILINE
)
DISPLAY_HASH = re.compile(
    r"\*\*Source integrity:\*\* SHA-256 `[0-9a-f]{64}`", re.MULTILINE
)


def main() -> int:
    changed = 0

    for filename in REACTIONS:
        path = MEDIA / filename
        text = path.read_text(encoding="utf-8")
        source, _ = extract_source(text)
        digest = source_hash(source)

        updated, front_count = FRONT_HASH.subn(
            f"source_sha256: {digest}", text, count=1
        )
        updated, display_count = DISPLAY_HASH.subn(
            f"**Source integrity:** SHA-256 `{digest}`", updated, count=1
        )

        if front_count != 1 or display_count != 1:
            raise RuntimeError(
                f"Could not update both checksum markers in {filename}: "
                f"front={front_count}, display={display_count}"
            )

        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"{filename}: {digest}")

    print(f"Refreshed authorized source hashes in {changed} reaction records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
