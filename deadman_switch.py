import os
import time
import threading
from pathlib import Path
from cryptography.fernet import Fernet


class DeadManSwitch:
    def __init__(self, target_file: Path | str, interval: int = 30):
        self.target_file = Path(target_file)
        self.interval = interval
        self.key = Fernet.generate_key()
        self.last_checkin = time.time()
        self.is_armed = False
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def time_remaining(self) -> float:
        if not self.is_armed:
            return 0.0
        return max(0.0, self.interval - (time.time() - self.last_checkin))

    def encrypt_file(self) -> Path:
        cipher = Fernet(self.key)
        raw_data = self.target_file.read_bytes()
        encrypted_data = cipher.encrypt(raw_data)
        self.target_file.write_bytes(encrypted_data)

        key_file = self.target_file.with_suffix(self.target_file.suffix + ".key")
        key_file.write_bytes(self.key)

        print(f"\n[!] SWITCH TRIGGERED: '{self.target_file.name}' has been encrypted!")
        print(f"[i] Recovery key saved to: '{key_file.name}'")
        return key_file

    @staticmethod
    def decrypt_file(file_path: Path | str, key: bytes | str) -> None:
        file_path = Path(file_path)
        if isinstance(key, str):
            key = key.encode("utf-8")
        cipher = Fernet(key)
        encrypted_data = file_path.read_bytes()
        decrypted_data = cipher.decrypt(encrypted_data)
        file_path.write_bytes(decrypted_data)
        print(f"[i] Successfully decrypted: '{file_path.name}'")

    def check_in(self) -> None:
        self.last_checkin = time.time()
        print(f"[+] Check-in recorded at {time.strftime('%H:%M:%S')}. Switch timer reset to {self.interval}s.")

    def arm(self) -> None:
        if not self.target_file.exists():
            raise FileNotFoundError(f"Target file does not exist: {self.target_file}")

        self.is_armed = True
        self.last_checkin = time.time()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()
        print(f"[*] CHECKMATE ARMED on '{self.target_file.name}' | Interval: {self.interval}s")

    def disarm(self) -> None:
        self.is_armed = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        print("[*] Switch disarmed safely.")

    def __enter__(self) -> "DeadManSwitch":
        self.arm()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disarm()

    def _monitor(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(0.5)
            elapsed = time.time() - self.last_checkin
            if elapsed >= self.interval:
                self.encrypt_file()
                self.is_armed = False
                print("[!] Emergency shutdown initiated by dead man switch.")
                os._exit(0)
