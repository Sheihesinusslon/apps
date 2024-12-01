import hashlib
import json
from time import time

from blockchain.chain_implementations import Chain, ChainType, create_chain
from blockchain.models import Block, HashString, Transaction


class Blockchain:
    def __init__(self, chain_type: ChainType):
        self.chain: Chain = create_chain(chain_type)
        self.current_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        _ = self.create_new_block(previous_hash=HashString("1"), proof=1)

    def create_new_block(self, previous_hash: HashString, proof: int) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash,
        )

        self.current_transactions = []
        self.chain.add_block(block)
        return block

    def add_new_transaction(self, transaction: Transaction) -> int:
        self.current_transactions.append(transaction)
        return self.chain.last_block.index + 1

    @staticmethod
    def hash_(block: Block) -> HashString:
        block_str = json.dumps(block, sort_keys=True).encode()
        return HashString(hashlib.sha256(block_str).hexdigest())

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            previous_block = self.chain.get_block_by_index(i - 1)
            current_block = self.chain.get_block_by_index(i)

            if current_block.previous_hash != self.hash_(previous_block):
                return False

            if not self.valid_proof(previous_block.proof, current_block.proof):
                return False

        return True
