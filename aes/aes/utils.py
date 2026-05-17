from typing import Optional

from aes.tables.sbox import S_BOX


def extract_words(block: bytes, word_size: Optional[int] = 4) -> list[bytes]:
    return [block[i : i + word_size] for i in range(0, len(block), word_size)]

def xor_words(word1: bytes, word2: bytes) -> bytes:
    return bytes(xor(a, b) for a, b in zip(word1, word2))

def xor(a: int, b: int) -> int:
    return a ^ b

def get_sbox_value_for(byte: int):
    row = byte >> 4
    col = byte & 0x0F
    return S_BOX[row][col]

def get_inv_sbox_value_for(byte: int):
    row = byte >> 4
    col = byte & 0x0F
    return S_BOX[row][col]