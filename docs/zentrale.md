# Lozi-Zentrale (Web-Oberfläche)

Eine Oberfläche, in der man **alles von Lozi auf einen Blick** sieht und verwaltet – vom Aufbau her wie die
Proxmox-Oberfläche (links ein Baum, rechts Details), aber eigenständig gestaltet und ohne typische „KI-Design“-Optik.
Läuft im Browser am PC und am Handy, ausgeliefert von Lozi-Core unter `http://<lozi-core>:8765/zentrale/`.

## Aufbau

Links ein Baum, rechts die Ansicht des gewählten Eintrags. Oben eine Statusleiste.

| Bereich im Baum | Inhalt rechts |
| --- | --- |
| **Übersicht** | Gesundheit aller Teile (HA, Lozi-Core, Satelliten, Displays), letzte Gespräche, API-Kosten diesen Monat gegen das Limit |
| **Räume** | Hauptraum, Küche, Werkstatt: Satellit, Lautsprecher, Licht, Display, Kamera je Raum mit Zustand |
| **Module** | Jedes Modul (Licht, Displays, Kameras, Dart, Audio, Boxautomat …) mit Status an/aus, Version, seinen Tools und Einstellungen |
| **Displays** | Verbundene Clients, aktueller Inhalt, Testbutton „etwas anzeigen“ |
| **Charaktere** | Lozi und spätere Charaktere: Wake-Word, Stimme, Persönlichkeit (Prompt), Probehören |
| **Gespräche** | Verlauf: was gesagt wurde, welche Tools liefen, Dauer, Kosten. Zum Nachjustieren der Persönlichkeit |
| **Einkaufsliste** | Liste ansehen, abhaken, ergänzen |
| **System** | Proxmox-Ressourcen (CPU, RAM, Disk), Logs, Backups-Stand |

## Technik

- Statische Web-App (Ordner `zentrale/`), ausgeliefert von Lozi-Core. Live-Daten per WebSocket/REST von Lozi-Core.
- Lozi-Core holt Gerätezustände aus Home Assistant (REST/WebSocket-API mit Long-Lived Token) und
  Server-Werte aus der Proxmox-API (eigener API-Token nur mit Leserechten).
- **Modul-Register:** Jedes Modul meldet sich bei Lozi-Core mit `name`, `version`, `status`, `tools`, `einstellungen`.
  Die Zentrale zeigt daraus automatisch eine Seite pro Modul. So erscheint ein neues Modul ohne Änderung an der Zentrale.
- Zugriff nur im Heimnetz bzw. per VPN, mit Login (ein Passwort reicht).

## Reihenfolge

1. Gerüst mit Baum + Übersicht + Displays (Daten aus Lozi-Core, die es schon gibt).
2. Modul-Register in Lozi-Core, Seite „Module“.
3. Anbindung HA (Räume, Einkaufsliste) und Gesprächsverlauf.
4. Charaktere, Kosten, System.
