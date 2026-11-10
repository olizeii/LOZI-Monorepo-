"""Baut die Web-App: MCP unter /mcp, WebSocket für Displays, kleine REST-API für Home Assistant."""
from __future__ import annotations

import hmac
import logging

from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

from . import __version__
from .config import Config
from .display_hub import ZUSTAENDE, DisplayHub, UnbekanntesDisplay
from .tools import registriere_tools

log = logging.getLogger("lozi.app")

ANWEISUNGEN = (
    "Lozi-Core stellt Werkzeuge bereit, mit denen du Inhalte auf den Bildschirmen im Raum zeigst. "
    "Geräte wie Licht steuerst du weiterhin über Home Assistant selbst."
)


def baue_app(config: Config) -> tuple[Starlette, MCPServer, DisplayHub]:
    hub = DisplayHub(config.displays)
    mcp = MCPServer(name="lozi-core", version=__version__, instructions=ANWEISUNGEN)
    registriere_tools(mcp, hub)

    @mcp.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        return JSONResponse({"ok": True, "version": __version__, "displays": hub.uebersicht()})

    @mcp.custom_route("/api/zustand", methods=["POST"])
    async def zustand(request: Request) -> JSONResponse:
        """Home Assistant meldet hier, was der Satellit gerade tut (Avatar-Animation)."""
        if config.api_token:
            gesendet = request.headers.get("authorization", "").removeprefix("Bearer ").strip()
            if not hmac.compare_digest(gesendet, config.api_token):
                return JSONResponse({"ok": False, "hinweis": "Token fehlt oder falsch"}, status_code=401)
        try:
            daten = await request.json()
            display = daten.get("display") or config.standard_display
            erreicht = await hub.setze_zustand(display, daten["zustand"])
        except (KeyError, ValueError, UnbekanntesDisplay) as fehler:
            return JSONResponse(
                {"ok": False, "hinweis": str(fehler), "erlaubt": list(ZUSTAENDE)}, status_code=400
            )
        return JSONResponse({"ok": True, "display": display, "clients": erreicht})

    async def display_socket(websocket: WebSocket) -> None:
        display = websocket.path_params["display"]
        if display not in hub.namen:
            await websocket.close(code=4404, reason="Unbekanntes Display")
            return
        await websocket.accept()
        await hub.anmelden(display, websocket)
        try:
            while True:
                # Clients senden bisher nur Pings; alles andere wird ignoriert.
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            await hub.abmelden(display, websocket)

    sicherheit = TransportSecuritySettings(
        enable_dns_rebinding_protection=True, allowed_hosts=config.allowed_hosts
    )
    app = mcp.streamable_http_app(transport_security=sicherheit, host=config.host)
    app.router.routes.append(WebSocketRoute("/ws/display/{display}", display_socket))
    return app, mcp, hub
