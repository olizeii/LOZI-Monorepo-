# LOZI

„Hey Lozi, mach's cozy.“ – Sprachassistent für Licht, Bildschirme, Musik, Kameras, Dart und Boxautomat.
Home Assistant ist das Rückgrat, Claude der Gesprächspartner, und dieses Repo liefert alles dazwischen.

| Ordner | Inhalt |
| --- | --- |
| `core/` | **Lozi-Core**: MCP-Server mit Lozis Werkzeugen + Display-Hub (Python) |
| `client/` | **Lozi-Client**: Web-App mit Avatar für alle Bildschirme |
| `zentrale/` | **Lozi-Zentrale**: Web-Oberfläche mit Übersicht über alles (geplant, `docs/zentrale.md`) |
| `modules/` | Feature-Module (Licht, Kameras, Dart, Audio, Boxautomat-Brücke …) |
| `homeassistant/` | HA-Konfiguration als Code (Szenen, Automatisierungen, Pipelines) |
| `satellites/` | ESPHome-Configs für Voice PE und ReSpeaker Lite |
| `deploy/` | Docker Compose für den Server |
| `docs/` | Architektur, Tool-Verträge, Protokolle, Setup-Anleitungen |

**Loslegen:** `docs/setup/01-proxmox.md`. **Für Claude Code:** `CLAUDE.md`.

## Lozi-Core lokal starten

```bash
cd core
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
lozi-core            # MCP: http://localhost:8765/mcp · Displays: ws://localhost:8765/ws/display/<name>
```
