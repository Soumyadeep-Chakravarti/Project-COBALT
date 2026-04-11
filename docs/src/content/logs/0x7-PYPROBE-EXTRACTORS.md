---
title: "Log 0x07: PyProbe — Full Type Support and Infrastructure"
date: 2026-03-27
categories: ["Engineering", "PyProbe"]
tags: ["python", "cpython", "type-extractors", "cycle-detection", "ci"]
mermaid: false
---

# [ COBALT Engineering Log 0x05 ]
## PyProbe — Full Type Support and Infrastructure

*March 27, 2026. One month since PyProbe's birth. Time for the big push.*

---

## What's New

A lot. After a month of on-and-off work, PyProbe got serious upgrades:

**Commits:**
- [pyprobe - idea updated, mde docs folder for quick ref of others](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/37d94011aba2737b4f308489673c86e2e2874f3c)

And then the big one:
- [pyprobe - Add extended type extractors, CI workflow, and project infrastructure](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/b221eaf547c44d6d6fca2e92095ec47b75ad9452)

---

## Extended Type Extractors

X-Ray now supports the full CPython type matrix:

| Type | Support |
|------|---------|
| int | ✅ |
| float | ✅ |
| str | ✅ (multi-encoding: ASCII, Latin-1, UCS-2, UCS-4) |
| bytes | ✅ |
| list | ✅ |
| tuple | ✅ |
| dict | ✅ (with cycle detection) |
| set | ✅ |

**The big win:** Cycle detection.

Python objects can reference each other. Without cycle detection, X-Ray would recurse forever on circular references. Now it tracks visited objects and safely breaks cycles.

```python
# Self-referential structure - used to hang forever
x = {"self": None}
x["self"] = x

ptr = pyprobe.pin(x)
result = ptr.xray()  # Safely returns with cycle marker
```

---

## CI Workflow

PyProbe now has automated testing via GitHub Actions.

Every push runs:
- Unit tests for all type extractors
- Cycle detection tests
- Memory safety validation
- Python 3.12 and 3.13 compatibility checks

---

## Docs Folder

Added a proper documentation structure:

```
docs/
├── INDEX.md         # Home
├── ARCHITECTURE.md  # System design
├── CPYTHON_MEMORY.md # CPython internals reference
├── SAFETY_MODEL.md  # When mutation is safe
├── ROADMAP.md       # Phase timeline
└── CONTRIBUTING.md  # How to help
```

This started as a personal project. Now it's becoming something publishable.

---

## The Research Angle

PyProbe isn't just for Nexus. It's genuinely interesting from a CS perspective:

- **CPython internals** — How does 3.12+ dict layout differ from 3.11?
- **Memory overhead** — What's the real cost of a Python object?
- **Safety invariants** — When is mutation actually safe vs. when does it corrupt state?

I'm thinking about submitting this to arXiv and JOSS eventually.

---

## Status

PyProbe X-Ray: Complete  
Type extractors: Full coverage  
CI: Automated  
Documentation: Comprehensive  

**PyProbe is ready to be the foundation. Next: PyJX.**

---

*Previous: [Log 0x06: PyJX — The Python-Java Bridge](./0x06-PYJX-INIT.md)*  
*Next: [Log 0x08: Nexus Resurfaces](./0x08-NEXUS-RESURFACE.md)*