from shared.block_cipher import BlockCipher, KeyT

class OperationMode:
    def __init__(self, algorithm: BlockCipher[KeyT]):
        self.algorithm = algorithm
        self.BLOCK_SIZE = algorithm.BLOCK_SIZE
        
    def split_blocks(self, input: bytes) -> list[bytes]:
        skip = self.BLOCK_SIZE

        blocks = []
        for start in range(0, len(input), skip):
            end = start + skip
            blocks.append(input[start:end])

        return blocks
