import json
import uuid
import hmac
import hashlib
import time
from fastapi import WebSocket, APIRouter

router = APIRouter()

SECRET_KEY = b"super_secret_key"  # ⚠️ à mettre dans ton .env

@router.websocket("/ws")
async def websocket_handler(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)

            action = payload.get("action")

            if action == "play_crash":
                players = payload.get("players", [])
                round_id = str(uuid.uuid4())
                timestamp = int(time.time())

                # Génération du crash point simulé (exponentiel pour réalisme)
                crash_point = round(1.0 + (time.time() % 5), 2)

                results = []
                for p in players:
                    bet = p.get("bet", 0)
                    auto_cashout = p.get("auto_cashout", crash_point)
                    gain = bet * (crash_point if crash_point < auto_cashout else auto_cashout)
                    results.append({
                        "id": p.get("id"),
                        "bet": bet,
                        "auto_cashout": auto_cashout,
                        "gain": round(gain, 2)
                    })

                # Preuve cryptographique
                proof_data = f"{round_id}:{crash_point}:{timestamp}"
                proof = hmac.new(
                    SECRET_KEY,
                    proof_data.encode(),
                    hashlib.sha256
                ).hexdigest()

                response = {
                    "round_id": round_id,
                    "timestamp": timestamp,
                    "crash_point": crash_point,
                    "results": results,
                    "proof": proof
                }

                await ws.send_text(json.dumps(response))

            elif action == "spectate":
                # Mode spectateur : juste un ping avec crash_point actuel
                crash_point = round(1.0 + (time.time() % 5), 2)
                await ws.send_text(json.dumps({
                    "mode": "spectator",
                    "crash_point": crash_point,
                    "timestamp": int(time.time())
                }))

    except Exception as e:
        await ws.close()
