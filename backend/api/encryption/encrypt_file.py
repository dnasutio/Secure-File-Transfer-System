import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Where to save the keys
KEYS_DIR = "api/keys"
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")


# Generates the RSA keys
def generate_keys():
    # Make the directory for the keys if it does not exist already
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    # If no keys exist in the keys directory, then generate the keys
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Create the private key
        with open(PRIVATE_KEY_PATH, "wb") as private_key_file:
            private_key_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Create the public key
        with open(PUBLIC_KEY_PATH, "wb") as public_key_file:
            public_key_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)


# Generate AES key
def generate_symmetric_key():
    return os.urandom(32)


def encrypt_file(file_data):
    public_key = load_public_key()
    symmetric_key = generate_symmetric_key()
    iv = os.urandom(16)
    # Con: Corrupted data cannot be recovered as each ciphertext relies on the other to be decrypted https://onboardbase.com/blog/aes-encryption-decryption/
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    # Encrypt the file with the AES key
    encrypted_file_data = encryptor.update(file_data) + encryptor.finalize()

    # Encrypt the AES symmetric key with the RSA public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return encrypted_file_data, encrypted_symmetric_key, iv


def decrypt_file(encrypted_file_data, encrypted_symmetric_key, iv):
    private_key = load_private_key()
    # Decrypt the AES key with the RSA private key
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decrypt the file with the AES key
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_file_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

    return decrypted_file_data
