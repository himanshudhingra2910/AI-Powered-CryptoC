# blockchain/block.py

import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index                      # Position in chain
        self.timestamp = time.time()            # When block is created
        self.transactions = transactions        # List of actions (e.g., mining)
        self.previous_hash = previous_hash      # Hash of previous block
        self.nonce = 0                          # Number used for mining
        self.difficulty = difficulty            # Controls how hard it is to mine
        self.hash = self.calculate_hash()       # Hash of this block

    def calculate_hash(self):
        """
        Creates a SHA256 hash (like a digital fingerprint) of the block’s contents.
        """
        block_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self):
        """
        Simple proof-of-work: keep changing nonce until hash starts with '00' or more depending on difficulty.
        """
        prefix_str = '0' * self.difficulty
        while not self.hash.startswith(prefix_str):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "difficulty": self.difficulty
        }

    @staticmethod
    def from_dict(data):
        block = Block(
            data["index"],
            data["transactions"],
            data["previous_hash"],
            data["difficulty"]
        )
        block.timestamp = data["timestamp"]
        block.nonce = data["nonce"]
        block.hash = data["hash"]
        return block