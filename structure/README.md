# Datenmodell für KI-geführte Kampagnen · Version 1

## Ziele

Eine andere KI soll eine unterbrochene Szene ohne früheren Chat übernehmen können. Sie muss unterscheiden können: **Was ist wahr? Was ist passiert? Was wissen die Figuren? Was wäre nur möglich?** Text bleibt lesbar; Zustand bleibt maschinenlesbar. Kein eigener Server und keine Vektordatenbank nötig.

## Ordnervertrag

| Pfad | Zweck | Verbindlichkeit |
|---|---|---|
| `AGENTS.md` | Repository-weite Spielleitungsanweisungen | Arbeitsanweisung |
| `campaigns/index.json` | Aktive Kampagne und Einstiegspfade | Einstieg |
| `structure/` | Format, Speicherablauf, JSON-Schemas | Datenvertrag |
| `campaigns/<id>/README.md` | Spoilerfreier Überblick | Orientierung |
| `players/` | Regeln, Rollen, bekannte Karte, Journal | Spieler dürfen alles hier lesen |
| `gm/START.md` | Kompakter Wiederaufnahme-Leitfaden | Leseplan |
| `gm/canon.json` | Feste Ausgangswahrheit, Entitäten, Hinweise | Vorbereiteter Kanon |
| `gm/*.md` | Schauplätze, Figuren, Szenen, Optionen | Bedingte Vorbereitung |
| `gm/handouts.md` | Noch nicht freigegebene Texte | Spoiler |
| `state/current.json` | Aktueller vollständiger Zustand | Verbindlicher Spielstand |
| `state/events.jsonl` | Chronologische Ereignisse, eine JSON-Zeile je Event | Revisionsspur |
| `state/resume.md` | Kompakte Übergabe mit offener Frage | Ableitung aus Zustand |
| `tools/validate_campaign.py` | Schema-, Referenz- und Konsistenzprüfung | Technische Prüfung |

## Identitäten und Datentypen

- UTF-8, Markdown und gültiges JSON ohne Kommentare; JSONL nur vollständige Zeilen.
- Englische, stabile Feldnamen; deutsche Inhalte. Pfade ASCII mit Bindestrichen. IDs bleiben trotz Umbenennung gleich.
- Präfixe: `pc-`, `npc-`, `loc-`, `scene-`, `clue-`, `item-`, `quest-`, `clock-`, `fact-`, `event-`. `player-1/2` sind neutrale Spielerplätze.
- `null` bedeutet unbekannt/nicht gewählt; leere Liste bedeutet derzeit keine Einträge. Unbekannt ist niemals automatisch falsch.
- Alle Zustandsänderungen erhöhen `revision` genau um eins und fügen genau ein Event hinzu; ein Event darf mehrere zusammengehörige Änderungen bündeln.
- Spielzeit (`game_time`) und reales Speicherdatum (`updated_at`, ISO 8601 mit Zeitzone) sind getrennt. Kein Zeitfortschritt durch Chatpausen.
- Jede neue improvisierte Entität vor Referenzierung in `gm/canon.json` registrieren; Ursprung und erstes Ereignis angeben. Vorbereitete Kanon-Einträge nicht heimlich umschreiben.

## Wahrheit und Wissen

`canon.facts` hält die Ausgangswahrheit. `current.world_changes` hält spätere, durch Ereignisse begründete Veränderungen; jede mit `source_event_id`. Beispiel: „Umleitung aktiv“ kann später behoben sein, die ursprüngliche Sabotage bleibt historisch wahr. `known_clues` enthält tatsächlich zugängliche Hinweise samt Entdeckungsereignis. Eine Schlussfolgerung erst bei ausreichender Bestätigung als `confirmed` speichern; ansonsten `hypothesis`. NSC wissen nur ihren ausdrücklich beschriebenen Teil der Wahrheit.

`party_hypotheses` speichert Vermutungen der Gruppe getrennt von Hinweisen. Offene Zukunft wird in `open_threads` verwaltet und niemals als bereits eingetreten protokolliert. Nicht gewählte Ideen bleiben Vorbereitung, keine Erinnerung.

## Felder des Spielstands

| Feld | Inhalt |
|---|---|
| `schema_version`, `campaign_id`, `revision`, `last_event_id` | Versions- und Konsistenzanker |
| `phase`, `session`, `game_time` | Figurenwahl, aktives Spiel, Pause oder abgeschlossen |
| `scene_id`, `location_id`, `present_npc_ids` | Exakte aktuelle Situation |
| `settings` | Würfelmodus und vereinbarter Fantasiegrad |
| `characters` | Zwei Spielerplätze, gewählte Rolle, Werte, Mut, Talentnutzung, Ausrüstung |
| `party` | Gemeinschaftsvorräte, Münzen, zugängliche Schlüsselgegenstände |
| `known_clues`, `party_hypotheses`, `npc_states`, `world_changes` | Wissen und veränderte Welt |
| `quests`, `clocks`, `open_threads` | Ziele, sichtbare Folgen, offene Fäden |
| `pending_action`, `pending_roll`, `pending_prompt`, `challenge` | Bereits erklärte Handlung, noch ausstehende Probe, nächste Frage und laufender Konflikt |
| `spotlight` | Letzte aktive Figur und nächste Einladung |
| `last_narration`, `last_resolution` | Letzte veröffentlichte Situation und Konsequenz |

`pending_roll` ist null oder enthält feste Probe-ID, handelnde Figur, Würfelzahl, Eigenschaft, Ziel, Bonus, Ansage der Folgen und noch fehlende Rohwürfel. Nach Wiederaufnahme niemals dieselbe bereits aufgelöste Probe erneut würfeln.

## Kontextbudget und Fortsetzung

Zuerst Index, Zustand, Übergabe, Regeln, Spielleiterstart und Kanon. Danach nur aktuelle Szene, beteiligte NSC und relevante Orte. Das vollständige Ereignisarchiv nur für Nachfragen, Konflikte oder Rekonstruktion laden. Lange Kampagnen können abgeschlossene Sitzungen in eindeutig im Index aufgeführte JSONL-Dateien aufteilen; nie still Ereignisse entfernen.

Git-Commits sind vollständige Snapshots. Das Eventlog ist **kein automatisch ausführbares Event-Sourcing-System**: Es dokumentiert semantische Änderungen, aber keine vollständigen JSON-Patches. Eine exakte Wiederherstellung erfolgt über den Git-Commit, nicht durch erfundene Wiedergabe des Logs. Jeder Commit enthält stets einen kompletten `current.json`.

Neue inkompatible Felder benötigen eine neue Schema-Version und eine dokumentierte Migration. Bis dahin Version 1 strikt einhalten.
