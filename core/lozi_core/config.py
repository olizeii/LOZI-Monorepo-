"""Einstellungen kommen aus Umgebungsvariablen (siehe deploy/lozi-core/.env.example)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _liste(wert: str) -> list[str]:
    return [teil.strip() for teil in wert.split(",") if teil.strip()]


@dataclass(frozen=True)
class Config:
    host: str = "0.0.0.0"
    port: int = 8765
    # Bekannte Bildschirme. Der erste ist der Standard, wenn niemand einen nennt.
    displays: list[str] = field(default_factory=lambda: ["tv", "beamer", "roehre", "boxautomat"])
    # Host-Header, die der MCP-Endpunkt akzeptiert (Schutz gegen DNS-Rebinding).
    # Beispiel: "10.0.0.90:*,lozi-core:*"
    allowed_hosts: list[str] = field(default_factory=lambda: ["127.0.0.1:*", "localhost:*"])
    # Optionales Token für POST /api/zustand. Leer = keine Prüfung (nur im Heimnetz!).
    api_token: str = ""
    log_level: str = "INFO"

    @property
    def standard_display(self) -> str:
        return self.displays[0]

    @classmethod
    def aus_umgebung(cls) -> "Config":
        standard = cls()
        return cls(
            host=os.environ.get("LOZI_HOST", standard.host),
            port=int(os.environ.get("LOZI_PORT", standard.port)),
            displays=_liste(os.environ.get("LOZI_DISPLAYS", "")) or standard.displays,
            allowed_hosts=_liste(os.environ.get("LOZI_ALLOWED_HOSTS", "")) or standard.allowed_hosts,
            api_token=os.environ.get("LOZI_API_TOKEN", ""),
            log_level=os.environ.get("LOZI_LOG_LEVEL", standard.log_level).upper(),
        )
