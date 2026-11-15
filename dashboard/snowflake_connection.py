
from pathlib import Path
import os
import getpass

import snowflake.connector
from cryptography.hazmat.primitives import serialization


def get_snowflake_connection():
    key_path = (
        Path(__file__).resolve().parent.parent
        / "consumer"
        / "snowflake_rsa_key.pem"
    )

    password = os.getenv("SNOWFLAKE_KEY_PASSWORD")
    if password is None:
        password = getpass.getpass(
            "Enter private key password: "
        )

    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None
        )

    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return snowflake.connector.connect(
        account="RIJILNL-DA81513",
        user="AMARSHARMAF20@GMAIL.COM",
        private_key=private_key_der,
        warehouse="SNOWFLAKE_LEARNING_WH",
        database="ATMOSYNC_DB",
        schema="ANALYTICS"
    )
