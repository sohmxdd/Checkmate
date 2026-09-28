# Architecture Overview

CHECKMATE is designed with a local-first philosophy, prioritizing simplicity, auditability, and deterministic behavior.

## Core Components

1. Switch Engine (DeadManSwitch):
   Maintains state (armed, disarmed, last_checkin, interval).

2. Background Monitor Thread:
   Monitors elapsed time without blocking terminal input or main loop execution.

3. Cryptographic Subsystem:
   Uses authenticated symmetric encryption (Fernet) to secure target files upon trigger.

## Threading Model

- Main Thread: Handles user commands, terminal input, and signaling.
- Daemon Thread: Executes regular time difference checks (time.time() - last_checkin).
- Exit Synchronization: Uses threading.Event for clean shutdown and atomic triggers.
