import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crash_play_multiple_players():
    payload = [
        {"id": 1, "bet": 100, "auto_cashout": 2.0, "risk_factor": 1.2},
        {"id": 2, "bet": 50, "auto_cashout": 5.0, "risk_factor": 0.8}
    ]

    response = client.post("/crash/play", json=payload)
    assert response.status_code == 200

    data = response.json()
    # Vérifications principales
    assert "round_id" in data
    assert "crash_point" in data
    assert "proof" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    # Vérifier que chaque joueur est bien traité
    assert len(data["results"]) == 2
    for player in data["results"]:
        assert "id" in player
        assert "bet" in player
        assert "auto_cashout" in player
        assert "win" in player
        assert player["status"] in ["winner", "loser"]
