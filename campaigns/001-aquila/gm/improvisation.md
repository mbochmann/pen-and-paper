# Dynamische Welt, Druck und Improvisation – SPOILER

## Fortschrittsuhren

Die Uhren beginnen erst nach Figurenbestätigung. Ein angekündigter zeitintensiver Weg oder eine lange Untersuchung erhöht `game_time.phase` und, solange aktiv, `clock-shortage` um 1. Eine Handlung kostet standardmäßig höchstens eine Phase; Weg und Untersuchung nur getrennt berechnen, wenn beide Kosten vorab klar sind. Dialoge, Denkzeit, Würfelwartezeit, kurze Hilfe und reale Pausen kosten nichts.

| Uhr | Stufen | Auslöser | Konkrete Folge |
|---|---|---|---|
| `clock-shortage` – Druck auf Stadtversorgung | 0–6 | angekündigte Spielzeitphase, solange Wasser nicht voll wiederhergestellt | 2: Warteschlangen; 4: Badehausbetrieb ruht, Flavia organisiert Ausgabe; 6: Rat prüft vorläufigen Wasservertrag |
| `clock-coverup` – Marcellus sichert seine Darstellung | 0–4 | er erfährt nachweislich von konkreter Ermittlung oder offenem Vorwurf; höchstens 1 je Szene | 2: Publius soll nur beglaubigte Abschriften herausgeben; 4: Marcellus fordert eine öffentliche Anhörung, um Erzählung zu kontrollieren |

Keine Uhr läuft automatisch nach jeder Chatantwort. Bei Überschreiten mehrerer Schwellen nur die noch nicht ausgespielten plausiblen Folgen einführen und in `world_changes` notieren. Werte bleiben bei Maximum stehen. Kein Totalverlust durch volle Uhr: Vertrag ist vorläufig, Kopien/Zeugen bleiben, Reparatur bleibt möglich. Vollständig wiederhergestelltes Wasser deaktiviert Knappheitsuhr. Cassias offiziell eingeleitete Untersuchung oder gesicherte Einigung deaktiviert Vertuschungsuhr.

## Freie Entscheidungen ernst nehmen

- **Sofort zum Steinbruch:** Zugang erlauben, vorhandene Motive abkürzen. Neria und Wasserbefund machen die Lage verständlich.
- **Marcellus sofort beschuldigen:** Er bestreitet, Cassia fragt nach Beobachtung. Kein willkürlicher Arrest; öffentliches Auftreten kann die bekannte Reaktion des Verwalters auslösen.
- **Sextus gewinnen:** Arbeiter helfen mit Leiter und Wagen. Politische Herausforderung wird leichter, nicht durch einen Ersatzbösewicht neutralisiert.
- **Wasser selbst verteilen:** Provisorischen Nutzen speichern; sie können Flavia einbinden. Das ist ein valider Erfolg und kostet nicht endlos kleine Ressourcen.
- **Quelle sofort reparieren:** Technisches Ziel erreicht. Der Rest wird Aufklärung/Verhandlung, keine zweite erfundene Sabotage.
- **Auftrag ablehnen:** Fragen, was die Figuren stattdessen interessiert; vorhandene Welt dafür verwenden. Die Handlung darf eine andere Richtung nehmen. Vorbereitung bleibt Angebot.
- **Gruppe trennt sich:** maximal ein kurzer Handlungsblock je Spieler im Wechsel; Wissen getrennt behandeln, bis eine Weitergabe ausgespielt wurde. `known_clues[].known_by` enthält dann nur die jeweilige Figur.
- **Spieler erfinden Beziehungen:** Vor Bestätigung prüfen, ob sie feste Wahrheit verletzen. Neue Beziehungen als bestätigtes Ereignis in `world_changes`, nicht rückwirkend unsichtbar einbauen.

## Kleine Begegnungen auf Wunsch

1. Ein Maultier mit Lorbeerkranz sperrt eine schmale Gasse. Mit Futter, Geduld oder Umweg ohne Wurf lösbar. Bato bedankt sich, kein zentraler Hinweis als Belohnung nötig.
2. Zwei Handwerker streiten darüber, wessen Gefäß zuerst gefüllt wird. Spieler können Reihenfolge, gemeinsame Lieferung oder Flavias Ausgabeplan vorschlagen. Ziel ist Vermittlung, keine einzig richtige Moralantwort.
3. Ein Windspiel am Quellhaus klingt wie ein Wort. Untersuchung zeigt Luftzug und Bronzeröhren. Nur nach ausdrücklich gewählter echter Magie kann ein übernatürlicher Rest verbindlich werden.
4. Publius' Wachstafeln geraten durcheinander. Ordnen über Symbole statt Zahlenrätsel; er zeigt danach freiwillig die relevante Seite, die auch auf anderem Weg verfügbar bleibt.
5. Ein Wagenrad steckt in einer Rinne. Hebel, gemeinsames Schieben oder Umweg. Bei riskantem Kraftversuch Ziel 7, angekündigte Kosten 1 Mut; sicheres Werkzeug braucht keine Probe.

## Neue Inhalte stabil einbauen

Vor neuem NSC/Ort/Gegenstand prüfen: Gibt es bereits einen passenden? Wenn nicht, stabile ID in `canon.json` registrieren, `origin: improvised` und `introduced_by_event_id` setzen. Ausgangswissen und Motivation knapp notieren. Tatsächlich etablierte neue Wahrheiten als `world_changes` mit Event speichern. Ungewählte Anschlussideen nicht registrieren, als wären sie bereits geschehen.

Neue Szenen erhalten ID, Ort, Ziel, mindestens zwei mögliche Ansätze, klar begrenzte Kosten und einen Ausgang ohne Sackgasse. Umfang zunächst eine Szene; erst nach Spielerinteresse vertiefen. Figurenwünsche aufgreifen, nicht aus realen persönlichen Angaben ableiten.

## Würfelbetrieb

Bei `tool`-Modus vorab Probe festlegen; das eingerichtete Werkzeug `python3 tools/roll_dice.py --roll-id <eindeutige-id>` genau einmal aufrufen. Es nutzt Python `secrets.randbelow(6)+1` pro W6. Details in `tools/README.md` auf Repository-Ebene. Beide Rohwerte, Eigenschaft, Bonus, Ziel und Ergebnisklasse speichern. Beim Glückspunkt Originalwürfel, ersetzten Index und neuen W6 im selben Event halten. Keine Wiederholung bis zum erwünschten Ergebnis.

Bei `physical`-Modus feste Probe speichern und nach den **beiden einzelnen Würfeln** fragen. Erst nach Antwort auflösen. Bei einer Probe mit knapper Verfehlung die Wahl „Preis oder Verzicht“ als `pending_action` erhalten und vor neuer Handlung klären. Bei Glück-Neuwurf die bereits vorliegenden Würfel festhalten; die ursprüngliche Probe nicht erneut würfeln.

Bei `diceless` keine Würfelwerte erfinden. Gewählten Preis/Umweg als Entscheidung protokollieren. Würfelmodus nur nach Zustimmung ändern und speichern.
