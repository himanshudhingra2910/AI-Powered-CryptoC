import os
import json

def get_leaderboard(metadata_dir="metadata"):
    leaderboard = []
    for file in os.listdir(metadata_dir):
        if file.endswith("_meta.json"):
            coin = file.replace("_meta.json", "")
            with open(os.path.join(metadata_dir, file), "r") as f:
                data = json.load(f)
                score = data.get("score", 0)
                mines = data.get("mines", 0)
                uploads = data.get("uploads", 0)
                dominance = score + (2 * mines) + (uploads * 0.5)
                leaderboard.append((coin, dominance))

    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard
