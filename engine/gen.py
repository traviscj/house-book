#!/usr/bin/env python3
"""$PROP/data.py -> $PROP/tex/{main.tex,preamble.tex,gen/*.tex}. Property-agnostic; data contract in ../SCHEMA.md."""
import datetime as dt, pathlib, re, runpy, os
E = pathlib.Path(__file__).resolve().parent
R = pathlib.Path(os.environ["PROP"]).resolve()
D = runpy.run_path(str(R / "data.py"))
OUT = R / "tex" / "gen"; OUT.mkdir(parents=True, exist_ok=True)
META = D["META"]
TODAY = dt.date.fromisoformat(META["asof"]) if META.get("asof") else dt.date.today()
SINCE = int(META.get("since") or 2020)
for k in ("PROJECTS", "QUIRKS", "PROVIDERS", "WARRANTIES", "INVOICES", "MAINTENANCE", "SYSTEMS", "FACTS", "UNITS", "COMPLIANCE", "OPEN_ISSUES", "PLANNED", "ACTIONS", "NAMEPLATE_WALK", "DRIVE_DOCS", "PANELS", "EMERGENCY", "TIMELINE_EXTRA", "REVENUE"):
    D.setdefault(k, [])
D.setdefault("PROSE", {}); D.setdefault("FINANCE", {})
EDITION = os.environ.get("EDITION", "full")          # full | share
if EDITION == "share":                               # drop private items everywhere
    for k, v in list(D.items()):
        if isinstance(v, list): D[k] = [x for x in v if not (isinstance(x, dict) and x.get("private"))]
    for u in D["UNITS"]:
        u.pop("tenants", None)
        for f in u.get("private_fields", []): u.pop(f, None)
    D["FINANCE"] = {}; D["REVENUE"] = []; D["ACTIONS"] = []
# tuple rows (FACTS, EMERGENCY, OPEN_ISSUES, ...) may carry a trailing True = private: drop in share, strip flag always
for k, v in list(D.items()):
    if isinstance(v, list) and any(isinstance(x, tuple) and len(x) >= 3 and x[-1] is True for x in v):
        D[k] = [x[:-1] if (isinstance(x, tuple) and len(x) >= 3 and x[-1] is True) else x for x in v
                if EDITION == "full" or not (isinstance(x, tuple) and len(x) >= 3 and x[-1] is True)]

def e(s):
    """LaTeX-escape plain text; allow **bold** and `mono`."""
    if s is None: return ""
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")]:
        s = s.replace(a, b)
    s = re.sub(r'(?<![\d.])(\d{1,3}(?:[./]\d+)?)"(?=[\s×x,;:).\-–]|$)', r"\1\\,in", s)   # inch marks (not years) before quote pairing
    s = re.sub(r"`(.+?)`", r"\\texttt{\1}", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r'"(.+?)"', r"``\1''", s)
    s = s.replace("->", r"$\rightarrow$").replace("→", r"$\rightarrow$")
    s = s.replace("▢", r"\tikz[baseline=-0.5pt]\draw[bad,line width=0.7pt](0,0)rectangle(6pt,6pt);").replace("★", r"$\star$")
    return s

def money(v):
    return "—" if v is None else f"\\${v:,.0f}"

def w(name, body): (OUT / f"{name}.tex").write_text(body)

def doc_pill(status):
    return {"have": r"\HAVE", "missing": r"\MISSING", "partial": r"\PARTIAL", "ask": r"\ASK"}.get(status, r"\UNKNOWN")

def warranty_pill(expiry):
    if not expiry: return r"\UNKNOWN"
    try: d = dt.date.fromisoformat(expiry)
    except ValueError: return r"\UNKNOWN"
    if d < TODAY: return r"\EXPIRED"
    if (d - TODAY).days < 365: return r"\SOON"
    return r"\ACTIVE"

def photos_block(ph, per_row=2):
    if not ph: return ""
    width = {1: "0.99", 2: "0.49", 3: "0.325", 4: "0.245"}[per_row]
    out = [r"\par\noindent"]
    for i, (f, cap) in enumerate(ph):
        out.append(rf"\photo[{width}]{{{f}}}{{{e(cap)}}}" + (r"\hfill" if (i + 1) % per_row else r"\par\vspace{4pt}\noindent"))
    return "\n".join(out) + r"\par"

# ---------------- projects
P = sorted(D["PROJECTS"], key=lambda p: p["date"] or "9999")
def best(p): return p.get("paid") if p.get("paid") else p.get("cost")
def costcell(p):
    c, pd = p.get("cost"), p.get("paid")
    if c and pd and abs(c - pd) > 1: return rf"{money(c)} \textcolor{{slate}}{{· paid {money(pd)}}}"
    return money(c if c else pd)
body = []
for p in P:
    title = e(p["title"]) + (r" \pill{bad}{EXCLUDED}" if p.get("exclude") else "")
    body.append(rf"\begin{{projbox}}{{{title}}}")
    body.append(rf"\projmeta{{{e(p['vendor'])}}}{{{e(p['date'] or '?')}}}{{{costcell(p)}}}{{{e(p.get('warranty') or '—')}}}{{{doc_pill(p.get('paperwork'))}}}")
    if p.get("scope"):
        body.append(r"\begin{itemize}" + "".join(rf"\item {e(x)}" for x in p["scope"]) + r"\end{itemize}")
    if p.get("notes"): body.append(r"\par\smallskip{\small " + e(p["notes"]) + r"}")
    body.append(photos_block(p.get("photos", []), p.get("per_row", 3)))
    tail = []
    if p.get("docs"): tail.append("On file: " + p["docs"])
    if p.get("sources"): tail.append("; ".join(p["sources"]))
    if tail: body.append(r"\par\hfill\src{" + e(" · ".join(tail)) + "}")
    body.append(r"\end{projbox}")
w("projects", "\n".join(body))

inc = [p for p in P if not p.get("exclude")]
tot_doc = sum(p.get("cost") or 0 for p in inc)
tot_paid = sum(p.get("paid") or 0 for p in inc)
tot_best = sum(best(p) or 0 for p in inc)
rows = []
for p in P:
    grey = r"\color{slate}" if p.get("exclude") else ""
    rows.append(rf"{grey}\num{{{e(p['date'] or '?')}}} & {grey}{e(p['title'])} & {grey}{e(p['vendor'])} & {grey}{money(p.get('cost'))} & {grey}{money(p.get('paid'))} & {doc_pill(p.get('paperwork'))}\\")
w("ledger", r"\begin{dtab}\begin{longtable}{@{}l>{\RaggedRight}p{2.3in}>{\RaggedRight}p{1.75in}rrc@{}}\toprule" +
  r"\thd{Date}&\thd{Project}&\thd{Vendor}&\thd{Documented}&\thd{Paid (traced)}&\thd{Paperwork}\\\midrule\endhead" + "\n" + "\n".join(rows) +
  rf"\midrule\rowcolor{{white}}&\textbf{{{len(inc)} projects (excl.\ disputed)}}&&\textbf{{{money(tot_doc)}}}&\textbf{{{money(tot_paid)}}}&\\" +
  rf"\rowcolor{{white}}&\textbf{{Best estimate}} {{\scriptsize\color{{slate}}(paid where traced, else documented)}}&&\multicolumn{{2}}{{r}}{{\textbf{{{money(tot_best)}}}}}&\\\bottomrule\end{{longtable}}\end{{dtab}}")
byyear = {}
for p in inc:
    v = best(p)
    if p["date"] and v: byyear[p["date"][:4]] = byyear.get(p["date"][:4], 0) + v
pts = sorted(byyear.items())
w("costchart", r"""\begin{tikzpicture}\begin{axis}[width=\linewidth,height=2.3in,ybar,bar width=16pt,
 symbolic x coords={%s},xtick=data,ymin=0,axis lines*=left,ymajorgrids,grid style={rule},
 yticklabel={\$\pgfmathprintnumber{\tick}k},font=\sffamily\scriptsize,
 nodes near coords={\$\pgfmathprintnumber[fixed,precision=0]{\pgfplotspointmeta}k},every node near coord/.append style={font=\sffamily\tiny},
 enlarge x limits=0.1,title={Capital improvements by year, best estimate (\$k)},title style={font=\sffamily\bfseries\small}]
\addplot[fill=brick,draw=none] coordinates {%s};
\end{axis}\end{tikzpicture}""" % (",".join(y for y, _ in pts), " ".join(f"({y},{v/1000:.1f})" for y, v in pts)))
w("total", money(tot_best) + "%")
w("totals_note", rf"Best estimate {money(tot_best)} across {len(inc)} projects (documented {money(tot_doc)}; payments traced {money(tot_paid)}).")

# timeline: swimlanes by category, angled labels
def frac(d):
    d = dt.date.fromisoformat(d[:10]); a, b = T0, dt.date(TODAY.year, 12, 31)
    return (d - a).days / (b - a).days
_dates = [p["date"][:10] for p in P if p.get("date")] + [d for d, _ in D["TIMELINE_EXTRA"]]
T0 = min([dt.date(SINCE, 1, 1)] + [dt.date.fromisoformat(d[:10]) for d in _dates])
T0 = dt.date(T0.year, 1, 1)
LANES = ["Exterior", "Structural", "Interior", "Unit turnover", "Mechanical", "Landscape", "Smart home"]
_cats = [p.get("cat") or "Other" for p in P if p.get("date")]
lanes = [l for l in LANES if l in _cats] + sorted({c for c in _cats if c not in LANES}) or ["All"]
if D["TIMELINE_EXTRA"]: lanes.append("Milestones")
LH = 46
tl = [r"\begin{tikzpicture}[x=0.86\linewidth,y=1pt]"]
_span = TODAY.year - T0.year + 1
for yr in range(T0.year + (1 if _span <= 8 else 0), TODAY.year + 1, 1 if _span <= 12 else 2):
    x = frac(f"{yr}-01-01")
    tl.append(rf"\draw[rule]({x:.4f},6)--({x:.4f},{-LH*len(lanes)+10}) node[below,font=\sffamily\scriptsize\bfseries,text=slate]{{{yr}}};")
for li, lane in enumerate(lanes):
    y = -li * LH
    tl.append(rf"\node[anchor=east,font=\sffamily\scriptsize\bfseries,text=slate] at (-0.01,{y}) {{{lane}}};\draw[slate!50,line width=0.8pt](0,{y})--(1,{y});")
    lastx, flip = -1, False
    for p in P:
        if not p["date"] or (p.get("cat") or "Other") != lane: continue
        x = frac(p["date"]); r = max(1.6, min(5.0, ((p.get("cost") or 0) / 1000) ** 0.5 * 0.55))
        flip = (not flip) if x - lastx < 0.025 else False; lastx = x
        rot, anc, dy = (-55, "north west", -r) if flip else (55, "south west", r)
        tl.append(rf"\fill[brick,opacity=0.85]({x:.4f},{y}) circle[radius={r:.1f}pt];"
                  rf"\node[rotate={rot},anchor={anc},font=\sffamily\tiny,inner sep=1pt] at ({x:.4f},{y+dy:.1f}) {{{e(p['short'])}}};")
if D["TIMELINE_EXTRA"]:
    y = -(len(lanes) - 1) * LH; lastx, flip = -1, False
    for d, lab in sorted(D["TIMELINE_EXTRA"]):
        x = frac(d); flip = (not flip) if x - lastx < 0.025 else False; lastx = x
        rot, anc, dy = (-55, "north west", -2.5) if flip else (55, "south west", 2.5)
        tl.append(rf"\fill[ink]({x:.4f},{y}) +(-2pt,-2pt) rectangle +(2pt,2pt);"
                  rf"\node[rotate={rot},anchor={anc},font=\sffamily\tiny,inner sep=1pt] at ({x:.4f},{y+dy:.1f}) {{{e(lab)}}};")
tl.append(r"\end{tikzpicture}")
w("timeline", "\n".join(tl))

# ---------------- quirks
w("quirks", "\n".join(
    rf"\quirk{{{e(q['title'])}}}{{{e(q['symptom'])}}}{{{e(q['cause'])}}}{{{e(q['fix'])}}}{{{e(q['src'])}}}"
    for q in D["QUIRKS"]))

# ---------------- providers
rows = [rf"{e(v['name'])} & {e(v['trade'])} & {e(v.get('contact',''))} & {e(v.get('work',''))} & \num{{{e(v.get('when',''))}}}\\" for v in sorted(D["PROVIDERS"], key=lambda v: v["trade"])]
w("providers", r"\begin{dtab}\begin{longtable}{@{}>{\RaggedRight\bfseries}p{1.35in}>{\RaggedRight}p{0.95in}>{\RaggedRight}p{1.45in}>{\RaggedRight}p{2.1in}>{\RaggedRight}p{0.7in}@{}}\toprule" +
  r"\thd{Provider}&\thd{Trade}&\thd{Contact}&\thd{Work here}&\thd{When}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- warranties
rows = [rf"{e(x['item'])} & {e(x['who'])} & {e(x['term'])} & \num{{{e(x.get('start') or '?')}}} & \num{{{'lifetime' if (x.get('expiry') or '').startswith('2099') else e(x.get('expiry') or '?')}}} & {warranty_pill(x.get('expiry'))} & {doc_pill(x.get('paperwork'))}\\" for x in sorted(D["WARRANTIES"], key=lambda x: x.get("expiry") or "9999")]
w("warranties", r"\begin{dtab}\begin{longtable}{@{}>{\RaggedRight}p{1.75in}>{\RaggedRight}p{1.2in}>{\RaggedRight}p{1.35in}llcc@{}}\toprule" +
  r"\thd{Item}&\thd{Warrantor}&\thd{Term}&\thd{Start}&\thd{Expires}&\thd{Status}&\thd{Doc}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- invoices
rows = [rf"\num{{{e(i['date'])}}} & {e(i['vendor'])} & {e(i['what'])} & {money(i.get('amount'))} & {e(i.get('where',''))}\\" for i in sorted(D["INVOICES"], key=lambda i: i["date"])]
w("invoices", r"\begin{dtab}\begin{longtable}{@{}l>{\RaggedRight}p{1.5in}>{\RaggedRight}p{2.6in}r>{\RaggedRight}p{1.2in}@{}}\toprule" +
  r"\thd{Date}&\thd{Vendor}&\thd{What}&\thd{Amount}&\thd{Where filed}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- paperwork to chase: missing/partial paper + who most likely holds it
def chase(p): return p.get("chase")
gaps = [p for p in P if p.get("paperwork") in ("missing", "partial", "ask", None) and chase(p) and not p.get("exclude")]
rows = [rf"{e(p['title'])} & \num{{{e(p['date'] or '?')}}} & {e(p['vendor'])} & {money(best(p))} & {doc_pill(p.get('paperwork'))} & {e(chase(p))}\\" for p in gaps]
w("chase", r"\begin{dtab}\begin{longtable}{@{}>{\RaggedRight\bfseries}p{1.35in}l>{\RaggedRight}p{1.05in}r c>{\RaggedRight}p{2.35in}@{}}\toprule" +
  r"\thd{Project}&\thd{Done}&\thd{Vendor}&\thd{Cost}&\thd{Have}&\thd{Who likely has it}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")
nog = [p for p in P if p.get("paperwork") in ("missing", "partial") and not chase(p) and not p.get("exclude")]
w("chase_n", str(len(gaps)))
w("nogap", ", ".join(e(p["title"]) for p in nog))

# ---------------- maintenance calendar
rows = [rf"\textbf{{{e(m['when'])}}} & {e(m['task'])} & {e(m.get('why',''))}\\" for m in D["MAINTENANCE"]]
w("maintenance", r"\begin{dtab}\begin{longtable}{@{}>{\RaggedRight}p{0.95in}>{\RaggedRight}p{2.7in}>{\RaggedRight}p{3.2in}@{}}\toprule" +
  r"\thd{When}&\thd{Task}&\thd{Why / notes}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- facts
w("facts", r"\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\color{slate}\bfseries}l X@{}}" +
  "\n".join(rf"{e(k)} & {e(v)}\\" for k, v in D["FACTS"]) + r"\end{tabularx}\end{dtab}")

# ---------------- systems (free-form sections: title, paragraphs/bullets, table rows)
out = []
for s in D["SYSTEMS"]:
    out.append(rf"\section{{{e(s['title'])}}}")
    if s.get("intro"): out.append(e(s["intro"]) + r"\par")
    if s.get("rows"):
        out.append(r"\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\RaggedRight\bfseries}p{1.5in}X@{}}")
        out += [rf"{e(k)} & {e(v)}\\" for k, v in s["rows"]]
        out.append(r"\end{tabularx}\end{dtab}\par")
    if s.get("bullets"): out.append(r"\begin{itemize}" + "".join(rf"\item {e(b)}" for b in s["bullets"]) + r"\end{itemize}")
    out.append(photos_block(s.get("photos", []), s.get("per_row", 3)))
    if s.get("raw"): out.append(s["raw"])
w("systems", "\n".join(out))

# ---------------- electrical panels (PANELS rows: slot, amps, poles, circuit, protection, note)
ns = dict(PANELS=D["PANELS"], SPARE=set(D.get("PANEL_SPARE", [])), DATE=D.get("PANEL_DATE", ""))
out = []
for p in ns["PANELS"]:
    by = {r[0]: r for r in p["rows"]}; cov = {r[0] + 2 for r in p["rows"] if r[2] == 2}
    def cell(s):
        if s in cov: return None
        r = by.get(s)
        if not r: return (str(s), "", r"\textcolor{rule}{" + ("spare" if p["id"] in ns["SPARE"] else "—") + "}", "")
        s_, a, pl, c, pr, n = r
        lab = (r"\textbf{" + e(c) + "}" if pl == 2 else e(c)) + (r" {\tiny\color{slate}[" + e(pr) + "]}" if pr else "") + (r"\textsuperscript{\color{brick}†}" if n else "")
        return (f"{s}–{s+2}" if pl == 2 else str(s), a, lab, pl)
    lines = []
    for k in range(p["slots"] // 2):
        L, Rr = cell(2 * k + 1), cell(2 * k + 2)
        def fmt(c): return "&&" if c is None else rf"\num{{{c[0]}}}&\num{{\textbf{{{c[1]}}}}}&{c[2]}"
        lines.append(fmt(L) + "&" + fmt(Rr) + r"\\")
    notes = [f"{r[0]}: {r[5]}" for r in sorted(p["rows"]) if r[5]]
    out.append(rf"\subsection*{{{e(p['title'])} \textmd{{\color{{slate}}— {e(p['desc'])}}}}}")
    out.append(r"\begin{dtab}\rowcolors{1}{white}{white}\begin{tabularx}{\linewidth}{@{}r r X @{\hspace{6pt}}!{\color{ink}\vrule width 1pt}@{\hspace{6pt}} r r X@{}}\toprule")
    out += lines
    out.append(r"\bottomrule\end{tabularx}\end{dtab}")
    if notes: out.append(r"{\scriptsize\sffamily\color{slate}\textcolor{brick}{†} " + e(" · ".join(notes)) + r"}\par")
w("panels", "\n".join(out))

# ---------------- panel loads: connected breaker capacity per leg / per column
# Split-phase bus: row k (slots 2k-1, 2k) is on leg A when k is odd, B when even; a 2-pole lands on both legs.
def amps(a): return float(str(a).rstrip("?"))
def leg(s): return "A" if ((s + 1) // 2) % 2 else "B"
MAIN = {p["id"]: p.get("main", 200) for p in D["PANELS"]}
LOADS = []
for p in ns["PANELS"]:
    t = dict(id=p["id"], A=0.0, B=0.0, L=0.0, R=0.0, a240=0.0, a120=0.0, n2=0, n1=0)
    for s, a, pl, c, pr, n in p["rows"]:
        A_ = amps(a); side = "L" if s % 2 else "R"
        if pl == 2: t["A"] += A_; t["B"] += A_; t[side] += 2 * A_; t["a240"] += A_; t["n2"] += 1
        else: t[leg(s)] += A_; t[side] += A_; t["a120"] += A_; t["n1"] += 1
    used = sum(r[2] for r in p["rows"]); t["free"] = p["slots"] - used
    feed = next((amps(r[1]) for r in p["rows"] if r[2] == 2 and "GENERATOR" in r[3].upper()), 0)
    t["feed"] = feed                                       # a main panel's 2-pole feed to a generator subpanel, counted inside its legs
    LOADS.append(t)
def bar(v, cap, col):
    f = min(v / cap, 3.0) / 3.0
    return rf"\tikz[baseline=-0.6ex]{{\fill[wash](0,-3pt)rectangle(1.1in,3pt);\fill[{col}](0,-3pt)rectangle({1.1*f:.3f}in,3pt);\draw[ink,line width=0.6pt]({1.1/3:.3f}in,-4.5pt)--({1.1/3:.3f}in,4.5pt);}}"
rows = []
for t in LOADS:
    m = MAIN[t["id"]]; hi = max(t["A"], t["B"])
    own = rf" \textcolor{{slate}}{{({t['A']-t['feed']:.0f}/{t['B']-t['feed']:.0f} excl.\ sub-feed)}}" if t["feed"] else ""
    rows.append(rf"\textbf{{Panel {t['id']}}} & \num{{{m}}} & \num{{{t['A']:.0f}}} & \num{{{t['B']:.0f}}} & {bar(hi, m, 'brick')} \num{{{hi/m:.2f}×}}{own} & \num{{{t['L']:.0f} / {t['R']:.0f}}} & \num{{{t['n1']} / {t['n2']}}} & \num{{{t['a240']:.0f}}} & \num{{{t['free']}}}\\")
w("panelloads", r"""\section*{Connected load, per leg}
Sum of breaker handle ratings on each bus leg: the \emph{most} each leg could draw if every circuit ran at its trip rating at once. It is not a demand load (an NEC~220 calculation would come out far lower), and connected capacity of 2--3$\times$ the main is normal. What it is good for is leg balance and headroom. A~2-pole breaker counts its full rating on both legs; slot rows alternate A, B, A, B down the panel. Column = left/right side of the door in amp-poles. In the bar, the tick marks 1× the main and the full bar 3×.\par\smallskip\noindent
\begin{dtab}\begin{tabularx}{\linewidth}{@{}l r r r X r r r r@{}}\toprule
\thd{Panel}&\thd{Main A}&\thd{Leg A}&\thd{Leg B}&\thd{Worst leg vs main}&\thd{Left / right}&\thd{1P / 2P}&\thd{240\,V A}&\thd{Free poles}\\\midrule
""" + "\n".join(rows) + r"""\bottomrule\end{tabularx}\end{dtab}
{\sffamily\scriptsize\color{slate}""" + e(D.get("PANEL_NOTE", "")) + r"}\par" + D["PROSE"].get("panel_demand", ""))

# ---------------- service demand (NEC 220.82 optional method, dwelling) + generator headroom
DM = D.get("DEMAND") or {}
out = []
if DM:
    V = DM.get("volts", 240)
    gen_rows = [("General lighting & receptacles", f"{DM['sqft']:,} sq ft × 3 VA", 3 * DM["sqft"]),
                ("Small-appliance + laundry circuits", f"{DM.get('small_appliance', 2) + DM.get('laundry', 1)} × 1,500 VA", 1500 * (DM.get("small_appliance", 2) + DM.get("laundry", 1)))]
    gen_rows += [(n.replace(" (~)", ""), "typical (no nameplate yet)" if "(~)" in n else "nameplate", va) for n, va in DM.get("appliances", [])]
    G = sum(r[2] for r in gen_rows); Gd = min(G, 10000) + 0.4 * max(G - 10000, 0)
    cool = sum(va for _, va in DM.get("cool", [])); heat = sum(va * f for _, va, f in DM.get("heat", []))
    hv = max(cool, heat); tot = Gd + hv; amps_ = tot / V; svc = DM.get("service_amps", 200)
    rows = [rf"{e(n)} & \textcolor{{slate}}{{{e(b)}}} & \num{{{va:,.0f}}}\\" for n, b, va in gen_rows]
    out.append(r"\section*{Service demand estimate}" + e(DM.get("note", "")) + r"\par\smallskip\begin{dtab}\begin{tabularx}{\linewidth}{@{}X>{\RaggedRight}p{1.6in}r@{}}\toprule\thd{Load}&\thd{Basis}&\thd{VA}\\\midrule" + "\n" +
               "\n".join(rows) + rf"\midrule\rowcolor{{white}}\textbf{{General loads}} & first 10\,kVA at 100\,\%, rest at 40\,\% & \num{{{G:,.0f}}} $\rightarrow$ \textbf{{\num{{{Gd:,.0f}}}}}\\" +
               rf"\rowcolor{{white}}\textbf{{Heating / cooling}} & larger of cooling \num{{{cool:,.0f}}} or heating \num{{{heat:,.0f}}} & \textbf{{\num{{{hv:,.0f}}}}}\\\midrule" +
               rf"\rowcolor{{white}}\textbf{{Calculated demand}} & \num{{{tot/1000:.1f}}}\,kVA at \num{{{V}}}\,V & \textbf{{\num{{{amps_:.0f}}}\,A}} = \textbf{{\num{{{100*amps_/svc:.0f}}}\,\%}} of \num{{{svc}}}\,A\\\bottomrule\end{{tabularx}}\end{{dtab}}")
    if DM.get("measured"):
        out.append(r"\par\smallskip\noindent{\sffamily\footnotesize\textbf{Measured} " + " · ".join(rf"{e(k)} \num{{{v:.1f}}}\,kW (\num{{{v*1000/V:.0f}}}\,A)" for k, v in DM["measured"]) + r"}\par")
gens = [p for p in D["PANELS"] if p.get("gen_kw")]
for p in gens:
    t = next(x for x in LOADS if x["id"] == p["id"]); ga = p["gen_kw"] * 1000 / 240; hi = max(t["A"], t["B"])
    out.append(rf"\par\smallskip\noindent{{\sffamily\footnotesize\textbf{{Generator headroom, Panel {e(p['id'])}.}} A \num{{{p['gen_kw']}}}\,kW unit supplies about \num{{{ga:.0f}}}\,A per leg at 240\,V. Connected capacity on the backed panel's worst leg is \num{{{hi:.0f}}}\,A, \textbf{{\num{{{hi/ga:.1f}}}× the generator}}: fine only as long as the big loads don't all start together.}}\par")
w("demand", "\n".join(out))

# ---------------- printable panel directories (one letter page each; tex/panel-labels.tex)
def lab_cell(r, x0, x1, y, h, right):
    s, a, pl, c, pr, n = r
    hh = h * pl; yc = y - hh / 2
    al, anc, xt = ("right", "east", x1 - 0.08) if right else ("left", "west", x0 + 0.08)
    badge = rf"\,\pbadge{{{e(pr)}}}" if pr else ""
    volt = r"\,\pbadge{240\,V}" if pl == 2 else ""
    name = (r"\bfseries " if pl == 2 else "") + e(c)
    note = rf"\\[-1pt]{{\scriptsize\itshape\color{{slate}}{e(n)}}}" if n else ""
    txt = (badge + volt + r"\ " + name) if right else (name + volt + badge)
    return rf"\node[anchor={anc},align={al},text width={x1-x0-0.16:.2f}in,font=\sffamily\small] at ({xt:.2f},{yc:.3f}) {{{txt}{note}}};"
pages = []
for p in ns["PANELS"]:
    t = next(x for x in LOADS if x["id"] == p["id"]); m = MAIN[p["id"]]
    nrow = p["slots"] // 2; h = min(0.6, 7.9 / nrow)
    by = {r[0]: r for r in p["rows"]}; cov = {r[0] + 2 for r in p["rows"] if r[2] == 2}
    X = dict(lc=(0, 3.01), la=(3.01, 3.46), ls=(3.46, 3.76), lg=(3.76, 3.94), rs=(3.94, 4.24), ra=(4.24, 4.69), rc=(4.69, 7.7))
    tz = [r"\begin{tikzpicture}[x=0.99in,y=1in]"]
    for k in range(nrow):
        y = -k * h; L, Rr = 2 * k + 1, 2 * k + 2; lg = leg(L)
        tz.append(rf"\fill[{'ink' if lg == 'A' else 'rule'}]({X['lg'][0]},{y:.3f})rectangle({X['lg'][1]},{y-h:.3f});"
                  rf"\node[font=\sffamily\bfseries\scriptsize,text={'white' if lg == 'A' else 'ink'}] at (3.85,{y-h/2:.3f}) {{{lg}}};")
        for s, (cc, ca, cs), right in ((L, ("lc", "la", "ls"), True), (Rr, ("rc", "ra", "rs"), False)):
            if s in cov: continue
            r = by.get(s); span = (r[2] if r else 1); yb = y - h * span
            if r and r[2] == 2: tz.append(rf"\fill[wash]({0 if right else 3.94},{y:.3f})rectangle({3.76 if right else 7.7},{yb:.3f});")
            nums = f"{s}\\\\[-2pt]{s+2}" if span == 2 else str(s)
            tz.append(rf"\node[align=center,font=\numfont\footnotesize,text=slate] at ({sum(X[cs])/2:.3f},{y-h*span/2:.3f}) {{{nums}}};")
            if r:
                tz.append(rf"\node[font=\numfont\bfseries\large] at ({sum(X[ca])/2:.3f},{y-h*span/2:.3f}) {{{e(r[1])}}};")
                tz.append(lab_cell(r, *X[cc], y, h, right))
            else:
                tz.append(rf"\node[anchor={'east' if right else 'west'},font=\sffamily\scriptsize,text=rule] at ({X[cc][1]-0.08 if right else X[cc][0]+0.08:.2f},{y-h/2:.3f}) {{{'spare' if p['id'] in ns['SPARE'] else ''}}};")
        if not (by.get(L) and by[L][2] == 2): tz.append(rf"\draw[rule,line width=0.4pt](0,{y-h:.3f})--(3.76,{y-h:.3f});")
        if not (by.get(Rr) and by[Rr][2] == 2): tz.append(rf"\draw[rule,line width=0.4pt](3.94,{y-h:.3f})--(7.7,{y-h:.3f});")
    tz.append(rf"\draw[ink,line width=1.2pt](0,0)--(7.7,0) (0,{-nrow*h:.3f})--(7.7,{-nrow*h:.3f});")
    tz.append(r"\end{tikzpicture}")
    gen_banner = (r"\par\vspace{2pt}{\sffamily\bfseries\small\color{white}\colorbox{ink}{\ " + e(p["banner"]) + r" \ }}") if p.get("banner") else ""
    tally = (rf"\textbf{{Connected load}}\quad leg A \num{{{t['A']:.0f}\,A}} · leg B \num{{{t['B']:.0f}\,A}} against a \num{{{m}\,A}} {'feed' if p.get('fed') else 'main'}"
             rf" ({max(t['A'],t['B'])/m:.2f}× worst leg) · {t['n1']} single-pole, {t['n2']} two-pole · {t['free']} free poles"
             + (rf" · incl. the \num{{{t['feed']:.0f}\,A}} sub-feed" if t["feed"] else ""))
    pages.append(rf"""\noindent{{\sffamily\bfseries\fontsize{{26}}{{28}}\selectfont {e(p['title'])}}}\hfill{{\sffamily\large {e(p['desc'])}}}\par\vspace{{-2pt}}
{{\color{{ink}}\rule{{\linewidth}}{{2pt}}}}\par\vspace{{1pt}}
{{\sffamily\scriptsize\color{{slate}}{e(META['title'])} · surveyed {ns['DATE']} · amps from each handle · shaded rows = 2-pole (240\,V) · centre strip = bus leg}}{gen_banner}\par\vspace{{8pt}}
\noindent{chr(10).join(tz)}\par\vspace{{6pt}}
{{\sffamily\footnotesize {tally}}}\par\vfill
{{\sffamily\tiny\color{{slate}}Print at 100\,\% on letter; trim and tape inside the panel door. Pencil corrections in the blank rows, then fix them in the book data.}}
\newpage""")
w("panellabels", "\n".join(pages))
print("generated:", ", ".join(sorted(f.stem for f in OUT.glob("*.tex"))))

w("edition", r"\newcommand{\EDNAME}{%s}\newif\ifprivate\private%s" % ("Full edition — private" if EDITION=="full" else "Share edition", "true" if EDITION=="full" else "false"))
# ---------------- open issues
ic = {"planned": "okg", "safety": "bad", "envelope": "amb", "mechanical": "brick", "plumbing": "slate", "comfort": "slate", "paperwork": "okg"}
rows = [rf"\pill{{{ic.get(k,'slate')}}}{{{k.upper()}}} & {e(t)}\\" for k, t in D.get("OPEN_ISSUES", [])]
w("openissues", r"\begin{dtab}\begin{longtable}{@{}l>{\RaggedRight}p{6.1in}@{}}\toprule\thd{Kind}&\thd{Issue}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")
# ---------------- planned projects
out = []
for t in D.get("PLANNED", []):
    out.append(rf"\begin{{qbox}}[colframe=okg]{{{e(t['title'])}}}\begin{{tabularx}}{{\linewidth}}{{@{{}}>{{\sffamily\scriptsize\color{{slate}}}}l X@{{}}}}WHY & {e(t['why'])}\\ PLAN & {e(t['plan'])}\\\end{{tabularx}}\end{{qbox}}")
w("planned", "\n".join(out))
# ---------------- action items
out = []
for i, a in enumerate(D.get("ACTIONS", []), 1):
    out.append(rf"\begin{{qbox}}[colframe=okg]{{\textcolor{{okg}}{{{i}.}} {e(a['title'])}\hfill\textcolor{{ink}}{{\numfont {e(a['value'])}}}}}"
               rf"\begin{{tabularx}}{{\linewidth}}{{@{{}}>{{\sffamily\scriptsize\color{{slate}}}}l X@{{}}}}WHY & {e(a['why'])}\\ DO & {e(a['how'])}\\ CONFIDENCE & {e(a['conf'])}\\\end{{tabularx}}\par\hfill\src{{{e(a['src'])}}}\end{{qbox}}")
w("actions", "\n".join(out))
# ---------------- at-a-glance vital signs
W = D["WARRANTIES"]
def wstat(x):
    ex = x.get("expiry")
    if not ex: return "unk"
    d = dt.date.fromisoformat(ex)
    return "exp" if d < TODAY else ("soon" if (d - TODAY).days < 365 else "ok")
ws = [wstat(x) for x in W]
pw = [p.get("paperwork") for p in inc]
tiles = [
  ("Invested since " + str(SINCE), money(tot_best), f"{len(inc)} projects · best estimate"),
  ("Paperwork on file", f"{pw.count('have')}/{len(pw)}", f"{pw.count('partial')} partial · {pw.count('missing')} missing"),
  ("Warranties", f"{ws.count('ok')} active", f"{ws.count('soon')} expiring <1 yr · {ws.count('exp')} expired · {ws.count('unk')} unknown"),
  ("Open issues", str(len(D.get('OPEN_ISSUES', []))), f"{sum(1 for k,_ in D.get('OPEN_ISSUES', []) if k=='safety')} safety"),
  (("Units", str(len(D["UNITS"])), META.get("units_note") or "see the Units chapter") if D["UNITS"] else ("Service providers", str(len(D["PROVIDERS"])), "with contacts")),
  ("Service log", str(len(D["INVOICES"])), f"visits & repairs, {min([i['date'][:4] for i in D['INVOICES']] or [str(SINCE)])}–{str(TODAY.year)[2:]}"),
]
cells = [rf"\begin{{minipage}}[t]{{0.325\linewidth}}\begin{{tcolorbox}}[colback=wash,colframe=wash,arc=0pt,left=5pt,right=5pt,top=3pt,bottom=3pt]{{\sffamily\scriptsize\color{{slate}}\MakeUppercase{{{e(a)}}}}}\par{{\numfont\bfseries\Large {b}}}\par{{\sffamily\scriptsize {e(c)}}}\end{{tcolorbox}}\end{{minipage}}" for a, b, c in tiles]
w("glance", r"\noindent" + r"\hfill".join(cells[:3]) + r"\par\vspace{2pt}\noindent" + r"\hfill".join(cells[3:]) + r"\par")

w("emergency", r"\section*{In an emergency}\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\color{bad}\bfseries}l X@{}}" + "\n".join(rf"{e(k)} & {e(v)}\\" for k, v in D.get("EMERGENCY", [])) + r"\end{tabularx}\end{dtab}")
# ---------------- manuals appendix
import csv as _csv
mrows = list(_csv.DictReader((R / "research/manuals.csv").open())) if (R / "research/manuals.csv").exists() else []
mp = {"exact": "okg", "family": "slate", "likely": "amb", "closest": "amb", "unconfirmed": "bad"}
rows = [rf"{e(m['system'])} & {e(m['equipment'])} & {e(m['maker'])} {e(m['model'])} & {e(m['doc_type'])} & \num{{{e(m['pages'])}}} & \pill{{{mp.get(m['model_match'],'slate')}}}{{{e(m['model_match']).upper()}}}\\"
        for m in sorted(mrows, key=lambda m: (m["system"], m["equipment"])) if m.get("file")]
need = [m for m in mrows if not m.get("file")]
w("manuals", rf"{len(rows)} manufacturer documents, filed in \texttt{{manuals/}} and shared alongside the photo index. Match: \pill{{okg}}{{EXACT}} this model · \pill{{slate}}{{FAMILY}} covers the series · \pill{{amb}}{{LIKELY}} · \pill{{bad}}{{UNCONFIRMED}} read the nameplate." +
  r"\begin{dtab}\begin{longtable}{@{}l>{\RaggedRight}p{1.55in}>{\RaggedRight}p{1.9in}>{\RaggedRight}p{1.55in}rc@{}}\toprule\thd{System}&\thd{Equipment}&\thd{Maker / model}&\thd{Document}&\thd{pp}&\thd{Match}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}" +
  r"\section*{Nameplate walk-through}Model numbers still needed. One pass through the house with a phone camera closes these out:" +
  r"\begin{dtab}\begin{longtable}{@{}>{\bfseries}p{1.7in}>{\RaggedRight}p{2.9in}>{\RaggedRight}p{2.0in}@{}}\toprule\thd{Item}&\thd{Where to look}&\thd{Why}\\\midrule" + "\n" +
  "\n".join(rf"{e(a)} & {e(b)} & {e(c)}\\" for a, b, c in D.get("NAMEPLATE_WALK", [])) + r"\bottomrule\end{longtable}\end{dtab}")
# ---------------- document index (Paperless downloads + Drive)
import re as _re
docs = []
for f in sorted((R / "docs/paperless").glob("*")):
    if f.suffix.lower() == ".png": continue
    m = _re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_(.+)_(\d+)$", f.stem)
    if m: docs.append((m.group(1), m.group(2).replace("-", " "), m.group(3).replace("-", " "), "Paperless " + m.group(4)))
for t, i, what in D.get("DRIVE_DOCS", []): docs.append(("", "Drive", f"{t}: {what}", "Drive " + i[:10] + "…"))
rows = [rf"\num{{{e(a)}}} & {e(b)} & {e(c)} & {e(d)}\\" for a, b, c, d in docs]
w("docindex", rf"{len(docs)} documents. Paperless originals (with page-1 previews) are copied to \texttt{{docs/paperless/}} next to this book." +
  r"\begin{dtab}\scriptsize\begin{longtable}{@{}l>{\RaggedRight}p{1.3in}>{\RaggedRight}p{3.9in}>{\RaggedRight}p{1.0in}@{}}\toprule\thd{Date}&\thd{From}&\thd{Document}&\thd{Where}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- raw prose fragments (LaTeX, written verbatim)
for k, v in D.get("PROSE", {}).items(): w(k, v)
print("prose:", ", ".join(D.get("PROSE", {})))
exec((E / "assemble.py").read_text())
