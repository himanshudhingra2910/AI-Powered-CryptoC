# test_user_coin.py

from blockchain.blockchain import Blockchain
from blockchain.metadata_manager import MetadataManager

coin_name = "skycoin"
user_chain = Blockchain.load_from_file(coin_name)

# Simulate upload (user boosts coin with creative content)
MetadataManager.record_upload(coin_name)

# Add a transaction + mine it
user_chain.add_transaction("User uploaded a digital painting for Skycoin")
user_chain.mine_pending_transactions()
MetadataManager.record_mine(coin_name)

# Save everything
user_chain.save_to_file(coin_name)

# Display chain
print(f"\n=== {coin_name.upper()} CHAIN ===")
for block in user_chain.chain:
    print(f"Block #{block.index} — {block.transactions}")

# Display metadata
print(f"\n=== {coin_name.upper()} METADATA ===")
meta = MetadataManager.load_metadata(coin_name)
print(meta)
