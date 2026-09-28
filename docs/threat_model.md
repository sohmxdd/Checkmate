# Threat Model

## Assumptions

- The host machine running the switch is initially under authorized user control.
- Target files reside on accessible local storage.

## Attack Vectors & Defenses

1. User Inactivity / Absence:
   - Threat: User becomes incapacitated or unable to protect sensitive files.
   - Defense: Automated countdown activates encryption when check-in is missed.

2. Malicious Interception:
   - Threat: Unauthorized actor inspects unencrypted files on unattended system.
   - Defense: Switch seals files into encrypted ciphertext.

## Out of Scope

- Kernel-level memory scraping during live execution prior to encryption.
- Hostile hardware compromise while the process is active in RAM.
