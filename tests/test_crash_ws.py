import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_websocket_crash_multiple_players():
    with client.websocket_connect("/ws") as ws:
        # Envoyer plusieurs joueurs dans un round
        payload = {
            "command": "numeric_crash",
            "players": [
                {"id": 1, "bet": 100, "auto_cashout": 2.0, "risk_factor": 1.2},
                {"id": 2, "bet": 50, "auto_cashout": 5.0, "risk_factor": 0.8}
            ]
        }
        ws.send_json(payload)

        # Recevoir le résultat
        data = ws.receive_json()

        # Vérifications principales
        assert "round_id" in data
        assert "crash_point" in data
        assert "proof" in data
        assert "result" in data
        assert isinstance(data["result"], list)

        # Vérifier que chaque joueur est bien traité
        assert len(data["result"]) == 2
        for player in data["result"]:
            assert "id" in player
            assert "bet" in player
            assert "auto_cashout" in player
            assert "win" in player
            assert player["status"] in ["winner", "loser"]
