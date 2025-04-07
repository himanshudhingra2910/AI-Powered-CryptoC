import os
import json

class Exchange:
    def __init__(self, metadata_folder="metadata"):
        self.metadata_folder = metadata_folder
        self.scores = self.load_scores()

    def load_scores(self):
        scores = {}
        for filename in os.listdir(self.metadata_folder):
            if filename.endswith(".json"):
                coin = filename.replace("_meta.json", "")
                with open(os.path.join(self.metadata_folder, filename), "r") as f:
                    data = json.load(f)
                    scores[coin] = data.get("score", 1)
        return scores

    def calculate_exchange_rates(self, base_currency):
        base_score = self.scores.get(base_currency, 1)
        rates = {}
        for coin, score in self.scores.items():
            if coin == base_currency:
                continue
            rate = round(score / base_score, 4) if base_score else 1.0
            rates[coin] = rate
        return rates

    def print_leaderboard(self):
        print("\n🏆 Leaderboard:")
        sorted_coins = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (coin, score) in enumerate(sorted_coins, 1):
            print(f"{rank}. {coin} - Score: {score}")
        print()

    def print_exchange_rates(self, base_currency):
        print(f"\n💱 Exchange rates relative to {base_currency}:")
        rates = self.calculate_exchange_rates(base_currency)
        for coin, rate in rates.items():
            print(f"1 {base_currency} = {rate} {coin}")
        print()
