# Entwicklungsregeln für Luck Meter

- Code modular halten.
- Kleine, klar getrennte Funktionen schreiben.
- Keine riesigen Dateien entstehen lassen.
- UI und Spiellogik strikt trennen.
- Kommentare nur verwenden, wenn sie echten Mehrwert liefern.
- Modernes, minimalistisches UI beibehalten.
- Keine externen Dependencies außer CustomTkinter verwenden.
- Animationen performant halten.
- Konsistente Benennung verwenden.
- Keine Magic Numbers einführen.
- Globale Zustände vermeiden, wenn es sinnvoll möglich ist.
- Typing für neue Funktionen und Klassen verwenden.
- PEP8-konform arbeiten.
- Neue Mini-Spiele erst implementieren, wenn sie explizit beauftragt werden.
- Deutsche Texte mit Umlauten schreiben, also ü, ä und ö statt ue, ae und oe verwenden.

## Bestehende Architektur

- `main.py` bleibt der kleine Einstiegspunkt und soll keine Spiellogik enthalten.
- `ui.py` enthält CustomTkinter-Screens, Navigation und Animationen.
- `games.py` enthält Mini-Spiel-Logik, Ergebnis-Dataclasses und Zufallsziehungen.
- `scoring.py` enthält finale Score-Berechnung, Score-Farben und Auswertungstexte.
- Neue Ergebnisdaten bevorzugt als `@dataclass(frozen=True)` modellieren.
- Screens sollen Daten aus `games.py` nur anzeigen und Nutzeraktionen weiterreichen.
- Der Ergebnis-Screen darf Scores visualisieren, aber keine Spielregeln berechnen.
- Persistenz für spätere Score-Verläufe in ein eigenes Modul auslagern.
- Fenstergröße und zentrale UI-Texte/Konstanten in `ui.py` konsistent pflegen.
