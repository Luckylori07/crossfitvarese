# CrossFit Varese — Report di consegna (demo Tramontis)

Data analisi: 16/10/2026. Sito analizzato: https://www.crossfitvarese.com/ (richieste con User-Agent da browser, pausa di 1–1,5 s, una sola richiesta per pagina).

## 1. Pagine realizzate

| Pagina | File | Note |
|---|---|---|
| Home | `index.html` | hero, Cos'è il CrossFit, programmi, come iniziare, il box, coach e community, prenota, dove siamo |
| Il CrossFit | `crossfit.html` | educativa: cos'è, come si svolge una lezione, tecnica, cosa aspettarsi dalla prova, FAQ |
| Programmi | `programmi.html` | 6 programmi presenti sul sito ufficiale, ognuno con ancora |
| Orari | `orari.html` | tabella giorno × fascia, responsive (card per giorno su smartphone) |
| Abbonamenti | `abbonamenti.html` | 6 formule **senza prezzi** (vedi §5) |
| Il box | `box.html` | descrizione spazi, attrezzatura visibile in foto, galleria con lightbox |
| Contatti | `contatti.html` | telefono, WhatsApp, email, indirizzo, Maps, Instagram |
| Prova gratuita | `prova-gratuita.html` | pagina di conversione (WhatsApp/telefono/email) — aggiunta rispetto all'elenco |
| Privacy | `privacy.html` | **bozza** da completare |
| — | `sitemap.xml`, `robots.txt` | generati dal build |

**Non create (per scelta)**: `coach.html` (le fonti ufficiali non presentano coach: vedi §6), pagine dedicate per programma (nessuna informazione sufficiente oltre le descrizioni già in `programmi.html`), `kids.html`/Open Gym ecc. (non offerti dal box).

## 2. Funzionalità implementate

- Design: palette ricavata dal box (pavimento nero, pareti bianche, rosso del logo `#DA291C`), titoli Big Shoulders Display, testo Barlow (self-hosted, SIL OFL).
- Animazioni (CSS, IntersectionObserver, transform/opacity): intro «timer» 00:03→00:00 con logo (home, una volta per sessione), titoli con reveal per riga, card e foto con reveal progressivo, parallax leggero su hero e foto, zoom foto in hover, header che cambia stile allo scroll, menu mobile animato, pulsanti con micro-interazione, barra CTA fissa su mobile.
- Lightbox accessibile su `<dialog>` (tastiera, frecce, Esc, ritorno del focus).
- `prefers-reduced-motion`: niente intro, parallax, reveal né transizioni.
- Interruttore demo unico `data-demo` sul `<body>` + `data/sito.json` (vedi README): banner, filigrana «DEMO», `noindex`, prefisso `[DEMO]`, credito Tramontis nel footer, link Tramontis con `target="_blank" rel="noopener"` in banner e footer di tutte le pagine.
- SEO: title e meta description in italiano, Open Graph, favicon dal logo, sitemap, robots, JSON-LD `SportsActivityLocation` (solo dati verificati).
- Dataset JSON modificabili e generatore `tools/build.py` (solo libreria standard); HTML generati già inclusi.

## 3. Fonti utilizzate

- https://www.crossfitvarese.com/ — `index`, `prova-gratuita`, `programmi`, `tariffe-orari`, `promozioni`, `calendario`, `contatti`, `open-day` (evento del settembre 2022, non riportato perché scaduto), `sitemap.xml` (ultimo aggiornamento 15/06/2023).
- Immagine degli orari `images/schedule_230928.png` (orario settembre 2023, trascritto in `data/orari.json`).
- Scheda affiliato: https://www.crossfit.com/gym/5630/crossfit-varese e https://games.crossfit.com/affiliate/5630 — indirizzo, telefono, email, «dal 2013 primo box CrossFit della provincia di Varese», titolare Riccardo Baldo.
- Link Google Maps ufficiale del sito (coordinate 45.772227, 8.783085), link WhatsApp e profilo Instagram `thisis_crossfitvarese` dal footer/contatti del sito.
- Fotografie e logo scaricati dal sito ufficiale (5 foto + logo); il logo è stato ricostruito in alta qualità dall'immagine degli orari (l'originale è 130×80 px).

## 4. Dati aziendali: confronto con le fonti

| Dato | Valore usato | Verifica |
|---|---|---|
| Indirizzo | Via I Maggio 10/A, 21022 Azzate (VA) | ✔ sito + scheda CrossFit.com |
| Telefono | +39 320 4292731 | ✔ sito + scheda CrossFit.com |
| Email | staff@crossfitvarese.com | ✔ sito + scheda CrossFit.com |
| WhatsApp | wa.me/393204292731 | ✔ link del sito, risponde |
| Instagram | @thisis_crossfitvarese | ✔ link del sito (il profilo richiede login, non ispezionabile) |
| Dal 2013, primo box della provincia | ✔ solo scheda CrossFit.com (**non** presente nelle pagine del sito ufficiale) |
| P.IVA 03966340121 | ✔ footer del sito ufficiale |
| Parcheggio gratuito >50 auto, uscita Azzate-Buguggiate | ✔ pagina Contatti |
| Facebook | non trovato su fonti ufficiali → omesso |

## 5. Informazioni da confermare con il titolare

1. **Orari**: l'orario trascritto è «da Settembre 2023». Non verificabile come attuale; è mostrato con avviso «Da confermare».
2. **Tariffe e promozioni**: tutti i prezzi del sito ufficiale sono del 2023 (con prezzo di listino barrato e promo). Non sono pubblicati; le formule compaiono con «Chiedi la tariffa aggiornata». Durate degli abbonamenti (1/3 mesi, 1 anno) e condizioni di promozione da riconfermare.
3. **Sistema di prenotazione**: il calendario Fitogram del sito attuale non è raggiungibile (vedi §7). Serve sapere se il box usa ancora Fitogram o altro sistema, e come gestisce le cancellazioni (sul sito attuale: entro 1 ora dall'inizio).
4. **Staff/coach**: nomi, ruoli, foto e qualifiche dei coach. L'unica persona identificabile è il titolare Riccardo Baldo (scheda CrossFit.com): confermare nome/ruolo e il consenso a mostrarlo.
5. **Programma Specialty ed Ego**: giorni, orari e destinatari non sono pubblicati.
6. **Attività extra** (Clinic, Workshop, Bootcamp): calendario e frequenza; nell'orario 2023 compare una Clinic il sabato 15:30–17:30.
7. **Struttura della lezione** (riscaldamento, tecnica/forza, allenamento del giorno) in `crossfit.html`: è una descrizione generale del metodo, da validare con i coach.
8. **Descrizione degli spazi** e dell'attrezzatura in `box.html`: ricavata dalle foto (rig, anelli, corde, bilancieri, kettlebell, plyo box, vogatori). Nessun dato su spogliatoi, docce, accessibilità: non inseriti.
9. **Ragione sociale**, referente privacy, base giuridica e conservazione dati: da inserire in `privacy.html`.
10. **Diritti sulle fotografie**: i file riportano «(c)DOMGARGA». Confermare licenza e dicitura del credito.
11. **Marchio**: la nota «CrossFit® è un marchio registrato di CrossFit, LLC» e l'uso di nome/logo come affiliato vanno allineati alle regole di CrossFit, LLC.

## 6. Immagini mancanti

- Nessuna foto identificabile dei coach/staff.
- Foto ad alta risoluzione (le disponibili sono 1200×630: l'hero a tutto schermo su monitor grandi risulta meno nitido).
- Foto degli spogliatoi, dell'ingresso, dell'area riservata alle lezioni individuali e dell'area esterna dei Bootcamp.
- Il logo originale è solo raster 130×80: servirebbe il file vettoriale (SVG/AI) per favicon e stampa.
- La mappa (`contatti.jpg`) è un'immagine del sito originale, non utilizzata.

## 7. Integrazioni che richiedono accesso a sistemi esterni

- **Fitogram** (calendario/prenotazione online, tenant `crossfit-varese`): il 16/10/2026 `widget.fitogram.pro`, `share.fitogram.pro` e `www.fitogram.pro` rispondevano con la pagina «This domain is for sale». Potrebbe dipendere dalla rete di analisi, quindi **va ricontrollato dal titolare** (accesso al pannello del gestionale). Finché non è chiarito, la prenotazione passa da WhatsApp/telefono/email.
- Hosting/dominio: pubblicazione sul dominio del box e relativi DNS.
- Google Search Console / sitemap dopo il go-live.

## 8. Test effettivamente eseguiti

Eseguiti in locale (server `python3 -m http.server`, Chromium headless con Playwright):

- Screenshot e ispezione visiva di tutte le 9 pagine a **375 px** e **1280 px**; nessuno scroll orizzontale (`scrollWidth` = larghezza viewport) su nessuna pagina.
- `tools/check.py`: 9 pagine con un solo H1, title con `[DEMO]`, meta robots `noindex, nofollow`, description e Open Graph, `alt` e `width`/`height` su tutte le immagini, risorse locali esistenti, link interni e ancore validi, banner e credito Tramontis presenti, link Tramontis con `target="_blank" rel="noopener"` (≥2 per pagina), `noopener` su tutti i link esterni `_blank`.
- Link esterni (HTTP): Tramontis 200, WhatsApp 200 (tutti i messaggi precompilati), CrossFit.com e scheda affiliato 200, Google Maps 200. Instagram risponde 429 (rate limit) alla richiesta automatica: non verificato in questa sessione.
- Interazioni (script Playwright, 19 controlli superati): intro e timer, non ripetuta nella stessa sessione; header allo scroll; lightbox con tastiera, frecce, Esc e ritorno del focus; menu mobile (inert da chiuso, `aria-expanded`, focus nel menu, Esc); barra CTA mobile; primo Tab sul link «Vai al contenuto»; `prefers-reduced-motion` (nessuna intro, reveal immediati, titolo hero visibile).
- Modalità demo spenta: verificata sia con `demo:false` + build, sia con la sostituzione manuale di `data-demo` (banner, filigrana, credito e noindex assenti).
- Contrasto WCAG calcolato sulle coppie di colori usate: tutte ≥ 4,5:1 (minimo 4,87:1).
- Nessun errore JavaScript in console, nessuna risorsa 404 sulle pagine caricate.

**Non eseguiti / non possibili**

- Test su dispositivi e browser reali (Safari/iOS, Firefox); solo Chromium.
- Lighthouse / misure di performance reali, test con screen reader (NVDA/VoiceOver), validazione W3C.
- Verifica dei link Instagram (rate limit), della prenotazione Fitogram (irraggiungibile) e dell'apertura dell'app WhatsApp su smartphone.
- Il comportamento del parallax e dell'intro è stato verificato per funzionamento, non valutato a occhio in movimento.

## 9. Problemi residui

- Foto 1200×630: hero poco nitido su schermi molto grandi.
- La filigrana «DEMO» è fissa sulla viewport e leggermente visibile sopra il testo (volutamente discreta).
- Le anteprime social (`og:image`) e il canonical in demo sono omessi finché non si imposta `demo_url` in `data/sito.json`.
- Privacy: bozza, non una informativa legale.
- Il testo delle sezioni editoriali sta nello script `tools/build.py`, non in JSON.
