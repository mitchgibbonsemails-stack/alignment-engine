# Contribution Submission Template for Alignment Engine Documentation

**Use this before proposing new content to the repository.**

---

## Pre-Submission Checklist (Do This First)

- [ ] I have read the Canonical Skeleton (takes 2 min, in mechanics.md)
- [ ] I have searched existing documentation for related concepts
- [ ] I have confirmed this isn't already expressed in existing layers
- [ ] I have written the three explanations below

---

## Submission Template

Copy and fill out this template. Paste in your response.

```
**CONTENT TITLE:** [What is this about?]

**PROPOSED LAYER:** [0-6, see QUICK_REFERENCE.md for guidance]

**TYPE:** [New mechanic / New invariant / New formal relation / Translation mapping / Clarification]

---

**CHECK 1 — NOVELTY**

Question: Is this genuinely new, or does it already exist in canon?

My answer:
[Explain what gap in the existing documentation this fills. Be specific.]

Reference: [Point to the Canonical Skeleton or existing section you're extending]

---

**CHECK 2 — STRUCTURAL IMPACT**

Question: Does this change how we understand or implement the system?

My answer:
[Explain how understanding this concept changes system behavior, analysis, or implementation]

Falsifiability: [How could we verify this is correct?]

---

**CHECK 3 — CLARITY GAIN**

Question: Does this reduce ambiguity without just restating existing ideas?

My answer:
[Explain who benefits and what new understanding they gain]

Non-redundancy: [Search existing documentation - did you find duplicate phrasing?]

---

**THE CONTENT:**

[Paste the proposed addition here. Keep it concise.]

---

**PLACEMENT RATIONALE:**

[Why does this belong in Layer X rather than another layer?]

---

**INTEGRATION NOTE:**

[Any other context the reviewer should know? (Dependencies, cross-references, etc.)]
```

---

## What Happens Next

1. Reviewer checks all three criteria (Novelty, Structural Impact, Clarity Gain)
2. **Pass all three:** → Content integrated into specified layer
3. **Fail any:** → Returned with specific feedback on what to revise

---

## Quality Expectations

**Conciseness matters.**  
Better to say it precisely in 3 sentences than clearly in 10.

**Mechanical precision matters.**  
Narrative improvement without mechanical precision goes in pedagogical artefacts (Layer 6), not core layers.

**One concept = one canonical expression.**  
If it's already in canon, add a cross-reference, don't duplicate.

---

## Examples of What Passes / What Doesn't

### ✓ PASSES

- "New mathematical relation: Coupling can degrade under distortion according to Phi_ij = Λ_ij * (M_i * M_j) / (D_ij² + ε). This is not captured in current mechanics."
- "New architectural element: Time pressure creates basin vulnerability. Proposed addition to critical distinctions."
- "Translation clarification: Harmonic damping maps to coherence loss. Adds new row to Translation Table."

### ✗ FAILS

- "Here's a clearer way to explain coherence" (Clarity gain without new mechanics → goes in Layer 6 only if different from existing)
- "Distortion comes from three sources: misinterpretation, noise, and delayed feedback" (Already in canon — would be redundant)
- "Systems that are well-aligned tend to work better" (Narrative truth, not mechanical insight)

---

## Reviewers: Evaluation Quick-Check

**For each submission, ask:**

1. **Novelty**: Is this concept missing from the Canonical Skeleton or existing 6 layers?
   - If yes → check Structural Impact
   - If no → REJECT as redundant

2. **Structural Impact**: Would understanding this change how we implement or analyze the system?
   - If yes → check Clarity Gain
   - If no → REJECT (insufficient mechanical precision)

3. **Clarity Gain**: Is this more precise or less ambiguous than existing expression?
   - If yes → ACCEPT, place in specified layer
   - If no → REJECT (narrative without precision, or duplication)

**All three must pass.** One failure = return for revision.

---

## Questions?

See:
- **Full protocol:** INTEGRATION_PROTOCOL.md
- **Where things live:** QUICK_REFERENCE.md
- **The foundation:** Canonical Skeleton in mechanics.md
