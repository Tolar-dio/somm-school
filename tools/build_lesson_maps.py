#!/usr/bin/env python3
"""Build the small region maps shown in region lessons.

Reads the atlas data in a Tolar-dio/wine-world checkout (region outlines,
country shapes, wine rivers) and writes one file per map to
assets/js/data/maps/<key>.js, plus assets/js/data/maps-index.js, which says
which lessons use which map. Lessons load their map on demand.

    python3 tools/build_lesson_maps.py /path/to/wine-world

Numbers on the map match the list printed beneath it, so no label can collide.
"""
import json, math, os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "../wine-world"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets/js/data/maps")
W = 640

FR_BDX = ["Médoc", "Graves", "Sauternais", "Libournais", "Entre-Deux-Mers", "Blaye and Bourg"]
FR_BURG = ["Chablis and the Grand Auxerrois", "Côte de Nuits", "Côte de Beaune", "Côte Chalonnaise", "Mâconnais", "Beaujolais"]
FR_CHAMP = ["Montagne de Reims", "Vallée de la Marne", "Côte des Blancs", "Côte de Sézanne", "Côte des Bar"]
FR_LOIRE = ["Pays Nantais", "Anjou-Saumur", "Touraine", "Centre-Loire"]
FR_SW = ["Bergerac and Dordogne", "Cahors and the Lot", "Gaillac, Fronton and the Tarn", "Gascony and the Pyrenees"]
IT_ALL = ["Valle d'Aosta", "Piedmont", "Liguria", "Lombardy", "Trentino-Alto Adige", "Veneto", "Friuli Venezia Giulia", "Emilia-Romagna",
          "Tuscany", "Umbria", "Marche", "Lazio", "Abruzzo", "Molise", "Campania", "Puglia", "Basilicata", "Calabria", "Sicily", "Sardinia"]
ES_MAIN = ["Galicia", "Bierzo", "Castilla y León", "Basque Country", "Rioja", "Navarra", "Aragón", "Catalonia", "Priorat", "Penedès",
           "Madrid", "Castilla-La Mancha", "Valencia", "Murcia", "Extremadura", "Andalusia", "Sherry Country"]
PT_MAIN = ["Vinho Verde", "Trás-os-Montes", "Douro Valley", "Távora-Varosa", "Bairrada", "Dão", "Beira Interior", "Lisboa", "Tejo",
           "Península de Setúbal", "Alentejo", "Algarve"]
DE_ALL = ["Ahr", "Mittelrhein", "Mosel", "Saar", "Ruwer", "Nahe", "Rheingau", "Rheinhessen", "Pfalz", "Hessische Bergstraße", "Franken",
          "Württemberg", "Baden", "Saale-Unstrut", "Sachsen"]
AT_ALL = ["Niederösterreich", "Wien", "Burgenland", "Steiermark"]
HU_ALL = ["Tokaj", "Upper Hungary", "Northern Pannonia", "Balaton", "Pannon", "Danube"]
GR_ALL = ["Macedonia", "Epirus", "Thessaly", "Central Greece and Attica", "Peloponnese", "Ionian Islands", "Aegean Islands", "Cyclades", "Dodecanese", "Crete"]
CA_US = ["Mendocino County", "Lake County", "Sonoma County", "Napa Valley", "Lodi", "Sierra Foothills", "Central Coast", "Paso Robles",
         "Santa Barbara County", "Southern California"]
AU_ALL = ["Western Australia", "South Australia", "Victoria", "New South Wales", "Tasmania", "Queensland"]
CL_ALL = ["Atacama", "Coquimbo", "Aconcagua", "Valle del Maipo", "Valle del Rapel", "Valle de Curicó", "Valle del Maule", "Sur", "Austral"]
AR_MAIN = ["Salta", "Catamarca", "La Rioja", "San Juan", "Mendoza", "Patagonia"]
ZA_ALL = ["Olifants River", "Cape West Coast", "Coastal Region", "Breede River Valley", "Klein Karoo", "Cape South Coast"]

# key: (title, country codes drawn, regions numbered, padding in degrees)
MAPS = {
    "bordeaux": ("Bordeaux", ["fr"], FR_BDX, 0.25),
    "burgundy": ("Burgundy and Beaujolais", ["fr"], FR_BURG, 0.3),
    "champagne": ("Champagne", ["fr"], FR_CHAMP, 0.3),
    "loire": ("The Loire", ["fr"], FR_LOIRE, 0.4),
    "loire-east": ("Loire, Alsace and Jura", ["fr"], FR_LOIRE + ["Alsace", "Jura"], 0.5),
    "alsace": ("Alsace", ["fr"], ["Alsace"], 0.5),
    "rhone-south": ("The Rhône and Southern France", ["fr"], ["Northern Rhône", "Southern Rhône", "Provence", "Languedoc-Roussillon", "Southwest France"], 0.4),
    "rhone": ("The Rhône", ["fr"], ["Northern Rhône", "Diois", "Southern Rhône"], 0.3),
    "midi": ("Languedoc-Roussillon and Provence", ["fr"], ["Languedoc-Roussillon", "Roussillon", "Provence"], 0.4),
    "france-rest": ("Jura, Savoie, Corsica and the Southwest", ["fr"], ["Jura", "Bugey", "Savoie"] + FR_SW + ["Corsica"], 0.4),
    "piedmont": ("Piedmont", ["it"], ["Alto Piemonte", "Roero", "Langhe", "Monferrato"], 0.3),
    "italy-north": ("Northern Italy", ["it"], IT_ALL[:8], 0.3),
    "italy-south": ("Central and Southern Italy", ["it"], IT_ALL[8:], 0.4),
    "italy-central": ("Central Italy", ["it"], ["Tuscany", "Umbria", "Marche", "Lazio", "Abruzzo"], 0.3),
    "italy": ("Italy", ["it"], IT_ALL, 0.4),
    "spain": ("Spain", ["es"], ES_MAIN, 0.4),
    "rioja": ("Rioja", ["es"], ["Rioja Alta", "Rioja Alavesa", "Rioja Oriental"], 0.3),
    "sherry": ("Sherry Country", ["es"], ["Sherry Country"], 0.6),
    "portugal": ("Portugal", ["pt"], PT_MAIN, 0.4),
    "germany": ("Germany", ["de"], DE_ALL, 0.4),
    "austria": ("Austria", ["at"], AT_ALL, 0.4),
    "hungary": ("Hungary", ["hu"], HU_ALL, 0.4),
    "greece": ("Greece", ["gr"], GR_ALL, 0.4),
    "switzerland": ("Switzerland", ["ch"], ["Genève", "Vaud", "Valais", "Three Lakes", "German-speaking Switzerland", "Ticino"], 0.3),
    "georgia": ("Georgia", ["ge"], ["Kakheti", "Kartli", "Imereti", "Racha-Lechkhumi and Kvemo Svaneti"], 0.4),
    "croatia": ("Croatia", ["hr"], ["Istria and Kvarner", "Dalmatia", "Croatian Uplands", "Slavonia and Croatian Danube"], 0.4),
    "california": ("California", ["us"], CA_US, 0.5),
    "northwest": ("Oregon and Washington", ["us"], ["Columbia Valley", "Willamette Valley", "Southern Oregon"], 0.6),
    "newyork": ("New York", ["us"], ["New York"], 0.5),
    "australia": ("Australia", ["au"], AU_ALL, 1.5),
    "newzealand": ("New Zealand", ["nz"], ["North Island", "South Island"], 0.8),
    "argentina": ("Argentina", ["ar", "cl"], AR_MAIN, 1.0),
    "chile": ("Chile", ["cl", "ar"], CL_ALL, 0.8),
    "southafrica": ("South Africa", ["za"], ZA_ALL, 0.5),
    "niagara": ("Ontario", ["ca"], ["Niagara Peninsula"], 0.8),
    "england": ("England and Wales", ["gb"], ["South East England", "Wessex", "East Anglia", "South West England", "Wales"], 0.4),
}
LESSONS = {
    "r1": ["bordeaux"], "r1b": ["bordeaux"], "r1c": ["bordeaux"],
    "r2": ["burgundy"], "r2b": ["burgundy"], "r2c": ["burgundy"],
    "r3": ["champagne"], "r3b": ["champagne"], "sp1": ["champagne"],
    "r4": ["loire-east"], "r4b": ["loire"], "r4c": ["alsace"], "r4d": ["france-rest"],
    "r5": ["rhone-south"], "r5b": ["france-rest"], "r5c": ["rhone"], "r5d": ["midi"],
    "r6": ["italy-north"], "r6b": ["piedmont"], "r7": ["italy-south"], "r7b": ["italy"], "r7c": ["italy-central"],
    "r7d": ["italy"], "r7e": ["italy"],
    "r8": ["spain", "rioja"], "r8b": ["spain"], "r8c": ["spain", "rioja"], "r9": ["sherry"], "fo1": ["sherry"],
    "r10": ["portugal"], "r10b": ["portugal"], "r11": ["germany"], "r11b": ["germany"],
    "r12": ["austria", "hungary", "greece"], "r12b": ["georgia", "croatia"], "r12c": ["austria"], "r12d": ["greece"],
    "r12e": ["hungary", "switzerland", "georgia"],
    "r13": ["california"], "r13b": ["california"], "r14": ["northwest", "newyork"], "r14b": ["northwest"],
    "r15": ["australia", "newzealand"], "r15b": ["australia"], "r15c": ["newzealand"],
    "r16": ["argentina", "chile"], "r16b": ["argentina", "chile"], "r17": ["southafrica", "niagara"], "r17b": ["southafrica"], "r18": ["england"],
}

def load(p):
    return json.load(open(os.path.join(SRC, "docs/data", p), encoding="utf-8"))["features"]

regions, countries, rivers = load("geo/_regions.geojson"), load("base/countries_low.geojson"), load("base/rivers.geojson")

def rings(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        return [r for poly in geom["coordinates"] for r in poly]
    if geom["type"] == "LineString":
        return [geom["coordinates"]]
    return geom["coordinates"]  # MultiLineString

def simplify(pts, tol):
    """Douglas-Peucker on projected points."""
    if len(pts) < 3:
        return pts
    keep, stack = {0, len(pts) - 1}, [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        best, idx = 0, None
        for i in range(a + 1, b):
            # a closed ring starts and ends on the same point: measure from that point instead
            d = abs(dy * (pts[i][0] - ax) - dx * (pts[i][1] - ay)) / n if n > 1e-9 else math.hypot(pts[i][0] - ax, pts[i][1] - ay)
            if d > best:
                best, idx = d, i
        if idx is not None and best > tol:
            keep.add(idx)
            stack += [(a, idx), (idx, b)]
    return [pts[i] for i in sorted(keep)]

def build(key):
    title, ccs, names, pad = MAPS[key]
    pick = []
    for n in names:
        hit = [f for f in regions if f["properties"]["name"] == n and f["properties"]["country"] in ccs]
        if not hit:
            raise SystemExit("no region %r for map %s" % (n, key))
        pick.append(hit[0])
    xs = [c[0] for f in pick for r in rings(f["geometry"]) for c in r]
    ys = [c[1] for f in pick for r in rings(f["geometry"]) for c in r]
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    k = math.cos(math.radians((y0 + y1) / 2))
    s = W / ((x1 - x0) * k)
    H = round((y1 - y0) * s)
    proj = lambda c: ((c[0] - x0) * k * s, (y1 - c[1]) * s)
    inside = lambda r: any(x0 <= c[0] <= x1 and y0 <= c[1] <= y1 for c in r)

    def path(geom, tol, close):
        out = []
        for r in rings(geom):
            if not inside(r):
                continue
            pts = simplify([proj(c) for c in r], tol)
            if len(pts) < (3 if close else 2):
                continue
            out.append("M" + "L".join("%.0f,%.0f" % p for p in pts) + ("Z" if close else ""))
        return "".join(out)

    land = "".join(path(f["geometry"], 1.0, True) for f in countries)
    riv = "".join(path(f["geometry"], 0.8, False) for f in rivers if f["properties"].get("wine"))
    chosen = {id(f) for f in pick}
    other = "".join(path(f["geometry"], 1.5, True) for f in regions
                    if id(f) not in chosen and f["properties"]["country"] in ccs)
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Map of %s">' % (W, H, title),
             '<rect class="m-sea" width="%d" height="%d"/>' % (W, H),
             '<path class="m-land" d="%s"/>' % land]
    if other:
        parts.append('<path class="m-other" d="%s"/>' % other)
    for f in pick:
        parts.append('<path class="m-reg" d="%s"/>' % path(f["geometry"], 1.0, True))
    if riv:
        parts.append('<path class="m-riv" d="%s"/>' % riv)
    legend = []
    mk = max(1.0, H / 560)  # tall maps are scaled down to fit the page, so their markers are drawn larger
    for i, f in enumerate(pick, 1):
        lx, ly = proj(f["properties"]["lp"] if isinstance(f["properties"]["lp"], list) else json.loads(f["properties"]["lp"]))
        lx, ly = min(max(lx, 12), W - 12), min(max(ly, 12), H - 12)
        parts.append('<g class="m-no"><circle cx="%.0f" cy="%.0f" r="%.0f"/><text x="%.0f" y="%.0f" font-size="%.0f">%d</text></g>'
                     % (lx, ly, 10 * mk, lx, ly + 4 * mk, 12 * mk, i))
        legend.append([f["properties"]["name"], f["properties"]["id"]])
    parts.append("</svg>")
    return {"t": title, "svg": "".join(parts), "legend": legend}

os.makedirs(OUT, exist_ok=True)
total = 0
for key in MAPS:
    js = "MAPDATA[%s]=%s;\n" % (json.dumps(key), json.dumps(build(key), ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(OUT, key + ".js"), "w", encoding="utf-8").write(js)
    total += len(js.encode())
open(os.path.join(ROOT, "assets/js/data/maps-index.js"), "w", encoding="utf-8").write(
    "// Generated by tools/build_lesson_maps.py. Do not edit by hand.\nconst LESSON_MAPS=%s;\nconst MAPDATA={};\n"
    % json.dumps(LESSONS, separators=(",", ":")))
print("%d maps, %d lessons, %.0f KB in all, largest %.0f KB" % (
    len(MAPS), len(LESSONS), total / 1024, max(os.path.getsize(os.path.join(OUT, k + ".js")) for k in MAPS) / 1024))
