# H_QC Phase 1 preflight falsification audit — 2026-08-09

## Status

**Synthetic design audit only. No biological data.**

The first preregistration draft (v1.0) failed its own preflight logic: formal ±3 pp TOST equivalence for Xe-132 vs Xe-134 with only 20 complete blocks was severely underpowered. Under the synthetic true-equivalence scenario, the gate passed only about 5% of runs, reducing strong-classification probability for an otherwise valid +7 pp target effect to about 3–4%.

This was treated as a design falsification and repaired before any real-world data collection.

## v1.1 repair

G5 was changed from “prove ±3 pp equivalence” to a conservative **spin-0 divergence red flag**:

- compute `D_spin0 = mean(Y_132 - Y_134)`;
- trigger the red flag only if `|D_spin0| > 3 pp` **and** its two-sided 95% CI excludes 0;
- G5 PASS means only “no large resolved spin-0 divergence detected”; it does not claim equivalence.

## Fixed-seed preflight operating characteristics

Monte Carlo configuration used for the preflight check:

- seed: 20260809
- repetitions: 3000 per scenario
- blocks: 20
- residual SD: 6 pp
- common block SD: 2 pp
- primary SESOI: +3 pp

Approximate fixed-seed results from the v1.1 logic:

| Scenario | True primary contrast | G5 pass | G6 pass | G7 pass | Strong statistical-core classification |
|---|---:|---:|---:|---:|---:|
| null | 0 pp | 0.949 | 0.000 | 0.297 | 0.000 |
| target | +7 pp | 0.948 | 0.812 | 1.000 | 0.771 |
| spin0 confound | +7 pp average, but Xe-132/Xe-134 differ by 8 pp | 0.017 | 0.813 | 1.000 | 0.014 |
| one-spin artifact | +7 pp average, driven asymmetrically | 0.949 | 0.818 | 0.107 | 0.101 |
| weak effect | +2 pp | 0.953 | 0.006 | 0.819 | 0.006 |

Interpretation:

- the SESOI-based primary gate rejects the null and +2 pp weak-effect scenarios;
- the target +7 pp scenario has useful detection probability at N=80;
- G5 catches the deliberately introduced spin-0 divergence in ~98% of simulations;
- G7 catches the deliberately asymmetric one-spin artifact in ~89% of simulations;
- the corrected combined gate no longer makes a true target replication nearly impossible.

## Frozen consequence

No magnetic-field, resonance, radical-pair, or consciousness-mechanism phase may begin unless real-world Phase 1 passes the preregistered primary replication gate.

These Monte Carlo results validate gate behavior only. They are not evidence that a xenon isotope effect exists in vivo.
