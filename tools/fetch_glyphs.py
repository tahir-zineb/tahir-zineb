"""Collect the logo glyph of every technology listed in tech.json into glyphs.json.

Sources (all fetched once, the result is committed so builds work offline):
  si     Simple Icons 16.31.0 (CC0)            https://simpleicons.org
  si9    Simple Icons 9.21.0 (CC0) — brands later removed from Simple Icons (AWS, Microsoft, Oracle, ...)
  aws    Official AWS Architecture Icons, package of 2026-07-31 (service pictograms)
  custom Drawn here (generic pictograms with no brand, e.g. SQL)

Each glyph also gets its real bounding box ("bbox"), measured with svgpathtools, so the tiles can
centre and scale every logo the same way whatever the margin of the original drawing.

Usage:  pip install svgpathtools && python tools/fetch_glyphs.py
"""
import io
import json
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from svgpathtools import parse_path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
SI = {"si": "16.31.0", "si9": "9.21.0"}
SI_DATA = {"si": "data/simple-icons.json", "si9": "_data/simple-icons.json"}
AWS_ZIP_URL = ("https://d1.awsstatic.com/onedam/marketing-channels/website/public/shared/architecture-icon-release/"
               "Icon-package_07312026.5846e92413caa21490223536cc97f1269e44fa92.zip")
AWS_ROOT = "Architecture-Service-Icons_07312026/"

CUSTOM = {
    # Generic database cylinder, 24x24, drawn for SQL (no brand logo exists).
    "database": {
        "viewBox": "0 0 24 24",
        "paths": [
            "M4 5.25a8 3 0 1 0 16 0a8 3 0 1 0-16 0Z",
            "M4 8.25v3.25c0 1.66 3.58 3 8 3s8-1.34 8-3V8.25c0 1.66-3.58 3-8 3s-8-1.34-8-3Z",
            "M4 14.75V18c0 1.66 3.58 3 8 3s8-1.34 8-3v-3.25c0 1.66-3.58 3-8 3s-8-1.34-8-3Z",
        ],
        "hex": "00ACD7",
    }
}


def get(url):
    CACHE.mkdir(exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", url)[-150:]
    f = CACHE / name
    if not f.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            f.write_bytes(r.read())
    return f.read_bytes()


def title_to_slug(title):
    s = title.lower()
    for a, b in (("+", "plus"), (".", "dot"), ("&", "and"), ("đ", "d"), ("ħ", "h"), ("ı", "i"), ("ĸ", "k"),
                 ("ŀ", "l"), ("ł", "l"), ("ß", "ss"), ("ŧ", "t")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFD", s)
    return re.sub(r"[^a-z0-9]", "", s)


def si_colours(src):
    data = json.loads(get(f"https://cdn.jsdelivr.net/npm/simple-icons@{SI[src]}/{SI_DATA[src]}"))
    icons = data["icons"] if isinstance(data, dict) else data
    return {(i.get("slug") or title_to_slug(i["title"])): i["hex"] for i in icons}


def parse_svg(raw):
    root = ET.fromstring(raw)
    ns = "{http://www.w3.org/2000/svg}"
    return root, ns


def si_glyph(src, slug, colours):
    raw = get(f"https://cdn.jsdelivr.net/npm/simple-icons@{SI[src]}/icons/{slug}.svg")
    root, ns = parse_svg(raw)
    paths = [p.get("d") for p in root.iter(ns + "path")]
    return {"viewBox": root.get("viewBox"), "paths": paths, "hex": colours[slug].upper(), "fillRule": "nonzero"}


def aws_glyph(zf, member):
    raw = zf.read(AWS_ROOT + member)
    root, ns = parse_svg(raw)
    bg = None
    for g in root.iter(ns + "g"):
        if (g.get("id") or "").startswith("Icon-Architecture-BG"):
            # Two export styles exist: fill on the group, or fill on the <rect> inside it.
            rect = g.find(ns + "rect")
            bg = g.get("fill") or (rect.get("fill") if rect is not None else None)
    paths = []
    for p in root.iter(ns + "path"):
        paths.append(p.get("d"))
    if not paths or not bg:
        raise ValueError(f"unexpected AWS icon structure: {member}")
    # The pictogram sits inside a 64x64 square with a margin; crop to it.
    return {"viewBox": "8 8 48 48", "paths": paths, "hex": bg.lstrip("#").upper(), "fillRule": "evenodd"}


def bbox(paths):
    xs, ys = [], []
    for d in paths:
        x0, x1, y0, y1 = parse_path(d).bbox()
        xs += [x0, x1]
        ys += [y0, y1]
    return [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]


def main():
    spec = json.loads((HERE / "tech.json").read_text(encoding="utf-8"))
    colours = {src: si_colours(src) for src in SI}
    zf = None
    out = {}
    for t in spec["tech"]:
        src, slug = t["src"], t["slug"]
        if src in SI:
            g = si_glyph(src, slug, colours[src])
            g["source"] = f"Simple Icons {SI[src]} ({slug})"
        elif src == "aws":
            if zf is None:
                zf = zipfile.ZipFile(io.BytesIO(get(AWS_ZIP_URL)))
            g = aws_glyph(zf, slug)
            g["source"] = "AWS Architecture Icons 2026-07-31"
        elif src == "custom":
            g = dict(CUSTOM[slug], fillRule="nonzero", source="custom")
        else:
            raise ValueError(src)
        g["bbox"] = bbox(g["paths"])
        out[t["key"]] = {"name": t["name"], "cat": t["cat"], **g}
        print(f"{t['key']:<16} {g['hex']}  {len(g['paths'])} path(s)  {g['source']}")
    (HERE / "glyphs.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(out)} glyphs -> tools/glyphs.json")


if __name__ == "__main__":
    sys.exit(main())
