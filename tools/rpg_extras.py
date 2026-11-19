"""Generate the scrolling ticker, section icons and closing arrow.

Usage:
    python tools/rpg_extras.py

Writes assets/ticker.svg, assets/icons/*.svg and assets/continue.svg.
"""

from pathlib import Path

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Courier New', monospace"
GREEN = "#3fb950"
GOLD = "#d29922"
BLUE = "#58a6ff"
RED = "#f85149"
MUTED = "#8b98a5"
BG = "#0b1017"
LINE = "#2b3a4a"

TICKER_TEXT = (
    "SAVE FILE 01 LOADED  \u25c6  07 ACHIEVEMENTS UNLOCKED  \u25c6  "
    "02 QUESTS CLEARED  \u25c6  CLASS: AI \u00d7 ANDROID  \u25c6  "
    "STATUS: ONLINE  \u25c6  BLOG: NAOJIANGHH.GITHUB.IO  \u25c6  "
)


def ticker() -> str:
    copies = "".join(
        f'<text x="{x}" y="23" font-family="{MONO}" font-size="13" letter-spacing="2" '
        f'fill="{MUTED}">{TICKER_TEXT}</text>'
        for x in (16, 1216, 2416)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 36" width="1200" height="36">
<rect width="1200" height="36" fill="{BG}"/>
<line x1="0" y1="1" x2="1200" y2="1" stroke="{LINE}" stroke-width="1"/>
<line x1="0" y1="35" x2="1200" y2="35" stroke="{LINE}" stroke-width="1"/>
<clipPath id="t"><rect x="0" y="2" width="1200" height="32"/></clipPath>
<g clip-path="url(#t)">
<g>
<animateTransform attributeName="transform" type="translate" from="0 0" to="-1200 0" dur="24s" repeatCount="indefinite"/>
{copies}
</g>
</g>
</svg>
"""


def icon_player() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<rect x="7" y="4" width="18" height="17" fill="{GREEN}"/>
<rect x="11" y="10" width="4" height="5" fill="{BG}">
<animate attributeName="height" values="5;5;1;5;5" keyTimes="0;0.45;0.5;0.55;1" dur="4s" repeatCount="indefinite"/>
</rect>
<rect x="19" y="10" width="4" height="5" fill="{BG}">
<animate attributeName="height" values="5;5;1;5;5" keyTimes="0;0.45;0.5;0.55;1" dur="4s" repeatCount="indefinite"/>
</rect>
<rect x="13" y="21" width="6" height="3" fill="{GREEN}"/>
<rect x="9" y="24" width="14" height="3" fill="{GREEN}" opacity=".55"/>
</svg>
"""


def icon_trophy() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<g fill="{GOLD}">
<rect x="8" y="6" width="16" height="11"/>
<rect x="14" y="17" width="4" height="5"/>
<rect x="10" y="22" width="12" height="3"/>
<rect x="4" y="8" width="3" height="6"/>
<rect x="25" y="8" width="3" height="6"/>
</g>
<g fill="#f0d060">
<rect x="24" y="2" width="3" height="3">
<animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" dur="2.4s" repeatCount="indefinite"/>
</rect>
<rect x="27" y="6" width="2" height="2">
<animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" begin=".8s" dur="2.4s" repeatCount="indefinite"/>
</rect>
</g>
</svg>
"""


def icon_map() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<rect x="4" y="8" width="24" height="17" fill="none" stroke="{BLUE}" stroke-width="2"/>
<line x1="12" y1="8" x2="12" y2="25" stroke="{BLUE}" stroke-width="1" opacity=".5"/>
<line x1="21" y1="8" x2="21" y2="25" stroke="{BLUE}" stroke-width="1" opacity=".5"/>
<circle cx="21" cy="14" r="2.5" fill="{RED}">
<animate attributeName="r" values="2.5;6;2.5" dur="2s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="1;0;1" dur="2s" repeatCount="indefinite"/>
</circle>
</svg>
"""


def icon_joystick() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<rect x="5" y="25" width="22" height="4" fill="{MUTED}"/>
<g transform="translate(16 25)">
<g>
<animateTransform attributeName="transform" type="rotate" values="-14;14;-14" dur="3.2s" repeatCount="indefinite"/>
<rect x="-2" y="-15" width="4" height="15" fill="{MUTED}"/>
<circle cx="0" cy="-17" r="5" fill="{GOLD}"/>
</g>
</g>
</svg>
"""


def continue_arrow() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 40" width="48" height="40">
<g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 7;0 0" dur="1.8s" repeatCount="indefinite"/>
<path d="M12 10 L24 24 L36 10" fill="none" stroke="{GREEN}" stroke-width="5"/>
</g>
</svg>
"""


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    assets = root / "assets"
    icons = assets / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    (assets / "ticker.svg").write_text(ticker(), encoding="utf-8")
    (assets / "continue.svg").write_text(continue_arrow(), encoding="utf-8")
    (icons / "player.svg").write_text(icon_player(), encoding="utf-8")
    (icons / "trophy.svg").write_text(icon_trophy(), encoding="utf-8")
    (icons / "map.svg").write_text(icon_map(), encoding="utf-8")
    (icons / "joystick.svg").write_text(icon_joystick(), encoding="utf-8")
    print("wrote ticker, continue and 4 icons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
