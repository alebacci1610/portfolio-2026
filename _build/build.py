"""Genera index.html e le pagine progetto a partire da data.py.

Uso, dalla cartella del sito:  python3 _build/build.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import BIO, PHOTO, PROJECTS  # noqa: E402
from images import web_image, web_video  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTS = json.load(open(os.path.join(os.path.dirname(__file__), "testi_originali.json"), encoding="utf-8"))

# piccole correzioni ai testi originali
FIXES = {
    "Syntax F-1 un’installazione interattiva analogicodigitale. L’utente": "Syntax F-1, un’installazione interattiva tra analogico e digitale. L’utente",
    "e ad ogni spostamento, un LLM": "e, a ogni spostamento, un LLM",
}

E = html.escape
FONTS = '<link rel="preload" href="fonts/anybody-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>'

CONTACTS = (
    '<a href="mailto:alebacci2003@gmail.com">alebacci2003@gmail.com</a><br>'
    '<a href="tel:+393346700302">+39 334 670 0302</a><br>'
    '<a href="https://instagram.com/burdeldesignstudio" target="_blank" rel="noopener">@burdeldesignstudio</a>'
)

LANG_SWITCH = ('<div class="lang-switch" role="group" aria-label="Lingua / Language">'
               '<button type="button" data-set-lang="it" aria-label="Italiano">IT</button>'
               '<span class="lang-sep" aria-hidden="true">/</span>'
               '<button type="button" data-set-lang="en" aria-label="English">EN</button></div>')


def bi(it, en):
    return f'<span lang="it">{it}</span><span lang="en">{en}</span>'


def fix(t):
    for a, b in FIXES.items():
        t = t.replace(a, b)
    return t


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{E(title)}</title>
    <meta name="description" content="{E(desc)}">
    <meta name="theme-color" content="#2f5e4f">
    {FONTS}
    <link rel="stylesheet" href="site.css">
    <link rel="stylesheet" href="lang.css">
    <script src="lang.js"></script>
    <script src="table.js" defer></script>
</head>"""


def img_tag(path, w, h, alt, cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{E(path)}" width="{w}" height="{h}" alt="{E(alt)}"{c}{l}{extra}>'


def figure(slug, src, cap_it, cap_en, alt, max_w=2000):
    p, w, h = web_image(src, slug, max_w=max_w, max_h=max_w)
    cap = f"\n            <figcaption>{bi(E(cap_it), E(cap_en))}</figcaption>" if cap_it else ""
    return f"""<figure>
            {img_tag(p, w, h, alt)}{cap}
        </figure>"""


def card(p, extra_attrs="", lazy=False):
    src, w, h = web_image(p["card"], p["slug"], max_w=900, max_h=900, suffix="-card")
    return src, w, h


# ---------------------------------------------------------------- home
HOME_LAYOUT = {  # posizione "spataccata" iniziale: frazione dello spazio libero + rotazione
    "fragma": (0.33, 0.40, -5),
    "sound-morphology": (0.60, 0.22, 4),
    "futbol": (0.90, 0.47, -3),
    "space-debris": (0.20, 0.96, 6),
    "esplorami": (0.50, 0.80, -7),
    "gestures": (0.76, 0.98, 5),
}


def build_home():
    prints = []
    for i, p in enumerate(PROJECTS):
        src, w, h = card(p)
        mx, my, r = HOME_LAYOUT[p["slug"]]
        meta = f'{bi(p["type"][0], p["type"][1])}, {p["year"]}'
        prints.append(f"""        <a class="print print--project" href="{p['slug']}.html" data-drag data-kind="project" data-mx="{mx}" data-my="{my}" data-r="{r}">
            {img_tag(src, w, h, '', lazy=False)}
            <span class="print-label"><span class="print-title">{E(p['title'])}</span><span class="print-meta">{meta}</span></span>
        </a>""")
    ph, pw, phh = web_image(PHOTO, "about", max_w=600, max_h=800)
    bio_it, bio_en = BIO
    html_out = head("Alessandro Bacci, portfolio", "Portfolio di Alessandro Bacci, interaction e communication designer a Milano.") + f"""
<body class="home">
    <a class="skip" href="#progetti">{bi('Vai ai progetti', 'Skip to projects')}</a>

    <main class="mat table" id="tavolo">
        <div class="imprint imprint--name">
            <h1 class="name">Alessandro Bacci</h1>
            <p class="role">{bi('Interaction &amp; communication designer, Milano', 'Interaction &amp; communication designer, Milan')}</p>
        </div>

        <div class="controls">
            <button type="button" class="tidy-btn" aria-pressed="false"><span class="when-messy">{bi('Metti in ordine', 'Tidy up')}</span><span class="when-tidy" hidden>{bi('Spataccia', 'Mess it up')}</span></button>
            {LANG_SWITCH}
        </div>

        <p class="imprint imprint--contacts">{CONTACTS}</p>

        <div class="imprint imprint--motto">
            <p>{bi('Sono solo un romagnolo a cui piace <i>spataccare</i>.', 'I’m just a guy from Romagna who likes to <i>spataccare</i>: to tinker, to make a glorious mess.')}</p>
            <p class="hint">{bi('Trascina le stampe, lanciale, cliccane una per aprirla.', 'Drag the prints, throw them, click one to open it.')}</p>
        </div>

        <nav id="progetti" aria-label="{E('Progetti')}">
{chr(10).join(prints)}
        </nav>

        <div class="print print--photo" data-drag data-kind="photo" data-mx="0.985" data-my="0.06" data-r="3">
            {img_tag(ph, pw, phh, 'Ritratto di Alessandro Bacci', cls='', lazy=False)}
            <span class="print-label"><span class="print-title">{bi('Ciao, sono io', 'Hi, that’s me')}</span><span class="print-meta">Riccione, Milano</span></span>
        </div>

        <div class="print print--note" data-drag data-kind="note" data-mx="0.0" data-my="0.62" data-r="-2">
            <p lang="it">{E(bio_it)}</p>
            <p lang="en">{E(bio_en)}</p>
        </div>
    </main>

    <script>
    document.addEventListener('DOMContentLoaded', function () {{
        var mat = document.getElementById('tavolo');
        var btn = document.querySelector('.tidy-btn');
        var body = document.body;
        var mobile = function () {{ return window.innerWidth < 860; }};
        var snap = function (v, e, g) {{ return e + Math.round((v - e) / g) * g; }};

        // calcola la disposizione ordinata e l'altezza del tavolo
        function slots(board) {{
            var css = getComputedStyle(document.documentElement);
            var g = parseFloat(css.getPropertyValue('--grid')), e = parseFloat(css.getPropertyValue('--edge'));
            var W = mat.clientWidth;
            var gap = g;
            var name = document.querySelector('.imprint--name');
            var y0 = snap(name.offsetTop + name.offsetHeight + 36, e, g);
            var x0 = snap(e + 8, e, g);
            var photo = board.items.filter(function (i) {{ return i.el.dataset.kind === 'photo'; }})[0];
            var note = board.items.filter(function (i) {{ return i.el.dataset.kind === 'note'; }})[0];
            var projects = board.items.filter(function (i) {{ return i.el.dataset.kind === 'project'; }});
            var out = new Map(), bottom = 0;
            if (!mobile()) {{
                out.set(photo, [x0, y0]);
                out.set(note, [x0, snap(y0 + photo.el.offsetHeight + gap, e, g)]);
                var gx = snap(x0 + note.el.offsetWidth + g * 3, e, g);
                var cw = projects[0].el.offsetWidth;
                var cols = Math.max(1, Math.min(3, Math.floor((W - 28 - gx + gap) / (cw + gap))));
                var y = y0, rowH = 0;
                projects.forEach(function (it, i) {{
                    var c = i % cols;
                    if (c === 0 && i) {{ y = snap(y + rowH + gap, e, g); rowH = 0; }}
                    out.set(it, [gx + c * (cw + gap), y]);
                    rowH = Math.max(rowH, it.el.offsetHeight);
                }});
                bottom = Math.max(y + rowH, out.get(note)[1] + note.el.offsetHeight);
            }} else {{
                // su telefono prima i progetti, poi chi sono
                var y = y0;
                var cw = projects[0].el.offsetWidth;
                var cols = W >= 560 ? 2 : 1, rowH = 0;
                projects.forEach(function (it, i) {{
                    var c = i % cols;
                    if (c === 0 && i) {{ y = snap(y + rowH + gap, e, g); rowH = 0; }}
                    out.set(it, [x0 + c * (cw + gap), y]);
                    rowH = Math.max(rowH, it.el.offsetHeight);
                }});
                y = snap(y + rowH + gap * 2, e, g);
                out.set(photo, [x0, y]); y = snap(y + photo.el.offsetHeight + gap, e, g);
                out.set(note, [x0, y]);
                bottom = y + note.el.offsetHeight;
            }}
            return {{ map: out, height: bottom + (mobile() ? 170 : 110) }};
        }}

        function fitHeight(h) {{
            var scroll = h > window.innerHeight;
            body.classList.toggle('is-scroll', scroll);
            mat.style.setProperty('--table-h', Math.max(h, window.innerHeight) + 'px');
        }}

        var board = new Tavolo.Board(mat, {{
            key: 'home',
            tidy: function (b, sizeOnly) {{
                var s = slots(b);
                fitHeight(s.height);
                if (sizeOnly) return;
                b.items.forEach(function (it) {{ var p = s.map.get(it); it.x = p[0]; it.y = p[1]; it.r = 0; }});
            }},
            beforeMessy: function (b) {{ fitHeight(mobile() ? slots(b).height : 0); }},
            onMode: function (mode) {{
                body.classList.toggle('is-tidy', mode === 'tidy');
                btn.setAttribute('aria-pressed', mode === 'tidy' ? 'true' : 'false');
                btn.querySelector('.when-messy').hidden = mode === 'tidy';
                btn.querySelector('.when-tidy').hidden = mode !== 'tidy';
            }}
        }});

        btn.addEventListener('click', function () {{
            var next = board.mode === 'tidy' ? 'messy' : 'tidy';
            body.classList.toggle('is-tidy', next === 'tidy');
            board.setMode(next, true);
            Tavolo.drawRulers(mat);
        }});

        try {{ var saved = JSON.parse(sessionStorage.getItem('tavolo:home') || 'null'); }} catch (err) {{ var saved = null; }}
        body.classList.toggle('is-tidy', saved ? saved.mode === 'tidy' : mobile());
        var restored = board.restore();
        if (restored !== true) {{
            board.setMode(typeof restored === 'string' ? restored : (mobile() ? 'tidy' : 'messy'), false);
            if (!restored) board.drop();
        }}
        Tavolo.drawRulers(mat);

        var t;
        window.addEventListener('resize', function () {{
            clearTimeout(t);
            t = setTimeout(function () {{ board.refit(); Tavolo.drawRulers(mat); }}, 150);
        }});
        document.fonts && document.fonts.ready.then(function () {{ board.refit(); Tavolo.drawRulers(mat); }});
    }});
    </script>
</body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html_out)


# ---------------------------------------------------------------- pagine progetto
def build_project(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    slug = p["slug"]
    t = TEXTS[slug]
    hero, hw, hh = web_image(p["card"], slug, max_w=1800, max_h=1800, suffix="-hero")
    n_src, n_w, n_h = card(nxt)

    # racconto: un titoletto per paragrafo
    story = []
    for k, (pit, pen) in enumerate(zip(t["it"], t["en"])):
        story.append(f"""            <section>
                <h2>{bi(p['headings'][0][k], p['headings'][1][k])}</h2>
                <p lang="it">{fix(pit)}</p>
                <p lang="en">{fix(pen)}</p>
            </section>""")

    # scheda
    rows = [
        (bi("Tipo", "Type"), bi(*p["type"])),
        (bi("Anno", "Year"), p["year"]),
        (bi("Contesto", "Context"), bi(*p["context"])),
    ]
    if p["team"]:
        rows.append(("Team", "<ul>" + "".join(f"<li>{E(n)}</li>" for n in p["team"]) + "</ul>"))
    rows.append((bi("Il mio ruolo", "My role"),
                 "<ul>" + "".join(f'<li class="me">{bi(a, b)}</li>' for a, b in zip(*p["role"])) + "</ul>"))
    if p["link"]:
        rows.append(("Link", f'<a href="{E(p["link"][0])}" target="_blank" rel="noopener">{E(p["link"][1])}</a>'))
    facts = "\n".join(f"                <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)

    # dietro le quinte
    process = ""
    if p["process"]:
        figs = "\n        ".join(figure(slug, s, a, b, f"{p['title']}, processo", max_w=1400) for s, a, b in p["process"])
        process = f"""
    <section class="chapter" aria-labelledby="h-process">
        <h2 id="h-process">{bi('Dietro le quinte', 'Behind the scenes')}</h2>
        <p class="lead">{bi('Ricerca, schizzi e prototipi: come ci siamo arrivati.', 'Research, sketches and prototypes: how we got there.') if p['team'] else bi('Ricerca, schizzi e prototipi: come ci sono arrivato.', 'Research, sketches and prototypes: how I got there.')}</p>
        <div class="process">
        {figs}
        </div>
    </section>"""

    # risultato
    blocks = []
    if p.get("video"):
        v, poster = web_video(p["video"], slug)
        blocks.append(f"""<figure>
            <video src="{E(v)}" poster="{E(poster)}" autoplay muted loop playsinline controls preload="metadata" aria-label="{E(p['title'])}, video"></video>
        </figure>""")
    for layout, imgs in p["result"]:
        if layout == "wide":
            s, a, b = imgs[0]
            blocks.append(figure(slug, s, a, b, p["title"]))
        elif layout == "pair":
            inner = "\n            ".join(figure(slug, s, a, b, p["title"], max_w=1300) for s, a, b in imgs)
            blocks.append(f'<div class="row-pair">\n            {inner}\n        </div>')
        elif layout == "phones":
            tags = []
            for k, (s, _, _) in enumerate(imgs):
                ip, iw, ih = web_image(s, slug, max_w=1100, max_h=1040)
                tags.append(img_tag(ip, iw, ih, f"{p['title']}, schermata {k + 1}"))
            blocks.append(f"""<div>
            <div class="phones" tabindex="0" aria-label="{E(p['title'])}: schermate del prototipo">
                {chr(10).join('                ' + x for x in tags).strip()}
            </div>
            <p class="phones-caption"><small>{bi('Il prototipo, schermata per schermata. Trascina o scorri di lato.', 'The prototype, screen by screen. Drag or scroll sideways.')}</small></p>
        </div>""")
    gallery = "\n        ".join(blocks)

    visit = ""
    if p["link"]:
        visit = f"""
    <div class="visit">
        <a href="{E(p['link'][0])}" target="_blank" rel="noopener">{bi('Visita il sito del progetto ↗', 'Visit the project website ↗')}</a>
        <span>{E(p['link'][1])}</span>
    </div>"""

    type_line = f'{bi(*p["type"])}, {p["year"]}'
    page = head(f"{p['title']}, Alessandro Bacci", p["pitch"][0]) + f"""
<body class="project">
    <a class="skip" href="#contenuto">{bi('Vai al contenuto', 'Skip to content')}</a>

    <header class="mat band" id="banco">
        <div class="topbar">
            <a href="index.html">{bi('← Torna al tavolo', '← Back to the table')}</a>
            <div class="right"><span class="nav-name">Alessandro Bacci</span>{LANG_SWITCH}</div>
        </div>
        <div class="print print--hero" data-drag data-mx="0.94" data-my="0.3" data-r="-2.5">
            {img_tag(hero, hw, hh, p['title'], lazy=False, extra=' style="view-transition-name: hero"')}
        </div>
        <div class="band-title">
            <h1>{E(p['title'])}</h1>
            <p>{type_line}</p>
        </div>
    </header>

    <main class="sheet" id="contenuto">
        <p class="pitch">{bi(E(p['pitch'][0]), E(p['pitch'][1]))}</p>

        <div class="brief">
            <dl class="facts">
{facts}
            </dl>
            <div class="story">
{chr(10).join(story)}
            </div>
        </div>
{process}
    <section class="chapter" aria-labelledby="h-result">
        <h2 id="h-result">{bi('Il risultato', 'The result')}</h2>
        <div class="gallery">
        {gallery}
        </div>
    </section>
{visit}
    </main>

    <a class="mat next" href="{nxt['slug']}.html">
        <span class="print" style="left: auto; right: max(28px, 10vw); top: 64px;">
            {img_tag(n_src, n_w, n_h, '')}
        </span>
        <span class="band-title">
            <p>{bi('Prossimo sul tavolo', 'Next on the table')}</p>
            <h2>{E(nxt['title'])}</h2>
        </span>
    </a>
    <footer class="footer-line">
        <span>Alessandro Bacci</span>
        <span><a href="mailto:alebacci2003@gmail.com">alebacci2003@gmail.com</a></span>
        <span><a href="https://instagram.com/burdeldesignstudio" target="_blank" rel="noopener">@burdeldesignstudio</a></span>
    </footer>

    <script>
    document.addEventListener('DOMContentLoaded', function () {{
        var band = document.getElementById('banco');
        var board = new Tavolo.Board(band, {{ key: '{slug}' }});
        if (board.restore() !== true) board.setMode('messy', false);
        [band, document.querySelector('.next')].forEach(Tavolo.drawRulers);
        var t;
        window.addEventListener('resize', function () {{
            clearTimeout(t);
            t = setTimeout(function () {{ board.refit(); [band, document.querySelector('.next')].forEach(Tavolo.drawRulers); }}, 150);
        }});
    }});
    </script>
</body>
</html>
"""
    open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    build_home()
    for i in range(len(PROJECTS)):
        build_project(i)
        print("ok", PROJECTS[i]["slug"])
