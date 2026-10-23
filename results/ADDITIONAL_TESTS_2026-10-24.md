# Additional tests — 2026-10-24 (JST)

Box env: Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1 (0B-I adds CVXPY 1.9.2, SCS 3.2.11), each from that phase's lock file.
No frozen protocol, threshold, seed, or decision logic was changed. Items marked **non-preregistered** are sensitivity checks only. They do not replace the frozen runs and carry no evidential weight.

## Summary

| Test | Result |
|---|---|
| (a) H_QC design-audit unit tests (16) | PASS |
| (b) Run-twice determinism, all 4 phases | PASS (all artifacts identical, wall-clock excluded) |
| (c) OpenBLAS kernel sweep, 7 kernels × {0A, 0A-R, 0B-I} | PASS: decisions unchanged everywhere; max deviations ≤ 3.7e-13 |
| (d1) H_QC 10,000 reps, frozen seed (non-preregistered) | 6/6 acceptance checks PASS |
| (d2) H_QC 3,000 reps, seeds 1, 2, 3 (non-preregistered) | 6/6 PASS for each seed |
| (d3) 0A / 0A-R with base seed 20261024 (non-preregistered) | same decisions |
| (d4) 0B-I single-threaded BLAS | identical to default run |

## (a) H_QC unit tests

`python -m unittest simulations.test_hqc_phase1_design_audit -v`: 16 tests OK (~28 s).
They cover:
- frozen constants (isotopes, SESOI 3.0, red-flag margin 3.0, 20 blocks, scenario list, SDs 6/2);
- hand-built datasets: a clear signal gives STRONG, a sub-SESOI effect gives NOT_REPLICATED, spin-0 divergence gives a red flag and CONDITIONAL, a one-spin artifact fails G7, zero variance is handled, wrong shape is rejected, common block shifts cancel;
- same seed gives an identical summary, and a different seed differs;
- null strong = 0 and G6 = 0;
- all G5/G6/G7/strong rates match `PREFLIGHT_AUDIT_2026-08-09.md` within its 3-dp rounding;
- all acceptance checks pass;
- CLI: small run writes outputs, non-integer `--reps` is rejected, and `--reps 0` exits non-zero.

**Limitation:** `--reps 0` and negative values are rejected only because the script crashes, not because of explicit validation. Adding validation would edit the frozen script, so it is listed as a proposal instead.

## (b) Determinism

`scripts/run_all.sh` was run twice, then `python scripts/compare_runs.py run1 run2`. All 10 artifact files were `same`, exit 0.

## (c) OpenBLAS kernel sweep

`scripts/blas_sweep.sh <ref> <out>` uses kernels Haswell, SkylakeX, Sandybridge, Zen, Nehalem, Prescott and Core2. The reference is the default (auto-detected) box run, and deviations are measured with `scripts/max_numeric_deviation.py`.

| Kernel | 0A max dev (rows / summary) | 0A-R max dev (rows / summary) | 0B-I max dev | Decisions |
|---|---|---|---|---|
| Haswell | 1.998e-15 / 4.441e-16 | 2.442e-15 / 4.441e-16 | 1.822e-13 | all same |
| SkylakeX | 0 / 0 | 0 / 0 | 1.822e-13 | all same |
| Sandybridge | 1.998e-15 / 4.441e-16 | 2.665e-15 / 4.441e-16 | 3.735e-13 | all same |
| Zen | 1.998e-15 / 4.441e-16 | 2.442e-15 / 4.441e-16 | 1.822e-13 | all same |
| Nehalem | 1.998e-15 / 4.441e-16 | 3.109e-15 / 4.441e-16 | 3.735e-13 | all same |
| Prescott | 1.998e-15 / 4.441e-16 | 3.109e-15 / 4.441e-16 | 5.639e-17 | all same |
| Core2 | 1.998e-15 / 4.441e-16 | 3.109e-15 / 4.441e-16 | 5.639e-17 | all same |

The 0B-I largest deviations are in SCS solver residual diagnostics (`scs_res_dual`), not in the gate quantities. OCB `R_CNS^g` printed as `0.1715728472869511` under all kernels.

**Observation:** forcing `SkylakeX`, the kernel the box auto-detects, still changes 0B-I residual diagnostics by 1.8e-13 relative to the auto run, while 0A and 0A-R are bit-identical. A repeated forced-SkylakeX run is self-identical, so the run is deterministic per configuration. The likely cause is that the environment variable also affects another BLAS consumer (for example SciPy or SCS linkage); this was not investigated further.

## (d) Cheap robustness checks (non-preregistered)

- **d1 H_QC, `--reps 10000 --seed 20260809`** (G6/G5/G7/strong):

  | Scenario | G6 | G5 | G7 | Strong |
  |---|---|---|---|---|
  | null | 0.000 | 0.951 | 0.307 | 0.000 |
  | target | 0.811 | 0.949 | 1.000 | 0.769 |
  | spin0_confound | 0.809 | 0.020 | 1.000 | 0.016 |
  | one_spin_artifact | 0.806 | 0.951 | 0.112 | 0.105 |
  | weak_effect | 0.004 | 0.953 | 0.808 | 0.004 |

  All 6 checks PASS.
- **d2 H_QC, 3,000 reps, seeds 1/2/3:** target strong was 0.768 / 0.766 / 0.769, null G6 0.000 for every seed, and all checks PASS for every seed. The frozen-seed values are not an unusually favourable draw.
- **d3 base seed 20261024:**
  - 0A: target_min_negativity 0.3132801948470328, mimic_max_negativity 3.984060192684342e-16, target_min_chsh 2.124262642583555, decision `P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS`.
  - 0A-R: gN 0.20807128906249953, G6 FAIL, decision `P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED`. gN barely changes because the target and mimic parameters follow fixed evenly spaced schedules (the minimum is set by the Werner endpoint p = 0.61); only the local unitaries and random mixtures depend on the seed.
- **d4 0B-I with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`:** max deviation 0, same decision.

## Interpretation limits

These tests check implementation, determinism and numerical stability of the frozen gate mechanics only. The sensitivity runs use parameters that were not preregistered and must not be cited as qualification results. Nothing here is biological, physical-mechanism, or consciousness evidence. The BLAS sweep was run on one CPU (box Intel Xeon) using forced kernels, not on real hardware of each kind.
