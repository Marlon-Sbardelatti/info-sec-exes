from aes.tables.s_box import S_BOX
from aes.utils import extract_words, get_table_value_for, xor_words

class KeySchedule:
    def __init__(self, key: bytes):
        self.WORDS_PER_ROUND = 4
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
        self.words: list[bytes] = []
        self._calculate_params(key)

    def _calculate_params(self, key: bytes) -> None:
        key_size = len(key)

        match key_size:
            case 16:
                self.WORDS_PER_KEY = 4
                self.ROUNDS = 10
            case 24:
                self.WORDS_PER_KEY = 6
                self.ROUNDS = 12
            case 32:
                self.WORDS_PER_KEY = 8
                self.ROUNDS = 14

            case _:
                raise ValueError(
                    "Chave inválida. Extensões aceitas: 128, 192 ou 256 bits."
                )

        self.key = key

    def expand(self) -> list[bytes]:
        self.words = extract_words(self.key)

        total_words = self.WORDS_PER_ROUND * (self.ROUNDS + 1)

        round = 1

        while len(self.words) < total_words:
            first_word = self.first_word(round)
            self.words.append(first_word)

            self.remaining_words()

            round += 1

        return self.words

    def first_word(self, round: int) -> bytes:
        word_idx = len(self.words)
        last_word = self.words[-1]

        temp = self._rot_word(last_word)
        temp = self._sub_word(temp)

        round_constant = self._round_constant(round)
        temp = xor_words(temp, round_constant)

        previous = self._get_previous_word_from_same_index(word_idx)

        return xor_words(previous, temp)

    def remaining_words(self):
        remaining_total = self.WORDS_PER_ROUND - 1

        for _ in range(remaining_total):
            word_idx = len(self.words)
            last_word = self.words[-1]

            # Etapa específica para chave de 256 bits
            if self.WORDS_PER_KEY > 6 and word_idx % self.WORDS_PER_KEY == 4:
                last_word = self._sub_word(last_word)

            previous = self._get_previous_word_from_same_index(word_idx)
            word = xor_words(previous, last_word)

            self.words.append(word)

    def _rot_word(self, word: bytes) -> bytes:
        return word[1:] + word[:1]

    def _sub_word(self, word: bytes) -> bytes:
        return [
            get_table_value_for(byte, S_BOX)
            for byte in word
        ]

    def _round_constant(self, round: int) -> bytes:
        first = self.ROUND_CONSTANT_FIRST_BYTES[round - 1]
        return bytes([first, 0x00, 0x00, 0x00])
    
    def _get_previous_word_from_same_index(self, index: int) -> bytes:
        return self.words[index - self.WORDS_PER_KEY]
        
