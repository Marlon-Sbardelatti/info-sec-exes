from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import Blowfish


def main():
    second()
    third()
    fourth()
    fifth()
    sixth()
    seventh()
    eighth()
    nineth()


def blowfish_ecb_encrypt(
    plaintext: bytes, key: bytes = bytes([65, 66, 67, 68, 69])
) -> bytes:
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_message = pad(plaintext, Blowfish.block_size, style="pkcs7")
    encrypted = cipher.encrypt(padded_message)
    pretty_print(encrypted)
    return encrypted


def blowfish_ecb_decrypt(
    plaintext: bytes, key: bytes = bytes([65, 66, 67, 68, 69])
) -> str:
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    decrypted_encoded = cipher.decrypt(plaintext)
    plaintext = unpad(decrypted_encoded, Blowfish.block_size, style="pkcs7")
    decrypted = plaintext.decode("utf-8")
    print("Texto decifrado:")
    print(decrypted)
    return decrypted


def blowfish_cbc_encrypt(
    plaintext: bytes,
    key: bytes = bytes([65, 66, 67, 68, 69]),
    iv: bytes = bytes([1, 1, 2, 2, 3, 3, 4, 4]),
) -> bytes:
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padded_message = pad(plaintext, Blowfish.block_size, style="pkcs7")
    encrypted = cipher.encrypt(padded_message)
    pretty_print(encrypted)
    return encrypted


def pretty_print(value: bytes):
    value_hex = value.hex()
    formatted = ""
    bytes_hex = [value_hex[i : i + 2] for i in range(0, len(value_hex), 2)]

    rows = [bytes_hex[i : i + 8] for i in range(0, len(bytes_hex), 8)]

    for row in rows:
        formatted += " ".join(row) + "\n"

    print("Texto cifrado:")
    print(formatted)


def second():
    print("Texto limpo: COMPUTADOR")
    plaintext = b"COMPUTADOR"
    blowfish_ecb_encrypt(plaintext)


def third():
    print("Texto limpo: SABONETE")
    plaintext = b"SABONETE"
    blowfish_ecb_encrypt(plaintext)


def fourth():
    print("Texto limpo (bytes): [8, 8, 8, 8, 8, 8, 8, 8]")
    plaintext = bytes([8, 8, 8, 8, 8, 8, 8, 8])
    blowfish_ecb_encrypt(plaintext)


def fifth():
    print("Texto limpo: SABONETESABONETESABONETE")
    plaintext = b"SABONETESABONETESABONETE"
    blowfish_ecb_encrypt(plaintext)


def sixth():
    print("Texto limpo: FURB")
    plaintext = b"FURB"
    blowfish_cbc_encrypt(plaintext)


def seventh():
    print("Texto limpo: SABONETESABONETESABONETE")
    plaintext = b"SABONETESABONETESABONETE"
    blowfish_cbc_encrypt(plaintext)


def eighth():
    print("Texto limpo: SABONETESABONETESABONETE")
    plaintext = b"SABONETESABONETESABONETE"
    iv = bytes([10, 20, 30, 40, 50, 60, 70, 80])
    blowfish_cbc_encrypt(plaintext, iv=iv)


def nineth():
    print("Texto limpo: FURB\n")
    plaintext = b"FURB"
    encrypted = blowfish_ecb_encrypt(plaintext)
    blowfish_ecb_decrypt(encrypted, key=bytes([1, 1, 1, 1, 1]))


if __name__ == "__main__":
    main()
