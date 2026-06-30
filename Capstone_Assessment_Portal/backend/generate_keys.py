from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

KEYS_DIRECTORY = "app/keys"

os.makedirs(KEYS_DIRECTORY, exist_ok=True)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

with open(
    os.path.join(KEYS_DIRECTORY, "private_key.pem"),
    "wb"
) as private_file:

    private_file.write(

        private_key.private_bytes(

            encoding=serialization.Encoding.PEM,

            format=serialization.PrivateFormat.TraditionalOpenSSL,

            encryption_algorithm=serialization.NoEncryption()

        )

    )

with open(
    os.path.join(KEYS_DIRECTORY, "public_key.pem"),
    "wb"
) as public_file:

    public_file.write(

        public_key.public_bytes(

            encoding=serialization.Encoding.PEM,

            format=serialization.PublicFormat.SubjectPublicKeyInfo

        )

    )

print("RSA key pair generated successfully.")