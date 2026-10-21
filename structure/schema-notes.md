# Schemas und Erweiterungen

`state.schema.json` und `event.schema.json` sind JSON Schema 2020-12-Dokumente. Die lokale Prüfung implementiert ausschließlich die hier verwendete Teilmenge: `type`, `enum`, `anyOf`, `properties`, `required`, `additionalProperties`, `items`, `minItems`, `maxItems`, `uniqueItems`, `minimum`, `maximum`, `minLength`, `pattern`, `format: date-time`. Sie benötigt keine externen Pakete. Neue Schema-Schlüssel dürfen nicht still hinzukommen; Validator und Schema gemeinsam erweitern oder einen vollständigen JSON-Schema-Validator verwenden.

Querverweise und Regeln werden zusätzlich semantisch geprüft: Revisionen, eindeutige IDs, vorhandene Entitäten, Figurenwerte, Ausrüstungsplätze, Uhren, Würfelsummen und aktive Szenen. Das ersetzt kein redaktionelles Prüfen von Spoilern oder der Erzählung.

## Laufende Änderungen

`world_changes` ist eine chronologische Liste etablierter Veränderungen. Für denselben `key` gilt der zuletzt hinzugefügte Eintrag; ältere Einträge bleiben nachvollziehbar. Verwende beispielsweise `water-restored`, `water-partial`, `neria-rescued`, `livia-cleared`, `marcellus-investigated`. Die Schreibweisen `water_restored` usw. in Szenenprosa bezeichnen diese Schlüssel sinngemäß; gespeichert werden ausschließlich die Bindestrich-IDs.

`known_clues` enthält jede Hinweis-ID höchstens einmal. Bei späterer Weitergabe `known_by` ergänzen, beim erstmaligen Entdecken `discovered_event_id` beibehalten; das Weitergeben bekommt ein eigenes Event. `revealed_text` enthält nur den wirklich bekannten Teil. Bestätigung einer Deutung verändert nicht rückwirkend den beobachteten Inhalt.

`npc_states` enthält den aktuellen Ort jeder Figur. `present_npc_ids` ist die Teilmenge der gerade mit den Helden interagierenden NSC, nicht automatisch jeder Bewohner des Ortes. Bei Reiseänderungen beide Felder konsistent halten. Die Positionen der Spieler bei Trennung in `world_changes` mit `pc-1-location` und `pc-2-location` festhalten; `location_id` folgt dem aktuellen Spotlight. Beim Zusammenfinden die beiden Positionsschlüssel wieder gemeinsam aktualisieren.

`pending_action` hält eine noch nicht aufgelöste Absicht. `pending_roll` enthält nur die ausstehende Probe; sobald Rohwurf inklusive möglichem Glückseinsatz endgültig ist, Ergebnis in `events[].rolls` eintragen und `pending_roll` leeren. Bei knappem Ergebnis bleibt die Kostenwahl in `pending_action` offen, bis der Spieler entscheidet. Ressourcen erst bei getroffener Wahl abbuchen.

`challenge` speichert laufende Konflikte oder Verfolgungen. Fortschritt wird nicht zwischen zwei Nachrichten zurückgesetzt. Der Zielwert für das Ende der Herausforderung ist von den einzelnen Proben-Zielwerten getrennt.

Alltägliche Ausrüstung steht mit Name und Platzbedarf direkt an der Figur (`item_id: null`). Einzigartige Abenteuergegenstände erhalten eine registrierte `item-`-ID und genau einen Besitzer: Figur oder gemeinsame Gruppe. Hinweise sind Wissen, keine automatisch übertragenen physischen Gegenstände. Ein gesehenes Dokument gehört nicht ohne ausgespielten Erwerb zur Ausrüstung.

## Rollendaten

`gm/roles.json` ist die maschinenlesbare Entsprechung der sechs Rollen. Bei bestätigter Wahl Werte kopieren, Mut auf 4, Glück auf 2 und vier Ausrüstungsplätze vergeben. Erst wenn beide Figuren gewählt und Bindung/Würfelmodus bestätigt sind, `party.starting_resources_granted` auf true und gemeinsame Münzen auf 12 setzen. Bei späterer Wiederaufnahme niemals erneut Startressourcen ausgeben. Benutzerdefinierte Rollen nur nach Zustimmung in derselben Datei registrieren.
