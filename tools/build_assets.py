"""Shared rendering utilities for the profile poster (dark and light variants).

Colour handling (brand colours nudged until they read on the tile), the glyph
placement helper, HTML escaping and the technology icon tile. tools/poster.py
imports these to compose the single-file README poster; see that module for the
actual README build. All output is self-contained SVG: no external requests and
no scripts. Texts use an Inter-first font stack; Inter's metrics (tools/fonts)
size and wrap the labels.
"""
import colorsys
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
GLYPHS = json.loads((HERE / "glyphs.json").read_text(encoding="utf-8"))

THEMES = {
    "dark": {
        "page": "#0d1117", "tileTop": "#161b22", "tileBottom": "#0d1117", "border": "#30363d",
        "highlight": "#ffffff", "highlightOpacity": 0.07, "glowOpacity": 0.22,
        "text": "#e6edf3", "muted": "#8b949e", "accent": "#00d4ff", "accent2": "#0099cc",
        "minContrast": 4.5,
    },
    "light": {
        "page": "#ffffff", "tileTop": "#ffffff", "tileBottom": "#f3f6f9", "border": "#d0d7de",
        "highlight": "#ffffff", "highlightOpacity": 0.9, "glowOpacity": 0.12,
        "text": "#1f2328", "muted": "#59636e", "accent": "#0086b3", "accent2": "#006a8f",
        "minContrast": 3.0,
    },
}

# Brand-specific colour choices where a mechanical lighten/darken would lose the identity.
OVERRIDES = {
    ("aws", "dark"): "#FF9900",
    ("javascript", "light"): "#C9A800",
}


# --------------------------------------------------------------------------- colour
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexs(c):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02X}" for v in c)


def luminance(h):
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def legible(hex_, theme, key):
    """Brand colour, lightened (dark theme) or darkened (light theme) in HLS until it reads on the tile."""
    t = THEMES[theme]
    if (key, theme) in OVERRIDES:
        return OVERRIDES[(key, theme)]
    base = "#" + hex_.lstrip("#")
    bg = t["tileTop"]
    if contrast(base, bg) >= t["minContrast"]:
        return base
    h, l, s = colorsys.rgb_to_hls(*rgb(base))
    if s < 0.15:
        # Black or grey brands (Kafka, OpenJDK, Ollama...): use the theme's text colour, not a muddy grey.
        return t["text"]
    step = 0.02 if theme == "dark" else -0.02
    for _ in range(60):
        l = max(0.0, min(1.0, l + step))
        cand = hexs(colorsys.hls_to_rgb(h, l, s if s > 0.05 else 0))
        if contrast(cand, bg) >= t["minContrast"]:
            return cand
    return t["text"]


# --------------------------------------------------------------------------- svg helpers
def glyph_svg(g, fill, cx, cy, max_w, max_h):
    """Place the glyph's real bounding box, scaled to fit max_w x max_h, centred on (cx, cy)."""
    x0, y0, x1, y1 = g["bbox"]
    w, h = x1 - x0, y1 - y0
    scale = min(max_w / w, max_h / h)
    dw, dh = w * scale, h * scale
    rule = ' fill-rule="evenodd" clip-rule="evenodd"' if g.get("fillRule") == "evenodd" else ""
    paths = "".join(f'<path d="{d}"/>' for d in g["paths"])
    return (f'<svg x="{cx - dw / 2:.2f}" y="{cy - dh / 2:.2f}" width="{dw:.2f}" height="{dh:.2f}" '
            f'viewBox="{x0} {y0} {w:.3f} {h:.3f}"><g fill="{fill}"{rule}>{paths}</g></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# --------------------------------------------------------------------------- icon tile
def icon_tile(key, g, theme):
    t = THEMES[theme]
    colour = legible(g["hex"], theme, key)
    uid = f"{key}-{theme}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" role="img" aria-label="{esc(g['name'])}">
<title>{esc(g['name'])}</title>
<defs>
<linearGradient id="bg-{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['tileTop']}"/><stop offset="1" stop-color="{t['tileBottom']}"/></linearGradient>
<radialGradient id="glow-{uid}" cx="0.5" cy="0.45" r="0.55"><stop offset="0" stop-color="{colour}" stop-opacity="{t['glowOpacity']}"/><stop offset="1" stop-color="{colour}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="2" y="2" width="92" height="92" rx="22" fill="url(#bg-{uid})"/>
<rect x="2" y="2" width="92" height="92" rx="22" fill="url(#glow-{uid})"/>
<rect x="2.5" y="2.5" width="91" height="91" rx="21.5" fill="none" stroke="{t['border']}"/>
<path d="M24 3.5h48" stroke="{t['highlight']}" stroke-opacity="{t['highlightOpacity']}" stroke-linecap="round"/>
{glyph_svg(g, colour, 48, 48, 60, 46)}
</svg>
"""
