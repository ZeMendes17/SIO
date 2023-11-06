import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def aes_encrypt():
    pass

def generate_key(size=32):
    return os.urandom(size)

def generate_iv(size=16):
    return os.urandom(size)

def sample_encrypt(message, key, iv, mode="CBC"):
    if mode == "CBC":
        mode = modes.CBC(iv)
    else:
        mode = modes.ECB()  

    cipher = Cipher(algorithms.AES(key), mode)

    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(message, "utf-8")) + encryptor.finalize()
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()

def main():
    print("Symmetric Encryption")
    print("####################")
    print()

    key = generate_key()
    iv = generate_iv()

    message = "a secret message123"

    print(sample_encrypt(message, key, iv).decode("utf-8"))
    print(sample_encrypt(message, key, iv, mode="ECB").decode("utf-8"))



if __name__ == "__main__":
    main()