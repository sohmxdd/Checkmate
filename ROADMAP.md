# CHECKMATE Development Roadmap

## Phase 1: Prototype (Completed)
- [x] Single-script in-process monitoring.
- [x] Symmetric AES-128 (Fernet) file encryption.
- [x] Interactive console check-in loop (`run_cli`).
- [x] Emergency key retention (`<filename>.key`).
- [x] Context manager protocol (`__enter__` / `__exit__`) support.
- [x] Dynamic `time_remaining` property inspection.
- [x] CLI `--decrypt` recovery workflow with automatic key discovery.
- [x] Automated pytest test suite covering switch lifecycle, cryptography, and context management.

## Phase 2: System Integration (Next)
- Background daemon / service support for Windows and Linux.
- System tray status indicator and notification prompts.
- Configurable notification threshold before switch triggers.

## Phase 3: Advanced Cryptography & Distribution
- Multi-file vault encryption.
- Shamir Secret Sharing (SSS) key split distribution.
- Remote check-in via secure authenticated webhook or local HTTP endpoint.
- Secure key destruction / zeroization upon timeout.
