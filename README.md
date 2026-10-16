# CrossFit Varese — proposta di sito (DEMO Tramontis)

Sito statico multipagina, senza framework e senza dipendenze a runtime. **È una demo**: non sostituisce ancora il sito ufficiale e non è indicizzabile finché la modalità demo è attiva.

## Contenuto del progetto

```
index.html, crossfit.html, programmi.html, orari.html, abbonamenti.html,
box.html, contatti.html, prova-gratuita.html, privacy.html   ← pagine generate (pubblicabili così come sono)
sitemap.xml, robots.txt                                       ← generati
assets/css/style.css   stile condiviso
assets/js/main.js      JavaScript condiviso (menu, animazioni, lightbox)
assets/fonts/          Big Shoulders Display + Barlow (licenza SIL OFL, self-hosted)
assets/img/            fotografie (WebP), logo, favicon
data/*.json            tutti i contenuti modificabili
tools/build.py         rigenera gli HTML dai JSON (solo Python 3, nessuna installazione)
tools/check.py         controlli automatici (link, H1, alt, requisiti demo)
docs/REPORT.md         report finale di analisi e consegna
```

## Vedere il sito in locale

```bash
python3 -m http.server 8000      # dalla cartella del progetto
# apri http://localhost:8000
```

Gli HTML sono già pronti: il sito si pubblica senza build. Il build serve solo quando si modificano i dati.

## Modificare i contenuti

I testi dinamici stanno in `data/`. Dopo ogni modifica:

```bash
python3 tools/build.py     # rigenera le pagine
python3 tools/check.py     # (facoltativo) verifica link e requisiti
```

| File | Cosa contiene |
|---|---|
| `data/azienda.json` | indirizzo, telefono, email, WhatsApp, Maps, social, P.IVA, titolare, accesso e parcheggio |
| `data/programmi.json` | programmi (nome, descrizione, obiettivo, destinatari, formato, orari). I campi `null` non vengono mostrati |
| `data/orari.json` | orario settimanale per giorno e fascia; `colonne` sono le fasce mostrate come colonne |
| `data/abbonamenti.json` | formule. `mostra_prezzi` è `false`: i prezzi non vengono mai stampati |
| `data/coach.json` | persone dello staff. `pagina_dedicata: false`: la pagina coach non esiste |
| `data/faq.json` | domande frequenti della pagina Il CrossFit |
| `data/sito.json` | modalità demo, dominio, agenzia |

I testi delle sezioni editoriali (home, Il CrossFit, Il box, privacy) si trovano in `tools/build.py`, nelle funzioni `page_*`.

### Orari
Modifica `data/orari.json`: ogni giorno ha una lista di `fasce` (`inizio`, `fine`, `tipi`). I tipi ammessi sono `class`, `individual`, `onramp`, `clinic`. Quando gli orari sono stati confermati dal box, imposta `"verificato_oggi": true` e riscrivi `avviso` (o svuotalo).

### Programmi
Aggiungi un oggetto alla lista `programmi` con un `id` univoco (diventa l'ancora `programmi.html#id`). Per aggiungere una pagina dedicata a un programma serve una nuova funzione in `tools/build.py`: creala solo per programmi confermati.

### Prezzi
Le tariffe 2023 del sito originale **non sono pubblicate** perché non verificabili come attuali (restano solo come riferimento interno in `prezzi_non_verificati_2023`). Per mostrare i prezzi, aggiungi un campo `prezzo` alle formule, imposta `mostra_prezzi` a `true` e adatta `plan_block()` in `tools/build.py`.

### Fotografie
- Le immagini sono in `assets/img/` in due misure (`nome.webp` 1200 px e `nome-640.webp`).
- Per sostituire una foto: esporta in WebP (qualità ~80) con lo stesso nome, oppure aggiorna `PHOTOS` e `CAPTIONS` in `tools/build.py` (percorsi e testi alternativi).
- Le foto attuali sono 1200×630: per un hero a tutto schermo nitido servono gli originali ad alta risoluzione.
- Crediti: i file portano nei metadati il copyright «DOMGARGA». **Verificare la licenza d'uso con il fotografo/titolare prima della pubblicazione.**

## Prenotazione della prova

La prova si prenota tramite i canali ufficiali, nessun dato passa dal sito:

- **WhatsApp** con messaggio precompilato (`whatsapp.messaggio_prova` in `data/azienda.json`);
- **telefono** (`telefono_tel`);
- **email** (`email`).

Il sito originale usava un calendario Fitogram (`widget.fitogram.pro`, tenant `crossfit-varese`): il 16/10/2026 tutti i domini `fitogram.pro` risultavano parcheggiati («This domain is for sale»), quindi **non è stato integrato**. Se il box usa un sistema aggiornato (Fitogram o altro): inserire l'URL in `prenotazione.url_prenotazione_esterna` di `data/azienda.json` e collegare i pulsanti in `tools/build.py` (`WA_PROVA`, `cta_band()`, `page_prova()`). Non esiste alcun modulo che simuli invii o conferme.

## Modalità demo e pubblicazione

La demo è governata da **un unico interruttore**.

**Metodo consigliato**

1. In `data/sito.json` imposta `"demo": false`.
2. Verifica `"dominio"` (usato per sitemap, canonical e anteprime social).
3. `python3 tools/build.py`

Effetti: `data-demo="false"` sul `<body>`, banner e credito Tramontis non vengono più generati, la filigrana «DEMO» sparisce, il meta `noindex` e il prefisso `[DEMO]` dei titoli vengono rimossi, `robots.txt` consente l'indicizzazione e riporta la sitemap.

**Metodo manuale (senza Python)**: sostituisci `data-demo="true"` con `data-demo="false"` in tutti gli HTML. CSS nasconde banner, filigrana e credito, e `main.js` rimuove noindex e prefisso `[DEMO]` dal titolo; per un risultato pulito (noindex fuori dall'HTML, `robots.txt`) preferisci il metodo consigliato.

Prima di pubblicare, completare l'elenco in `docs/REPORT.md` («Da confermare con il titolare») e la pagina `privacy.html`.

**Hosting**: basta qualsiasi hosting statico (Netlify, Apache, ecc.): carica l'intera cartella. Se la demo è pubblicata su un URL proprio, impostalo in `data/sito.json` → `demo_url` per avere canonical e anteprime social corrette.

## Accessibilità e performance

HTML semantico, un solo H1 per pagina, link «Vai al contenuto», focus visibile, menu mobile con `aria-expanded`, `Esc` e gestione del focus, lightbox su `<dialog>`, contrasto AA, `prefers-reduced-motion` rispettato (nessuna intro, nessun parallax, nessun reveal). Immagini WebP con `width`/`height`, `srcset` e lazy loading; font self-hosted; nessun tracciamento.
