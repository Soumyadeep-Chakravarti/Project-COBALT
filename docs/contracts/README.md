# CIS - COBALT Interop Standard

**Version:** 0.1.0-draft  
**Status:** DRAFT

The CIS defines how layers communicate within the COBALT architecture.

## Transport Layer

| Channel | Protocol | Purpose |
|---------|----------|---------|
| Control Signals | Protobuf over Unix Domain Sockets | Layer-to-layer coordination |
| Data Payloads | Shared Memory (mmap) | Zero-copy data transfer |

## Core Messages (Proto Definition)

See: `cobalt_interop.proto`

## Memory Model

All shared memory is allocated by Nexus (L03) via Java 25's `Arena.ofShared()` and mapped by specialists using their native FFI bindings.

## Lifecycle

1. Nexus allocates buffer via `Arena.ofShared()`
2. Memory address published via UDS to target specialist
3. Specialist maps pointer into its address space
4. Zero-copy read/write
5. Nexus deallocates on execution complete

---

*This document is the source of truth for inter-layer contracts.*
