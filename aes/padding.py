class Padding:
    @staticmethod
    def pad(block_size: int, blocks: list[bytes]) -> list[bytes]:
        last_block = blocks[-1]

        diff = block_size - len(last_block)
        if diff > 0:
            for i in range(1, diff):
                last_block[i * -1] = diff
        else:
            padding_block = bytes([block_size for _ in range(block_size)])
            blocks.append(padding_block)
        
        return blocks

    @staticmethod
    def unpad():
        pass