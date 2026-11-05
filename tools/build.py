#!/usr/bin/env python3
"""Build the Vercel copy of Columbus Clash.

The artifact source is one self-contained HTML file with every image inlined as a
data: URI (about 11.5 MB). That is slow to download and parse before anything shows.
This script moves every inlined image into assets/<hash>.webp (PNG becomes lossless
WebP), adds the page head (doctype, viewport, app metas) and a small loader that shows
progress until the fighter and stage images are in. pixelfx effect atlases (fx-*.webp)
keep loading in the background.

usage: python3 tools/build.py src/columbus-clash.html .
"""
import base64, hashlib, io, os, re, sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
os.makedirs(os.path.join(out, "assets"), exist_ok=True)
# PFX (pixelfx atlases) live in one const; mark their URIs so the loader can skip them
pfx_lo = s.find("const PFX={"); pfx_hi = s.find("};", pfx_lo) if pfx_lo >= 0 else -1
cache, stats = {}, [0, 0]

def repl(m):
    mime, data = m.group(1), m.group(2)
    raw = base64.b64decode(data)
    if data in cache: return cache[data]
    fx = pfx_lo <= m.start() <= pfx_hi
    if mime == "image/png":
        im = Image.open(io.BytesIO(raw)); im.load()
        b = io.BytesIO(); im.save(b, "WEBP", lossless=True, quality=100, method=6, exact=True); raw2 = b.getvalue()
        if len(raw2) >= len(raw): raw2, ext = raw, "png"
        else: ext = "webp"
    else:
        raw2, ext = raw, mime.split("/")[1]
    name = ("fx-" if fx else "") + hashlib.sha1(raw2).hexdigest()[:12] + "." + ext
    with open(os.path.join(out, "assets", name), "wb") as f: f.write(raw2)
    stats[0] += len(data); stats[1] += len(raw2)
    cache[data] = "assets/" + name
    return cache[data]

body = re.sub(r"data:(image/(?:png|webp|jpeg|gif));base64,([A-Za-z0-9+/=]+)", repl, s)

head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">'
        '<meta name="theme-color" content="#0c0714"><meta name="apple-mobile-web-app-capable" content="yes">'
        '<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
        '<meta name="apple-mobile-web-app-title" content="Columbus Clash">'
        '<meta name="description" content="Retro pixel fighting game in the Columbus tavern on Halloween night.">')
loader = r'''<style>#ccload{position:fixed;inset:0;z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:#0c0714;color:#ffd23a;font:bold 14px/1.4 monospace;letter-spacing:.12em;transition:opacity .3s}#ccload i{display:block;width:min(260px,70vw);height:8px;border:2px solid #4a3166;background:#1a0e28}#ccload b{display:block;height:100%;width:0;background:linear-gradient(90deg,#ff7a1a,#ffd23a)}</style>
<script>(()=>{const I=window.Image,L=[];window.Image=function(w,h){const im=new I(w,h);L.push(im);return im;};window.Image.prototype=I.prototype;
const el=document.createElement('div');el.id='ccload';el.innerHTML='<div>COLUMBUS CLASH</div><i><b id="ccbar"></b></i><div id="ccpct" style="color:#b9a4d6;font-size:11px">LOADING 0%</div>';document.documentElement.appendChild(el);
const t0=Date.now(),bar=el.querySelector('#ccbar'),pct=el.querySelector('#ccpct');
const tick=()=>{const c=L.filter(i=>i.src&&i.src.indexOf('/fx-')<0),n=c.length,d=c.filter(i=>i.complete).length,p=n?Math.round(100*d/n):0;
 bar.style.width=p+'%';pct.textContent='LOADING '+p+'%';if((n&&d===n&&Date.now()-t0>300)||Date.now()-t0>20000){el.style.opacity=0;setTimeout(()=>el.remove(),320);return;}setTimeout(tick,100);};
window.addEventListener('DOMContentLoaded',tick);})();</script>'''
# keep any <head> content the source already has; the source starts with <title>/<style>
html = head + loader + body + "</html>\n"
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
print(f"index.html {len(html)/1e6:.2f} MB, assets {stats[1]/1e6:.2f} MB (was {stats[0]/1e6:.2f} MB inline)")
