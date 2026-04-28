from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, User, Bonus
from core.bonus import welcome_bonus, ambassador_bonus, random_promo

router = APIRouter(prefix="/bonuses", tags=["bonuses"])

@router.post("/welcome/{user_id}")
def give_welcome_bonus(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    bonus = welcome_bonus(db, user_id)
    return {"message": "Bonus de bienvenue attribué", "bonus_id": bonus.id}

@router.post("/ambassador/{user_id}")
def give_ambassador_bonus(user_id: int, code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    bonus = ambassador_bonus(db, user_id, code)
    return {"message": "Bonus ambassadeur attribué", "bonus_id": bonus.id}

@router.post("/promo/{user_id}")
def give_random_promo(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    bonus = random_promo(db, user_id)
    return {"message": "Promotion aléatoire attribuée", "bonus_id": bonus.id}

@router.get("/history/{user_id}")
def bonus_history(user_id: int, db: Session = Depends(get_db)):
    bonuses = db.query(Bonus).filter(Bonus.user_id == user_id).order_by(Bonus.timestamp.desc()).limit(10).all()
    return [
        {"id": b.id, "type": b.type, "free_turns": b.free_turns, "amount_bigcoin": b.amount_bigcoin, "timestamp": b.timestamp.isoformat()}
        for b in bonuses
    ]
