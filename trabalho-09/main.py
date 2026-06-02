import os

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def save_key(key: bytes, path: str):
    with open(path, "wb") as f:
        f.write(key)


def encrypt_message(message: bytes, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_message_bytes(ciphertext: bytes, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_message(ciphertext: bytes, private_key):
    return decrypt_message_bytes(ciphertext, private_key).decode()


def encrypt_aes_file(key: bytes, input_path: str, output_path: str):
    nonce = os.urandom(12)
    with open(input_path, "rb") as f:
        plaintext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_path, "wb") as f:
        f.write(nonce)
        f.write(encryptor.tag)
        f.write(ciphertext)


def decrypt_aes_file(key: bytes, input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        nonce = f.read(12)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_path, "wb") as f:
        f.write(plaintext)


def save_keys(private_key, public_key, name: str):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    save_key(private_key_pem, f"{name}/keys/private_key.pem")
    save_key(public_key_pem, f"{name}/keys/public_key.pem")


def sign_file(private_key, file_path: str, signature_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    with open(signature_path, "wb") as f:
        f.write(signature)


def verify_file(public_key, file_path: str, signature_path: str) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()
    with open(signature_path, "rb") as f:
        signature = f.read()
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def first_question(priv_marlon, pub_marlon, priv_sofia, pub_sofia):
    msg_marlon = "Ola, Sofia! Aqui e o Marlon."
    encrypted_to_sofia = encrypt_message(msg_marlon.encode(), pub_sofia)
    save_key(encrypted_to_sofia, "sofia/01/mensagem_cifrada.bin")

    msg_sofia = "Ola, Marlon! Aqui e a Sofia."
    encrypted_to_marlon = encrypt_message(msg_sofia.encode(), pub_marlon)
    save_key(encrypted_to_marlon, "marlon/01/mensagem_cifrada.bin")

    decrypted_marlon = decrypt_message(encrypted_to_marlon, priv_marlon)
    print(f"Marlon decifrou a mensagem de Sofia: {decrypted_marlon}")

    decrypted_sofia = decrypt_message(encrypted_to_sofia, priv_sofia)
    print(f"Sofia decifrou a mensagem de Marlon: {decrypted_sofia}")


def second_question(public_key):
    with open("L09 - Chave assimétrica (novo).pdf", "rb") as f:
        pdf_data = f.read()

    print(f"Tamanho do PDF: {len(pdf_data)} bytes")

    try:
        encrypt_message(pdf_data, public_key)
    except ValueError as e:
        print(f"Erro ao cifrar: {e}")


def third_question(priv_marlon, pub_marlon, priv_sofia, pub_sofia):
    aes_key_marlon = os.urandom(32)
    encrypt_aes_file(aes_key_marlon, "tux-vs-windows.jpg", "sofia/03/img_cifrada.bin")
    encrypted_aes_key_marlon = encrypt_message(aes_key_marlon, pub_sofia)
    save_key(encrypted_aes_key_marlon, "sofia/03/chave_aes_cifrada.bin")

    aes_key_sofia = os.urandom(32)
    encrypt_aes_file(aes_key_sofia, "tux.png", "marlon/03/img_cifrada.bin")
    encrypted_aes_key_sofia = encrypt_message(aes_key_sofia, pub_marlon)
    save_key(encrypted_aes_key_sofia, "marlon/03/chave_aes_cifrada.bin")

    # Marlon decifra a imagem enviada por sofia
    aes_key_sofia_dec = decrypt_message_bytes(encrypted_aes_key_sofia, priv_marlon)
    decrypt_aes_file(
        aes_key_sofia_dec, "marlon/03/img_cifrada.bin", "marlon/03/img_decifrada.jpg"
    )

    # Sofia decifra a imagem enviada por marlon
    aes_key_marlon_dec = decrypt_message_bytes(encrypted_aes_key_marlon, priv_sofia)
    decrypt_aes_file(
        aes_key_marlon_dec, "sofia/03/img_cifrada.bin", "sofia/03/img_decifrada.png"
    )

    print("Imagens decifradas com sucesso!")


def fourth_question(priv_marlon, pub_marlon, priv_sofia, pub_sofia):
    sign_file(priv_marlon, "tux.png", "sofia/04/assinatura_marlon.bin")
    save_key(
        open("tux.png", "rb").read(), "sofia/04/tux.png"
    )  # serve apenas para copiar o arquivo para o diretório de destino, simulando um envio.

    sign_file(priv_sofia, "tux-vs-windows.jpg", "marlon/04/assinatura_sofia.bin")
    save_key(open("tux-vs-windows.jpg", "rb").read(), "marlon/04/tux-vs-windows.jpg")

    ok = verify_file(
        pub_sofia, "marlon/04/tux-vs-windows.jpg", "marlon/04/assinatura_sofia.bin"
    )
    print(f"Marlon: arquivo da Sofia autentico? {ok}")

    ok = verify_file(pub_marlon, "sofia/04/tux.png", "sofia/04/assinatura_marlon.bin")
    print(f"Sofia: arquivo do Marlon autentico? {ok}")


def main():
    private_key_marlon, public_key_marlon = generate_key()
    private_key_sofia, public_key_sofia = generate_key()

    save_keys(private_key_marlon, public_key_marlon, "marlon")
    save_keys(private_key_sofia, public_key_sofia, "sofia")

    print("Questão 01:")
    first_question(
        private_key_marlon, public_key_marlon, private_key_sofia, public_key_sofia
    )
    print()

    print("Questão 02:")
    second_question(public_key_marlon)
    print()

    print("Questão 03:")
    third_question(
        private_key_marlon, public_key_marlon, private_key_sofia, public_key_sofia
    )
    print()

    print("Questão 04:")
    fourth_question(
        private_key_marlon, public_key_marlon, private_key_sofia, public_key_sofia
    )


if __name__ == "__main__":
    main()
