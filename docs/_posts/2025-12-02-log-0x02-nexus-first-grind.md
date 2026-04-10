---
layout: post
title: "Log 0x02: The First Grind"
date: 2025-12-02 03:00:00 +0530
categories: [Engineering, Architecture]
tags: [nexus, java, project-panama, ffi, challenges]
mermaid: false
---

# [ COBALT Engineering Log 0x02 ]
## The First Grind

*December 2, 2025. Three weeks of Nexus development. Here's what's been breaking and what I've learned.*

---

## The Problem I Didn't Anticipate

Nexus is coming along, but I hit something unexpected: **the Panama API surface is massive**.

Java 25's Foreign Function & Memory API is powerful, but it's also sprawling. `MemorySegment`, `Arena`, `SymbolLookup`, `Linker`, `FunctionDescriptor` — they all interact in ways the documentation doesn't fully explain.

I spent two weeks just understanding how to:
1. Allocate memory that survives GC
2. Create a struct layout that matches a C header
3. Pass a pointer to an external process without losing it

**Latest commits:**
- [Nexus - Update](https://github.com/Soumyadeep-Chakravarti/Nexus/commit/0ff4d26a2ebe794d4d12730e93338de581522a18)
- [Nexus - Update](https://github.com/Soumyadeep-Chakravarti/Nexus/commit/2eda3081462171783e7650df6c95378cc2dfb4f4)
- [Nexus - Docs](https://github.com/Soumyadeep-Chakravarti/Nexus/commit/974d8fcbac05fff2cce846058f612b221af8df35)

---

## What Actually Works

Right now Nexus can:
- Allocate native memory via `Arena.ofShared()`
- Define C struct layouts using `MemoryLayout`
- Call a simple native function (tested with `printf`)

What doesn't work:
- Passing memory to Python (the GIL fights back)
- Passing memory to Rust (no stable ABI yet)
- Multi-threaded memory sharing (race conditions everywhere)

---

## The Python Problem (Preview)

I tried to hand a `MemorySegment` address to a Python process today.

Python said "thanks" and moved the data somewhere else because that's what CPython's allocator does.

The JVM tried to read the old address.

**Segfault.**

This is why I haven't pushed a "working" Nexus yet. The memory sharing works in Java-land. The moment I try to cross the runtime boundary, everything breaks.

---

## Docs Were Written

I spent a day documenting what I *do* know. The Nexus docs folder has:
- Memory model overview
- Arena lifecycle
- Struct layout examples

It's sparse, but it's something.

---

## Status

Nexus: Working (within JVM bounds)  
Python interop: Blocked  
Coffee: Empty  
Sanity: Deteriorating  

**Three weeks in. The Java side is solid. The external runtime communication is the wall I'm hitting.**

---

*Previous: [Log 0x01: Nexus — The First Spark](./2025-11-04-log-0x01-nexus-init.md)*  
*Next: [Log 0x03: The Pivot — Restarting with new vision](./2025-12-23-log-0x03-nexus-restart.md)*
