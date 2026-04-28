from fastapi import FastAPI
from core.database import init_db
from routers import auth, users, transactions, bonuses, crash
from core import websocket   # <-- AJOUT

# Initialisation de l'application FastAPI
app = FastAPI(
    title="BigGame Backend",
    description="Backend artisanal BigGame avec dépôts locaux, bonus et jeux",
    version="1.0.0"
)

# Initialiser la base de données
@app.on_event("startup")
def startup_event():
    init_db()

# Brancher les routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(bonuses.router)
app.include_router(crash.router)
app.include_router(websocket.router)   # <-- AJOUT

# Route de test
@app.get("/")
def root():
    return {"message": "Bienvenue sur BigGame API — Backend Premium artisanal prêt"}
