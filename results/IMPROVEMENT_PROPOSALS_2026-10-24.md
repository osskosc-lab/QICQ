# Improvement proposals — 2026-10-24 (not applied)

These touch frozen protocols, manifests, CI behaviour that defines a frozen environment, or open research decisions. They require the owner's decision and, where frozen content is affected, a new protocol version with preserved lineage.

1. **Pin the BLAS kernel in CI** (`OPENBLAS_CORETYPE=Haswell` or a single-kernel BLAS build) so last-digit values are platform-independent. This changes the frozen numerical environment definition, so it should be a documented version bump, not a silent edit.
2. **0A-R baseline provenance**: `qbg/phase0ar/manifest.json` and `BASELINE_MARGIN` hard-code the v0.1.1 CI values to 17 significant digits. Consider documenting in a future 0A-R version that the baseline is platform-dependent at ~1e-16, or comparing with a stated tolerance. (Baseline is informational; no gate uses it.)
3. **H_QC design-audit unit tests**: `simulations/` has no deterministic tests analogous to the QBG phases (e.g. checking the acceptance thresholds in code match the preregistration table).
4. **0A CI path filter** includes `README.md`, so documentation-only edits re-run 0A. Harmless, but could be narrowed; left as is because the workflow file is part of the frozen 0A provenance.
5. **Determinism check in CI**: run each qualification twice and diff with `scripts/compare_runs.py`.
6. **Open branch `prereg/hqc-v1.2-predata-amendment`** (CI runs on 2026-09-26, not merged to main) appears to add an ethics statement and a citation. Decide whether to merge it; this re-run used v1.1 as on main.
