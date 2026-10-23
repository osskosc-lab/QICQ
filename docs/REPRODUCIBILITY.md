# Reproducibility notes

## One-command re-run

`scripts/run_all.sh [LOGDIR]` runs the four frozen qualifications with exactly the CI commands
(H_QC preflight v1.1, QBG 0A, 0A-R, 0B-I). It changes no seed, threshold, or decision logic.
Use one Python 3.12.14 environment per phase, installed from that phase's `requirements-lock.txt`
(`simulations/`, `qbg/phase0a/`, `qbg/phase0ar/`, `qbg/phase0bi/`), and pass them via
`PY_SIM`, `PY_0A`, `PY_0AR`, `PY_0BI`.

`python scripts/compare_runs.py DIR_A DIR_B` compares two artifact directories, ignoring
wall-clock fields such as the 0B-I SDP `solve_time`.

## Known platform sensitivity: Phase 0A last-digit negativity values

The 0A-R spec §1, `qbg/phase0ar/manifest.json` and `BASELINE_MARGIN` in `qbg_phase0ar.py` record the
0A v0.1.1 baseline as target min negativity `0.31254751364720484` and mimic max negativity
`3.409409165475825e-16`. A 2026-10-23 box run gave `0.3125475136472048` / `3.283669267264406e-16`.

Investigation (2026-10-24):

- Same pinned environment (Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1; NumPy's bundled
  scipy-openblas 0.3.34 built with `DYNAMIC_ARCH`).
- Running the code at v0.1 (`b37f825`), v0.1.1 (`bdc3dce`) and current main on the same box gives
  the same box values, so the difference is **not** a code change.
- Forcing the OpenBLAS kernel with `OPENBLAS_CORETYPE`:

| OPENBLAS_CORETYPE | target_min_negativity | mimic_max_negativity | decision |
|---|---|---|---|
| Haswell | 0.31254751364720484 | 3.409409165475825e-16 | P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS |
| Zen | 0.31254751364720484 | 3.409409165475825e-16 | same |
| Sandybridge | 0.31254751364720484 | 3.409409165475825e-16 | same |
| SkylakeX (box auto-detect) | 0.3125475136472048 | 3.283669267264406e-16 | same |
| Nehalem / Prescott | 0.3125475136472049 | 3.2738678767362766e-16 | same |

Cause: OpenBLAS selects a CPU-specific kernel at runtime. Different floating-point summation order
changes values at ~1e-16, i.e. machine-precision level. All values stay far from every frozen
tolerance (`N >= 0.20`, mimic `N <= 1e-9`), and decisions are unchanged. The recorded baseline is
reproduced exactly with `OPENBLAS_CORETYPE=Haswell` (likely the kernel used on the GitHub Actions runner;
not verified on the runner itself).

To reproduce the recorded CI values bit-for-bit on another machine: `export OPENBLAS_CORETYPE=Haswell`.

The same sensitivity applies to 0A-R and 0B-I at the last-digit level. With `OPENBLAS_CORETYPE=Haswell`
on the box (2026-10-24), 0A-R gave `resource_separation_margin_gN = 0.20807128906249964` (box auto-detect:
`0.20807128906249944`) and some 0B-I raw values differed in trailing digits; both decisions were unchanged
(`P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED`, `P0BI_DETERMINISTIC_CNS_SDP_QUALIFIED`; OCB `R_CNS^g` printed
as `0.1715728472869511` in both). H_QC preflight outputs were byte-identical across runs.
