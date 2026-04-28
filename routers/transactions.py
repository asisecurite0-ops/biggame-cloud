from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, User, Transaction
from core.payment import LocalPaymentSystem
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])
payment_system = LocalPaymentSystem()

# --- Dépôt artisanal ---
@router.post("/deposit")
def deposit(user_id: int, amount_fcfa: float, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    bigcoin = payment_system.deposit(user_id, amount_fcfa)
    user.balance += bigcoin

    tx = Transaction(type="deposit", amount=amount_fcfa, user_id=user.id, timestamp=datetime.utcnow())
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "message": f"Acheter vos BigCoin en FCFA via ce numéro local pour participer au jeu.",
        "user": user.username,
        "bigcoin_credit": bigcoin,
        "balance": user.balance,
        "transaction": tx.id
    }

# --- Retrait artisanal ---
@router.post("/withdraw")
def withdraw(user_id: int, bigcoin: float, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if bigcoin > user.balance:
        raise HTTPException(status_code=400, detail="Solde insuffisant")

    amount_fcfa = payment_system.withdraw(user_id, bigcoin)
    user.balance -= bigcoin

    tx = Transaction(type="withdraw", amount=amount_fcfa, user_id=user.id, timestamp=datetime.utcnow())
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "message": f"Vendre vos BigCoin en FCFA via ce numéro local.",
        "user": user.username,
        "fcfa_credit": amount_fcfa,
        "balance": user.balance,
        "transaction": tx.id
    }

# --- Historique des transactions ---
@router.get("/history/{user_id}")
def transaction_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    txs = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.timestamp.desc()).limit(10).all()
    return [
        {"id": tx.id, "type": tx.type, "amount": tx.amount, "timestamp": tx.timestamp.isoformat()}
        for tx in txs
    ]
