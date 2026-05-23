from modes.operation_mode import OperationMode
from shared.padding import Padding

class ECBMode(OperationMode):
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        padded = Padding(self.BLOCK_SIZE).pad(plaintext)

        blocks = self.split_blocks(padded)
        
        final_key = self.algorithm.prepare_key(key)

        cipher = b""
        for block in blocks:
            cipher += self.algorithm.encrypt(block, final_key)

        return cipher

    def decrypt(self, cipher: bytes, key: bytes) -> bytes:
        blocks = self.split_blocks(cipher)
        
        final_key = self.algorithm.prepare_key(key)

        plaintext = b""
        for block in blocks:
            plaintext += self.algorithm.decrypt(block, final_key)

        return Padding(self.BLOCK_SIZE).unpad(plaintext)
