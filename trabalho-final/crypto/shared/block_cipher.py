from abc import ABC, abstractmethod
from typing import Generic, TypeVar

KeyT = TypeVar("KeyT")


class BlockCipher(ABC, Generic[KeyT]):
    BLOCK_SIZE: int

    @abstractmethod
    def prepare_key(
        self,
        key: bytes,
    ) -> KeyT:
        pass

    @abstractmethod
    def encrypt(
        self,
        block: bytes,
        key: KeyT,
    ) -> bytes:
        pass

    @abstractmethod
    def decrypt(
        self,
        block: bytes,
        key: KeyT,
    ) -> bytes:
        pass
