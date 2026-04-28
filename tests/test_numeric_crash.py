import pytest
from fastapi.testclient import TestClient
from main import app
from games.numeric_crash import simulate_numeric_crash

client = TestClient(app)

def test_simulate_numeric_crash_basic():
    result = simulate_numeric_crash(bet_amount=100, auto_cashout=2.0, user_id=1)
    assert "crash_point" in result
    assert "proof" in result
    assert "results" in result
    assert isinstance(result["results"], list)

def test_websocket_numeric_crash():
    with client.websocket_connect("/ws") as ws:
        ws.send_json({"command": "numeric_crash", "bet": 100, "auto_cashout": 2.0, "user_id": 1})
        data = ws.receive_json()
        assert "proof" in data
        assert "crash_point" in data
        assert "result" in data
