from app.constants import KEY_SIZE, IV_SIZE
from app.types import OperationOption, ModeOption

class InputHandler:
    @staticmethod
    def request_operation() -> OperationOption:
        while True:
            print("\nSelecione a operação:")
            print("[1] Cifrar")
            print("[2] Decifrar")

            option = input("Opção: ").strip()

            if option == "1":
                return "encrypt"

            if option == "2":
                return "decrypt"

            print("\nOperação inválida.")

    @staticmethod
    def request_mode() -> ModeOption:
        while True:
            print("\nSelecione o modo:")
            print("[1] ECB")
            print("]2] CBC")

            option = input("Opção: ").strip()

            if option == "1":
                return "ECB"

            if option == "2":
                return "CBC"

            print("\nModo inválido.")

    @staticmethod
    def request_input_file() -> str:
        while True:
            path = input("\nArquivo de entrada: ").strip()

            if path:
                return path

            print("\nCaminho inválido.")

    @staticmethod
    def request_output_file() -> str:
        while True:
            path = input("Arquivo de saída: ").strip()

            if path:
                return path

            print("\nCaminho inválido.")

    @staticmethod
    def request_key() -> bytes:
        return InputHandler._request_byte_sequence(
            "\nInforme a chave (16 bytes decimais separados por vírgula): ", KEY_SIZE
        )

    @staticmethod
    def request_iv() -> bytes:
        return InputHandler._request_byte_sequence(
            "\nInforme o IV (16 bytes decimais separados por vírgula): ", IV_SIZE
        )

    @staticmethod
    def _request_byte_sequence(message: str, expected_size: int) -> bytes:

        while True:
            try:
                raw = input(message)

                values = [int(value.strip()) for value in raw.split(",")]

                if len(values) != expected_size:
                    print(f"\nA sequência deve possuir {expected_size} valores.")
                    continue

                if any(value < 0 or value > 255 for value in values):
                    print("\nTodos os valores devem estar entre 0 e 255.")
                    continue

                return bytes(values)

            except ValueError:
                print("\nEntrada inválida. Use apenas números separados por vírgula.")
