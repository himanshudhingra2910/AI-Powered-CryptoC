from ai.miners.text_miner import TextMiner
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet

user = "himanshu"
coin_name = "dragoncoin"

# Load user's wallet and chain
wallet = Wallet(user)
wallet.create_currency(coin_name)

blockchain = Blockchain()
miner = TextMiner(blockchain, wallet)

# Example mining
text = "The dragon soared above the clouds, its heart full of hope."
miner.mine_text(text, coin_name)
