#!/usr/bin/env python3
"""Verifiche statiche sul sito generato: link interni, ancore, requisiti demo, H1, alt, immagini."""
import re, sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
pages = sorted(ROOT.glob("*.html"))
problems = []

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ids=set(); s.h1=0; s.imgs=[]; s.meta={}; s.title=""; s._t=False; s.body={}; s.srcs=[]
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "a" and "href" in a: s.links.append((a["href"], a))
        if tag == "h1": s.h1 += 1
        if tag == "img": s.imgs.append(a)
        if tag == "meta" and a.get("name"): s.meta[a["name"]] = a.get("content", "")
        if tag == "meta" and a.get("property"): s.meta[a["property"]] = a.get("content", "")
        if tag == "title": s._t = True
        if tag == "body": s.body = a
        if tag in ("link",) and a.get("href"): s.srcs.append(a["href"])
        if tag in ("script",) and a.get("src"): s.srcs.append(a["src"])
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
    def handle_data(s, d):
        if s._t: s.title += d

parsed = {}
for f in pages:
    p = P(); p.feed(f.read_text(encoding="utf-8")); parsed[f.name] = p

for name, p in parsed.items():
    if p.h1 != 1: problems.append(f"{name}: H1 = {p.h1}")
    if not p.title.startswith("[DEMO] ") and p.body.get("data-demo") == "true": problems.append(f"{name}: manca prefisso [DEMO]")
    if p.meta.get("robots") != "noindex, nofollow" and p.body.get("data-demo") == "true": problems.append(f"{name}: manca noindex")
    if not p.meta.get("description"): problems.append(f"{name}: manca description")
    if not p.meta.get("og:title") or not p.meta.get("og:description"): problems.append(f"{name}: OG incompleto")
    for im in p.imgs:
        if "alt" not in im: problems.append(f"{name}: img senza alt {im.get('src')}")
        if not (im.get("width") and im.get("height")): problems.append(f"{name}: img senza width/height {im.get('src')}")
        src = im.get("src","")
        if src and not (ROOT/src).exists() and src: problems.append(f"{name}: img mancante {src}")
    for s in p.srcs:
        if not s.startswith("http") and not (ROOT/s).exists(): problems.append(f"{name}: risorsa mancante {s}")
    tram = [a for h,a in p.links if h == "https://tramontis.netlify.app/"]
    if len(tram) < 2: problems.append(f"{name}: link Tramontis < 2 ({len(tram)})")
    for a in tram:
        if a.get("target") != "_blank" or "noopener" not in a.get("rel",""): problems.append(f"{name}: link Tramontis senza target/rel")
    html = (ROOT/name).read_text(encoding="utf-8")
    if "Proposta di sito realizzata da" not in html: problems.append(f"{name}: manca credito footer")
    if "VERSIONE DEMO — Proposta di sito non ancora attiva. Per pubblicarla sul vostro dominio contatta" not in html: problems.append(f"{name}: banner demo")
    for h, a in p.links:
        if h.startswith(("http", "mailto:", "tel:")): 
            if h.startswith("http") and a.get("target") == "_blank" and "noopener" not in a.get("rel",""): problems.append(f"{name}: _blank senza noopener {h}")
            continue
        path, _, frag = h.partition("#")
        tgt = path or name
        if tgt not in parsed: problems.append(f"{name}: link interno rotto {h}")
        elif frag and frag not in parsed[tgt].ids: problems.append(f"{name}: ancora mancante {h}")

print(f"{len(pages)} pagine controllate")
print("\n".join(problems) if problems else "Nessun problema trovato")
sys.exit(1 if problems else 0)
