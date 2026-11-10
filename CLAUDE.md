# LOZI – Anweisungen für Claude Code

Lozi ist Olivers Sprachassistent für seine Räume („Hey Lozi“): Licht, Bildschirme, Beamer, Musik in mehreren
Räumen, Kameras, Dart, Boxautomat und eine Einkaufsliste. Dieses Repo enthält **alles außer Home Assistant selbst**.
Lies vor jeder Arbeit `docs/architektur.md`. Sprache im Code, in Commits und in der Doku: **Deutsch**.

## Grundprinzip

- **Home Assistant (HA) ist das Rückgrat.** Es kennt alle Geräte, macht die Sprachkette (Wake-Word → Spracherkennung
  → Sprachmodell → Stimme) und erledigt einfache Befehle lokal. Was HA mit Bordmitteln oder einer fertigen
  Integration kann, bauen wir **nicht** nach.
- **Claude ist der Gesprächspartner** über die Anthropic-Integration in HA.
- **Lozi-Core (`core/`) ist ein MCP-Server.** HA bindet ihn über die Integration „Model Context Protocol“ ein und
  reicht seine Tools an Claude weiter. Alles, was HA nicht kann (Bildschirme ansteuern, Kamera-Rückblick, Dart …),
  wird hier ein Tool.
- **Lozi-Client (`client/`) ist eine Web-App** im Vollbild auf jedem Bildschirm (Chromecast am TV, PCs, Boxautomat).
  Sie zeigt den Avatar und was Lozi-Core per WebSocket schickt.
- **Jedes Feature ist ein Modul** mit klarer Schnittstelle. Ein Modul darf nur über seine Tools, MQTT-Topics oder
  das Display-Protokoll mit dem Rest reden.

## Infrastruktur

- Server: Proxmox VE 9 auf i5-6500, aktuell 8 GB RAM (16 GB geplant), 240-GB-SSD, 6 TB WD Red für Aufnahmen.
- VM „Home Assistant OS“ (Add-ons: Mosquitto, Music Assistant).
- LXC „docker“: Lozi-Core, später Frigate (mit Intel-iGPU).
- Bestehender CT 101 `matrix-server` – nicht anfassen.
- Alles per LAN, Netz 10.0.0.0/24. Keine Portfreigaben nach außen; Fernzugriff nur per VPN.

## Regeln für Code

- Python ≥ 3.12, Typen überall, kleine Module. Bibliothek für MCP: `mcp` 2.x (`from mcp.server.mcpserver import MCPServer`,
  **nicht** das alte `FastMCP`).
- Neue Tools nach `docs/tool-vertraege.md`: deutscher snake_case-Name, Docstring sagt dem Modell *wann* es das Tool
  benutzt, Rückgabe immer `{"ok": bool, ...}`, bei Fehlern ein `hinweis`, den Lozi vorlesen kann.
- Jede Änderung an einem Tool, Topic oder am Display-Protokoll **zuerst** in `docs/` nachziehen.
- Tests mit pytest, laufen ohne Hardware und ohne Netz. Vor jedem Commit: `cd core && pytest -q`.
- Geheimnisse nur in `.env` (nie committen). Beispielwerte in `.env.example`.
- API-Kosten: Ziel klar unter 100 € im Monat. Nichts bauen, das ohne Grund das Sprachmodell in Schleifen aufruft.

## Regeln für Oberflächen (`client/`)

Keine typische „KI-Design“-Optik. Bei UI-Arbeit die installierten Design-Skills verwenden (apple-design u. a.).
Der Avatar ist eine schlichte, futuristische 2D-Figur, die auf Sprechen und Zuhören reagiert.

## Persönlichkeit und Zentrale

- Lozi redet wie ein Kumpel, nicht wie eine KI: kurz, gesprochen, locker, österreichisch. Maßgeblich ist
  `homeassistant/persona/lozi.md`. Jede Antwort, die Lozi vorliest, muss dazu passen (keine Listen, kein Markdown).
- Die **Lozi-Zentrale** (`zentrale/`, Spezifikation `docs/zentrale.md`) ist die Web-Oberfläche für alles.
  Neue Module müssen sich im Modul-Register melden, damit sie dort automatisch erscheinen.

## Arbeitsweise

Bau-Aufträge stehen in `docs/bau-auftraege.md`. Pro Auftrag ein Branch und ein Pull Request; Oliver merged.

## Aktueller Stand

Phase 1 (Grundgerüst). Fertig: Lozi-Core mit Display-Hub und Tools `zeige_auf`, `bildschirm_leeren`,
`displays_auflisten`. Als Nächstes: HA-VM aufsetzen (`docs/setup/01-proxmox.md`), Lozi-Core einbinden,
Lozi-Client mit Avatar bauen. Den Phasenplan findest du in `docs/architektur.md`.
