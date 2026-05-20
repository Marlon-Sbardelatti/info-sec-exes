from aes.aes import AES

if __name__ == "__main__":
    aes = AES(b"sabonetesabonete")
    cipher = aes.encrypt(b"historiahistoria")
    print(cipher)

    plain = aes.decrypt(cipher).decode("utf-8")
    print(plain)
