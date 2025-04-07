from blockchain.blockchain import Blockchain

my_chain = Blockchain()

# Add some transactions
my_chain.add_transaction("Alice uploaded an image")
my_chain.add_transaction("Bob mined using a poem")

# Mine the block
my_chain.mine_pending_transactions()

# View the blockchain
for block in my_chain.chain:
    print(f"Index: {block.index}, Hash: {block.hash}")
    print(f"Transactions: {block.transactions}")
