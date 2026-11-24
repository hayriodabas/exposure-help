#!/usr/bin/env python3
"""Builds Exposure's standalone 12-locale Help & Privacy static site (Selenium palette)."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://hayriodabas.github.io/exposure-help"
CONTACT_EMAIL = "hayriodabas@gmail.com"

CSS = """\
:root {
  color-scheme: light dark;
  --ground: #e8e6e1;
  --surface: #f2f1ed;
  --raised: #fbfaf7;
  --hairline: #c4bfb5;
  --ink: #171612;
  --ink2: #555048;
  --tick: #7a7469;
  --amber: #b56a00;
  --amber-text: #955600;
}
@media (prefers-color-scheme: dark) {
  :root {
    --ground: #121110;
    --surface: #1b1916;
    --raised: #24211d;
    --hairline: #3a3630;
    --ink: #ede6d8;
    --ink2: #a69e90;
    --tick: #7a7266;
    --amber: #f0a63a;
    --amber-text: #f0a63a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font: 16.5px/1.62 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
.scale-bar {
  position: relative;
  height: 28px;
  border-bottom: 1px solid var(--hairline);
  background:
    repeating-linear-gradient(
      90deg,
      transparent 0,
      transparent 23px,
      var(--tick) 23px,
      var(--tick) 24px
    );
  background-size: 100% 10px;
  background-repeat: no-repeat;
  background-position: top;
}
.scale-bar::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  width: 3px;
  height: 24px;
  transform: translateX(-50%);
  background: var(--amber);
}
main {
  max-width: 740px;
  margin: 0 auto;
  padding: 36px 20px 68px;
}
.kicker {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--amber-text);
}
h1 {
  font-size: 36px;
  line-height: 1.12;
  font-weight: 700;
  margin: 10px 0 6px;
  letter-spacing: -0.015em;
}
.lede {
  font-size: 18.5px;
  color: var(--ink2);
  margin: 0 0 22px;
}
nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  padding: 12px 0;
  border-top: 1px solid var(--hairline);
  border-bottom: 1px solid var(--hairline);
  margin-bottom: 28px;
  font-size: 14.5px;
  font-weight: 500;
}
a {
  color: var(--amber-text);
  text-decoration-thickness: 1.5px;
  text-underline-offset: 3px;
}
h2 {
  font-size: 21px;
  line-height: 1.25;
  margin: 32px 0 10px;
  font-weight: 650;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: 5px;
  padding: 16px 18px;
  margin: 12px 0;
}
.panel strong {
  display: block;
  margin-bottom: 4px;
}
ul, ol {
  padding-left: 20px;
}
li {
  margin: 7px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: 5px;
}
th, td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid var(--hairline);
  font-size: 15px;
}
th {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink2);
}
tr:last-child td { border-bottom: none; }
.langs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 10px;
  list-style: none;
  padding: 0;
}
.langs li {
  margin: 0;
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: 5px;
  padding: 11px 14px;
}
footer {
  margin-top: 44px;
  padding-top: 16px;
  border-top: 1px solid var(--hairline);
  color: var(--ink2);
  font-size: 14px;
}
@media (max-width: 560px) {
  h1 { font-size: 29px; }
  main { padding: 26px 16px 52px; }
}
"""

LOCALES = {
    "en-US": {
        "name": "English",
        "html_lang": "en",
        "app": "Exposure",
        "nav_help": "Help",
        "nav_privacy": "Privacy Policy",
        "nav_langs": "All languages",
        "contact_title": "Contact",
        "contact_body": f"Questions or bug reports about Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Effective November 24, 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Help & Guide",
            "lede": "Reflected-light film meter built around your own camera's shutter and aperture marks.",
            "steps_title": "Using Exposure",
            "steps": [
                ("Film and camera", "Tap the top bar to set box speed and exposed ISO (push/pull), then define your cameras: fastest and slowest shutter speeds (whole, half, third stops, or older 1/25–1/50–1/100 sequences), B mode, lens aperture clicks, or a fixed-aperture pinhole. Exposure answers only with settings that camera can actually set."),
                ("Spot and whole-frame metering", "Point your iPhone at the subject. Tap any point in the viewfinder to spot-meter it, or tap Spot to return to whole-frame averaging. Hold reading freezes the EV with its elapsed age while you adjust your camera."),
                ("Shadow, highlight & scene band", "In harsh contrast, tap the deepest shadow that must keep detail, wait briefly for auto-exposure to settle, and tap Shadow. Tap the brightest area and tap Highlight. The Scene band compares both against your film's detail window (default −2 to +2 EV, adjustable in Film and camera). Place shadow, middle, or highlight, or drag the ruler in thirds of a stop."),
                ("Out-of-range limits", "When the light exceeds your camera's fastest speed or smallest aperture, Exposure hatches unavailable marks and offers a one-tap fix such as stopping down, slowing the shutter, or adding an ND filter."),
                ("Exposure Pro (one-time purchase)", "Adds the Roll Log (load a roll, write frames in one tap with aperture, speed, EV, scene ends, notes, and text/CSV export) and Long Exposure tools (ND2 to 16-stop filters, HARMAN technology ILFORD/KENTMERE reciprocity Tc = Tm^p or custom exponent, and a B-shutter countdown timer)."),
            ],
            "faq_title": "Frequently asked questions",
            "faq": [
                ("How accurate is an iPhone as a light meter?", "An iPhone camera estimates reflected light from its auto-exposure system; it is not a lab-calibrated meter. Match it once to a trusted meter in Settings › Match my meter, or dial a −3 to +3 EV calibration offset stored locally on your device."),
                ("Does Exposure take or save photos?", "No. The camera stream is used solely to read auto-exposure parameters (aperture, exposure duration, ISO, target offset). No frame is captured, stored, or transmitted."),
                ("Can I use Exposure without camera access?", "Yes. Tap By hand in the finder to dial EV directly in thirds of a stop or select a row from the Kodak TRI-X F-4017 daylight exposure table."),
                ("I already bought Exposure Pro — how do I restore it?", "Open Settings (top right) and tap Restore purchase using the same Apple Account. Refunds are handled by Apple at reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Privacy Policy",
            "lede": "Exposure collects no personal data, requires no account, and keeps everything on your device.",
            "summary_title": "Data summary",
            "rows": [
                ("Camera", "Reads auto-exposure values on-device to compute EV. No photo or video is taken, saved, or sent."),
                ("Rolls, cameras & settings", "Saved locally inside the app's sandbox on your device (rolls.json and UserDefaults). No location is recorded."),
                ("Accounts, analytics & ads", "None. No third-party tracking, advertising, or analytics SDKs are included."),
                ("Network traffic", "StoreKit (Apple) only, when loading prices, purchasing, or restoring Exposure Pro."),
            ],
            "sections": [
                ("No data collection", "Exposure does not collect, transmit, sell, or share any personal information, usage telemetry, crash logs, or device identifiers. Everything you enter — film stocks, camera profiles, calibration offsets, and roll logs — stays exclusively on your iPhone or iPad."),
                ("Camera permission", "Camera access is requested only after you tap Start the meter. Exposure reads the camera hardware's exposure duration, lens aperture, ISO, and exposure target offset to calculate EV. Video frames are discarded immediately on arrival and are never saved to Photos or uploaded."),
                ("Deleting your data", "To erase all logged rolls and frames at once, open Settings › Delete all rolls. Deleting the app removes all remaining preferences and camera profiles from your device."),
                ("In-app purchase", "Exposure Pro is a single non-consumable purchase processed directly by Apple through StoreKit. We do not receive your payment details or Apple Account credentials."),
            ],
        },
    },
    "de-DE": {
        "name": "Deutsch",
        "html_lang": "de",
        "app": "Belichtungsmesser (Exposure)",
        "nav_help": "Hilfe",
        "nav_privacy": "Datenschutz",
        "nav_langs": "Alle Sprachen",
        "contact_title": "Kontakt",
        "contact_body": f"Fragen oder Hinweise zu Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Stand: 24. November 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Hilfe & Anleitung",
            "lede": "Objektmessung für analoge Kameras – abgestimmt auf die eigenen Blenden- und Zeitenrasten.",
            "steps_title": "So funktioniert Exposure",
            "steps": [
                ("Film und Kamera", "Oben Film, Nenn- und Belichtungsempfindlichkeit (Push/Pull) sowie die eigenen Kameras festlegen: kürzeste und längste Zeiten (ganze, halbe, Drittelstufen oder alte Reihe 1/25–1/50–1/100), B, Blendenbereich oder Lochkamera. Exposure nennt nur Werte, die diese Kamera einstellen kann."),
                ("Spot- und Gesamtmessung", "Auf das Motiv richten. Ein Tipp im Sucher misst gezielt als Spot; ein Tipp auf Spot kehrt zur Gesamtmessung zurück. Messwert halten friert den EV-Wert samt Alter ein."),
                ("Schatten, Lichter & Motivband", "Bei starkem Kontrast dunkelste Stelle mit Zeichnung antippen, kurz warten bis sich die Belichtung beruhigt, und Schatten setzen; danach Lichter setzen. Das Motivband zeigt den Kontrastumfang im Zeichnungsfenster des Films (Standard −2 bis +2 EV) und lässt sich in Drittelstufen schieben."),
                ("Kameragrenzen", "Reicht der Bereich deiner Kamera nicht aus, schraffiert Exposure unmögliche Werte und schlägt direkt Abblenden, längere Zeit oder ND-Filter vor."),
                ("Exposure Pro (Einmalkauf)", "Schaltet das Filmtagebuch (Kader mit einem Tipp speichern, Notizen, Text-/CSV-Export) und Langzeitbelichtung (ND2 bis 16 Blenden, HARMAN-Schwarzschildfaktoren Tc = Tm^p oder eigener Exponent, B-Countdown) frei."),
            ],
            "faq_title": "Häufige Fragen",
            "faq": [
                ("Wie genau misst ein iPhone?", "Die Kamera schätzt das Licht aus ihrer Belichtungsautomatik. Unter Einstellungen › Mein Messer abgleichen lässt sich der Wert einmalig an einen vertrauten Belichtungsmesser anpassen (−3 bis +3 EV)."),
                ("Werden Fotos aufgenommen oder gespeichert?", "Nein. Es werden nur Belichtungsparameter gelesen; weder Fotos noch Videos werden aufgenommen oder übertragen."),
                ("Funktioniert die App auch ohne Kamera?", "Ja. Über Von Hand im Sucher lässt sich der EV in Drittelstufen oder anhand der Kodak-TRI-X-Tageslichttabelle F-4017 wählen."),
                ("Kauf wiederherstellen", "Unter Einstellungen › Kauf wiederherstellen mit demselben Apple Account. Erstattungen laufen über reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Datenschutzerklärung",
            "lede": "Exposure erfasst keine personenbezogenen Daten, benötigt kein Konto und speichert alles lokal.",
            "summary_title": "Überblick",
            "rows": [
                ("Kamera", "Liest nur Belichtungsdaten zur EV-Berechnung. Keine Fotos oder Videos werden gespeichert oder gesendet."),
                ("Rollen, Kameras & Einstellungen", "Ausschließlich lokal auf deinem Gerät (rolls.json und UserDefaults). Kein Standort."),
                ("Konten, Analyse & Werbung", "Keine. Keine Tracking- oder Analyse-SDKs von Drittanbietern."),
                ("Netzwerk", "Nur StoreKit (Apple) für Preisabruf, Kauf oder Wiederherstellung von Exposure Pro."),
            ],
            "sections": [
                ("Keine Datenerfassung", "Exposure sammelt, überträgt oder teilt keinerlei personenbezogene Daten, Nutzungsstatistiken oder Gerätekennungen."),
                ("Kamerazugriff", "Der Zugriff wird erst nach Tipp auf Messung starten angefragt. Einzelbilder werden sofort verworfen und nie gesichert."),
                ("Daten löschen", "Unter Einstellungen › Alle Filme löschen entfernst du das Filmtagebuch vollständig; das Löschen der App entfernt alle übrigen Einstellungen."),
                ("In-App-Kauf", "Exposure Pro ist ein einmaliger Kauf über Apples StoreKit. Zahlungsdaten erhalten wir nicht."),
            ],
        },
    },
    "fr-FR": {
        "name": "Français",
        "html_lang": "fr",
        "app": "Posemètre (Exposure)",
        "nav_help": "Aide",
        "nav_privacy": "Confidentialité",
        "nav_langs": "Toutes les langues",
        "contact_title": "Contact",
        "contact_body": f"Questions ou retours sur Exposure : <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "En vigueur le 24 novembre 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Aide & Guide",
            "lede": "Posemètre en lumière réfléchie réglé sur les crans exacts de votre appareil argentique.",
            "steps_title": "Utiliser Exposure",
            "steps": [
                ("Pellicule et appareil", "Touchez la barre supérieure pour régler la sensibilité boîte/exposée (push/pull) et vos boîtiers : vitesses (entiers, demi, tiers ou ancienne suite 1/25–1/50–1/100), pose B, ouvertures ou sténopé."),
                ("Mesure spot et globale", "Pointez le sujet. Touchez un point du viseur pour une mesure spot, ou touchez Spot pour revenir à la mesure globale. Figer la mesure bloque l'EV avec son ancienneté."),
                ("Ombres, hautes lumières et scène", "En lumière dure, marquez l'ombre puis la haute lumière après stabilisation. La bande Scène compare l'écart à la fenêtre de détail de votre pellicule (−2 à +2 EV par défaut)."),
                ("Limites de l'appareil", "Hors plage, les crans inutilisables sont hachurés et une correction en un geste est proposée (fermer, ralentir ou filtre ND)."),
                ("Exposure Pro (achat unique)", "Ajoute le carnet de pellicule (vues enregistrées en un geste, notes, export texte/CSV) et les poses longues (filtres ND2 à 16 IL, réciprocité HARMAN ILFORD/KENTMERE Tc = Tm^p ou exposant libre, minuteur pose B)."),
            ],
            "faq_title": "Questions fréquentes",
            "faq": [
                ("Quelle est la précision d'un iPhone ?", "Le téléphone estime la lumière via son exposition automatique. Calibrez-le une fois dans Réglages › Accorder mon posemètre (−3 à +3 EV)."),
                ("L'app prend-elle des photos ?", "Non. Seuls les paramètres d'exposition sont lus ; aucune image n'est capturée, enregistrée ou envoyée."),
                ("Sans accès caméra ?", "Touchez À la main dans le viseur pour régler l'EV ou utiliser le tableau jour Kodak TRI-X F-4017."),
                ("Restaurer l'achat", "Ouvrez Réglages › Restaurer l'achat avec le même compte Apple. Remboursements via reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Politique de confidentialité",
            "lede": "Exposure ne collecte aucune donnée personnelle, ne demande aucun compte et garde tout sur l'appareil.",
            "summary_title": "Résumé",
            "rows": [
                ("Appareil photo", "Lit uniquement l'exposition automatique sur l'appareil. Aucune photo ni vidéo enregistrée ou envoyée."),
                ("Pellicules & réglages", "Stockés localement sur l'appareil (rolls.json et UserDefaults). Aucune géolocalisation."),
                ("Comptes, analyse & pub", "Aucun. Aucun SDK tiers de suivi ou de publicité."),
                ("Réseau", "Uniquement StoreKit (Apple) pour Exposure Pro."),
            ],
            "sections": [
                ("Aucune collecte", "Exposure ne collecte, ne transmet et ne partage aucune donnée personnelle ni télémétrie."),
                ("Accès caméra", "Demandé uniquement après votre action. Les images ne sont jamais conservées."),
                ("Suppression", "Réglages › Supprimer toutes les pellicules efface le journal ; désinstaller l'app supprime le reste."),
                ("Achat intégré", "Exposure Pro est un achat unique traité par Apple StoreKit."),
            ],
        },
    },
    "es-ES": {
        "name": "Español",
        "html_lang": "es",
        "app": "Fotómetro (Exposure)",
        "nav_help": "Ayuda",
        "nav_privacy": "Privacidad",
        "nav_langs": "Todos los idiomas",
        "contact_title": "Contacto",
        "contact_body": f"Consultas o avisos sobre Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Vigente desde el 24 de noviembre de 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Ayuda y guía",
            "lede": "Fotómetro de luz reflejada ajustado a las marcas exactas de tu cámara de película.",
            "steps_title": "Cómo usar Exposure",
            "steps": [
                ("Película y cámara", "Toca la barra superior para definir ISO nominal y forzado (push/pull) y añadir tus cámaras: velocidades (pasos enteros, medios, tercios o serie clásica 1/25–1/50–1/100), modo B, diafragmas o estenopeica."),
                ("Medición puntual y general", "Apunta al sujeto. Toca un punto en el visor para medir puntual o vuelve a medición general. Fijar lectura congela el EV mostrando su antigüedad."),
                ("Sombras, luces y banda Escena", "En luz dura fija la sombra y la luz más alta tras estabilizarse el EV. La banda Escena indica si caben en la ventana de detalle de tu película (−2 a +2 EV por defecto)."),
                ("Límites de la cámara", "Cuando la luz supera tu cámara, las marcas imposibles aparecen rayadas con una solución en un toque."),
                ("Exposure Pro (compra única)", "Añade el registro de carretes (anotar fotogramas, notas, exportar texto/CSV) y largas exposiciones (filtros ND2 a 16 pasos, reciprocidad HARMAN ILFORD/KENTMERE Tc = Tm^p y temporizador en B)."),
            ],
            "faq_title": "Preguntas frecuentes",
            "faq": [
                ("¿Qué precisión tiene el iPhone?", "Estima la luz desde su exposición automática. Calíbralo una vez en Ajustes › Igualar mi fotómetro (−3 a +3 EV)."),
                ("¿Guarda fotos o vídeos?", "No. Solo lee parámetros de exposición; nunca captura ni envía imágenes."),
                ("¿Sin cámara?", "Usa A mano en el visor para fijar el EV o elegir la tabla de luz diurna Kodak TRI-X F-4017."),
                ("Restaurar compra", "Ajustes › Restaurar compra con la misma cuenta de Apple. Reembolsos en reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Política de privacidad",
            "lede": "Exposure no recopila datos personales, no requiere cuenta y guarda todo en tu dispositivo.",
            "summary_title": "Resumen",
            "rows": [
                ("Cámara", "Lee solo datos de exposición automática en el dispositivo. No guarda ni envía fotos."),
                ("Carretes y ajustes", "Guardados localmente (rolls.json y UserDefaults). Sin ubicación."),
                ("Cuentas, analítica y anuncios", "Ninguno. Sin SDKs de terceros."),
                ("Red", "Solo StoreKit (Apple) para Exposure Pro."),
            ],
            "sections": [
                ("Sin recopilación de datos", "Exposure no recopila ni comparte información personal, ubicación ni telemetría."),
                ("Permiso de cámara", "Se solicita solo al iniciar el fotómetro; los fotogramas de vídeo se descartan al instante."),
                ("Eliminar datos", "En Ajustes › Eliminar todos los carretes borras el registro; desinstalar elimina todos los ajustes."),
                ("Compra integrada", "Exposure Pro es un pago único procesado por Apple StoreKit."),
            ],
        },
    },
    "it": {
        "name": "Italiano",
        "html_lang": "it",
        "app": "Esposimetro (Exposure)",
        "nav_help": "Aiuto",
        "nav_privacy": "Privacy",
        "nav_langs": "Tutte le lingue",
        "contact_title": "Contatti",
        "contact_body": f"Domande o segnalazioni su Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "In vigore dal 24 novembre 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Guida e aiuto",
            "lede": "Esposimetro a luce riflessa calibrato sulle tacche reali della tua fotocamera a pellicola.",
            "steps_title": "Come usare Exposure",
            "steps": [
                ("Pellicola e fotocamera", "Tocca in alto per impostare ISO nominale ed esposto (push/pull) e definire le tue fotocamere: tempi (stop interi, mezzi, terzi o serie classica 1/25–1/50–1/100), posa B, diaframmi o stenopeico."),
                ("Misura spot e globale", "Punta il soggetto, tocca un punto nel mirino per la misura spot e usa Blocca misura per congelare l'EV con il tempo trascorso."),
                ("Ombre, alte luci e banda Scena", "Con forte contrasto fissa ombra e alta luce dopo l'assestamento; la banda Scena mostra lo scarto rispetto alla finestra di dettaglio (−2 / +2 EV)."),
                ("Limiti della fotocamera", "Fuori gamma i valori impossibili sono tratteggiati con suggerimento rapido (chiudi diaframma, rallenta o filtro ND)."),
                ("Exposure Pro (acquisto unico)", "Aggiunge il registro rullini (esportazione testo/CSV) e gli strumenti per pose lunghe (ND2–16 stop, reciprocità HARMAN ILFORD/KENTMERE Tc = Tm^p e timer posa B)."),
            ],
            "faq_title": "Domande frequenti",
            "faq": [
                ("Quanto è preciso l'iPhone?", "Stima la luce dall'esposizione automatica. Abbinalo una volta al tuo esposimetro in Impostazioni › Allinea esposimetro."),
                ("Scatta o salva foto?", "No. Legge solo i parametri di esposizione senza salvare o inviare immagini."),
                ("Senza fotocamera?", "Tocca A mano nel mirino per impostare l'EV o usare la tabella diurna Kodak TRI-X F-4017."),
                ("Ripristino acquisto", "Impostazioni › Ripristina acquisto con lo stesso Apple Account. Rimborsi su reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Informativa sulla privacy",
            "lede": "Exposure non raccoglie dati personali, non usa account e conserva tutto solo sul dispositivo.",
            "summary_title": "Sintesi",
            "rows": [
                ("Fotocamera", "Legge solo i dati di esposizione automatica sul dispositivo; nessuna foto salvata o inviata."),
                ("Rullini e impostazioni", "Archiviati localmente (rolls.json e UserDefaults). Nessuna posizione GPS."),
                ("Account, analisi e pubblicità", "Nessuno. Zero SDK di tracciamento di terze parti."),
                ("Rete", "Solo Apple StoreKit per Exposure Pro."),
            ],
            "sections": [
                ("Nessuna raccolta dati", "Exposure non raccoglie, trasmette né condivide dati personali o statistiche."),
                ("Accesso fotocamera", "Usato solo per calcolare l'EV; i fotogrammi vengono scartati immediatamente."),
                ("Cancellazione", "Impostazioni › Elimina tutti i rullini cancella il registro; rimuovere l'app elimina ogni impostazione."),
                ("Acquisto in-app", "Exposure Pro è un acquisto singolo gestito da Apple StoreKit."),
            ],
        },
    },
    "pt-BR": {
        "name": "Português (Brasil)",
        "html_lang": "pt-BR",
        "app": "Fotômetro (Exposure)",
        "nav_help": "Ajuda",
        "nav_privacy": "Privacidade",
        "nav_langs": "Todos os idiomas",
        "contact_title": "Contato",
        "contact_body": f"Dúvidas ou feedback sobre o Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Em vigor em 24 de novembro de 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Ajuda e guia",
            "lede": "Fotômetro de luz refletida feito para as marcas reais da sua câmera analógica.",
            "steps_title": "Como usar o Exposure",
            "steps": [
                ("Filme e câmera", "Toque no topo para definir o ISO nominal e exposto (push/pull) e cadastrar suas câmeras: velocidades (pontos inteiros, meios, terços ou série antiga 1/25–1/50–1/100), modo B, aberturas ou pinhole."),
                ("Medição pontual e geral", "Aponte para o assunto, toque no visor para medição pontual e use Fixar leitura para travar o EV."),
                ("Sombra, alta luz e faixa Cena", "Em luz dura fixe sombra e alta luz após estabilizar; a faixa Cena mostra se ambos cabem na janela de detalhes do filme (−2 a +2 EV)."),
                ("Limites da câmera", "Quando a luz passa do limite da câmera, marcas indisponíveis ficam hachuradas com correção em um toque."),
                ("Exposure Pro (compra única)", "Libera o registro de filmes (anotar quadros, exportar texto/CSV) e longas exposições (ND2 a 16 pontos, reciprocidade HARMAN ILFORD/KENTMERE Tc = Tm^p e cronômetro B)."),
            ],
            "faq_title": "Perguntas frequentes",
            "faq": [
                ("Qual a precisão do iPhone?", "O celular estima a luz pela exposição automática. Calibre uma vez em Ajustes › Igualar ao meu fotômetro."),
                ("O app tira ou salva fotos?", "Não. Apenas lê dados de exposição; nenhuma foto ou vídeo é gravado ou enviado."),
                ("Sem câmera?", "Toque em Manual no visor para ajustar o EV ou usar a tabela de luz solar Kodak TRI-X F-4017."),
                ("Restaurar compra", "Ajustes › Restaurar compra com a mesma Conta Apple. Reembolsos em reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Política de privacidade",
            "lede": "O Exposure não coleta dados pessoais, não exige conta e mantém tudo somente no dispositivo.",
            "summary_title": "Resumo",
            "rows": [
                ("Câmera", "Lê apenas metadados de exposição automática no aparelho; nenhuma imagem é salva ou enviada."),
                ("Filmes e ajustes", "Armazenados localmente (rolls.json e UserDefaults). Sem localização."),
                ("Contas, análise e anúncios", "Nenhum. Zero SDKs de terceiros."),
                ("Rede", "Apenas Apple StoreKit para o Exposure Pro."),
            ],
            "sections": [
                ("Sem coleta de dados", "O Exposure não coleta, vende nem compartilha dados pessoais ou telemetria."),
                ("Permissão de câmera", "Usada somente para calcular o EV; quadros de vídeo são descartados imediatamente."),
                ("Exclusão", "Ajustes › Apagar todos os filmes remove os registros; remover o app apaga o restante."),
                ("Compra no app", "Exposure Pro é compra única processada pelo Apple StoreKit."),
            ],
        },
    },
    "nl-NL": {
        "name": "Nederlands",
        "html_lang": "nl",
        "app": "Belichtingsmeter (Exposure)",
        "nav_help": "Hulp",
        "nav_privacy": "Privacybeleid",
        "nav_langs": "Alle talen",
        "contact_title": "Contact",
        "contact_body": f"Vragen of meldingen over Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Ingangsdatum: 24 november 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Hulp & Handleiding",
            "lede": "Reflectielichtmeter afgestemd op de eigen sluitertijden en diafragma's van jouw analoge camera.",
            "steps_title": "Zo gebruik je Exposure",
            "steps": [
                ("Film en camera", "Tik bovenaan voor box-ISO en belichte ISO (push/pull) en leg je camera's vast: hele, halve, derde stops of klassieke reeks 1/25–1/50–1/100, B, diafragmabereik of pinhole."),
                ("Spot- en totaalmeting", "Richt op het onderwerp, tik in de zoeker voor spotmeting en zet de waarde vast met Meting vasthouden."),
                ("Schaduw, hooglicht en scèneband", "Zet bij hard licht schaduw en hooglicht vast zodra de waarde stilstaat; de scèneband toont of beide binnen het detailvenster (−2 tot +2 EV) passen."),
                ("Cameragrenzen", "Buiten bereik worden onbruikbare standen gearceerd met een directe tip (diafragmeren, langzamer of ND-filter)."),
                ("Exposure Pro (eenmalig)", "Voegt het fotorollogboek (tekst/CSV-export) en lange sluitertijden toe (ND2–16 stops, HARMAN ILFORD/KENTMERE-reciprociteit Tc = Tm^p en B-timer)."),
            ],
            "faq_title": "Veelgestelde vragen",
            "faq": [
                ("Hoe nauwkeurig is een iPhone?", "Een telefoon schat het licht via automatische belichting. Kalibreer eenmalig via Instellingen › Vergelijk met mijn meter."),
                ("Maakt de app foto's?", "Nee. Er worden uitsluitend belichtingswaarden gelezen; er wordt niets opgeslagen of verzonden."),
                ("Zonder camera?", "Tik op Handmatig in de zoeker voor directe EV-invoer of de Kodak TRI-X F-4017 daglichttabel."),
                ("Aankoop herstellen", "Instellingen › Aankoop herstellen met dezelfde Apple Account. Terugbetaling via reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Privacybeleid",
            "lede": "Exposure verzamelt geen persoonsgegevens, vraagt geen account en bewaart alles lokaal.",
            "summary_title": "Overzicht",
            "rows": [
                ("Camera", "Leest alleen belichtingswaarden op het apparaat; geen foto's of video's opgeslagen of verstuurd."),
                ("Rollen & instellingen", "Lokaal opgeslagen (rolls.json en UserDefaults). Geen locatiegegevens."),
                ("Accounts, analyse & advertenties", "Geen. Geen tracking-SDK's van derden."),
                ("Netwerk", "Uitsluitend Apple StoreKit voor Exposure Pro."),
            ],
            "sections": [
                ("Geen gegevensverzameling", "Exposure verzamelt, verzendt of deelt geen persoonsgegevens of gebruiksstatistieken."),
                ("Cameratoegang", "Alleen gebruikt voor lichtmeting; camerabeelden worden direct weggegooid."),
                ("Gegevens verwijderen", "Via Instellingen › Alle rollen verwijderen wis je het logboek; de app verwijderen wist alles."),
                ("In-app-aankoop", "Exposure Pro is een eenmalige aankoop via Apple StoreKit."),
            ],
        },
    },
    "ja": {
        "name": "日本語",
        "html_lang": "ja",
        "app": "露出計 (Exposure)",
        "nav_help": "ヘルプ",
        "nav_privacy": "プライバシーポリシー",
        "nav_langs": "言語一覧",
        "contact_title": "お問い合わせ",
        "contact_body": f"Exposure に関するご質問・不具合報告：<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>",
        "updated": "改定日：2026年11月24日 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "ヘルプ・使い方",
            "lede": "お使いのフィルムカメラの絞りとシャッター目盛りだけで答える反射光式露出計。",
            "steps_title": "基本的な使い方",
            "steps": [
                ("フィルムとカメラ", "上部バーからフィルムの箱感度と撮影感度（増感・減感）、カメラのシャッター速度（1段・1/2段・1/3段、旧系列 1/25・1/50・1/100）、B、絞り範囲、ピンホールを登録できます。"),
                ("スポット測光と全体測光", "ファインダー内をタップするとその位置をスポット測光し、測光値を固定で EV と経過時間を保持できます。"),
                ("シャドー・ハイライトとシーン帯", "明暗差が大きい場面では暗部をシャドー、明部をハイライトに設定すると、フィルムの許容範囲（初期値 −2〜+2 EV）に収まるかをシーン帯で確認し露出位置を調整できます。"),
                ("カメラ限界の案内", "カメラの限界を超える光では使えない目盛りに斜線が入り、絞り込みや ND フィルターをワンタップで提案します。"),
                ("Exposure Pro（買い切り）", "ロール記録（ワンタップ記録・メモ・テキスト/CSV書き出し）と長時間露光計算（ND2〜16段、HARMAN 社 ILFORD/KENTMERE 相反則不軌 Tc = Tm^p、B 門カウントダウン）を追加します。"),
            ],
            "faq_title": "よくある質問",
            "faq": [
                ("iPhone での測光精度は？", "カメラの自動露出から光を推定します。設定 › 露出計に合わせる で信頼できる露出計と一度補正値（−3〜+3 EV）を合わせられます。"),
                ("写真や動画は保存されますか？", "いいえ。露出パラメータのみを読み取り、画像の保存や送信は一切行いません。"),
                ("カメラなしで使えますか？", "ファインダーの手動から EV を直接入力するか、Kodak TRI-X F-4017 の日中露出表を選べます。"),
                ("購入を復元したい", "設定 › 購入を復元 から同じ Apple Account で復元できます。返金は reportaproblem.apple.com をご利用ください。"),
            ],
        },
        "privacy": {
            "title": "プライバシーポリシー",
            "lede": "Exposure は個人情報を一切収集せず、アカウント不要ですべて端末内のみで動作します。",
            "summary_title": "データの扱い",
            "rows": [
                ("カメラ", "EV 計算のため端末内で自動露出値のみを参照します。写真・動画の撮影、保存、送信は行いません。"),
                ("ロールと設定", "端末内のみに保存（rolls.json / UserDefaults）。位置情報は記録しません。"),
                ("アカウント・解析・広告", "なし。外部の解析・広告 SDK は一切組み込んでいません。"),
                ("通信", "Exposure Pro の価格取得・購入・復元のための Apple StoreKit 通信のみ。"),
            ],
            "sections": [
                ("情報収集なし", "Exposure は個人情報、位置情報、利用状況ログ、識別子を収集・送信・共有しません。"),
                ("カメラ権限", "測光開始時のみ求められ、映像フレームは即座に破棄されます。"),
                ("データ削除", "設定 › すべてのロールを削除 で記録を消去でき、アプリ削除で全設定が消去されます。"),
                ("App 内課金", "Exposure Pro は Apple StoreKit 経由の買い切り課金です。"),
            ],
        },
    },
    "ko": {
        "name": "한국어",
        "html_lang": "ko",
        "app": "노출계 (Exposure)",
        "nav_help": "도움말",
        "nav_privacy": "개인정보 처리방침",
        "nav_langs": "모든 언어",
        "contact_title": "문의",
        "contact_body": f"Exposure 문의 및 오류 제보: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>",
        "updated": "시행일: 2026년 11월 24일 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "도움말 및 안내",
            "lede": "내 필름 카메라의 조리개와 셔터 눈금에 맞춰 답하는 반사광 노출계입니다.",
            "steps_title": "사용 방법",
            "steps": [
                ("필름과 카메라", "상단 바에서 박스 감도와 촬영 감도(증감/감감)를 정하고 카메라의 셔터 속도(1/½/⅓스톱 또는 구형 1/25·1/50·1/100), B 셔터, 조리개 범위, 핀홀을 설정합니다."),
                ("스팟 및 전체 측광", "뷰파인더의 한 지점을 탭하면 스팟 측광을 수행하며, 측광값 고정으로 EV와 경과 시간을 유지합니다."),
                ("섀도·하이라이트 장면 밴드", "명암 차가 큰 장면에서 어두운 부분(섀도)과 밝은 부분(하이라이트)을 지정하면 필름 계조 창(기본 −2~+2 EV)에 맞는지 확인하고 ⅓스톱씩 노출을 조절할 수 있습니다."),
                ("카메라 한계 안내", "카메라 범위를 벗어난 눈금은 빗금으로 표시되며 조리개 조이기·ND 필터 등의 해법을 한 번에 제안합니다."),
                ("Exposure Pro (1회 구매)", "롤 기록(원탭 프레임 저장, 메모, 텍스트/CSV 내보내기)과 장노출 도구(ND2~16스톱, HARMAN ILFORD/KENTMERE 상반칙불궤 Tc = Tm^p, B 타이머)를 제공합니다."),
            ],
            "faq_title": "자주 묻는 질문",
            "faq": [
                ("아이폰 노출계의 정확도는?", "카메라 자동 노출에서 빛을 추정합니다. 설정 › 내 노출계와 맞추기에서 기존 노출계와 −3~+3 EV 보정값을 한 번 맞출 수 있습니다."),
                ("사진이나 영상을 저장하나요?", "아니요. 노출 수치만 읽으며 사진·영상을 촬영, 보관, 전송하지 않습니다."),
                ("카메라 권한 없이 쓸 수 있나요?", "뷰파인더의 수동 모드에서 EV를 직접 맞추거나 Kodak TRI-X F-4017 주광표를 선택할 수 있습니다."),
                ("구매 복원", "설정 › 구매 복원에서 같은 Apple 계정으로 복원할 수 있습니다. 환불은 reportaproblem.apple.com에서 진행됩니다."),
            ],
        },
        "privacy": {
            "title": "개인정보 처리방침",
            "lede": "Exposure는 개인정보를 수집하지 않으며 계정 없이 모든 데이터를 기기에만 보관합니다.",
            "summary_title": "데이터 요약",
            "rows": [
                ("카메라", "EV 계산을 위해 기기 내 자동 노출 값만 읽습니다. 사진·영상은 저장되거나 전송되지 않습니다."),
                ("롤 및 설정", "기기에만 저장(rolls.json 및 UserDefaults). 위치 정보는 기록하지 않습니다."),
                ("계정·분석·광고", "없음. 제3자 추적·광고 SDK를 포함하지 않습니다."),
                ("네트워크", "Exposure Pro 결제 및 복원을 위한 Apple StoreKit 통신만 사용합니다."),
            ],
            "sections": [
                ("개인정보 미수집", "Exposure는 어떠한 개인정보, 위치, 사용 로그도 수집·전송·공유하지 않습니다."),
                ("카메라 권한", "측광을 시작할 때만 요청하며 영상 프레임은 즉시 폐기됩니다."),
                ("데이터 삭제", "설정 › 모든 롤 삭제에서 기록을 지울 수 있으며 앱을 삭제하면 모든 설정이 제거됩니다."),
                ("앱 내 구입", "Exposure Pro는 Apple StoreKit으로 처리되는 1회성 구매입니다."),
            ],
        },
    },
    "zh-Hans": {
        "name": "简体中文",
        "html_lang": "zh-Hans",
        "app": "测光表 (Exposure)",
        "nav_help": "帮助",
        "nav_privacy": "隐私政策",
        "nav_langs": "所有语言",
        "contact_title": "联系方式",
        "contact_body": f"关于 Exposure 的问题或反馈：<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>",
        "updated": "生效日期：2026年11月24日 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "帮助与使用指南",
            "lede": "按你胶片相机的实际光圈与快门档位作答的反射式测光表。",
            "steps_title": "使用方法",
            "steps": [
                ("胶片与相机", "点击顶部栏设置胶片标称感光度与迫冲/减冲 EI，并添加你的相机：快门范围（整档、半档、1/3 档或旧式 1/25·1/50·1/100）、B 门、镜头光圈范围或针孔相机。"),
                ("点测光与全局测光", "对准被摄体，点击取景器任意位置即可点测光；点击“保持读数”可锁定当前 EV 及经过时间。"),
                ("暗部、高光与场景标尺", "大光比下先标记暗部再标记高光，场景标尺会显示反差是否落在胶片细节窗口内（默认 −2 至 +2 EV），并可按 1/3 档滑动调整曝光位置。"),
                ("超出相机范围提示", "超出相机极限的档位会以斜线标出，并提供一键缩光圈、降快门或加 ND 滤镜建议。"),
                ("Exposure Pro（一次性买断）", "解锁胶卷记录（一键记录每帧光圈、快门、EV、场景两端与备注，导出文本/CSV）和长曝光工具（ND2 至 16 档、HARMAN ILFORD/KENTMERE 倒易律 Tc = Tm^p 与 B 门倒计时）。"),
            ],
            "faq_title": "常见问题",
            "faq": [
                ("iPhone 测光有多准确？", "手机通过相机自动曝光估算亮度。可在 设置 › 校准测光表 中与你信赖的测光表对齐一次（−3 至 +3 EV）。"),
                ("会拍照或上传图像吗？", "不会。仅读取曝光参数，绝不拍摄、保存或上传任何照片或视频。"),
                ("没有相机权限也能用吗？", "可以。点击取景器中的“手动”即可按 1/3 档设置 EV 或选用 Kodak TRI-X F-4017 日光曝光表。"),
                ("如何恢复购买？", "打开 设置 › 恢复购买，使用同一 Apple 账户即可恢复。退款请访问 reportaproblem.apple.com。"),
            ],
        },
        "privacy": {
            "title": "隐私政策",
            "lede": "Exposure 不收集任何个人数据，无需登录账号，所有内容均仅保存在你的设备本地。",
            "summary_title": "数据概要",
            "rows": [
                ("相机", "仅在本地读取自动曝光数值以计算 EV，不拍摄、保存或上传任何照片或视频。"),
                ("胶卷与设置", "仅保存在本机沙盒中（rolls.json 与 UserDefaults），不记录位置信息。"),
                ("账号、分析与广告", "无。不含任何第三方跟踪、分析或广告 SDK。"),
                ("网络通信", "仅通过 Apple StoreKit 加载、购买或恢复 Exposure Pro。"),
            ],
            "sections": [
                ("零数据收集", "Exposure 不收集、传输、出售或共享任何个人信息、定位数据或使用遥测。"),
                ("相机权限", "仅在点击开始测光后请求，视频帧到达后立即丢弃，绝不写入相册。"),
                ("删除数据", "前往 设置 › 删除所有胶卷 可一键清空记录；卸载应用将删除其余本地设置。"),
                ("App 内购买项目", "Exposure Pro 为一次性买断，由 Apple StoreKit 直接处理。"),
            ],
        },
    },
    "ru": {
        "name": "Русский",
        "html_lang": "ru",
        "app": "Экспонометр (Exposure)",
        "nav_help": "Справка",
        "nav_privacy": "Конфиденциальность",
        "nav_langs": "Все языки",
        "contact_title": "Контакты",
        "contact_body": f"Вопросы и отзывы об Exposure: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Действует с 24 ноября 2026 г. · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Справка и руководство",
            "lede": "Экспонометр отражённого света, настроенный под реальные шкалы вашей плёночной камеры.",
            "steps_title": "Как пользоваться Exposure",
            "steps": [
                ("Плёнка и камера", "Нажмите верхнюю строку, чтобы задать ISO и пуш/пул, а также описать камеры: диапазон выдержек (целые, полступени, трети или старый ряд 1/25–1/50–1/100), B, диафрагмы или камеру-обскуру."),
                ("Точечный и общий замер", "Наведите на объект, коснитесь точки в видоискателе для точечного замера и используйте «Удержать замер» для фиксации EV."),
                ("Тени, света и шкала сцены", "В жёстком свете отметьте тень и свет после стабилизации замера — шкала «Сцена» покажет, помещается ли контраст в окно деталей плёнки (по умолчанию −2…+2 EV)."),
                ("Пределы камеры", "Недоступные значения заштрихованы, а при избытке или нехватке света предлагается решение в одно касание."),
                ("Exposure Pro (разовая покупка)", "Добавляет журнал плёнок (запись кадра в одно касание, заметки, экспорт в текст и CSV) и длинные выдержки (фильтры ND2–16 ступеней, взаимозаместимость HARMAN ILFORD/KENTMERE Tc = Tm^p и таймер B)."),
            ],
            "faq_title": "Частые вопросы",
            "faq": [
                ("Насколько точен iPhone?", "Телефон оценивает свет по автоэкспозиции камеры. Калибруйте его один раз в Настройки › Сверить с моим экспонометром (−3…+3 EV)."),
                ("Сохраняются ли фотографии?", "Нет. Читаются только параметры экспозиции; фото и видео не снимаются и не передаются."),
                ("Можно ли без камеры?", "Да — нажмите «Вручную» в видоискателе для ввода EV или выбора таблицы дневного света Kodak TRI-X F-4017."),
                ("Восстановить покупку", "Настройки › Восстановить покупку с тем же аккаунтом Apple. Возвраты оформляются на reportaproblem.apple.com."),
            ],
        },
        "privacy": {
            "title": "Политика конфиденциальности",
            "lede": "Exposure не собирает персональные данные, не требует аккаунта и хранит всё только на устройстве.",
            "summary_title": "Кратко о данных",
            "rows": [
                ("Камера", "Считывает только параметры автоэкспозиции на устройстве; фото и видео не сохраняются и не отправляются."),
                ("Плёнки и настройки", "Хранятся локально (rolls.json и UserDefaults). Геолокация не записывается."),
                ("Аккаунты, аналитика и реклама", "Отсутствуют. Нет сторонних SDK отслеживания."),
                ("Сеть", "Только Apple StoreKit для Exposure Pro."),
            ],
            "sections": [
                ("Никакого сбора данных", "Exposure не собирает, не передаёт и не делится персональной информацией или телеметрией."),
                ("Доступ к камере", "Используется исключительно для расчёта EV; видеокадры немедленно отбрасываются."),
                ("Удаление данных", "Настройки › Удалить все плёнки стирает журнал; удаление приложения очищает все настройки."),
                ("Встроенная покупка", "Exposure Pro — разовая покупка через Apple StoreKit."),
            ],
        },
    },
    "tr": {
        "name": "Türkçe",
        "html_lang": "tr",
        "app": "Pozometre (Exposure)",
        "nav_help": "Yardım",
        "nav_privacy": "Gizlilik Politikası",
        "nav_langs": "Tüm diller",
        "contact_title": "İletişim",
        "contact_body": f"Exposure hakkında soru ve geri bildirimler: <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>.",
        "updated": "Yürürlük tarihi: 24 Kasım 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş",
        "help": {
            "title": "Yardım ve Kılavuz",
            "lede": "Filmli makinenin gerçek diyafram ve örtücü işaretlerine göre yanıt veren yansıyan ışık ölçer.",
            "steps_title": "Exposure Nasıl Kullanılır?",
            "steps": [
                ("Film ve makine", "Üst çubuğa dokunarak kutu ISO'sunu ve pozlama hızını (push/pull) girin; makinelerinizi tanımlayın (tam, yarım, üçte bir durak ya da eski 1/25–1/50–1/100 dizilimi, B modu, objektif diyafram aralığı veya iğne deliği). Exposure yalnızca o makinenin ayarlayabildiği değerlerle yanıt verir."),
                ("Spot ve tüm kare ölçümü", "iPhone'u konuya doğrultun. Vizörde bir noktaya dokunarak spot ölçüm yapın; Ölçümü tut ile EV değerini yaşıyla birlikte dondurun."),
                ("Gölge, parlak alan ve Sahne bandı", "Sert ışıkta ayrıntı kalması gereken en koyu noktaya dokunup ölçüm oturunca Gölge, en parlak noktada Parlak olarak işaretleyin. Sahne bandı iki ucun filmin ayrıntı penceresine (varsayılan −2 / +2 EV) sığıp sığmadığını gösterir."),
                ("Makine sınırları", "Işık makinenin sınırlarını aştığında kullanılamayan işaretler taranır ve tek dokunuşla diyafram kısma, yavaşlatma veya ND filtre önerilir."),
                ("Exposure Pro (tek seferlik)", "Rulo günlüğünü (tek dokunuşla kare kaydı, notlar, metin/CSV dışa aktarma) ve uzun pozlama araçlarını (ND2–16 durak, HARMAN ILFORD/KENTMERE karşılıklılık Tc = Tm^p ve B geri sayımı) açar."),
            ],
            "faq_title": "Sık Sorulan Sorular",
            "faq": [
                ("iPhone pozometre olarak ne kadar hassastır?", "Telefon kamerası otomatik pozlamadan ışığı tahmin eder. Ayarlar › Ölçerimle eşle ekranından güvendiğiniz bir pozometreyle bir kez kalibre edebilirsiniz (−3 ile +3 EV)."),
                ("Fotoğraf veya video kaydediliyor mu?", "Hayır. Yalnızca otomatik pozlama parametreleri okunur; hiçbir görüntü çekilmez, kaydedilmez veya gönderilmez."),
                ("Kamera izni olmadan kullanabilir miyim?", "Evet. Vizördeki Elle düğmesiyle EV'yi üçte bir duraklarla girebilir veya Kodak TRI-X F-4017 gün ışığı tablosundan seçebilirsiniz."),
                ("Satın almayı geri yükleme", "Ayarlar › Satın almayı geri yükle ile aynı Apple Hesabınız üzerinden geri yükleyebilirsiniz. İadeler reportaproblem.apple.com üzerinden Apple tarafından yapılır."),
            ],
        },
        "privacy": {
            "title": "Gizlilik Politikası",
            "lede": "Exposure kişisel veri toplamaz, hesap istemez ve tüm verilerinizi yalnızca cihazınızda saklar.",
            "summary_title": "Veri özeti",
            "rows": [
                ("Kamera", "EV hesaplamak için yalnızca cihaz içi otomatik pozlama değerlerini okur. Fotoğraf veya video çekilmez, saklanmaz, gönderilmez."),
                ("Rulolar ve ayarlar", "Yalnızca cihazınızda uygulama alanında saklanır (rolls.json ve UserDefaults). Konum bilgisi tutulmaz."),
                ("Hesap, analitik ve reklam", "Yok. Üçüncü taraf izleme, analiz veya reklam SDK'sı bulunmaz."),
                ("Ağ trafiği", "Yalnızca Exposure Pro fiyat yükleme, satın alma ve geri yükleme için Apple StoreKit."),
            ],
            "sections": [
                ("Veri toplanmaz", "Exposure hiçbir kişisel bilgiyi, kullanım istatistiğini, konum verisini veya cihaz kimliğini toplamaz, aktarmaz veya paylaşmaz."),
                ("Kamera izni", "Kamera izni yalnızca Ölçeri başlat düğmesine dokunduğunuzda istenir. Video kareleri anında atılır ve asla kaydedilmez."),
                ("Verilerin silinmesi", "Ayarlar › Tüm ruloları sil ile rulo günlüğünü tek seferde silebilir, uygulamayı kaldırarak tüm kalan ayarları temizleyebilirsiniz."),
                ("Uygulama içi satın alma", "Exposure Pro, Apple StoreKit üzerinden işlenen tek seferlik bir satın almadır; ödeme bilgilerinize erişmeyiz."),
            ],
        },
    },
}


def render_help(locale: str, data: dict) -> str:
    h = data["help"]
    steps_html = "".join(
        f"<li><strong>{html.escape(title)}.</strong> {html.escape(body)}</li>"
        for title, body in h["steps"]
    )
    faq_html = "".join(
        f'<div class="panel"><strong>{html.escape(q)}</strong>{html.escape(a)}</div>'
        for q, a in h["faq"]
    )
    return f"""<!doctype html>
<html lang="{data['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(data['app'])} — {html.escape(h['title'])}</title>
<link rel="canonical" href="{BASE_URL}/{locale}/help.html">
<style>{CSS}</style>
</head>
<body>
<div class="scale-bar" aria-hidden="true"></div>
<main>
  <div class="kicker">{html.escape(data['app'])}</div>
  <h1>{html.escape(h['title'])}</h1>
  <p class="lede">{html.escape(h['lede'])}</p>
  <nav>
    <a href="help.html">{html.escape(data['nav_help'])}</a>
    <a href="privacy.html">{html.escape(data['nav_privacy'])}</a>
    <a href="../index.html">{html.escape(data['nav_langs'])}</a>
  </nav>
  <h2>{html.escape(h['steps_title'])}</h2>
  <ol>{steps_html}</ol>
  <h2>{html.escape(h['faq_title'])}</h2>
  {faq_html}
  <h2>{html.escape(data['contact_title'])}</h2>
  <p>{data['contact_body']}</p>
  <footer>{html.escape(data['updated'])}</footer>
</main>
</body>
</html>
"""


def render_privacy(locale: str, data: dict) -> str:
    p = data["privacy"]
    rows_html = "".join(
        f"<tr><td><strong>{html.escape(k)}</strong></td><td>{html.escape(v)}</td></tr>"
        for k, v in p["rows"]
    )
    sec_html = "".join(
        f"<h2>{html.escape(title)}</h2><p>{html.escape(body)}</p>"
        for title, body in p["sections"]
    )
    return f"""<!doctype html>
<html lang="{data['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(data['app'])} — {html.escape(p['title'])}</title>
<link rel="canonical" href="{BASE_URL}/{locale}/privacy.html">
<style>{CSS}</style>
</head>
<body>
<div class="scale-bar" aria-hidden="true"></div>
<main>
  <div class="kicker">{html.escape(data['app'])}</div>
  <h1>{html.escape(p['title'])}</h1>
  <p class="lede">{html.escape(p['lede'])}</p>
  <nav>
    <a href="help.html">{html.escape(data['nav_help'])}</a>
    <a href="privacy.html">{html.escape(data['nav_privacy'])}</a>
    <a href="../index.html">{html.escape(data['nav_langs'])}</a>
  </nav>
  <h2>{html.escape(p['summary_title'])}</h2>
  <table><tbody>{rows_html}</tbody></table>
  {sec_html}
  <h2>{html.escape(data['contact_title'])}</h2>
  <p>{data['contact_body']}</p>
  <footer>{html.escape(data['updated'])}</footer>
</main>
</body>
</html>
"""


def render_index() -> str:
    items = "".join(
        f'<li><strong>{html.escape(d["name"])}</strong><br>'
        f'<a href="{loc}/help.html">{html.escape(d["nav_help"])}</a> · '
        f'<a href="{loc}/privacy.html">{html.escape(d["nav_privacy"])}</a></li>'
        for loc, d in LOCALES.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Exposure — Help &amp; Privacy</title>
<link rel="canonical" href="{BASE_URL}/">
<style>{CSS}</style>
</head>
<body>
<div class="scale-bar" aria-hidden="true"></div>
<main>
  <div class="kicker">Exposure · Film Light Meter</div>
  <h1>Help &amp; Privacy</h1>
  <p class="lede">Reflected-light film meter built around your own camera's aperture and shutter marks. Select your language below.</p>
  <ul class="langs">{items}</ul>
  <footer>Effective November 24, 2026 · Exposure (app.klarwerk.exposure) · Hayri Odabaş · <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></footer>
</main>
</body>
</html>
"""


def main() -> None:
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    for locale, data in LOCALES.items():
        loc_dir = ROOT / locale
        loc_dir.mkdir(parents=True, exist_ok=True)
        (loc_dir / "help.html").write_text(render_help(locale, data), encoding="utf-8")
        (loc_dir / "privacy.html").write_text(render_privacy(locale, data), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    # Root fallbacks matching en-US so direct /privacy.html or /help.html links also resolve 200.
    (ROOT / "help.html").write_text(render_help("en-US", LOCALES["en-US"]), encoding="utf-8")
    (ROOT / "privacy.html").write_text(render_privacy("en-US", LOCALES["en-US"]), encoding="utf-8")
    print(f"Generated {len(LOCALES) * 2 + 3} HTML pages in {ROOT}")


if __name__ == "__main__":
    main()
