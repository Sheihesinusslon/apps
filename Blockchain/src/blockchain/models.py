from typing import Sequence, NewType

from pydantic import BaseModel

HashString = NewType("HashString", str)


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class Block(BaseModel):
    index: int
    timestamp: int
    transactions: Sequence
    proof: int
    previous_hash: HashString
