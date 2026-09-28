# CHECKMATE

A local-first, software-based dead man switch.

## Overview

CHECKMATE provides an automated, local safety mechanism for safeguarding sensitive data. If regular check-ins are not maintained within a specified interval, the switch triggers defensive measures such as encrypting designated files.

## Core Concept

The switch operates on a simple principle:
1. Arm the switch with a target file and a timeout interval.
2. Regularly reset the countdown by checking in.
3. If a check-in is missed, the switch triggers automated protection immediately.
