# QICQ QBG Phase 0B-I v0.1 — Deterministic Process-Matrix CNS Qualification

**Study ID:** QICQ-QBG-P0BI  
**Status:** FROZEN DETERMINISTIC SDP QUALIFICATION  
**Parent:** Phase 0A-R v0.1 / head `d2bf56534c314f922c874ac9efa38b5e6f559fa8`  
**Claim ceiling:** numerical qualification of a bipartite process-matrix causal-nonseparability resource test on frozen synthetic gold cases only.

## 1. Mission

Phase 0B-I tests whether the QICQ claim-firewall can be lifted from a two-qubit state proxy to a genuine process-matrix domain without conflating resource certification with a particular operational witness.

This phase is deliberately deterministic. It does **not** run a Quantum Switch adversarial experiment. It first qualifies B0–B6 on analytically specified bipartite gold cases.

## 2. Frozen process convention

Tensor order:

`A_I ⊗ A_O ⊗ B_I ⊗ B_O`

All four spaces are qubits, so the process operator is `16 × 16` and normalized by

`Tr(W) = d_AO d_BO = 4`.

For subsystem `X`, `_X W` denotes replacement of `X` by maximally mixed identity:

`_X W = I_X/d_X ⊗ Tr_X W`, with tensor positions restored to the frozen order.

A bipartite process is treated as valid when it is Hermitian PSD, has trace 4, and satisfies the standard homogeneous linear process constraints used by this implementation:

- `[1-B_O] A_I A_O W = 0`
- `[1-A_O] B_I B_O W = 0`
- `[1-A_O][1-B_O] W = 0`

Definite order adds:

- `A≺B`: `_B_O W = W`
- `B≺A`: `_A_O W = W`

## 3. Frozen causally-separable cone

The unnormalized causally separable cone is represented as

`X_sep = X_AtoB + X_BtoA`,

where both components are PSD, satisfy the homogeneous process constraints, and satisfy their respective definite-order constraint.

## 4. Primary resource quantity

Phase 0B-I uses a numerical generalized causal robustness SDP:

`R_CNS^g(W) = min Tr(X_sep)/4 - 1`

subject to

- `X_sep` belongs to the unnormalized causally-separable cone;
- `X_sep - W >= 0`.

Because `X_sep` and `W` satisfy the same homogeneous process subspace constraints, the PSD difference is an unnormalized valid-process noise term in this frozen formulation.

This is a numerical SDP qualification, not a formal analytic proof.

## 5. Frozen gold cases

### Free calibration

`W_AtoB = 1/4 [I + I⊗Z⊗Z⊗I]`

`W_BtoA = 1/4 [I + Z⊗I⊗X⊗Z]`

`W_mix = 0.5 W_AtoB + 0.5 W_BtoA`

### Structural/off-diagonal free mimic

`W_AtoB_offdiag = 1/4 [I + 0.8 I⊗X⊗X⊗I]`

It is deliberately off-diagonal in the computational basis while remaining definite order `A≺B`.

### CNS target

The deterministic OCB reference is

`W_OCB = 1/4 [I + (I⊗Z⊗Z⊗I + Z⊗I⊗X⊗Z)/sqrt(2)]`.

The purpose is implementation qualification against a known synthetic causally-nonseparable reference, not a new physical discovery.

## 6. Frozen tolerances and solver

- Python `3.12.14`
- NumPy `2.5.3`
- SciPy `1.18.1`
- CVXPY `1.9.2`
- SCS `3.2.11`
- SCS `eps_abs = 1e-7`
- SCS `eps_rel = 1e-7`
- SCS `max_iters = 200000`
- process residual tolerance: `1e-8`
- free robustness tolerance: `5e-5`
- positive CNS threshold: `1e-4`
- solver residual/gap ceiling: `1e-5`
- representation robustness tolerance: `5e-5`
- tested-free-mixing tolerance: `5e-5`

No threshold may be changed after the first qualification output merely to obtain PASS.

## 7. Gates

| Gate | Frozen requirement |
|---|---|
| B0 PROCESS VALIDITY | every gold process satisfies PSD, trace, and frozen process linear constraints |
| B1 FREE-SET CALIBRATION | `W_AtoB`, `W_BtoA`, `W_mix` each have `R_CNS^g <= 5e-5` |
| B2 CNS RESOURCE CERTIFICATION | `W_OCB` has `R_CNS^g > 1e-4` |
| B3 ADVERSARIAL FREE/MIMIC EXCLUSION | off-diagonal definite-order mimic has `R_CNS^g <= 5e-5` |
| B4 REPRESENTATION ROBUSTNESS | party-swap-equivalent OCB representation changes robustness by at most `5e-5` |
| B5 TESTED FREE-MIXING NONINCREASE | mixing OCB with the maximally mixed free process does not increase robustness beyond `5e-5` numerical tolerance |
| B6 SDP NUMERICAL CERTIFICATION | all required solves report `optimal` and SCS primal residual, dual residual, and gap are each `<=1e-5` |

B0–B6 are all core in Phase 0B-I.

## 8. Decision rule

If all B0–B6 pass:

`P0BI_DETERMINISTIC_CNS_SDP_QUALIFIED`

Otherwise:

- B0/B4/B6 failure → `STOP_IMPLEMENTATION_OR_CERTIFICATION_FAILURE`
- B1/B2/B3/B5 failure → `STOP_RESOURCE_QUALIFICATION_FAILURE`

The exact failed gates are also emitted.

## 9. Resource certification is not particular-witness certification

Phase 0B-I intentionally contains no B7 particular operational witness. The optimal SDP dual variables are solver certificates associated with B2/B6; they are **not** relabeled as an independently pre-specified operational witness.

A later phase may add B7 only after B0–B6 qualify.

## 10. Quantum Switch firewall

The Quantum Switch is **not executed in Phase 0B-I**. Its process representation, tripartite/control convention, witness family, access assumptions, and adversarial envelope must be separately frozen after this deterministic bipartite qualification passes.

## 11. Claim firewall

Even a complete PASS permits only:

> Under the frozen bipartite process representation, causally-separable cone, solver, and numerical tolerances, the deterministic synthetic reference suite numerically qualifies the process-level CNS resource-certification machinery.

It does not establish a new physical resource, an experimental Quantum Switch, indefinite causal order in nature, a biological quantum mechanism, xenon causality, or quantum consciousness.

## 12. Deferred Phase 0B prerequisites (NOT tested by Phase 0B-I)

The main `README.md` section "Next methodological boundary" and the Phase 0A spec §9 ("Phase 0B entry condition") list prerequisites that a full Phase 0B must freeze before execution. Phase 0B-I addresses only the deterministic process-representation / validity / causally-separable-cone / SDP-certification subset (items 1–4 and 7 of Phase 0A §9, plus a deterministic off-diagonal definite-order mimic for item 5). The following prerequisites are explicitly **DEFERRED** and are **not tested** by Phase 0B-I:

| Deferred prerequisite | Source | Status in Phase 0B-I |
|---|---|---|
| Intervention / tomography access assumptions and operational access assumptions (what parties can actually prepare, intervene on, and measure; how `W` would be reconstructed) | README "Next methodological boundary" ("operational access assumptions"); Phase 0A §9 item 9 | **DEFERRED — not tested.** All gold cases are analytically specified; no tomography, intervention model, or finite-data reconstruction is simulated. |
| Classical / non-Markovian memory mimics | Phase 0A §9 item 6 | **DEFERRED — not tested.** No classical-memory, non-Markovian, or latent-environment mimic is included in B3. B3 covers only one deterministic off-diagonal definite-order process. |
| Free-supermap monotonicity scope (which class of free supermaps/operations `R_CNS^g` must be non-increasing under, and a test over that class) | README "Next methodological boundary" ("free-supermap monotonicity scope"); Phase 0A §9 item 8 | **DEFERRED — not tested.** No supermap family is frozen or sampled. B5 is not a monotonicity test (see §13). |

A Phase 0B-I PASS therefore does **not** satisfy the full Phase 0B entry requirements. These items must be frozen and tested in a later phase before any claim that depends on them.

## 13. Scope note on B5 (tested free-mixing nonincrease)

B5 tests exactly one case: `W_B5 = η W_OCB + (1-η) W_white` with `η = 0.5`, where `W_white = I_16 / 4` is the maximally mixed process. `W_white` is a product, definite-order process and is itself already in the frozen causally-separable (free) set (`R_CNS^g = 0`). In the qualification run the mixture itself also evaluates to `R_CNS^g = 0.0` (vs. `R_CNS^g(W_OCB) ≈ 0.17157`), i.e. at `η = 0.5` the mixture already lies in the free set.

B5 is therefore a single-point sanity check of mixing with one free process at one noise level. It is **not** a test of monotonicity under free supermaps, not a scan over `η`, and not a test with other free processes. Its name ("tested free-mixing nonincrease") should be read with this restricted scope.

## 14. Amendment log

| Version | Date (JST) | Change | Direction | scientific_spec_changed | Claim ceiling | Rationale |
|---|---|---|---|---|---|---|
| v0.1 | (initial) | Initial frozen deterministic SDP qualification spec; initial qualification run 34479107644 at `25c98a9`. | — | — | as §11 | — |
| v0.1 (provenance) | (pre-2026-09-26) | Reproducibility hardening: pip and transitive package versions pinned (`4eb8ea7`, `c0e9876`, `7095aef`). | none | false | unchanged | Recorded in `manifest.json` `reproducibility_hardening`. |
| v0.1 (docs-1) | 2026-09-26 | Docs only: added §12 (deferred prerequisites: intervention/tomography and operational access assumptions; classical/non-Markovian memory mimics; free-supermap monotonicity scope — not tested by 0B-I), §13 (B5 scope: OCB with η=0.5 white noise only; white noise already free, mixture R=0), and this log. No code, gold case, gate, threshold, tolerance, solver setting, or decision rule changed. | none (clarification of scope; no gate loosened or tightened) | false | unchanged | Make explicit which Phase 0B entry prerequisites (README "Next methodological boundary", Phase 0A §9) remain outstanding, so a 0B-I PASS is not over-read as satisfying them. |
