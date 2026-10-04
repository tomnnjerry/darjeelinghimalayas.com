"""Build content/outlines.json for the self-drawn SVG maps (no map API, no tiles).

Sources (public domain, Natural Earth, https://www.naturalearthdata.com):
- ne_10m_admin_0_countries_ind: country outlines as seen from India's point of view
  (so India's borders follow the official Survey of India depiction).
- ne_10m_admin_1_states_provinces: West Bengal and Sikkim state lines.
- ne_10m_rivers_lake_centerlines: the Teesta.

Only the Darjeeling-Sikkim-Dooars window is kept, simplified lightly so hill-scale maps stay accurate.
Usage: python tools/build_outlines.py   (downloads the files into .cache/ on first run)
"""
import json
import math
import sys
import urllib.request
from pathlib import Path

sys.setrecursionlimit(100000)
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
COUNTRIES = ["India", "Nepal", "Bhutan", "Bangladesh", "China", "People's Republic of China"]
STATES = ["West Bengal", "Sikkim", "Bihar", "Assam"]
RIVERS = ["Tista"]
BOX = (86.8, 25.6, 90.6, 28.8)  # lng/lat window we ever draw
EPS = 0.0025


def fetch(name):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / name
    if not p.exists():
        print("downloading", name)
        urllib.request.urlretrieve(BASE + name, p)
    return json.loads(p.read_text(encoding="utf-8"))


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def in_box(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return not (max(xs) < BOX[0] or min(xs) > BOX[2] or max(ys) < BOX[1] or min(ys) > BOX[3])


def simplify_ring(ring):
    # split closed rings in two halves first, or RDP collapses them
    half = len(ring) // 2
    a = rdp(ring[: half + 1], EPS)
    b = rdp(ring[half:], EPS)
    return [[round(x, 4), round(y, 4)] for x, y in a[:-1] + b]


def clip(ring):
    """Sutherland-Hodgman clip of a polygon ring to BOX, so big countries stay small."""
    x0, y0, x1, y1 = BOX
    edges = [(lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
             (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))]
    pts = [tuple(p[:2]) for p in ring]
    for inside, cut in edges:
        if not pts:
            break
        out, prev = [], pts[-1]
        for cur in pts:
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
            prev = cur
        pts = out
    return pts


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for p in polys:
        c = clip(p[0])
        if len(c) > 3:
            out.append(simplify_ring(c))
    return out


def main():
    out = {"countries": {}, "states": {}, "rivers": {}}
    for f in fetch("ne_10m_admin_0_countries_ind.geojson")["features"]:
        name = f["properties"].get("NAME_EN") or f["properties"].get("NAME")
        if name in COUNTRIES:
            rs = rings(f["geometry"])
            if rs:
                out["countries"]["China" if "China" in name else name] = rs
    for f in fetch("ne_10m_admin_1_states_provinces.geojson")["features"]:
        pr = f["properties"]
        if pr.get("admin") == "India" and pr.get("name") in STATES:
            rs = rings(f["geometry"])
            if rs:
                out["states"][pr["name"]] = rs
    for f in fetch("ne_10m_rivers_lake_centerlines.geojson")["features"]:
        name = f["properties"].get("name")
        if name in RIVERS:
            g = f["geometry"]
            lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
            out["rivers"][name] = [[[round(x, 4), round(y, 4)] for x, y in rdp(ln, EPS)] for ln in lines if in_box(ln)]
    p = ROOT / "content" / "outlines.json"
    p.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print("wrote", p, p.stat().st_size // 1024, "KB", {k: list(v) for k, v in out.items()})


if __name__ == "__main__":
    main()
