# Tool-Verträge (Lozi-Core → Claude)

Alle Tools laufen über den MCP-Endpunkt `http://<lozi-core>:8765/mcp` (Streamable HTTP).

## Regeln

- Name: deutsch, snake_case, ohne Umlaute (`zeige_auf`, `kamera_rueckblick`).
- Beschreibung: sagt dem Modell **wann** es das Tool benutzt, mit Beispielsätzen.
- Parameter mit sinnvollen Standardwerten; der Mensch soll nicht alles sagen müssen.
- Rückgabe immer ein Objekt mit `ok`. Bei `ok: false` ein `hinweis` in einfachem Deutsch, den Lozi vorlesen kann.
- Keine Exceptions bis zum Modell. Kein Tool löst teure Folgeaufrufe aus.

## Vorhanden

| Tool | Parameter | Rückgabe |
| --- | --- | --- |
| `zeige_auf` | `inhalt`, `art` = text·liste·bild·video·webseite, `titel` = "", `display` = erstes Display | `{ok, display, clients}` oder `{ok: false, hinweis}` wenn nicht verbunden/unbekannt |
| `bildschirm_leeren` | `display` | `{ok, display, clients}` |
| `displays_auflisten` | – | `{ok, displays: [{display, verbunden, clients, zustand}]}` |

## Geplant

| Tool | Phase | Idee |
| --- | --- | --- |
| `kamera_rueckblick` | 3 | `raum`, `minuten_zurueck`, `display` → Frigate-Clip auf Display |
| `boxautomat` | 3 | `aktion` = scoreboard·bildschirm_an·bildschirm_aus |
| `dart_starten` | 4 | `spieler`, `modus` (z. B. 501), `double_out` |
| `pc_wecken` / `stream_starten` | 2 | Wake-on-LAN + Moonlight auf Ziel-Display |
