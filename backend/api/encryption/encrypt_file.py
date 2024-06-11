import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEYS_DIR = 'api/keys'
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, 'public_key.pem')
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, 'private_key.pem')

def generate_keys():
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        with open(PRIVATE_KEY_PATH, 'wb') as private_key_file:
            private_key_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        with open(PUBLIC_KEY_PATH, 'wb') as public_key_file:
            public_key_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

def load_public_key():
    with open(PUBLIC_KEY_PATH, 'rb') as key_file:
        return serialization.load_pem_public_key(key_file.read())

def load_private_key():
    with open(PRIVATE_KEY_PATH, 'rb') as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

def generate_symmetric_key():
    return os.urandom(32)

def encrypt_file(file_data):
    public_key = load_public_key()
    symmetric_key = generate_symmetric_key()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_file_data = encryptor.update(file_data) + encryptor.finalize()

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_file_data, encrypted_symmetric_key, iv

def decrypt_file(encrypted_file_data, encrypted_symmetric_key, iv):
    private_key = load_private_key()
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_file_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

    return decrypted_file_data
