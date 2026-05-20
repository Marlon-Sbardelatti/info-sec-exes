from typing import override

from modes.base import OperationMode

class ECBMode(OperationMode):
    @override
    def encrypt(self, plaintext):
        blocks = self.split_blocks(plaintext)

        ciphers = b""
        for b in blocks: 
            ciphers += self.algorithm.encrypt(b)

        return ciphers
    
    @override
    def decrypt(self, cipher):
        blocks = self.split_blocks(cipher)

        plaintext = b""

        for b in blocks:
            plaintext += self.algorithm.decrypt(b)


        return plaintext
