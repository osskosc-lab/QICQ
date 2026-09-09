# QICQ QBG Phase 0A

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
