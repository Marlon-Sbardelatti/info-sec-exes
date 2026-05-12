
from abc import ABC, abstractmethod


class CipherAlgorithm(ABC):
    def __init__(self, name: str, block_size: int):
        super().__init__()
        self.name = name
        self.block_size = block_size

    @abstractmethod
    def encrypt(self, key: bytes, plaintext: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, key: bytes, cipher: bytes) -> bytes:
        pass