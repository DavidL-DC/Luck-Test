# Luck Meter

Luck Meter ist eine minimalistische Desktop-App für einen interaktiven
Glückstest. Die App führt durch fünf kurze Mini-Spiele und berechnet daraus
einen finalen Luck Score von 0 bis 10.

Die App ist als lokales Python-Projekt mit CustomTkinter umgesetzt und bleibt
bewusst kompakt: keine Web-Komponenten, keine Datenbank, keine zusätzlichen
externen Dependencies.

## Funktionsumfang

- Startscreen mit Einstieg in den Glückstest
- Mini-Spiel 1: Münzwurf-Serie
- Mini-Spiel 2: Glückszahl
- Mini-Spiel 3: Schatzkisten
- Mini-Spiel 4: Risiko-Rad
- Mini-Spiel 5: Glückswürfel
- Ergebnis-Screen mit animiertem Score-Ring
- Farbliche Score-Auswertung von rot bis gold
- Datum, Uhrzeit, Auswertungstext und kompakte Einzel-Scores

## Spielablauf

```text
Startscreen
→ Münzwurf-Serie
→ Glückszahl
→ Schatzkisten
→ Risiko-Rad
→ Glückswürfel
→ Ergebnis-Screen
```

## Scoring

Jedes Mini-Spiel liefert einen Score von 0 bis 100 Punkten. Aus allen
Mini-Spiel-Scores wird der Durchschnitt gebildet. Dieser Durchschnitt wird auf
einen finalen Luck Score von 0 bis 10 skaliert.

Der Ergebnis-Screen zeigt zusätzlich einen kurzen dynamischen Text abhängig vom
finalen Luck Score.

## Setup

Voraussetzung: Python 3.12 oder neuer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install customtkinter
```

## Start

```powershell
python main.py
```

## Projektstruktur

```text
luck_test/
├── main.py       # Einstiegspunkt der App
├── ui.py         # CustomTkinter UI, Screens und Animationen
├── games.py      # Spiellogik und Ergebnisdaten der Mini-Spiele
├── scoring.py    # Score-Berechnung, Ergebnisfarben und Auswertungstexte
├── README.md     # Projektdokumentation
├── AGENTS.md     # Entwicklungsregeln für Codex
└── .gitignore    # Ignorierte lokale Dateien
```

## Architektur

- `main.py` startet nur die App und bleibt bewusst klein.
- `ui.py` enthält Screens, Navigation und UI-Animationen.
- `games.py` enthält die reine Spiellogik der Mini-Spiele.
- `scoring.py` enthält finale Auswertungslogik, Score-Farben und Ergebnistexte.

UI und Spiellogik sind getrennt, damit neue Spiele oder spätere Auswertungen
gezielt ergänzt werden können.

## Mögliche spätere Erweiterungen

- Verlauf vergangener Scores
- Übersicht oder Statistikseite
- Export oder lokale Speicherung von Ergebnissen
- Weitere Mini-Spiele
- Feineres UI-Polishing
