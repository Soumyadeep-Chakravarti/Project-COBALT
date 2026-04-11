---
title: "Log 0x04: PyProbe — Memory Introspection From Scratch"
date: 2026-02-28
categories: ["Engineering", "PyProbe"]
tags: ["python", "cpython", "memory", "cffi", "introspection"]
mermaid: false
---

# [ COBALT Engineering Log 0x04 ]
## PyProbe — Memory Introspection From Scratch

*February 28, 2026. PyProbe gets its first real code. This is where the rubber meets the road. No more theory. No more speculation. Code. Actual code. Finally.*

---

## The Birth

Today I finally got SERIOUS about solving Python's memory problem. Not thinking about it. Not planning it. ACTUALLY DOING IT.

**PyProbe** is born. First commits hit the repo like bullets:

- [pyprobe - init and made basic memory scanner, still working on dictionary](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/9b384e1705aed76999b0db5a75f94c25a56bf5e8)
- [pyprobe - Add README.md](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/de850aa6da93ff09e47e7ca8dede45755e77d81d)

The goal is brutally simple, almost laughably so in its ambition: **pin Python objects to fixed memory addresses so external processes can read them safely without the memory running away like a scared cat**

That's it. That's the whole thing. Sounds simple. Will probably take 6 months. Worth it.

---

## The Approach

I'm not fighting CPython's allocator. That's suicide. I'm *reading* it. I'm watching it. I'm understanding its patterns so I can predict where things will be.

Using ctypes, I can:
1. Access `PyObject_HEAD` to get type info and refcount (the skeleton of every Python object)
2. Traverse `PyDictObject` internals to extract key-value pairs (the treasure inside)
3. Validate addresses before dereferencing (safety first, don't crash, don't die)

```python
import pyprobe

# Pin a dict
data = {"name": "Alice", "age": 30}
ptr = pyprobe.pin(data)

# X-Ray: see what's really in memory
result = ptr.xray()
print(result)  # {'name': 'Alice', 'age': 30}
```

This is the dream. This is what I want to work. X-Ray into Python's brain and see what's actually happening in there instead of guessing.

---

## What "Working on Dictionary" Means

The scanner works for simple types (int, float, str, bytes). Easy. Child's play.

But `dict`? `dict` is a DIFFERENT BEAST. A rabid one.

CPython 3.12+ changed the dict implementation from "compact" to something more complex. The hash table entries are now "split" across multiple arrays. Empty slots use "dummy" tombstones. It's a whole thing. A whole annoying thing.

I spent 6 HOURS today just understanding how to iterate a `PyDictObject` in Python 3.12. Six hours. For ONE data structure. My brain hurts.

The answer involves:
- `ma_keys` (keys array)
- `ma_values` (values array, if split table)
- `dk_nentries` (occupied slots)
- Tombstone detection (entries set to dummy values that LOOK occupied but AREN'T)

This is what nobody talks about when they talk about "Python internals". It's not magic. It's not elegant. It's a bunch of arrays with special rules and if you get ONE thing wrong everything segfaults.

---

## Current Status

PyProbe X-Ray: Working (basic types, at least)  
PyProbe Dict support: Deciphering CPython internals (slowly, painfully, one byte at a time)  
Coffee: Triple shot. Needed. Very needed.  
Sanity: Focused. Finally. Something is working. After all this time, something is actually WORKING.

**The foundation is being built. PyProbe will be the anchor that makes everything else possible. This is the thing that holds the whole system together. This is the thing I needed to build before I could build anything else. And it's happening. Finally. It's happening.**

---

*Previous: [Log 0x03: The Pivot](/logs/0x3-nexus-restart)*  
*Next: [Log 0x05: PyProbe Documentation — Cleaning Up the Chaos](/logs/0x5-pyprobe-docs)*
