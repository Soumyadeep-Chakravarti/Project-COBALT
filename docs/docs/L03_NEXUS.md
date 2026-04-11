---
title: L03 - Nexus Architecture
layout: page
---

# L03: Nexus — The Polyglot Bridge

**Nexus** is the foundational pillar implemented in **Java 25**. While other layers handle the "thinking," Nexus handles the **mechanical reality** of cross-language execution.

---

## Purpose

Nexus serves as the **Spine** of the COBALT system:

1. **State Persistence** — Unlike ephemeral scripts, Nexus maintains a persistent JVM-based state machine that tracks the health of all external language processes.
2. **Environment Provisioning** — It dynamically generates the necessary environment variables, pathing, and dependency contexts required for a specialist to run without host pollution.
3. **The Common Tongue** — It acts as the primary orchestrator for **FFI (Foreign Function Interface)** and **Internal RPC**.
4. **Standalone Capability** — Designed as an independent library/service, allowing for polyglot interop even outside the full COBALT stack.

---

## Technology Stack

- **Language:** Java 25
- **API:** Project Panama (Foreign Function & Memory API)
- **Memory Model:** `Arena.ofShared()` for zero-copy cross-process communication

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    COBALT                           │
│                  (The Dream)                        │
└─────────────────────┬───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Nexus (Java 25)                        │
│  - FFI bridge via Project Panama                   │
│  - Memory allocation via Arena.ofShared()          │
│  - Process lifecycle management                     │
└──────────┬──────────────────────────┬───────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐    ┌─────────────────────────┐
│  PyJX (Python)      │    │  Rust Guardian (L04)   │
│  - PyProbe wrapper  │    │  (future)               │
│  - Stable pointers  │    │                         │
└─────────────────────┘    └─────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│           PyProbe (C/Python)                        │
│  - Memory pinning                                  │
│  - X-Ray introspection                             │
│  - Scalpel mutation (future)                       │
└─────────────────────────────────────────────────────┘
```

---

## Key APIs

### Memory Allocation

```java
try (Arena arena = Arena.ofShared()) {
    MemorySegment buffer = arena.allocate(1024);
    long address = buffer.address();
    
    // Send 'address' to Python, Rust, whatever
    // They read/write directly. Zero copy.
}
```

### Process Lifecycle

Nexus manages the complete lifecycle of external language processes:

- Spawning specialists with proper environment variables
- Monitoring health via heartbeat checks
- Graceful shutdown and cleanup

---

## Dependencies

```
PyProbe      → pins Python memory
    ↓
PyJX         → PyProbe wrapper + Java bridge
    ↓
Nexus        → uses PyJX for Python interop
    ↓
COBALT       → the orchestrator
```

---

## Status

- **Current:** Active development
- **Focus:** Java 25 Panama integration, PyJX bridge
- **Future:** Rust Guardian integration (L04)

---

*See also: [Engineering Logs](../_posts/2026-04-11-log-0x08-nexus-resurface.md)*