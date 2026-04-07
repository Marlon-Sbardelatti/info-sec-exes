import string

ABC_LIST = list(string.ascii_uppercase)


def main() -> None:
    operation = None

    while operation != 3:
        print("Transposição Geométrica Colunar")
        print("[1] Criptografar")
        print("[2] Descriptografar")
        print("[3] Sair")

        operation = input("Escolha a opção: ")
        if not operation.isnumeric():
            print("Operação inválida.")
            continue

        operation = int(operation)

        match operation:
            case 1:
                key = str(input("Chave (mínimo 3 caracteres): "))
                plaintext = input("Texto claro: ")

                encrypted = encrypt(plaintext, key)
                print("Texto cifrado:", encrypted, "\n")

            case 2:
                key = str(input("Chave (mínimo 3 caracteres): "))
                encrypted_text = input("Texto cifrado: ")

                decrypted = decrypt(encrypted_text, key)
                print("Texto claro:", decrypted, "\n")

            case 3:
                break

            case _:
                print("Operação inválida.\n")


def encrypt(plaintext: str, key: str) -> str:
    plaintext = sanitize(plaintext)
    encrypted = ""

    key_pointer = 0
    for char in plaintext:
        key_char_idx = ABC_LIST.index(key[key_pointer])
        text_char_idx = ABC_LIST.index(char)

        new_char = ABC_LIST[(key_char_idx + text_char_idx) % len(ABC_LIST)]
        encrypted += new_char

        key_pointer = (key_pointer + 1) % len(key)

    return encrypted


def decrypt(encrypted_text: str, key: str) -> str:
    decrypted = ""

    key_pointer = 0
    for char in encrypted_text:
        key_char_idx = ABC_LIST.index(key[key_pointer])
        text_char_idx = ABC_LIST.index(char)

        new_char = ABC_LIST[(text_char_idx - key_char_idx) % len(ABC_LIST)]
        decrypted += new_char

        key_pointer = (key_pointer + 1) % len(key)
    return decrypted


def sanitize(plaintext: str) -> str:
    return plaintext.strip().upper()


if __name__ == "__main__":
    main()
