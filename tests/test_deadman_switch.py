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
