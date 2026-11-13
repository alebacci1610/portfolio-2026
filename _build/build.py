"""Genera index.html e le pagine progetto a partire da data.py.

Uso, dalla cartella del sito:  python3 _build/build.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import BIO, PHOTO, PROJECTS  # noqa: E402
from images import web_image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTS = json.load(open(os.path.join(os.path.dirname(__file__), "testi_originali.json"), encoding="utf-8"))
FC = "foto copia/"

# colore di ogni progetto (palette: lime, magenta, violet)
ACCENT = {
    "fragma": "magenta", "sound-morphology": "violet", "futbol": "lime",
    "space-debris": "magenta", "esplorami": "violet", "gestures": "lime",
}
# video che parte da solo (cartella video/); chi non ce l'ha usa una sequenza di immagini
VIDEO = {"fragma", "sound-morphology", "futbol", "space-debris"}
START = {"fragma": "#t=9"}  # il video di Fragma parte da una scena, non dal nero iniziale
SLIDES = {
    "esplorami": [FC + "EsploraMI/Tokyo Subway Poster Mockup.jpg", FC + "EsploraMI/mockup instagram flyer.png",
                  FC + "EsploraMI/Screenshot 2026-05-12 alle 17.23.21.png", FC + "EsploraMI/Screenshot 2026-04-10 alle 13.35.55.png"],
    "gestures": [FC + "Gestures/mockup iphone.jpg", FC + "Gestures/home.jpg", FC + "Gestures/Screenshot 2026-04-06 alle 21.05.03.png",
                 FC + "Gestures/Screenshot 2026-04-06 alle 21.05.30.png", FC + "Gestures/Screenshot 2026-04-06 alle 21.06.46.png"],
}

# piccole correzioni ai testi originali
FIXES = {
    "Syntax F-1 un’installazione interattiva analogicodigitale. L’utente": "Syntax F-1, un’installazione interattiva tra analogico e digitale. L’utente",
    "e ad ogni spostamento, un LLM": "e, a ogni spostamento, un LLM",
}

CLAIM = ("Progetto cose che si toccano, si cliccano e ogni tanto si rompono.",
         "I design things you can touch, click and occasionally break.")
BIO_SHORT = (
    "Sono Alessandro, ho 22 anni, vengo da Riccione e studio Design della Comunicazione al Politecnico di Milano. "
    "Lavoro dove il fisico incontra il digitale: progetto l’idea, poi la costruisco, in codice o con le mani.",
    "I’m Alessandro, I’m 22, I come from Riccione and I study Communication Design at Politecnico di Milano. "
    "I work where physical meets digital: I design the idea, then I build it, in code or by hand.",
)

E = html.escape


def bi(it, en):
    return f'<span lang="it">{it}</span><span lang="en">{en}</span>'


def fix(t):
    for a, b in FIXES.items():
        t = t.replace(a, b)
    return t


LANG_SWITCH = ('<div class="lang-switch" role="group" aria-label="Lingua / Language">'
               '<button type="button" data-set-lang="it" aria-label="Italiano">IT</button>'
               '<span class="lang-sep" aria-hidden="true">/</span>'
               '<button type="button" data-set-lang="en" aria-label="English">EN</button></div>')


def head(title, desc, module=False):
    extra = '\n    <script type="module" src="scene.js"></script>' if module else ""
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{E(title)}</title>
    <meta name="description" content="{E(desc)}">
    <link rel="preload" href="fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="fonts/instrument-serif-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="site.css">
    <link rel="stylesheet" href="lang.css">
    <script src="lang.js"></script>
    <script src="fx.js" defer></script>{extra}
</head>"""


def bar(home=False):
    left = '<a href="index.html">Alessandro Bacci</a>'
    pre = "" if home else "index.html"
    return f"""    <header class="bar">
        {left}
        <nav aria-label="Menu">
            <a href="{pre}#progetti">{bi('Progetti', 'Projects')}</a>
            <a href="{pre}#info">Info</a>
            {LANG_SWITCH}
        </nav>
    </header>"""


def img_tag(path, w, h, alt, cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{E(path)}" width="{w}" height="{h}" alt="{E(alt)}"{c}{l}>'


def media(p, lazy=True, size=1600):
    """Il riquadro principale di un progetto: video oppure sequenza di immagini."""
    slug = p["slug"]
    if slug in VIDEO:
        poster, _, _ = web_image(p["card"], slug, max_w=1600, max_h=1600, suffix="-hero")
        if slug != "fragma":
            poster = f"video/{slug}.webp"
        pre = "metadata" if lazy else "auto"
        return (f'<div class="frame bend" data-bend><video data-auto src="video/{slug}.mp4{START.get(slug, "")}" poster="{E(poster)}" '
                f'muted loop playsinline preload="{pre}" aria-label="{E(p["title"])}"></video></div>')
    tags = []
    for k, src in enumerate(SLIDES[slug]):
        ip, iw, ih = web_image(src, slug, max_w=size, max_h=size)
        tags.append(img_tag(ip, iw, ih, p["title"] if k == 0 else "", cls="is-on" if k == 0 else "", lazy=lazy or k > 0))
    return f'<div class="frame bend slides" data-bend data-slides>{"".join(tags)}</div>'


def figure(slug, src, cap_it, cap_en, alt, max_w=2000):
    ip, w, h = web_image(src, slug, max_w=max_w, max_h=max_w)
    cap = f"<figcaption>{bi(E(cap_it), E(cap_en))}</figcaption>" if cap_it else ""
    return f'<figure><div class="bend" data-bend>{img_tag(ip, w, h, alt)}</div>{cap}</figure>'


def foot():
    return """    <footer class="foot">
        <span>Alessandro Bacci, 2026</span>
        <a href="mailto:alebacci2003@gmail.com">alebacci2003@gmail.com</a>
        <a href="https://instagram.com/burdeldesignstudio" target="_blank" rel="noopener">@burdeldesignstudio</a>
    </footer>"""


# ---------------------------------------------------------------- home
def build_home():
    types = []
    for p in PROJECTS:
        if p["type"] not in types:
            types.append(p["type"])
    filters = [f'<button type="button" data-filter="all" aria-pressed="true">{bi("Tutti", "All")}</button>']
    for t in types:
        filters.append(f'<button type="button" data-filter="{E(t[1])}" aria-pressed="false">{bi(*t)}</button>')

    works = []
    for i, p in enumerate(PROJECTS):
        works.append(f"""        <a class="work" href="{p['slug']}.html" data-type="{E(p['type'][1])}" data-accent="{ACCENT[p['slug']]}">
            {media(p, lazy=i > 0)}
            <div class="work-info">
                <h3 class="display" data-swap>{E(p['title'])}</h3>
                <div class="work-meta">
                    <span class="tag" data-scramble>{bi(*p['type'])}</span>
                    <p>{bi(E(p['pitch'][0]), E(p['pitch'][1]))}</p>
                    <span class="label">{p['year']}, {bi(*p['context'])}</span>
                </div>
            </div>
        </a>""")

    ph, pw, phh = web_image(PHOTO, "about", max_w=600, max_h=800)
    scene_data = json.dumps([{"slug": p["slug"], "title": p["title"], "type": list(p["type"]), "accent": ACCENT[p["slug"]]} for p in PROJECTS],
                            ensure_ascii=False)
    page = head("Alessandro Bacci, portfolio", "Portfolio di Alessandro Bacci, interaction e communication designer a Milano.", module=True) + f"""
<body>
    <a class="skip" href="#progetti">{bi('Vai ai progetti', 'Skip to projects')}</a>
{bar(home=True)}

    <section class="stage" aria-label="{E('Apertura')}">
        <canvas id="scene" aria-hidden="true"></canvas>
        <div class="claim">
            <h1 class="display" data-swap>{bi(E(CLAIM[0]), E(CLAIM[1]))}</h1>
            <p class="label hint" data-scramble>{bi('Trascina per ruotare gli oggetti. Clicca per entrare in un progetto.', 'Drag to rotate the objects. Click one to open a project.')}</p>
        </div>
    </section>
    <div class="pointer-label" id="pointer-label" aria-hidden="true"></div>
    <script>window.PROJECTS = {scene_data};</script>

    <main>
        <div class="section-head" id="progetti">
            <h2 class="display" data-swap>{bi('Progetti', 'Projects')}</h2>
            <div class="filters" role="group" aria-label="{E('Filtra per disciplina')}">
                {chr(10).join('                ' + f for f in filters).strip()}
            </div>
        </div>
        <div class="works">
{chr(10).join(works)}
        </div>

        <section class="field info" id="info" data-accent="lime">
            <h2 class="display" data-swap>Info</h2>
            <div class="bio">
                <p>{bi(E(BIO_SHORT[0]), E(BIO_SHORT[1]))}</p>
                <p>{bi('Sono solo un romagnolo a cui piace <i>spataccare</i>: metterci le mani, smontare, provare.', 'I’m just a guy from Romagna who likes to <i>spataccare</i>: to tinker, take things apart and try.')}</p>
            </div>
            <div class="side">
                {img_tag(ph, pw, phh, 'Ritratto di Alessandro Bacci')}
                <address>
                    <a href="mailto:alebacci2003@gmail.com">alebacci2003@gmail.com</a><br>
                    <a href="tel:+393346700302">+39 334 670 0302</a><br>
                    <a href="https://instagram.com/burdeldesignstudio" target="_blank" rel="noopener">@burdeldesignstudio</a>
                </address>
                <a class="btn" href="Alessandro-Bacci-CV.pdf" download>{bi('Scarica il CV (PDF)', 'Download CV (PDF)')}</a>
            </div>
        </section>
    </main>
{foot()}
</body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)


# ---------------------------------------------------------------- pagine progetto
def result_block(p, layout, imgs):
    slug = p["slug"]
    if layout == "wide":
        s, a, b = imgs[0]
        return f'<div class="media-wide">{figure(slug, s, a, b, p["title"])}</div>'
    if layout == "pair":
        return '<div class="media-pair">' + "".join(figure(slug, s, a, b, p["title"], max_w=1300) for s, a, b in imgs) + "</div>"
    tags = []
    for k, (s, _, _) in enumerate(imgs):
        ip, iw, ih = web_image(s, slug, max_w=1100, max_h=1040)
        tags.append(img_tag(ip, iw, ih, f"{p['title']}, schermata {k + 1}"))
    return (f'<div><div class="phones" tabindex="0" aria-label="{E(p["title"])}: schermate del prototipo">{"".join(tags)}</div>'
            f'<p class="label" style="margin-top:10px">{bi("Il prototipo, schermata per schermata. Trascina o scorri di lato.", "The prototype, screen by screen. Drag or scroll sideways.")}</p></div>')


def build_project(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    slug = p["slug"]
    t = TEXTS[slug]

    rows = []
    if p["team"]:
        rows.append(("Team", "<ul>" + "".join(f"<li>{E(n)}</li>" for n in p["team"]) + "</ul>"))
    rows.append((bi("Il mio ruolo", "My role"), "<ul>" + "".join(f'<li class="me">{bi(a, b)}</li>' for a, b in zip(*p["role"])) + "</ul>"))
    rows.append((bi("Contesto", "Context"), f'{bi(*p["context"])}<br>{p["year"]}'))
    if p["link"]:
        rows.append((bi("Sito del progetto", "Project website"), f'<a href="{E(p["link"][0])}" target="_blank" rel="noopener">{E(p["link"][1])} ↗</a>'))
    facts = "\n".join(f"            <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)

    # racconto: testo e immagini si alternano
    blocks = [result_block(p, layout, imgs) for layout, imgs in p["result"]]
    story = []
    for k, (pit, pen) in enumerate(zip(t["it"], t["en"])):
        story.append(f"""        <div class="story-text">
            <h2>{bi(p['headings'][0][k], p['headings'][1][k])}</h2>
            <p lang="it">{fix(pit)}</p>
            <p lang="en">{fix(pen)}</p>
        </div>""")
        if blocks:
            story.append("        " + blocks.pop(0))
    story += ["        " + b for b in blocks]

    process = ""
    if p["process"]:
        figs = "\n        ".join(figure(slug, s, a, b, f"{p['title']}, processo", max_w=1400) for s, a, b in p["process"])
        lead = (bi("Ricerca, schizzi e prototipi: come ci siamo arrivati.", "Research, sketches and prototypes: how we got there.") if p["team"]
                else bi("Ricerca, schizzi e prototipi: come ci sono arrivato.", "Research, sketches and prototypes: how I got there."))
        process = f"""
    <div class="chapter-head">
        <h2 class="display" data-swap>{bi('Dietro le quinte', 'Behind the scenes')}</h2>
        <p>{lead}</p>
    </div>
    <div class="process">
        {figs}
    </div>"""

    page = head(f"{p['title']}, Alessandro Bacci", p["pitch"][0]) + f"""
<body data-accent="{ACCENT[slug]}">
    <a class="skip" href="#contenuto">{bi('Vai al contenuto', 'Skip to content')}</a>
{bar()}

    <main id="contenuto">
    <div class="hero">
        {media(p, lazy=False, size=2000)}
    </div>

    <div class="title-block">
        <div class="stack label">
            <span data-scramble>{bi(*p['type'])}</span>
            <span data-scramble>{p['year']}</span>
            <span data-scramble>{bi(*p['context'])}</span>
        </div>
        <h1 class="display" data-swap>{E(p['title'])}</h1>
        <p class="pitch">{bi(E(p['pitch'][0]), E(p['pitch'][1]))}</p>
    </div>

    <dl class="field facts">
{facts}
    </dl>

    <div class="story">
{chr(10).join(story)}
    </div>
{process}
    </main>

    <a class="field next" href="{nxt['slug']}.html" data-accent="{ACCENT[nxt['slug']]}">
        <span class="label" data-scramble>{bi('Progetto successivo', 'Next project')}</span>
        <strong class="display" data-swap>{E(nxt['title'])}</strong>
    </a>
{foot()}
</body>
</html>
"""
    open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    build_home()
    for i in range(len(PROJECTS)):
        build_project(i)
        print("ok", PROJECTS[i]["slug"])
