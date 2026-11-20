#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120: "The World Today".

A newspaper front page summing up Friday 20 November 2026, drawn
programmatically (see draw_frontpage.py) and held in this repository as
entry.png. This program copies it to the output directory, unchanged,
so both graded runs write byte-identical output. No network is used.

Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_png(data: bytes) -> None:
    """Enforce the competition's gate: a whole PNG, at most 1 MiB
    and at most 1024 by 1024 pixels."""
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > 1_048_576:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(f"entry.png is {width}x{height}, over the limit")
    if not data.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82"):
        raise SystemExit("entry.png is truncated: missing IEND chunk")


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    check_png(data)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(
        data
    ).hexdigest():
        raise SystemExit("copy verification failed")


if __name__ == "__main__":
    main()
