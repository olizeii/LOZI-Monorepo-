# Bau-Aufträge für Claude Code

Die Umsetzung passiert in **Claude Code** in diesem Repo. Planung und Konzept laufen im Chat.
Jeder Auftrag hier ist so geschrieben, dass er als erste Nachricht in einer neuen Claude-Code-Session
reicht. `CLAUDE.md` wird automatisch gelesen.

Ablauf pro Auftrag: Session starten → Auftrag einfügen → Claude Code plant, baut, testet → Branch + Pull Request
→ Oliver schaut drüber und merged. Danach in `CLAUDE.md` unter „Aktueller Stand“ nachtragen.

## 1. Lozi-Client mit Avatar

> Baue den Lozi-Client in `client/` nach `docs/display-protokoll.md`: eine Web-App ohne Build-Schritt, die
> Lozi-Core unter `/client/?display=<name>` ausliefert. Vollbild, dunkel, für TV aus 3 m Entfernung lesbar.
> Avatar: schlichte futuristische 2D-Figur (Canvas oder SVG), vier Zustände schlaeft/hoert_zu/denkt/spricht mit
> weichen Übergängen. Inhalte (`text`, `liste`, `bild`, `video`, `webseite`) erscheinen neben dem Avatar.
> Automatisches Neuverbinden. Benutze die Design-Skills (apple-design u. a.), keine typische KI-Optik.
> Schreibe Tests für die Auslieferung in Lozi-Core und prüfe das Aussehen mit Playwright-Screenshots.

## 2. Lozi-Zentrale, Schritt 1

> Setze Schritt 1 aus `docs/zentrale.md` um: Gerüst der Zentrale in `zentrale/` mit Baum links (Übersicht,
> Displays) und Detailansicht rechts, ausgeliefert von Lozi-Core unter `/zentrale/`, Login per Passwort aus `.env`.
> Daten aus `/health` und einem neuen WebSocket für Live-Updates. Design-Skills verwenden, eigenständiger Look,
> funktioniert am Handy. Playwright-Screenshots als Nachweis.

## 3. Modul-Register

> Ergänze Lozi-Core um das Modul-Register aus `docs/zentrale.md` (Name, Version, Status, Tools, Einstellungen),
> mache die bestehenden Display-Tools zum ersten Modul „displays“ und zeige die Module in der Zentrale.
> Erst `docs/` anpassen, dann Code, dann Tests.
