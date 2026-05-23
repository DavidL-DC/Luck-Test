# Luck Meter

Luck Meter ist eine Desktop-App für einen interaktiven Glückstest.
Die App startet mit einer Münzwurf-Serie, führt danach durch das
Glückszahl-Spiel und die Schatzkisten und zeigt am Ende einen Luck Score
von 0 bis 10.

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
├── games.py      # Spiellogik für Mini-Spiele
├── scoring.py    # Berechnung des finalen Glücks-Scores
├── README.md     # Projektdokumentation
├── AGENTS.md     # Entwicklungsregeln für Codex
└── .gitignore    # Ignorierte lokale Dateien
```

## Geplante Features

- Vollständiger Ablauf: Startscreen, Münzwurf-Serie, Glückszahl, Schatzkisten, Ergebnis-Screen
- Mehrere kurze Mini-Spiele
- Interaktive Auswertung pro Spiel
- Finaler Glücks-Score von 0 bis 10
- Minimalistische quadratische Desktop-UI
- Dezente, performante Animationen
- Saubere Trennung zwischen UI, Spiellogik und Scoring
