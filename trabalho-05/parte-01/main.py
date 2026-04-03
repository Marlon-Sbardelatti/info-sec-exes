import math


def main():
    menu()


def menu():
    print(
        "Escolha uma funcionalidade: \n1 - Encriptar \n2 - Descriptografar \n3 - Sair \n"
    )
    option = int(input())

    while option != 3:
        match option:
            case 1:
                encrypt()
            case 2:
                decrypt()

        print(
            "Escolha uma funcionalidade: \n1 - Encriptar \n2 - Descriptografar \n3 - Sair \n"
        )
        option = int(input())


def encrypt():
    # Exemplo de entrada:
    # VAMOS ATACAR O SUL NO FINAL DESTA SEMANA
    print("\nInforme o parâmetro - Número de colunas:")
    param = int(input())

    print("\nInforme o texto claro:")
    plaintext = input().strip()
    plaintext = plaintext.replace(" ", "")

    matrix = create_matrix(plaintext, param)

    encrpyted = encrypt_matrix(matrix, param)
    print("\nTexto encriptado:", encrpyted)
    print()


def create_matrix(plaintext: str, param: int) -> list[list[str]]:
    plaintext_size = len(plaintext)
    rows = math.ceil(plaintext_size / int(param))
    matrix = [["X" for _ in range(param)] for _ in range(rows)]

    idx = 0
    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if idx > plaintext_size - 1:
                break
            matrix[i][j] = plaintext[idx]
            idx += 1

    return matrix


def encrypt_matrix(matrix: list[list[str]], param: int) -> str:
    encrypted = ""
    num_linhas = len(matrix)
    num_colunas = param

    for clm in range(num_colunas):
        for row in range(num_linhas):
            encrypted += matrix[row][clm]

    return encrypted


def decrypt():
    # Exemplo de entrada
    # VALLEACNDMMAOEAORFSNSOITAASNAXTUASX
    print("\nInforme o parâmetro - Número de colunas:")
    param = int(input())

    print("\nInforme o texto encriptado:")
    encrypted_text = input().strip()

    matrix = create_matrix_from_encrypted(encrypted_text, param)

    decrypted = decrypt_matrix(matrix)

    print("\nTexto Descriptografado:", decrypted)
    print()


def decrypt_matrix(matrix: list[list[str]]) -> str:
    decrypted = ""
    for row in matrix:
        for elm in row:
            decrypted += elm

    return decrypted


def create_matrix_from_encrypted(encrypted_text: str, param: int) -> list[list[str]]:
    rows = math.ceil(len(encrypted_text) / param)

    matrix: list[list[str]] = [["" for _ in range(param)] for _ in range(rows)]

    index = 0
    for clm in range(param):
        for row in range(rows):
            matrix[row][clm] = encrypted_text[index]
            index += 1
    return matrix


if __name__ == "__main__":
    main()
