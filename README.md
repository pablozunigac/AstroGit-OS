## AstroGit-OS --- GitOps Architecture for State Governance and Operational Lineage of Astronomical Instrumentation

| Metric | Value |
| :--- | :--- |
| **Author** | [Pablo Zúñiga](https://pablozunigac.github.io) |
| **Status** | `Phase 0 / Draft` |
| **Stable Release** | Early Q4 2026 |
| **Next Milestone** | Read-only demonstrator against operational subsystem |
| **License** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) (Architecture & Specs) / [MIT](https://tlo.mit.edu/understand-ip/exploring-mit-open-source-license-comprehensive-guide) (Code) |

---

**AstroGit-OS is a reference declarative architecture for the configuration, maintenance, and operational lineage of optomechanical instrumentation in next-generation astronomical observatories.** Applying GitOps and Infrastructure-as-Code principles, AstroGit-OS dispenses with massive astronomical data and focuses exclusively on the operational metadata required to govern scientific infrastructure.

![AstroGit-OS](/images/diagrams/diagram-3.png)

---

### The Value of Operational Certainty in Astronomy

Through an operational state reconciliation architecture, AstroGit-OS:
* **Governs Infrastructure Evolution**  
Tracks state changes across instrumentation subsystems.
* **Detects Configuration Drift**  
Identifies deviations between observed state (*As-Is*) and desired configuration (*To-Be*).
* **Establishes Traceability**  
Links observation blocks to versioned operational states via passive telemetry and non-intrusive extraction agents.

---

### Scope and Boundaries of AstroGit-OS

AstroGit-OS does not capture, store, process, simulate, or transmit astronomical data, nor does it operate telescopes in real time. Its function is to govern a versioned, asynchronous digital representation of the operational state of telescopes and other scientific infrastructure, decoupling scientific activities from engineering operations. AstroGit-OS records, stores, and audits the evolution of infrastructure configuration through Git as a version-controlled governance mechanism, keeping the declarative representation of operational state separate from its physical implementation across the instrumentation.

---

### AstroGit-OS Differentiating Principles

* **Scientific Lineage Without Massive Data**  
Associates each astronomical observation block with a SHA-256 identifier of the hardware operational state, enabling verifiable scientific traceability without burdening the repository with massive datasets.

* **Distributed Operational Resilience**  
Supports operational continuity and the recovery of versioned configurations at remote high-altitude observatories through decentralized and synchronized Git topologies.

* **Non-Intrusive Declarative Governance**  
Translates infrastructure maintenance into an auditable workflow through Pull Requests and human approval, operating strictly asynchronously without interfering with real-time telescope operations.

---

### Declarative State Example (`instrumentation.yaml`)

```yaml
version: "v0.2"
timestamp: "2026-09-10T13:38:00Z"

# Master Region (Site) Compound Operational State
site:
  id: "ESO-PARANAL-UT1"
  canonical_state: "WORKING"

# Orthogonal / Concurrent Regions (via UML Concurrent State Diagram)
# Subsystems: {Dome, Mount, Optics, Instrumentation}
subsystems:
  region_dome:
    entity: "Dome"
    active_state: "OPEN"
    substates:
      shutter: "FULL_OPEN"
      azimuth_lock: "ENGAGED"

  region_mount:
    entity: "Mount"
    active_state: "TRACKING"
    substates:
      axis_ra: "ENCODER_LOCKED"
      axis_dec: "ENCODER_LOCKED"

  region_optics:
    entity: "Optics"
    active_state: "WAITING"
    substates:
      m1_actuators: "PARKED"
      adaptive_loop: "OPEN"

  region_instruments:
    entity: "Instrumentation"
    active_state: "WAITING"
    substates:
      cryo_temperature: "STABLE"
      detector: "IDLE"

# Cryptographic Lineage Metadata (State Hash)
lineage:
  state_sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
```

---
Content & Architecture under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en). Code under [**MIT**](https://tlo.mit.edu/understand-ip/exploring-mit-open-source-license-comprehensive-guide).  
**2026 Cuxhaven Labs.**
