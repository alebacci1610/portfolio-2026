# Contenuti del portfolio.
# Per cambiare testi o immagini: modifica qui e lancia `python3 _build/build.py` dalla cartella del sito.
# (GitHub Pages ignora le cartelle che iniziano con "_", quindi questa non finisce online.)
#
# Le immagini vengono prese da "foto copia/" e salvate ottimizzate in "img/".
# Ogni immagine: (file sorgente, didascalia IT, didascalia EN) — didascalie vuote = nessuna didascalia.
# Layout del risultato: "wide" = a tutta larghezza, "pair" = due affiancate, "phones" = striscia di schermate da scorrere.

FC = "foto copia/"

PROJECTS = [
    {
        "slug": "fragma",
        "title": "Fragma",
        "type": ("Speculative design", "Speculative design"),
        "year": "2025/26",
        "context": ("Politecnico di Milano", "Politecnico di Milano"),
        "team": ["Allen Jonathan Marco", "Micucci Mattia", "Salvi Alessandro", "Schiavi Carlotta", "Villa Eleonora"],
        "role": (["Prototipazione", "Coding", "Interazione"], ["Prototyping", "Coding", "Interaction"]),
        "link": ("https://alebacci1610.github.io/FRAGMA/", "alebacci1610.github.io/FRAGMA"),
        "card": FC + "Fragma/fragma- foto ale salvi/b2.png",
        "pitch": (
            "Una macchina che riscrive le notizie mentre sposti le pedine: un’installazione sul potere delle parole.",
            "A machine that rewrites the news as you move the pieces: an installation about the power of words.",
        ),
        "headings": (
            ["Il tema", "Il concept", "L’installazione", "Perché conta"],
            ["The theme", "The concept", "The installation", "Why it matters"],
        ),
        "process": [
            (FC + "Fragma/WhatsApp Image 2026-01-31 at 15.25.51.jpeg", "Il primo prototipo della plancia, tra legno, cavi e sensori.", "The first prototype of the board: wood, wires and sensors."),
            (FC + "Fragma/#1-conflitto linguistico-1.png", "Ricerca: i livelli del conflitto cognitivo.", "Research: the levels of cognitive warfare."),
            (FC + "Fragma/#1-conflitto linguistico-4.png", "Lo schema del sistema AI che guida l’installazione.", "A breakdown of the AI system behind the installation."),
        ],
        "result": [
            ("wide", [(FC + "Fragma/fragma- foto ale salvi/b6.png", "", "")]),
            ("wide", [(FC + "Fragma/frg2.png", "Ogni pedina controlla un parametro linguistico.", "Each piece controls one linguistic parameter.")]),
            ("pair", [(FC + "Fragma/fragma- foto ale salvi/b5.png", "", ""), (FC + "Fragma/fragma- foto ale salvi/b3.png", "", "")]),
            ("wide", [(FC + "Fragma/macchina in studio.png", "", "")]),
            ("wide", [(FC + "Fragma/WhatsApp Image 2026-02-03 at 13.08.54.jpeg", "Syntax F-1 in uso.", "Syntax F-1 in use.")]),
            ("wide", [(FC + "Fragma/Poster 1.jpg", "", "")]),
        ],
        "video": FC + "Fragma/fragma.mp4",
    },
    {
        "slug": "sound-morphology",
        "title": "Sound Morphology",
        "type": ("Web design", "Web design"),
        "year": "2025",
        "context": ("Politecnico di Milano", "Politecnico di Milano"),
        "team": ["Allen Jonathan Marco", "De Sensi Aurora", "Micucci Mattia", "Salvi Alessandro", "Villa Eleonora"],
        "role": (["Coding", "User interface", "UX"], ["Coding", "User interface", "UX"]),
        "link": ("https://wddc-cintaincoccodrillo.webflow.io", "wddc-cintaincoccodrillo.webflow.io"),
        "card": FC + "Medusound/hor.png",
        "pitch": (
            "Un archivio web immersivo per il DJ GNMR, da esplorare dentro una medusa fatta di particelle.",
            "An immersive web archive for DJ GNMR, explored inside a jellyfish made of particles.",
        ),
        "headings": (
            ["La sfida", "Il contenuto", "Due modi di esplorare", "La medusa"],
            ["The challenge", "The content", "Two ways to explore", "The jellyfish"],
        ),
        "process": [
            (FC + "Medusound/Screenshot 2026-04-06 alle 21.21.53.png", "Sviluppo: il codice accanto all’anteprima del sito.", "Development: the code next to a live preview of the site."),
        ],
        "result": [
            ("wide", [(FC + "Medusound/medusahome.png", "La medusa è anche la mappa di navigazione.", "The jellyfish doubles as the navigation map.")]),
            ("wide", [(FC + "Medusound/cinema.png", "", "")]),
            ("pair", [(FC + "Medusound/eraserhead.png", "", ""), (FC + "Medusound/seoul.png", "", "")]),
            ("wide", [(FC + "Medusound/about.png", "", "")]),
            ("pair", [(FC + "Medusound/Screenshot 2026-04-08 alle 22.43.01.png", "", ""), (FC + "Medusound/Screenshot 2026-04-08 alle 22.43.24.png", "", "")]),
            ("wide", [(FC + "Medusound/hands_iphones_preview_1_e5c82f2363.jpg", "", "")]),
        ],
    },
    {
        "slug": "futbol",
        "title": "Futbol",
        "type": ("Web design", "Web design"),
        "year": "2026",
        "context": ("Progetto personale", "Personal project"),
        "team": [],
        "role": (["Coding", "User interface", "Fotoritocco"], ["Coding", "User interface", "Photo editing"]),
        "link": ("https://alebacci1610.github.io/futbol/", "alebacci1610.github.io/futbol"),
        "card": FC + "Futbol/Screenshot 2026-04-09 alle 12.12.39.png",
        "pitch": (
            "Un archivio delle maglie che hanno fatto la storia del calcio, con un quiz per scoprire la tua.",
            "An archive of the shirts that made football history, with a quiz to find yours.",
        ),
        "headings": (
            ["L’idea", "L’archivio", "La navigazione", "Il quiz"],
            ["The idea", "The archive", "Navigation", "The quiz"],
        ),
        "process": [],
        "result": [
            ("wide", [(FC + "Futbol/Screenshot 2026-04-09 alle 11.52.40.png", "La home: una griglia a scorrimento infinito.", "The homepage: an infinite-scroll grid.")]),
            ("wide", [(FC + "Futbol/Screenshot 2026-04-09 alle 11.53.19.png", "La scheda di ogni maglia.", "A detail page for each shirt.")]),
            ("pair", [(FC + "Futbol/Screenshot 2026-04-09 alle 11.53.25.png", "", ""), (FC + "Futbol/Screenshot 2026-04-09 alle 11.53.39.png", "", "")]),
            ("wide", [(FC + "Futbol/Screenshot 2026-04-09 alle 11.54.12.png", "Il risultato del quiz.", "The quiz result.")]),
            ("wide", [(FC + "Futbol/Screenshot 2026-04-09 alle 11.54.26.png", "", "")]),
        ],
    },
    {
        "slug": "space-debris",
        "title": "Space Debris",
        "type": ("Data visualization", "Data visualization"),
        "year": "2024",
        "context": ("Politecnico di Milano", "Politecnico di Milano"),
        "team": ["Frigeni Lara", "Leonardi Jacopo", "Raimondo Sofia", "Villa Eleonora", "Zanchetta Francesco"],
        "role": (["Costruzione del dataset", "User interface", "Coding"], ["Dataset building", "User interface", "Coding"]),
        "link": ("https://lcg-infodesign.github.io/lavoro-di-gruppo-gruppo-2/", "lcg-infodesign.github.io"),
        "card": FC + "Space Debrys/Screenshot 2026-04-07 alle 15.21.09.png",
        "pitch": (
            "Oltre 15.000 detriti in orbita, resi esplorabili per paese, dimensione e altitudine.",
            "More than 15,000 pieces of orbital debris, explorable by country, size and altitude.",
        ),
        "headings": (
            ["Il tema", "Il linguaggio visivo", "L’interazione"],
            ["The topic", "Visual language", "Interaction"],
        ),
        "process": [
            (FC + "Space Debrys/Screenshot 2026-04-07 alle 15.23.36.png", "Il dataset in lavorazione.", "Working on the dataset."),
        ],
        "result": [
            ("wide", [(FC + "Space Debrys/Screenshot 2026-04-07 alle 15.20.08.png", "La timeline mostra la crescita dei detriti anno dopo anno.", "The timeline shows the debris growing year after year.")]),
            ("wide", [(FC + "Space Debrys/Screenshot 2026-04-07 alle 15.21.51.png", "", "")]),
            ("pair", [(FC + "Space Debrys/Screenshot 2026-04-07 alle 15.21.27.png", "", ""), (FC + "Space Debrys/Screenshot 2026-04-07 alle 15.21.45.png", "", "")]),
            ("wide", [(FC + "Space Debrys/Screenshot 2026-04-08 alle 22.49.38.png", "", "")]),
        ],
    },
    {
        "slug": "esplorami",
        "title": "EsploraMi",
        "type": ("Service design", "Service design"),
        "year": "2025",
        "context": ("Politecnico di Milano", "Politecnico di Milano"),
        "team": ["Frigeni Lara", "Guerra Matteo", "Marrone Lorenzo", "Villa Eleonora"],
        "role": (["Coding", "User interface", "UX"], ["Coding", "User interface", "UX"]),
        "link": None,
        "card": FC + "EsploraMI/Tokyo Subway Poster Mockup.jpg",
        "pitch": (
            "Un servizio che ti porta nei posti giusti di Milano, all’ora giusta, lontano dalla folla.",
            "A service that takes you to the right places in Milan at the right time, away from the crowds.",
        ),
        "headings": (
            ["Il problema", "Come funziona", "Cosa c’è di nuovo"],
            ["The problem", "How it works", "What’s new"],
        ),
        "process": [
            (FC + "EsploraMI/Screenshot 2026-04-10 alle 13.35.55.png", "Schizzo del percorso dell’utente.", "A sketch of the user journey."),
            (FC + "EsploraMI/Screenshot 2026-04-10 alle 13.35.03.png", "Le mappe di ricerca e brainstorming.", "Research and brainstorming boards."),
        ],
        "result": [
            ("phones", [(FC + f"EsploraMI/Screenshot 2026-04-10 alle {t}.png", "", "") for t in [
                "13.42.20", "13.42.25", "13.42.28", "13.42.32", "13.42.34", "13.42.36", "13.42.43", "13.42.45",
                "13.42.49", "13.43.10", "13.43.16", "13.43.24", "13.43.43", "13.43.54", "13.43.57", "13.44.26", "13.50.31"]]),
            ("wide", [(FC + "EsploraMI/Screenshot 2026-05-12 alle 17.23.21.png", "Tutte le schermate del prototipo.", "Every screen of the prototype.")]),
            ("pair", [(FC + "EsploraMI/mockup instagram flyer.png", "", ""), (FC + "EsploraMI/Screenshot 2026-04-10 alle 13.29.55.png", "", "")]),
        ],
    },
    {
        "slug": "gestures",
        "title": "Gestures",
        "type": ("Web design", "Web design"),
        "year": "2025",
        "context": ("Progetto personale", "Personal project"),
        "team": [],
        "role": (["Coding", "User interface", "Fotoritocco"], ["Coding", "User interface", "Photo editing"]),
        "link": ("https://gestures.webflow.io", "gestures.webflow.io"),
        "card": FC + "Gestures/mockup iphone.jpg",
        "pitch": (
            "Un’indagine ironica sulle regole non scritte della vita sociale, tutta su una landing page.",
            "A tongue-in-cheek investigation into the unwritten rules of social life, on a single landing page.",
        ),
        "headings": (
            ["Il tema", "Il racconto", "La navigazione"],
            ["The topic", "The story", "Navigation"],
        ),
        "process": [
            (FC + "Gestures/Screenshot 2026-04-06 alle 21.08.27.png", "La costruzione in Webflow.", "Building it in Webflow."),
        ],
        "result": [
            ("wide", [(FC + "Gestures/home.jpg", "", "")]),
            ("wide", [(FC + "Gestures/Screenshot 2026-04-06 alle 21.05.03.png", "", "")]),
            ("pair", [(FC + "Gestures/Screenshot 2026-04-06 alle 21.05.30.png", "", ""), (FC + "Gestures/Screenshot 2026-04-06 alle 21.06.46.png", "", "")]),
        ],
    },
]

PHOTO = FC + "foto mia/IMG_2347.jpg"

BIO = (
    "Sono Alessandro, ho 22 anni, vengo da Riccione e studio Design della Comunicazione al Politecnico di Milano. "
    "Sono un designer guidato da una forte curiosità e dalla ricerca del perfetto equilibrio tra materia fisica ed ecosistemi digitali. "
    "Unisco creatività, pensiero critico e precisione per sviluppare concept solidi e trasversali. "
    "Il mio approccio è pragmatico: amo risolvere problemi complessi e trasformare un’idea in una soluzione d’impatto visivo e funzionale.",
    "I’m Alessandro, I’m 22, I come from Riccione and I study Communication Design at Politecnico di Milano. "
    "I’m a designer driven by strong curiosity and by the search for the right balance between physical matter and digital ecosystems. "
    "I combine creativity, critical thinking and precision to develop solid, cross-disciplinary concepts. "
    "My approach is pragmatic: I love solving complex problems and turning an idea into a solution with visual and functional impact.",
)
