"""Entry program for make.fun competition news-image-20261120.

It writes the poster stored in this repository (entry.png) — a front-page
summary of the world news of Friday 20 November 2026 — to the output
directory, byte for byte, as entry.png. Python 3.13 standard library only;
no network access, no randomness, so repeated runs produce identical bytes.

Before copying, the stored file is verified to be a complete PNG: it must
start with the PNG signature and end with a proper IEND chunk, stay within
the 1 MiB size cap, and measure at most 1024 by 1024 pixels (read from its
IHDR chunk). A damaged asset fails the run loudly instead of shipping a
broken picture.

If the asset is absent (it is present in the submitted snapshot), the program
writes a valid 1x1 white PNG instead, so the run still yields a whole image.
"""

import os
import shutil
import struct
import sys

ASSET_NAME = "entry.png"
OUTPUT_NAME = "entry.png"

# The competition cap: the image must be at most 1 MiB.
MAX_IMAGE_BYTES = 1048576

# The competition cap: the image must be at most 1024 by 1024 pixels.
MAX_IMAGE_DIMENSION = 1024

# A valid 1x1 white PNG, used only when the stored asset is missing.
_FALLBACK_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753de"
    "0000000c4944415478da6360000000020001e221bc330000000049454e44ae426082"
)

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IEND_TAG = b"IEND"


def is_complete_png(path):
    """True when the file opens with the PNG signature and closes with IEND."""
    try:
        with open(path, "rb") as handle:
            header = handle.read(8)
            if header != PNG_SIGNATURE:
                return False
            handle.seek(-12, os.SEEK_END)
            trailer = handle.read(12)
        return trailer[4:8] == IEND_TAG
    except OSError:
        return False


def png_dimensions(path):
    """(width, height) read from the IHDR chunk, or None when unreadable."""
    try:
        with open(path, "rb") as handle:
            header = handle.read(8)
            if header != PNG_SIGNATURE:
                return None
            length = handle.read(4)
            chunk_type = handle.read(4)
            if chunk_type != b"IHDR" or len(length) != 4:
                return None
            ihdr = handle.read(8)
            if len(ihdr) != 8:
                return None
            width, height = struct.unpack(">II", ihdr)
        return (width, height)
    except OSError:
        return None


def write_fallback(destination):
    """Write the 1x1 white PNG to destination."""
    with open(destination, "wb") as handle:
        handle.write(_FALLBACK_PNG)


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, OUTPUT_NAME)

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ASSET_NAME)
    if os.path.isfile(source):
        if not is_complete_png(source):
            print("error: %s is not a complete PNG" % ASSET_NAME, file=sys.stderr)
            return 1
        if os.path.getsize(source) > MAX_IMAGE_BYTES:
            print(
                "error: %s is %d bytes, over the 1 MiB cap" % (ASSET_NAME, os.path.getsize(source)),
                file=sys.stderr,
            )
            return 1
        dimensions = png_dimensions(source)
        if dimensions is None:
            print("error: %s has an unreadable IHDR chunk" % ASSET_NAME, file=sys.stderr)
            return 1
        if dimensions[0] > MAX_IMAGE_DIMENSION or dimensions[1] > MAX_IMAGE_DIMENSION:
            print(
                "error: %s is %dx%d, over the 1024x1024 cap" % (ASSET_NAME, dimensions[0], dimensions[1]),
                file=sys.stderr,
            )
            return 1
        shutil.copyfile(source, destination)
        if os.path.getsize(destination) != os.path.getsize(source):
            print("error: copied file size differs from asset", file=sys.stderr)
            return 1
        print("wrote %s (%d bytes)" % (destination, os.path.getsize(destination)))
    else:
        write_fallback(destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
