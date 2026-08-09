# H_QC Phase 1 — Xenon Isotope Replication
## Frozen Preregistration Protocol v1.0

**Study ID:** H_QC-P1-XIR  
**Status:** DESIGN FROZEN / NO REAL-WORLD DATA YET  
**Study class:** confirmatory replication  
**Claim ceiling:** replicated xenon-isotope-dependent anesthetic phenotype only

## 1. Primary question

Does the previously reported xenon-isotope-dependent anesthetic phenotype replicate under a blocked, blinded design when spin-bearing isotopes are contrasted with spin-0 isotopes?

This phase does **not** test whether consciousness is quantum mechanical, whether nuclear spin is the causal mechanism, Orch OR, or any soul-related ontology.

## 2. Primary estimand

For each animal, define `Y` as the xenon concentration threshold for loss of righting reflex (LORR) under fixed 0.50% isoflurane.

Primary contrast:

`Delta_spin = mean(Y_129, Y_131) - mean(Y_132, Y_134)`

Positive values mean a higher xenon threshold in the spin-bearing isotope group.

## 3. Arms

- Xe-129: nuclear spin 1/2
- Xe-131: nuclear spin 3/2
- Xe-132: spin 0
- Xe-134: spin 0

Planned confirmatory sample: **N = 80**, 20 animals per isotope.

Experimental unit must be an independent exposure run. If multiple animals share one gas circuit/chamber exposure, the chamber/run is the experimental unit and the analysis must account for clustering; animals sharing a single exposure may not be treated as fully independent replicates.

## 4. Blocking and randomization

Use 20 complete randomized blocks. Each block contains one independent exposure run for each isotope. Isotope order within each block is generated before experimentation and concealed from outcome scorers.

Randomization must prevent isotope from being aliased with date, time, analyzer drift, operator, cylinder lot, or run order.

## 5. Blinding

- isotope code holder: unblinded, not involved in scoring or confirmatory analysis;
- exposure operator: blinded where technically feasible;
- LORR scorer / video scorer: blinded;
- statistician / confirmatory analysis: blinded until frozen outputs and hashes are produced.

Unblinding occurs only after confirmatory analysis artifacts are frozen.

## 6. Exposure protocol

Direct-replication target:

- fixed isoflurane: 0.50%;
- xenon staircase: increments of 2.5 percentage points;
- equilibration: 15 minutes per step;
- LORR operational definition: failure to right within 10 seconds after placement supine.

For each animal:

`Y_i = (C_prev + C_loss) / 2`

where `C_prev` is the highest xenon concentration at which righting is retained and `C_loss` is the first concentration at which LORR occurs.

## 7. Primary confirmatory analysis

Frozen model:

`Y_bi = alpha_block[b] + beta_isotope[i] + epsilon_bi`

Primary pre-specified contrast:

`C = 0.5*beta_129 + 0.5*beta_131 - 0.5*beta_132 - 0.5*beta_134`

Report:

- raw group distributions;
- estimate of `Delta_spin`;
- 95% confidence interval;
- standardized effect;
- block-adjusted estimate.

A p-value alone is never a success criterion.

## 8. Smallest effect size of interest

`SESOI = +3.0 percentage points`.

Primary replication gate requires the lower bound of the 95% CI for `Delta_spin` to exceed +3.0 pp.

## 9. Negative controls

### NC1 — spin-0 isotope equivalence

Xe-132 and Xe-134 are both spin 0.

Equivalence margin:

`-3.0 pp <= mean(Y_132)-mean(Y_134) <= +3.0 pp`

Two one-sided tests (TOST) or an equivalent pre-specified CI criterion must be used.

### NC2 — directional consistency

Both spin-bearing isotope means must lie above the pooled spin-0 mean:

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

Allowed run exclusions include:

- analyzer failure;
- gas concentration validation failure;
- chamber control failure;
- isotope-code integrity failure;
- endpoint video/data loss before ascertainment.

Forbidden post-hoc exclusions include:

- outcome is too high/low;
- outcome is an outlier relative to its isotope group;
- observation weakens the hypothesis;
- deletion improves significance.

Any replacement must occur while isotope identity remains blinded and must replace the same coded condition.

## 12. Gate table

| Gate | Test | Frozen pass condition |
|---|---|---|
| G0 | ethics + preregistration | approvals complete; protocol/hash frozen before data |
| G1 | isotope identity/purity | independent verification passes |
| G2 | randomization | 20 complete blocks executed or deviations fully declared |
| G3 | blinding | no material outcome/analysis unblinding |
| G4 | implementation balance | no major isotope-specific gas/environment leakage |
| G5 | spin-0 negative control | Xe-132 vs Xe-134 equivalent within ±3 pp |
| G6 | primary replication | 95% CI lower bound for `Delta_spin` > +3 pp |
| G7 | directional consistency | Xe-129 and Xe-131 each above pooled spin-0 mean |
| G8 | baseline anesthetic control | no meaningful allocation-linked baseline difference |
| G9 | robustness | block-adjusted estimate retains direction and substantive size |

**G6 is the primary confirmatory gate.**

## 13. Decision rule

### STRONG REPLICATION
All G0–G9 pass.

Permitted claim: **the xenon-isotope-dependent anesthetic phenotype replicated under the frozen design.**

### CONDITIONAL REPLICATION
G6 passes but one or more of G5/G7/G8 fail.

Permitted claim: **a signal replicated, but isotope/spin mechanism attribution remains unresolved.**

### NOT REPLICATED
The lower 95% CI bound for `Delta_spin` does not exceed +3 pp.

Permitted claim: **the preregistered confirmatory experiment did not reproduce a substantively large spin-group isotope phenotype.**

### HARD INVALID
Material protocol corruption, isotope-code failure, confirmatory endpoint change after data inspection, or major uncontrolled exposure failure.

No positive or negative mechanistic inference is permitted.

## 14. Kill / stop rule

Do **not** proceed to magnetic-field or resonance mechanism discrimination if the primary replication gate G6 fails.

A Phase 1 failure directly kills `H_Xe-rep`, not every possible quantum contribution to neurobiology.

## 15. Claim ladder lock

Even a strong Phase 1 replication does **not** establish:

- nuclear-spin causality;
- a radical-pair mechanism;
- a quantum mechanism of consciousness;
- necessity of quantum mechanics for consciousness;
- Orch OR;
- any new ontology.

A successful Phase 1 authorizes only the next mechanism-discrimination phase.

## 16. Computational design audit

Before real-world data are accepted, the repository simulation must demonstrate that the frozen gates behave sensibly under at least:

1. null effect;
2. target replication effect;
3. spin-0 mass/isotope confound;
4. one-spin-isotope-only artifact;
5. block/run drift.

Synthetic simulations are design checks only and must never be reported as biological evidence.
