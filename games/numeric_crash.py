import uuid, hmac, hashlib, time
import numpy as np
from datetime import datetime

SECRET_KEY = b"biggame_secret_key"

def ai_adjust_crash_point(base_point: float, risk_factor: float) -> float:
    """IA ajuste le crash point selon le profil joueur"""
    adjusted = base_point * (1.0 - (0.05 * (risk_factor - 1)))
    return round(min(max(adjusted, 1.0), 30.0), 2)

def simulate_numeric_crash(players: list[dict]):
    base_point = np.random.exponential(scale=3.0)
    crash_point = round(min(max(base_point, 1.0), 30.0), 2)
    forced = int(time.time()) % 3600 == 0
    round_id = str(uuid.uuid4())

    proof_data = f"{crash_point}:{forced}:{round_id}"
    proof = hmac.new(SECRET_KEY, proof_data.encode(), hashlib.sha512).hexdigest()

    results = []
    winners = []

    for p in players:
        adjusted_crash = ai_adjust_crash_point(crash_point, p.get("risk_factor", 1.0))
        win = 0
        status = "loser"
        if p["auto_cashout"] <= adjusted_crash:
            win = p["bet"] * p["auto_cashout"]
            status = "winner"
            winners.append(p["id"])

        results.append({
            "id": p["id"],
            "bet": p["bet"],
            "auto_cashout": p["auto_cashout"],
            "win": round(win, 2),
            "status": status
        })

    return {
        "round_id": round_id,
        "crash_point": crash_point,
        "forced": forced,
        "winners": winners,
        "results": results,
        "proof": proof,
        "timestamp": datetime.utcnow().isoformat()
    }
