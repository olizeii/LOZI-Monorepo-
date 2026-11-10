"""Display-Hub: hält die WebSocket-Verbindungen aller Lozi-Clients und schickt ihnen Nachrichten.

Protokoll: siehe docs/display-protokoll.md. Jede Nachricht ist ein JSON-Objekt mit dem Feld "typ".
"""
from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

log = logging.getLogger("lozi.display")

ZUSTAENDE = ("schlaeft", "hoert_zu", "denkt", "spricht")


class Sender(Protocol):
    async def send_json(self, data: Any) -> None: ...


@dataclass
class _DisplayState:
    clients: set[Sender] = field(default_factory=set)
    letzter_inhalt: dict[str, Any] | None = None
    zustand: str = "schlaeft"


class UnbekanntesDisplay(ValueError):
    pass


class DisplayHub:
    def __init__(self, displays: list[str]):
        if not displays:
            raise ValueError("Mindestens ein Display muss konfiguriert sein")
        self._displays = {name: _DisplayState() for name in displays}
        self._lock = asyncio.Lock()

    # --- Abfragen -------------------------------------------------------
    @property
    def namen(self) -> list[str]:
        return list(self._displays)

    def verbunden(self, display: str) -> bool:
        return bool(self._state(display).clients)

    def uebersicht(self) -> list[dict[str, Any]]:
        return [
            {"display": name, "verbunden": bool(s.clients), "clients": len(s.clients), "zustand": s.zustand}
            for name, s in self._displays.items()
        ]

    def _state(self, display: str) -> _DisplayState:
        try:
            return self._displays[display]
        except KeyError:
            raise UnbekanntesDisplay(
                f"Unbekanntes Display '{display}'. Bekannt sind: {', '.join(self._displays)}"
            ) from None

    # --- Verbindungen ---------------------------------------------------
    async def anmelden(self, display: str, client: Sender) -> None:
        state = self._state(display)
        async with self._lock:
            state.clients.add(client)
        log.info("Client an Display '%s' angemeldet (%d verbunden)", display, len(state.clients))
        await client.send_json({"typ": "hallo", "display": display, "zustand": state.zustand})
        if state.letzter_inhalt is not None:
            await client.send_json(state.letzter_inhalt)

    async def abmelden(self, display: str, client: Sender) -> None:
        state = self._state(display)
        async with self._lock:
            state.clients.discard(client)
        log.info("Client von Display '%s' abgemeldet (%d verbunden)", display, len(state.clients))

    # --- Senden ---------------------------------------------------------
    async def zeige(self, display: str, art: str, titel: str, inhalt: str) -> int:
        nachricht = {"typ": "zeige", "art": art, "titel": titel, "inhalt": inhalt, "zeit": time.time()}
        self._state(display).letzter_inhalt = nachricht
        return await self._senden(display, nachricht)

    async def leeren(self, display: str) -> int:
        self._state(display).letzter_inhalt = None
        return await self._senden(display, {"typ": "leeren"})

    async def setze_zustand(self, display: str, zustand: str) -> int:
        if zustand not in ZUSTAENDE:
            raise ValueError(f"Unbekannter Zustand '{zustand}'. Erlaubt: {', '.join(ZUSTAENDE)}")
        self._state(display).zustand = zustand
        return await self._senden(display, {"typ": "zustand", "zustand": zustand})

    async def _senden(self, display: str, nachricht: dict[str, Any]) -> int:
        state = self._state(display)
        async with self._lock:
            clients = list(state.clients)
        erreicht = 0
        for client in clients:
            try:
                await client.send_json(nachricht)
                erreicht += 1
            except Exception:  # Verbindung tot – aufräumen, Rest weiter beliefern
                log.warning("Senden an Display '%s' fehlgeschlagen, Client wird entfernt", display)
                await self.abmelden(display, client)
        return erreicht
