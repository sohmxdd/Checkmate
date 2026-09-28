import time
import threading
from pathlib import Path
from cryptography.fernet import Fernet


def generate_key() -> bytes:
    
    return Fernet.generate_key()


def encrypt_file(file_path: Path, key: bytes) -> Path:
    
    cipher = Fernet(key)
    raw_data = file_path.read_bytes()
    encrypted_data = cipher.encrypt(raw_data)

    # Overwrite the target file with encrypted payload
    file_path.write_bytes(encrypted_data)

    # Save the key next to the file for recovery during testing
    key_file = file_path.with_suffix(file_path.suffix + ".key")
    key_file.write_bytes(key)

    print(f"\n[!] SWITCH TRIGGERED: '{file_path.name}' has been encrypted!")
    print(f"[i] Recovery key saved to: '{key_file.name}'")
    return key_file


def decrypt_file(file_path: Path, key: bytes) -> None:
    cipher = Fernet(key)
    encrypted_data = file_path.read_bytes()
    decrypted_data = cipher.decrypt(encrypted_data)
    file_path.write_bytes(decrypted_data)
    print(f"[i] Successfully decrypted: '{file_path.name}'")
