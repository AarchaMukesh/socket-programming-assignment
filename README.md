# Socket Programming Assignment

This repository contains my implementation of the socket programming assignment.

## Contents

- `client.py` – Provided client program used for testing the servers.
- `server1.py` – Single-process server handling one client at a time.
- `server2.py` – Multi-process server using `fork()` to handle multiple clients.
- `server3.py` – Single-process server using `select()` to handle multiple clients.

## Supported Operations

The servers support arithmetic operations on two integer operands:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)

Example:

```text
10 + 20