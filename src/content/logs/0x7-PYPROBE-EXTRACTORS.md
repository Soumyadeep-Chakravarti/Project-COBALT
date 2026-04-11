---
title: "Log 0x07: PyProbe — Full Type Support and Infrastructure"
date: 2026-03-27
categories: ["Engineering", "PyProbe"]
tags: ["python", "cpython", "type-extractors", "cycle-detection", "ci"]
mermaid: false
---

# [ COBALT Engineering Log 0x07 ]
## PyProbe — Full Type Support and Infrastructure

*March 27, 2026. One month since PyProbe's birth. Time for the big push. Time to make it something real.*

---

## What's New

A LOT. After a month of on-and-off work, on weekends and late nights and random Tuesday evenings when I should have been sleeping, PyProbe got serious upgrades. The kind of upgrades that turn "interesting idea" into "actual usable tool".

**Commits:**
- [pyprobe - idea updated, mde docs folder for quick ref of others](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/37d94011aba2737b4f308489673c86e2e2874f3c)

And THEN the big one, the one that matters, the one that changes everything:
- [pyprobe - Add extended type extractors, CI workflow, and project infrastructure](https://github.com/Soumyadeep-Chakravarti/PyProbe/commit/b221eaf547c44d6d6fca2e92095ec47b75ad9452)

Infrastructure. CI. Testing. The boring stuff that makes projects actually LAST. The unsexy stuff that's somehow the most important. I hate maintaining CI configs but I love having them when things break. Paradox of software development.

---

## Extended Type Extractors

X-Ray now supports the FULL CPython type matrix. Every type that matters. Every type you'd want to look at:

| Type | Support |
|------|---------|
| int | ✅ |
| float | ✅ |
| str | ✅ (multi-encoding: ASCII, Latin-1, UCS-2, UCS-4 — Python's encoding is a nightmare) |
| bytes | ✅ |
| list | ✅ |
| tuple | ✅ |
| dict | ✅ (with cycle detection — the thing that almost killed me) |
| set | ✅ |

**The big win: Cycle detection.**

Python objects can reference each other. Lists can contain dicts that contain lists that contain dicts. Without cycle detection, X-Ray would recurse forever on circular references. Infinite loop. Stack overflow. Dead program. Gone.

Now it tracks visited objects and safely breaks cycles. Like a spider web — you can see the pattern, you know where you've been, you don't get stuck going around and around forever.

```python
# Self-referential structure - used to hang forever before
x = {"self": None}
x["self"] = x

ptr = pyprobe.pin(x)
result = ptr.xray()  # Safely returns with cycle marker
```

Used to crash. Now returns. Progress.

---

## CI Workflow

PyProbe now has automated testing via GitHub Actions. Real CI. The kind that catches your mistakes before you push to main and pretend they didn't happen.

Every push runs:
- Unit tests for all type extractors (if something breaks, we know immediately)
- Cycle detection tests (verify the thing actually works)
- Memory safety validation (don't segfault, that's the goal)
- Python 3.12 and 3.13 compatibility checks (both versions, both need to work)

This is the infrastructure that separates "I wrote some code" from "this is a real project". This is what makes something maintainable. This is what I should have done from day one but didn't because I was too excited to just get it working.

---

## Docs Folder

Added a proper documentation structure, the kind of docs that actually help instead of just existing to exist:

```
docs/
├── INDEX.md         # Home
├── ARCHITECTURE.md  # System design
├── CPYTHON_MEMORY.md # CPython internals reference (for the insane)
├── SAFETY_MODEL.md  # When mutation is safe vs when it will destroy you
├── ROADMAP.md       # Phase timeline (where we're going)
└── CONTRIBUTING.md  # How to help (if anyone ever wants to help lol)
```

This started as a personal project. A thing I was building for myself. Now it's becoming something publishable. Something other people could actually use. That's weird to think about. That's actually kind of cool.

---

## The Research Angle

PyProbe isn't just for Nexus. It's genuinely interesting from a CS perspective — genuinely interesting problems that actual computer scientists would care about:

- **CPython internals** — How does 3.12+ dict layout differ from 3.11? (Spoiler: massively, it's a completely different structure)
- **Memory overhead** — What's the REAL cost of a Python object? (Spoiler: more than you think, much more)
- **Safety invariants** — When is mutation actually safe vs. when does it corrupt state and make your program explode?

I'm thinking about submitting this to arXiv and JOSS eventually. A paper. Real academic publication. Me. Writing. About code I wrote at 2 AM. What is my life.

---

## Status

PyProbe X-Ray: Complete. Done. Shipped.  
Type extractors: Full coverage. All the things.  
CI: Automated. Running. Catching bugs before I do.  
Documentation: Comprehensive. Actual docs. Not just "it works trust me"

**PyProbe is ready to be the foundation. The anchor. The thing everything else builds on. Next: PyJX. Let's go.**

---

*Previous: [Log 0x06: PyJX — The Python-Java Bridge](/logs/0x6-pyjx-init)*  
*Next: [Log 0x08: Nexus Resurfaces](/logs/0x8-nexus-resurface)*