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
