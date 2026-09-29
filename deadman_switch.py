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


def run_cli() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="CHECKMATE - Local-First Dead Man's Switch CLI"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Path to the target file to protect",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=30,
        help="Check-in timeout interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--decrypt",
        metavar="ENCRYPTED_FILE",
        help="Decrypt a previously triggered target file",
    )
    parser.add_argument(
        "--key",
        metavar="KEY_FILE_OR_STRING",
        help="Key file path or raw Fernet key string for decryption",
    )

    args = parser.parse_args()

    # Handle decryption workflow
    if args.decrypt:
        target_path = Path(args.decrypt)
        if not target_path.exists():
            print(f"[!] Error: File '{target_path}' not found.", file=sys.stderr)
            sys.exit(1)

        key_bytes: bytes
        if args.key:
            potential_key_file = Path(args.key)
            if potential_key_file.exists():
                key_bytes = potential_key_file.read_bytes().strip()
            else:
                key_bytes = args.key.encode("utf-8").strip()
        else:
            default_key_path = target_path.with_suffix(target_path.suffix + ".key")
            if default_key_path.exists():
                print(f"[i] Using auto-detected key file: '{default_key_path.name}'")
                key_bytes = default_key_path.read_bytes().strip()
            else:
                print(
                    f"[!] Error: Recovery key not provided and '{default_key_path.name}' not found.",
                    file=sys.stderr,
                )
                sys.exit(1)

        try:
            DeadManSwitch.decrypt_file(target_path, key_bytes)
        except Exception as e:
            print(f"[!] Decryption failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Handle dead man switch monitoring workflow
    target_input = args.target
    if not target_input:
        try:
            target_input = input("Enter target file path to protect [secret.txt]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)
        if not target_input:
            target_input = "secret.txt"

    target_path = Path(target_input)
    if not target_path.exists():
        try:
            create_choice = input(
                f"File '{target_path}' does not exist. Create sample file for testing? [Y/n]: "
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)

        if create_choice in ("", "y", "yes"):
            target_path.write_text("CONFIDENTIAL: Checkmate Dead Man Switch test payload.\n", encoding="utf-8")
            print(f"[+] Created sample file: '{target_path.resolve()}'")
        else:
            print(f"[!] Error: Target file '{target_path}' does not exist.", file=sys.stderr)
            sys.exit(1)

    switch = DeadManSwitch(target_file=target_path, interval=args.interval)

    print("\n" + "=" * 60)
    print("                 CHECKMATE DEAD MAN SWITCH")
    print("=" * 60)
    print(f" Target file : {target_path.resolve()}")
    print(f" Interval    : {args.interval} seconds")
    print("-" * 60)
    print(" Commands:")
    print("   [Enter] or 'c' : Check in (reset timer)")
    print("   's'            : Show status & remaining time")
    print("   'd' or 'q'     : Disarm and safely exit")
    print("   'h'            : Show commands help")
    print("=" * 60 + "\n")

    switch.arm()

    try:
        while switch.is_armed:
            prompt = f"[{int(switch.time_remaining)}s left] checkmate> "
            cmd = input(prompt).strip().lower()
            if cmd in ("", "c", "checkin", "check-in"):
                switch.check_in()
            elif cmd in ("s", "status"):
                remaining = switch.time_remaining
                print(
                    f"[i] Status: {'ARMED' if switch.is_armed else 'DISARMED'} | "
                    f"Time remaining: {remaining:.1f}s | "
                    f"Interval: {switch.interval}s"
                )
            elif cmd in ("d", "disarm", "q", "quit", "exit"):
                switch.disarm()
                break
            elif cmd in ("h", "help"):
                print("Available commands:")
                print("  [Enter], c, checkin : Reset switch timer")
                print("  s, status           : Display remaining time")
                print("  d, disarm, q, quit  : Safely disarm and exit")
                print("  h, help             : Show this message")
            else:
                print(f"[?] Unknown command: '{cmd}'. Press Enter to check in, or 'h' for help.")
    except (KeyboardInterrupt, EOFError):
        print("\n[*] Interrupted by user.")
        if switch.is_armed:
            switch.disarm()


if __name__ == "__main__":
    run_cli()
