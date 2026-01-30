from cryptography.fernet import Fernet
import os
import json

# In a real app, this should be a secure key retrieved from a vault/env var
# DO NOT COMMIT THIS KEY IN PRODUCTION.
# For this prototype, we will generate/get from env.
KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())

cipher_suite = Fernet(KEY.encode())

def encrypt_data(data: dict) -> str:
    """Encrypts a dictionary and returns a base64 encoded string."""
    json_str = json.dumps(data)
    encrypted_bytes = cipher_suite.encrypt(json_str.encode())
    return encrypted_bytes.decode()

def decrypt_data(encrypted_str: str) -> dict:
    """Decrypts a base64 encoded string back to a dictionary."""
    if not encrypted_str:
        return {}
    decrypted_bytes = cipher_suite.decrypt(encrypted_str.encode())
    return json.loads(decrypted_bytes.decode())
