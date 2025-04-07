# blockchain/metadata_manager.py

import os
import json

# ✅ Ensure metadata folder exists
if not os.path.exists("metadata"):
    os.makedirs("metadata")

class MetadataManager:
    @staticmethod
    def get_metadata_file(coin_name):
        return os.path.join("metadata", f"{coin_name}_meta.json")

    @staticmethod
    def load_metadata(coin_name):
        path = MetadataManager.get_metadata_file(coin_name)
        if not os.path.exists(path):
            print(f"🧾 Creating new metadata for {coin_name}")
            data = {
                "uploads": 0,
                "mines": 0,
                "score": 0
            }
            MetadataManager.save_metadata(coin_name, data)
            return data
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_metadata(coin_name, data):
        path = MetadataManager.get_metadata_file(coin_name)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


# Leaderboard and Exchange Rate System

def get_leaderboard():
    scores = {}
    for file in os.listdir("metadata"):
        if file.endswith("_meta.json"):
            coin_name = file.replace("_meta.json", "")
            path = os.path.join("metadata", file)
            with open(path, "r") as f:
                data = json.load(f)
                scores[coin_name] = data.get("score", 0)
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    return sorted_scores

def get_exchange_rates(base_coin):
    leaderboard = get_leaderboard()
    if base_coin not in leaderboard:
        return {}

    base_score = leaderboard[base_coin]
    rates = {}

    for coin, score in leaderboard.items():
        if coin == base_coin:
            continue
        if score == 0:
            rates[coin] = "∞"
        else:
            rates[coin] = round(base_score / score, 2)

    return rates
