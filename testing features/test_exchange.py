from wallet.wallet import Wallet
from economy.exchange import get_exchange_rate

wallet = Wallet("himanshu")

rate = get_exchange_rate("skycoin", "pikachucoin")
wallet.exchange("skycoin", "pikachucoin", 1, rate)
