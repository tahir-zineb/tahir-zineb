"""README components in the "data pipeline" style: header, buttons, section titles, metrics, "What I do" rows.

Each function returns a complete SVG string for one theme ("dark" or "light"). Visual language: a dark card
with a faint grid, nodes linked by edges with data packets flowing along them, cyan accent from the portfolio.
Animations are SMIL/CSS inside the SVG and always play (GitHub shows them through <img>).
"""
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
SANS = "'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Mono',Consolas,'Liberation Mono',Menlo,monospace"

THEME = {
    "dark": dict(
        card="#0a0d12", cardStroke="#1e2731", bar="#0d1218", grid="#a8bccf", gridOp=0.075,
        strong="#ffffff", text="#cdd5dd", muted="#8a949e", acc1="#00d4ff", acc2="#0099cc",
        ok="#00ff88", node="#0f151c", nodeStroke="#29353f", icon="#9aabba", edge="#24313d",
        glowOp=0.11, haloOp=0.28, cell="#0a0f14",
    ),
    "light": dict(
        card="#f5f7fa", cardStroke="#dce3ea", bar="#edf1f5", grid="#0a0f14", gridOp=0.055,
        strong="#0a0f14", text="#2a3540", muted="#5b6672", acc1="#0086b3", acc2="#006a8f",
        ok="#00a36c", node="#ffffff", nodeStroke="#c6d1dc", icon="#4f5e6c", edge="#c0ccd7",
        glowOp=0.09, haloOp=0.22, cell="#edf1f5",
    ),
}

# --------------------------------------------------------------------------- text metrics (Inter)
_FONTS = {}


def text_width(text, size, weight=400):
    """Advance width of `text` in Inter at `size` px — used to size buttons and place carets exactly."""
    if weight not in _FONTS:
        _FONTS[weight] = TTFont(HERE / "fonts" / f"inter-{weight}.woff")
    font = _FONTS[weight]
    cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    space = hmtx[cmap[ord(" ")]][0]
    return sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else space for c in text) * size / upm


def f(x):
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s if s else "0"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


STYLE = """<style>
.s{font-family:%s}.m{font-family:%s}
.fu{animation:fu .9s cubic-bezier(.2,.8,.2,1) both}.d1{animation-delay:.08s}.d2{animation-delay:.18s}.d3{animation-delay:.3s}
@keyframes fu{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.caret{animation:bl 1.05s steps(1) infinite}@keyframes bl{50%%{opacity:0}}
</style>""" % (SANS, MONO)


# --------------------------------------------------------------------------- stroke pictograms (centred on 0,0)
IC = {
    "code": '<path d="M-3 -5 L-7.5 0 L-3 5 M3 -5 L7.5 0 L3 5"/>',
    "stream": '<path d="M-7.5 -3.5 q1.9 -2.6 3.75 0 t3.75 0 t3.75 0 t3.75 0 M-7.5 3.5 q1.9 -2.6 3.75 0 t3.75 0 t3.75 0 t3.75 0"/>',
    "db": '<ellipse cx="0" cy="-5" rx="6.5" ry="2.4"/><path d="M-6.5 -5 V5 A6.5 2.4 0 0 0 6.5 5 V-5 M-6.5 0 A6.5 2.4 0 0 0 6.5 0"/>',
    "funnel": '<path d="M-9 -7 H9 L2.2 1.2 V7.5 L-2.2 5.2 V1.2 Z"/>',
    "cloud": '<path d="M-5.5 5.5 H5.8 A4.2 4.2 0 0 0 6.3 -2.9 A6.2 6.2 0 0 0 -5.6 -2.2 A3.9 3.9 0 0 0 -5.5 5.5 Z"/>',
    "spark": '<path d="M0 -7.5 C.7 -2.2 2.2 -.7 7.5 0 C2.2 .7 .7 2.2 0 7.5 C-.7 2.2 -2.2 .7 -7.5 0 C-2.2 -.7 -.7 -2.2 0 -7.5 Z"/>',
    "bars": '<path d="M-6 6.5 V1 M-.5 6.5 V-6 M5 6.5 V-2 M-8 6.5 H7.5"/>',
    "globe": '<circle cx="0" cy="0" r="8"/><ellipse cx="0" cy="0" rx="3.4" ry="8"/><path d="M-8 0H8M-6.6 -4.5H6.6M-6.6 4.5H6.6"/>',
    "mail": '<rect x="-8" y="-6" width="16" height="12" rx="2"/><path d="M-7.5 -5 L0 1 L7.5 -5"/>',
    "file": '<path d="M-5.5 -8 H2 L6 -4 V8 H-5.5 Z M2 -8 V-4 H6"/><path d="M0 -1.5 V5 M-2.8 2.4 L0 5 L2.8 2.4"/>',
    "brain": '<path d="M-1 -7.5 C-5.5 -7.5 -7.5 -4 -6.5 -1 C-8.5 1 -7.5 5.5 -3.5 6 C-2.5 8 0 8 0 6.5 V-6 C0 -7 -.5 -7.5 -1 -7.5 Z M1 -7.5 C5.5 -7.5 7.5 -4 6.5 -1 C8.5 1 7.5 5.5 3.5 6 C2.5 8 0 8 0 6.5"/>',
}
# LinkedIn mark from Simple Icons (CC0), filled, 24x24.
LINKEDIN = ("M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046"
            "c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 "
            "0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452z"
            "M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 "
            "22.222 0h.003z")


def grid_defs(t, w, h, cx, cy):
    return (f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 .5H.5V32" fill="none" '
            f'stroke="{t["grid"]}" stroke-opacity="{t["gridOp"]}"/></pattern>'
            f'<radialGradient id="gf" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{max(w, h) * .55}">'
            f'<stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#fff" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="gm"><rect width="{w}" height="{h}" fill="url(#gf)"/></mask>')


# --------------------------------------------------------------------------- header
def header(mode, p):
    t = THEME[mode]
    W, H = 1200, 320
    BAR = 282

    # typing line: monospace, textLength-locked so the caret lands on the text end in any monospace font
    roles = p["roles"]
    fs_role, cw = 15, 9.0
    tx0, ty = 76, 222
    seq, wins, tt = [], [], 0.0
    for r in roles:
        n, start = len(r), tt
        for i in range(n + 1):
            seq.append((tt, i))
            tt += 0.075 if i < n else 1.9
        for i in range(n - 1, -1, -1):
            seq.append((tt, i))
            tt += 0.03 if i > 0 else 0.45
        wins.append((start, tt))
    TT = tt
    kt = ";".join(f(s / TT) for s, _ in seq)
    wv = ";".join(f(i * cw + 2) for _, i in seq)
    cxv = ";".join(f(tx0 + i * cw + 3) for _, i in seq)
    role_txt = []
    for k, (r, (a, b)) in enumerate(zip(roles, wins)):
        if k == 0:
            vals, kts = "1;0", f"0;{f(b / TT)}"
        elif k == len(roles) - 1:
            vals, kts = "0;1", f"0;{f(a / TT)}"
        else:
            vals, kts = "0;1;0", f"0;{f(a / TT)};{f(b / TT)}"
        role_txt.append(
            f'<text x="{tx0}" y="{ty}" textLength="{f(len(r) * cw)}" lengthAdjust="spacing" opacity="{1 if k == 0 else 0}">{esc(r)}'
            f'<animate attributeName="opacity" calcMode="discrete" values="{vals}" keyTimes="{kts}" dur="{f(TT)}s" repeatCount="indefinite"/></text>')
    w0 = len(roles[0]) * cw

    # pipeline: sources -> pipeline -> cloud -> insights
    CY = 160
    cS, cP, cC, cI = 752, 874, 998, 1116
    sY = [CY - 56, CY, CY + 56]
    iY = [CY - 40, CY + 40]
    edges = {
        "e1": f"M{cS + 16} {sY[0]} C{cS + 60} {sY[0]} {cP - 67} {CY} {cP - 23} {CY}",
        "e2": f"M{cS + 16} {CY} H{cP - 23}",
        "e3": f"M{cS + 16} {sY[2]} C{cS + 60} {sY[2]} {cP - 67} {CY} {cP - 23} {CY}",
        "e4": f"M{cP + 23} {CY} H{cC - 20}",
        "e5": f"M{cC + 20} {CY} C{cC + 62} {CY} {cI - 58} {iY[0]} {cI - 16} {iY[0]}",
        "e6": f"M{cC + 20} {CY} C{cC + 62} {CY} {cI - 58} {iY[1]} {cI - 16} {iY[1]}",
    }
    T = 4.4
    packets = [("e1", .001, .26), ("e2", .03, .27), ("e3", .06, .28), ("e4", .34, .52), ("e5", .58, .84), ("e6", .60, .86)]

    def pulse(base, hot, at, dur=.16):
        a = max(at - .004, .001)
        return (f'<animate attributeName="stroke" values="{base};{base};{hot};{base};{base}" '
                f'keyTimes="0;{f(a)};{f(min(at + .02, .99))};{f(min(at + dur, .995))};1" dur="{T}s" repeatCount="indefinite"/>')

    def node(x, y, s, icon, at):
        h = s / 2
        return (f'<g><rect x="{f(x - h + .5)}" y="{f(y - h + .5)}" width="{s - 1}" height="{s - 1}" rx="{f(s * .26)}" '
                f'fill="{t["node"]}" stroke="{t["nodeStroke"]}">{pulse(t["nodeStroke"], t["acc1"], at)}</rect>'
                f'<g transform="translate({x} {y})" fill="none" stroke="{t["icon"]}" stroke-width="1.5" stroke-linecap="round" '
                f'stroke-linejoin="round">{IC[icon]}</g></g>')

    ring = (f'<circle cx="{cP}" cy="{CY}" r="36" fill="none" stroke="{t["acc1"]}" stroke-opacity=".45" stroke-width="1.2" '
            f'stroke-dasharray="2.5 7.5"><animateTransform attributeName="transform" type="rotate" from="0 {cP} {CY}" '
            f'to="360 {cP} {CY}" dur="28s" repeatCount="indefinite"/></circle>')
    heads = [(cS, "01", "SOURCES"), (cP, "02", "PIPELINE"), (cC, "03", "CLOUD"), (cI, "04", "INSIGHTS")]
    head_svg = "".join(
        f'<text x="{x}" y="66" text-anchor="middle" textLength="{f((len(n) + 3) * 6.6 + (len(n) + 2) * 1.2)}" lengthAdjust="spacing" '
        f'letter-spacing="1.2"><tspan fill="{t["acc1"]}">{i}</tspan> {n}</text>' for x, i, n in heads)
    guides = "".join(f'<path d="M{x} 78 V{BAR - 22}" stroke="{t["grid"]}" stroke-opacity=".16" stroke-dasharray="2 5"/>'
                     for x, _, _ in heads)
    edge_svg = "".join(f'<path id="{k}" d="{d}"/>' for k, d in edges.items())
    ports = "".join(
        f'<circle cx="{x}" cy="{y}" r="2.6" fill="{t["card"]}" stroke="{t["nodeStroke"]}" stroke-width="1.2"/>'
        for x, y in [(cS + 16, sY[0]), (cS + 16, CY), (cS + 16, sY[2]), (cP - 23, CY), (cP + 23, CY),
                     (cC - 20, CY), (cC + 20, CY), (cI - 16, iY[0]), (cI - 16, iY[1])])
    pk = "".join(
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f(a)};{f(a + .03)};{f(b - .02)};{f(b)};1" '
        f'dur="{T}s" repeatCount="indefinite"/><animateMotion dur="{T}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;0;1;1" '
        f'keyTimes="0;{f(a)};{f(b)};1" keySplines="0 0 1 1;.5 0 .5 1;0 0 1 1"><mpath xlink:href="#{e}"/></animateMotion>'
        f'<circle r="7" fill="{t["acc1"]}" opacity="{t["haloOp"]}"/><circle r="2.8" fill="{t["acc1"]}"/></g>'
        for e, a, b in packets)
    nodes = "".join([
        node(cS, sY[0], 32, "code", .001), node(cS, sY[1], 32, "stream", .03), node(cS, sY[2], 32, "db", .06),
        node(cP, CY, 46, "funnel", .27), node(cC, CY, 40, "cloud", .52),
        node(cI, iY[0], 32, "spark", .84), node(cI, iY[1], 32, "bars", .86),
    ])

    first, last = p["name"]
    titles = p["badge"].split(" · ")
    title_svg = f' <tspan fill="{t["acc1"]}">·</tspan> '.join(esc(x) for x in titles)
    status_l = p.get("statusLeft", "now @ LNA Santé · work-study since 2024")
    status_r = p.get("statusRight", "Paris · 2+ yrs")
    mono12 = 7.2
    name_w = text_width(f"{first} ", 54, 800) - 1 * len(first)  # letter-spacing -1

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">{first} {last}</title>
<desc id="d">{esc(p["badge"])}. {esc(p.get("statusLeft","").replace("now @ ","Currently at ").split(" · ")[0])}.</desc>
{STYLE}
<defs>
<linearGradient id="acc" gradientUnits="userSpaceOnUse" x1="{f(54 + name_w)}" y1="0" x2="{f(54 + name_w + 300)}" y2="0"><stop offset="0" stop-color="{t["acc1"]}"/><stop offset="1" stop-color="{t["acc2"]}"/></linearGradient>
{grid_defs(t, W, BAR, 930, CY)}
<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="{cP + 40}" cy="{CY}" r="300"><stop offset="0" stop-color="{t["acc1"]}" stop-opacity="{t["glowOp"]}"/><stop offset="1" stop-color="{t["acc1"]}" stop-opacity="0"/></radialGradient>
<clipPath id="cc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
<clipPath id="tc"><rect x="{tx0 - 1}" y="{ty - 16}" width="{f(w0 + 2)}" height="22"><animate attributeName="width" calcMode="discrete" values="{wv}" keyTimes="{kt}" dur="{f(TT)}s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="16" fill="{t["card"]}"/>
<g clip-path="url(#cc)">
<rect width="{W}" height="{BAR}" fill="url(#grid)" mask="url(#gm)"/>
<rect width="{W}" height="{BAR}" fill="url(#glow)"/>
<rect y="{BAR}" width="{W}" height="{H - BAR}" fill="{t["bar"]}"/>
<path d="M0 {BAR}.5H{W}" stroke="{t["cardStroke"]}"/>
</g>
<g class="s">
<g class="fu"><text class="m" x="56" y="66" font-size="13" textLength="{f(8 * 7.8)}" lengthAdjust="spacing"><tspan fill="{t["acc1"]}">$</tspan><tspan fill="{t["muted"]}"> whoami</tspan></text></g>
<g class="fu d1"><text x="54" y="138" font-size="54" font-weight="800" letter-spacing="-1" fill="{t["strong"]}">{esc(first)} <tspan fill="url(#acc)">{esc(last)}</tspan></text></g>
<g class="fu d2"><text x="56" y="178" font-size="19" font-weight="500" fill="{t["text"]}">{title_svg}</text></g>
<g class="fu d3 m" font-size="{fs_role}">
<text x="56" y="{ty}" fill="{t["acc1"]}">&gt;</text>
<g clip-path="url(#tc)" fill="{t["strong"]}">{"".join(role_txt)}</g>
<rect class="caret" x="{f(tx0 + w0 + 3)}" y="{ty - 13}" width="2" height="16" fill="{t["acc1"]}"><animate attributeName="x" calcMode="discrete" values="{cxv}" keyTimes="{kt}" dur="{f(TT)}s" repeatCount="indefinite"/></rect>
</g>
</g>
<g class="m" font-size="11" fill="{t["muted"]}">{head_svg}</g>
<g fill="none">{guides}</g>
<g fill="none" stroke="{t["edge"]}" stroke-width="1.5">{edge_svg}</g>
{ring}
{ports}
{nodes}
{pk}
<g class="m" font-size="12">
<circle cx="61" cy="{BAR + 19}" r="3.5" fill="{t["ok"]}"/>
<circle cx="61" cy="{BAR + 19}" r="3.5" fill="none" stroke="{t["ok"]}"><animate attributeName="r" values="3.5;9" dur="2.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".7;0" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="74" y="{BAR + 23}" textLength="{f(len(status_l) * mono12)}" lengthAdjust="spacing" fill="{t["muted"]}">{esc(status_l)}</text>
<text x="{W - 56}" y="{BAR + 23}" text-anchor="end" textLength="{f(len(status_r) * mono12)}" lengthAdjust="spacing" fill="{t["muted"]}">{esc(status_r)}</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{t["cardStroke"]}"/>
</svg>
'''


# --------------------------------------------------------------------------- link button
def button(mode, label, icon, primary=False):
    t = THEME[mode]
    label_w = text_width(label, 15, 600)
    W = round(44 + 14 + label_w + 14 + 10 + 16)
    ax = W - 16 - 10
    if icon == "linkedin":
        glyph = (f'<svg x="13" y="13" width="18" height="18" viewBox="0 0 24 24"><path fill="{t["acc1"]}" d="{LINKEDIN}"/></svg>')
    else:
        glyph = (f'<g transform="translate(22 22)" fill="none" stroke="{t["acc1"]}" stroke-width="1.5" stroke-linecap="round" '
                 f'stroke-linejoin="round">{IC[icon]}</g>')
    top = (f'<rect width="{f(W * .6)}" height="1.5" fill="url(#a)"/>' if not primary
           else f'<rect width="{W}" height="2" fill="url(#a)"/>')
    stroke = t["acc1"] if primary else t["nodeStroke"]
    stroke_op = ' stroke-opacity=".7"' if primary else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="44" viewBox="0 0 {W} 44" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["acc1"]}"/><stop offset="1" stop-color="{t["acc2"]}" stop-opacity="{1 if primary else 0}"/></linearGradient>
<clipPath id="c"><rect x=".5" y=".5" width="{W - 1}" height="43" rx="10"/></clipPath></defs>
<rect x=".5" y=".5" width="{W - 1}" height="43" rx="10" fill="{t["node"]}"/>
<g clip-path="url(#c)"><rect width="44" height="44" fill="{t["cell"]}"/><path d="M44.5 0V44" stroke="{t["nodeStroke"]}"/>{top}</g>
<rect x=".5" y=".5" width="{W - 1}" height="43" rx="10" fill="none" stroke="{stroke}"{stroke_op}/>
{glyph}
<text x="58" y="27.5" textLength="{f(label_w)}" lengthAdjust="spacingAndGlyphs" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["strong"]}">{esc(label)}</text>
<path d="M{ax} 27L{ax + 9} 18M{ax + 2.5} 18H{ax + 9}V24.5" fill="none" stroke="{t["muted"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''


# --------------------------------------------------------------------------- section title
def section_title(mode, title, W=880):
    """A node, the title, then an edge running to a port on the right — the pipeline motif as a divider."""
    t = THEME[mode]
    tw = text_width(title, 24, 800)
    x_line = 44 + tw + 18
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="56" viewBox="0 0 {W} 56" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs><linearGradient id="l" gradientUnits="userSpaceOnUse" x1="{f(x_line)}" y1="0" x2="{W - 8}" y2="0"><stop offset="0" stop-color="{t["acc1"]}"/><stop offset="1" stop-color="{t["edge"]}"/></linearGradient></defs>
<rect x="4.75" y="16.75" width="22.5" height="22.5" rx="6" fill="{t["node"]}" stroke="{t["nodeStroke"]}" stroke-width="1.5"/>
<circle cx="16" cy="28" r="4" fill="{t["acc1"]}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="44" y="37" font-family="{SANS}" font-size="24" font-weight="800" letter-spacing="-.3" fill="{t["strong"]}">{esc(title)}</text>
<path d="M{f(x_line)} 28.5H{W - 14}" stroke="url(#l)" stroke-width="1.5" stroke-dasharray="3 5"/>
<circle cx="{W - 9}" cy="28.5" r="3.2" fill="{t["card"]}" stroke="{t["nodeStroke"]}" stroke-width="1.4"/>
<circle r="2.6" fill="{t["acc1"]}"><animateMotion dur="3.6s" repeatCount="indefinite" path="M{f(x_line)} 28.5H{W - 14}"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="3.6s" repeatCount="indefinite"/></circle>
</svg>
'''


# --------------------------------------------------------------------------- metrics strip
def metrics(mode, items, W=880):
    t = THEME[mode]
    H = 112
    n = len(items)
    cw = W / n
    cells = []
    for i, it in enumerate(items):
        cx = cw * i + cw / 2
        cells.append(
            f'<g class="fu" style="animation-delay:{i * .12:.2f}s">'
            f'<text x="{f(cx)}" y="56" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="800" letter-spacing="-.5" fill="url(#acc)">{esc(it["n"])}</text>'
            f'<text x="{f(cx)}" y="84" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="500" fill="{t["muted"]}">{esc(it["l"])}</text></g>')
        if i:
            cells.append(f'<path d="M{f(cw * i)} 26V86" stroke="{t["grid"]}" stroke-opacity=".18" stroke-dasharray="2 5"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(" · ".join(f"{i['n']} {i['l']}" for i in items))}">
<title>Key figures</title>
{STYLE}
<defs><linearGradient id="acc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["acc1"]}"/><stop offset="1" stop-color="{t["acc2"]}"/></linearGradient>
{grid_defs(t, W, H, W / 2, H / 2)}</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["card"]}" stroke="{t["cardStroke"]}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="url(#grid)" mask="url(#gm)"/>
{"".join(cells)}
</svg>
'''


# --------------------------------------------------------------------------- "What I do" row
def wrap(text, size, weight, max_w):
    lines, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}".strip()
        if cur and text_width(cand, size, weight) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def doing_row(mode, item, glyph_svg, index, W=880):
    t = THEME[mode]
    lines = wrap(item["text"], 15, 400, W - 150)
    H = 72 + 22 * len(lines)
    body = "".join(f'<text x="112" y="{66 + 22 * k}" font-family="{SANS}" font-size="15" fill="{t["text"]}">{esc(l)}</text>'
                   for k, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(item["title"])}: {esc(item["text"])}">
<title>{esc(item["title"])}</title>
{STYLE}
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["card"]}" stroke="{t["cardStroke"]}"/>
<path d="M1 {H / 2 - 14}V{H / 2 + 14}" stroke="{t["acc1"]}" stroke-width="2.5" stroke-linecap="round"/>
<g class="fu" style="animation-delay:{index * .1:.2f}s">
<rect x="28.75" y="{H / 2 - 27.25}" width="54.5" height="54.5" rx="14" fill="{t["node"]}" stroke="{t["nodeStroke"]}" stroke-width="1.5"/>
{glyph_svg(56, H / 2)}
<text x="112" y="40" font-family="{SANS}" font-size="19" font-weight="700" fill="{t["strong"]}">{esc(item["title"])}</text>
{body}
</g>
</svg>
'''


def category_label(mode, title, count, W=880):
    t = THEME[mode]
    tw = text_width(title, 15, 600)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="34" viewBox="0 0 {W} 34" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<circle cx="7" cy="17" r="3.5" fill="{t["acc1"]}"/>
<text x="20" y="22" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["strong"]}">{esc(title)}</text>
<text x="{f(20 + tw + 10)}" y="22" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{count:02d}</text>
<path d="M{f(20 + tw + 40)} 17.5H{W - 4}" stroke="{t["edge"]}" stroke-dasharray="2 5"/>
</svg>
'''
