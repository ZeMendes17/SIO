from cryptography.hazmat.primitives.asymmetric import rsa
import cryptography
import sys

# prgram to generate a RSA key pair, with a length defined by the user (1024, 2048, 3072 or 4096)


# generate a private key
def generate_private_key(key_length):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_length,
    )
    return private_key

def generate_public_key(private_key):
    public_key = private_key.public_key()
    return public_key

def main():
    # args: public_file private_file key_length
    public_file = sys.argv[1]
    private_file = sys.argv[2]
    key_length = int(sys.argv[3])

    # generate the private key
    private_key = generate_private_key(key_length)

    # generate the public key
    public_key = generate_public_key(private_key)

    # write the keys to the files
    with open(public_file, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
            format=cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

    with open(private_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
            format=cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
            encryption_algorithm=cryptography.hazmat.primitives.serialization.NoEncryption(),
        ))



if __name__ == "__main__":
    main()