# exec'd at the end of gen.py (shares its globals): units/compliance/finance chapters + preamble + main.tex assembly.

# ---------------- units
U = D["UNITS"]
if U:
    out = [r"\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\bfseries}l>{\RaggedRight}p{1.1in}>{\RaggedRight}p{1.6in}X@{}}\toprule\thd{Unit}&\thd{Floor}&\thd{Layout}&\thd{Status}\\\midrule"]
    out += [rf"{e(u['unit'])} & {e(u.get('floor',''))} & {e(u.get('layout',''))} & {e(u.get('status',''))}\\" for u in U]
    out.append(r"\bottomrule\end{tabularx}\end{dtab}\par")
    for u in U:
        out.append((r"\section*{" if len(U) > 8 else r"\section{") + rf"{e(u['unit'])}" + (rf" \textmd{{\color{{slate}}— {e(u['floor'])}}}" if u.get("floor") else "") + "}")
        kv = [(k, u.get(f)) for k, f in (("Layout", "layout"), ("Systems", "systems"), ("Features", "features"), ("Status", "status"), ("Notes", "notes")) if u.get(f)]
        if kv:
            out.append(r"\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\RaggedRight\bfseries}p{1.0in}X@{}}" + "\n".join(rf"{e(k)} & {e(v)}\\" for k, v in kv) + r"\end{tabularx}\end{dtab}\par")
        if u.get("tenants"):
            out.append(r"\subsection*{Tenancy}\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\RaggedRight}p{1.6in}llr X@{}}\toprule\thd{Tenant}&\thd{From}&\thd{To}&\thd{Rent}&\thd{Notes}\\\midrule" + "\n" +
                       "\n".join(rf"{e(t.get('name'))} & \num{{{e(t.get('start') or '?')}}} & \num{{{e(t.get('end') or '')}}} & {money(t.get('rent')) if isinstance(t.get('rent'), (int, float)) else e(t.get('rent') or '—')} & {e(t.get('notes',''))}\\" for t in u["tenants"]) +
                       r"\bottomrule\end{tabularx}\end{dtab}\par")
        out.append(photos_block(u.get("photos", []), u.get("per_row", 3)))
    w("units", "\n".join(out))

# ---------------- compliance
cp = {"ok": ("okg", "OK"), "due": ("amb", "DUE"), "overdue": ("bad", "OVERDUE"), "unknown": ("slate", "UNKNOWN"), "na": ("rule", "N/A")}
if D["COMPLIANCE"]:
    rows = [rf"{e(c['item'])} & {e(c.get('authority',''))} & \pill{{{cp.get(c.get('status'), cp['unknown'])[0]}}}{{{cp.get(c.get('status'), cp['unknown'])[1]}}} & \num{{{e(c.get('last') or '?')}}} & \num{{{e(c.get('next') or '')}}} & {e(c.get('notes',''))}\\"
            for c in D["COMPLIANCE"]]
    w("compliance", r"\begin{dtab}\begin{longtable}{@{}>{\RaggedRight\bfseries}p{1.45in}>{\RaggedRight}p{0.95in}cll>{\RaggedRight}p{2.6in}@{}}\toprule\thd{Item}&\thd{Authority}&\thd{Status}&\thd{Last}&\thd{Next}&\thd{Notes}\\\midrule\endhead" + "\n" + "\n".join(rows) + r"\bottomrule\end{longtable}\end{dtab}")

# ---------------- finance + revenue (private; emptied in share edition)
F = D["FINANCE"]
if F or D["REVENUE"]:
    out = []
    if F.get("rows"):
        out.append(r"\begin{dtab}\begin{tabularx}{\linewidth}{@{}>{\color{slate}\bfseries}l X@{}}" + "\n".join(rf"{e(k)} & {e(v)}\\" for k, v in F["rows"]) + r"\end{tabularx}\end{dtab}")
    if F.get("taxes"):
        out.append(r"\section*{Property tax}\begin{dtab}\begin{longtable}{@{}ll r>{\RaggedRight}p{3.6in}@{}}\toprule\thd{Tax year}&\thd{PIN}&\thd{Amount}&\thd{Notes}\\\midrule\endhead" +
                   "\n".join(rf"\num{{{e(a)}}} & \num{{{e(b)}}} & {money(c) if isinstance(c, (int, float)) else e(c)} & {e(n)}\\" for a, b, c, n in F["taxes"]) + r"\bottomrule\end{longtable}\end{dtab}")
    if D["REVENUE"]:
        out.append(r"\section*{Gross rent by year}\begin{dtab}\begin{tabularx}{\linewidth}{@{}l r X@{}}\toprule\thd{Year}&\thd{Gross}&\thd{Notes}\\\midrule" + "\n" +
                   "\n".join(rf"\num{{{e(y)}}} & {money(g)} & {e(n)}\\" for y, g, n in D["REVENUE"]) + r"\bottomrule\end{tabularx}\end{dtab}")
    w("finance", "\n".join(out))

# ---------------- preamble + main.tex
TEX = R / "tex"
def tx(s): return e(s)
title = META["title"]
pre = (E / "preamble.tex").read_text()
BOOK = META.get("book", "HOUSE BOOK")
for k, v in {"@@PDFTITLE@@": tx(title) + " — " + tx(BOOK.title()), "@@AUTHOR@@": tx(META.get("author", "")),
             "@@HEAD@@": tx(title.upper()) + r" \textbullet{} " + tx(BOOK), "@@ASOF@@": TODAY.isoformat(),
             "@@ASK@@": ("ASK " + tx(META.get("ask", ""))).upper().strip(),
             "@@PORTABLE@@": r"\portabletrue" if os.environ.get("HOUSEBOOK_PORTABLE_FONTS") == "1" else ""}.items():
    pre = pre.replace(k, v)
(TEX / "preamble.tex").write_text(pre)

has = lambda n: (OUT / f"{n}.tex").exists() and (OUT / f"{n}.tex").stat().st_size > 0
P_ = D["PROSE"]
yrs = TODAY.year - SINCE
NUMW = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}
ch = []
A = ch.append
A(r"\chapter{At a Glance}\label{ch:glance}" "\n" r"\input{gen/glance}\medskip" "\n" + (P_.get("intro", "") + r"\par\medskip" if P_.get("intro") else "") + r"\input{gen/facts}\input{gen/emergency}")
if D["ACTIONS"]: A(r"\chapter{Money \& Risk on the Table}\label{ch:actions}Found while assembling this book: items that are worth money, or that keep a future claim from being denied. Most likely first; each one cites its evidence.\input{gen/actions}")
if U: A(r"\chapter{Units}\label{ch:units}" + P_.get("units_intro", "") + r"\input{gen/units}")
A(r"\chapter{Systems}\label{ch:systems}\input{gen/systems}")
if D["PANELS"]: A(r"\chapter{Electrical Panels}\label{ch:panels}" + P_.get("panels_intro", "") + r"\input{gen/panels}\input{gen/panelloads}\input{gen/demand}Printable door directories are in Appendix~\ref{ch:panellabels}.")
if D["COMPLIANCE"]: A(r"\chapter{Compliance \& Inspections}\label{ch:compliance}" + P_.get("compliance_intro", r"Status as of \EDITION. \pill{okg}{OK} current · \pill{amb}{DUE} within a year or now · \pill{bad}{OVERDUE} · \pill{slate}{UNKNOWN} no record found.") + r"\par\input{gen/compliance}")
if D["QUIRKS"]: A(r"\chapter{Quirks \& Field Notes}\label{ch:quirks}Every entry below cost real time to figure out. Format: what you'll see, why it happens, what to do.\input{gen/quirks}")
A(r"\chapter{Service Providers}\label{ch:providers}\input{gen/providers}")
A(r"\chapter{Warranties}\label{ch:warranties}Status as of \EDITION: \ACTIVE{} more than a year left, \SOON{} under a year, \EXPIRED, \UNKNOWN{} term or start date not found.\input{gen/warranties}")
A(r"\chapter{Invoice Ledger}\label{ch:invoices}\input{gen/ledger}\section{Individual invoices \& receipts on file}\input{gen/invoices}")
if F or D["REVENUE"]: A(r"\chapter{Ownership \& Finance}\label{ch:finance}" + P_.get("finance_intro", "") + r"\input{gen/finance}")
if EDITION == "full" and int((OUT / "chase_n.tex").read_text() or 0):
    A(r"\chapter{Paperwork to Chase}\label{ch:chase}" + P_.get("receipts_intro", r"Improvements with no invoice or final receipt in email, scanned documents, the drive or messages, and the person most likely to hold it.\par\smallskip{\small Gaps with no obvious holder: \input{gen/nogap}.}\par\medskip") + r"\input{gen/chase}")
A(r"\chapter{Open Issues}\label{ch:open}Known problems and unknowns as of \EDITION, safety first.\input{gen/openissues}" + (r"\section{Project queue}\input{gen/planned}" if D["PLANNED"] else "") + P_.get("open_extra", ""))
if D["MAINTENANCE"]: A(r"\chapter{Maintenance Calendar}\label{ch:maint}\input{gen/maintenance}")
A(r"\appendix")
A(rf"\chapter{{{NUMW.get(yrs, str(yrs))} Years in One Line}}\label{{ch:timeline}}From {SINCE} through \EDITION, \textbf{{\input{{gen/total}}}} of documented capital improvements." "\n"
  r"\par\vspace{40pt}\noindent\hspace*{0.1\linewidth}\input{gen/timeline}\par\vspace{30pt}" "\n" r"\noindent\input{gen/costchart}")
A(r"\chapter{Improvements}\label{ch:improvements}\input{gen/projects}")
if D["PANELS"]: A(r"\chapter{Printable Panel Directories}\label{ch:panellabels}One letter page per panel, generated from the same directory data as Chapter~\ref{ch:panels}. Print at 100\,\%, trim, and tape inside each panel door." "\n" r"\includepdf[pages=-,pagecommand={\thispagestyle{empty}}]{panel-labels.pdf}")
if P_.get("drawings"): A(r"\chapter{Drawings \& Plans}\label{ch:drawings}\input{gen/drawings}")
if mrows or D["NAMEPLATE_WALK"]: A(r"\chapter{Equipment Manuals}\label{ch:manuals}\input{gen/manuals}")
if EDITION == "full" and docs: A(r"\chapter{Document Index}\label{ch:index}\input{gen/docindex}")

cover = rf"""\begin{{titlepage}}
\newgeometry{{margin=0pt}}
\begin{{tikzpicture}}[remember picture,overlay]
  \fill[ink] (current page.north west) rectangle ([yshift=-4.6in]current page.north east);
  \IfFileExists{{../photos/print/cover.jpg}}{{%
    \node[anchor=north,inner sep=0] at ([yshift=-4.6in]current page.north) {{\includegraphics[width=\paperwidth,height=6.4in,keepaspectratio=false]{{cover.jpg}}}};}}{{}}
  \node[anchor=north west,text=white,align=left,inner sep=0] at ([xshift=0.75in,yshift=-0.9in]current page.north west)
   {{{{\sffamily\bfseries\large\color{{brick!40!white}} {tx(BOOK)} \textbullet{{}} \MakeUppercase{{\EDNAME}} \textbullet{{}} \EDITION}}\\[14pt]
    {{\displayfont\fontsize{{{META.get('title_pt', 50)}}}{{{META.get('title_pt', 50) + 2}}}\selectfont {tx(title)}}}\\[8pt]
    {{\sffamily\Large {tx(META.get('place',''))}}}\\[6pt]
    {{\sffamily\large\color{{white!85!black}} {tx(META.get('kind',''))}}}\\[14pt]
    {{\sffamily\small\color{{white!75!black}} {tx(META.get('blurb','Units · systems · quirks · providers · warranties · invoices'))}}}\\[2pt]
    {{\sffamily\small\color{{white!75!black}} {tx(META.get('span',''))}}}}};
  \node[anchor=south east,font=\sffamily\scriptsize,text=slate] at ([xshift=-0.5in,yshift=0.35in]current page.south east) {{Compiled from email, messages, documents, photos \& field notes.}};
\end{{tikzpicture}}
\restoregeometry
\end{{titlepage}}"""
(TEX / "main.tex").write_text("\\input{preamble}\n\\input{gen/edition}\n\\begin{document}\n\\frontmatter\n\\pagestyle{empty}\n" + cover +
    "\n\\pagestyle{scrheadings}\n\\setcounter{tocdepth}{1}\n{\\sffamily\\small\\tableofcontents}\n\\mainmatter\n" + "\n\n".join(ch) + "\n\\end{document}\n")
(TEX / "panel-labels.tex").write_text("\\input{preamble}\n\\input{gen/edition}\n\\begin{document}\n\\newgeometry{top=0.45in,bottom=0.4in,left=0.4in,right=0.4in}\n\\pagestyle{empty}\n\\input{gen/panellabels}\n\\end{document}\n")
print("chapters:", len(ch), "·", EDITION)
