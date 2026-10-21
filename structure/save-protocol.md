# Savepoints und Wiederaufnahme

## Ein Speicherpunkt = ein Git-Commit

Auf `main` immer gemeinsam schreiben:

1. `state/current.json` – vollständiger neuer Zustand;
2. `state/events.jsonl` – altes Log unverändert plus neues Event;
3. `state/resume.md` – knappe Übergabe inklusive offener Frage;
4. `players/journal.md` – ausschließlich bereits bekanntes Wissen;
5. gegebenenfalls neue Kanon-Einträge, aktualisierte bekannte Karte oder freigegebene Handouts.

Commit-Namen: `save(aquila): r0001 Figuren gewählt` bzw. `save(aquila): r0007 Am Mühlentor pausiert`. Revision 0 ist die initiale Vorbereitung. Änderungen an Vorbereitung ohne Spielzustandsänderung erhalten `prep(aquila): …` und erzeugen kein fiktives Spielereignis.

## Ablauf während des Spiels

1. Remote-Head lesen und als erwarteten Eltern-Commit merken. Aktuellen Zustand laden; niemals blind einen alten lokalen Stand überschreiben.
2. Spielerabsicht und ggf. ausstehende Würfel prüfen. Nur tatsächlich entschiedene Vorgänge auflösen. Risiko vor dem Wurf ansagen.
3. Event-ID aus neuer Revision bilden (`event-000001` usw.). Event notiert Szene vor/nach, Entscheidung in neutraler Paraphrase, Veränderungen, tatsächliche Würfel, bekannt gewordene Hinweise und neue offene Frage. Keine Rohtranskripte speichern.
4. Zustand und Ableitungen aktualisieren. `last_narration` ist der spielbare Erzähltext inklusive neuer Situation; `pending_prompt` die genaue nächste Frage. Bei noch offener Probe ist diese nicht aufgelöst und keine Konsequenz vorweggenommen.
5. Validator ausführen. Bei einem Fehler nicht veröffentlichen.
6. Alle Dateien in einem Commit mit dem zuvor gelesenen Eltern-Commit speichern. Git-Push ohne Force oder Git-Tree/Commit plus Ref-Update mit `expected_sha`. Bei geändertem Remote-Head abbrechen, neu lesen und semantisch abgleichen; keine konkurrierenden Spielzüge automatisch zusammenmischen.
7. Remote-Head und `current.json` am neuen Commit lesen. Erst nach dieser Bestätigung „gespeichert“ melden. Im normalen Spiel genügt am Szenenende/Pause eine knappe Statuszeile; die technischen Details nicht jedes Mal erzählen.

Bei API-Zugriff ohne Checkout: Inhalte lokal validieren, einen Tree auf Basis des aktuellen Remote-Trees erstellen, einen Commit mit diesem Head als Parent erstellen, Ref mit erwartetem Head aktualisieren. Keine fünf unabhängigen Contents-API-Updates für einen Savepoint; das könnte halbe Zustände hinterlassen.

## Fehler und Sonderfälle

- **Kein Zugriff:** ausdrücklich „Der neue Spielzug ist noch nicht im Repository gespeichert.“ Keine weiteren folgenreichen Aktionen still vorziehen. Den ausstehenden Stand im aktuellen Chat sichern und später exakt diesen nachtragen. Die bestätigte Remote-Revision bleibt der letzte sichere Savepoint.
- **Abbruch nach Commit, vor Chatantwort:** `last_narration` und `pending_prompt` erneut zeigen, keine zweite Auflösung. So kann der Erzähltext nachgeliefert werden.
- **Doppelte Nutzernachricht:** Gegen offene Handlung/Probe und letzten Event prüfen, nicht zweimal Münzen oder Mut abziehen.
- **Widerspruch zwischen JSON und Markdown:** JSON gewinnt; abgeleitete Texte korrigieren. Bei Widerspruch zwischen aktuellem JSON und Log zuletzt konsistenten Commit suchen, nicht raten.
- **Spielkorrektur:** neues `correction`-Event mit Verweis auf das betroffene Ereignis und Begründung. Danach alle betroffenen Werte und Wissenseinträge korrigieren. Alte Events behalten.
- **Rollback auf alten Savepoint:** nach ausdrücklichem Spielerwunsch neuen Commit erstellen, der den damaligen Inhalt als neuen Zustand übernimmt, Revision weiterzählt und die überholten Ereignisse benennt. Nie Branch-Historie zurücksetzen.
- **Sitzungsende:** `phase: paused`, offene Frage festhalten. Bei Wiederaufnahme `phase: playing` erst wenn die Figurenwahl abgeschlossen ist; Figurenwahl kann auch in einer Pause offen sein.

## Was wird wann gespeichert?

| Auslöser | Verhalten |
|---|---|
| Figur/Regeloption gewählt | Teilwahl sofort speichern; anderen Platz offen lassen |
| Handlung mit Folge oder neuem Hinweis | Ein gemeinsamer Savepoint nach Auflösung |
| Physischer Würfelwurf angefordert | Offene Probe und Einsatz speichern, vor Ergebnis |
| Regelfrage ohne neue Entscheidung | Keine Revision und keine Spielzeit |
| Szene abgeschlossen, Pause oder Ende | Sicher speichern und knapp bestätigen |
| Stunden/Tage ohne Nachrichten | Keine Veränderung |

## Wiederaufnahme-Check

Revision und letztes Event stimmen überein; aktuelle Szene existiert; Orte, NSC und Hinweise sind registriert; Figurenwerte liegen im gültigen Bereich; kein Würfelwurf wird wiederholt; alle freigegebenen Informationen stehen im Journal; nächste Frage ist eindeutig. Ein neuer Chat mit Zugriff braucht keine bisherige Unterhaltung.
