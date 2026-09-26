# QICQ Quantum Behavior Qualification Gate (QBG)
## Phase 0A-R — Adversarial Generalization Challenge v0.1

**Study ID:** QICQ-QBG-P0AR  
**Status:** FROZEN ADVERSARIAL GENERALIZATION CHALLENGE / NO PROCESS-MATRIX CLAIM  
**Parent:** QBG Phase 0A v0.1.1 debug-hardened head `bdc3dce5f7d4b8dce73a34f6c0f91e76e5ace613`  
**Execution class:** falsification-first generalization stress test  
**Claim ceiling:** synthetic two-qubit qualification-gate mechanics only.

## 0. Purpose

Phase 0A established that the frozen two-qubit proxy pipeline can separate a structural diagnostic from a stronger free-set-relative resource and an optional operational witness. Phase 0A-R asks a narrower next question:

> Do the same core gate semantics survive when the exact Phase 0A generator is replaced by a broader, adversarially varied two-qubit proxy family whose envelope is frozen before execution?

"Adversarially varied" does **not** mean post-hoc tuning. The variation envelope, thresholds, seed schedule, target families, mimic families, channel families, and stopping rules below are frozen before the qualification run.

This phase is **not** a process-matrix test and does not evaluate causal nonseparability, the Quantum Switch, indefinite causal order, a biological quantum mechanism, or consciousness.

## 1. One proposition / one primary metric / one baseline / one falsification experiment

### Proposition

The Phase 0A core qualification semantics generalize beyond the exact frozen candidate: resource-positive two-qubit targets remain separated from adversarial separable mimics, local-basis changes preserve negativity, and the expanded tested local-channel family does not increase negativity or produce invalid states.

### Primary metric

Resource separation margin

\[
 g_N = \min_{\rho\in T} N(\rho) - \max_{\sigma\in M} N(\sigma).
\]

Frozen primary pass floor:

\[
 g_N \ge 0.20 - 10^{-9}.
\]

This margin is a finite-sample property of the frozen adversarial run. It is not a population-level generalization theorem.

### Baseline

QBG Phase 0A v0.1.1 frozen result:

- target minimum negativity: `0.31254751364720484`;
- mimic maximum negativity: `3.409409165475825e-16`;
- baseline separation margin: approximately `0.3125475136472045`.

### Falsification experiment

Run the unchanged resource threshold and mimic tolerance against a broader target/mimic family, stronger local-channel stress, and denser basis trials. Any failure of G0–G5 is a core STOP. G6 remains optional and witness-family-relative.

## 2. Frozen target families

Each of 256 seeds contains two target states.

### T1 — Adversarial Werner–Bell family

\[
\rho_W(p)=p|\Phi^+\rangle\langle\Phi^+|+(1-p)I/4,
\]

with an evenly spaced schedule over

\[
p\in[0.61,1.00]
\]

followed by independent random local unitaries.

The lower endpoint remains above the frozen negativity threshold `0.20` but enters the known region where CHSH violation need not occur. This deliberately stresses the distinction between L2 resource qualification and a particular L3 witness.

### T2 — Schmidt-pure family

\[
|\psi_\lambda\rangle=\sqrt{\lambda}|00\rangle+\sqrt{1-\lambda}|11\rangle,
\]

with an evenly spaced schedule over

\[
\lambda\in[0.05,0.50]
\]

plus random local unitaries.

## 3. Frozen adversarial mimic families

Each seed contains four separable mimics:

1. **maximal product-coherence mimic** — a locally rotated product pure state;
2. **variable-rank separable mixture** — convex mixture of 2–12 random product states;
3. **rotated classical common-cause mimic** — a diagonal correlated state followed by local unitary rotations, allowing large computational-basis off-diagonal structure while remaining separable;
4. **Werner separability-boundary mimic** — a locally rotated Werner state with `p` scheduled in `[0.30, 1/3]`.

The word "mimic" denotes an adversarial alternative within this synthetic state-space test only. It is not a claim about a real physical mechanism.

## 4. Structural diagnostic

Phase 0A-R uses only

\[
C_{\rm off}(\rho)=\|\rho-\operatorname{diag}(\rho)\|_F
\]

as a basis-dependent scalar structural diagnostic.

No estimator, bound, monotone, restriction, or certificate relation is claimed between `C_off` and the historical process-level operator quantity `Q_delta(W)`, `M_CNS`, or indefinite causal order.

## 5. Resource and witness

Resource quantity:

\[
N(\rho)=\frac{\|\rho^{T_B}\|_1-1}{2}.
\]

Frozen thresholds are unchanged from Phase 0A:

- target: `N >= 0.20`;
- mimic: `N <= 1e-9`.

Optional operational witness:

- maximal two-qubit CHSH value;
- target witness PASS condition: `S_CHSH > 2 + 1e-6`;
- mimic witness PASS condition: `S_CHSH <= 2 + 1e-6`.

G6 is a witness-family-relative gate. Failure of G6 does not imply absence of the L2 entanglement resource.

## 6. Expanded tested local-channel family

The numerical audit checks nonincrease under the following **finite tested channel family** independently on subsystem A and subsystem B:

- dephasing: `lambda = 0.25, 0.50`;
- depolarizing: `lambda = 0.10, 0.30, 0.60`;
- amplitude damping: `gamma = 0.15, 0.50, 0.85`;
- four seeded random qubit CPTP channels generated as rank-4 isometries per evaluated state.

Every output must remain a physical density matrix. The empirical claim is only **nonincrease under this frozen tested channel family**. Phase 0A-R does not claim to prove general free-operation monotonicity.

## 7. Frozen gates

| Gate | Test | Pass condition |
|---|---|---|
| G0 | physical validity | every generated state and every tested channel output is Hermitian, trace 1, PSD within `1e-10` |
| G1 | structural diagnostic insufficiency | a target and a separable coherent product both have `C_off > 0.1`, while only the target exceeds the negativity threshold |
| G2 | target resource exclusion | every target has `N >= 0.20` |
| G3 | local-basis robustness | negativity changes by at most `1e-9` over 16 frozen random local-unitary trials per state |
| G4 | tested-channel nonincrease | every tested local-channel output is physical and increases negativity by at most `1e-9` |
| G5 | adversarial mimic exclusion | every mimic has `N <= 1e-9` |
| G6 | optional CHSH witness | every target has `S_CHSH > 2+1e-6` and every mimic has `S_CHSH <= 2+1e-6` |

G0–G5 are core. G6 is optional and must not be interpreted as necessary for entanglement.

## 8. Frozen execution

- seeds: `256`;
- base seed: `20260910`;
- target Werner schedule: `[0.61, 1.00]`;
- target Schmidt schedule: `[0.05, 0.50]`;
- Werner mimic schedule: `[0.30, 1/3]`;
- local-unitary trials per state: `16`;
- random CPTP channels per state: `4`;
- environment: Python `3.12.14`, NumPy `2.5.3`, SciPy `1.18.1`.

No threshold or family may be changed after the first qualification output is observed. Any revision requires a new protocol version and preserved failed lineage.

## 9. Decision rule

### `P0AR_CORE_GENERALIZES_WITH_CHSH`

G0–G5 PASS and G6 PASS.

### `P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED`

G0–G5 PASS and G6 FAIL.

Interpretation: the resource/gate core survived the adversarial family, while the selected CHSH witness is not universal over that resource-positive target family.

### `STOP_P0AR_...`

Any G0–G5 failure. The failed gate names are appended to the machine decision.

## 10. Required outputs

- full machine-readable row table;
- gate vector;
- `g_N` resource separation margin;
- target/mimic negativity quantiles;
- target/mimic CHSH quantiles;
- minimum target-minus-mimic paired negativity margin by seed;
- maximum local-basis negativity delta;
- maximum tested-channel negativity increase;
- physical-output status;
- decision text.

## 11. Claim firewall

A Phase 0A-R PASS may support only:

> The frozen Phase 0A resource-qualification gate mechanics survived the specified adversarially varied two-qubit synthetic challenge.

It does **not** establish:

- process-level `M_CNS`;
- causal nonseparability;
- indefinite causal order;
- Quantum Switch certification;
- a new physical quantum resource;
- any biological quantum mechanism;
- xenon causality;
- quantum consciousness;
- ontology.

Phase 0B remains a separate later escalation to a genuine process representation and SDP-based causal-nonseparability qualification.