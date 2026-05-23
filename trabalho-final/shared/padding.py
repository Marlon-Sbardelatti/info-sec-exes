class Padding:
    def __init__(self, block_size: int):
        self.block_size = block_size


    def pad(self, data: bytes) -> bytes:
        diff = self.block_size - (len(data) % self.block_size)

        if diff == 0:
            diff = self.block_size

        padding = bytes([diff] * diff)
        return data + padding


    def unpad(self, data: bytes) -> bytes:
        padded_bytes = data[-1]

        if padded_bytes < 1 or padded_bytes > self.block_size:
            raise ValueError("Padding inválido.")

        expected = bytes([padded_bytes] * padded_bytes)

        if data[-padded_bytes:] != expected:
            raise ValueError("Padding inválido.")

        return data[:-padded_bytes]