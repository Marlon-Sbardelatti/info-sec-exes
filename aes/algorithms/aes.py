from typing import Optional

from aes.algorithms.base import CipherAlgorithm


class AES(CipherAlgorithm):
    def __init__(self, block_size: Optional[int] = 16):
        super().__init__('AES', block_size)
        self.key_schedule = []

    def _extract_words(self, key: bytes) -> list[bytes]:
        skip = 4
        words = []

        for i in range(0, len(key), skip):
            start = i * skip
            end = start + skip
            words[i] = key[start:end]

        return words

    def _expand_key(self, key: bytes):
        pass

    def encrypt(self, key, plaintext):
        return super().encrypt(key, plaintext)
    
    def decrypt(self, key, cipher):
        return super().decrypt(key, cipher)