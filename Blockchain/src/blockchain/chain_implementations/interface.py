from typing import Protocol

from blockchain.models import Block


class ChainProtocol(Protocol):
    def add_block(self, block: Block) -> None: ...

    def get_block_by_index(self, index: int) -> Block: ...

    @property
    def last_block(self) -> Block: ...

    def __len__(self) -> int: ...
