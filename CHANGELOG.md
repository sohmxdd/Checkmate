# Changelog

All notable changes to CHECKMATE will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- Core DeadManSwitch class with arm, disarm, and check-in methods.
- In-memory key generation using cryptography.fernet.
- Automated target file encryption upon timeout expiration.
- Emergency key preservation to adjacent .key file.
- Decryption restoration helper.
