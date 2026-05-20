from abc import ABC, abstractmethod
from aes.aes import AES


class OperationMode(ABC):
    def __init__(self, algorithm: AES):
        super().__init__()
        self.algorithm = algorithm
        self.BLOCK_SIZE = algorithm.BLOCK_SIZE

    def split_blocks(self, input: bytes) -> list[list[bytes]]:
        skip = self.BLOCK_SIZE

        blocks = []
        for i in range(0, len(input), skip):
            start = i * skip
            end = start + skip
            # blocks[i] = input[start:end]
            blocks.append(input[start:end])

        return blocks

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, cipher: bytes) -> bytes:
        pass
