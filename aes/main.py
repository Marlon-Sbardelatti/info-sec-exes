from aes.aes import AES
from modes.ecb import  ECBMode

if __name__ == "__main__":
    aes = AES(b"sabonetesabonete")
    mode = ECBMode(aes)
    cipher = mode.encrypt(b"historiahistoria")
    print(cipher)

    plaintext = mode.decrypt(cipher).decode("utf-8")
    print(plaintext)

    # aes = AES(b"sabonetesabonete")
    # cipher = aes.encrypt(b"historiahistoria")
    # print(cipher)
    #
    # plain = aes.decrypt(cipher).decode("utf-8")
    # print(plain)
