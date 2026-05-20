from typing import TypeAlias

from aes.tables.inverse_s_box import INVERSE_S_BOX
from aes.tables.s_box import S_BOX
from aes.tables.e_table import E_TABLE
from aes.tables.l_table import L_TABLE
from aes.tables.m_matrix import M_MATRIX
from aes.tables.inverse_m_matrix import INVERSE_M_MATRIX
from aes.key_schedule import KeySchedule
from aes.utils import get_table_value_for, xor

State: TypeAlias = list[list[int]]

class AES:
    def __init__(self, key: bytes):
        self.BLOCK_SIZE = 16
        self.key_schedule = self._expand_key(key)
        self.rounds = len(self.key_schedule) // 4

    def encrypt(self, plaintext: bytes) -> bytes:
        state = self._bytes_to_state(plaintext)

        round_0 = self._get_round_key(0)
        state = self._add_round_key(state, round_0)

        for round in range(1, self.rounds - 1):
            state = self._sub_bytes(state)

            state = self._shift_rows(state)
            
            state = self._mix_columns(state)

            round_key = self._get_round_key(round)
            state = self._add_round_key(state, round_key)
            
        state = self._sub_bytes(state)

        state = self._shift_rows(state)
        
        round_n = self._get_round_key(self.rounds - 1)
        state = self._add_round_key(state, round_n)

        return self._state_to_bytes(state)

    def decrypt(self, cipher: bytes) -> bytes:
        state = self._bytes_to_state(cipher)

        round_n = self._get_round_key(self.rounds - 1)
        state = self._add_round_key(state, round_n)

        state = self._shift_rows(state, inverse=True)

        state = self._sub_bytes(state, inverse=True)

        for round in range(self.rounds - 2, 0, -1):
            round_key = self._get_round_key(round)
            state = self._add_round_key(state, round_key)

            state = self._mix_columns(state, inverse=True)

            state = self._shift_rows(state, inverse=True)
        
            state = self._sub_bytes(state, inverse=True)

        round_0 = self._get_round_key(0)
        state = self._add_round_key(state, round_0)

        return self._state_to_bytes(state)

    def _mix_columns(self, state: State, inverse: bool = False) -> State:
        result = self._empty_state()

        m_matrix = INVERSE_M_MATRIX if inverse else M_MATRIX

        for col in range(4):
            for row in range(4):
                col_from_state = [state[i][col] for i in range(4)]
                row_from_matrix = [m_matrix[row][i] for i in range(4)]
                
                factors = [self._galois_product(a, b) for a, b in zip(col_from_state, row_from_matrix)]
                
                byte = 0x00
                for f in factors:
                    byte = xor(byte, f)

                result[row][col] = byte

        return result

    def _galois_product(self, a: int, b: int) -> int:
        if 0 in (a, b):
            return 0
        if a == 1:
            return b
        if b == 1:
            return a
        
        a = get_table_value_for(a, L_TABLE)
        b = get_table_value_for(b, L_TABLE)

        result = a + b
        if result > 0xFF:
            result %= 0xFF
        
        return get_table_value_for(result, E_TABLE)
        
    def _shift_rows(self, state: State, inverse: bool = False) -> State:
        result = self._empty_state()

        for row in range(4):
            shift = row
            if inverse:
                shift = -shift

            result[row] = state[row][shift:] + state[row][:shift]

        return result

    def _add_round_key(self, state: State, round_key: State) -> State:
        result = self._empty_state()

        for col in range(4):
            for row in range(4):
                result[row][col] = xor(state[row][col], round_key[row][col])

        return result

    def _sub_bytes(self, state: State, inverse: bool = False) -> State:
        result = self._empty_state()

        table = INVERSE_S_BOX if inverse else S_BOX
        for col in range(4):
            for row in range(4):
                result[row][col] = get_table_value_for(state[row][col], table)

        return result

    def _get_round_key(self, round: int) -> State:
        start = round * 4
        round_key = b"".join(
            self.key_schedule[start:start + 4]
        )
        return self._bytes_to_state(round_key)

    def _expand_key(self, key: bytes) -> None:
        schedule = KeySchedule(key)
        return schedule.expand()

    def _bytes_to_state(self, block: bytes) -> State:
        state = self._empty_state()

        for i, byte in enumerate(block):
            row = i % 4
            col = i // 4
            state[row][col] = byte

        return state

    def _state_to_bytes(self, state: State) -> bytes:
        output = []

        for col in range(4):
            for row in range(4):
                output.append(state[row][col])

        return bytes(output)

    def _empty_state(self) -> State:
        return [[0] * 4 for _ in range(4)]
