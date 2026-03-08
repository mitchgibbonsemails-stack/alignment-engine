# Alignment Engine Documentation — Quick Reference & Current State

**Use this to orient yourself in seconds. For details, see INTEGRATION_PROTOCOL.md**

---

## What This System Is (30-second version)

Real events have multiple simultaneous projections: physical, mathematical, harmonic, logical, geometric, computational.

The Alignment Engine selects actions that reduce the system's distance from aligned-with-reality.

A model is valid if the same structure holds across all projections.

---

## Documentation Hierarchy

```
LAYER 0: CANONICAL SKELETON
    ↓
    Core principle, core loop, core metric, core rule
    (All else unfolds from this)
    
LAYER 1: SURFACE
    ↓
    Conceptual explanation for general audience
    
LAYER 2: STRUCTURE
    ↓
    Diamond geometry, 8-node lattice, system map
    
LAYER 3: MECHANICS
    ↓
    Algorithm, mathematics, distortion model, coupling
    
LAYER 4: TRANSLATION
    ↓
    Cross-domain mappings (math ↔ harmonic ↔ physical, etc.)
    
LAYER 5: FORMAL SPECIFICATION
    ↓
    Specification v1.0: Official structure, all layers unified
    
LAYER 6: PEDAGOGICAL ARTEFACTS
    ↓
    Presentations at different depths (surface/geometry/deep)
```

---

## Where Each Concept Lives

| Concept | Primary Layer | Reference |
|---------|---------------|-----------|
| One event = multiple projections | Layer 0 | Canonical Skeleton |
| Core loop (signal → action) | Layer 0 | Canonical Skeleton |
| Distance from alignment (Δ) | Layer 0 | Canonical Skeleton |
| 8 signal channels (S, D, C, B, Λ, Tᵤ, Ω, Z) | Layer 3 | Specification v1.0 Section 1 |
| State vector X = [S, D, C, K, B, Tᵤ, Ω, Λ] | Layer 2 | 8-Node Lattice Structure |
| Diamond Layer (translation hub) | Layer 2 | Diamond Layer Architecture |
| Alignment functional A(X, u, R) | Layer 3 | Mathematical Framework |
| Distortion D = \|\|Δ\|\| + αI + βV + γK | Layer 3 | Specification v1.0 |
| Coherence C = 1/(1+D) | Layer 5 | Specification v1.0 |
| Action selection u* = argmin V(x) | Layer 0 | Canonical Skeleton |
| Transient turbulence window | Layer 5 | Specification v1.0 |
| Misalignment debt | Layer 5 | Specification v1.0 |
| Basin of attraction | Layer 5 | Specification v1.0 |
| Coupling strength Φ = Λ(M₁M₂)/(D²+ε) | Layer 5 | Specification v1.0 |
| Convergence rule: dD/dt ≤ 0, dΩ/dt ≥ 0 | Layer 1 | Core Principles |
| 12-step engine algorithm | Layer 3 | Alignment Engine Algorithm |
| Cross-domain translation table | Layer 4 | Universal Translation Table |
| Critical distinctions (visibility window, false basin, etc.) | Layer 5 | Specification v1.0 |
| Surface explanations (Canon, Core Page, Simple Summary) | Layer 6 | Layered Documentation Artefacts |
| Geometry explanations (Diamond, State, Ground) | Layer 6 | Layered Documentation Artefacts |
| Deep mechanics (equations, proofs, precision) | Layer 6 | Layered Documentation Artefacts |

---

## Current State Summary

| Layer | Status | File | Key Sections |
|-------|--------|------|--------------|
| 0 | ✓ Complete | mechanics.md | Canonical Skeleton |
| 1 | ✓ Complete | mechanics.md | Universal Alignment Canon, Core Principles |
| 2 | ✓ Complete | mechanics.md | Diamond Layer, 8-Node Lattice, System Map |
| 3 | ✓ Complete | mechanics.md | Algorithm, Mathematical Framework |
| 4 | ✓ Complete | mechanics.md | Universal Translation Table |
| 5 | ✓ Complete | mechanics.md | Specification v1.0 |
| 6 | ✓ Complete | mechanics.md | Layered Documentation Artefacts |

**Total coverage:** All foundational layers implemented. Architecture is complete.

---

## If You Want to Propose New Content

1. **Read** the Canonical Skeleton (Layer 0) first — takes 2 minutes
2. **Check** does your content already exist in Layers 1-6?
3. **Answer** these three questions:
   - Is this genuinely new? (Check 1: Novelty)
   - Does it change how we understand the system? (Check 2: Structural Impact)
   - Does it reduce ambiguity? (Check 3: Clarity Gain)
4. **Use the template** in INTEGRATION_PROTOCOL.md Section 13

If all three checks pass → your content belongs in the canon.  
If any fail → either revise or the material is deferred.

---

## What Success Looks Like

The documentation is optimized for:
- ✓ **Orientation speed**: New reader understands in minutes, not hours
- ✓ **Mechanical clarity**: Equations, not narrative
- ✓ **No redundancy**: One concept = one canonical statement
- ✓ **Structural coherence**: Everything derives from Skeleton
- ✓ **Scalability**: Growing in precision, not length

---

## Files in the Documentation

- **mechanics.md**: Complete unified documentation (Layers 0-6)
- **INTEGRATION_PROTOCOL.md**: This file (review procedures, checks, versioning)
- **QUICK_REFERENCE.md**: Orientation guide (you are here)

---

## Version Info

- **Specification v1.0**: Current canonical mechanics
- **Integration Protocol v1.0**: Current review standard
- **Documentation Status**: Complete/Stable

Next addition will trigger version assessment per INTEGRATION_PROTOCOL.md Section 7.

---

## Want to Understand This Better?

**2-minute introduction:**  
Read Canonical Skeleton in mechanics.md

**10-minute introduction:**  
Read Canonical Skeleton + Layer 0 context in mechanics.md

**30-minute deep dive:**  
Read Specification v1.0 in mechanics.md

**Complete mastery:**  
Read all 6 layers in mechanics.md in order, top to bottom

**Contributing:**  
Read INTEGRATION_PROTOCOL.md Sections 2-4, then use Section 13 template
