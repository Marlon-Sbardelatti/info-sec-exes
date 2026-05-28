from Crypto.Cipher import AES

def main():
    exercise_1()
    # exercise_2()
    # exercise_3()
    # exercise_4()

def print_with_spaces(value: bytes):
    value_hex = value.hex()

    bytes_hex = [value_hex[i : i + 2] for i in range(0, len(value_hex), 2)] 
    output = " ".join(bytes_hex)

    print(output)

def exercise_1():
    print("Texto limpo: SEGURANCA DA INFORMACAO")
    plaintext = b"SEGURANCA DA INFORMACAO"
    print(f"Tamanho do texto limpo: {len(plaintext)} bytes")

    key = bytes(range(50,66)) # chave com bytes de 50 a 65
    nonce = bytes([99] * 12) # nonce com 12 bytes de valor 99
    counter = bytes([0, 0, 0, 2])   

    ciphertext = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=counter).encrypt(plaintext)

    print("Texto cifrado:")
    print_with_spaces(ciphertext)
    print(f"Tamanho do texto cifrado: {len(ciphertext)} bytes")

def exercise_2():
    print("Texto limpo: SEGURANCA DA INFORMACAO")
    plaintext = b"SEGURANCA DA INFORMACAO"
    print(f"Tamanho do texto limpo: {len(plaintext)} bytes")

    key = bytes(range(50,66)) # chave com bytes de 50 a 65
    nonce = bytes([99] * 12) # nonce com 12 bytes de valor 99
    aad = b"main.py" # nome do programa como AAD

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    print("Texto cifrado:")
    print_with_spaces(ciphertext)
    print(f"Tamanho do texto cifrado: {len(ciphertext)} bytes")
    print(f"Tag de autenticação:")
    print_with_spaces(tag)
    print(f"Tamanho da tag de autenticação: {len(tag)} bytes")

    # salvar o texto cifrado em arquivo
    with open("./ciphertext.bin", "wb") as f:
        f.write(ciphertext)
        f.write(tag)

    print("Texto cifrado salvo no arquivo 'ciphertext.bin'.")

def exercise_3():
    with open("./ciphertext.bin", "rb") as f:
        content = f.read() 
        ciphertext = content[:-16]  # tudo menos os últimos 16 bytes
        tag = content[-16:]  # últimos 16 bytes

    print("Texto cifrado:")
    print_with_spaces(ciphertext)
    print(f"Tag de autenticação:")
    print_with_spaces(tag)

    key = bytes(range(50,66)) # chave com bytes de 50 a 65
    nonce = bytes([99] * 12) # nonce com 12 bytes de valor 99
    aad = b"main.py" # nome do programa como AAD

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    print("Texto decifrado:")
    print(plaintext.decode())

def exercise_4():
    with open("./edited_ciphertext.bin", "rb") as f:
        content = f.read() 
        ciphertext = content[:-16]  # tudo menos os últimos 16 bytes
        tag = content[-16:]  # últimos 16 bytes

    print("Texto cifrado:")
    print_with_spaces(ciphertext)
    print(f"Tag de autenticação:")
    print_with_spaces(tag)

    key = bytes(range(50,66)) # chave com bytes de 50 a 65
    nonce = bytes([99] * 12) # nonce com 12 bytes de valor 99
    aad = b"main.py" # nome do programa como AAD

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    print("Texto decifrado:")
    print(plaintext.decode())

if __name__ == "__main__":
    main()
