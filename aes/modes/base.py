
from abc import ABC, abstractmethod

from aes.algorithms.base import CipherAlgorithm


class OperationMode(ABC):
    def __init__(self, algorithm: CipherAlgorithm):
        super().__init__()
        self.algorithm = algorithm
        self.block_size = algorithm.block_size

    def split_blocks(self, input: bytes) -> list[list[bytes]]:
        skip = self.block_size
    
        blocks = []
        for i in range(0, len(input), skip):
            start = i * skip
            end = start + skip
            blocks[i] = input[start:end]
        
        return blocks

    @abstractmethod
    def encrypt(self, key: bytes, plaintext: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, key: bytes, cipher: bytes) -> bytes:
        pass