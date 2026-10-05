#!/usr/bin/env python3
"""Render a name in a script font as a transparent PNG for the cover letter.

Usage:
    python scripts/make_signature.py --name "First Last" [--out signature.png]
        [--font PATH] [--ink "#14183a"] [--height 300] [--force]

Writes signature.png (by default in the current folder). coverletter.cls
looks for signature.png beside the .tex file, so write it into the
application folder and the letter picks it up with no edits.

Uses the bundled OFL font in ../assets/fonts, never a system font, so the
output is the same on every machine. Refuses to overwrite an existing file
without --force: a user may have put a scan of their real signature there,
and that always wins.
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("FAIL: Pillow is not installed. Run `pip install pillow` and try again.")
    sys.exit(1)

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
DEFAULT_FONT = FONT_DIR / "GreatVibes-Regular.ttf"


def cmap_codepoints(font_path: Path) -> set[int]:
    """Code points the font maps to a real glyph (cmap formats 4 and 12)."""
    data = font_path.read_bytes()
    num_tables = struct.unpack_from(">H", data, 4)[0]
    cmap_off = None
    for i in range(num_tables):
        tag, _, off, _ = struct.unpack_from(">4sIII", data, 12 + 16 * i)
        if tag == b"cmap":
            cmap_off = off
    if cmap_off is None:
        return set()
    n_sub = struct.unpack_from(">H", data, cmap_off + 2)[0]
    points: set[int] = set()
    for i in range(n_sub):
        plat, enc, off = struct.unpack_from(">HHI", data, cmap_off + 4 + 8 * i)
        if (plat, enc) not in ((3, 1), (3, 10), (0, 3), (0, 4), (0, 6)):
            continue
        sub = cmap_off + off
        fmt = struct.unpack_from(">H", data, sub)[0]
        if fmt == 4:
            seg2 = struct.unpack_from(">H", data, sub + 6)[0]
            ends = struct.unpack_from(f">{seg2 // 2}H", data, sub + 14)
            starts = struct.unpack_from(f">{seg2 // 2}H", data, sub + 16 + seg2)
            deltas = struct.unpack_from(f">{seg2 // 2}h", data, sub + 16 + 2 * seg2)
            ro_base = sub + 16 + 3 * seg2
            ranges = struct.unpack_from(f">{seg2 // 2}H", data, ro_base)
            for k, (s, e) in enumerate(zip(starts, ends)):
                for c in range(s, e + 1):
                    if c == 0xFFFF:
                        continue
                    if ranges[k] == 0:
                        gid = (c + deltas[k]) & 0xFFFF
                    else:
                        addr = ro_base + 2 * k + ranges[k] + 2 * (c - s)
                        gid = struct.unpack_from(">H", data, addr)[0]
                        if gid:
                            gid = (gid + deltas[k]) & 0xFFFF
                    if gid:
                        points.add(c)
        elif fmt == 12:
            n_groups = struct.unpack_from(">I", data, sub + 12)[0]
            for g in range(n_groups):
                s, e, gid = struct.unpack_from(">III", data, sub + 16 + 12 * g)
                for c in range(s, e + 1):
                    if gid + (c - s):
                        points.add(c)
    return points


def parse_ink(ink: str) -> tuple[int, int, int]:
    h = ink.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"ink must look like #14183a, got {ink!r}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def render(name: str, font_path: Path, ink: tuple[int, int, int], height: int) -> Image.Image:
    # Render large, crop to the real ink (script swashes overrun the nominal
    # bounding box), then scale to the requested height. BASIC layout keeps
    # the output identical whether or not libraqm is installed.
    size = 400
    font = ImageFont.truetype(str(font_path), size, layout_engine=ImageFont.Layout.BASIC)
    left, top, right, bottom = font.getbbox(name)
    pad = size  # generous room for swashes
    canvas = Image.new("L", (right - left + 2 * pad, bottom - top + 2 * pad), 0)
    ImageDraw.Draw(canvas).text((pad - left, pad - top), name, font=font, fill=255)
    box = canvas.getbbox()
    if box is None:
        raise ValueError("nothing was drawn; check the name and font")
    mask = canvas.crop(box)
    margin = max(4, round(0.06 * mask.height))
    framed = Image.new("L", (mask.width + 2 * margin, mask.height + 2 * margin), 0)
    framed.paste(mask, (margin, margin))
    scale = height / framed.height
    framed = framed.resize((max(1, round(framed.width * scale)), height), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", framed.size, ink + (0,))
    out.putalpha(framed)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help='name as it should be signed, e.g. "John Doe"')
    ap.add_argument("--out", type=Path, default=Path("signature.png"))
    ap.add_argument("--font", type=Path, default=DEFAULT_FONT, help="TrueType/OpenType script font")
    ap.add_argument("--ink", default="#14183a", help="ink colour (default dark blue-black)")
    ap.add_argument("--height", type=int, default=300, help="image height in px (minimum 300)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    args = ap.parse_args(argv)

    name = " ".join(args.name.split())
    if not name:
        print("FAIL: --name is empty.")
        return 1
    if args.height < 300:
        print(f"FAIL: --height {args.height} is below 300 px; the signature would print soft at 1.2 cm.")
        return 1
    if not args.font.exists():
        print(f"FAIL: font not found: {args.font}")
        return 1
    if args.out.exists() and not args.force:
        print(f"STOP: {args.out} already exists and was left alone. It may be a scan of a real "
              "signature, which always wins. Use --force to replace it.")
        return 1
    try:
        ink = parse_ink(args.ink)
    except ValueError as e:
        print(f"FAIL: {e}")
        return 1

    have = cmap_codepoints(args.font)
    missing = sorted({ch for ch in name if not ch.isspace() and ord(ch) not in have})
    if missing:
        shown = ", ".join(f"'{c}' (U+{ord(c):04X})" for c in missing)
        print(f"FAIL: {args.font.name} has no glyph for {shown}. Nothing was written. "
              "Pass --font with a script font that covers these characters, or use a scanned signature.")
        return 1

    img = render(name, args.font, ink, args.height)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out, format="PNG", optimize=False)
    print(f"OK    {args.out}  ({img.width} x {img.height} px, {args.font.name}, ink {args.ink})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
