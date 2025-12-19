#!/usr/bin/env python3
"""Entry point for the Keylights CLI."""

from __future__ import annotations

import sys
from pathlib import Path


def _main() -> int:
    src_path = Path(__file__).resolve().parent / "src"
    sys.path.insert(0, str(src_path))

    from keylights.cli import main  # noqa: E402

    return main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(_main())
