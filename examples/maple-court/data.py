# 17 Maple Court: a FICTIONAL example house. Every name, address, vendor, phone number, serial number,
# amount and date in examples/maple-court/ is invented. Phone numbers use the reserved 555-01xx range.
# Single entry point for the engine (contract: ../../SCHEMA.md); long lists live in the sibling data_*.py files.
# Citation codes used in this example: E = email thread, S = scanned document id, M = text message, D = drive doc,
# N = nameplate photo, B = bank/card statement.
import pathlib as _pl

META = dict(
    slug="maple-court", title="17 Maple Court", place="Anytown, USA 00000",
    kind="Two-story colonial · 4 bed / 2.5 bath · built 1994",
    book="HOUSE BOOK", span="June 2018 — October 2026", since=2018, prefix="17-Maple-Court",
    asof="2026-10-01",                      # fixed build date: warranty pills + ages are computed against it
    cover="session/cover-front-elevation.png",
    blurb="Systems · panels · quirks · providers · warranties · invoices · paperwork",
    author="The owners of 17 Maple Court (fictional)",
    ask="ALEX",                             # paperwork="ask" pill reads ASK ALEX
)

FACTS = [
    ("Address", "17 Maple Court, Anytown · cul-de-sac lot, house faces south · attached 2-car garage on the east"),
    ("Built", "1994 (tract builder, 3rd phase of the subdivision) · 2×6 exterior walls, vinyl siding over OSB · full unfinished basement, poured walls"),
    ("Size", "~2,450 sq ft above grade (1st 1,250 + 2nd 1,200) · basement ~1,150 sq ft unfinished · lot ~0.31 acre"),
    ("Bought", "2018-06-15 from the original owners (24 years in the house); seller's info sheet + 2018 inspection are the baseline for everything here"),
    ("Owners", "Sam & Alex Example · title as joint tenants · Alex handles the contractor paperwork for exterior jobs", True),
    ("Parcel", "PIN 00-00-000-017 (example) · residential class · homeowner exemption on file only from TY2022 (see Money & Risk)", True),
    ("HVAC", "Two independent zones, both gas furnace + split A/C: zone 1 = basement furnace serving 1st floor + basement; zone 2 = attic furnace serving the 2nd floor (replaced 2020)"),
    ("Electric", "200 A overhead service · Square D Homeline 40-space main panel in the basement · 22 kW standby generator → 100 A automatic transfer switch → 12-circuit generator subpanel"),
    ("Water", "Municipal water + sewer · 1\" copper service, shutoff on the basement north wall · 40-gal gas power-vent water heater (2025) · sump pit with primary + battery-backup pumps"),
    ("Roof", "Architectural asphalt shingles, full tear-off 2019 · ridge vent + soffit intake · 6\" aluminum gutters"),
]

EMERGENCY = [
    ("Water leak", "Main shutoff: basement north wall, behind the water heater, red-handled ball valve (quarter turn). Then Dry Basin Plumbing 555-0142."),
    ("Basement water", "Check the sump pit (basement SE corner). Primary pump on generator circuit G-5; the battery backup alarms on its own. If both are running and losing, call Dry Basin and start a wet-vac."),
    ("Gas smell", "Leave the house, then call the gas utility and 911 from outside. Meter + shutoff on the west wall by the AC pad."),
    ("No heat / no cool", "Thermostat batteries → furnace switch (light switch on the furnace) → filter → breaker (furnaces are on the generator subpanel: G-1 zone 1, G-3 zone 2). Then Acme Heating & Cooling 555-0117 with zone number + model from the Systems chapter."),
    ("Power out", "Generator starts in ~10 s and carries only the generator subpanel (see the panel directory). EV charger, both A/C condensers and the kitchen countertops are NOT backed."),
    ("Fire / CO", "911. Interconnected smoke/CO on every floor (2-yr-old units, replaced 2024). The power-vent water heater and both furnaces share the basement mechanical area."),
    ("Alarm / locks", "Alarm and keypad codes live in the password manager entry \"house access\", never on paper.", True),
]

for _f in ("data_systems.py", "data_projects.py", "data_ops.py"):
    exec((_pl.Path(__file__).parent / _f).read_text())
