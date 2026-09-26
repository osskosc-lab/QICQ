# H_QC Phase 1 — Xenon Isotope Replication
## Preregistration Protocol v1.2 (pre-data amendment)

**Study ID:** H_QC-P1-XIR  
**Status:** DRAFT / NO REAL-WORLD DATA YET — **NOT FROZEN**. This document becomes FROZEN only through the §17 procedure: ethics approval number inserted, hashes recorded, tag created, external registration made.  
**Supersedes:** v1.1 (`preregistration/H_QC_Phase1_Xenon_Isotope_Replication_v1.1.md`, retained unchanged except for a superseded note)  
**Study class:** confirmatory replication  
**Claim ceiling:** replicated xenon-isotope-dependent anesthetic phenotype only  
**Open PI decisions:** items marked **PLACEHOLDER** or **PI DECISION REQUIRED** must be resolved before freeze. They are collected in §18.

## 0. Why v1.2 exists

v1.2 is a **pre-data** amendment. No real-world data exist. It fixes gaps found in the 2026-09-26 readiness review of v1.1:

1. There was no ethics statement (§0b).
2. The +7 pp target effect and the 6 pp residual SD had no cited source (§1b).
3. The primary CI method was ambiguous: two estimators were described (§7).
4. G9 duplicated the primary estimate (`mean(d_b) > 3`), so it was not a real robustness gate (§12, §7.3).
5. G1, G4 and G8 had no numeric criteria (§12).
6. The decision rule did not cover every gate outcome, and there was no rule for incomplete blocks (§13).
7. The operating-characteristic requirements were qualitative (§16).
8. Sensitivity to the SD assumption was not examined (§16b).
9. There was no firewall between H_QC and QBG in the other direction (§15b).
10. There was no explicit freeze and registration procedure (§17).

The following are unchanged from v1.1: the primary estimand, the SESOI (+3.0 pp), G5 (spin-0 divergence red flag), G6 (primary gate), G7, the arms, the exposure protocol, the blinding roles, the exclusion policy, the claim ceiling, and the kill rule. Direction of change: **stricter** (G9 becomes a genuine gate) and **more fully specified**. No gate is loosened.

### 0a. Amendment log

| Version | Date (JST) | Change | Direction | Real-world data at time of change | Rationale |
|---|---|---|---|---|---|
| v1.0 | ≤2026-08-09 | Initial draft; G5 = formal ±3 pp TOST equivalence of Xe-132 vs Xe-134 | — | none | — |
| v1.1 | 2026-08-09 | G5 changed to a spin-0 divergence red flag (`|D_spin0| > 3 pp` and 95% CI excludes 0) | redesign (preflight falsified v1.0 G5: ~5% pass under true equivalence) | none | `simulations/PREFLIGHT_AUDIT_2026-08-09.md` |
| v1.2 | 2026-09-26 | Ethics statement; Li 2018 derivation; primary CI fixed as paired t (df = B−1); genuine G9 (additive and covariate-adjusted models); G1/G4/G8 numeric placeholders; complete decision rule and incomplete-block rule; numeric OC thresholds; SD sensitivity with a PI decision; reciprocal firewall; freeze procedure | stricter / specification | none | readiness review 2026-09-26; `simulations/PREFLIGHT_AUDIT_2026-09-26.md` |

## 0b. Ethics Statement

All procedures require prospective approval by the responsible animal-ethics body **before any animal is ordered or exposed**. No data may be collected under this protocol until the fields below are filled in and the protocol is frozen (§17).

- Approving body (IACUC / institutional animal care and use committee / national equivalent): **PLACEHOLDER — [committee name, institution, country]**
- Approval / protocol number: **PLACEHOLDER — [approval number]**
- Approval date and expiry: **PLACEHOLDER — [YYYY-MM-DD / YYYY-MM-DD]**
- Applicable regulations and guidelines: **PLACEHOLDER — [e.g. national animal-welfare law; institutional guidelines]**. Reporting will follow ARRIVE 2.0.
- Species / strain / sex / age / supplier: **PLACEHOLDER — PI to confirm**. For a direct replication of Li et al. 2018: C57BL/6 male mice, 7 weeks old.
- Housing, acclimatization and husbandry: **PLACEHOLDER**
- Humane endpoints and monitoring during and after exposure: **PLACEHOLDER — [criteria; who monitors; action taken]**
- Anesthetic and gas safety (xenon/isoflurane scavenging; hypoxia/hypercapnia limits): **PLACEHOLDER — [limits]**. These must match the G4 tolerances in §12.
- Euthanasia method at end of study (if applicable): **PLACEHOLDER**
- 3Rs justification for N (see §3 and §16b): **PLACEHOLDER — PI to confirm after the §16b decision**

A welfare-driven exclusion is always allowed (§11). It is recorded while the isotope code is still blinded.

## 1. Primary question

Does the previously reported xenon-isotope-dependent anesthetic phenotype replicate under a blocked, blinded design when spin-bearing isotopes are compared with spin-0 isotopes?

This phase does **not** test whether consciousness is quantum mechanical, whether nuclear spin is the causal mechanism, Orch OR, or any soul-related ontology.

## 1b. Source study, target effect and SD assumption

**Primary source.** Li N, Lu D, Yang L, Tao H, Xu Y, Wang C, Fu L, Liu H, Chummum Y, Zhang S. *Nuclear Spin Attenuates the Anesthetic Potency of Xenon Isotopes in Mice: Implications for the Mechanisms of Anesthesia and Consciousness.* **Anesthesiology** 2018;129(2):271–277. **DOI: 10.1097/ALN.0000000000002226**. PMID 29642079. Editorial comment: Anesthesiology 2018;129(2):228–231, DOI 10.1097/ALN.0000000000002273.

**Reported values** (abstract). The study used 80 male C57BL/6 mice (7 weeks old) in four groups, so about 20 per group. LORR ED50 of xenon combined with 0.50% isoflurane:

| Isotope | Nuclear spin | LORR ED50 (%, reported as mean ± ·) |
|---|---|---|
| Xe-132 | 0 | 15 ± 4 |
| Xe-134 | 0 | 16 ± 5 |
| Xe-131 | 3/2 | 22 ± 5 |
| Xe-129 | 1/2 | 23 ± 7 |

**Derivation of the +7 pp target.** Using the §2 contrast: spin-bearing mean = (22 + 23)/2 = 22.5; spin-0 mean = (15 + 16)/2 = 15.5; so `Delta_spin` = **+7.0 pp**. This is the effect size the source study reports. Published effects tend to be inflated (winner's curse), so the true effect may be smaller. The SESOI (+3 pp) is the confirmatory criterion, not +7 pp.

**SD assumption and the SD/SEM caveat.** The design audit assumes a residual (within-block) SD of **6 pp** and a block SD of 2 pp. This number is **not reported as such** in the source:

- The abstract does not say whether "±" is an SD or an SEM. The full text was not accessible when v1.2 was drafted.
- *If "±" is an SD:* the pooled RMS of the four values is sqrt((4² + 5² + 5² + 7²)/4) ≈ **5.36 pp** and the maximum is 7 pp. The 6 pp assumption is then plausible but not conservative; 7 pp is the natural upper sensitivity value (§16b).
- *If "±" is an SEM:* with about 20 animals per group, the per-animal SD would be about √20 ≈ 4.5 times larger (roughly 18–31 pp). The planned N would then be grossly underpowered and the design would have to be reconsidered before freeze.
- The reported values are group ED50 summaries, not per-animal thresholds. The residual SD of per-run staircase thresholds in a blocked design is a different quantity, and the 2.5 pp staircase discretization adds variance (≈0.72 pp SD).

**Action required before freeze.** The PI must confirm the meaning of "±" from the full text, or from the authors, and record the answer here: **PLACEHOLDER — ["±" = SD / SEM; source]**. The choice in §16b depends on it.

## 2. Primary estimand

For each independent exposure run, `Y` is the xenon concentration threshold for loss of righting reflex (LORR) under fixed 0.50% isoflurane.

Primary contrast:

`Delta_spin = mean(Y_129, Y_131) - mean(Y_132, Y_134)`

A positive value means a higher xenon threshold in the spin-bearing isotope group.

## 3. Arms and sample

- Xe-129: nuclear spin 1/2
- Xe-131: nuclear spin 3/2
- Xe-132: spin 0
- Xe-134: spin 0

**Planned confirmatory sample: PI DECISION REQUIRED (§16b).**

- **Option A:** fix **B = 22** complete blocks (N = 88) now.
- **Option B:** plan **B = 20** complete blocks (N = 80), with the pre-specified blinded SD re-estimation rule in §16b (sample size can only increase, up to a cap).

v1.1 specified B = 20 (N = 80). The CI design audit still runs at B = 20 / SD 6 as the reference configuration.

The experimental unit must be an independent exposure run. If several animals share one gas circuit/chamber exposure, the chamber/run is the experimental unit and the clustering must be modeled. Animals sharing one exposure may not be treated as fully independent replicates.

## 4. Blocking and randomization

Use B complete randomized blocks. Each block contains one independent exposure run per isotope. The isotope order within each block is generated before experimentation, hash-frozen (§17), and concealed from outcome scorers.

Randomization must prevent isotope from being aliased with date, time, analyzer drift, operator, cylinder lot, or run order.

## 5. Blinding

- Isotope code holder: unblinded; not involved in outcome scoring or confirmatory analysis.
- Exposure operator: blinded where technically feasible.
- LORR/video scorer: blinded.
- Statistician / confirmatory analysis: blinded until frozen output artifacts and hashes are produced.

Unblinding occurs only after the confirmatory outputs are frozen. Any §16b interim SD re-estimation (Option B only) is performed **without** isotope labels.

## 6. Exposure protocol

Direct-replication target:

- fixed isoflurane: 0.50%;
- xenon staircase: +2.5 percentage points per step;
- equilibration: 15 minutes per step;
- LORR: failure to right within 10 seconds after being placed supine.

For each run:

`Y_i = (C_prev + C_loss) / 2`

where `C_prev` is the highest concentration at which righting was retained and `C_loss` is the first concentration that produced LORR.

## 7. Confirmatory analysis

### 7.1 Primary estimator and CI (G6) — frozen

Complete-block difference:

`d_b = (Y_129,b + Y_131,b)/2 - (Y_132,b + Y_134,b)/2`, for each complete block b = 1..B

`Delta_spin = mean_b(d_b)`

**Primary 95% CI:** the one-sample (paired) t interval on the B values `d_b`, with **df = B − 1**:

`Delta_spin ± t_{0.975, B-1} · SD(d_b)/sqrt(B)`

This is the only interval used for G6. Only complete blocks enter the primary analysis (§13.3).

### 7.2 Secondary: additive two-way model

`Y_bi = mu + alpha_block[b] + beta_isotope[i] + epsilon_bi`, fitted by OLS, with contrast `C = 0.5*beta_129 + 0.5*beta_131 - 0.5*beta_132 - 0.5*beta_134`. The CI uses the model residual variance with df = n − rank(X). With complete blocks, df = 3(B − 1), and the point estimate equals `Delta_spin`.

This model is **secondary**. It feeds G9 and can use runs from incomplete blocks (§13.3). It never replaces the §7.1 interval for G6.

### 7.3 Secondary: covariate-adjusted additive model

This is the §7.2 model plus pre-specified run-level covariates: **body mass (standardized), baseline body temperature (standardized), and run position within the block**. **PI to confirm the covariate list before freeze** (§18). The covariates are fixed before any data are seen. No covariate selection is allowed after data inspection.

The design audit simulates these covariates as independent of isotope and with zero true effect. That is the conservative case, where adjustment only costs degrees of freedom.

### 7.4 Reporting

Report for every model: the estimate, 95% CI, standardized effect and raw distributions. A p-value alone is never a success criterion.

## 8. SESOI and primary gate

`SESOI = +3.0 percentage points`.

Primary replication gate G6 passes only if:

`95% CI lower bound(Delta_spin) > +3.0 pp`, using the §7.1 paired t interval.

## 9. Negative controls

### NC1 — spin-0 divergence red flag (G5; unchanged from v1.1)

`D_spin0 = mean_b(Y_132,b - Y_134,b)`. A **material spin-0 divergence red flag** is triggered only when both of the following hold:

1. `|D_spin0| > 3.0 pp`, and
2. the two-sided 95% paired t CI for `D_spin0` (df = B − 1) excludes 0.

G5 passes when the red flag is absent. A G5 PASS does **not** prove that Xe-132 and Xe-134 are equivalent. Formal ±3 pp equivalence is not claimed.

### NC2 — directional consistency (G7; unchanged)

Both spin-bearing isotope means must exceed the pooled spin-0 mean: `mean(Y_129) > mean(Y_spin0)` and `mean(Y_131) > mean(Y_spin0)`. Individual significance is not required.

### NC3 — isoflurane-only baseline control (G8)

Baseline anesthetic sensitivity without xenon must show no meaningful allocation-linked imbalance. The numeric criterion is in §12 (**PLACEHOLDER**).

## 10. Classical leakage / implementation audit

Record, per independent run, at minimum:

- actual Xe concentration
- actual isoflurane concentration
- chamber temperature
- O2
- CO2
- pressure
- animal body mass
- baseline body temperature
- exposure duration
- run order
- block ID
- operator ID
- cylinder lot
- analyzer calibration status

A balance/audit table is mandatory. Any isotope-specific implementation drift is treated as a competing classical explanation (G4). It is never adjusted away silently.

## 11. Exclusions

Only pre-specified technical or welfare exclusions are permitted.

Allowed run exclusions: analyzer failure, gas-concentration validation failure (outside the G4 tolerances), chamber control failure, isotope-code integrity failure, a welfare/humane endpoint (§0b), or endpoint data lost before ascertainment.

Forbidden post-hoc exclusions: removing observations because they are extreme, inconsistent with the hypothesis, or reduce statistical significance.

Any replacement must happen while the isotope identity is still blinded, and must replace the same coded condition within the same block (§13.3).

## 12. Gate table

| Gate | Test | Pass condition (v1.2) |
|---|---|---|
| G0 | ethics + preregistration | ethics approval number recorded in §0b; §17 freeze completed (hashes, tag, external registration ID) **before** the first animal exposure |
| G1 | isotope identity/purity | Each cylinder lot has independent verification of isotopic enrichment ≥ **PLACEHOLDER — PI must specify before freeze: [X]% target isotope** by **PLACEHOLDER — [method, e.g. isotope-ratio mass spectrometry; certificate + independent lab]**, with cross-isotope contamination ≤ **PLACEHOLDER — [Y]%**. Chemical impurities (O2/N2/other) ≤ **PLACEHOLDER — [Z] ppm**. |
| G2 | randomization / completeness | Blocks executed as randomized; number of complete blocks B_complete ≥ ceil(0.9 × B_planned) (§13.3); every deviation declared |
| G3 | blinding | no material outcome/analysis unblinding (any unblinding before output freeze counts as material) |
| G4 | implementation balance | (a) every run is within tolerance: delivered Xe within ±**PLACEHOLDER — PI must specify before freeze: [a] pp** of the nominal staircase step; isoflurane 0.50% ± **PLACEHOLDER [b]** % (absolute); chamber temperature ± **PLACEHOLDER [c] °C**; O2 ≥ **PLACEHOLDER [d]%**; CO2 ≤ **PLACEHOLDER [e]%**; pressure ± **PLACEHOLDER [f]**. Out-of-tolerance runs are excluded under §11 and replaced under §13.3. (b) **Balance:** for each recorded implementation variable, the between-isotope-group difference (spin-bearing vs spin-0, and each isotope vs the pooled mean) stays within the **PLACEHOLDER — PI must specify before freeze: [margin per variable, e.g. absolute units or standardized mean difference]** margin. |
| G5 | spin-0 divergence audit | no material resolved Xe-132 vs Xe-134 divergence (`|D_spin0|` > 3 pp **and** 95% CI excluding 0) |
| G6 | primary replication | §7.1 paired t 95% CI lower bound for `Delta_spin` > +3 pp |
| G7 | directional consistency | Xe-129 and Xe-131 each above the pooled spin-0 mean |
| G8 | baseline anesthetic control | isoflurane-only baseline (e.g. LORR ED50/threshold without xenon) shows no allocation-linked difference beyond **PLACEHOLDER — PI must specify before freeze: margin ±[m] (units) and test [e.g. 90% CI of the spin-bearing vs spin-0 baseline difference lies within ±m]** |
| G9 | robustness (**genuine**, v1.2) | **both** (i) the §7.2 additive model and (ii) the §7.3 covariate-adjusted model give a primary-contrast estimate **> +3 pp** with a 95% CI lower bound **> 0** |

**G6 is the primary confirmatory gate.** The G1/G4/G8 numbers are experimental facts: which enrichment is achievable, which analyzer tolerances are realistic, and which margins matter. Only the PI can set them. They are placeholders here and **must** be filled in before freeze. A protocol with any PLACEHOLDER remaining cannot be FROZEN (§17).

## 13. Decision rule (complete)

### 13.1 Order of evaluation

1. **HARD INVALID** if any of the following holds: G0 fails (data collected before freeze/approval); G1 fails for any lot used in the confirmatory data; G3 fails (material unblinding); G4(b) fails (isotope-specific implementation imbalance, i.e. an unexcluded competing classical explanation); B_complete < ceil(0.75 × B_planned); endpoint change after data inspection; isotope-code failure; major uncontrolled exposure failure.
2. Otherwise, if G6 **fails**, the result is **NOT REPLICATED**. This holds whatever G5/G7/G8/G9 show.
3. Otherwise (G6 passes): **STRONG REPLICATION** if G2, G5, G7, G8 and G9 all pass. **CONDITIONAL REPLICATION** if any of G2, G5, G7, G8 or G9 fails.

### 13.2 Outcome table and permitted claims

| Outcome | Condition | Permitted claim |
|---|---|---|
| STRONG REPLICATION | 13.1 step 3, all of G2/G5/G7/G8/G9 pass (and G0/G1/G3/G4 pass by step 1) | **the xenon-isotope-dependent anesthetic phenotype replicated under the frozen design.** |
| CONDITIONAL REPLICATION | G6 passes; ≥1 of G2/G5/G7/G8/G9 fails | **a confirmatory spin-group signal replicated, but isotope/spin attribution, or its robustness, remains unresolved.** The failed gates must be named. |
| NOT REPLICATED | G6 fails (step 2) | **the preregistered confirmatory experiment did not reproduce a substantively large spin-group isotope phenotype.** This includes the case where the CI excludes 0 but not +3 pp. That case may be described only as "a smaller-than-SESOI difference cannot be excluded or confirmed". |
| HARD INVALID | step 1 | No positive or negative mechanistic inference is permitted. |

v1.1 did not assign an outcome when G6 passed but G9 failed, when G2 failed, or when G1/G3/G4 failed. v1.2 covers these cases explicitly.

### 13.3 Incomplete-block rule

- **Replacement first:** a run excluded under §11 is replaced by a new run of the **same coded condition in the same block**, scheduled while blinding is intact, if feasible within **PLACEHOLDER — PI to confirm: [time window, e.g. the same experimental week]**.
- **Primary analysis (G5, G6, G7):** complete blocks only (all four isotopes present).
- **Secondary models (G9):** all valid runs, including those from incomplete blocks (OLS handles unbalanced cells).
- **Thresholds.** These are proposed defaults and the PI may revise them before freeze:
  - B_complete ≥ ceil(0.9 × B_planned): G2 passes (if no other deviation);
  - ceil(0.75 × B_planned) ≤ B_complete < ceil(0.9 × B_planned): G2 fails, so the best possible outcome is CONDITIONAL;
  - B_complete < ceil(0.75 × B_planned): HARD INVALID.
- For reference: with B_planned = 20 the 90% floor is 18. At SD 6 and 18 complete blocks, the audit gives target G6 = 0.743 and strong = 0.703 (`simulations/PREFLIGHT_AUDIT_2026-09-26.md`).
- Blocks may not be dropped or added for any reason other than §11 or the §16b rule (Option B only).

## 14. Kill / stop rule

Do **not** proceed to magnetic-field or resonance mechanism discrimination if G6 fails, or if the outcome is HARD INVALID.

A Phase 1 failure directly kills `H_Xe-rep`. It does not kill every possible quantum contribution to neurobiology.

## 15. Claim ladder lock

Even STRONG REPLICATION does not establish nuclear-spin causality, a radical-pair mechanism, quantum consciousness, the necessity of quantum mechanics for consciousness, Orch OR, or any new ontology.

A successful Phase 1 authorizes only the next mechanism-discrimination phase.

## 15b. Reciprocal firewall (H_QC ↔ QBG)

The QBG line (`qbg/`) is synthetic methodological infrastructure. In both directions:

- No QBG result (Phase 0A, 0A-R, 0B-I or later) raises or lowers the evidential status of H_QC. None may be cited as prior support, used to set H_QC priors, or used to change H_QC thresholds.
- No H_QC result (positive, negative or invalid) may be used to change QBG gates, thresholds, free sets or claim ceilings, or be cited as validating any QBG quantity.
- Neither line may be combined with the other to support a quantum-consciousness claim. Each line's claim ceiling applies independently.

## 16. Preflight operating-characteristic requirements (numeric)

Before real-world execution, the synthetic audit (`simulations/hqc_phase1_design_audit.py`, seed 20260809, 3000 reps per scenario) must meet **all** of the following at the chosen design (B, SD assumption):

| Check | Scenario (true effects, pp: 129/131/132/134) | Requirement |
|---|---|---|
| null false positive | null (0/0/0/0) | G6 pass rate ≤ **1%** |
| target detection | target (7/7/0/0) | G6 pass rate ≥ **70%** |
| target strong classification | target | STRONG (G5, G6, G7, G9) rate ≥ **65%** |
| weak-effect rejection | weak (2/2/0/0) | G6 pass rate ≤ **5%** |
| spin-0 confound detection | spin0_confound (7/7/−4/4) | G5 pass rate ≤ **10%** |
| one-spin artifact detection | one_spin_artifact (16/−2/0/0) | G7 pass rate ≤ **25%** |

The script exits with an error if any check fails (sensitivity runs use `--allow-check-failure`). Results at B = 20 / SD 6: all six pass (target G6 0.812, strong 0.771; null G6 0.000). See `simulations/PREFLIGHT_AUDIT_2026-09-26.md`.

Synthetic simulations are design checks only and must never be reported as biological evidence.

## 16b. SD sensitivity and sample-size decision — **PI DECISION REQUIRED**

Audit results (seed 20260809, 3000 reps per scenario, block SD 2 pp):

| Design | Residual SD | Target G6 | Target strong | All 6 checks |
|---|---:|---:|---:|---|
| B = 20 (N = 80) | 6 pp | 0.812 | 0.771 | PASS |
| B = 20 (N = 80) | **7 pp** | **0.680** | **0.645** | **FAIL** (target detection < 70%, strong < 65%) |
| B = 22 (N = 88) | 7 pp | 0.730 | 0.702 | PASS |
| B = 22 (N = 88) | 6 pp | 0.850 | 0.818 | PASS |

So the v1.1 design (B = 20) meets its own OC requirements only if SD ≤ ~6 pp. The source does not establish that (§1b). The PI must choose **one** of the two options below before freeze. This protocol deliberately does **not** choose.

**Option A — fix N now at B = 22 complete blocks (N = 88).**
- Meets all §16 checks up to SD 7 pp.
- Costs 8 more animals and 8 more runs than B = 20. There are no interim looks.
- If "±" in the source turns out to be an SEM (§1b), even B = 22 is inadequate and the design must be revisited.

**Option B — B = 20 with a blinded SD re-estimation rule.**
- After **PLACEHOLDER — [k, e.g. 10]** complete blocks, a statistician who is not the code holder estimates the residual SD **without isotope labels**. The estimate uses the pooled within-block variance of the four runs per block, `s²_blind`, adjusted for the assumed target pattern (Kieser–Friede-type adjusted one-sample estimator): `s²_adj = s²_blind − Delta_target²/3`, with `Delta_target = 7 pp`.
- Rule: if `s_adj ≤ 6.0 pp`, keep B = 20. If `6.0 < s_adj ≤ 7.0 pp`, increase to B = 22. If `s_adj > 7.0 pp`, increase to **PLACEHOLDER — [B_max, e.g. 24]** and record that the OC requirements may not be met.
- B can never decrease. No effect estimate is computed or looked at. The decision and `s_adj` are logged before blinded data collection continues.
- **Before freeze, the operating characteristics of this rule must themselves be audited by simulation** (type I error, target power, strong-classification rate). This audit has **not** been done yet. It would require an extension of the design-audit script.

**PI decision record:** **PLACEHOLDER — [Option A / Option B; date; rationale]**. §3, §4 and §0b (3Rs) must then be updated to match.

## 17. Freeze & Registration procedure (ordered)

Each step starts only after the previous one is complete. Steps 2, 3, 5 and 6 are real-world actions by the PI/owner. They cannot be done or simulated by automation.

1. **Merge v1.2 with CI green.** All PLACEHOLDER / PI DECISION items (§18) are resolved in a follow-up commit, the design audit passes in CI at the chosen design, and the PR is merged into `main` with a merge commit.
2. **Ethics / IACUC approval** is obtained for the protocol as merged (§0b).
3. **Insert the approval number** and approval details into §0b and set the Status header to **FROZEN**. Commit.
4. **Compute SHA-256 hashes** of:
   - (a) this preregistration file (as frozen);
   - (b) `simulations/hqc_phase1_design_audit.py` and the final confirmatory analysis script;
   - (c) `simulations/requirements-lock.txt`;
   - (d) the randomization schedule. The schedule is stored so the code holder keeps custody: the hash is public, the contents stay concealed.

   Record the hashes, file paths, commit SHA and date in `preregistration/FREEZE.md`. Create an annotated git tag, e.g. `hqc-p1-prereg-v1.2-frozen`, on that commit.
5. **External registration** on OSF Registries or AsPredicted (**PLACEHOLDER — platform**), attaching or linking the frozen file and the FREEZE.md hashes. Record the registration ID/URL and timestamp in `FREEZE.md` (in a follow-up commit; the frozen files themselves are not modified).
6. **Data collection** begins only after steps 1–5. The first-exposure date must be after the external registration timestamp.

Any change after step 3 requires a new version (v1.3+) with an amendment-log entry that states whether any real-world data existed at the time of the change.

## 18. Open PI decisions (must be resolved before freeze)

1. **Sample size (§16b):** Option A (B = 22, N = 88) or Option B (B = 20 plus blinded SD re-estimation; also k, B_max, and an OC audit of the rule).
2. **Meaning of "±" in Li et al. 2018 (§1b):** SD or SEM. If SEM, the design must be revisited.
3. **G1:** enrichment threshold, verification method, contamination and chemical-impurity limits.
4. **G4:** per-run tolerances (Xe, isoflurane, temperature, O2, CO2, pressure) and balance margins per implementation variable.
5. **G8:** baseline-control margin and test.
6. **Covariate list** for the G9 covariate-adjusted model (§7.3).
7. **Incomplete-block thresholds and replacement window** (§13.3): confirm or revise the proposed 90% / 75% floors.
8. **Ethics details (§0b):** approving body, approval number and dates, humane endpoints, gas-safety limits, and animal strain/sex/age/supplier.
9. **External registration platform** (§17 step 5): OSF Registries or AsPredicted.
