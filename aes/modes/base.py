
from abc import ABC, abstractmethod
from typing import Optional


class OperationMode(ABC):
    def __init__(self, block_size: Optional[int] = 16):
        super().__init__()
        self.block_size = block_size

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