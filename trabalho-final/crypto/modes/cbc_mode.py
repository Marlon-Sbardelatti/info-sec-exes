from crypto.modes.operation_mode import OperationMode
from crypto.shared import Padding, xor_words


class CBCMode(OperationMode):
    
    def encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        padded = Padding(self.BLOCK_SIZE).pad(plaintext)

        blocks = self.split_blocks(padded)

        final_key = self.algorithm.prepare_key(key)

        last_cipher = iv
        cipher = b""

        for block in blocks:
            xored = xor_words(block, last_cipher)

            current_cipher = self.algorithm.encrypt(
                xored,
                final_key,
            )

            cipher += current_cipher

            last_cipher = current_cipher

        return cipher

    def decrypt(self, cipher: bytes, key: bytes, iv: bytes) -> bytes:
        blocks = self.split_blocks(cipher)

        final_key = self.algorithm.prepare_key(key)

        last_cipher = iv
        plaintext = b""

        for block in blocks:
            decrypted = self.algorithm.decrypt(
                block,
                final_key,
            )

            plaintext += xor_words(
                decrypted,
                last_cipher,
            )

            last_cipher = block

        return Padding(self.BLOCK_SIZE).unpad(plaintext)
