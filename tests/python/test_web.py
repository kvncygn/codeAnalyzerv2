from __future__ import annotations

from pathlib import Path

import pytest
from flask.testing import FlaskClient

from codeanalyzer.analyzer_bridge import find_analyzer
from codeanalyzer.web import create_app


@pytest.fixture(autouse=True)
def _isolate_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Keep last-folder persistence out of the real $HOME during tests.
    monkeypatch.setenv("CODEANALYZER_STATE", str(tmp_path / "state.json"))


@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_pick_folder_is_graceful_without_gui(client: FlaskClient) -> None:
    # Headless CI/dev boxes have no display; the endpoint must report unavailable,
    # never 500. (With a GUI it returns the chosen path instead.)
    resp = client.get("/pick-folder")
    assert resp.status_code == 200
    assert "available" in resp.get_json()


def test_last_folder_is_remembered(client: FlaskClient, tmp_path: Path) -> None:
    client.post("/analyze", data={"folder": str(tmp_path), "prefix": "ABC"})
    body = client.get("/").get_data(as_text=True)
    assert str(tmp_path) in body  # prefilled from saved state
    assert 'value="ABC"' in body


def test_access_token_gate() -> None:
    # A fresh app (not TESTING) enforces the local access token.
    app = create_app()
    token = app.config["ACCESS_TOKEN"]
    c = app.test_client()
    assert c.get("/").status_code == 403  # no token -> blocked
    assert c.get(f"/?t={token}").status_code == 200  # token -> authed (sets cookie)
    # The cookie now authorizes follow-up requests.
    assert c.post("/analyze", data={"folder": "", "prefix": "TCF"}).status_code == 200


def test_index_shows_the_form(client: FlaskClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Folder path" in body
    assert "TCF prefix" in body


def test_empty_folder_shows_error(client: FlaskClient) -> None:
    resp = client.post("/analyze", data={"folder": "", "prefix": "TCF"})
    assert resp.status_code == 200
    assert "Please enter a folder path." in resp.get_data(as_text=True)


def test_invalid_folder_shows_error(client: FlaskClient) -> None:
    resp = client.post("/analyze", data={"folder": "/no/such/dir/zzz", "prefix": "TCF"})
    assert resp.status_code == 200
    assert "does not exist" in resp.get_data(as_text=True)


@pytest.mark.skipif(find_analyzer() is None, reason="analyzer executable not built")
def test_analyze_renders_report(client: FlaskClient, tmp_path: Path) -> None:
    (tmp_path / "S.cs").write_text(
        "class S { public int TCF_M() { return 1; } }", encoding="utf-8"
    )
    resp = client.post("/analyze", data={"folder": str(tmp_path), "prefix": "TCF"})
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Project Summary" in body
    assert "TCF_M" in body
