#!/usr/bin/env python3
"""photos/orig/** -> photos/print (1600px q82, for LaTeX) + photos/web (2560px q88 + 480px thumbs).
All derivatives: EXIF stripped except DateTimeOriginal/orientation baked in; GPS never survives."""
import subprocess, pathlib, sys
import os
R = pathlib.Path(os.environ["PROP"]).resolve()
ORIG, PRINT, WEB = R/"photos/orig", R/"photos/print", R/"photos/web"
EXT = {".jpg",".jpeg",".png",".heic",".heif"}
def slug(p): return str(p.relative_to(ORIG).with_suffix("")).replace("/","__")
def mk(src, dst, size, q):
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime: return
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["magick", str(src)+"[0]", "-auto-orient", "-resize", f"{size}x{size}>",
                    "-strip", "-quality", str(q), "-interlace", "Plane", str(dst)], check=True)
n = 0
for src in sorted(p for p in ORIG.rglob("*") if p.suffix.lower() in EXT):
    s = slug(src)
    mk(src, PRINT/f"{s}.jpg", 1300, 74)
    mk(src, WEB/"full"/f"{s}.jpg", 2560, 88)
    mk(src, WEB/"thumb"/f"{s}.jpg", 480, 78)
    n += 1
print(f"{n} photos processed")
