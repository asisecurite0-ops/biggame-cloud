import uuid, json
from datetime import datetime

class LocalPaymentSystem:
    """
    Système artisanal BigCoin :
    - Dépôt : acheter des BigCoin en FCFA via numéro local
    - Retrait : vendre des BigCoin en FCFA via numéro local
    - Garantie : remboursement maison à 100% en cas de perte
    """

    def __init__(self, commission_rate=0.05):
        self.house_account = 0.0
        self.game_account = 0.0
        self.commission_rate = commission_rate
        self.logs = []

    def deposit(self, player_id: int, amount_fcfa: float):
        """Le joueur achète des BigCoin via numéro local"""
        bigcoin = amount_fcfa / 100  # exemple conversion 100 FCFA = 1 BigCoin
        self.game_account += bigcoin
        self.save_logs("deposit", player_id, bigcoin)
        return bigcoin

    def withdraw(self, player_id: int, bigcoin: float):
        """Le joueur vend ses BigCoin via numéro local"""
        amount_fcfa = bigcoin * 100
        if bigcoin > self.game_account:
            # remboursement maison si perte
            self.house_account -= (bigcoin - self.game_account)
            bigcoin = self.game_account
        self.game_account -= bigcoin
        self.save_logs("withdraw", player_id, amount_fcfa)
        return amount_fcfa

    def apply_commission(self, pot: float):
        commission = pot * self.commission_rate
        self.house_account += commission
        return pot - commission

    def forced_crash(self):
        """Crash forcé toutes les 60 minutes → transfert à la maison"""
        self.house_account += self.game_account
        self.save_logs("forced_crash", "house", self.game_account)
        self.game_account = 0.0

    def save_logs(self, type, player, amount):
        log = {
            "id": str(uuid.uuid4()),
            "type": type,
            "player": player,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs.append(log)
        with open("transactions.json", "a") as f:
            f.write(json.dumps(log) + "\n")
