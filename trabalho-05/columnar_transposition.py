import math


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
                cols = int(input("Número de colunas: "))
                plaintext = input("Texto claro: ")

                encrypted = encrypt(plaintext, cols)
                print("Texto cifrado:", encrypted, "\n")

            case 2:
                cols = int(input("Número de colunas: "))
                encrypted_text = input("Texto cifrado: ")

                decrypted = decrypt(encrypted_text, cols)
                print("Texto claro:", decrypted, "\n")

            case 3:
                break

            case _:
                print("Operação inválida.\n")


def encrypt(plaintext: str, cols: int):
    sanitized = plaintext.strip().replace(" ", "")
    matrix = create_matrix(sanitized, cols)
    return encrypt_matrix(matrix, cols)


def create_matrix(plaintext: str, cols: int) -> list[list[str]]:
    plaintext_size = len(plaintext)
    rows = math.ceil(plaintext_size / int(cols))
    matrix = [["X" for _ in range(cols)] for _ in range(rows)]

    idx = 0
    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if idx > plaintext_size - 1:
                break
            matrix[i][j] = plaintext[idx]
            idx += 1

    return matrix


def encrypt_matrix(matrix: list[list[str]], cols: int) -> str:
    encrypted = ""
    rows = len(matrix)

    for col in range(cols):
        for row in range(rows):
            encrypted += matrix[row][col]
    return encrypted


def decrypt(encrypted_text: str, cols: int):
    sanitized = encrypted_text.strip().replace(" ", "")
    matrix = create_matrix_from_encrypted(sanitized, cols)
    return decrypt_matrix(matrix)


def decrypt_matrix(matrix: list[list[str]]) -> str:
    decrypted = ""
    for row in matrix:
        for elm in row:
            decrypted += elm
    return decrypted


def create_matrix_from_encrypted(encrypted_text: str, cols: int) -> list[list[str]]:
    rows = math.ceil(len(encrypted_text) / cols)

    matrix: list[list[str]] = [["" for _ in range(cols)] for _ in range(rows)]

    index = 0
    for clm in range(cols):
        for row in range(rows):
            matrix[row][clm] = encrypted_text[index]
            index += 1
    return matrix


if __name__ == "__main__":
    main()
