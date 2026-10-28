#!/usr/bin/env python3
"""Draw the example's illustrations (no real photos anywhere in this repo).
SVG -> PNG via rsvg-convert (librsvg) into photos/orig/session/. Rerun after editing; build.sh picks the PNGs up."""
import pathlib, subprocess, html

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "photos/orig/session"; OUT.mkdir(parents=True, exist_ok=True)
INK, BRICK, SLATE, RULE, WASH = "#16181D", "#9B2C1C", "#4A5563", "#C9CDD3", "#F3F1EC"
FONT = "Helvetica, Arial, sans-serif"

def save(name, w, h, body, bg=WASH):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    src = OUT / f"{name}.svg"; src.write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(OUT / f"{name}.png"), str(src)], check=True)
    src.unlink()

def t(x, y, s, size=28, fill=INK, anchor="start", weight="normal"):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>'

def stamp(w, h):   # every image says what it is
    return (f'<rect x="{w-430}" y="{h-58}" width="410" height="40" fill="{INK}" opacity="0.85"/>'
            + t(w - 225, h - 30, "ILLUSTRATION · FICTIONAL HOUSE", 20, "#fff", "middle", "bold"))

# ---- cover: front elevation of a 1990s two-story with an attached two-car garage
def window(x, y, w=90, h=120):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#DDE6EE" stroke="{INK}" stroke-width="5"/>'
            f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="{INK}" stroke-width="3"/>'
            f'<line x1="{x}" y1="{y+h/2}" x2="{x+w}" y2="{y+h/2}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x-22}" y="{y}" width="18" height="{h}" fill="{SLATE}"/><rect x="{x+w+4}" y="{y}" width="18" height="{h}" fill="{SLATE}"/>')
W, H = 2550, 1920
b = [f'<rect width="{W}" height="{H*0.72}" fill="#C8D7E3"/>', f'<rect y="{H*0.72}" width="{W}" height="{H*0.28}" fill="#8FA77E"/>',
     f'<rect x="1080" y="1380" width="1400" height="10" fill="{SLATE}" opacity="0.3"/>']
# main block
b += [f'<rect x="420" y="620" width="1180" height="770" fill="#EDE6D6" stroke="{INK}" stroke-width="6"/>',
      f'<polygon points="360,630 1010,300 1660,630" fill="#5B5F66" stroke="{INK}" stroke-width="6"/>',
      f'<rect x="1300" y="330" width="90" height="200" fill="{BRICK}" stroke="{INK}" stroke-width="5"/>']
for x in (520, 760, 1170, 1410): b.append(window(x, 690))
for x in (520, 760, 1410): b.append(window(x, 1040))
b += [f'<rect x="1150" y="1050" width="150" height="340" fill="{BRICK}" stroke="{INK}" stroke-width="5"/>',
      f'<circle cx="1275" cy="1230" r="9" fill="#E8C66A"/>',
      f'<polygon points="1100,1050 1225,960 1350,1050" fill="#5B5F66" stroke="{INK}" stroke-width="5"/>']
# garage wing
b += [f'<rect x="1600" y="900" width="760" height="490" fill="#EDE6D6" stroke="{INK}" stroke-width="6"/>',
      f'<polygon points="1560,910 1980,700 2400,910" fill="#5B5F66" stroke="{INK}" stroke-width="6"/>']
for x in (1660, 2010):
    b.append(f'<rect x="{x}" y="1080" width="300" height="310" fill="#F7F4EC" stroke="{INK}" stroke-width="5"/>')
    b += [f'<line x1="{x}" y1="{1080+k*62}" x2="{x+300}" y2="{1080+k*62}" stroke="{RULE}" stroke-width="4"/>' for k in range(1, 5)]
b += [f'<rect x="0" y="1390" width="{W}" height="14" fill="{INK}" opacity="0.4"/>',
      f'<rect x="1640" y="1404" width="720" height="516" fill="#B9B6AE"/>',
      stamp(W, H)]
save("cover-front-elevation", W, H, "".join(b))

# ---- floor plans (drawings chapter)
def plan(name, title, rooms, extra=""):
    w, h = 2200, 1400
    s = [f'<rect x="100" y="150" width="2000" height="1150" fill="#fff" stroke="{INK}" stroke-width="14"/>', t(100, 110, title, 48, INK, weight="bold")]
    for (x, y, rw, rh, lab, sub) in rooms:
        s.append(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" fill="none" stroke="{INK}" stroke-width="6"/>')
        s.append(t(x + rw / 2, y + rh / 2, lab, 34, INK, "middle", "bold"))
        if sub: s.append(t(x + rw / 2, y + rh / 2 + 42, sub, 24, SLATE, "middle"))
    save(name, w, h, "".join(s) + extra + stamp(w, h), bg="#fff")
plan("plan-first-floor", "FIRST FLOOR · ~1,250 sq ft (garage not counted)", [
    (100, 150, 700, 560, "Living room", "13'×18'"), (800, 150, 600, 560, "Dining", "12'×13'"),
    (1400, 150, 700, 560, "Kitchen", "16'×13' · gas range"), (100, 710, 520, 590, "Family room", "15'×16' · fireplace"),
    (620, 710, 360, 590, "Foyer + stair", ""), (980, 710, 420, 300, "Powder", ""), (980, 1010, 420, 290, "Laundry", "dryer: gas"),
    (1400, 710, 700, 590, "Office / den", "door to garage")],
    f'<circle cx="1000" cy="1275" r="12" fill="{BRICK}"/>' + t(1020, 1283, "main water shutoff (basement, below)", 20, BRICK))
plan("plan-second-floor", "SECOND FLOOR · ~1,200 sq ft", [
    (100, 150, 800, 620, "Primary bedroom", "14'×17'"), (900, 150, 500, 620, "Primary bath", "+ walk-in closet"),
    (1400, 150, 700, 620, "Bedroom 2", "11'×13'"), (100, 770, 650, 530, "Bedroom 3", "11'×12'"),
    (750, 770, 450, 530, "Hall bath", ""), (1200, 770, 900, 530, "Bedroom 4", "11'×14' · attic hatch in closet")])

# ---- placeholder "photo" cards: a pictogram + caption
def card(name, label, sub, glyph):
    w, h = 1600, 1200
    body = (f'<rect x="30" y="30" width="{w-60}" height="{h-60}" fill="none" stroke="{RULE}" stroke-width="6" stroke-dasharray="24 14"/>'
            + glyph + t(w / 2, 1000, label, 56, INK, "middle", "bold") + t(w / 2, 1060, sub, 32, SLATE, "middle") + stamp(w, h))
    save(name, w, h, body)
g = lambda s: f'<g stroke="{INK}" stroke-width="10" fill="none">{s}</g>'
FURN = g('<rect x="620" y="200" width="360" height="620" rx="12"/><rect x="680" y="280" width="240" height="160"/><line x1="680" y1="560" x2="920" y2="560"/><line x1="680" y1="620" x2="920" y2="620"/><line x1="800" y1="200" x2="800" y2="120"/><line x1="800" y1="120" x2="1100" y2="120"/>')
COND = g('<rect x="560" y="300" width="480" height="480" rx="16"/><circle cx="800" cy="540" r="170"/><line x1="800" y1="370" x2="800" y2="710"/><line x1="630" y1="540" x2="970" y2="540"/><line x1="1040" y1="400" x2="1200" y2="400"/>')
WH = g('<rect x="650" y="220" width="300" height="600" rx="150"/><line x1="800" y1="220" x2="800" y2="120"/><rect x="740" y="640" width="120" height="80"/>')
SUMP = g(f'<ellipse cx="800" cy="300" rx="300" ry="60"/><line x1="500" y1="300" x2="500" y2="820"/><line x1="1100" y1="300" x2="1100" y2="820"/><path d="M500 820 Q800 900 1100 820"/><rect x="720" y="600" width="160" height="200"/><line x1="800" y1="600" x2="800" y2="160"/><line x1="800" y1="160" x2="1200" y2="160"/>') + f'<path d="M500 700 Q800 740 1100 700" stroke="#3B6EA5" stroke-width="8" fill="none"/>'
PANEL = g('<rect x="560" y="140" width="480" height="720"/>' + "".join(f'<rect x="{x}" y="{240+k*52}" width="150" height="34"/>' for k in range(11) for x in (610, 840)) + '<rect x="700" y="160" width="200" height="60"/>')
GEN = g('<rect x="480" y="320" width="640" height="460" rx="20"/>' + "".join(f'<line x1="{x}" y1="400" x2="{x}" y2="700"/>' for x in range(560, 1100, 60)) + '<line x1="480" y1="780" x2="440" y2="840"/><line x1="1120" y1="780" x2="1160" y2="840"/>')
ROOF = g('<polygon points="300,700 800,250 1300,700"/>' + "".join(f'<line x1="{300+k*55}" y1="{700-k*50}" x2="{1300-k*55}" y2="{700-k*50}"/>' for k in range(1, 9)) + '<rect x="980" y="330" width="80" height="140"/>')
WIN = g('<rect x="560" y="200" width="480" height="620"/><line x1="800" y1="200" x2="800" y2="820"/><line x1="560" y1="510" x2="1040" y2="510"/>') + f'<path d="M600 560 L700 520" stroke="{BRICK}" stroke-width="8"/>'
PATIO = g("".join(f'<rect x="{360+c*180+(r%2)*90}" y="{300+r*110}" width="170" height="100"/>' for r in range(5) for c in range(5))) + f'<ellipse cx="800" cy="560" rx="260" ry="120" fill="{BRICK}" opacity="0.18"/>'
ATTIC = g('<polygon points="300,820 800,260 1300,820"/>' + "".join(f'<line x1="{x}" y1="820" x2="{x}" y2="{820-(560*(1-abs(x-800)/500))}"/>' for x in range(400, 1250, 100))) + f'<rect x="330" y="740" width="940" height="80" fill="#E8C66A" opacity="0.5"/>'
ATS = g('<rect x="600" y="180" width="400" height="640"/><circle cx="800" cy="360" r="70"/><line x1="800" y1="360" x2="850" y2="310"/><rect x="680" y="560" width="240" height="160"/>')
DECK = g("".join(f'<rect x="300" y="{220+k*70}" width="1000" height="60"/>' for k in range(9))) + f'<rect x="300" y="500" width="1000" height="60" fill="{BRICK}" opacity="0.25"/>'
for n, l, s, gl in [
    ("hvac-upstairs-furnace", "Attic furnace (zone 2)", "nameplate photo goes here", FURN),
    ("hvac-main-furnace", "Basement furnace (zone 1)", "nameplate photo goes here", FURN),
    ("hvac-condensers", "Condensers, east side yard", "zone 1 (left) · zone 2 (right)", COND),
    ("water-heater", "Water heater", "40 gal power-vent, basement", WH),
    ("sump-pit", "Sump pit", "primary + battery backup pump", SUMP),
    ("panel-main-door", "Main panel, door open", "200 A · 40 spaces", PANEL),
    ("panel-gen-door", "Generator subpanel", "12 circuits behind the transfer switch", PANEL),
    ("generator", "Standby generator", "22 kW air-cooled (19.5 kW on natural gas)", GEN),
    ("transfer-switch", "Automatic transfer switch", "next to the main panel", ATS),
    ("roof-2019", "Roof after tear-off", "architectural shingles, 2019", ROOF),
    ("window-seal", "Fogged IGU, dining room", "failed seal, sash 2 of 3", WIN),
    ("patio-settling", "Paver patio settling", "low spot by the downspout", PATIO),
    ("attic-insulation", "Attic after blow-in", "R-49 cellulose over old batts", ATTIC),
    ("deck-boards", "Composite deck", "rebuilt 2020 · composite boards", DECK),
]:
    card(n, l, s, gl)
print("wrote", len(list(OUT.glob("*.png"))), "PNGs to", OUT)
