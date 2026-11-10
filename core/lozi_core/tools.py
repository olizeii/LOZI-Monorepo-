"""Lozis Werkzeuge. Home Assistant reicht sie per MCP an das Sprachmodell weiter.

Regeln für neue Tools (siehe auch docs/tool-vertraege.md):
- Name und Parameter auf Deutsch, snake_case, ohne Umlaute.
- Docstring = Beschreibung fürs Sprachmodell: wann benutzen, was kommt zurück.
- Immer ein dict mit "ok" zurückgeben. Bei Fehlern "ok": False und ein "hinweis",
  den Lozi dem Menschen vorlesen kann. Keine Exceptions bis zum Modell durchreichen.
"""
from __future__ import annotations

from typing import Any, Literal

from mcp.server.mcpserver import MCPServer

from .display_hub import DisplayHub, UnbekanntesDisplay

Art = Literal["text", "liste", "bild", "video", "webseite"]


def registriere_tools(mcp: MCPServer, hub: DisplayHub) -> None:
    displays = ", ".join(hub.namen)
    standard = hub.namen[0]

    @mcp.tool(
        description=(
            "Zeigt etwas auf einem Bildschirm im Raum an. Benutze das, wenn der Mensch sagt "
            "'zeig mir', 'mach das auf dem Fernseher/Beamer/der Röhre', oder wenn eine Antwort "
            "besser zu sehen als zu hören ist (Listen, Bilder, längere Texte). "
            f"Bekannte Displays: {displays}. Ohne Angabe: '{standard}'. "
            "art: 'text' (Markdown), 'liste' (eine Zeile pro Punkt), 'bild' / 'video' / 'webseite' (inhalt = URL)."
        )
    )
    async def zeige_auf(inhalt: str, art: Art = "text", titel: str = "", display: str = standard) -> dict[str, Any]:
        try:
            erreicht = await hub.zeige(display, art, titel, inhalt)
        except UnbekanntesDisplay as fehler:
            return {"ok": False, "hinweis": str(fehler)}
        if erreicht == 0:
            return {
                "ok": False,
                "display": display,
                "hinweis": f"Der Bildschirm '{display}' ist gerade nicht verbunden oder ausgeschaltet.",
            }
        return {"ok": True, "display": display, "clients": erreicht}

    @mcp.tool(
        description=(
            "Leert einen Bildschirm, sodass nur noch der Avatar zu sehen ist. "
            "Benutze das bei 'mach das weg', 'schließ das', 'Bildschirm frei'."
        )
    )
    async def bildschirm_leeren(display: str = standard) -> dict[str, Any]:
        try:
            erreicht = await hub.leeren(display)
        except UnbekanntesDisplay as fehler:
            return {"ok": False, "hinweis": str(fehler)}
        return {"ok": True, "display": display, "clients": erreicht}

    @mcp.tool(
        description=(
            "Listet alle Bildschirme und ob sie gerade verbunden sind. Benutze das, bevor du etwas "
            "auf einem Bildschirm zeigen willst, bei dem du unsicher bist, ob er an ist."
        )
    )
    async def displays_auflisten() -> dict[str, Any]:
        return {"ok": True, "displays": hub.uebersicht()}
