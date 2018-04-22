from hashlib import sha256
from datetime import datetime

# Structure of each block in blockchain
class Block:
    # constructor
    def __init__(self, index, previous_hash, timestamp, data, difficulty, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.calculate_hash()

    # Calculates the hash for the block
    def calculate_hash(self, nonce=None):
        if nonce is None:
            nonce = self.nonce

        return sha256(str(self.index) +
                    str(self.previous_hash) +
                    str(self.timestamp) +
                    str(self.data) +
                    str(self.difficulty) +
                    str(self.nonce)
                    ).hexdigest()

# This class handles the creation and validation of blocks
class Blockchain:
    # constructor
    def __init__(self):
        self.difficulty = 2
        self.blockchain = [self.create_genesis_block()]

    # finds the next valid block for given parameters
    def find_block(self, index, previous_hash, data):
        nonce = 0
        while True:
            new_block = Block(index, previous_hash, datetime.now(), data, self.difficulty, nonce)
            if new_block.hash.startswith("0"*self.difficulty):
                return new_block
            nonce = nonce + 1

    # creates genesis block
    def create_genesis_block(self):
        return self.find_block(0, "0", "Genesis block")

    # returns full blockchain
    def get_all_blocks(self):
        return self.blockchain

    # returns the latest block in blockchain
    def get_latest_block(self):
        return self.blockchain[len(self.blockchain) - 1]

    # returns a new block
    def generate_next_block(self, latest_block, data):
        index = latest_block.index + 1
        previous_hash = latest_block.hash
        return self.find_block(index, previous_hash, data)

    # structure validation of block
    def is_valid_structure(self, new_block):
        return type(new_block.index == "number") and type(new_block.previous_hash == "string") and type(new_block.timestamp == "number") and type(new_block.data == "string") and type(new_block.difficulty == "number") and type(new_block.nonce == "number")

    # validation of block based on hashes
    def is_valid_block(self, new_block, old_block):
        if not self.is_valid_structure(new_block):
            print "Not valid structure"
            return False
        if old_block.index + 1 != new_block.index:
            print "Error in indexing", old_block.index, new_block.index
            return False
        elif old_block.hash != new_block.previous_hash:
            print "Error in storing hashes"
            return False
        return True

    # checks whether a block is valid or not
    def validate_block(self, new_block, old_block):
        return self.is_valid_structure(new_block) and self.is_valid_block(new_block, old_block)

    # adds the new_block to the blockchain
    def add_block(self, new_block):
        self.blockchain.append(new_block)
