# H_QC Phase 1 — Xenon Isotope Replication
## Frozen Preregistration Protocol v1.1

**Study ID:** H_QC-P1-XIR  
**Status:** PREFLIGHT-REVISED / NO REAL-WORLD DATA YET  
**Study class:** confirmatory replication  
**Claim ceiling:** replicated xenon-isotope-dependent anesthetic phenotype only

## 0. Why v1.1 exists

A preregistration preflight Monte Carlo audit identified a design flaw in v1.0: requiring formal ±3 pp equivalence of Xe-132 vs Xe-134 with only 20 complete blocks had very low operating power even when the true difference was exactly zero. Under the frozen synthetic audit assumptions (residual SD 6 pp), that gate passed only ~5% of null-equivalent datasets and would have made an otherwise valid target replication almost impossible to classify as strong.

Because no real-world data exist yet, v1.0 is superseded before data collection. v1.1 retains ±3 pp as a **meaningful-difference threshold**, but changes G5 from a formal equivalence requirement to a pre-specified **spin-0 divergence red-flag test**. This is an audit repair, not an outcome-driven change.

## 1. Primary question

Does the previously reported xenon-isotope-dependent anesthetic phenotype replicate under a blocked, blinded design when spin-bearing isotopes are contrasted with spin-0 isotopes?

This phase does **not** test whether consciousness is quantum mechanical, whether nuclear spin is the causal mechanism, Orch OR, or any soul-related ontology.

## 2. Primary estimand

For each animal, define `Y` as the xenon concentration threshold for loss of righting reflex (LORR) under fixed 0.50% isoflurane.

Primary contrast:

`Delta_spin = mean(Y_129, Y_131) - mean(Y_132, Y_134)`

Positive values mean a higher xenon threshold in the spin-bearing isotope group.

## 3. Arms and sample

- Xe-129: nuclear spin 1/2
- Xe-131: nuclear spin 3/2
- Xe-132: spin 0
- Xe-134: spin 0

Planned confirmatory sample: **N = 80**, 20 animals per isotope, organized as 20 complete blocks.

Experimental unit must be an independent exposure run. If multiple animals share one gas circuit/chamber exposure, the chamber/run is the experimental unit and clustering must be modeled; animals sharing one exposure may not be treated as fully independent replicates.

## 4. Blocking and randomization

Use 20 complete randomized blocks. Each block contains one independent exposure run for each isotope. Isotope order within each block is generated before experimentation and concealed from outcome scorers.

Randomization must prevent isotope from being aliased with date, time, analyzer drift, operator, cylinder lot, or run order.

## 5. Blinding

- isotope code holder: unblinded, not involved in outcome scoring or confirmatory analysis;
- exposure operator: blinded where technically feasible;
- LORR/video scorer: blinded;
- statistician / confirmatory analysis: blinded until frozen output artifacts and hashes are produced.

Unblinding occurs only after confirmatory outputs are frozen.

## 6. Exposure protocol

Direct-replication target:

- fixed isoflurane: 0.50%;
- xenon staircase: +2.5 percentage points per step;
- equilibration: 15 minutes per step;
- LORR: failure to right within 10 seconds after placement supine.

For each animal:

`Y_i = (C_prev + C_loss) / 2`

where `C_prev` is the highest concentration with retained righting and `C_loss` is the first concentration producing LORR.

## 7. Primary confirmatory analysis

Frozen blocked contrast:

`Y_bi = alpha_block[b] + beta_isotope[i] + epsilon_bi`

Primary contrast:

`C = 0.5*beta_129 + 0.5*beta_131 - 0.5*beta_132 - 0.5*beta_134`

Equivalent complete-block estimator:

`d_b = (Y_129,b + Y_131,b)/2 - (Y_132,b + Y_134,b)/2`

`Delta_spin = mean_b(d_b)`

Report estimate, 95% CI, standardized effect, and raw distributions. A p-value alone is never a success criterion.

## 8. SESOI and primary gate

`SESOI = +3.0 percentage points`.

Primary replication gate G6 passes only if:

`95% CI lower bound(Delta_spin) > +3.0 pp`

## 9. Negative controls

### NC1 — spin-0 divergence red flag

Xe-132 and Xe-134 are both spin 0. Define:

`D_spin0 = mean(Y_132 - Y_134)`

A **material spin-0 divergence red flag** is triggered only when both are true:

1. `|D_spin0| > 3.0 pp`, and
2. the two-sided 95% CI for `D_spin0` excludes 0.

G5 passes when this red flag is absent.

Important: G5 PASS does **not** prove Xe-132 and Xe-134 are equivalent. It only means the study did not detect a large, statistically resolved spin-0 divergence. Formal ±3 pp equivalence is not claimed at N=20 blocks.

### NC2 — directional consistency

Both spin-bearing isotope means must exceed the pooled spin-0 mean:

- `mean(Y_129) > mean(Y_spin0)`
- `mean(Y_131) > mean(Y_spin0)`

Individual significance is not required.

### NC3 — isoflurane-only baseline control

Where operationally feasible, baseline anesthetic sensitivity without xenon must show no meaningful group imbalance attributable to allocation.

## 10. Classical leakage / implementation audit

Record per independent run at minimum:

- actual Xe concentration;
- actual isoflurane concentration;
- chamber temperature;
- O2;
- CO2;
- pressure;
- animal body mass;
- baseline body temperature;
- exposure duration;
- run order;
- block ID;
- operator ID;
- cylinder lot;
- analyzer calibration status.

A balance/audit table is mandatory. Any isotope-specific implementation drift is treated as a competing classical explanation, not adjusted away silently.

## 11. Exclusions

Only pre-specified technical or welfare exclusions are permitted.

Allowed run exclusions include analyzer failure, gas concentration validation failure, chamber control failure, isotope-code integrity failure, or endpoint data loss before ascertainment.

Forbidden post-hoc exclusions include removing observations because they are extreme, hypothesis-inconsistent, or reduce statistical significance.

Any replacement must occur while isotope identity remains blinded and must replace the same coded condition.

## 12. Gate table

| Gate | Test | Frozen pass condition |
|---|---|---|
| G0 | ethics + preregistration | approvals complete; protocol/hash frozen before data |
| G1 | isotope identity/purity | independent verification passes |
| G2 | randomization | 20 complete blocks executed or deviations declared |
| G3 | blinding | no material outcome/analysis unblinding |
| G4 | implementation balance | no major isotope-specific gas/environment leakage |
| G5 | spin-0 divergence audit | no material resolved Xe-132 vs Xe-134 divergence (>3 pp and 95% CI excluding 0) |
| G6 | primary replication | 95% CI lower bound for `Delta_spin` > +3 pp |
| G7 | directional consistency | Xe-129 and Xe-131 each above pooled spin-0 mean |
| G8 | baseline anesthetic control | no meaningful allocation-linked baseline difference |
| G9 | robustness | block-adjusted estimate retains direction and substantive size |

**G6 is the primary confirmatory gate.**

## 13. Decision rule

### STRONG REPLICATION
G0–G9 all pass.

Permitted claim: **the xenon-isotope-dependent anesthetic phenotype replicated under the frozen design.**

### CONDITIONAL REPLICATION
G6 passes but one or more of G5/G7/G8 fail.

Permitted claim: **a confirmatory spin-group signal replicated, but isotope/spin mechanism attribution remains unresolved.**

### NOT REPLICATED
The lower 95% CI bound for `Delta_spin` does not exceed +3 pp.

Permitted claim: **the preregistered confirmatory experiment did not reproduce a substantively large spin-group isotope phenotype.**

### HARD INVALID
Material protocol corruption, isotope-code failure, endpoint change after data inspection, or major uncontrolled exposure failure.

No positive or negative mechanistic inference is permitted.

## 14. Kill / stop rule

Do **not** proceed to magnetic-field or resonance mechanism discrimination if G6 fails.

A Phase 1 failure directly kills `H_Xe-rep`, not every possible quantum contribution to neurobiology.

## 15. Claim ladder lock

Even STRONG REPLICATION does not establish nuclear-spin causality, radical-pair mechanism, quantum consciousness, necessity of quantum mechanics for consciousness, Orch OR, or any new ontology.

A successful Phase 1 authorizes only the next mechanism-discrimination phase.

## 16. Preflight operating-characteristic requirements

Before real-world execution, the synthetic audit must show:

- null scenario: G6 false-positive rate near zero under the SESOI rule;
- target +7 pp scenario: useful G6 detection probability;
- weak +2 pp scenario: rarely passes G6;
- spin-0 divergence scenario: G5 catches the competing pattern at high probability;
- one-spin-isotope artifact: G7 catches the asymmetric pattern at high probability.

Synthetic simulations are design checks only and must never be reported as biological evidence.
