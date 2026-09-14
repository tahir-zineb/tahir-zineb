"""Generate every visual asset of the profile README, in a dark and a light variant.

  assets/icons/{dark,light}/<key>.svg   one tile per technology (tools/glyphs.json)
  assets/ui/{dark,light}/*.svg          header, buttons, key figures, section titles, "What I do" rows
  README.md                             assembled from tools/profile.json and tools/tech.json

GitHub shows the variant matching the viewer's appearance setting through
<picture><source media="(prefers-color-scheme: dark)">. All SVGs are self-contained:
no external requests and no scripts. Texts use an Inter-first font stack; Inter's metrics
(tools/fonts) size the buttons and wrap the lines.

Usage:  python tools/build_assets.py
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


def build_icons():
    for theme in THEMES:
        out = ROOT / "assets" / "icons" / theme
        out.mkdir(parents=True, exist_ok=True)
        for key, g in GLYPHS.items():
            (out / f"{key}.svg").write_text(icon_tile(key, g, theme), encoding="utf-8")
    print(f"icons: {len(GLYPHS)} x {len(THEMES)} themes")


# --------------------------------------------------------------------------- README visuals
import components as C  # noqa: E402

PROFILE = json.loads((HERE / "profile.json").read_text(encoding="utf-8"))
TECH = json.loads((HERE / "tech.json").read_text(encoding="utf-8"))


def build_ui():
    count = 0
    for theme in THEMES:
        out = ROOT / "assets" / "ui" / theme
        out.mkdir(parents=True, exist_ok=True)
        files = {"header.svg": C.header(theme, PROFILE), "metrics.svg": C.metrics(theme, PROFILE["metrics"])}
        for b in PROFILE["buttons"]:
            files[f"button-{b['id']}.svg"] = C.button(theme, b["label"], b["icon"], b.get("primary", False))
        for sid, title in PROFILE["sections"].items():
            files[f"section-{sid}.svg"] = C.section_title(theme, title)
        for i, item in enumerate(PROFILE["doing"]):
            g = GLYPHS[item["glyph"]]
            colour = legible(g["hex"], theme, item["glyph"])
            files[f"doing-{i + 1}.svg"] = C.doing_row(
                theme, item, lambda cx, cy, g=g, colour=colour: glyph_svg(g, colour, cx, cy, 30, 30), i)
        for cat in TECH["categories"]:
            n = sum(1 for t in TECH["tech"] if t["cat"] == cat["id"])
            files[f"cat-{cat['id']}.svg"] = C.category_label(theme, cat["title"], n)
        for name, svg in files.items():
            (out / name).write_text(svg, encoding="utf-8")
        count = len(files)
    print(f"ui: {count} x {len(THEMES)} themes")


def picture(path, alt, width=None, height=None):
    """<picture> that follows the viewer's GitHub theme; dark is the fallback."""
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{path.format(theme="dark")}">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{path.format(theme="light")}">'
            f'<img alt="{esc(alt)}" src="assets/{path.format(theme="dark")}"{size}></picture>')


def build_readme():
    p, L = PROFILE, PROFILE["links"]
    nl = "\n"
    buttons = nl.join(
        f'  <a href="{L[b["id"]]}">{picture("ui/{theme}/button-" + b["id"] + ".svg", b["label"])}</a>' for b in p["buttons"])
    doing = nl.join(
        f'  {picture("ui/{theme}/doing-" + str(i + 1) + ".svg", d["title"] + ": " + d["text"], width=880)}'
        for i, d in enumerate(p["doing"]))
    stack = []
    for cat in TECH["categories"]:
        items = [t for t in TECH["tech"] if t["cat"] == cat["id"]]
        icons = nl.join(f'  {picture("icons/{theme}/" + t["key"] + ".svg", t["name"], 52, 52)}' for t in items)
        label = picture("ui/{theme}/cat-" + cat["id"] + ".svg", cat["title"], width=880)
        stack.append(f"<p>{nl}  {label}{nl}</p>{nl}<p>{nl}{icons}{nl}</p>")

    def section(sid):
        return f'<p>{nl}  {picture("ui/{theme}/section-" + sid + ".svg", p["sections"][sid], width=880)}{nl}</p>'

    readme = f"""<!-- Generated by tools/build_assets.py from tools/profile.json and tools/tech.json. Edit those, then rebuild. -->

<p align="center">
  <a href="{L["portfolio"]}">{picture("ui/{theme}/header.svg", "Mohammed EL-KHOU — " + p["badge"], width=1200)}</a>
</p>

<p align="center">
{buttons}
</p>

<p align="center">
  {picture("ui/{theme}/metrics.svg", "Key figures: " + ", ".join(m["n"] + " " + m["l"] for m in p["metrics"]), width=880)}
</p>

{section("about")}

I'm a **Data & Cloud Engineer** in Paris with 6+ years of experience. At **RMC BFM ADS (Altice Media)** I build the data platforms behind TV and digital advertising: Python ETL and data warehouses, serverless pipelines on AWS, and LLM-powered audience matching on Amazon Bedrock.

Before that I ran Big Data pipelines on Cloudera for **BPCE-SI**, and took computer-vision, NLP and speech models to production at **IMPERIUM** and **3W Media**. MSc in Data Science & AI, Université Sorbonne Paris Nord.

My full résumé, projects and certifications are on my **[portfolio]({L["portfolio"]})** · [projects]({L["projects"]}) · [résumé (PDF)]({L["cv"]}).

{section("doing")}

<p>
{doing}
</p>

{section("stack")}

{chr(10).join(stack)}

{section("connect")}

Open to data and cloud engineering challenges. The fastest way to reach me is by [email]({L["email"]}) or on [LinkedIn]({L["linkedin"]}).

<p align="center">
{buttons}
</p>

<p align="center"><sub>Visuals generated by <a href="tools/">tools/</a> · logos from Simple Icons (CC0) and the AWS Architecture Icons · all trademarks belong to their owners.</sub></p>
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print("README.md written")


def main():
    build_icons()
    build_ui()
    build_readme()


if __name__ == "__main__":
    sys.exit(main())
