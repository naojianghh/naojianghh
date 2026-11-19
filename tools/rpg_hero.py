"""Generate the RPG-style hero panel and blog button for the profile README.

Usage:
    python tools/rpg_hero.py

Writes assets/hero-dark.svg, assets/hero-light.svg and assets/blog-button.svg.
"""

from __future__ import annotations

from pathlib import Path

from make_banner import FONT

W, H = 1200, 440
NAME_CW, NAME_CH = 10, 14

PALETTES = {
    "dark": {
        "bg": "#0b1017",
        "border": "#2b3a4a",
        "ink": "#e6e0cf",
        "muted": "#8b98a5",
        "accent": "#7ee787",
        "accent2": "#f0b429",
        "empty": "#1d2834",
    },
    "light": {
        "bg": "#f7f1e3",
        "border": "#bdb39c",
        "ink": "#1f2328",
        "muted": "#6e6759",
        "accent": "#1a7f37",
        "accent2": "#9a6700",
        "empty": "#e4dcc9",
    },
}

STATS = [
    ("ANDROID", 8),
    ("KOTLIN", 8),
    ("PYTHON", 7),
    ("TYPESCRIPT", 6),
    ("AI / LLM", 8),
]

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Courier New', monospace"


def pixel_text(text: str, x: int, y: int, palette: dict, shadow: bool) -> tuple[str, int]:
    glyphs = [FONT.get(char, FONT[" "]) for char in text.upper()]
    rects: list[str] = []
    cursor = x
    for glyph in glyphs:
        for row, line in enumerate(glyph):
            for col, pixel in enumerate(line):
                if pixel == "#":
                    rects.append(
                        f'<rect x="{cursor + col * NAME_CW}" y="{y + row * NAME_CH}" '
                        f'width="{NAME_CW}" height="{NAME_CH}"/>'
                    )
        cursor += (len(glyph[0]) + 1) * NAME_CW
    width = cursor - x - NAME_CW
    body = "".join(rects)
    out = ""
    if shadow:
        out += f'<g fill="{palette["accent2"]}" transform="translate(4 4)" opacity=".85">{body}</g>'
    out += f'<g fill="{palette["ink"]}">{body}</g>'
    return out, width


def status_rows(palette: dict) -> str:
    rows = []
    top = 128
    for i, (label, value) in enumerate(STATS):
        y = top + i * 46
        segments = []
        for s in range(10):
            fill = palette["accent"] if s < value else palette["empty"]
            segments.append(
                f'<rect x="{856 + s * 26}" y="{y}" width="22" height="14" fill="{fill}"/>'
            )
        rows.append(
            f'<text x="660" y="{y + 13}" font-family="{MONO}" font-size="16" '
            f'letter-spacing="1" fill="{palette["ink"]}">{label}</text>'
            f'<text x="1158" y="{y + 13}" text-anchor="end" font-family="{MONO}" '
            f'font-size="15" fill="{palette["muted"]}">{value:02d}</text>'
            + "".join(segments)
        )
    return "".join(rows)


def hero_svg(theme: str) -> str:
    p = PALETTES[theme]
    name, name_w = pixel_text("NAOJIANGHH", 44, 86, p, shadow=True)
    corners = "".join(
        f'<rect x="{x}" y="{y}" width="10" height="10" fill="{p["accent"]}"/>'
        for x, y in ((8, 8), (W - 18, 8), (8, H - 18), (W - 18, H - 18))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="{p["bg"]}"/>
<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="none" stroke="{p["border"]}" stroke-width="2"/>
<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{p["border"]}" stroke-width="1" opacity=".4"/>
{corners}
<text x="44" y="56" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">SAVE FILE 01</text>
<text x="{W - 44}" y="56" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">PLAYER STATUS</text>
{name}
<text x="44" y="212" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{p["accent"]}">CLASS : AI × ANDROID</text>
<text x="44" y="246" font-family="{MONO}" font-size="16" letter-spacing="1" fill="{p["muted"]}">Fuzhou University · Computer Science · Class of 2028</text>
<line x1="640" y1="150" x2="640" y2="352" stroke="{p["border"]}" stroke-width="1"/>
<text x="660" y="112" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">SKILLS</text>
{status_rows(p)}
<line x1="44" y1="382" x2="{W - 44}" y2="382" stroke="{p["border"]}" stroke-width="1"/>
<text x="44" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">ACHIEVEMENTS 07</text>
<text x="300" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">QUESTS 02</text>
<text x="470" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">BLOG naojianghh.github.io</text>
<text x="{W - 44}" y="412" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["accent"]}">▶ PRESS START</text>
</svg>
"""


def blog_button() -> str:
    p = PALETTES["dark"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 60" width="380" height="60">
<rect width="380" height="60" fill="{p["bg"]}"/>
<rect x="2" y="2" width="376" height="56" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
<rect x="12" y="20" width="12" height="12" fill="{p["accent"]}"/>
<text x="38" y="34" font-family="{MONO}" font-size="18" letter-spacing="3" fill="{p["accent"]}">VISIT BLOG</text>
<text x="366" y="35" text-anchor="end" font-family="{MONO}" font-size="15" fill="{p["muted"]}">naojianghh.github.io</text>
</svg>
"""


def main() -> int:
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        (assets / f"hero-{theme}.svg").write_text(hero_svg(theme), encoding="utf-8")
    (assets / "blog-button.svg").write_text(blog_button(), encoding="utf-8")
    print("wrote hero-dark.svg, hero-light.svg, blog-button.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
