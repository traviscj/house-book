# House book data contract

One engine (`engine/`), one data directory per house (`examples/<slug>/` or anywhere with a `data.py`).
Build: `./build.sh <slug|dir>` → `<dir>/out/<PREFIX>-Book-{full,share}.pdf` (+ `<PREFIX>-Panel-Labels.pdf` when
`PANELS` exists) + a GPS-stripped photo/manual web package (`<PREFIX>-photos.zip`).
The worked example is `examples/maple-court/` (fictional). Copy it and replace the data.

## Layout of a house directory
```
data.py                 # single entry point; may exec() sibling data_*.py files (the example does)
research/*.md           # optional raw notes per source (email.md, scans.md, photos.md, ...): not rendered
research/manuals.csv    # file,system,equipment,maker,model,doc_type,source_url,pages,model_match,notes
photos/orig/<group>/<YYYY-MM-DD>_<category>_<desc>.jpg   # originals (any of jpg/png/heic); never published as-is
manuals/<system>__<maker>-<model>__<doctype>.pdf
docs/paperless/<date>_<vendor>_<title>_<docid>.pdf       # optional scanned-document exports → Document Index
```
A photo is referenced in data by its *derived* name: its path under `photos/orig` with `/`→`__`, extension `.jpg`.
`photos/orig/session/sump-pit.png` → `"session__sump-pit.jpg"`.

Generated and safe to delete: `tex/`, `out/`, `photos/{print,web,publish}/`.

## data.py top-level names (all optional unless marked *)
Strings support `**bold**`, `` `mono` ``, `"quotes"`, `→`. They are plain text, NOT LaTeX: `gen.py` escapes
`$ % & # _ { } ~ ^ \`. The exception is `PROSE`, whose values are raw LaTeX.

```python
META = dict(*                          # cover, headers, filenames
  slug="maple-court", title="17 Maple Court", place="Anytown, USA 00000",
  kind="Two-story colonial · 4 bed / 2.5 bath",    # cover subtitle line
  book="HOUSE BOOK",                               # cover kicker + running header
  span="June 2018 — October 2026",                 # ownership window on the cover
  since=2018,                                      # first year of ownership (timeline, cost chart)
  asof="2026-10-01",                               # build date; warranty pills are computed against it (default: today)
  prefix="17-Maple-Court",                         # output filename prefix
  cover="session/cover.png",                       # path under photos/orig; cropped to 8.5×6.4 in
  blurb="Systems · panels · quirks · ...",
  author="", ask="ALEX")                           # PDF author; paperwork="ask" renders an "ASK <ask>" pill
FACTS = [("Address", "..."), ("Built", "..."), ...]                      # * key/value, At a Glance
EMERGENCY = [("Water leak", "main shutoff is ..."), ...]                 # shutoffs + who to call
SYSTEMS = [dict(title, intro=None, rows=[(k, v)], bullets=[], photos=[(file, caption)], per_row=3, raw=None)]
PROJECTS = [dict(short, cat, title, vendor, date, cost, paid=None, scope=[], notes=None, warranty=None,
                 paperwork="have|partial|missing|ask", chase=None, photos=[(file, caption)], per_row=3,
                 exclude=False, sources=[], docs=None)]
       # cat ∈ Exterior|Structural|Interior|Unit turnover|Mechanical|Landscape|... (timeline swimlanes)
       # chase = who most likely holds the missing paper → Paperwork to Chase chapter (full edition)
       # exclude=True = shown greyed out, left out of every total (e.g. an invoice for a different address)
QUIRKS = [dict(title, symptom, cause, fix, src)]
PROVIDERS = [dict(name, trade, contact, work, when)]
WARRANTIES = [dict(item, who, term, start, expiry, paperwork)]  # expiry ISO or None; "2099-12-31" = lifetime
INVOICES = [dict(date, vendor, what, amount, where)]            # where = your citation code for the proof
ACTIONS = [dict(title, value, why, how, conf, src)]             # "Money & Risk on the Table" (full edition only)
COMPLIANCE = [dict(item, authority, status, last, next, notes)] # status: ok|due|overdue|unknown|na
OPEN_ISSUES = [(kind, text)]       # kind ∈ safety|envelope|mechanical|plumbing|comfort|paperwork|planned
PLANNED = [dict(title, why, plan)]
MAINTENANCE = [dict(when, task, why)]
NAMEPLATE_WALK = [(item, where_to_look, why)]
DRIVE_DOCS = [(title, doc_id, what)]                            # extra rows for the Document Index
FINANCE = dict(rows=[(k, v)], taxes=[(tax_year, pin, amount, notes)])   # full edition only
TIMELINE_EXTRA = [(date, label)]   # non-project milestones on the timeline
PHOTO_META = {stem: dict(date, caption, category, project, source)}     # web gallery: only captioned photos publish
WEB_EXCLUDE = ["substr", ...]      # photo stems never published to the web gallery (plans, receipts, screenshots)
WEB_NAMES = ["Sam", ...]           # people's names scrubbed from web captions
PROSE = dict(intro="", panels_intro="", panel_demand="", drawings="", receipts_intro="",
             compliance_intro="", finance_intro="", open_extra="")    # raw LaTeX fragments
# rentals / multi-unit buildings
UNITS = [dict(unit, floor, layout, systems, features, status, notes, photos=[], tenants=[dict(name, start, end, rent, notes)],
              private_fields=["status", "notes"])]              # tenants always dropped from the share edition
REVENUE = [(year, gross, notes)]                                # full edition only
```

### Electrical panels
```python
PANELS = [dict(id="M", title="MAIN PANEL", desc="...", slots=40, main=200,
               fed=False,          # True: `main` is a feed breaker, not a main (label text says "feed")
               gen_kw=None,        # set on a generator-backed panel → generator headroom check
               banner=None,        # optional black banner on the printable door label
               rows=[(slot, amps, poles, circuit, protection, note)])]
PANEL_DATE = "2026-09-20"; PANEL_SPARE = ["M"]; PANEL_NOTE = "footnote under the load table"
```
`amps` is a string so uncertainty survives: `"15?"` prints as-is and parses as 15. A 2-pole row occupies `slot` and
`slot+2`. A 2-pole whose circuit name contains `GENERATOR` is treated as the feed to a generator subpanel.
Leg assignment is by row parity (slots 1–2 = leg A, 3–4 = B, ...). The engine renders the directory, a per-leg
connected-capacity table, and one printable letter-size door label per panel.

```python
DEMAND = dict(sqft, small_appliance=2, laundry=1, volts=240, service_amps=200,
              appliances=[(name, VA)],        # "(~)" in the name = typical value, no nameplate yet
              cool=[(name, VA)], heat=[(name, VA, factor)],
              measured=[(label, kW)], note="")
```
Renders an NEC 220.82 (optional method, dwelling) demand estimate: general loads at 100 % of the first 10 kVA and
40 % of the rest, plus the larger of cooling or heating, compared with the service rating and any measured peaks.
It's a planning estimate, not a stamped load calculation.

## Two editions
`EDITION=full|share` is set by `build.sh`. The share edition is for contractors, house-sitters, buyers.
- Any dict row with `private=True` is dropped from the share edition.
- Any tuple row (FACTS, EMERGENCY, OPEN_ISSUES, ...) ending in a trailing `True` is private.
- ACTIONS, FINANCE, REVENUE, UNITS[].tenants, the Paperwork to Chase chapter and the Document Index are full-only.
- PROSE is printed in both; wrap private prose in `\ifprivate ... \fi`.

## Rules that keep the book trustworthy
- **Every fact carries a source.** Projects cite where the proof lives; invoices say where they're filed. Mark
  inference `(inf)` or `?`.
- **Keep uncertainty in the data.** `"15?"` and "verify" notes print, so the next person with a flashlight knows.
- **Attribute by address evidence.** Vendors who work on several properties produce invoices that get filed under the
  wrong one. When in doubt, `exclude=True` with a note.
- **Write current state.** Edit the row; don't append "correction:" text after stale text.
- **Privacy:** never record passwords, door/alarm/lockbox codes, Wi-Fi keys, or full account/policy/loan numbers
  (last 4 at most). No photos of people. `photos.py` strips EXIF/GPS from every derivative; `WEB_EXCLUDE` keeps plans,
  receipts and screenshots out of the web gallery.
