import time
from pathlib import Path
import pytest
from deadman_switch import DeadManSwitch


def test_switch_initialization(tmp_path: Path):
    target = tmp_path / "secret.txt"
    target.write_text("classified data")

    switch = DeadManSwitch(target_file=target, interval=45)
    assert switch.target_file == target
    assert switch.interval == 45
    assert not switch.is_armed
    assert switch.time_remaining == 0.0
    assert switch.key is not None


def test_arm_raises_file_not_found(tmp_path: Path):
    non_existent = tmp_path / "missing.txt"
    switch = DeadManSwitch(target_file=non_existent, interval=10)

    with pytest.raises(FileNotFoundError, match="Target file does not exist"):
        switch.arm()


def test_arm_and_disarm_lifecycle(tmp_path: Path):
    target = tmp_path / "secret.txt"
    target.write_text("classified data")

    switch = DeadManSwitch(target_file=target, interval=30)
    assert not switch.is_armed

    switch.arm()
    assert switch.is_armed
    assert switch.time_remaining > 0.0

    switch.disarm()
    assert not switch.is_armed
    assert switch.time_remaining == 0.0


def test_check_in_resets_timer(tmp_path: Path):
    target = tmp_path / "secret.txt"
    target.write_text("classified data")

    switch = DeadManSwitch(target_file=target, interval=20)
    switch.arm()
    try:
        initial_checkin = switch.last_checkin
        time.sleep(0.1)
        switch.check_in()
        assert switch.last_checkin > initial_checkin
        assert switch.time_remaining <= 20.0
    finally:
        switch.disarm()


def test_encryption_and_key_retention(tmp_path: Path):
    target = tmp_path / "data.txt"
    original_content = "TOP SECRET BLUEPRINT 42"
    target.write_text(original_content, encoding="utf-8")

    switch = DeadManSwitch(target_file=target, interval=30)
    key_file = switch.encrypt_file()

    assert key_file.exists()
    assert key_file == target.with_suffix(".txt.key")
    assert key_file.read_bytes() == switch.key

    encrypted_content = target.read_bytes()
    assert encrypted_content != original_content.encode("utf-8")

    # Verify decryption with bytes key
    DeadManSwitch.decrypt_file(target, key_file.read_bytes())
    assert target.read_text(encoding="utf-8") == original_content


def test_decryption_with_string_key(tmp_path: Path):
    target = tmp_path / "notes.txt"
    original_content = "CONFIDENTIAL NOTES"
    target.write_text(original_content, encoding="utf-8")

    switch = DeadManSwitch(target_file=target, interval=30)
    key_file = switch.encrypt_file()

    key_str = key_file.read_bytes().decode("utf-8")
    DeadManSwitch.decrypt_file(target, key_str)
    assert target.read_text(encoding="utf-8") == original_content


def test_decryption_with_invalid_key_fails(tmp_path: Path):
    from cryptography.fernet import InvalidToken, Fernet

    target = tmp_path / "secure.txt"
    target.write_text("SENSITIVE", encoding="utf-8")

    switch = DeadManSwitch(target_file=target, interval=30)
    switch.encrypt_file()

    wrong_key = Fernet.generate_key()
    with pytest.raises(InvalidToken):
        DeadManSwitch.decrypt_file(target, wrong_key)


def test_context_manager_arms_and_disarms(tmp_path: Path):
    target = tmp_path / "cm_test.txt"
    target.write_text("context manager payload")

    with DeadManSwitch(target_file=target, interval=30) as switch:
        assert switch.is_armed
        assert switch.time_remaining > 0

    assert not switch.is_armed


def test_context_manager_disarms_on_exception(tmp_path: Path):
    target = tmp_path / "cm_error_test.txt"
    target.write_text("context manager payload")

    switch_ref = None
    with pytest.raises(RuntimeError, match="Intentional failure"):
        with DeadManSwitch(target_file=target, interval=30) as switch:
            switch_ref = switch
            assert switch.is_armed
            raise RuntimeError("Intentional failure")

    assert switch_ref is not None
    assert not switch_ref.is_armed


def test_cli_decrypt_workflow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import sys
    from deadman_switch import run_cli

    target = tmp_path / "cli_encrypted.txt"
    target.write_text("CONFIDENTIAL PAYLOAD", encoding="utf-8")

    switch = DeadManSwitch(target_file=target, interval=30)
    key_file = switch.encrypt_file()
    assert target.read_bytes() != b"CONFIDENTIAL PAYLOAD"

    # Test running CLI decrypt command
    monkeypatch.setattr(
        sys,
        "argv",
        ["deadman_switch.py", "--decrypt", str(target), "--key", str(key_file)],
    )
    run_cli()

    assert target.read_text(encoding="utf-8") == "CONFIDENTIAL PAYLOAD"


