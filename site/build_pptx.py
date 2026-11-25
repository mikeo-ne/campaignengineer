#!/usr/bin/env python3
"""Compatibility stub for the retired slide generator."""
from __future__ import annotations

import sys

ROOT_HINT = "Use: .venv/bin/python build_assets.py"


def main() -> int:
    print(
        "build_pptx.py is retired. It no longer regenerates the old draft deck.\n"
        f"{ROOT_HINT}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
