#!/usr/bin/env python3
"""Run the canonical linker with cached compiled alias patterns."""

from functools import lru_cache

import link_markdown_references as linker

linker.alias_pattern = lru_cache(maxsize=None)(linker.alias_pattern)

if __name__ == "__main__":
    raise SystemExit(linker.main())
