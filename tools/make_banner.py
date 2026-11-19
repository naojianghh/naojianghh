"""Generate the pixel-art banner for a GitHub profile README.

Usage:
    python tools/make_banner.py "YOUR NAME"

Writes assets/banner-dark.svg and assets/banner-light.svg. Re-run the command
whenever the text or the palette changes.
"""

from __future__ import annotations

import sys
from pathlib import Path

CELL_W = 14
CELL_H = 20
GAP = 1
MARGIN_X = 26
MARGIN_TOP = 26
SHADOW_DX = 5
SHADOW_DY = 6
GRADIENT = ("#38bdf8", "#8b5cf6", "#d946ef", "#f43f5e")
SHADOW = {"dark": "#30363d", "light": "#d0d7de"}

FONT: dict[str, list[str]] = {
    " ": ["..", "..", "..", "..", ".."],
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"],
    "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"],
    "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "O": [".#.", "#.#", "#.#", "#.#", ".#."],
    "P": ["##.", "#.#", "##.", "#..", "#.."],
    "Q": [".#.", "#.#", "#.#", "##.", ".##"],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."],
    "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "V": ["#.#", "#.#", "#.#", ".#.", ".#."],
    "W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Z": ["###", "..#", ".#.", "#..", "###"],
    "0": ["###", "#.#", "#.#", "#.#", "###"],
    "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["##.", "..#", ".#.", "#..", "###"],
    "3": ["##.", "..#", ".#.", "..#", "##."],
    "4": ["#.#", "#.#", "###", "..#", "..#"],
    "5": ["###", "#..", "##.", "..#", "##."],
    "6": [".##", "#..", "###", "#.#", "###"],
    "7": ["###", "..#", ".#.", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"],
    "9": ["###", "#.#", "###", "..#", "##."],
    ".": [".", ".", ".", ".", "#"],
    "-": ["...", "...", "###", "...", "..."],
    "_": ["...", "...", "...", "...", "###"],
}


def layout(text: str) -> tuple[int, int, list[str]]:
    glyphs = [FONT.get(char, FONT[" "]) for char in text.upper()]
    width = sum(len(glyph[0]) * CELL_W for glyph in glyphs)
    width += GAP * CELL_W * (len(glyphs) - 1)
    width += MARGIN_X * 2
    height = MARGIN_TOP * 2 + 5 * CELL_H

    rects: list[str] = []
    x = MARGIN_X
    for glyph in glyphs:
        for row, line in enumerate(glyph):
            for col, pixel in enumerate(line):
                if pixel == "#":
                    rects.append(
                        f'<rect x="{x + col * CELL_W}" y="{MARGIN_TOP + row * CELL_H}" '
                        f'width="{CELL_W}" height="{CELL_H}"/>'
                    )
        x += (len(glyph[0]) + GAP) * CELL_W
    return width, height, rects


def build_svg(text: str, theme: str) -> str:
    width, height, rects = layout(text)
    body = "".join(rects)
    stops = "".join(
        f'<stop offset="{offset}" stop-color="{color}"/>'
        for offset, color in zip(("0", ".45", ".75", "1"), GRADIENT)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">\n'
        f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" '
        f'x2="{width}" y2="0">{stops}</linearGradient></defs>\n'
        f'<g fill="{SHADOW[theme]}" transform="translate({SHADOW_DX} {SHADOW_DY})" '
        f'shape-rendering="crispEdges">{body}</g>\n'
        f'<g fill="url(#g)" shape-rendering="crispEdges">{body}</g>\n'
        f"</svg>\n"
    )


def main() -> int:
    text = " ".join(sys.argv[1:]).strip() or "YOUR NAME"
    root = Path(__file__).resolve().parent.parent
    assets = root / "assets"
    assets.mkdir(exist_ok=True)
    for theme, name in (("dark", "banner-dark.svg"), ("light", "banner-light.svg")):
        (assets / name).write_text(build_svg(text, theme), encoding="utf-8")
        print(f"wrote {assets / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
