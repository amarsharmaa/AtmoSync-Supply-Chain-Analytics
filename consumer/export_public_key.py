from pathlib import Path
from getpass import getpass
from cryptography.hazmat.primitives import serialization

key_path = Path("consumer/snowflake_rsa_key.pem")

password = getpass("Enter private key password: ")

private_key = serialization.load_pem_private_key(
    key_path.read_bytes(),
    password=password.encode()
)
public_key_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

Path("consumer/snowflake_rsa_key.pub").write_bytes(public_key_pem)

print("Existing Private Key Loaded Successfully!")