# CHECKMATE Development Roadmap

## Phase 1: Prototype (Current)
- Single-script in-process monitoring.
- Symmetric AES-128 (Fernet) file encryption.
- Interactive console check-in loop.
- Emergency key retention.

## Phase 2: System Integration
- Background daemon / service support for Windows and Linux.
- System tray status indicator and notification prompts.
- Configurable notification threshold before switch triggers.

## Phase 3: Advanced Cryptography & Distribution
- Multi-file vault encryption.
- Shamir Secret Sharing (SSS) key split distribution.
- Remote check-in via secure authenticated webhook or local HTTP endpoint.
- Secure key destruction / zeroization upon timeout.
