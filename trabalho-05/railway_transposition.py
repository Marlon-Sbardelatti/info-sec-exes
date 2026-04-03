from typing import List

def sanitize_text(text: str) -> str:
  return text.replace(' ', '')

def zigzag_track_indexes(length: int, tracks_num: int) -> List[int]:
  indexes = []
  current_track = 0
  direction = 1  # 1 = Baixo, -1 = Cima

  for _ in range(length):
    indexes.append(current_track)

    if current_track == 0: # Primeiro trilho
      direction = 1
    elif current_track == tracks_num - 1: # Último trilho
      direction = -1

    current_track += direction

  return indexes


def build_tracks(text: str, tracks_num: int) -> List[List[str]]:
  cols = len(text)
  tracks = [[' ' for _ in range(cols)] for _ in range(tracks_num)]

  indexes = zigzag_track_indexes(cols, tracks_num)
  for col, (char, row) in enumerate(zip(text, indexes)):
    tracks[row][col] = char

  return tracks

def read_tracks_horizontally(tracks: List[List[str]]) -> str:
  result = []
  for track in tracks:
    for char in track:
      if char != ' ':
        result.append(char)
  return ''.join(result)


def encrypt(plain_text: str, tracks_num: int) -> str:
  sanitized = sanitize_text(plain_text)
  tracks = build_tracks(sanitized, tracks_num)
  return read_tracks_horizontally(tracks)


def decrypt(encrypted_text: str, tracks_num: int) -> str:
  sanitized = sanitize_text(encrypted_text)
  length = len(sanitized)

  indexes = zigzag_track_indexes(length, tracks_num)
  tracks = build_tracks('@' * length, tracks_num)

  char_pointer = 0
  for row in range(tracks_num):
    for col in range(length):
      if tracks[row][col] == '@':
        tracks[row][col] = sanitized[char_pointer]
        char_pointer += 1

  decrypted = ''
  for col, row in enumerate(indexes):
    decrypted += tracks[row][col]

  return decrypted


def main() -> None:
  operation = None

  while operation != 3:
    print('Transposição Ferroviária')
    print('[1] Criptografar')
    print('[2] Descriptografar')
    print('[3] Sair')

    operation = input('Escolha a opção: ')
    if not operation.isnumeric():
      print('Operação inválida.')
      continue

    operation = int(operation)

    match operation:
      case 1:
        tracks_num = int(input('Número de trilhos: '))
        plain_text = input('Texto claro: ')

        encrypted = encrypt(plain_text, tracks_num)
        print('Texto cifrado:', encrypted, '\n')

      case 2:
        tracks_num = int(input('Número de trilhos: '))
        encrypted_text = input('Texto cifrado: ')

        decrypted = decrypt(encrypted_text, tracks_num)
        print('Texto claro:', decrypted, '\n')

      case 3:
        break

      case _:
        print('Operação inválida.\n')
        
        
if __name__ == '__main__':
    main()