# Display-Protokoll (Lozi-Core ↔ Lozi-Client)

Der Client verbindet sich per WebSocket mit `ws://<lozi-core>:8765/ws/display/<name>`.
`<name>` muss in `LOZI_DISPLAYS` stehen (Standard: `tv,beamer,roehre,boxautomat`), sonst wird die
Verbindung mit Code 4404 geschlossen. Mehrere Clients pro Display sind erlaubt.

Bricht die Verbindung ab, verbindet sich der Client mit wachsender Wartezeit neu (1 s, 2 s, 4 s … max. 30 s).

## Server → Client (JSON, Feld `typ`)

| typ | Felder | Bedeutung |
| --- | --- | --- |
| `hallo` | `display`, `zustand` | direkt nach dem Verbinden |
| `zeige` | `art`, `titel`, `inhalt`, `zeit` | Inhalt anzeigen. `art`: `text` (Markdown), `liste` (eine Zeile pro Punkt), `bild`/`video`/`webseite` (`inhalt` = URL). Wird nach `hallo` erneut geschickt, wenn noch aktuell. |
| `leeren` | – | Inhalt weg, nur Avatar |
| `zustand` | `zustand` = `schlaeft`·`hoert_zu`·`denkt`·`spricht` | Avatar-Animation |

## Client → Server

Bisher nur Text-Pings zum Wachhalten (Inhalt wird ignoriert).

## Zustände aus Home Assistant

HA meldet Satelliten-Zustände per `POST /api/zustand` mit JSON `{"display": "tv", "zustand": "hoert_zu"}`
und Header `Authorization: Bearer <LOZI_API_TOKEN>`. Beispiel für `configuration.yaml`:

```yaml
rest_command:
  lozi_zustand:
    url: "http://10.0.0.90:8765/api/zustand"
    method: POST
    headers:
      Authorization: !secret lozi_api_token
    content_type: "application/json"
    payload: '{"display": "{{ display }}", "zustand": "{{ zustand }}"}'
```

`lozi_api_token` in `secrets.yaml` als `"Bearer <token>"` eintragen.
