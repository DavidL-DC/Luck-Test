# Luck Meter

Luck Meter ist eine Desktop-App für einen späteren interaktiven Glückstest.
Mehrere Mini-Spiele sollen am Ende zu einem Glücks-Score von 0 bis 10 führen.

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
├── games.py      # Platzhalter für Mini-Spiel-Architektur
├── scoring.py    # Berechnung des finalen Glücks-Scores
├── README.md     # Projektdokumentation
├── AGENTS.md     # Entwicklungsregeln für Codex
└── .gitignore    # Ignorierte lokale Dateien
```

## Geplante Features

- Mehrere kurze Mini-Spiele
- Interaktive Auswertung pro Spiel
- Finaler Glücks-Score von 0 bis 10
- Minimalistische quadratische Desktop-UI
- Dezente, performante Animationen
- Saubere Trennung zwischen UI, Spiellogik und Scoring
