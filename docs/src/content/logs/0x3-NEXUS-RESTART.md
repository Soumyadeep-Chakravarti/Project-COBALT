---
title: "Log 0x03: The Pivot"
date: 2025-12-23
categories: ["Engineering", "Architecture"]
tags: ["nexus", "python", "pyprobe", "architecture"]
mermaid: false
---

# [ COBALT Engineering Log 0x02 ]
## The Pivot

*December 23, 2025. Three weeks of hitting the Python wall. Time to rethink everything.*

---

## The Realization

I've been trying to solve the wrong problem.

I kept asking: "How do I make Nexus talk to Python?"

The better question: "Why is Python so hard to talk to?"

And the answer is brutal: **Python's memory model is fundamentally incompatible with zero-copy sharing.**

- The GC moves objects whenever it wants
- The allocator can promote/demote memory at any time
- The GIL means even reading from another thread is unsafe

I can't hand Python a memory address and expect it to still point to valid data five seconds later.

---

## The Pivot: Build PyProbe First

If I want Python to participate in shared memory IPC, I need to **control Python's memory**, not work around it.

I need a layer that pins Python objects to fixed addresses. That understands how CPython's allocator works. That can hand me a stable pointer instead of a moving target.

**That's PyProbe.**

Nexus had to wait. The foundation needed a foundation first.

---

## Nexus "Restarting"

I pushed a commit today that says it all:

[nexus - restarting](https://github.com/Soumyadeep-Chakravarti/Nexus/commit/9a15ebdae35be16a8832a203b66222d8dad18111)

This isn't a failure. This is architecture evolving.

The original Nexus design assumed I could solve the Python problem within Nexus. I can't. PyProbe is a prerequisite.

---

## The New Dependency Chain

```
pyprobe     → pins Python memory (THE FOUNDATION)
    ↓
pyjx        → PyProbe wrapper for Java-Python bridge
    ↓
nexus       → FFI bridge using pyjx
    ↓
cobalt      → The orchestrator
```

Nexus isn't the spine anymore. **PyProbe is.**

---

## What Happens to Nexus?

Nexus gets rebuilt with the understanding that:
1. Python memory is managed by PyProbe
2. Nexus talks to PyProbe via PyJX
3. The "Nexus way" is to delegate, not to solve everything internally

I'll be documenting this new architecture in the new year.

---

## Status

Nexus: Restarting (architecture redesign)  
PyProbe: Born  
Coffee: Stolen by Christmas spirit  
Sanity: Adjusted expectations  

**Sometimes you have to go deeper before you can go higher.**

---

*Previous: [Log 0x02: The First Grind](./0x02-NEXUS-FIRST-GRIND.md)*