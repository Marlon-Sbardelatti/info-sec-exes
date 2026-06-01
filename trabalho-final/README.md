# AES - Advanced Encryption Standard

Implementação didática do AES em Python puro, sem dependências externas. Suporta os modos **ECB** e **CBC** com chaves de 128, 192 ou 256 bits.

## Funcionalidades

- **AES-128/192/256**: cifragem e decifragem seguindo o padrão FIPS-197
- **Modos de operação**: ECB (Electronic Codebook) e CBC (Cipher Block Chaining)
- **Padding PKCS#7**
- **Interface CLI interativa** em português para cifrar/decifrar arquivos
- **Zero dependências**: apenas biblioteca padrão do Python (3.10+)

**Obs**: Apesar da implementação com suporte aos três tamanhos de chave, a interface CLI suporta apenas chaves de 128 bits, por requisito do trabalho.

## Estrutura do Projeto

A estrutura do projeto foi pensada de forma modular, orientada a classes abstratas, de modo que fosse possível incluir mais algoritmos de criptografia e modos de operação no futuro.


```
.
├── main.py                    # Ponto de entrada
├── app/
│   ├── constants.py           # KEY_SIZE e IV_SIZE (16 bytes)
│   ├── types.py               # Type aliases (OperationOption, ModeOption)
│   ├── menu.py                # Orquestração do menu interativo
│   ├── input_handler.py       # Entrada de dados do usuário
│   └── file_manager.py        # Leitura e escrita de arquivos binários
└── crypto/
    ├── shared/
    │   ├── block_cipher.py    # Classe abstrata para cifras de bloco
    │   ├── padding.py         # PKCS#7 padding/unpadding
    │   └── utils.py           # XOR, extração de palavras, lookup em tabelas
    ├── modes/
    │   ├── operation_mode.py  # Classe abstrata para modos de operação
    │   ├── ecb_mode.py        # Modo ECB
    │   └── cbc_mode.py        # Modo CBC
    └── aes/
        ├── aes.py             # Implementação do AES 
        ├── key_schedule.py    # Expansão da chave (suporte a 128/192/256 bits)
        └── tables/
            ├── s_box.py       # S-BOX 16x16
            ├── inverse_s_box.py
            ├── e_table.py     # Tabela E para multiplicação em Galois
            ├── l_table.py     # Tabela L para multiplicação em Galois
            ├── m_matrix.py    # Matriz de MixColumns
            └── inverse_m_matrix.py
```

## Como Executar

```bash
python3 main.py
```

O programa solicitará interativamente:

1. **Operação**: Cifrar (1) ou Decifrar (2)
2. **Modo**: ECB (1) ou CBC (2)
3. **Arquivo de entrada**: caminho para o arquivo a ser processado
4. **Arquivo de saída**: caminho para salvar o resultado
5. **Chave**: 16 bytes decimais separados por vírgula (ex: `1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16`)
6. **IV** (apenas CBC): 16 bytes decimais separados por vírgula

### Exemplo

```
Selecione a operação:
[1] Cifrar
[2] Decifrar
Opção: 1

Selecione o modo:
[1] ECB
[2] CBC
Opção: 2

Arquivo de entrada: documento.pdf
Arquivo de saída: documento.pdf.cifrado

Informe a chave (16 bytes decimais separados por vírgula): 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16

Informe o IV (16 bytes decimais separados por vírgula): 16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1

Arquivo cifrado com sucesso!
```

## Arquitetura

O projeto segue uma arquitetura baseada em classes abstratas:

- `BlockCipher`: interface genérica para cifras de bloco (implementada por `AES`)
- `OperationMode`: interface genérica para modos de operação (implementada por `ECBMode` e `CBCMode`)
- `AES` gerencia o estado interno como uma matriz 4×4 (matriz de estado) e executa as transformações:
  - `SubBytes` / `InvSubBytes`: substituição via S-BOX
  - `ShiftRows` / `InvShiftRows`: deslocamento circular das linhas
  - `MixColumns` / `InvMixColumns`: multiplicação em Galois usando tabelas E/L
  - `AddRoundKey`: XOR com a chave da rodada

A multiplicação em **Galois** é feita via tabelas de logaritmo discreto (`L_TABLE` e `E_TABLE`).