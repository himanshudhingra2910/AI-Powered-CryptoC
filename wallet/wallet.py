import os
import json

class Wallet:
    def __init__(self, user):
        self.user = user
        self.wallet_file = os.path.join("wallet", f"{user}_wallet.json")
        self.data = self.load_wallet()
        self.normalize_currency_keys()  # Fix mixed-case duplicates

    def load_wallet(self):
        if not os.path.exists(self.wallet_file):
            return {"currencies": {}}
        with open(self.wallet_file, "r") as f:
            return json.load(f)

    def save_wallet(self):
        with open(self.wallet_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def normalize_currency_keys(self):
        """Ensure all currency keys are lowercase and merged properly."""
        normalized = {}
        for k, v in self.data.get("currencies", {}).items():
            k_lower = k.lower()
            normalized[k_lower] = normalized.get(k_lower, 0) + v
        self.data["currencies"] = normalized
        self.save_wallet()

    def create_currency(self, currency_name):
        currency_name = currency_name.lower()
        if currency_name not in self.data["currencies"]:
            self.data["currencies"][currency_name] = 0
            self.save_wallet()
            print(f"🪙 New currency created: {currency_name}")
        else:
            print(f"⚠️ Currency '{currency_name}' already exists.")

    def credit(self, currency_name, amount):
        currency_name = currency_name.lower()
        if currency_name not in self.data["currencies"]:
            self.create_currency(currency_name)
        self.data["currencies"][currency_name] += amount
        self.save_wallet()
        print(f"💰 {amount} {currency_name} credited to {self.user}'s wallet.")

    def get_balances(self):
        """Returns a copy of user's wallet balances in lowercase."""
        return dict(sorted(self.data["currencies"].items()))

    def trade_currency(self, from_coin, to_coin, amount, exchange_rates):
        from_coin = from_coin.lower()
        to_coin = to_coin.lower()
        balances = self.data["currencies"]

        if from_coin not in balances or balances[from_coin] < amount:
            print("❌ Insufficient balance.")
            return False

        rate = exchange_rates.get(to_coin, 1.0)
        received = round(amount * rate, 2)

        # Trade execution
        balances[from_coin] -= amount
        balances[to_coin] = balances.get(to_coin, 0) + received

        # Ocean equilibrium: Reduce all other coins slightly
        for coin in balances:
            if coin not in [from_coin, to_coin]:
                balances[coin] = round(balances[coin] * 0.99, 2)

        print(f"🔄 Traded {amount} {from_coin} ➡️ {received} {to_coin} at rate {rate}")
        self.save_wallet()
        self.log_trade(from_coin, to_coin, amount, received, rate)
        return True

    def log_trade(self, from_coin, to_coin, amount, received, rate):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{self.user}_trades.log")

        with open(log_file, "a") as f:
            f.write(
                f"TRADE | {from_coin.upper()} ➡️ {to_coin.upper()} | "
                f"{amount} {from_coin} ➡️ {received} {to_coin} | Rate: {rate}\n"
            )
