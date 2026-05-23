from aes.aes import AES
from modes.ecb import ECBMode

if __name__ == "__main__":
    key = b"sabonetesabonete"
    
    mode = ECBMode(AES())
    cipher = mode.encrypt(b"historiahistoria", key)
    print('Cifrado', cipher)

    plaintext = mode.decrypt(cipher, key).decode("utf-8")
    print('Decifrado', plaintext)
