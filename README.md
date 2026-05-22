# Luck Meter

Luck Meter ist eine Desktop-App fuer einen spaeteren interaktiven Glueckstest.
Mehrere Mini-Spiele sollen am Ende zu einem Gluecks-Score von 0 bis 10 fuehren.

## Setup

Voraussetzung: Python 3.12

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
├── ui.py         # CustomTkinter UI und Screens
├── games.py      # Platzhalter fuer Mini-Spiel-Architektur
├── scoring.py    # Berechnung des finalen Gluecks-Scores
├── README.md     # Projektdokumentation
├── AGENTS.md     # Entwicklungsregeln fuer Codex
└── .gitignore    # Ignorierte lokale Dateien
```

## Geplante Features

- Mehrere kurze Mini-Spiele
- Interaktive Auswertung pro Spiel
- Finaler Gluecks-Score von 0 bis 10
- Minimalistische quadratische Desktop-UI
- Dezente, performante Animationen
- Saubere Trennung zwischen UI, Spiellogik und Scoring
