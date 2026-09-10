# QBG Phase 0B-I v0.1

Deterministic qualification of the process-matrix causal-nonseparability SDP layer.

## Scope

This directory is the first genuine process-matrix stage after the state-level Phase 0A / 0A-R proxy work.

It freezes and tests:

- bipartite qubit process convention `A_I ⊗ A_O ⊗ B_I ⊗ B_O`;
- process validity constraints;
- definite-order cones;
- a causally separable cone decomposition;
- numerical generalized causal robustness `R_CNS^g`;
- free-case calibration;
- an off-diagonal definite-order mimic;
- a known deterministic OCB CNS reference;
- party-swap representation robustness;
- tested free-mixing nonincrease;
- SCS primal/dual/gap certification.

## Explicit exclusions

Phase 0B-I does not execute the Quantum Switch and does not define a B7 particular operational witness. Those are held behind successful qualification of B0–B6.

The SDP dual information is treated as numerical certification support, not silently promoted into an independent operational witness.

## Run

```bash
pip install -r qbg/phase0bi/requirements-lock.txt
python -m unittest qbg.phase0bi.test_qbg_phase0bi -v
python -m qbg.phase0bi.qbg_phase0bi --outdir artifacts/qbg_phase0bi
```

## Claim firewall

A PASS qualifies only the frozen deterministic synthetic process-matrix certification machinery. It is not evidence of an experimental Quantum Switch, indefinite causal order in nature, biology, xenon causality, or quantum consciousness.
