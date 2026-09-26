# QBG Phase 0A-R — Adversarial Generalization Challenge

Phase 0A-R is the next falsification stage after the frozen Phase 0A v0.1.1 proxy qualification.

It does **not** move QICQ into process-matrix claims. Instead, it challenges whether the Phase 0A gate semantics survive a broader, pre-frozen adversarial envelope of two-qubit target and separable mimic families.

## Frozen execution

```bash
python -m unittest qbg.phase0ar.test_qbg_phase0ar -v
python qbg/phase0ar/qbg_phase0ar.py \
  --seeds 256 \
  --base-seed 20260910 \
  --outdir artifacts/qbg_phase0ar
```

## Primary metric

```text
resource_separation_margin_gN
= min(target negativity) - max(mimic negativity)
```

Frozen pass floor: `0.20 - 1e-9`.

## Core interpretation

G0–G5 are core qualification gates. G6 is an optional, witness-family-relative CHSH gate.

A G6 failure with G0–G5 passing is a valid scientific outcome:

```text
P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED
```

It means the resource-level qualification survives while the selected CHSH witness is not universal over the adversarial resource-positive target family.

## Claim firewall

A PASS here supports only synthetic two-qubit gate-mechanics generalization under the frozen adversarial envelope. It does not establish process-level `M_CNS`, causal nonseparability, indefinite causal order, the Quantum Switch, a physical quantum mechanism, biology, or consciousness.

See `QICQ_QBG_Phase0AR_v0.1.md` and `manifest.json` for the frozen protocol.