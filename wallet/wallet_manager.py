# wallet/wallet_manager.py
def credit_wallet(user_data, coin_name, amount):
    wallet = user_data.get("wallet", {})
    wallet[coin_name] = wallet.get(coin_name, 0) + amount
    user_data["wallet"] = wallet
    return user_data

def display_wallet(user_data):
    return user_data.get("wallet", {})
