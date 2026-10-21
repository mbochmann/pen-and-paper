# Ergänzungen aus Spielzug 6

## Leih-Brieftauben

Die Spieler haben je zwei Tauben gewünscht. Als neue, ausgespielte Gelegenheit verfügt Livias Wasserbauwerkstatt über vier trainierte Heimkehrtauben. Sie hat diese kostenlos für die Ermittlung ausgeliehen; keine rückwirkende Startausrüstung und keine Ausgabe gemeinsamer Münzen.

IDs `item-pigeon-1/2` bei Cäsar, `item-pigeon-3/4` bei Augustus. Je Vogel mit kleinem Transportkorb und Nachrichtenzetteln ein Platz. Beide Figuren nun 6/6. Die Tiere sind ruhige Reisetiere; keine zusätzliche Tierpflege-Buchhaltung, kein unangekündigtes Tierleid. Diese konkrete Werkstattausstattung ist Fiktion, keine historische Tatsachenbehauptung.

Alle vier haben denselben Heimatschlag: `loc-workshop`. Livia bleibt als Empfängerin dort. Sie fliegen nach Freilassen nach Hause, nicht zum Aufenthaltsort des anderen Helden. Noch kein Vogel ist losgeschickt. Für eine Nachricht konkreten Text/Absicht und Absender festhalten. Nach Freilassen Besitz des Vogels in `current.json` korrekt übertragen und Status als world_change festhalten. Leerer Korb verbleibt bis zum Ablegen bei der Figur; frei gewordenen Platz nicht doppelt zählen. Ankunft und tatsächliches Lesen getrennt von Versand etablieren; keine verzögerungsfreie Übermittlung. Zustellung an den anderen Helden erst durch ausdrücklich ausgespielten plausiblen Botenweg. Nachrichtentexte können Kenntnis nur bei tatsächlichem Empfang erweitern. Keine Antworten durch dieselbe Taube ohne erneuten Transport zum Absender.

## Wache am Mühlentor

`npc-gatekeeper`, Name unbekannt; neutraler Diensthabender aus den vorbereiteten Torwachen. Möchte verhindern, dass Unkundige die Wasseranlage beschädigen. Kennt den Auftrag noch nicht. Ehrliche Erklärung des Ausfalls und Hilfe für Livia erlaubt Gespräch/überwachte Inspektion. Ein Redner-Talent kann einen wahren Beweggrund ergeben (Angst vor Ärger bei einer beschädigten Anlage), aber ist nicht erforderlich. Unbegründetes Einschleichen kann eine angekündigte Geschickprobe 7 auslösen; bei Misslingen folgt ein Gespräch, kein automatischer Kampf.

## Parallele Zeitskala

Cäsars Ankunft nach etwa 30 Minuten, Augustus' nach etwa 45 Minuten werden als eine parallele Reisephase abgebildet. Erzählblöcke sind zeitlich versetzt; Cäsar hat nicht eigenmächtig 15 Minuten gewartet. Kurze Handlungen beider Orte zunächst in diesem Zeitfenster abwickeln. Nicht pro Spieler oder Chatantwort die Weltuhr erhöhen. Bei neuem längerem Vorgehen Kosten vorher ansagen und zeitliche Überlappung beachten.

Aktueller sichtbarer Kontext ist `scene-03` am Mühlentor; Augustus' offener Kontext `scene-05` am Steinbruch ist in world_changes und Übergabe festgehalten. Bei Spotlightwechsel `scene_id`, `location_id` und `present_npc_ids` auf den aktuellen Ort setzen. Keine gemeinsame Fernkenntnis: Wachenwissen nur Cäsar, Steinbruchbeobachtungen nur Augustus, bis Nachrichten oder Treffen stattfinden.
