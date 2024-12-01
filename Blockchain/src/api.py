from fastapi import FastAPI, status

from blockchain.blockchain_main import Blockchain
from blockchain.chain_implementations import ChainType
from blockchain.models import Transaction

app = FastAPI()
blockchain = Blockchain(chain_type=ChainType.ARRAY_CHAIN)


@app.get("/mine", status_code=status.HTTP_200_OK)
def mine() -> dict:
    """Mining new block: find the proof of work, then add the block to the chain."""
    last_block = blockchain.chain.last_block
    last_proof = last_block.proof

    proof = blockchain.proof_of_work(last_proof)
    blockchain.add_new_transaction(Transaction(sender="0", recipient="miner_address", amount=1))

    previous_hash = blockchain.hash_(last_block)
    block = blockchain.create_new_block(previous_hash, proof)

    return {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": block.transactions,
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }


@app.post("/transactions/new", status_code=status.HTTP_201_CREATED)
def new_transaction(transaction: Transaction) -> dict:
    """Create a new transaction and add it to the blockchain"""
    index = blockchain.add_new_transaction(transaction)

    return {"message": f"Transaction will be added to Block {index}."}


@app.get("/chain", status_code=status.HTTP_200_OK)
def full_chain() -> dict:
    """Return the full blockchain"""
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
