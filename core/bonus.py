from sqlalchemy.orm import Session
from core.database import Bonus
from datetime import datetime

def welcome_bonus(db: Session, user_id: int):
    bonus = Bonus(type="welcome", free_turns=5, amount_bigcoin=100, user_id=user_id, timestamp=datetime.utcnow())
    db.add(bonus)
    db.commit()
    db.refresh(bonus)
    return bonus

def ambassador_bonus(db: Session, user_id: int, code: str):
    bonus = Bonus(type="ambassador", free_turns=10, amount_bigcoin=200, promo_code=code, user_id=user_id, timestamp=datetime.utcnow())
    db.add(bonus)
    db.commit()
    db.refresh(bonus)
    return bonus

def random_promo(db: Session, user_id: int):
    bonus = Bonus(type="promo", free_turns=3, amount_bigcoin=50, user_id=user_id, timestamp=datetime.utcnow())
    db.add(bonus)
    db.commit()
    db.refresh(bonus)
    return bonus
