import json

import pytest
from starlette.testclient import TestClient

from lozi_core.app import baue_app
from lozi_core.config import Config


@pytest.fixture
def teile():
    return baue_app(Config(displays=["tv", "beamer"], api_token="geheim"))


def _ergebnis(antwort):
    """call_tool liefert ein CallToolResult; die Daten stecken im ersten Textinhalt."""
    return json.loads(antwort.content[0].text)


async def test_tools_sind_registriert(teile):
    _, mcp, _ = teile
    namen = {t.name for t in await mcp.list_tools()}
    assert {"zeige_auf", "bildschirm_leeren", "displays_auflisten"} <= namen


async def test_zeige_auf_ohne_client_meldet_nicht_verbunden(teile):
    _, mcp, _ = teile
    ergebnis = _ergebnis(await mcp.call_tool("zeige_auf", {"inhalt": "Milch"}))
    assert ergebnis["ok"] is False
    assert "nicht verbunden" in ergebnis["hinweis"]


async def test_zeige_auf_unbekanntes_display(teile):
    _, mcp, _ = teile
    ergebnis = _ergebnis(await mcp.call_tool("zeige_auf", {"inhalt": "x", "display": "kueche"}))
    assert ergebnis["ok"] is False
    assert "Unbekanntes Display" in ergebnis["hinweis"]


def test_display_client_bekommt_inhalt_und_zustand(teile):
    app, _, hub = teile
    with TestClient(app) as client, client.websocket_connect("/ws/display/tv") as ws:
        assert ws.receive_json() == {"typ": "hallo", "display": "tv", "zustand": "schlaeft"}
        assert hub.verbunden("tv")

        client.portal.call(hub.zeige, "tv", "liste", "Einkaufsliste", "Milch\nBrot")
        nachricht = ws.receive_json()
        assert nachricht["typ"] == "zeige" and nachricht["inhalt"] == "Milch\nBrot"

        antwort = client.post(
            "/api/zustand", json={"display": "tv", "zustand": "hoert_zu"},
            headers={"Authorization": "Bearer geheim"},
        )
        assert antwort.status_code == 200 and antwort.json()["clients"] == 1
        assert ws.receive_json() == {"typ": "zustand", "zustand": "hoert_zu"}


def test_neuer_client_bekommt_letzten_inhalt(teile):
    app, _, hub = teile
    with TestClient(app) as client:
        client.portal.call(hub.zeige, "beamer", "text", "Hallo", "Servus")
        with client.websocket_connect("/ws/display/beamer") as ws:
            ws.receive_json()  # hallo
            assert ws.receive_json()["inhalt"] == "Servus"


def test_unbekanntes_display_wird_abgelehnt(teile):
    app, _, _ = teile
    with TestClient(app) as client:
        with pytest.raises(Exception), client.websocket_connect("/ws/display/kueche") as ws:
            ws.receive_json()


def test_zustand_braucht_token_und_gueltigen_wert(teile):
    app, _, _ = teile
    with TestClient(app) as client:
        assert client.post("/api/zustand", json={"zustand": "denkt"}).status_code == 401
        falsch = client.post(
            "/api/zustand", json={"zustand": "tanzt"}, headers={"Authorization": "Bearer geheim"}
        )
        assert falsch.status_code == 400 and "hoert_zu" in falsch.json()["erlaubt"]


def test_health(teile):
    app, _, _ = teile
    with TestClient(app) as client:
        daten = client.get("/health").json()
        assert daten["ok"] and [d["display"] for d in daten["displays"]] == ["tv", "beamer"]


def test_config_aus_umgebung(monkeypatch):
    monkeypatch.setenv("LOZI_DISPLAYS", "tv, roehre")
    monkeypatch.setenv("LOZI_PORT", "9000")
    config = Config.aus_umgebung()
    assert config.displays == ["tv", "roehre"] and config.port == 9000 and config.standard_display == "tv"
