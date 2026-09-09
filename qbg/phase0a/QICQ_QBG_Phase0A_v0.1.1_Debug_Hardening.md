# QICQ QBG Phase 0A — v0.1.1 Debug Hardening

**Parent:** QICQ-QBG-P0A v0.1  
**Class:** implementation / reproducibility hardening only  
**Claim ceiling change:** none

## Why this patch exists

The v0.1 qualification passed, but a post-qualification code audit found two implementation-hardening gaps:

1. G4 described local free-channel monotonicity while the implementation applied the frozen channel family to subsystem A only.
2. The QBG workflow installed broad dependency ranges, so a future dependency release could change a supposedly frozen numerical qualification.

## Frozen scientific content retained

No target family, threshold, seed schedule, resource definition, mimic family, gate decision rule, or Claim Firewall is relaxed.

The v0.1 result remains historical evidence for the original frozen execution. This v0.1.1 run is a stricter reproducibility/debug qualification and does not retroactively rewrite the v0.1 artifacts.

## Debug changes

### D1 — bilateral local-channel coverage

For every frozen G4 channel, the audit now checks the channel independently on subsystem A and subsystem B.

Pass condition remains:

[
N(\Lambda_{A/B}(\rho)) - N(\rho) \le 10^{-9}.
]

### D2 — numerical environment lock

The QBG workflow is pinned to Python 3.12.14 and:

- NumPy 2.5.3
- SciPy 1.18.1

These are the versions observed in the successful v0.1 main qualification run.

### D3 — CI trigger hardening

The QBG lockfile is itself a workflow trigger path. A numerical-environment change can no longer bypass QBG CI.

## Claim Firewall

A v0.1.1 PASS still establishes only two-qubit synthetic resource-proxy gate mechanics. It does not establish causal nonseparability, a Quantum Switch, indefinite causal order, a biological quantum mechanism, consciousness, or ontology.


### D4 — free-channel output validity

G4 now treats physical output validity as a prerequisite for monotonicity.
Every frozen local channel output must remain Hermitian, unit-trace, and PSD
within the existing physical tolerance. A malformed or non-trace-preserving
would-be free operation can no longer pass merely because it lowers
negativity.
