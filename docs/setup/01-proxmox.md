# Setup 1: Home Assistant und Lozi-Core auf Proxmox

Ziel: Am Ende kannst du in der Home-Assistant-App am Handy „Zeig mir eine Einkaufsliste mit Milch und Brot
am Fernseher“ sagen, und Lozi-Core bekommt den Auftrag. Dafür ist noch keine neue Hardware nötig.

RAM-Plan mit 8 GB: Proxmox ~1,5 GB · CT 101 matrix-server (bleibt) · HA-VM 3 GB · Docker-LXC 1,5 GB.
Nach der Aufrüstung auf 16 GB bekommt die HA-VM 4 GB und der Docker-LXC 6 GB.

## 0. Vorher

- Proxmox → *Datacenter → pve → Updates → Repositories*: Enterprise-Repos deaktiviert, „No-Subscription“ aktiv.
  Die Warnung „Non production-ready repository enabled“ ist dann normal.
- Backup-Ziel anlegen: externe 4-TB-Platte als Storage (Typ *Directory*, Inhalt *VZDump backup file*).

## 1. Home-Assistant-VM

Im Proxmox-Webinterface: *pve → Shell*, dann:

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
```

*Advanced* wählen: **Stable**, Hostname `homeassistant`, **2 Kerne, 3072 MB RAM**, 32 GB Disk, Bridge `vmbr0`.
Danach im Router eine feste IP für die VM vergeben und `http://<ha-ip>:8123` öffnen, Konto anlegen.

In HA:
1. *Einstellungen → Add-ons*: **Mosquitto broker** installieren und starten. Music Assistant kommt in Phase 2.
2. *Einstellungen → Geräte & Dienste → Integration hinzufügen → Anthropic*, API-Key aus der Anthropic Console.
   Im Konto ein **monatliches Ausgabenlimit** setzen.
3. *Einstellungen → Sprachassistenten*: neuen Assistenten „Lozi“, Sprache Deutsch, Konversationsagent = Claude,
   **„Befehle lokal bevorzugt verarbeiten“** einschalten.

## 2. Docker-LXC für Lozi-Core

In der Proxmox-Shell:

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/docker.sh)"
```

*Advanced*: 2 Kerne, 1536 MB RAM, 16 GB Disk. Feste IP vergeben (Beispiel unten: `10.0.0.90`).
Dann in der Konsole des Containers:

```bash
apt install -y git
git clone https://github.com/olizeii/LOZI-Monorepo-.git /opt/lozi
cd /opt/lozi/deploy/lozi-core
cp .env.example .env
nano .env                    # LOZI_ALLOWED_HOSTS mit der echten IP, LOZI_API_TOKEN setzen
docker compose up -d --build
curl http://localhost:8765/health
```

## 3. Lozi-Core in Home Assistant einbinden

1. *Geräte & Dienste → Integration hinzufügen → Model Context Protocol*, URL `http://10.0.0.90:8765/mcp`.
2. In den Optionen der Anthropic-Integration unter *KI-Tools* zusätzlich **lozi-core** aktivieren.
3. Test im Assist-Dialog (Sprechblase oben rechts oder HA-App am Handy):
   „Welche Bildschirme kennst du?“ → Claude ruft `displays_auflisten` auf.
   „Zeig die Einkaufsliste Milch, Brot am Fernseher“ → Antwort sinngemäß „Der Fernseher ist nicht verbunden“.
   Das ist richtig so, denn der Lozi-Client kommt im nächsten Schritt.

## 4. Backups

*Datacenter → Backup → Hinzufügen*: VM Home Assistant + Docker-LXC, wöchentlich, auf die externe Platte,
Modus *Snapshot*, 4 Stände behalten. Vor jedem großen HA-Update zusätzlich einen Snapshot anlegen.
