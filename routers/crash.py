from fastapi import APIRouter
from games.numeric_crash import simulate_numeric_crash

router = APIRouter()

@router.post("/crash/play")
def play_crash(players: list[dict]):
    """
    Exemple payload JSON :
    [
        {"id": 1, "bet": 100, "auto_cashout": 2.0, "risk_factor": 1.2},
        {"id": 2, "bet": 50, "auto_cashout": 5.0, "risk_factor": 0.8}
    ]
    """
    result = simulate_numeric_crash(players)
    return result
