from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
from pathlib import Path

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(
        __import__("getpass").getpass("Key password: ").encode()
    )
)

Path("consumer/snowflake_rsa_key.pem").write_bytes(private_key_pem)
public_key_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

Path("consumer/snowflake_rsa_key.pub").write_bytes(public_key_pem)

print("RSA Key Generated Successfully!")