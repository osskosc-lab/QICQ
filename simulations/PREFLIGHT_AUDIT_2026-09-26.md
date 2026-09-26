# H_QC Phase 1 preflight design audit — 2026-09-26 (protocol v1.2 draft)

## Status

**Synthetic design audit only. No biological data.** These outputs test gate mechanics and operating characteristics. They are not evidence that a xenon isotope effect exists in vivo.

This audit accompanies the pre-data amendment `preregistration/H_QC_Phase1_Xenon_Isotope_Replication_v1.2.md`, which is DRAFT and not frozen. It supplements the earlier audit `PREFLIGHT_AUDIT_2026-08-09.md`, which stays unchanged.

## What changed in the audit script (v1.1 → v1.2)

- **G9 is now genuine.** Two models must each give a primary-contrast estimate > +3 pp with a 95% CI lower bound > 0:
  - the additive two-way OLS model (block + isotope; df = 3(B−1));
  - the covariate-adjusted additive model (covariates: body mass z, baseline body temperature z, run position in block; simulated independent of isotope with zero true effect; df = 3(B−1) − 3).
  
  v1.1 G9 was `mean(d_b) > 3`, which duplicated the primary estimate.
- The primary G6 CI is unchanged: paired t on `d_b`, df = B − 1.
- New options: `--residual-sd`, `--n-blocks`, and `--allow-check-failure` (sensitivity runs only).
- With the default settings, the simulated outcome stream is identical to v1.1. Covariates come from an independent RNG stream. The G5, G6 and G7 rates at SD 6 / B = 20 therefore reproduce the 2026-08-09 audit exactly.
- New unit tests: `simulations/test_hqc_phase1_design_audit.py`.

## Environment

- Python 3.12.14, numpy 2.5.3, scipy 1.18.1 (`simulations/requirements-lock.txt`)
- seed 20260809; 3000 repetitions per scenario; block SD 2 pp; SESOI +3 pp; spin-0 red-flag margin 3 pp
- run date: 2026-09-26 (JST), on the analysis box; the CI workflow reruns the SD 6 / B = 20 configuration and the two SD 7 sensitivity runs
- SHA-256 at time of run (informational; the freeze hashes are computed under prereg §17):
```
e5aa3fb708c2cca78206f106ad0a168d15a551cbde396ff6cfa2b781e1595d55  simulations/hqc_phase1_design_audit.py
6e69ffe6f7841e5d8aea3f05a4bf77c60055d3b0717fcccbb31fd19647e07b7b  simulations/requirements-lock.txt
```

## Summary

| Design | Residual SD | null G6 | target G6 | target strong | weak G6 | spin0_confound G5 | one_spin G7 | target G9 | all 6 checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B=20 (N=80) | 6 pp | 0.000 | 0.812 | 0.771 | 0.006 | 0.017 | 0.107 | 0.996 | PASS |
| B=20 (N=80) | 7 pp | 0.000 | 0.680 | 0.645 | 0.007 | 0.070 | 0.150 | 0.989 | **FAIL** |
| B=22 (N=88) | 7 pp | 0.000 | 0.730 | 0.702 | 0.005 | 0.056 | 0.135 | 0.993 | PASS |
| B=22 (N=88) | 6 pp | 0.000 | 0.850 | 0.818 | 0.003 | 0.013 | 0.099 | 0.999 | PASS |
| B=18 (N=72) | 6 pp | 0.000 | 0.743 | 0.703 | 0.004 | 0.029 | 0.121 | 0.996 | PASS |

Required thresholds (prereg v1.2 §16): null G6 ≤ 1%; target G6 ≥ 70%; target strong ≥ 65%; weak G6 ≤ 5%; spin0_confound G5 ≤ 10%; one_spin G7 ≤ 25%.

## Interpretation

- At the v1.1 design (B = 20) with the frozen SD 6 assumption, all six checks pass. The stricter v1.2 G9 barely changes the strong-classification rate (target 0.771, same as v1.1), because G9 almost always passes when G6 passes.
- At **SD 7, B = 20 fails two checks**: target G6 = 0.680 < 0.70 and target strong = 0.645 < 0.65. Run without `--allow-check-failure`, the script exits with code 1 ("Preflight design audit FAILED").
- **B = 22 restores all checks at SD 7** (target G6 0.730, strong 0.702).
- Which design to adopt — Option A (fix B = 22) or Option B (B = 20 with blinded SD re-estimation) — is a **PI DECISION** (prereg v1.2 §16b). This audit does not make it. Option B would also need its own simulation audit of the re-estimation rule before freeze; that audit has not been performed.
- Everything here depends on SD being ≈6–7 pp. If "±" in Li et al. 2018 is an SEM (§1b), the per-animal SD would be far larger and none of these designs would be adequate.

## Raw outputs

### B=20 (N=80), SD 6 — reference / CI configuration

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 6.0 pp | blocks = 20 (N = 80) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.949 | G7=0.297 | G9=0.011 | strong=0.000
            target | true Δ= 7.00 | G6=0.812 | G5=0.948 | G7=1.000 | G9=0.996 | strong=0.771
    spin0_confound | true Δ= 7.00 | G6=0.813 | G5=0.017 | G7=1.000 | G9=0.999 | strong=0.014
 one_spin_artifact | true Δ= 7.00 | G6=0.818 | G5=0.949 | G7=0.107 | G9=0.996 | strong=0.101
       weak_effect | true Δ= 2.00 | G6=0.006 | G5=0.953 | G7=0.819 | G9=0.210 | strong=0.006
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  PASS  target_primary_detection_ge_70pct
  PASS  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd6_b20/operating_characteristics.csv
Wrote <outdir>/sd6_b20/audit_summary.json
exit_code=0
```

### B=20 (N=80), SD 7 — sensitivity

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 --residual-sd 7 --allow-check-failure
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 7.0 pp | blocks = 20 (N = 80) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.947 | G7=0.297 | G9=0.017 | strong=0.000
            target | true Δ= 7.00 | G6=0.680 | G5=0.946 | G7=1.000 | G9=0.989 | strong=0.645
    spin0_confound | true Δ= 7.00 | G6=0.689 | G5=0.070 | G7=1.000 | G9=0.987 | strong=0.048
 one_spin_artifact | true Δ= 7.00 | G6=0.694 | G5=0.947 | G7=0.150 | G9=0.988 | strong=0.138
       weak_effect | true Δ= 2.00 | G6=0.007 | G5=0.950 | G7=0.765 | G9=0.203 | strong=0.007
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  FAIL  target_primary_detection_ge_70pct
  FAIL  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd7_b20/operating_characteristics.csv
Wrote <outdir>/sd7_b20/audit_summary.json
NOTE: acceptance checks FAILED under these sensitivity settings (--allow-check-failure set; exit 0).
exit_code=0
```

### B=22 (N=88), SD 7 — Option A check

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 --residual-sd 7 --n-blocks 22 --allow-check-failure
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 7.0 pp | blocks = 22 (N = 88) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.947 | G7=0.308 | G9=0.014 | strong=0.000
            target | true Δ= 7.00 | G6=0.730 | G5=0.960 | G7=1.000 | G9=0.993 | strong=0.702
    spin0_confound | true Δ= 7.00 | G6=0.722 | G5=0.056 | G7=1.000 | G9=0.993 | strong=0.042
 one_spin_artifact | true Δ= 7.00 | G6=0.724 | G5=0.951 | G7=0.135 | G9=0.994 | strong=0.125
       weak_effect | true Δ= 2.00 | G6=0.005 | G5=0.953 | G7=0.777 | G9=0.209 | strong=0.005
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  PASS  target_primary_detection_ge_70pct
  PASS  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd7_b22/operating_characteristics.csv
Wrote <outdir>/sd7_b22/audit_summary.json
exit_code=0
```

### B=22 (N=88), SD 6 — supplementary

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 --residual-sd 6 --n-blocks 22 --allow-check-failure
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 6.0 pp | blocks = 22 (N = 88) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.949 | G7=0.308 | G9=0.006 | strong=0.000
            target | true Δ= 7.00 | G6=0.850 | G5=0.962 | G7=1.000 | G9=0.999 | strong=0.818
    spin0_confound | true Δ= 7.00 | G6=0.843 | G5=0.013 | G7=1.000 | G9=1.000 | strong=0.010
 one_spin_artifact | true Δ= 7.00 | G6=0.844 | G5=0.952 | G7=0.099 | G9=1.000 | strong=0.093
       weak_effect | true Δ= 2.00 | G6=0.003 | G5=0.955 | G7=0.831 | G9=0.194 | strong=0.003
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  PASS  target_primary_detection_ge_70pct
  PASS  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd6_b22/operating_characteristics.csv
Wrote <outdir>/sd6_b22/audit_summary.json
exit_code=0
```

### B=18 (N=72), SD 6 — supplementary (incomplete-block floor, §13.3)

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 --residual-sd 6 --n-blocks 18 --allow-check-failure
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 6.0 pp | blocks = 18 (N = 72) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.952 | G7=0.308 | G9=0.013 | strong=0.000
            target | true Δ= 7.00 | G6=0.743 | G5=0.947 | G7=1.000 | G9=0.996 | strong=0.703
    spin0_confound | true Δ= 7.00 | G6=0.758 | G5=0.029 | G7=1.000 | G9=0.996 | strong=0.024
 one_spin_artifact | true Δ= 7.00 | G6=0.762 | G5=0.954 | G7=0.121 | G9=0.996 | strong=0.113
       weak_effect | true Δ= 2.00 | G6=0.004 | G5=0.951 | G7=0.793 | G9=0.199 | strong=0.004
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  PASS  target_primary_detection_ge_70pct
  PASS  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd6_b18/operating_characteristics.csv
Wrote <outdir>/sd6_b18/audit_summary.json
exit_code=0
```

### SD 7, B = 20 without `--allow-check-failure` (the gating behaviour used in CI)

```
$ python simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 --residual-sd 7
H_QC Phase 1 synthetic design audit v1.2
WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE
residual SD = 7.0 pp | blocks = 20 (N = 80) | reps = 3000 | seed = 20260809
              null | true Δ= 0.00 | G6=0.000 | G5=0.947 | G7=0.297 | G9=0.017 | strong=0.000
            target | true Δ= 7.00 | G6=0.680 | G5=0.946 | G7=1.000 | G9=0.989 | strong=0.645
    spin0_confound | true Δ= 7.00 | G6=0.689 | G5=0.070 | G7=1.000 | G9=0.987 | strong=0.048
 one_spin_artifact | true Δ= 7.00 | G6=0.694 | G5=0.947 | G7=0.150 | G9=0.988 | strong=0.138
       weak_effect | true Δ= 2.00 | G6=0.007 | G5=0.950 | G7=0.765 | G9=0.203 | strong=0.007
Acceptance checks:
  PASS  null_primary_false_positive_le_1pct
  FAIL  target_primary_detection_ge_70pct
  FAIL  target_strong_classification_ge_65pct
  PASS  weak_effect_primary_pass_le_5pct
  PASS  spin0_confound_g5_pass_le_10pct
  PASS  one_spin_artifact_g7_pass_le_25pct
Wrote <outdir>/sd7_b20_strict/operating_characteristics.csv
Wrote <outdir>/sd7_b20_strict/audit_summary.json
Preflight design audit FAILED: revise before real-world data collection.
exit_code=1
```

### Unit tests

```
$ python simulations/test_hqc_phase1_design_audit.py
test_additive_estimate_equals_paired_mean_for_complete_blocks (__main__.HQCDesignAuditV12Tests.test_additive_estimate_equals_paired_mean_for_complete_blocks) ... ok
test_covariates_shape_and_run_position_balance (__main__.HQCDesignAuditV12Tests.test_covariates_shape_and_run_position_balance) ... ok
test_default_outcome_stream_unchanged_from_v11 (__main__.HQCDesignAuditV12Tests.test_default_outcome_stream_unchanged_from_v11) ... ok
test_g9_fails_below_sesoi_estimate (__main__.HQCDesignAuditV12Tests.test_g9_fails_below_sesoi_estimate) ... ok
test_g9_fails_when_ci_includes_zero (__main__.HQCDesignAuditV12Tests.test_g9_fails_when_ci_includes_zero) ... ok
test_g9_requires_both_models (__main__.HQCDesignAuditV12Tests.test_g9_requires_both_models) ... ok
test_primary_ci_is_paired_t_with_b_minus_1_df (__main__.HQCDesignAuditV12Tests.test_primary_ci_is_paired_t_with_b_minus_1_df) ... ok
test_protocol_version (__main__.HQCDesignAuditV12Tests.test_protocol_version) ... ok
test_strong_requires_g9 (__main__.HQCDesignAuditV12Tests.test_strong_requires_g9) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.012s

OK
exit_code=0
```

## Frozen consequence

No real-world data may be collected until prereg v1.2 is completed (PI decisions), merged, ethics-approved, frozen, hashed and externally registered (prereg v1.2 §17).
