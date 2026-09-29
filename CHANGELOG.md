# Changelog

All notable changes to CHECKMATE will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- Core `DeadManSwitch` class with `arm()`, `disarm()`, and `check_in()` methods.
- In-memory key generation using `cryptography.fernet`.
- Automated target file encryption upon timeout expiration.
- Emergency key preservation to adjacent `.key` file.
- Decryption restoration helper via `DeadManSwitch.decrypt_file()`.
- Interactive console check-in loop (`run_cli()`) with live remaining time countdown.
- Context manager protocol (`__enter__` and `__exit__`) for scoped execution and safe disarm.
- Dynamic `time_remaining` property calculation without modifying switch state.
- CLI argument parsing (`target`, `--interval`, `--decrypt`, `--key`) and sample file creation prompt.
- Console script entrypoint `checkmate` defined in `pyproject.toml`.
- Comprehensive automated test suite in `tests/test_deadman_switch.py`.
