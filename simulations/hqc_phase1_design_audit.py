#!/usr/bin/env python3
"""H_QC Phase 1 preregistration design audit v1.2.

Synthetic Monte Carlo only. This script tests whether the frozen gate logic
behaves as intended under positive and adversarial scenarios. It is NOT a
biological experiment and MUST NOT be interpreted as evidence for a xenon,
quantum, anesthesia, or consciousness mechanism.

v1.2 changes (pre-data amendment, see
preregistration/H_QC_Phase1_Xenon_Isotope_Replication_v1.2.md):

* G9 is now a genuine robustness gate: the additive two-way model
  (block + isotope) AND the covariate-adjusted additive model must each give a
  primary-contrast estimate > +3 pp with a 95% CI lower bound > 0.
  (v1.1 G9 was only ``mean(d_b) > 3``, which duplicated the primary estimate.)
* The primary CI is unchanged: paired t on d_b with df = B - 1.
* ``--residual-sd`` / ``--n-blocks`` allow the pre-specified SD sensitivity
  runs (v1.2 section 16b). Defaults (SD 6, 20 blocks) reproduce the v1.1
  simulated outcomes exactly; covariates are drawn from an independent RNG
  stream so the outcome stream is unchanged.
* ``--allow-check-failure`` reports failing acceptance checks without a
  non-zero exit, for sensitivity runs only. CI uses the default invocation.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from scipy import stats

ISOTOPES = (129, 131, 132, 134)
SESOI = 3.0
SPIN0_RED_FLAG_MARGIN = 3.0
N_BLOCKS = 20
PROTOCOL_VERSION = "1.2"
G9_ESTIMATE_MIN = 3.0  # pp; estimate must exceed SESOI in both robustness models
G9_CI_LOW_MIN = 0.0    # pp; 95% CI lower bound must exceed 0 in both models
# Pre-specified covariates for the G9 covariate-adjusted model (PI to confirm
# the list before freeze). Simulated here as independent of isotope and with
# zero true effect on the outcome, i.e. adjustment only costs degrees of freedom.
COVARIATES = ("body_mass_z", "baseline_body_temp_z", "run_position_in_block")
COVARIATE_STREAM = 1  # SeedSequence spawn key for the covariate RNG


@dataclass(frozen=True)
class Scenario:
    name: str
    effects: Dict[int, float]
    residual_sd: float = 6.0
    block_sd: float = 2.0
    description: str = ""


SCENARIOS = {
    "null": Scenario(
        "null", {129: 0.0, 131: 0.0, 132: 0.0, 134: 0.0},
        description="No isotope effect. G6 should almost never pass.",
    ),
    "target": Scenario(
        "target", {129: 7.0, 131: 7.0, 132: 0.0, 134: 0.0},
        description="Symmetric +7 pp spin-bearing replication signal.",
    ),
    "spin0_confound": Scenario(
        "spin0_confound", {129: 7.0, 131: 7.0, 132: -4.0, 134: 4.0},
        description="Primary contrast remains positive but the two spin-0 isotopes diverge by 8 pp; G5 should flag it.",
    ),
    "one_spin_artifact": Scenario(
        "one_spin_artifact", {129: 16.0, 131: -2.0, 132: 0.0, 134: 0.0},
        description="Average primary contrast can look positive but only one spin-bearing isotope drives it; G7 should fail often.",
    ),
    "weak_effect": Scenario(
        "weak_effect", {129: 2.0, 131: 2.0, 132: 0.0, 134: 0.0},
        description="Nonzero but below the +3 pp SESOI; G6 should rarely license replication.",
    ),
}


def t_interval(values: np.ndarray, confidence: float) -> Tuple[float, float, float]:
    values = np.asarray(values, dtype=float)
    n = len(values)
    mean = float(np.mean(values))
    se = float(stats.sem(values))
    if se == 0.0:
        return mean, mean, mean
    alpha = 1.0 - confidence
    crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=n - 1))
    return mean, mean - crit * se, mean + crit * se


def simulate_dataset(rng: np.random.Generator, scenario: Scenario, n_blocks: int = N_BLOCKS) -> np.ndarray:
    """Return shape (blocks, isotopes) in ISOTOPES order."""
    y = np.zeros((n_blocks, len(ISOTOPES)), dtype=float)
    block_effects = rng.normal(0.0, scenario.block_sd, size=n_blocks)
    for b in range(n_blocks):
        for j, iso in enumerate(ISOTOPES):
            y[b, j] = (
                20.0
                + block_effects[b]
                + scenario.effects[iso]
                + rng.normal(0.0, scenario.residual_sd)
            )
    return y


def simulate_covariates(rng: np.random.Generator, n_blocks: int) -> np.ndarray:
    """Return shape (blocks, isotopes, len(COVARIATES)).

    body mass and baseline temperature: standardized, independent of isotope;
    run position: randomized order 0..3 within each block, centered.
    """
    n_iso = len(ISOTOPES)
    cov = np.zeros((n_blocks, n_iso, len(COVARIATES)), dtype=float)
    cov[:, :, 0] = rng.normal(0.0, 1.0, size=(n_blocks, n_iso))
    cov[:, :, 1] = rng.normal(0.0, 1.0, size=(n_blocks, n_iso))
    for b in range(n_blocks):
        cov[b, :, 2] = rng.permutation(n_iso) - (n_iso - 1) / 2.0
    return cov


def additive_design(n_blocks: int) -> np.ndarray:
    """Intercept + (B-1) block dummies + isotope dummies (Xe-129 reference).

    Rows are block-major: row = b * 4 + j with j indexing ISOTOPES.
    """
    n_iso = len(ISOTOPES)
    n = n_blocks * n_iso
    x = np.zeros((n, 1 + (n_blocks - 1) + (n_iso - 1)), dtype=float)
    x[:, 0] = 1.0
    for b in range(n_blocks):
        for j in range(n_iso):
            r = b * n_iso + j
            if b > 0:
                x[r, b] = 1.0
            if j > 0:
                x[r, n_blocks - 1 + j] = 1.0
    return x


def primary_contrast_vector(n_columns: int, n_blocks: int) -> np.ndarray:
    """C = 0.5*b129 + 0.5*b131 - 0.5*b132 - 0.5*b134 with b129 = 0 (reference)."""
    c = np.zeros(n_columns, dtype=float)
    base = n_blocks  # column index of the Xe-131 dummy
    c[base + 0] = 0.5   # Xe-131
    c[base + 1] = -0.5  # Xe-132
    c[base + 2] = -0.5  # Xe-134
    return c


def ols_contrast(y: np.ndarray, x: np.ndarray, c: np.ndarray, confidence: float = 0.95) -> Tuple[float, float, float, int]:
    """OLS estimate of c'beta with a t-based CI (df = n - rank(X))."""
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    df = int(len(y) - rank)
    sigma2 = float(resid @ resid) / df
    xtx_inv = np.linalg.pinv(x.T @ x)
    est = float(c @ beta)
    se = float(np.sqrt(sigma2 * float(c @ xtx_inv @ c)))
    crit = float(stats.t.ppf(1.0 - (1.0 - confidence) / 2.0, df=df))
    return est, est - crit * se, est + crit * se, df


def analyze_dataset(y: np.ndarray, covariates: np.ndarray | None = None) -> Dict[str, object]:
    """Apply the v1.2 frozen gate logic to one complete-block dataset.

    y: shape (blocks, 4) in ISOTOPES order.
    covariates: shape (blocks, 4, k) or None. If None, the covariate-adjusted
    G9 model cannot be evaluated and G9 fails (it is a required component).
    """
    n_blocks = y.shape[0]
    # Primary complete-block contrast (paired t on d_b, df = B - 1);
    # common block shifts cancel.
    spin = (y[:, 0] + y[:, 1]) / 2.0
    spin0 = (y[:, 2] + y[:, 3]) / 2.0
    d = spin - spin0
    delta, l95, u95 = t_interval(d, 0.95)

    # v1.1 G5: divergence RED FLAG, not formal equivalence.
    # v1.0 required a ±3 pp TOST equivalence result at n=20 blocks and was
    # rejected by preflight because it passed only ~5% even when the true
    # Xe-132 vs Xe-134 difference was exactly zero.
    e = y[:, 2] - y[:, 3]
    e_mean, e_l95, e_u95 = t_interval(e, 0.95)
    spin0_resolved_nonzero = (e_l95 > 0.0) or (e_u95 < 0.0)
    spin0_material = abs(e_mean) > SPIN0_RED_FLAG_MARGIN
    spin0_red_flag = spin0_resolved_nonzero and spin0_material
    g5 = not spin0_red_flag

    means = {str(iso): float(np.mean(y[:, j])) for j, iso in enumerate(ISOTOPES)}
    pooled_spin0 = (means["132"] + means["134"]) / 2.0
    g7 = (means["129"] > pooled_spin0) and (means["131"] > pooled_spin0)

    g6 = l95 > SESOI

    # v1.2 G9: genuine robustness gate. Both the additive two-way model
    # (block + isotope) and the covariate-adjusted additive model must give an
    # estimate > +3 pp and a 95% CI lower bound > 0.
    y_flat = y.reshape(-1)
    x_add = additive_design(n_blocks)
    c_add = primary_contrast_vector(x_add.shape[1], n_blocks)
    add_est, add_l95, add_u95, add_df = ols_contrast(y_flat, x_add, c_add)
    g9_additive = (add_est > G9_ESTIMATE_MIN) and (add_l95 > G9_CI_LOW_MIN)
    if covariates is not None:
        z = covariates.reshape(n_blocks * len(ISOTOPES), -1)
        x_cov = np.hstack([x_add, z])
        c_cov = np.concatenate([c_add, np.zeros(z.shape[1])])
        cov_est, cov_l95, cov_u95, cov_df = ols_contrast(y_flat, x_cov, c_cov)
        g9_covariate = (cov_est > G9_ESTIMATE_MIN) and (cov_l95 > G9_CI_LOW_MIN)
    else:
        cov_est = cov_l95 = cov_u95 = float("nan")
        cov_df = 0
        g9_covariate = False
    g9 = g9_additive and g9_covariate

    if g6 and g5 and g7 and g9:
        decision = "STRONG_REPLICATION_STATISTICAL_CORE"
    elif g6:
        decision = "CONDITIONAL_SIGNAL"
    else:
        decision = "NOT_REPLICATED"

    return {
        "delta_spin": delta,
        "ci95_low": l95,
        "ci95_high": u95,
        "spin0_diff_132_minus_134": e_mean,
        "spin0_ci95_low": e_l95,
        "spin0_ci95_high": e_u95,
        "spin0_red_flag": bool(spin0_red_flag),
        "G5_spin0_no_red_flag": bool(g5),
        "G6_primary": bool(g6),
        "G7_directional_consistency": bool(g7),
        "additive_estimate": add_est,
        "additive_ci95_low": add_l95,
        "additive_ci95_high": add_u95,
        "additive_df": add_df,
        "covariate_adjusted_estimate": cov_est,
        "covariate_adjusted_ci95_low": cov_l95,
        "covariate_adjusted_ci95_high": cov_u95,
        "covariate_adjusted_df": cov_df,
        "G9_additive": bool(g9_additive),
        "G9_covariate_adjusted": bool(g9_covariate),
        "G9_robustness": bool(g9),
        "decision": decision,
        **{f"mean_{iso}": means[str(iso)] for iso in ISOTOPES},
    }


def audit_scenario(
    rng: np.random.Generator,
    scenario: Scenario,
    reps: int,
    n_blocks: int = N_BLOCKS,
    cov_rng: np.random.Generator | None = None,
) -> Dict[str, object]:
    if cov_rng is None:
        cov_rng = np.random.default_rng(0)
    rows = []
    for _ in range(reps):
        y = simulate_dataset(rng, scenario, n_blocks)
        cov = simulate_covariates(cov_rng, n_blocks)
        rows.append(analyze_dataset(y, cov))

    def rate(key: str) -> float:
        return float(np.mean([bool(r[key]) for r in rows]))

    decisions = [r["decision"] for r in rows]
    deltas = np.array([r["delta_spin"] for r in rows], dtype=float)

    return {
        "scenario": scenario.name,
        "description": scenario.description,
        "reps": reps,
        "n_blocks": n_blocks,
        "residual_sd": scenario.residual_sd,
        "block_sd": scenario.block_sd,
        "true_spin_contrast": (
            (scenario.effects[129] + scenario.effects[131]) / 2.0
            - (scenario.effects[132] + scenario.effects[134]) / 2.0
        ),
        "mean_estimated_delta": float(np.mean(deltas)),
        "sd_estimated_delta": float(np.std(deltas, ddof=1)),
        "G5_pass_rate": rate("G5_spin0_no_red_flag"),
        "G6_pass_rate": rate("G6_primary"),
        "G7_pass_rate": rate("G7_directional_consistency"),
        "G9_pass_rate": rate("G9_robustness"),
        "G9_additive_pass_rate": rate("G9_additive"),
        "G9_covariate_adjusted_pass_rate": rate("G9_covariate_adjusted"),
        "strong_replication_rate": float(np.mean([d == "STRONG_REPLICATION_STATISTICAL_CORE" for d in decisions])),
        "conditional_signal_rate": float(np.mean([d == "CONDITIONAL_SIGNAL" for d in decisions])),
        "not_replicated_rate": float(np.mean([d == "NOT_REPLICATED" for d in decisions])),
    }


def validate_operating_characteristics(summary_by_name: Dict[str, Dict[str, object]]) -> Dict[str, bool]:
    """Pre-data design acceptance checks. Failure means redesign, not science."""
    checks = {
        "null_primary_false_positive_le_1pct": summary_by_name["null"]["G6_pass_rate"] <= 0.01,
        "target_primary_detection_ge_70pct": summary_by_name["target"]["G6_pass_rate"] >= 0.70,
        "target_strong_classification_ge_65pct": summary_by_name["target"]["strong_replication_rate"] >= 0.65,
        "weak_effect_primary_pass_le_5pct": summary_by_name["weak_effect"]["G6_pass_rate"] <= 0.05,
        "spin0_confound_g5_pass_le_10pct": summary_by_name["spin0_confound"]["G5_pass_rate"] <= 0.10,
        "one_spin_artifact_g7_pass_le_25pct": summary_by_name["one_spin_artifact"]["G7_pass_rate"] <= 0.25,
    }
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--outdir", type=Path, default=Path("artifacts/hqc_phase1_design_audit"))
    parser.add_argument("--residual-sd", type=float, default=6.0,
                        help="Residual SD (pp) for all scenarios. Frozen primary assumption: 6.0. Sensitivity: 7.0.")
    parser.add_argument("--n-blocks", type=int, default=N_BLOCKS,
                        help="Number of complete blocks (4 animals/runs each). Frozen default: 20.")
    parser.add_argument("--allow-check-failure", action="store_true",
                        help="Sensitivity runs only: report failing acceptance checks without a non-zero exit.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    cov_rng = np.random.default_rng(np.random.SeedSequence(args.seed, spawn_key=(COVARIATE_STREAM,)))
    scenarios = [replace(s, residual_sd=args.residual_sd) for s in SCENARIOS.values()]
    summaries = [audit_scenario(rng, s, args.reps, args.n_blocks, cov_rng) for s in scenarios]
    by_name = {row["scenario"]: row for row in summaries}
    checks = validate_operating_characteristics(by_name)

    csv_path = args.outdir / "operating_characteristics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)

    json_path = args.outdir / "audit_summary.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "warning": "SYNTHETIC DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE",
                "protocol_version": PROTOCOL_VERSION,
                "seed": args.seed,
                "reps_per_scenario": args.reps,
                "n_blocks": args.n_blocks,
                "residual_sd": args.residual_sd,
                "g9_rule": "additive AND covariate-adjusted: estimate > 3 pp and 95% CI lower bound > 0",
                "g9_covariates": list(COVARIATES),
                "sesoi_pp": SESOI,
                "spin0_red_flag_margin_pp": SPIN0_RED_FLAG_MARGIN,
                "operating_characteristic_checks": checks,
                "all_checks_pass": all(checks.values()),
                "scenarios": summaries,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"H_QC Phase 1 synthetic design audit v{PROTOCOL_VERSION}")
    print("WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE")
    print(f"residual SD = {args.residual_sd} pp | blocks = {args.n_blocks} (N = {4 * args.n_blocks}) | reps = {args.reps} | seed = {args.seed}")
    for row in summaries:
        print(
            f"{row['scenario']:>18s} | true Δ={row['true_spin_contrast']:5.2f} | "
            f"G6={row['G6_pass_rate']:.3f} | G5={row['G5_pass_rate']:.3f} | "
            f"G7={row['G7_pass_rate']:.3f} | G9={row['G9_pass_rate']:.3f} | strong={row['strong_replication_rate']:.3f}"
        )
    print("Acceptance checks:")
    for name, passed in checks.items():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")

    if not all(checks.values()):
        if args.allow_check_failure:
            print("NOTE: acceptance checks FAILED under these sensitivity settings (--allow-check-failure set; exit 0).")
        else:
            raise SystemExit("Preflight design audit FAILED: revise before real-world data collection.")


if __name__ == "__main__":
    main()
