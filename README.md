# CHECKMATE

A local-first, software-based dead man switch.

## Overview

CHECKMATE provides an automated, local safety mechanism for safeguarding sensitive data. If regular check-ins are not maintained within a specified interval, the switch triggers defensive measures such as encrypting designated files.

## Core Concept

The switch operates on a simple principle:
1. Arm the switch with a target file and a timeout interval.
2. Regularly reset the countdown by checking in.
3. If a check-in is missed, the switch triggers automated protection immediately.

## Switch Lifecycle

- UNARMED: Switch is idle and no background monitoring is active.
- ARMED: Background monitor tracks elapsed time since last check-in.
- RESET: A valid check-in restarts the interval timer.
- TRIGGERED: Timer expired; target file encryption executes.
- DISARMED: Switch is halted safely by the user.

## Configuration Options

| Parameter   | Type | Default | Description |
| ----------- | ---- | ------- | ----------- |
| target_file | Path | (req)   | File path to protect upon switch trigger |
| interval    | int  | 30      | Maximum seconds between check-ins |

## Installation

### Prerequisites
- Python 3.10 or newer

### Setup
Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/sohmxdd/Checkmate.git
cd Checkmate
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

### 1. Interactive CLI Mode

Launch the interactive console check-in loop directly:

```bash
# Run with default 30-second interval (prompts for target file)
python deadman_switch.py

# Or specify target file and interval
python deadman_switch.py secret.txt -i 60
```

Once armed, the interactive prompt lets you reset the countdown or inspect switch status:

```text
[58s left] checkmate> c
[+] Check-in recorded at 14:22:05. Switch timer reset to 60s.

[59s left] checkmate> s
[i] Status: ARMED | Time remaining: 57.4s | Interval: 60s

[55s left] checkmate> d
[*] Switch disarmed safely.
```

#### CLI Interactive Commands

| Command | Alias | Description |
| ------- | ----- | ----------- |
| `[Enter]` | `c`, `checkin` | Reset switch timer back to full interval |
| `s` | `status` | Query active status and exact remaining seconds |
| `d` | `q`, `disarm`, `quit` | Safely disarm the switch and terminate the session |
| `h` | `help` | Print list of available interactive commands |

#### CLI Flags & Options

```text
usage: deadman_switch.py [-h] [-i INTERVAL] [--decrypt ENCRYPTED_FILE]
                         [--key KEY_FILE_OR_STRING] [target]

positional arguments:
  target                Path to target file to protect

options:
  -h, --help            Show this help message and exit
  -i, --interval INTERVAL
                        Check-in timeout interval in seconds (default: 30)
  --decrypt ENCRYPTED_FILE
                        Decrypt a previously triggered target file
  --key KEY_FILE_OR_STRING
                        Key file path or raw Fernet key string for decryption
```

### 2. Programmatic Python API

#### Manual Arming & Disarming

```python
from pathlib import Path
from deadman_switch import DeadManSwitch

switch = DeadManSwitch(target_file=Path("secret.txt"), interval=30)
switch.arm()
switch.check_in()
print(f"Remaining: {switch.time_remaining:.1f}s")
switch.disarm()
```

#### Context Manager Pattern (`with` statement)

`DeadManSwitch` supports the context management protocol. Entering the context automatically arms the switch, and exiting automatically and safely disarms it—even if unexpected exceptions arise:

```python
from pathlib import Path
from deadman_switch import DeadManSwitch

with DeadManSwitch(target_file=Path("secret.txt"), interval=45) as switch:
    # Perform sensitive operational tasks
    switch.check_in()
# Automatically disarmed upon exiting the block
```

## Recovery & Decryption

During prototype testing, the encryption key is preserved alongside the target file as `<filename>.key`.

### Via CLI

```bash
# Automatically finds secret.txt.key adjacent to target file:
python deadman_switch.py --decrypt secret.txt

# Or provide explicit key file or key string:
python deadman_switch.py --decrypt secret.txt --key secret.txt.key
```

### Via Python API

To restore an encrypted file programmatically:

```python
from pathlib import Path
from deadman_switch import DeadManSwitch

target = Path("secret.txt")
key = Path("secret.txt.key").read_bytes()
DeadManSwitch.decrypt_file(target, key)
```

## Documentation & Roadmap

- Architecture: docs/architecture.md
- Threat Model: docs/threat_model.md
- Roadmap: ROADMAP.md
- Changelog: CHANGELOG.md
- Security Policy: SECURITY.md
- Contributing: CONTRIBUTING.md

## License

This project is licensed under the MIT License - see the LICENSE file for details.
