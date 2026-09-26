# QICQ QBG Phase 0A — v0.1.2 Reference-Mimic Gating and Manifest Consistency

**Parent:** QICQ-QBG-P0A v0.1.1 (tag `qbg-p0a-v0.1.1-frozen`, main merge commit `b9bf949`, scientific head `bdc3dce`)
**Class:** stricter gate inputs plus a provenance test
**Claim ceiling change:** none

## Why this amendment exists

A post-freeze external audit (2026-09-26) found two remaining spec/code gaps in v0.1.1:

1. Spec §3 lists deterministic reference mimics (|+><+| ⊗ |0><0|, the classical 00/11 common-cause mixture, a product mixed state, and the maximally mixed state), and spec §5 G5 requires *all* product and classical-common-cause mimics to be excluded. In v0.1 and v0.1.1 these reference mimics were computed and reported, but only the coherent-product mimic entered any gate (via G1). They were not inputs to G5 or G6.
2. `manifest.json` duplicated the code constants, but no test checked that the two agree, so they could drift silently.

## Changes

### R1 — reference mimics are G5/G6 gate inputs (stricter)

`REFERENCE_MIMICS = (fixed_order_coherent_product_mimic, classical_common_cause_mimic, product_mixed_mimic, maximally_mixed_mimic)`.

- G5 now additionally requires `N(rho_ref) <= 1e-9` for every reference mimic.
- G6 now additionally requires `S_CHSH(rho_ref) <= 2 + 1e-6` for every reference mimic.
- The summary reports `reference_mimics_gated`, `reference_mimic_max_negativity`, and `reference_mimic_max_chsh`.

The existing stochastic-mimic conditions are unchanged. Adding inputs to an all-must-pass gate can only make the gate harder to pass.

### R2 — manifest-vs-code consistency test (provenance)

New deterministic tests load `manifest.json` and assert equality with the code constants: version, seeds, base seed, Werner range, negativity threshold, all tolerances, local-unitary trials, the frozen channel list, the CHSH thresholds, the reference-mimic list, and the gate names. They also check that `manifest_v0.1.json` and `manifest_v0.1.1.json` keep the same frozen parameters. To make this testable, the channel family and trial count are now module constants (`FREE_CHANNEL_SPECS`, `LOCAL_UNITARY_TRIALS_PER_CASE`) with the same values. The numerical behaviour is unchanged.

## Frozen scientific content retained

Seeds (100 from 20260909), the Werner target family p ∈ [0.75, 1.0], the stochastic mimic families, and every threshold and tolerance are unchanged. Gate names, decision labels, and the Claim Firewall are also unchanged. `manifest_v0.1.json` and `manifest_v0.1.1.json` (byte-identical to the v0.1.1 `manifest.json`) are preserved. The v0.1 and v0.1.1 records are not rewritten.

## Pre-merge local qualification (reviewer environment: Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1)

- 16 deterministic tests: OK.
- 100-seed qualification: G0–G6 PASS; decision `P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS` (unchanged).
- `reference_mimic_max_negativity = 0.0`; `reference_mimic_max_chsh = 2.0` (classical common cause, at the classical bound and within the 1e-6 margin).
- `qualification_rows.csv` is byte-identical to the v0.1.1 run, because the per-seed rows are unchanged.
- Phase 0A-R (which imports `qbg.phase0a` primitives) run against v0.1.2: identical rows, decision `P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED`.

## Amendment log (修正履歴)

| Version | Date (JST) | Change | Direction | Rationale | CI |
|---|---|---|---|---|---|
| 0.1 | 2026-09-09 | Original freeze | — | — | 34355035990: success |
| 0.1.1 | 2026-09-09 → 2026-09-26 | Bilateral G4 plus free-channel output validity; environment lock (see the v0.1.1 record) | stricter | Spec/implementation mismatch in G4 | 34410854079 (PR), 36226660867 (main): success |
| 0.1.2 | 2026-09-26 | R1: reference mimics gated in G5/G6. R2: manifest-vs-code consistency tests. VERSION 0.1.2. Manifest lineage block. `manifest_v0.1.1.json` preserved. | stricter (R1); provenance only (R2) | Spec §3/§5 require the reference mimics to be excluded; the manifest must not drift from the code | recorded in the PR and on the tag `qbg-p0a-v0.1.2-frozen` |

## Claim Firewall

Unchanged. A v0.1.2 PASS still establishes only two-qubit synthetic resource-proxy gate mechanics. It does not establish causal nonseparability, a Quantum Switch, indefinite causal order, a biological quantum mechanism, xenon causality, consciousness, or any ontology.
