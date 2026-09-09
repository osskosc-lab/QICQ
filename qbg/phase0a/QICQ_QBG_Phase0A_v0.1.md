# QICQ Quantum Behavior Qualification Gate (QBG)
## Phase 0A — Minimal Synthetic Resource Qualification v0.1

**Study ID:** QICQ-QBG-P0A  
**Status:** FROZEN SYNTHETIC QUALIFICATION / NO PROCESS-MATRIX CLAIM  
**Execution class:** falsification-first gate mechanics audit  
**Claim ceiling:** a two-qubit resource proxy can distinguish coherence-only mimics from an entanglement resource under the frozen synthetic design.

## 0. Why this phase exists

QICQ needs a bridge quantity only if it can separate:

1. a generic causal/structural difference,
2. a genuinely quantum resource relative to a frozen free set,
3. an operationally useful quantum signature.

A basis-dependent off-diagonal quantity such as Q_delta is not enough by itself. Phase 0A therefore freezes a deliberately small synthetic problem where the stronger resource is exactly auditable.

This phase is not a Quantum Switch simulation and not a process-matrix causal-nonseparability test.

## 1. Frozen bridge architecture

The intended hierarchy is:

Correlation
-> intervention-accessible structure
-> resource relative to a free set
-> optional operational witness

For this Phase 0A proxy:

- diagnostic coherence:
  Q_delta(rho) = ||rho - diag(rho)||_F
- free set:
  separable two-qubit states
- resource quantity:
  entanglement negativity
- optional operational witness:
  maximal CHSH value

The future QICQ process-matrix line must replace this proxy free set with the scientifically relevant process free set, e.g. causally separable processes for M_CNS.

## 2. Resource quantity

For a two-qubit density operator rho,

N(rho) = (||rho^(T_B)||_1 - 1) / 2.

For 2 x 2 systems the PPT criterion is necessary and sufficient for separability, so N(rho) > 0 excludes the separable free set in this proxy.

Frozen qualification threshold:

N(rho_target) >= 0.20.

Frozen mimic tolerance:

N(rho_mimic) <= 1e-9.

This does not imply causal nonseparability, indefinite causal order, or quantum-controlled order.

## 3. Frozen synthetic classes

### Target class

Noisy Bell/Werner proxy:

rho(p) = p |Phi+><Phi+| + (1-p) I/4

with:

- p sampled uniformly from [0.75, 1.00];
- independent random local unitaries applied;
- 100 frozen seeds beginning at 20260909.

### Mimic classes

Each seed includes:

- product-coherence mimic;
- separable-memory mimic: convex mixture of random product states;
- classical common-cause mimic: random diagonal correlated state.

Deterministic reference mimics also include:

- |+><+| tensor |0><0|;
- a classical 00/11 common-cause mixture;
- product mixed state;
- maximally mixed state.

## 4. Why Q_delta is explicitly demoted to diagnostic status

The deterministic target Bell proxy and the coherent product mimic are frozen so that both have the same off-diagonal Frobenius norm:

Q_delta(target) = Q_delta(coherent product mimic).

Yet:

N(target) > 0

and:

N(coherent product mimic) = 0.

Therefore a coherence-only quantity cannot be promoted to the resource measure in this gate.

## 5. Frozen gates

| Gate | Test | Frozen pass condition |
|---|---|---|
| G0 | physical validity | every generated 4x4 state is Hermitian, PSD within 1e-10, and trace 1 |
| G1 | coherence insufficiency | target and coherent-product mimic both have Q_delta > 0.1, while only target exceeds the negativity threshold |
| G2 | target resource exclusion | all 100 target seeds have negativity >= 0.20 |
| G3 | local-basis robustness | negativity changes by <= 1e-9 under frozen random local-unitary trials |
| G4 | free-operation monotonicity | local dephasing/depolarizing channels increase negativity by at most 1e-9 |
| G5 | mimic exclusion | all product, separable-memory, and classical-common-cause mimics have negativity <= 1e-9 |
| G6 | optional operational witness | all targets have S_CHSH > 2 + 1e-6 and all mimics have S_CHSH <= 2 + 1e-6 |

G0-G5 are the core Phase 0A qualification gates. G6 is intentionally optional and must not be treated as a necessary condition for quantum resource existence in general.

## 6. Decision rule

### P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS

G0-G5 pass and G6 passes.

Permitted claim:

The frozen two-qubit proxy pipeline distinguishes coherence-only/separable mimics from the target resource and also recovers the frozen CHSH witness.

### P0A_PROXY_QUALIFIED_RESOURCE_ONLY

G0-G5 pass and G6 fails.

Permitted claim:

The frozen resource proxy passes, but the selected operational witness is not qualified.

### STOP_...

Any G0-G5 failure.

Permitted claim:

The bridge gate mechanics are not qualified and must be repaired before any process-matrix extension.

## 7. Claim firewall

Phase 0A does not establish:

- causal nonseparability;
- quantum-controlled causal order;
- indefinite causal order;
- a Quantum Switch implementation;
- quantum memory in any biological system;
- quantum consciousness;
- Orch OR;
- a xenon mechanism;
- any soul, self, or ontology claim.

The word "quantum" in Phase 0A refers only to a standard two-qubit entanglement resource under the frozen proxy.

## 8. Relationship to H_QC

H_QC Phase 1 remains an independent real-world replication line.

QBG Phase 0A is methodological infrastructure. Its synthetic success cannot raise the H_QC claim level and cannot authorize any biological or consciousness inference.

## 9. Phase 0B entry condition

Phase 0B may begin only if G0-G5 pass in CI.

Phase 0B must replace the density-operator proxy with a genuine process representation and must freeze:

1. process validity constraints;
2. the causally separable free set;
3. M_CNS or another explicitly defined distance/witness;
4. an SDP or equivalent certified optimizer;
5. fixed-order + coherence adversarial mimics;
6. classical/non-Markov memory mimics where operationally applicable;
7. basis/representation robustness rules;
8. free-supermap monotonicity scope;
9. intervention/tomography access assumptions;
10. a claim firewall no weaker than this phase.

No result from Phase 0A alone may be described as evidence for causal nonseparability.
