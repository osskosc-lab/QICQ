# QICQ QBG Phase 0A

Current implementation: **v0.1.2** (lineage: v0.1 → v0.1.1 debug hardening → v0.1.2 reference-mimic gating and manifest consistency).

Minimal synthetic qualification for the **Quantum Behavior Qualification Gate (QBG)**.

This line exists to test the gate mechanics before any full process-matrix / causal-nonseparability implementation is attempted.

## What Phase 0A does

It checks whether a frozen two-qubit resource proxy can:

- reject coherence-only as a sufficient quantum-resource criterion;
- separate a Bell/Werner target from separable/classical mimics;
- remain invariant under local basis rotations;
- remain non-increasing under a frozen family of local free channels;
- survive 100 deterministic stochastic seeds;
- optionally recover a CHSH operational witness.

## What Phase 0A does not do

It does **not** test or establish:

- causal nonseparability;
- indefinite causal order;
- quantum-controlled causal order;
- a Quantum Switch;
- a biological quantum mechanism;
- consciousness.

## Run locally

```bash
python qbg/phase0a/test_qbg_phase0a.py
python qbg/phase0a/qbg_phase0a.py \
  --seeds 100 \
  --base-seed 20260909 \
  --outdir artifacts/qbg_phase0a
```

Outputs:

- `artifacts/qbg_phase0a/qualification_summary.json`
- `artifacts/qbg_phase0a/qualification_rows.csv`
- `artifacts/qbg_phase0a/decision.txt`

## Frozen files

- `QICQ_QBG_Phase0A_v0.1.md` — scientific/claim specification
- `manifest.json` — machine-readable thresholds and gate freeze
- `qbg_phase0a.py` — qualification implementation
- `test_qbg_phase0a.py` — deterministic unit tests

## Phase 0B firewall

Phase 0B is not automatically a positive-mechanism phase.

If Phase 0A core gates pass, Phase 0B is authorized only as a **process-matrix falsification phase**. It must freeze genuine process validity constraints, the causally separable free set, a certified CNS/QCO metric or witness, adversarial fixed-order+coherence mimics, and the operational access assumptions before execution.

## v0.1.1 debug hardening

- preserves the v0.1 claim ceiling and frozen thresholds;
- extends G4 to apply every frozen local channel independently to subsystem A and subsystem B;
- freezes the successful CI numerical environment via `requirements-lock.txt` and Python 3.12.14;
- preserves the original v0.1 manifest as `manifest_v0.1.json`.

See `QICQ_QBG_Phase0A_v0.1.1_Debug_Hardening.md`.

## v0.1.2 reference-mimic gating and manifest consistency

- the deterministic reference mimics of spec §3 are now gate inputs to G5 (negativity) and G6 (CHSH), which is stricter;
- `manifest.json` is checked against the code constants by deterministic unit tests;
- seeds, thresholds, families, decision labels and claim ceiling are unchanged;
- `manifest_v0.1.json` and `manifest_v0.1.1.json` are preserved.

See `QICQ_QBG_Phase0A_v0.1.2_Reference_Mimics_Manifest.md`.
