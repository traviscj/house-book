# exec'd from data.py: ACTIONS, COMPLIANCE, FINANCE, OPEN_ISSUES, PLANNED, MAINTENANCE, NAMEPLATE_WALK,
# DRIVE_DOCS, TIMELINE_EXTRA, PHOTO_META, PROSE. Fictional.

ACTIONS = [   # "Money & risk on the table": full edition only
 dict(title="Claim the homeowner exemption refund for TY2019–2021", value="≈ $2,700",
      why="The exemption first appears on the TY2022 bill. The deed was recorded late (2018-07) and the application was never filed for the first three tax years; at this county's rate it's worth about $900/yr.",
      how="File a certificate-of-error request with the county assessor for each year (they accept up to 3 prior years) with the deed and proof of residency (driver's license with this address, a 2019 utility bill).",
      conf="High: the TY2019–21 bills show no exemption line; TY2022 does.", src="S tax bills 2019–2022"),
 dict(title="File the patio settling claim before 2027-04-30", value="≈ $1,500 repair",
      why="Greenway's contract warrants against settling over 1/2 in for 3 years. The low spot by the NE downspout measured ~3/4 in under a straightedge in 2026-05.",
      how="Photograph with a level + tape in frame, email Greenway citing the warranty clause, and keep the downspout extension disconnected until they look.",
      conf="High: warranty clause in the signed contract.", src="E 2024-03 contract · photo 2026-05"),
 dict(title="Find the zone 1 leak before buying refrigerant again", value="$400/yr → or a $2,900 coil",
      why="Two top-offs in two summers (5 lb total). The 2024 visit added UV dye specifically so the leak could be found 30 days later; nobody went back. Topping off a leaking 2012 system every summer is the most expensive option.",
      how="Book Acme for a UV inspection (coil, line-set flares, service valves) on the next cooling-season visit. If it's the evaporator coil, price a coil vs a full zone 1 replacement before signing.",
      conf="Medium: the leak location is unknown; the trend isn't.", src="E Acme 2024-07-16, 2024-10-09, 2026-06-23"),
 dict(title="Get the roof's manufacturer warranty registration", value="system warranty",
      why="The 2019 contract sells an enhanced manufacturer system warranty, which is only valid if the contractor registered the job. Without the certificate, a shingle defect claim falls back to the basic material warranty.",
      how="Ask Summit Roofing's office for the registration certificate (job address, install date). If it was never registered, ask whether late registration is still possible.",
      conf="Medium: the absence of a certificate isn't proof it wasn't registered.", src="E 2019-04-02 contract"),
 dict(title="Re-attribute the $6,850 gutter invoice", value="$6,850 out of the cost basis",
      why="The 2022 Summit invoice is for 71 Maple Court. It was in this house's improvement total, which overstates the cost basis.",
      how="Move it out of this house's records (already excluded from every total in this book); forward it to the neighbor if they ask.",
      conf="High: the address line on the invoice.", src="S 0310"),
]

COMPLIANCE = [
 dict(item="Smoke + CO alarms", authority="local fire code", status="ok", last="2024-01-12", next="2034-01", notes="Interconnected, replaced 2024 (10-yr sealed batteries). Test monthly."),
 dict(item="Radon retest", authority="state guidance", status="due", last="2018-09-04", next="2020-09", notes="Retest every 2 years after mitigation and after major HVAC changes; nothing since the post-mitigation test."),
 dict(item="Generator permits", authority="building dept", status="ok", last="2021-12-03", next="", notes="Electrical + gas permits closed; final sticker inside the transfer switch door."),
 dict(item="EV circuit permit", authority="building dept", status="ok", last="2023-04-06", next="", notes="Closed."),
 dict(item="Backflow (lawn irrigation)", authority="water utility", status="na", last="", next="", notes="No irrigation system; utility confirmed no device required."),
 dict(item="Deck permit", authority="building dept", status="unknown", last="", next="", notes="Deckworks said they pulled one; no permit number in any document. Check the building dept's online permit search."),
 dict(item="Homeowner exemption", authority="county assessor", status="overdue", last="TY2022", next="", notes="Missing TY2019–21 (see Money & Risk).", private=True),
 dict(item="Chimney inspection", authority="NFPA 211 (advisory)", status="overdue", last="2018-07-02", next="2019-07", notes="Fireplace used ~10×/yr; annual inspection recommended."),
]

FINANCE = dict(rows=[
    ("Purchase", "2018-06-15 · price and closing statement in the drive folder (example data, not reproduced)"),
    ("Insurance", "HO-3, policy …0000 (example); water backup / sump endorsement added 2021 after the float failure: confirm limit ≥ the basement contents"),
    ("Cost basis adds", "Best-estimate improvements in this book; the 2022 gutter invoice is excluded"),
], taxes=[
    ("TY2019", "00-00-000-017", "no exemption", "exemption not applied"),
    ("TY2020", "00-00-000-017", "no exemption", "exemption not applied"),
    ("TY2021", "00-00-000-017", "no exemption", "exemption not applied"),
    ("TY2022", "00-00-000-017", "exemption applied", "first year with the homeowner exemption"),
])

OPEN_ISSUES = [
 ("safety", "Radon retest overdue since 2020; the 2020 HVAC replacement changed basement pressure."),
 ("safety", "Panel M-37 (smoke/CO) handle rating unreadable: verify it's 15 A, not 20 A on 14 AWG."),
 ("mechanical", "Zone 1 A/C leaking refrigerant (5 lb over two summers); leak not located."),
 ("mechanical", "Zone 1 furnace + A/C are 2012 equipment; the seller sheet's capacities were wrong (nameplate: 80k / 3.5 t)."),
 ("envelope", "Six original 1994 window units show early seal fogging."),
 ("envelope", "Patio low spot by the NE downspout; under installer warranty until 2027-04-30."),
 ("paperwork", "Roof manufacturer warranty registration, deck change order + permit number, Clearview invoice, paint balance."),
 ("comfort", "Bedroom 4 (over the garage) runs 3–4 °F warmer than the rest of zone 2 in summer."),
 ("planned", "Zone 1 replacement decision (see the project queue)."),
]

PLANNED = [
 dict(title="Zone 1 HVAC: repair or replace", why="Leaking 2012 system, two top-offs, a $2,900 coil quote on the table.",
      plan="UV leak search first. If it's the coil, get a full-replacement quote sized from a load calc (the seller's 4-ton claim was wrong; it's 3.5 t now and may only need 3). Consider a heat pump: the dead 30 A dryer circuit and 200 A demand headroom both allow it."),
 dict(title="Re-glaze or replace the remaining six windows", why="Early seal failure on six 1994 units.",
      plan="Price IGU-only replacement (Clearview) against full inserts. IGU-only keeps the frames and costs ~30 % as much."),
 dict(title="Bedroom 4 comfort", why="Room over the garage, warmer in summer.",
      plan="Check the duct run in the garage ceiling for disconnection first; then a balancing damper. Mini-split only if both fail."),
]

MAINTENANCE = [
 dict(when="Monthly", task="Test smoke/CO alarms; check the radon manometer (liquid offset, not level)", why="A level manometer = fan stopped."),
 dict(when="Every 90 days", task="Zone 2 filter, 20×20×1 at the attic return", why="Reachable through the bedroom 4 closet hatch."),
 dict(when="Every 6 months", task="Zone 1 media filter, 16×25×4", why="Basement cabinet next to the furnace."),
 dict(when="March", task="Generator annual service (GenReady)", why="Oil, filter, plugs, battery load test."),
 dict(when="April", task="Clear the condenser fins + level the pads; confirm both A/C zones before the first hot week", why="Zone 1 is the known leaker."),
 dict(when="May", task="Gutters + downspout extensions; check the patio for settling", why="Patio warranty claims need dated photos."),
 dict(when="October", task="HVAC fall tune-up, both zones (Acme)", why="Ask for the zone 1 UV dye check until the leak is found."),
 dict(when="October", task="Bucket test both sump pumps; press the backup's battery test", why="The 2021 failure was a stuck float."),
 dict(when="November", task="Shut and drain the hose bibs from inside (frost-free, but disconnect hoses)", why="A frost-free bib with a hose attached still splits."),
 dict(when="Every 2 years", task="Radon retest (short-term kit, basement, closed-house conditions)", why="Overdue since 2020."),
 dict(when="Every 5 years", task="Sump backup battery", why="Last 2025-10."),
 dict(when="Annually", task="Chimney inspection before the first fire", why="Last 2018."),
]

NAMEPLATE_WALK = [
 ("Zone 1 condenser", "east side yard, left unit, label on the back corner", "confirm 3.5 t and the factory charge for the leak math"),
 ("Main panel catalog label", "inside the door, lower left", "confirm copper bus and the max-breaker-space count"),
 ("Dishwasher", "inside the door edge", "model for the manuals table"),
 ("Garage door opener", "on the motor head", "model + horsepower (it's on the generator)"),
 ("Breaker M-37", "main panel, left column, near the bottom", "handle rating unreadable in the photo"),
]

DRIVE_DOCS = [
 ("2018 home inspection", "EXAMPLE-DOC-01", "baseline condition; note on the dryer circuit"),
 ("Seller's info sheet", "EXAMPLE-DOC-02", "the (wrong) zone 1 capacities"),
 ("Closing statement", "EXAMPLE-DOC-03", "purchase + transfer date"),
 ("Generator permit set", "EXAMPLE-DOC-04", "single-line diagram + load list"),
]

TIMELINE_EXTRA = [("2018-06-15", "Bought"), ("2023-02-23", "Ice storm, 31 h on generator")]

PHOTO_META = {f"session__{k}": dict(date=d, caption=c, category=cat, project=pr, source="illustration") for k, d, c, cat, pr in [
 ("cover-front-elevation", "2026-09-01", "Front elevation (illustration)", "exterior", ""),
 ("hvac-main-furnace", "2026-09-20", "Zone 1 furnace, basement", "hvac", ""),
 ("hvac-upstairs-furnace", "2020-04-22", "Zone 2 furnace, attic", "hvac", "Zone 2 HVAC"),
 ("hvac-condensers", "2026-09-20", "Both condensers, east side yard", "hvac", ""),
 ("water-heater", "2025-02-10", "Power-vent water heater", "plumbing", "Water heater"),
 ("sump-pit", "2021-05-03", "Sump pit, primary + backup", "plumbing", "Sump"),
 ("panel-main-door", "2026-09-20", "Main panel", "electrical", ""),
 ("panel-gen-door", "2026-09-20", "Generator subpanel", "electrical", "Generator"),
 ("generator", "2021-11-15", "Standby generator", "electrical", "Generator"),
 ("transfer-switch", "2021-11-15", "Transfer switch", "electrical", "Generator"),
 ("roof-2019", "2019-05-14", "Roof after tear-off", "exterior", "Roof"),
 ("window-seal", "2023-06-12", "Fogged glass, dining room", "exterior", "IGUs"),
 ("patio-settling", "2026-05-18", "Patio settling by the downspout", "exterior", "Patio"),
 ("attic-insulation", "2019-10-03", "Attic after blow-in", "interior", "Attic R-49"),
 ("deck-boards", "2020-08-10", "Composite deck", "exterior", "Deck"),
]}
WEB_EXCLUDE = ["plan-"]   # floor plans stay out of the public web gallery
WEB_NAMES = ["Sam", "Alex"]

PROSE = dict(
intro=r"""This book is the house's documentation, generated from data: every system, circuit, repair, warranty and invoice, each with a pointer to where the proof lives. It exists so that the next furnace call, insurance claim, contractor bid or sale starts from facts instead of memory. \textbf{17 Maple Court is fictional}: it's the example that ships with the engine.\par""",
panels_intro=r"""One 200\,A Square~D panel (\textbf{M}) and a 12-space generator subpanel (\textbf{G}) behind a 100\,A automatic transfer switch, fed from M's 60\,A two-pole in slots 1--3. Directories were transcribed from door photos (\PANELDATE) and checked against each handle rating. One rating is unreadable and is marked with a~? until someone looks with a flashlight.\par""".replace(r"\PANELDATE", "2026-09-20"),
panel_demand=r"""\par\smallskip{\small Connected capacity on panel~M is well over the 200\,A main, which is normal. The demand estimate below is the number that matters for new loads, and the generator check is the real constraint: panel~G's worst leg is connected at about 1.4$\times$ the generator's per-leg output, so the furnaces, sump and refrigerator starting together after an outage is the case to watch.}\par""",
drawings=r"""No permit drawings survive from the 1994 build; these sketches were drawn from the 2018 inspection report and a tape measure. They show room names, not circuits; the panel chapter is the circuit map.
\par\medskip\noindent
\includegraphics[width=\linewidth]{session__plan-first-floor.jpg}\par{\sffamily\scriptsize\color{slate}First floor. Main water shutoff is directly below the laundry, on the basement north wall.}\par\medskip
\noindent\includegraphics[width=\linewidth]{session__plan-second-floor.jpg}\par{\sffamily\scriptsize\color{slate}Second floor. Zone 2 attic access is the hatch in the bedroom 4 closet.}\par""",
)
