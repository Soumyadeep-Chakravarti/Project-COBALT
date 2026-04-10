# [ PROJECT COBALT ]
### **"ABSTRACTION IS A WEAPON. USE IT."**

The objective is a synthetic infrastructure counterpart designed to serve as the **cognitive core of a custom AR-based Operating System**. One interface, nine specialized languages, and a complete removal of the friction between human intent and bare-metal execution.

---

## 📡 Engineering Logs
The development journey, documented in real-time:
- **[Log 0x00: Genesis](./engineering-logs/LOG_0x00_GENESIS.md)** — The thesis, the anatomy, the blueprint
- [Log 0x01: The Handshake](./engineering-logs/LOG_0x01_HANDSHAKE.md) *(coming soon)* — Java 25 FFM API meets Unix Domain Sockets
- [Log 0x02: The Stabilizer](./engineering-logs/LOG_0x02_STABILIZER.md) *(coming soon)* — PyProbe and the war against the GIL

---

## 📁 Repository Structure
```text
/project-cobalt
├── /nexus              # L03: Java 25 Panama Bridge (The Interop Spine)
├── /specialists        # Language Specialists
│   ├── /rust-guardian  # L04: Integrity & Safety
│   ├── /c-mechanic     # L01: GPU/Wayland Metal
│   ├── /py-researcher  # L05: AI Logic (PyProbe-powered)
│   └── /julia-scientist# L06: Spatial Math
├── /orchestrator       # L06: Specialist Selector
├── /docs
│   ├── /engineering-logs  # The development journal
│   └── /contracts      # CIS Standard & .proto files
└── /ar-os-substrate    # OpenXR/Wayland AR Layer
```

---

## 1. THE SPECIALIST HIVEMIND
Architecture is a meritocracy. In COBALT, languages are chosen solely for their domain-specific superpowers.

* **[🦀] THE GUARD (Rust):** **Memory Safety.** The paranoid core. Binary integrity and memory-safe system daemons.
* **[🔌] THE MECHANIC (C):** **Raw Access.** Direct driver interfacing, kernel hooks, and low-level hardware control. 
* **[🚀] THE DISPATCHER (Go):** **Concurrency.** High-speed networking, API gateways, and asynchronous orchestration.
* **[☕] THE NEXUS (Java):** **Stability.** **The L3 Foundation.** Built for transactional consistency and long-term state management.
* **[🐍] THE RESEARCHER (Python):** **AI/Automation.** Rapid prototyping and high-level logic mapping. 
* **[💧] THE MEDIC (Elixir):** **Resilience.** Fault tolerance via the BEAM VM. Self-healing process isolation.
* **[λ] THE LOGIC (Haskell):** **Verification.** Functional purity and mathematically proven state transitions.
* **[🟢] THE SCIENTIST (Julia):** **Computation.** Native, parallel matrix operations and numerical simulation.
* **[🌙] THE GHOST (Lua):** **Agility.** Lightweight scripting for hot-swappable logic injection.

---

## 2. THE 11-LAYER ANATOMY
A vertical chain of command structured to compartmentalize functional responsibility from the persona down to the hardware.

* **L11 - L10 [CONTROL]:** Governance (Cost/Compliance) and Persona (Spatial Intent/Affective Engine).
* **L09 - L07 [BRAIN]:** Evolution (Self-healing), Temporal (History/Rollback), and Translator (Planning).
* **L06 - L05 [ORCHESTRATION]:** Polyglot Selector (Language choice) and Model Synthesis (Config Graph).
* **L04 - L01 [SUBSTRATE]:** Guardian (Integrity), Nexus (Interop), Foundation (I/O), and Metal (Kernel/GPU).

---

## 3. PROJECT NEXUS: THE POLYGLOT BRIDGE (L3)
**Nexus** is the foundational pillar implemented in **Java**. While other layers handle the "thinking," Nexus handles the **mechanical reality** of cross-language execution.

* **State Persistence:** Unlike ephemeral scripts, Nexus maintains a persistent JVM-based state machine that tracks the health of all external language processes.
* **Environment Provisioning:** It dynamically generates the necessary environment variables, pathing, and dependency contexts required for a specialist to run without host pollution.
* **The Common Tongue:** It acts as the primary orchestrator for **FFI (Foreign Function Interface)** and **Internal RPC**. It ensures data structures passed from a Go network service are correctly interpreted by a C-based hardware hook.
* **Standalone Capability:** Designed as an independent library/service, allowing for polyglot interop even outside the full COBALT stack.

---

## 4. THE EXECUTION LOOP (INTENT TO ACTION)
The system operates on a strict **Evaluation $\rightarrow$ Provisioning $\rightarrow$ Execution** pipeline to ensure that no code is run without total environmental control.

1.  **Selection (L06):** The Orchestrator analyzes the task and selects the optimal language specialists. (e.g., Julia for spatial math, C for the AR-OS render).
2.  **Bridge Construction (L03):** **Nexus** establishes the communication bridge, provisioning the virtual memory or RPC sockets needed for distinct runtimes to share data.
3.  **Integrity Check (L04):** The **Guardian** performs a SHA-256 verification of the generated logic and the Nexus-provisioned environment to prevent injection.
4.  **Process Dispatch (L02/L01):** The task is dispatched to the Foundation layer. Nexus monitors the process lifecycle, while the Bare Metal layer manages CPU priority and GPU scheduling.
5.  **Audit Commit (L04/L08):** Upon completion, the result is piped back through the Nexus, verified, and committed to the Temporal Layer for historical audit.

---

## 5. ARCHITECTURAL REALITY
**NO AUTHORITY. NO MONOCULTURES. JUST PURE POLYGLOT POWER.**

COBALT is moving from a **Python Blueprint** to a **Native Substrate** hosted on a **Custom AR-OS**. As the logic matures, the scaffolding is replaced by the specialist languages. The result is a system as safe as Rust, as fast as C, and as stable as Java.

> *"They said a polyglot AR system was impossible. I told them their imagination was just limited by their current window manager."*
