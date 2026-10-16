#!/usr/bin/env python3
"""
Generatore del sito statico CrossFit Varese.

Legge i dataset in data/*.json e scrive gli HTML nella radice del progetto.
Usa solo la libreria standard di Python 3: nessuna installazione richiesta.

    python3 tools/build.py

Gli HTML generati sono già nel repository: il sito si pubblica senza build.
Lo script serve solo quando si modificano contenuti o dati.
"""
import json
import html as _html
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


SITO = load("sito")
AZ = load("azienda")
PROG = load("programmi")
ORARI = load("orari")
ABB = load("abbonamenti")
COACH = load("coach")
FAQ = load("faq")

DEMO = bool(SITO["demo"])
BASE = SITO["dominio"].rstrip("/")
# In demo i meta con URL assoluti usano l'indirizzo della demo (se noto), mai il sito attuale.
META_BASE = ((SITO.get("demo_url") or "").rstrip("/") if SITO["demo"] else BASE)
AG = SITO["agenzia"]
esc = _html.escape

ADDR_LINE = f'{AZ["indirizzo"]["via"]}, {AZ["indirizzo"]["comune"]} ({AZ["indirizzo"]["provincia"]}) {AZ["indirizzo"]["cap"]}'


# ---------------------------------------------------------------- utilità
def wa(msg):
    return f'https://wa.me/{AZ["whatsapp"]["numero"]}?text={quote(msg)}'


WA_PROVA = wa(AZ["whatsapp"]["messaggio_prova"])
WA_INFO = wa(AZ["whatsapp"]["messaggio_info"])
TEL = f'tel:{AZ["telefono_tel"]}'
MAIL = f'mailto:{AZ["email"]}'
EXT = 'target="_blank" rel="noopener"'

ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "whatsapp": '<path d="M3 21l1.65-4.9A9 9 0 1 1 8 19.4L3 21z"/><path d="M9 8.5c.4 3 3.2 5.8 6.2 6.2l1.3-1.5-2.1-1-.9.8c-.9-.4-1.8-1.3-2.2-2.2l.8-.9-1-2.1L9 8.5z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "left": '<path d="M15 5l-7 7 7 7"/>',
    "right": '<path d="M9 5l7 7-7 7"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


def lines(text, start=0, tag_attrs=""):
    """Titolo con reveal per riga. `text` può contenere '|' per andare a capo."""
    out = []
    for i, part in enumerate(text.split("|")):
        out.append(f'<span class="line"><span style="--i:{i + start}">{esc(part)}</span></span>')
    return "".join(out)


def btn(label, href, kind="", ico=None, ext=False):
    cls = "btn" + (f" btn--{kind}" if kind else "")
    attrs = f" {EXT}" if ext else ""
    ic = icon(ico) if ico else ""
    return f'<a class="{cls}" href="{esc(href)}"{attrs}>{ic}<span>{esc(label)}</span></a>'


def link_arrow(label, href):
    return f'<a class="link-arrow" href="{esc(href)}"><span>{esc(label)}</span>{icon("arrow")}</a>'


def img(name, alt, w=1200, h=630, cls="", lazy=True, sizes="100vw", eager=False):
    small = name.replace(".webp", "-640.webp")
    load_attr = 'loading="eager" fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}" srcset="assets/img/{small} 640w, assets/img/{name} 1200w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load_attr}>')


PHOTOS = {
    "classe": ("classe-riscaldamento-ampia.webp",
               "Una classe di CrossFit Varese durante il riscaldamento: i partecipanti sollevano i bilancieri sopra la testa nell'ampio spazio del box, con anelli e corde appesi al soffitto."),
    "tecnica": ("coach-tecnica-trazioni.webp",
                "Un coach sostiene una partecipante che esegue un esercizio alla sbarra, mentre altre persone si allenano agli anelli e alle sbarre."),
    "correzione": ("coach-correzione-movimento.webp",
                   "Durante una lezione una persona in maglia verde fluo segue da vicino il movimento di una partecipante, mentre il resto della classe si allena sullo sfondo."),
    "vogatori": ("box-vogatori-attrezzatura.webp",
                 "Partecipanti si allenano sui vogatori in una sala con rig, anelli e kettlebell; sulla parete la scritta CrossFit Varese."),
    "bilancieri": ("classe-bilancieri-box.webp",
                   "La classe esegue un esercizio con il bilanciere davanti alla parete rossa e bianca con il logo CrossFit Varese; sul soffitto anelli e corde."),
}
CAPTIONS = {
    "classe": "La classe durante il riscaldamento",
    "tecnica": "Il coach segue la tecnica alla sbarra",
    "correzione": "Attenzione al movimento durante la lezione",
    "vogatori": "Vogatori, rig e kettlebell",
    "bilancieri": "Bilancieri davanti al logo CrossFit Varese",
}


def photo(key, cls="", sizes="(min-width: 900px) 50vw, 100vw", px=False, reveal=None, w=1200, h=630, pos=None):
    f, alt = PHOTOS[key]
    style = f' style="--pos:{pos}"' if pos else ""
    reveal_attr = f' data-reveal="{reveal}"' if reveal else ""
    inner = img(f, alt, w, h, sizes=sizes)
    if px:
        inner = f'<div class="px" data-parallax="0.08">{inner}</div>'
        cls = (cls + " photo--px").strip()
    return f'<figure class="photo {cls}"{reveal_attr}{style}>{inner}</figure>'


def gallery_item(key, i):
    f, alt = PHOTOS[key]
    return (f'<button class="g-item" type="button" data-full="assets/img/{f}" data-alt="{esc(alt)}" '
            f'data-caption="{esc(CAPTIONS[key])}" aria-label="Ingrandisci la foto: {esc(CAPTIONS[key])}" '
            f'data-reveal="item" style="--i:{i}">'
            f'<figure class="photo">{img(f, alt, sizes="(min-width: 760px) 40vw, 100vw")}</figure></button>')


# ---------------------------------------------------------------- navigazione
NAV = [
    ("index.html", "Home"),
    ("crossfit.html", "Il CrossFit"),
    ("programmi.html", "Programmi"),
    ("orari.html", "Orari"),
    ("abbonamenti.html", "Abbonamenti"),
    ("box.html", "Il box"),
    ("contatti.html", "Contatti"),
]


def demo_prefix():
    return "[DEMO] " if DEMO else ""


def json_ld():
    a = AZ["indirizzo"]
    data = {
        "@context": "https://schema.org",
        "@type": "SportsActivityLocation",
        "name": AZ["nome"],
        "telephone": AZ["telefono"],
        "email": AZ["email"],
        "foundingDate": str(AZ["anno_apertura"]),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": a["via"],
            "postalCode": a["cap"],
            "addressLocality": a["comune"],
            "addressRegion": a["provincia"],
            "addressCountry": "IT",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": AZ["coordinate"]["lat"], "longitude": AZ["coordinate"]["lng"]},
        "hasMap": AZ["maps_url"],
        "sameAs": [AZ["social"]["instagram"]["url"]],
    }
    if META_BASE:
        data["url"] = META_BASE + "/"
        data["image"] = f"{META_BASE}/assets/img/og-image.jpg"
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def layout(page):
    """page: dict(file, title, desc, body, home=False, lightbox=False, ld=False, og_title=None)"""
    f = page["file"]
    title = f'{demo_prefix()}{page["title"]} | {AZ["nome"]}' if f != "index.html" else f'{demo_prefix()}{AZ["nome"]} | Box CrossFit ad Azzate (Varese)'
    desc = page["desc"]
    url = (f"{META_BASE}/" if f == "index.html" else f"{META_BASE}/{f}") if META_BASE else ""
    robots = '<meta name="robots" content="noindex, nofollow">\n  ' if DEMO else ""
    ld = json_ld() if page.get("ld") else ""
    canon = f'<link rel="canonical" href="{url}">' if url else ""
    og_url = f'<meta property="og:url" content="{url}">\n  ' if url else ""
    og_img = (f'<meta property="og:image" content="{META_BASE}/assets/img/og-image.jpg">\n  <meta property="og:image:width" content="1200">\n'
              f'  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="Una classe di CrossFit Varese durante l\'allenamento">') if META_BASE else ""
    body_cls = "has-hero" if page.get("home") else ""
    intro_script = ""
    if page.get("home"):
        intro_script = (
            "try{if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!sessionStorage.getItem('cfv-intro')){"
            "document.documentElement.classList.add('intro-on');sessionStorage.setItem('cfv-intro','1');"
            "setTimeout(function(){document.documentElement.classList.remove('intro-on')},2900)}}catch(e){}"
        )
    head_script = f"<script>document.documentElement.classList.add('js');{intro_script}</script>"

    nav_items = []
    for i, (href, label) in enumerate(NAV):
        cur = ' aria-current="page"' if href == f else ""
        nav_items.append(f'<li style="--i:{i}"><a href="{href}"{cur}>{esc(label)}</a></li>')
    cta_cur = ' aria-current="page"' if f == "prova-gratuita.html" else ""
    nav_html = (
        '<nav class="primary-nav" id="primary-nav" aria-label="Navigazione principale">'
        f'<ul>{"".join(nav_items)}</ul>'
        f'<a class="btn" href="prova-gratuita.html"{cta_cur}><span>Prenota una prova</span></a>'
        "</nav>"
    )

    banner = (
        f'<div class="demo-banner" role="note">{esc(SITO["banner_demo"])} '
        f'<a href="{AG["url"]}" target="_blank" rel="noopener">{esc(AG["nome"])}</a></div>'
    ) if DEMO else ""

    intro = ""
    if page.get("home"):
        intro = (
            '<div class="intro" aria-hidden="true">'
            '<img src="assets/img/logo.png" width="400" height="255" alt="">'
            '<div class="intro-clock"><span data-clock>00:03</span></div></div>'
        )

    footer_links = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for h, l in NAV[1:])
    credit = (
        f'<p class="footer-credit demo-only">{esc(SITO["credito_footer"])} '
        f'<a href="{AG["url"]}" target="_blank" rel="noopener">{esc(AG["nome"])}</a></p>'
    ) if DEMO else ""
    lightbox = ""
    if page.get("lightbox"):
        lightbox = (
            '<dialog class="lightbox" aria-label="Galleria fotografica">'
            '<button class="lb-btn lb-close" type="button" aria-label="Chiudi la galleria">' + icon("x") + '</button>'
            '<div class="lb-inner"><div class="lb-stage"><img src="" alt="" width="1200" height="630"></div>'
            '<div class="lb-bar"><p class="lb-caption" aria-live="polite"></p><div class="lb-controls">'
            '<button class="lb-btn lb-prev" type="button" aria-label="Foto precedente">' + icon("left") + '</button>'
            '<button class="lb-btn lb-next" type="button" aria-label="Foto successiva">' + icon("right") + '</button>'
            '</div></div></div></dialog>'
        )

    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  {robots}<meta name="theme-color" content="#14161a">
  {canon}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="{AZ["nome"]}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  {og_url}{og_img}
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" href="assets/img/favicon-32.png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/BigShouldersDisplay-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/Barlow-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/style.css">
  {head_script}
  {ld}
</head>
<body class="{body_cls}" data-demo="{'true' if DEMO else 'false'}">
  <a class="skip-link" href="#contenuto">Vai al contenuto</a>
  {banner}
  {intro}
  <header class="site-header">
    <div class="container">
      <a class="brand" href="index.html" aria-label="{AZ["nome"]} — Home"><img src="assets/img/logo.png" width="400" height="255" alt="{AZ["nome"]}" style="aspect-ratio:400/255"></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Apri il menu"><span></span></button>
      {nav_html}
    </div>
  </header>
  <main id="contenuto">
{page["body"]}
  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <img src="assets/img/logo.png" width="400" height="255" alt="{AZ["nome"]}" loading="lazy" style="aspect-ratio:400/255">
          <p><strong>{AZ["nome"]}</strong></p>
          <address>{esc(AZ["indirizzo"]["via"])}<br>{AZ["indirizzo"]["cap"]} {AZ["indirizzo"]["comune"]} ({AZ["indirizzo"]["provincia"]})</address>
          {btn("Prenota una prova", "prova-gratuita.html")}
        </div>
        <div>
          <h2>Contatti</h2>
          <ul>
            <li><a href="{TEL}">{esc(AZ["telefono"])}</a></li>
            <li><a href="{MAIL}">{esc(AZ["email"])}</a></li>
            <li><a href="{WA_INFO}" {EXT}>WhatsApp</a></li>
            <li><a class="social" href="{AZ["social"]["instagram"]["url"]}" {EXT}>{icon("instagram")}<span>Instagram @{AZ["social"]["instagram"]["handle"]}</span></a></li>
          </ul>
        </div>
        <div>
          <h2>Il sito</h2>
          <ul>{footer_links}<li><a href="prova-gratuita.html">Prova gratuita</a></li></ul>
        </div>
        <div>
          <h2>CrossFit</h2>
          <ul>
            <li><a href="{AZ["link_ufficiali"]["crossfit_affiliato"]}" {EXT}>Scheda affiliato su CrossFit.com</a></li>
            <li><a href="{AZ["link_ufficiali"]["crossfit_com"]}" {EXT}>CrossFit.com</a></li>
            <li><a href="privacy.html">Privacy</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-base">
        <p>{AZ["nome"]} · P.IVA {AZ["partita_iva"]} · CrossFit® è un marchio registrato di CrossFit, LLC. {AZ["nome"]} è un box affiliato.</p>
        {credit}
      </div>
    </div>
  </footer>
  <div class="sticky-cta" aria-label="Contatto rapido">
    {btn("Prenota una prova", WA_PROVA, "", "whatsapp", ext=True)}
    <a class="btn btn--ghost btn--call" href="{TEL}" aria-label="Chiama {AZ["nome"]}">{icon("phone")}</a>
  </div>
  {lightbox}
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- blocchi riusabili
def sec_head(title, lead=None, extra=""):
    p = f"<p>{esc(lead)}</p>" if lead else ""
    return f'<div class="sec-head"><h2 data-reveal="lines">{lines(title)}</h2>{p}{extra}</div>'


def page_hero(title, lead, photo_name=None, buttons=""):
    style = ""
    cls = "page-hero"
    if photo_name:
        cls += " page-hero--photo"
        style = f' style="--hero-img:url(../img/{photo_name})"'
    btns = f'<div class="btn-row">{buttons}</div>' if buttons else ""
    return (f'<section class="{cls}"{style}><div class="container"><h1>{lines(title)}</h1>'
            f'<p>{esc(lead)}</p>{btns}</div></section>')


def cta_band(title="Prenota una prova", text=None):
    text = text or "Una lezione individuale gratuita con il Personal Trainer: analizziamo le tue esigenze e costruiamo il percorso più adatto ai tuoi obiettivi."
    return f"""
    <section class="section section--red" aria-labelledby="cta-title">
      <div class="container cta-band">
        <div>
          <h2 id="cta-title" data-reveal="lines">{lines(title)}</h2>
          <p>{esc(text)}</p>
          <p class="cta-alt">Oppure scrivici a <a href="{MAIL}">{esc(AZ["email"])}</a></p>
        </div>
        <div class="btn-row">
          {btn("Scrivici su WhatsApp", WA_PROVA, "white", "whatsapp", ext=True)}
          {btn("Chiama " + AZ["telefono"], TEL, "ghost", "phone")}
        </div>
      </div>
    </section>"""


# ---------------------------------------------------------------- pagine
def page_home():
    cards = "".join(
        f'<li data-reveal="item" style="--i:{i}"><a class="card" href="programmi.html#{p["id"]}">'
        f'<h3>{esc(p["nome"])}</h3><p>{esc(p["sintesi"])}</p>'
        f'<span class="link-arrow"><span>Scopri il programma</span>{icon("arrow")}</span></a></li>'
        for i, p in enumerate(PROG["programmi"])
    )
    # le <li> sono dentro .cards (grid): reset stile lista
    steps = [
        ("Contattaci", "Prenota la lezione di prova su WhatsApp, per telefono o via mail."),
        ("Incontra un coach", "Ti alleni con il Personal Trainer, che analizza le tue esigenze."),
        ("Scopri il metodo", "Provi un allenamento di CrossFit e capisci come si lavora in un box."),
        ("Scegli il programma", "Valutate insieme la formula più adatta: classi, On Ramp o lezioni individuali."),
    ]
    steps_html = "".join(
        f'<li data-reveal="item" style="--i:{i}"><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>'
        for i, (t, d) in enumerate(steps)
    )
    owner = COACH["persone"][0]
    body = f"""
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-media" data-parallax="0.18">{img(PHOTOS["classe"][0], PHOTOS["classe"][1], eager=True, sizes="100vw")}</div>
      <div class="container hero-inner">
        <h1 id="hero-title">{lines("Diventa con noi|la versione migliore|di te stesso")}</h1>
        <p class="hero-lead">CrossFit Varese è il primo box CrossFit della provincia di Varese, dal {AZ["anno_apertura"]}. Classi con l'allenamento del giorno, sempre diverso e personalizzato sulle capacità di ciascuno.</p>
        <div class="btn-row">
          {btn("Prenota una prova", "prova-gratuita.html")}
          {btn("Scopri il CrossFit", "crossfit.html", "ghost")}
        </div>
      </div>
      <div class="container">
        <ul class="facts">
          <li><strong>{AZ["anno_apertura"]}</strong><span>Il primo box CrossFit della provincia di Varese</span></li>
          <li><strong>Lun–Sab</strong><span>Classi la mattina, a pranzo e la sera</span></li>
          <li><strong>Gratis</strong><span>La lezione di prova con il Personal Trainer</span></li>
          <li><strong>50+</strong><span>Posti auto gratuiti di fronte al box</span></li>
        </ul>
      </div>
    </section>

    <section class="section section--light" id="crossfit" aria-labelledby="t-crossfit">
      <div class="container split split--wide-media">
        <div>
          <div class="sec-head"><h2 id="t-crossfit" data-reveal="lines">{lines("Che cos'è|il CrossFit")}</h2></div>
          <div class="prose">
            <p>CrossFit è un metodo di allenamento che combina diverse discipline sportive per migliorare le prestazioni fisiche, la forma e la salute a qualsiasi età.</p>
          </div>
          <ul class="pillars">
            <li><h3>Niente macchine</h3><p>Esercizi di ginnastica, pesistica e atletica che attivano tutto il corpo in modo naturale e sicuro.</p></li>
            <li><h3>No alla routine</h3><p>Gli esercizi cambiano ogni giorno, per mantenere lo stimolo sempre al massimo e divertirsi.</p></li>
            <li><h3>Adatto a tutti</h3><p>Non bisogna essere già allenati: il programma si adatta a qualsiasi esigenza.</p></li>
          </ul>
          <p style="margin-top:1.75rem">{link_arrow("Scopri come funziona", "crossfit.html")}</p>
        </div>
        {photo("tecnica", "photo--tall", px=True, reveal="wipe", sizes="(min-width: 900px) 45vw, 100vw", pos=None)}
      </div>
    </section>

    <section class="section section--dark" id="programmi" aria-labelledby="t-prog">
      <div class="container">
        <div class="sec-head"><h2 id="t-prog" data-reveal="lines">{lines("I nostri programmi")}</h2><p>{esc(PROG["introduzione"])}</p></div>
        <ul class="cards">{cards}</ul>
        <p style="margin-top:2rem">{btn("Tutti i programmi", "programmi.html", "ghost")}</p>
      </div>
    </section>

    <section class="section section--concrete" id="come-iniziare" aria-labelledby="t-start">
      <div class="container">
        {sec_head("Come iniziare", "Quattro passi per partire, senza bisogno di essere già allenati.").replace('<h2 data-reveal', '<h2 id="t-start" data-reveal')}
        <ol class="steps">{steps_html}</ol>
        <p class="note">Percorso indicativo: giorni, orari e modalità della prova si concordano direttamente con il box.</p>
      </div>
    </section>

    <section class="section section--dark" id="box" aria-labelledby="t-box">
      <div class="container">
        <div class="split">
          <div>
            <div class="sec-head"><h2 id="t-box" data-reveal="lines">{lines("Il box")}</h2></div>
            <div class="prose">
              <p>Uno spazio ampio e luminoso, con finestre e lucernari, pensato per allenarsi in gruppo. Rig con sbarre e anelli, bilancieri, kettlebell, plyo box e vogatori: l'attrezzatura di un vero box CrossFit.</p>
              <p>Si arriva facilmente dall'autostrada e di fronte all'ingresso c'è un ampio parcheggio gratuito.</p>
            </div>
            <p style="margin-top:1.5rem">{btn("Visita il box", "box.html", "ghost")}</p>
          </div>
          <div class="mosaic">
            <div class="m-a">{gallery_item("vogatori", 0)}</div>
            <div>{gallery_item("bilancieri", 1)}</div>
            <div>{gallery_item("correzione", 2)}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--light" id="coach" aria-labelledby="t-coach">
      <div class="container split">
        {photo("correzione", sizes="(min-width: 900px) 50vw, 100vw", px=True, reveal="wipe")}
        <div>
          <div class="sec-head"><h2 id="t-coach" data-reveal="lines">{lines("Coach|e community")}</h2></div>
          <div class="prose">
            <p>In classe l'allenamento è personalizzato in base alle capacità di ogni partecipante; nelle lezioni individuali ti segue un Personal Trainer.</p>
            <p>Si lavora fianco a fianco, ciascuno al proprio livello: ogni giorno un allenamento diverso, da lunedì a sabato.</p>
            <p><strong>{esc(owner["nome"])}</strong>, {esc(owner["ruolo"].lower())} del box.</p>
          </div>
        </div>
      </div>
    </section>

    {cta_band()}

    <section class="section section--light" id="dove-siamo" aria-labelledby="t-dove">
      <div class="container split">
        <div>
          <div class="sec-head"><h2 id="t-dove" data-reveal="lines">{lines("Dove siamo")}</h2></div>
          <dl class="datalist">
            <div><dt>Indirizzo</dt><dd>{esc(AZ["indirizzo"]["via"])}<br>{AZ["indirizzo"]["cap"]} {AZ["indirizzo"]["comune"]} ({AZ["indirizzo"]["provincia"]})</dd></div>
            <div><dt>Telefono</dt><dd><a href="{TEL}">{esc(AZ["telefono"])}</a></dd></div>
            <div><dt>Email</dt><dd><a href="{MAIL}">{esc(AZ["email"])}</a></dd></div>
          </dl>
          <div class="btn-row" style="margin-top:1.75rem">
            {btn("Apri su Google Maps", AZ["maps_url"], "", "pin", ext=True)}
            {btn("Chiama", TEL, "ink-outline", "phone")}
          </div>
        </div>
        <div class="prose">
          <h3>Come arrivare</h3>
          <p>{esc(AZ["accesso"]["descrizione"])}</p>
          <p>{esc(AZ["accesso"]["parcheggio"])}</p>
        </div>
      </div>
    </section>"""
    return dict(file="index.html", title=AZ["nome"],
                desc="CrossFit Varese ad Azzate: il primo box CrossFit della provincia di Varese, dal 2013. Classi da lunedì a sabato e lezione di prova gratuita con il Personal Trainer.",
                body=body, home=True, lightbox=True, ld=True)


def faq_html(items=None):
    items = items or FAQ["faq"]
    out = "".join(
        f'<details><summary>{esc(i["d"])}</summary><div class="answer"><p>{esc(i["r"])}</p></div></details>' for i in items
    )
    return f'<div class="faq">{out}</div>'


def page_crossfit():
    body = f"""
    {page_hero("Il CrossFit", "Un metodo di allenamento per chi parte da zero e per chi si allena da anni: spiegato semplice, prima di venire in box.", "classe-bilancieri-box.webp", btn("Prenota una prova", "prova-gratuita.html"))}

    <section class="section section--light" aria-labelledby="t1">
      <div class="container split">
        <div>
          <div class="sec-head"><h2 id="t1" data-reveal="lines">{lines("Che cos'è|il CrossFit")}</h2></div>
          <div class="prose">
            <p>CrossFit è un metodo di allenamento che combina diverse discipline sportive per migliorare le prestazioni fisiche, la forma e la salute a qualsiasi età.</p>
            <p>L'allenamento è basato su esercizi di ginnastica, pesistica e atletica che attivano tutto il corpo in modo naturale e sicuro. Non ci sono macchine da gestire: si lavora con il proprio corpo, con bilancieri e con attrezzi semplici.</p>
            <p>Gli esercizi cambiano ogni giorno, per mantenere lo stimolo sempre al massimo.</p>
          </div>
        </div>
        {photo("classe", sizes="(min-width: 900px) 50vw, 100vw", px=True, reveal="wipe")}
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="t2">
      <div class="container">
        {sec_head("Come si svolge una lezione", "Le classi durano un'ora. In generale una lezione di CrossFit segue questa struttura; ordine e durata di ogni parte li decide il coach in base all'allenamento del giorno.").replace('<h2 data-reveal', '<h2 id="t2" data-reveal')}
        <ol class="cards steps-dark" style="list-style:none">
          <li class="card" data-reveal="item" style="--i:0"><h3>Riscaldamento</h3><p>Si prepara il corpo al lavoro, con movimenti che servono anche a ripassare la tecnica.</p></li>
          <li class="card" data-reveal="item" style="--i:1"><h3>Tecnica e forza</h3><p>Il coach spiega e mostra i movimenti previsti: la tecnica viene prima del carico e della velocità.</p></li>
          <li class="card" data-reveal="item" style="--i:2"><h3>Allenamento del giorno</h3><p>Il lavoro principale, sempre diverso, che ognuno svolge secondo le proprie capacità.</p></li>
        </ol>
        <p class="note">Descrizione generale del metodo CrossFit, da confermare con i coach del box per quanto riguarda la struttura esatta delle classi.</p>
      </div>
    </section>

    <section class="section section--concrete" aria-labelledby="t3">
      <div class="container split split--top">
        <div>
          <div class="sec-head"><h2 id="t3" data-reveal="lines">{lines("Tecnica|e progressione")}</h2></div>
          <div class="prose">
            <p>Imparare bene un movimento viene prima di aggiungere peso o velocità. Per questo chi inizia può partire dal corso <a href="programmi.html#on-ramp">On Ramp</a>: 6 lezioni per imparare i movimenti fondamentali, in piccoli gruppi di massimo 4 persone con il Personal Trainer.</p>
            <p>In classe l'allenamento del giorno è personalizzato in base alle capacità di ogni partecipante: non bisogna essere già allenati, il programma si adatta a qualsiasi esigenza e permette a chiunque di migliorare.</p>
          </div>
        </div>
        <div>
          <div class="sec-head"><h2 data-reveal="lines">{lines("Cosa aspettarsi|dalla prova")}</h2></div>
          <div class="prose">
            <p>La prova è una lezione individuale gratuita con il Personal Trainer. Insieme analizziamo le tue esigenze e programmiamo il percorso ideale per raggiungere i tuoi obiettivi.</p>
            <p>Abbigliamento, durata e giorno li concordi con il box al momento della prenotazione. Se hai problemi di salute o dubbi sulla tua condizione fisica, parlane con il tuo medico prima di iniziare e segnalalo al coach.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--light" aria-labelledby="t4">
      <div class="container">
        {sec_head("Domande frequenti").replace('<h2 data-reveal', '<h2 id="t4" data-reveal')}
        {faq_html()}
      </div>
    </section>

    {cta_band()}"""
    return dict(file="crossfit.html", title="Che cos'è il CrossFit",
                desc="Che cos'è il CrossFit, come si svolge una lezione, come si lavora su tecnica e progressione e cosa aspettarsi dalla prova gratuita a CrossFit Varese, ad Azzate.",
                body=body)


def prog_block(p):
    spec = []
    for key, label in [("obiettivo", "Obiettivo"), ("destinatari", "Per chi"), ("prerequisiti", "Prerequisiti"),
                       ("formato", "Formato"), ("orari", "Orari")]:
        if p.get(key):
            val = esc(p[key])
            if key == "orari" and p.get("orari_link"):
                val += f' <a href="{p["orari_link"]}">Vedi gli orari</a>'
            spec.append(f"<div><dt>{label}</dt><dd>{val}</dd></div>")
    msg = wa(f"Ciao CrossFit Varese, vorrei avere informazioni sul programma {p['nome']}.")
    return f"""
        <article class="program" id="{p["id"]}" data-reveal="item">
          <div>
            <h2>{esc(p["nome"])}</h2>
            <p class="tagline">{esc(p["sintesi"])}</p>
          </div>
          <div>
            <p>{esc(p["descrizione"])}</p>
            <dl class="spec">{"".join(spec)}</dl>
            <div class="btn-row">{btn("Chiedi informazioni", msg, "", "whatsapp", ext=True)}{btn("Prenota una prova", "prova-gratuita.html", "ghost")}</div>
          </div>
        </article>"""


def page_programmi():
    nav = "".join(f'<a href="#{p["id"]}">{esc(p["nome"])}</a>' for p in PROG["programmi"])
    blocks = "".join(prog_block(p) for p in PROG["programmi"])
    body = f"""
    {page_hero("Programmi", PROG["introduzione"], "coach-tecnica-trazioni.webp", btn("Prenota una prova", "prova-gratuita.html"))}
    <section class="section section--dark">
      <div class="container">
        <nav class="program-nav" aria-label="Programmi">{nav}</nav>
        {blocks}
      </div>
    </section>
    {cta_band("Non sai da dove partire?", "Prenota la lezione di prova gratuita: con il Personal Trainer valuti quale programma è più adatto a te.")}"""
    return dict(file="programmi.html", title="Programmi e corsi",
                desc="I programmi di CrossFit Varese: On Ramp per principianti, Classe, Specialty, Ego, Personal e attività extra come Clinic, Workshop e Bootcamp all'aperto.",
                body=body)


def cell(fasce_by_start, start):
    f = fasce_by_start.get(start)
    if not f:
        return '<td data-empty></td>'
    label = f'{f["inizio"]}–{f["fine"]}'
    chips = "".join(f'<span class="chip chip--{t}">{esc(ORARI["tipi"][t])}</span>' for t in f["tipi"])
    return (f'<td data-label="{label}"><span class="range">{label}</span>'
            f'<div class="chips">{chips}</div></td>')


def page_orari():
    cols = ORARI["colonne"]
    head = "".join(f'<th scope="col">{c}</th>' for c in cols)
    rows = []
    for g in ORARI["giorni"]:
        by = {f["inizio"]: f for f in g["fasce"]}
        cells = "".join(cell(by, c) for c in cols)
        rows.append(f'<tr><th scope="row">{esc(g["giorno"])}</th>{cells}</tr>')
    legend = "".join(f'<li><span class="chip chip--{k}">{esc(v)}</span></li>' for k, v in ORARI["tipi"].items())
    body = f"""
    {page_hero("Orari", "Da lunedì a sabato: la mattina, in pausa pranzo e la sera. Decidi tu quando allenarti, in classe o individualmente.", None, btn("Prenota una prova", "prova-gratuita.html"))}
    <section class="section section--light" aria-labelledby="t-orari">
      <div class="container">
        <h2 id="t-orari" class="sr-only">Tabella degli orari</h2>
        <div class="avviso" role="note"><p><strong>Da confermare.</strong> {esc(ORARI["avviso"])}</p></div>
        <ul class="legend" aria-label="Legenda">{legend}</ul>
        <table class="schedule">
          <caption class="sr-only">Orario settimanale delle classi e delle lezioni individuali, per giorno e fascia oraria</caption>
          <thead><tr><th scope="col"><span class="sr-only">Giorno</span></th>{head}</tr></thead>
          <tbody>{"".join(rows)}</tbody>
        </table>
        <div class="prose" style="margin-top:2.5rem">
          <ul class="ticks">
            <li><strong>Class</strong>: l'allenamento del giorno in gruppo, adatto a ogni età e livello.</li>
            <li><strong>Individual</strong>: lezioni individuali con il Personal Trainer, nell'area riservata.</li>
            <li><strong>On Ramp</strong>: il corso di inserimento per principianti, in small group.</li>
            <li><strong>Clinic (Extra)</strong>: attività tematica in aggiunta alle classi.</li>
          </ul>
          <p>Per chiedere disponibilità o prenotare un posto contatta il box: <a href="{WA_INFO}" {EXT}>WhatsApp</a>, <a href="{TEL}">{esc(AZ["telefono"])}</a> oppure <a href="{MAIL}">{esc(AZ["email"])}</a>.</p>
        </div>
      </div>
    </section>
    {cta_band()}"""
    return dict(file="orari.html", title="Orari delle lezioni",
                desc="Orari delle classi di CrossFit Varese da lunedì a sabato: mattina, pausa pranzo e sera, con lezioni individuali, On Ramp per principianti e attività extra.",
                body=body)


def plan_block(p, i):
    dl = [f'<div><dt>Lezioni</dt><dd>{esc(p["lezioni"])}</dd></div>']
    if p.get("limitazioni"):
        dl.append(f'<div><dt>Condizioni</dt><dd>{esc(p["limitazioni"])}</dd></div>')
    dl.append("<div><dt>Prezzo</dt><dd>Chiedi la tariffa aggiornata</dd></div>")
    msg = wa(f"Ciao CrossFit Varese, vorrei informazioni su tariffe e iscrizione alla formula {p['nome']}.")
    return (f'<li class="plan" data-reveal="item" style="--i:{i % 3}"><p class="kind">{esc(p["tipo"])}</p>'
            f'<h3>{esc(p["nome"])}</h3><p>{esc(p["descrizione"])}</p><dl>{"".join(dl)}</dl>'
            f'{btn("Chiedi informazioni", msg, "dark", "whatsapp", ext=True)}</li>')


def page_abbonamenti():
    plans = "".join(plan_block(p, i) for i, p in enumerate(ABB["formule"]))
    body = f"""
    {page_hero("Abbonamenti", "Con abbonamento o con ingressi, in classe o individualmente: scegli la formula adatta al tuo ritmo.", None, btn("Prenota una prova", "prova-gratuita.html"))}
    <section class="section section--concrete" aria-labelledby="t-abb">
      <div class="container">
        <h2 id="t-abb" class="sr-only">Le formule</h2>
        <div class="price-note">
          <div><h2>Tariffe aggiornate su richiesta</h2><p>{esc(ABB["avviso"])}</p></div>
          {btn("Chiedi le tariffe", wa("Ciao CrossFit Varese, vorrei conoscere le tariffe aggiornate."), "", "whatsapp", ext=True)}
        </div>
        <ul class="plans">{plans}</ul>
        <p class="note">Non è previsto alcun pagamento online: l'iscrizione si definisce direttamente con il box.</p>
      </div>
    </section>
    {cta_band("Inizia con una prova", "Prima di scegliere una formula puoi provare: lezione individuale gratuita con il Personal Trainer.")}"""
    return dict(file="abbonamenti.html", title="Abbonamenti e formule",
                desc="Le formule di CrossFit Varese: Open 6 Classi, Open 3 Classi, Under 21, On Ramp, Drop-in e Personal. Chiedi al box le tariffe aggiornate.",
                body=body)


def page_box():
    gallery = "".join(f'<li>{gallery_item(k, i)}</li>' for i, k in enumerate(["classe", "vogatori", "bilancieri", "tecnica", "correzione"]))
    body = f"""
    {page_hero("Il box", "Uno spazio ampio e luminoso, attrezzato per allenarsi in gruppo. Ecco cosa trovi entrando.", "box-vogatori-attrezzatura.webp", btn("Prenota una prova", "prova-gratuita.html"))}

    <section class="section section--light" aria-labelledby="t-spazi">
      <div class="container split">
        <div>
          <div class="sec-head"><h2 id="t-spazi" data-reveal="lines">{lines("Lo spazio")}</h2></div>
          <div class="prose">
            <p>Un'unica grande sala con finestre e lucernari che portano luce naturale, pareti bianche con dettagli rossi e una pavimentazione scura.</p>
            <p>Gli attrezzi sono quelli di un box CrossFit: niente file di macchine, ma spazio per muoversi, sollevare e lavorare in gruppo.</p>
          </div>
        </div>
        {photo("classe", sizes="(min-width: 900px) 50vw, 100vw", px=True, reveal="wipe")}
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="t-attr">
      <div class="container split">
        <div>
          <div class="sec-head"><h2 id="t-attr" data-reveal="lines">{lines("L'attrezzatura")}</h2></div>
          <ul class="ticks prose">
            <li>Rig con sbarre, anelli e corde per la ginnastica</li>
            <li>Bilancieri e dischi per la pesistica</li>
            <li>Kettlebell</li>
            <li>Plyo box</li>
            <li>Vogatori</li>
          </ul>
        </div>
        <div>
          <div class="sec-head"><h2 data-reveal="lines">{lines("Ambiente|e community")}</h2></div>
          <div class="prose">
            <p>Le classi sono momenti in cui si lavora insieme, ciascuno al proprio livello, con un allenamento sempre diverso. Che tu sia alla prima lezione o ti alleni da anni, troverai spazio e persone con cui condividere la fatica.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--concrete" aria-labelledby="t-gal">
      <div class="container">
        {sec_head("Galleria", "Tocca una foto per ingrandirla.").replace('<h2 data-reveal', '<h2 id="t-gal" data-reveal')}
        <ul class="gallery-grid">{gallery}</ul>
        <p class="note">Fotografie: DOMGARGA.</p>
      </div>
    </section>

    <section class="section section--light" aria-labelledby="t-acc">
      <div class="container split">
        <div>
          <div class="sec-head"><h2 id="t-acc" data-reveal="lines">{lines("Come arrivare")}</h2></div>
          <div class="prose"><p>{esc(AZ["accesso"]["descrizione"])}</p><p>{esc(AZ["accesso"]["parcheggio"])}</p></div>
        </div>
        <div>
          <dl class="datalist"><div><dt>Indirizzo</dt><dd>{esc(AZ["indirizzo"]["via"])}<br>{AZ["indirizzo"]["cap"]} {AZ["indirizzo"]["comune"]} ({AZ["indirizzo"]["provincia"]})</dd></div></dl>
          <div class="btn-row" style="margin-top:1.5rem">{btn("Apri su Google Maps", AZ["maps_url"], "", "pin", ext=True)}</div>
        </div>
      </div>
    </section>
    {cta_band()}"""
    return dict(file="box.html", title="Il box",
                desc="Il box di CrossFit Varese ad Azzate: uno spazio ampio e luminoso con rig, bilancieri, kettlebell e vogatori, parcheggio gratuito e uscita Azzate-Buguggiate a pochi minuti.",
                body=body, lightbox=True)


def page_contatti():
    ig = AZ["social"]["instagram"]
    body = f"""
    {page_hero("Contatti", "Domande? Siamo qui per te. Scegli il canale che preferisci.", None, btn("Prenota una prova", "prova-gratuita.html"))}
    <section class="section section--concrete" aria-labelledby="t-cont">
      <div class="container">
        <h2 id="t-cont" class="sr-only">Come contattarci</h2>
        <div class="contact-grid">
          <div class="contact-card">{icon("whatsapp", "icon")}<h2>WhatsApp</h2><p>Scrivici per informazioni o per prenotare la prova.</p>{btn("Apri WhatsApp", WA_INFO, "", "whatsapp", ext=True)}</div>
          <div class="contact-card">{icon("phone", "icon")}<h2>Telefono</h2><a class="big" href="{TEL}">{esc(AZ["telefono"])}</a><p>Chiamaci per parlare direttamente con il box.</p></div>
          <div class="contact-card">{icon("mail", "icon")}<h2>Email</h2><a class="big" href="{MAIL}">{esc(AZ["email"])}</a><p>Per richieste e informazioni.</p></div>
          <div class="contact-card">{icon("pin", "icon")}<h2>Indirizzo</h2><address class="big" style="font-style:normal">{esc(AZ["indirizzo"]["via"])}<br>{AZ["indirizzo"]["cap"]} {AZ["indirizzo"]["comune"]} ({AZ["indirizzo"]["provincia"]})</address>{btn("Apri su Google Maps", AZ["maps_url"], "dark", "pin", ext=True)}</div>
          <div class="contact-card">{icon("instagram", "icon")}<h2>Instagram</h2><a class="big" href="{ig["url"]}" {EXT}>@{ig["handle"]}</a><p>Il profilo ufficiale del box.</p></div>
          <div class="contact-card"><h2>Come arrivare</h2><p>{esc(AZ["accesso"]["descrizione"])}</p><p>{esc(AZ["accesso"]["parcheggio"])}</p></div>
        </div>
      </div>
    </section>
    {cta_band()}"""
    return dict(file="contatti.html", title="Contatti",
                desc="Contatta CrossFit Varese: telefono, WhatsApp, email e indirizzo in Via I Maggio 10/A ad Azzate (VA). Prenota la tua lezione di prova gratuita.",
                body=body, ld=True)


def page_prova():
    DEMO_NOTE = ('<div class="avviso demo-only" role="note" style="margin-top:2.5rem"><p><strong>Nota per la demo.</strong> '
                 "Il calendario di prenotazione online del sito attuale (Fitogram) non risulta raggiungibile: in questa proposta la prova si prenota "
                 "tramite i contatti ufficiali del box. L'integrazione di un eventuale sistema online va concordata con il titolare.</p></div>") if DEMO else ""
    def chan(ico, title, text, button):
        return f'<div class="contact-card" data-reveal="item">{icon(ico, "icon")}<h2>{title}</h2><p>{text}</p>{button}</div>'
    body = f"""
    {page_hero("Prova gratuita", "Una lezione individuale con il Personal Trainer, per provare un allenamento di CrossFit e scoprire come raggiungere i tuoi obiettivi.", "coach-correzione-movimento.webp")}
    <section class="section section--light" aria-labelledby="t-prova">
      <div class="container">
        <div class="sec-head"><h2 id="t-prova" data-reveal="lines">{lines("Prenota la tua prova")}</h2><p>Scegli come contattarci: ti aiutiamo a scegliere giorno e orario.</p></div>
        <div class="contact-grid contact-grid--3">
          {chan("whatsapp", "WhatsApp", "Apri la chat con il messaggio già pronto: devi solo inviarlo.", btn("Scrivici su WhatsApp", WA_PROVA, "", "whatsapp", ext=True))}
          {chan("phone", "Telefono", f'<a href="{TEL}">{esc(AZ["telefono"])}</a>', btn("Chiama ora", TEL, "dark", "phone"))}
          {chan("mail", "Email", f'<a href="{MAIL}">{esc(AZ["email"])}</a>', btn("Scrivi una mail", MAIL + "?subject=" + quote("Richiesta lezione di prova gratuita"), "ink-outline", "mail"))}
        </div>
        <div class="prose" style="margin-top:3rem">
          <h3>Cosa succede nella prova</h3>
          <p>Vieni a provare una lezione introduttiva con il Personal Trainer: analizziamo le tue esigenze e programmiamo il percorso più adatto per raggiungere i tuoi obiettivi.</p>
          <p>Se non hai mai fatto CrossFit, leggi <a href="crossfit.html">come funziona</a> o scopri il corso <a href="programmi.html#on-ramp">On Ramp</a> pensato per i principianti.</p>
        </div>
        {DEMO_NOTE}
      </div>
    </section>"""
    return dict(file="prova-gratuita.html", title="Prova gratuita",
                desc="Prenota la lezione di prova gratuita con il Personal Trainer a CrossFit Varese, ad Azzate: scrivici su WhatsApp, chiamaci o mandaci una mail.",
                body=body)


def page_privacy():
    body = f"""
    {page_hero("Privacy", "Informazioni sul trattamento dei dati personali. Pagina in bozza, da completare con il titolare e con il consulente responsabile.")}
    <section class="section section--light">
      <div class="container legal">
        <div class="todo" role="note">
          <p><strong>Bozza da completare prima della pubblicazione.</strong> Questa pagina descrive come funziona oggi il sito proposto e indica ciò che va verificato. Non è un'informativa legale completa e non sostituisce la consulenza di un professionista.</p>
        </div>

        <h2>Titolare del trattamento</h2>
        <p>{AZ["nome"]}, {esc(ADDR_LINE)}. Partita IVA {AZ["partita_iva"]}. Email: <a href="{MAIL}">{esc(AZ["email"])}</a>.</p>
        <div class="todo"><p>Da completare: ragione sociale, eventuale referente privacy, recapito per l'esercizio dei diritti.</p></div>

        <h2>Dati raccolti da questo sito</h2>
        <ul>
          <li><strong>Moduli:</strong> il sito non contiene moduli di raccolta dati. Le richieste arrivano solo se scegli di contattare il box.</li>
          <li><strong>Cookie e analisi:</strong> il sito non utilizza cookie di profilazione, strumenti di analisi o tracciamento. Il browser conserva solo un'informazione tecnica temporanea (sessionStorage) per non ripetere l'animazione iniziale.</li>
          <li><strong>Font e immagini:</strong> sono ospitati sul sito stesso, senza richieste a servizi esterni.</li>
        </ul>

        <h2>Contatti e prenotazione della prova</h2>
        <p>La lezione di prova si prenota tramite contatti diretti:</p>
        <ul>
          <li><strong>WhatsApp:</strong> il pulsante apre l'app con un messaggio precompilato. I dati che invii (numero di telefono, nome, contenuto) sono trattati dal box per rispondere alla richiesta e da WhatsApp secondo la sua informativa.</li>
          <li><strong>Telefono ed email:</strong> i dati che comunichi sono usati solo per rispondere e organizzare la prova.</li>
        </ul>

        <h2>Collegamenti a servizi esterni</h2>
        <p>Il sito contiene collegamenti a Google Maps, Instagram, WhatsApp e CrossFit.com. Aprendoli lasci questo sito e valgono le informative dei rispettivi gestori.</p>

        <h2>Da verificare prima della pubblicazione</h2>
        <div class="todo">
          <ul>
            <li>Base giuridica, finalità, tempi di conservazione e diritti dell'interessato (artt. 13-14 GDPR).</li>
            <li>Se il sito attuale usa un sistema di prenotazione online (Fitogram) con raccolta dati: informativa e nomina del fornitore a responsabile del trattamento.</li>
            <li>Eventuale aggiunta di strumenti di analisi, mappe incorporate o moduli: aggiornare questa pagina e valutare il banner cookie.</li>
            <li>Gestione dei dati degli iscritti in palestra (certificati medici, tesseramento): fuori dall'ambito del sito.</li>
          </ul>
        </div>
      </div>
    </section>"""
    return dict(file="privacy.html", title="Privacy",
                desc="Informazioni sul trattamento dei dati personali di CrossFit Varese (bozza da completare con il titolare).",
                body=body)


PAGES = [page_home, page_crossfit, page_programmi, page_orari, page_abbonamenti, page_box, page_contatti, page_prova, page_privacy]


def main():
    written = []
    for fn in PAGES:
        p = fn()
        out = layout(p)
        (ROOT / p["file"]).write_text(out, encoding="utf-8")
        written.append(p["file"])

    today = date.today().isoformat()
    urls = []
    for f in written:
        loc = f"{BASE}/" if f == "index.html" else f"{BASE}/{f}"
        pr = "1.0" if f == "index.html" else ("0.3" if f == "privacy.html" else "0.8")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    if DEMO:
        robots = "# Versione DEMO: non indicizzare.\nUser-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"Generate {len(written)} pagine (demo={'ON' if DEMO else 'OFF'}).")


if __name__ == "__main__":
    main()
