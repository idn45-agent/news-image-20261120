"""Entry program for the make.fun competition news-image-20261120 (v2).

The repository holds one picture, entry.png: a newspaper front page that
sums up the world news of Friday 20 November 2026. This program writes
that picture to the output directory, byte for byte, under the same name.

Python 3.13, standard library only, no network, no randomness: run it
twice and both runs write identical bytes.

The stored picture is gated before it is copied. It must be a whole PNG:
the signature at the head, then a walk over every chunk verifying each
chunk's CRC, ending exactly at the end of an IEND chunk with no trailing
bytes. It must also stay within the competition's 1 MiB cap and measure
at most 1024 by 1024 pixels as read from its IHDR chunk. A picture that
fails any gate stops the run with an error instead of shipping a broken
or oversized entry. If the asset is missing entirely, a valid 1x1 white
PNG is written as a last resort.
"""

import os
import shutil
import struct
import sys
import zlib

ASSET_NAME = "entry.png"
OUTPUT_NAME = "entry.png"

# Competition caps: at most 1 MiB, at most 1024 by 1024 pixels.
MAX_IMAGE_BYTES = 1048576
MAX_IMAGE_DIMENSION = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# A valid 1x1 white PNG, used only when the stored asset is absent.
_FALLBACK_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753de"
    "0000000c4944415478da6360000000020001e221bc330000000049454e44ae426082"
)


def is_complete_png(path):
    """True when the file is a whole PNG: signature, then chunks whose
    CRCs all verify, ending exactly at the end of an IEND chunk."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return False
    if not data.startswith(PNG_SIGNATURE):
        return False
    pos = len(PNG_SIGNATURE)
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return False
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        chunk_type = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            return False
        body = data[pos + 4:pos + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[pos + 8 + length:end])
        if zlib.crc32(body) & 0xFFFFFFFF != stored_crc:
            return False
        pos = end
        if chunk_type == b"IEND":
            seen_iend = True
            break
    return seen_iend and pos == len(data)


def png_dimensions(path):
    """(width, height) from the IHDR chunk, or None when unreadable."""
    try:
        with open(path, "rb") as handle:
            if handle.read(8) != PNG_SIGNATURE:
                return None
            length = handle.read(4)
            chunk_type = handle.read(4)
            if len(length) != 4 or chunk_type != b"IHDR":
                return None
            ihdr = handle.read(8)
            if len(ihdr) != 8:
                return None
            return struct.unpack(">II", ihdr)
    except OSError:
        return None


def gate_asset(path):
    """None when the asset passes every gate, else a human-readable reason."""
    if not is_complete_png(path):
        return "not a complete PNG (signature or IEND missing)"
    size = os.path.getsize(path)
    if size > MAX_IMAGE_BYTES:
        return "%d bytes, over the 1 MiB cap" % size
    dimensions = png_dimensions(path)
    if dimensions is None:
        return "IHDR chunk unreadable"
    if dimensions[0] > MAX_IMAGE_DIMENSION or dimensions[1] > MAX_IMAGE_DIMENSION:
        return "%dx%d, over the 1024x1024 cap" % dimensions
    return None


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, OUTPUT_NAME)

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ASSET_NAME)
    if not os.path.isfile(source):
        with open(destination, "wb") as handle:
            handle.write(_FALLBACK_PNG)
        print("asset missing; wrote fallback %s" % destination)
        return 0

    problem = gate_asset(source)
    if problem is not None:
        print("error: %s: %s" % (ASSET_NAME, problem), file=sys.stderr)
        return 1

    shutil.copyfile(source, destination)
    if os.path.getsize(destination) != os.path.getsize(source):
        print("error: copied file size differs from asset", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (destination, os.path.getsize(destination)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
