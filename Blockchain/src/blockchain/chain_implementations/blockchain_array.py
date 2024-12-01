from blockchain.models import Block


class ArrayChain:
    def __init__(self):
        self.chain = []

    def add_block(self, block: Block) -> None:
        self.chain.append(block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def get_block_by_index(self, index: int) -> Block:
        return self.chain[index]

    def __repr__(self):
        return f"ArrayChain(chain={self.chain})"

    def __len__(self):
        return len(self.chain)
