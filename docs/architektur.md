# Architektur

## Datenfluss eines Sprachbefehls

```
Satellit (Wake-Word „Hey Lozi“)
  → Home Assistant Assist-Pipeline
      → Spracherkennung (Cloud)
      → einfacher Befehl? → HA schaltet sofort lokal (z. B. „Licht links aus“)
      → sonst Claude (Anthropic-Integration)
            → HA-Tools (Geräte steuern)
            → Lozi-Core-Tools per MCP (zeige_auf, später kamera_rueckblick, dart_starten …)
      → Stimme (geklonte Stimme, Cloud) → Satellit im selben Raum
Lozi-Core → WebSocket → Lozi-Client (TV, Beamer, Röhre, Boxautomat)
```

- **Raum:** Der Satellit, der das Wake-Word hört, bestimmt den Raum. Antworten und „Musik leiser“ gelten dort.
- **Charaktere:** pro Satellit bis zu zwei Wake-Words mit je eigener Pipeline (Stimme + Persönlichkeit).
- **Ducking:** Beim Wake-Word senkt HA Musik und TV im Raum ab (fremde Boxen kann der Satellit nicht herausrechnen).
- **Ohne Internet:** Schalter und Fernbedienungen funktionieren weiter, Lozi selbst nicht. Das ist so gewollt.

## Komponenten

| Komponente | Wo | Aufgabe |
| --- | --- | --- |
| Home Assistant OS | Proxmox-VM | Geräte, Sprachkette, Szenen, Einkaufsliste, Wake-on-LAN |
| Mosquitto | HA-Add-on | MQTT-Bus für eigene Module (Boxautomat, Dart) |
| Music Assistant | HA-Add-on | Multiroom-Musik (Sendspin), Lautstärke pro Raum |
| Lozi-Core | Docker-LXC | MCP-Server + Display-Hub |
| Frigate | Docker-LXC (Phase 3) | Kameras, Clips, Highlights (Intel-iGPU) |
| Lozi-Client | jeder Bildschirm | Avatar + Inhalte im Vollbild-Browser |
| Satelliten | Hauptraum (Voice PE), Küche + Werkstatt (ReSpeaker Lite) | Mikrofon + Lautsprecherausgang |

## Phasen

1. **Grundgerüst:** HA-VM, Lozi-Core, Shellys, LED-Strips, Satelliten, Avatar am TV, Einkaufsliste.
   Fertig, wenn „Hey Lozi, mach's cozy“ in jedem Raum klappt und der TV den Avatar zeigt.
2. **Medien:** IR für Receiver/Beamer, Client auf allen PCs, Wake-on-LAN, Multiroom-Audio, geklonte Stimme.
3. **Kameras & Boxautomat:** Frigate, Rückblick per Sprache, MQTT-Brücke im Boxautomat.
4. **Spaß & Ausbau:** Autodarts, Emulatoren, Highlight-KI, weitere Charaktere, Sprechererkennung.

Das ausführliche Konzept mit Einkaufsliste liegt als Dokument bei Oliver.
