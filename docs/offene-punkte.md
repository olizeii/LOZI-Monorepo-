# Offene Punkte

Dinge, die später noch erledigt werden müssen. Erledigtes abhaken und mit Datum versehen.

## Netzwerk

- [ ] **Feste IPs im Haupt-Router (10.0.0.138) vergeben.** Aktuell gibt es noch keinen vollen Zugriff auf diesen
      Router. Sobald er da ist, DHCP-Reservierungen anlegen für:
  - Home-Assistant-VM (ID 100), MAC `02:11:DB:B9:C4:22`
  - Docker-LXC mit Lozi-Core (sobald angelegt)
  - Proxmox (10.0.0.86) prüfen, ob die Adresse bereits fest ist
  - später: Satelliten, Chromecast, Shellys, Kameras
  
  Bis dahin laufen die Geräte per DHCP. Ändert sich eine Adresse, müssen `LOZI_ALLOWED_HOSTS` in
  `deploy/lozi-core/.env` und die MCP-URL in Home Assistant angepasst werden.
- Hinweis: Der OpenWrt-Router (TP-Link TL-WR1043ND, 192.168.1.1) hängt nur als Client im 10.0.0.x-Netz
  (WAN 10.0.0.88). Für das Netz von Proxmox und Home Assistant ist er nicht zuständig.

## Speicher

- [ ] `ssd-store` ist überbucht (112 GB zugesagt, ca. 91 GB vorhanden). Belegung unter *pve → Disks → LVM-Thin*
      im Blick behalten (unter 80 %). Große Daten (Aufnahmen, Backups, Musik) nur auf `local-lvm` (6 TB).

## Hardware

- [ ] RAM des Servers von 8 auf 16 GB aufrüsten (vor Frigate / Phase 3). Vorher prüfen: freie Steckplätze, RAM-Typ.
