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


def pixel_body(text: str, x: int, y: int) -> tuple[str, int]:
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
    return "".join(rects), cursor - x - NAME_CW


def pixel_text(text: str, x: int, y: int, palette: dict, shadow: bool) -> tuple[str, int]:
    body, width = pixel_body(text, x, y)
    out = ""
    if shadow:
        out += (
            f'<g fill="{palette["accent2"]}" transform="translate(4 4)" opacity=".85">'
            f'<animate attributeName="opacity" values=".85;.55;.85" dur="4s" repeatCount="indefinite"/>'
            f"{body}</g>"
        )
    out += f'<g fill="{palette["ink"]}">{body}</g>'
    return out, width


def status_rows(palette: dict) -> str:
    rows = []
    top = 128
    for i, (label, value) in enumerate(STATS):
        y = top + i * 46
        segments = []
        for s in range(10):
            if s < value:
                segments.append(
                    f'<rect x="{856 + s * 26}" y="{y}" width="22" height="14" '
                    f'fill="{palette["accent"]}">'
                    f'<animate attributeName="width" from="0" to="22" dur="0.5s" '
                    f'begin="0s" fill="freeze"/></rect>'
                )
            else:
                segments.append(
                    f'<rect x="{856 + s * 26}" y="{y}" width="22" height="14" '
                    f'fill="{palette["empty"]}"/>'
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
    body, _ = pixel_body("NAOJIANGHH", 44, 86)
    corners = "".join(
        f'<rect x="{x}" y="{y}" width="10" height="10" fill="{p["accent"]}"/>'
        for x, y in ((8, 8), (W - 18, 8), (8, H - 18), (W - 18, H - 18))
    )
    stars = "".join(
        f'<rect x="{30 + (i * 167) % 1120}" y="-20" width="2" height="2" '
        f'fill="{p["accent"]}" opacity=".2">'
        f'<animate attributeName="y" values="-20;460" dur="{9 + (i % 5) * 2}s" '
        f'begin="-{(i * 2.3) % 9:.1f}s" repeatCount="indefinite"/></rect>'
        for i in range(24)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="{p["bg"]}"/>
<defs>
<clipPath id="frame"><rect x="16" y="16" width="{W - 32}" height="{H - 32}"/></clipPath>
<clipPath id="nameClip">{body}</clipPath>
<linearGradient id="shine" x1="0" x2="1">
<stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
<stop offset=".5" stop-color="#ffffff" stop-opacity=".55"/>
<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
</defs>
<g clip-path="url(#frame)">{stars}</g>
<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="none" stroke="{p["border"]}" stroke-width="2">
<animate attributeName="stroke-opacity" values="1;.55;1" dur="5s" repeatCount="indefinite"/>
</rect>
<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{p["border"]}" stroke-width="1" opacity=".4"/>
{corners}
<text x="44" y="56" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">SAVE FILE 01</text>
<text x="{W - 44}" y="56" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">PLAYER STATUS</text>
{name}
<g fill="#58a6ff" opacity="0" transform="translate(-3 0)">
<animate attributeName="opacity" values="0;0;.5;.5;0" keyTimes="0;.93;.94;.96;.97" dur="8s" repeatCount="indefinite"/>
{body}
</g>
<g fill="#f85149" opacity="0" transform="translate(3 0)">
<animate attributeName="opacity" values="0;0;.5;.5;0" keyTimes="0;.93;.94;.96;.97" dur="8s" repeatCount="indefinite"/>
{body}
</g>
<rect x="-260" y="80" width="150" height="100" fill="url(#shine)" clip-path="url(#nameClip)">
<animate attributeName="x" values="-260;760" dur="6s" begin="1.5s" repeatCount="indefinite"/>
</rect>
<text x="44" y="212" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{p["accent"]}">CLASS : AI × ANDROID</text>
<rect x="356" y="195" width="10" height="20" fill="{p["accent"]}">
<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
<text x="44" y="246" font-family="{MONO}" font-size="16" letter-spacing="1" fill="{p["muted"]}">Fuzhou University · Computer Science · Class of 2028</text>
<g transform="translate(64 280)">
<g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="3.8s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>
<g transform="scale(2)">
<g fill="#58a6ff" opacity=".9">
<rect x="6" y="8" width="20" height="16"/>
<rect x="9" y="4" width="14" height="5"/>
<rect x="6" y="24" width="5" height="4"/>
<rect x="13" y="24" width="5" height="4"/>
<rect x="20" y="24" width="5" height="4"/>
</g>
<rect x="11" y="12" width="4" height="5" fill="{p["bg"]}">
<animate attributeName="height" values="5;5;1;5;5" keyTimes="0;.45;.5;.55;1" dur="4.2s" repeatCount="indefinite"/>
</rect>
<rect x="18" y="12" width="4" height="5" fill="{p["bg"]}">
<animate attributeName="height" values="5;5;1;5;5" keyTimes="0;.45;.5;.55;1" dur="4.2s" repeatCount="indefinite"/>
</rect>
</g>
</g>
</g>
<line x1="640" y1="150" x2="640" y2="352" stroke="{p["border"]}" stroke-width="1"/>
<text x="660" y="112" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{p["muted"]}">SKILLS</text>
{status_rows(p)}
<line x1="44" y1="382" x2="{W - 44}" y2="382" stroke="{p["border"]}" stroke-width="1"/>
<text x="44" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">ACHIEVEMENTS 07</text>
<text x="300" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">QUESTS 02</text>
<text x="470" y="412" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["muted"]}">BLOG naojianghh.github.io</text>
<text x="{W - 44}" y="412" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{p["accent"]}">▶ PRESS START<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></text>
<g clip-path="url(#frame)" opacity="0">
<rect x="16" y="20" width="{W - 32}" height="1" fill="{p["accent"]}">
<animate attributeName="y" values="20;420" dur="7s" repeatCount="indefinite"/>
</rect>
<animate attributeName="opacity" values="0;.05;.05;0" keyTimes="0;.12;.88;1" dur="7s" repeatCount="indefinite"/>
</g>
</svg>
"""


def blog_button() -> str:
    p = PALETTES["dark"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 60" width="380" height="60">
<defs><linearGradient id="bs" x1="0" x2="1">
<stop offset="0" stop-color="#7ee787" stop-opacity="0"/>
<stop offset=".5" stop-color="#7ee787" stop-opacity=".22"/>
<stop offset="1" stop-color="#7ee787" stop-opacity="0"/>
</linearGradient></defs>
<rect width="380" height="60" fill="{p["bg"]}"/>
<rect x="2" y="2" width="376" height="56" fill="none" stroke="{p["accent"]}" stroke-width="2">
<animate attributeName="stroke-opacity" values="1;.45;1" dur="2s" repeatCount="indefinite"/>
</rect>
<rect x="-100" y="2" width="90" height="56" fill="url(#bs)">
<animate attributeName="x" values="-100;400" dur="3.5s" repeatCount="indefinite"/>
</rect>
<rect x="12" y="20" width="12" height="12" fill="{p["accent"]}">
<animate attributeName="opacity" values="1;.3;1" dur="1.2s" repeatCount="indefinite"/>
</rect>
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
