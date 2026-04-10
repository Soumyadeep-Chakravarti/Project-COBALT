# Rust Guardian (L04)

**Role:** Integrity & Safety  
**Layer:** L04 - Guardian  
**Status:** PLANNED

The paranoid core. Verifies SHA-256 hashes on all buffers before specialists can touch them.

## Responsibilities
- Binary integrity validation
- Memory-safe system daemons
- Pre-execution buffer verification

## Interface
Consumes shared memory segments from Nexus via UDS. Outputs verification result to Foundation (L02).
