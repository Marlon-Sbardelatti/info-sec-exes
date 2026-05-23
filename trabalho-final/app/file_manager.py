class FileManager:
    @staticmethod
    def read_bytes(path: str) -> bytes:
        with open(path, "rb") as file:
            return file.read()

    @staticmethod
    def write_bytes(path: str, data: bytes):
        with open(path, "wb") as file:
            file.write(data)
