from algorithms.aes.shared.tables.sbox import S_BOX


class KeySchedule:
    def __init__(self):
        self.ROUND_KEY_SIZE = 4
        self.ROUND_CONSTANT_FIRST_BYTES = [
            0x01,
            0x02,
            0x04,
            0x08,
            0x10,
            0x20,
            0x40,
            0x80,
            0x1B,
            0x36,
        ]
        self.key_schedule = []

    def expand(self, key: bytes):
        normalized_key = self._normalize_key(key)

        round_key_0 = self._extract_words(normalized_key)
        self.key_schedule.extend(round_key_0)

        for round in range(1, 10):
            first_word = self.first_word(round)
            self.key_schedule.append(first_word)
            
            self.remaining_words()
            
        print(self.key_schedule)
        return self.key_schedule
            
    
    def first_word(self, round: int) -> bytes:
        previous_rk_start = (round - 1) * self.ROUND_KEY_SIZE
        
        first_word = self.key_schedule[previous_rk_start]
        last_word = self.key_schedule[previous_rk_start + self.ROUND_KEY_SIZE - 1]

        word = self._rot_word(last_word)
        word = self._sub_word(word)
        
        round_constant = self._round_constant(round)
        
        word = self._xor_words(word, round_constant)
        word = self._xor_words(word, first_word)

        return word
    
    def remaining_words(self):
        remaining_start = len(self.key_schedule)
        remaining_total = self.ROUND_KEY_SIZE - 1
        
        for i in range(remaining_start, remaining_start + remaining_total):
            previous_word = self.key_schedule[i - 1]
            index_last_word = self.key_schedule[i - self.ROUND_KEY_SIZE]
            
            word_i = self._xor_words(previous_word, index_last_word)
            self.key_schedule.append(word_i)

    def _rot_word(self, word: bytes) -> bytes:
        return word[1:] + word[:1]

    def _sub_word(self, word: bytes) -> bytes:
        sub_word = []

        for byte in word:
            row = byte >> 4
            col = byte & 0x0F

            new_byte = int(S_BOX[row][col], 16)
            sub_word.append(new_byte)

        return bytes(sub_word)

    def _round_constant(self, round: int) -> bytes:
        first = self.ROUND_CONSTANT_FIRST_BYTES[round - 1]
        return bytes([first, 0x00, 0x00, 0x00])
    
    def _xor_words(self, word1: bytes, word2: bytes) -> bytes:
        return bytes(a ^ b for a, b in zip(word1, word2))

    def _normalize_key(self, key: bytes) -> bytes:
        max_length = self.ROUND_KEY_SIZE**2
        return key[: max_length]

    def _extract_words(self, key: bytes) -> list[bytes]:
        skip = self.ROUND_KEY_SIZE
        words = []

        for i in range(0, len(key), skip):
            word = key[i : i + skip]
            words.append(word)

        return words