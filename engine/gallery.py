#!/usr/bin/env python3
"""photos/web/{full,thumb} + research/*photos*.csv + data.PHOTO_META -> photos/web/index.html + manifest.{json,csv}.
Static, self-contained, relative paths: zip photos/web/ or rsync it anywhere."""
import csv, html, json, pathlib, runpy
import os
R = pathlib.Path(os.environ["PROP"]).resolve()
WEB = R / "photos/web"
PUB = R / "photos/publish"   # only what passes curation + WEB_EXCLUDE; this is the thing you share
import shutil
shutil.rmtree(PUB, ignore_errors=True); (PUB / "full").mkdir(parents=True); (PUB / "thumb").mkdir()
D = runpy.run_path(str(R / "data.py"))

meta = {}  # slug -> dict(date, caption, category, project, source)
def load(csvpath, prefix, source):
    if not csvpath.exists(): return
    for row in csv.DictReader(csvpath.open()):
        if (row.get("contains_people") or "no").lower().startswith("y"): continue
        stem = pathlib.Path(row["file"]).stem
        meta[f"{prefix}__{stem}"] = dict(date=row.get("date", "")[:10], caption=row.get("caption", ""),
                                         category=row.get("category", "other"), project=row.get("project", ""), source=source)
load(R / "research/photos.csv", "library", "Photos library")
load(R / "research/imessage_photos.csv", "imessage", "Messages")
for slug, m in D.get("PHOTO_META", {}).items(): meta.setdefault(slug, {}).update(m)

items = []
for f in sorted((WEB / "full").glob("*.jpg")):
    s = f.stem; m = meta.get(s)
    if m is None or m.get("exclude"): continue          # only curated, captioned photos get published
    if any(x in s for x in D.get("WEB_EXCLUDE", [])): continue
    shutil.copy2(f, PUB / "full" / f.name); shutil.copy2(WEB / "thumb" / f.name, PUB / "thumb" / f.name)
    items.append(dict(file=f"full/{f.name}", thumb=f"thumb/{f.name}", kb=f.stat().st_size // 1024, **m))
import re as _re
NAMES = "|".join(map(_re.escape, list(D.get("WEB_NAMES", [])) or ["(?!x)x"]))   # people named in captions; stripped from the public gallery
for i in items:                                   # web captions: no people's names, no chatty asides
    c = _re.sub(r"\s*\([^)]*\)", "", i.get("caption", ""))
    c = _re.sub(r"neighbor (?:" + NAMES + r")'s", "a neighbor's", c)
    c = _re.sub(r"\b(?:" + NAMES + r")\b:?", "", c)
    i["caption"] = _re.sub(r"\s{2,}", " ", c).strip(" ;,-–")
items.sort(key=lambda i: (i.get("date") or "9999", i["file"]))
(PUB / "manifest.json").write_text(json.dumps(items, indent=1))
with (PUB / "manifest.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["file", "date", "category", "project", "caption", "source", "kb"], extrasaction="ignore")
    w.writeheader(); w.writerows(items)

# ---- manuals: copy + table
man = []
mcsv = R / "research/manuals.csv"
if mcsv.exists():
    (PUB / "manuals").mkdir(exist_ok=True)
    for m in csv.DictReader(mcsv.open()):
        f = R / "manuals" / (m.get("file") or "")
        if m.get("file") and f.exists():
            shutil.copy2(f, PUB / "manuals" / f.name); man.append(m)
man.sort(key=lambda m: (m["system"], m["equipment"]))
cats = sorted({i.get("category") or "other" for i in items})
e = html.escape
tiles = "\n".join(
    f'<a class=t href="{e(i["file"])}" data-c="{e(i.get("category") or "other")}" data-q="{e((i.get("caption","")+" "+i.get("project","")).lower())}">'
    f'<img loading=lazy src="{e(i["thumb"])}" alt="{e(i.get("caption",""))}"><b>{e(i.get("date") or "????-??-??")}</b>'
    f'<i>{e(i.get("category") or "")}</i><span>{e(i.get("caption",""))}</span></a>' for i in items)
chips = "".join(f'<button data-c="{e(c)}">{e(c)} <em>{sum(1 for i in items if (i.get("category") or "other")==c)}</em></button>' for c in cats)
(PUB / "index.html").write_text(f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>{e(D["META"]["title"])} Photos</title>
<style>
:root{{--bg:#fbfaf7;--fg:#16181d;--dim:#6b7580;--line:#d9dcdf;--acc:#9b2c1c;--tile:#fff;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0b0e11;--fg:#d7dde3;--dim:#7d8792;--line:#1f252c;--acc:#e0765f;--tile:#12161b}}}}
:root[data-theme=dark]{{--bg:#0b0e11;--fg:#d7dde3;--dim:#7d8792;--line:#1f252c;--acc:#e0765f;--tile:#12161b}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--fg);font:12px/1.25 var(--mono);margin:0;padding:6px 16px}}
header{{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;border-bottom:2px solid var(--acc);padding:2px 0 4px;position:sticky;top:0;background:var(--bg);z-index:2}}
h1{{font-size:14px;margin:0}}h1 span{{color:var(--dim);font-weight:400}}
input{{font:inherit;padding:1px 4px;border:1px solid var(--line);background:var(--tile);color:var(--fg);width:16em}}
button{{font:inherit;border:1px solid var(--line);background:var(--tile);color:var(--fg);padding:0 5px;cursor:pointer}}
button em{{color:var(--dim);font-style:normal}}button.on{{background:var(--acc);color:#fff;border-color:var(--acc)}}button.on em{{color:#fff}}
#g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px;padding-top:6px}}
.t{{display:block;background:var(--tile);border:1px solid var(--line);color:inherit;text-decoration:none;font-size:10.5px;line-height:1.2}}
.t img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}}.t b{{font-weight:600;padding:1px 3px}}.t i{{float:right;color:var(--acc);font-style:normal;padding:1px 3px}}
.t span{{display:block;padding:0 3px 3px;color:var(--dim);max-height:3.7em;overflow:hidden}}.t:hover{{outline:2px solid var(--acc)}}
#lb{{position:fixed;inset:0;background:#000e;display:none;flex-direction:column;align-items:center;justify-content:center;z-index:9;color:#ddd;padding:8px}}
#lb img{{max-width:100%;max-height:calc(100vh - 60px);object-fit:contain}}#lb p{{margin:4px 0 0;max-width:90ch;text-align:center}}
footer{{color:var(--dim);padding:8px 0}}
h2{{font-size:13px;margin:14px 0 2px;border-bottom:1px solid var(--line)}}h2 span{{color:var(--dim);font-weight:400}}
.mt{{border-collapse:collapse;width:100%;font-size:11px}}.mt th,.mt td{{padding:1px 6px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}}
.mt th{{color:var(--dim);font-weight:400}}.mt td.n{{text-align:right}}.mt a{{color:var(--acc)}}
.mm.exact{{color:#3fb950}}.mm.family{{color:var(--dim)}}.mm.likely{{color:#d29922}}.mm.unconfirmed{{color:#f85149;font-weight:700}}
</style></head><body>
<header><h1>{e(D["META"]["title"])} <span>· photo index · {len(items)} photos · GPS stripped</span></h1>
<input id=q placeholder="filter caption / project…"> <span id=chips><button data-c="" class=on>all <em>{len(items)}</em></button>{chips}</span>
<a href="#manuals" style="color:var(--acc)">manuals</a> <a href="manifest.csv" style="color:var(--acc)">manifest.csv</a></header>
<div id=g>{tiles}</div>
<h2 id=manuals>Equipment manuals <span>· {len(man)} manufacturer PDFs</span></h2>
<table class=mt><tr><th>system<th>equipment<th>maker / model<th>document<th class=n>pp<th>match<th>source</tr>
{"".join(f'<tr><td>{e(m["system"])}<td>{e(m["equipment"])}<td>{e(m["maker"])} {e(m["model"])}<td><a href="manuals/{e(m["file"])}">{e(m["doc_type"])}</a><td class=n>{e(m["pages"])}<td class="mm {e(m["model_match"])}">{e(m["model_match"])}<td><a href="{e(m["source_url"])}">origin</a></tr>' for m in man)}
</table>
<div id=lb><img alt=""><p></p></div>
<footer>Full-resolution images (≤2560 px) in <code>full/</code>; metadata in manifest.json / manifest.csv. ←/→ step, Esc closes.</footer>
<script>
const tiles=[...document.querySelectorAll('.t')],lb=document.getElementById('lb'),li=lb.querySelector('img'),lp=lb.querySelector('p');
let cat='',q='',cur=-1;
function apply(){{tiles.forEach(t=>t.hidden=!((!cat||t.dataset.c===cat)&&(!q||t.dataset.q.includes(q))))}}
document.getElementById('chips').onclick=ev=>{{const b=ev.target.closest('button');if(!b)return;cat=b.dataset.c;
 document.querySelectorAll('#chips button').forEach(x=>x.classList.toggle('on',x===b));apply()}};
document.getElementById('q').oninput=ev=>{{q=ev.target.value.toLowerCase();apply()}};
const vis=()=>tiles.filter(t=>!t.hidden);
function show(i){{const v=vis();if(!v.length)return;cur=(i+v.length)%v.length;const t=v[cur];li.src=t.getAttribute('href');
 lp.textContent=t.querySelector('b').textContent+' · '+t.querySelector('span').textContent;lb.style.display='flex'}}
tiles.forEach(t=>t.onclick=ev=>{{ev.preventDefault();show(vis().indexOf(t))}});
lb.onclick=()=>{{lb.style.display='none';li.removeAttribute('src')}};
document.onkeydown=ev=>{{if(lb.style.display!=='flex')return;if(ev.key==='Escape')lb.onclick();if(ev.key==='ArrowRight')show(cur+1);if(ev.key==='ArrowLeft')show(cur-1)}};
</script></body></html>""")
print(f"gallery: {len(items)} photos, {len(cats)} categories -> {PUB/'index.html'}")
