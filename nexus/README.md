# Project Nexus (L03)

**Role:** Polyglot Bridge / Memory Arbiter  
**Layer:** L03 - The Interop Spine  
**Status:** PLANNED

The foundational pillar. Handles cross-language execution, FFI via Project Panama, and memory provisioning.

## Responsibilities
- FFI (Foreign Function Interface) via Java 25 FFM API
- Shared memory allocation via `Arena.ofShared()`
- UDS (Unix Domain Socket) server for control signals
- Process lifecycle management for all specialists

## Architecture
```
┌─────────────┐     UDS      ┌─────────────┐
│  Orchestrator│◄────────────►│   Nexus    │
│   (L06)      │   Protobuf   │  (L03)     │
└─────────────┘              └──────┬──────┘
                                     │ Shared Memory
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ Rust Guardian │          │  C Mechanic   │          │ Julia Scientist│
│    (L04)      │          │    (L01)      │          │   (L06)        │
└───────────────┘          └───────────────┘          └───────────────┘
```

## CIS Compliance
All inter-layer communication follows the COBALT Interop Standard (CIS):
- Control signals: Protobuf over Unix Domain Sockets
- Data payloads: Shared memory via Java 25 FFM API (Project Panama)
