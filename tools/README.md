# Würfelwerkzeug

Python 3.10 oder neuer genügt. `secrets` gehört zur Standardbibliothek und ist in der Spielumgebung bereits installiert; keine zusätzliche Paketinstallation nötig.

Nach vorheriger Ansage der Probe genau einmal ausführen:

```sh
python3 tools/roll_dice.py --roll-id roll-000003-pc-1
```

Ausgabe: eindeutige Probe-ID, Zeit, Rohwürfel, Summe und Zufallsquelle. Eigenschaften und Boni erst danach entsprechend der angesagten Probe addieren. Rohwürfel unverändert im Ereignis speichern. Das Werkzeug schreibt selbst keinen Spielstand und verhindert keine doppelten Aufrufe: Vor Aufruf deshalb offene Probe und vorhandene Events prüfen, nach erfolgreicher Ausgabe nie erneut würfeln, um ein Ergebnis zu ersetzen. Bei Speicherfehler die bereits erhaltenen Werte nachtragen.

Für einen ausdrücklich gewählten Glückseinsatz nur einen Ersatzwürfel mit einer abgeleiteten ID erzeugen (`--count 1`); ursprüngliche Würfel und ersetzten Index im Spielereignis erhalten.

`secrets.randbelow(6) + 1` verwendet den kryptografischen Zufallsgenerator des Betriebssystems. Keine festen Seeds, keine vom Sprachmodell gewählten Würfelzahlen, kein einfacher Modulo-Operator auf Zufallsbytes. Das ist keine Behauptung eines direkt angeschlossenen physikalischen Hardware-Zufallsgenerators. Ein externes Zufallsangebot wird nicht benötigt.

Quelle, geprüft am 21. Oktober 2026: [Offizielle Python-Dokumentation zu secrets](https://docs.python.org/3/library/secrets.html).
