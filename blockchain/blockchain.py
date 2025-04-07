# blockchain/blockchain.py
import json
import os
from .block import Block

class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty                # Set difficulty first ✅
        self.chain = [self.create_genesis_block()]  # Then create the genesis block
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0", self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash,
            difficulty=self.difficulty
        )
        new_block.mine_block()
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain]
        }

    @staticmethod
    def from_dict(data):
        blockchain = Blockchain(data["difficulty"])
        blockchain.chain = [Block.from_dict(b) for b in data["chain"]]
        return blockchain

    def save_to_file(self, name):
        filepath = os.path.join("chains", f"{name}_chain.json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @staticmethod
    def load_from_file(name):
        filepath = os.path.join("chains", f"{name}_chain.json")
        if not os.path.exists(filepath):
            return Blockchain()
        with open(filepath, "r") as f:
            data = json.load(f)
            return Blockchain.from_dict(data)