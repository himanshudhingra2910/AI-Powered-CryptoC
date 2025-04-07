from economy.leaderboard import get_leaderboard

board = get_leaderboard()
print("\n🏆 Current Crypto Leaderboard:\n")
for rank, (coin, dom) in enumerate(board, 1):
    print(f"{rank}. {coin} — Dominance Score: {dom}")
