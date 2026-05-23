from crypto.aes.aes import AES
from crypto.modes import ECBMode, CBCMode

from app.file_manager import FileManager
from app.input_handler import InputHandler
from app.types import OperationOption, ModeOption


class Menu:
    def __init__(self):
        self._aes = AES()

    def start(self):
        operation = InputHandler.request_operation()

        mode_name = InputHandler.request_mode()

        input_path = InputHandler.request_input_file()

        output_path = InputHandler.request_output_file()

        key = InputHandler.request_key()

        iv = None
        if mode_name == "CBC":
            iv = InputHandler.request_iv()

        try:
            data = FileManager.read_bytes(input_path)

        except FileNotFoundError:
            print("\nArquivo de entrada não encontrado.")
            return

        try:
            result = self._execute_operation(
                operation=operation, mode_name=mode_name, data=data, key=key, iv=iv
            )

            FileManager.write_bytes(output_path, result)

            if operation == "encrypt":
                print("\nArquivo cifrado com sucesso!")
            else:
                print("\nArquivo decifrado com sucesso!")

        except Exception as error:
            print(f"\nErro durante processamento: {error}")


    def _execute_operation(
        self,
        operation: OperationOption,
        mode_name: ModeOption,
        data: bytes,
        key: bytes,
        iv: bytes | None,
    ) -> bytes:
        # Cifragem
        if operation == "encrypt":
            if mode_name == "CBC":
                return CBCMode(self._aes).encrypt(data, key, iv)

            return ECBMode(self._aes).encrypt(data, key)

        # Decifragem
        if mode_name == "CBC":
            return CBCMode(self._aes).decrypt(data, key, iv)

        return ECBMode(self._aes).decrypt(data, key)
