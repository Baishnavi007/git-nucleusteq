"""
Utility functions for decrypting passwords
received from the frontend using the RSA private key.
"""

import base64

from cryptography.hazmat.primitives import (
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    padding
)

from app.exceptions.unauthorized_exception import (
    UnauthorizedException
)

from app.utils.loggers import (
    logger
)

# Location of the RSA private key.
PRIVATE_KEY_PATH = "app/keys/private_key.pem"

# Load the private key once during application startup.
with open(
        PRIVATE_KEY_PATH,
        "rb"
) as key_file:

    private_key = serialization.load_pem_private_key(

        key_file.read(),

        password=None

    )


def decrypt_password(
        encrypted_password: str
) -> str:
    """
    Decrypt the password received from the frontend
    using the RSA private key.
    """

    try:

        logger.info(
            "Starting password decryption."
        )

        decrypted_password = private_key.decrypt(

            base64.b64decode(
                encrypted_password
            ),

            padding.PKCS1v15()

        )

        logger.info(
            "Password decrypted successfully."
        )

        return decrypted_password.decode()

    except Exception as error:

        logger.exception(
            "Password decryption failed: %s",
            str(error)
        )

        raise UnauthorizedException(
            "Invalid encrypted password."
        )