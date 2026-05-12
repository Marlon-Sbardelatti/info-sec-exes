from typing import override

from aes.modes.base import OperationMode

class ECBMode(OperationMode):
    @override
    def encrypt(self, key, plaintext):
        _ = self.split_blocks(plaintext)
        pass
    
    @override
    def decrypt(self, key, cipher):
        _ = self.split_blocks(cipher)
        pass