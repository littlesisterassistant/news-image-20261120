#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the pre-rendered entry.png (Friday 20 November 2026 world news:
Trump defers the Iran decision to 2027, Houthi missiles hit Riyadh's
tallest tower, the ICJ rules Myanmar committed genocide, Trump pardons
baseball's Pete Rose) to the output directory and checks the result fits
the competition limits: at most 1 MiB and at most 1024x1024.

Python 3.13, standard library only. Deterministic: the output is a byte
copy of the bundled image, so two runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def out_dir():
    """Output dir: --output <dir> / --output=<dir>, else
    $MAKEFUN_OUTPUT_DIR, else /output."""
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--output" and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--output="):
            return arg[len("--output="):]
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def png_size(path):
    """Read (width, height) from the PNG IHDR chunk, stdlib only."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("no IHDR chunk found")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256_of(path):
    """SHA-256 of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out = out_dir()
    os.makedirs(out, exist_ok=True)
    dst = os.path.join(out, "entry.png")
    shutil.copyfile(src, dst)

    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    width, height = png_size(dst)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png is {width}x{height}, over the 1024x1024 limit",
              file=sys.stderr)
        return 1
    if sha256_of(src) != sha256_of(dst):
        print("copy mismatch: output differs from the bundled image",
              file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
