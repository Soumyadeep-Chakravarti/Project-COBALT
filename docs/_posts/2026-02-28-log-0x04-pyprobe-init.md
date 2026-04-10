---
layout: post
title: "Log 0x04: PyProbe — Memory Introspection From Scratch"
date: 2026-02-28 03:30:00 +0530
categories: [Engineering, PyProbe]
tags: [python, cpython, memory, cffi, introspection]
mermaid: false
---

# [ COBALT Engineering Log 0x04 ]
## PyProbe — Memory Introspection From Scratch

*February 28, 2026. PyProbe gets its first real code. This is where the rubber meets the road.*

---

## The Birth

Today I finally got serious about solving Python's memory problem.

**PyProbe** is born. First commits:

- [pyprobe - init and made basic memory scanner, still working on dictionary](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/9b384e1705aed76999b0db5a75f94c25a56bf5e8)
- [pyprobe - Add README.md](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/de850aa6da93ff09e47e7ca8dede45755e77d81d)

The goal is brutally simple: **pin Python objects to fixed memory addresses so external processes can read them safely.**

---

## The Approach

I'm not fighting CPython's allocator. I'm *reading* it.

Using ctypes, I can:
1. Access `PyObject_HEAD` to get type info and refcount
2. Traverse `PyDictObject` internals to extract key-value pairs
3. Validate addresses before dereferencing (safety first)

```python
import pyprobe

# Pin a dict
data = {"name": "Alice", "age": 30}
ptr = pyprobe.pin(data)

# X-Ray: see what's really in memory
result = ptr.xray()
print(result)  # {'name': 'Alice', 'age': 30}
```

---

## What "Working on Dictionary" Means

The scanner works for simple types (int, float, str, bytes). But `dict` is a different beast.

CPython 3.12+ changed the dict implementation from "compact" to something more complex. The hash table entries are now "split" across multiple arrays. Empty slots use "dummy" tombstones.

I spent 6 hours today just understanding how to iterate a `PyDictObject` in Python 3.12.

The answer involves:
- `ma_keys` (keys array)
- `ma_values` (values array, if split table)
- `dk_nentries` (occupied slots)
- Tombstone detection (entries set to dummy values)

---

## Current Status

PyProbe X-Ray: Working (basic types)  
PyProbe Dict support: Deciphering CPython internals  
Coffee: Triple shot  
Sanity: Focused  

**The foundation is being built. PyProbe will be the anchor that makes everything else possible.**

---

*Next: [Log 0x05: PyProbe Documentation — Cleaning Up the Chaos](./2026-02-28-log-0x05-pyprobe-docs.md)*
