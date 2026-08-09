#!/usr/bin/env python3
"""H_QC Phase 1 preregistration design audit v1.1.

Synthetic Monte Carlo only. This script tests whether the frozen gate logic
behaves as intended under positive and adversarial scenarios. It is NOT a
biological experiment and MUST NOT be interpreted as evidence for a xenon,
quantum, anesthesia, or consciousness mechanism.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from scipy import stats

ISOTOPES = (129, 131, 132, 134)
SESOI = 3.0
SPIN0_RED_FLAG_MARGIN = 3.0
N_BLOCKS = 20


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


def simulate_dataset(rng: np.random.Generator, scenario: Scenario) -> np.ndarray:
    """Return shape (blocks, isotopes) in ISOTOPES order."""
    y = np.zeros((N_BLOCKS, len(ISOTOPES)), dtype=float)
    block_effects = rng.normal(0.0, scenario.block_sd, size=N_BLOCKS)
    for b in range(N_BLOCKS):
        for j, iso in enumerate(ISOTOPES):
            y[b, j] = (
                20.0
                + block_effects[b]
                + scenario.effects[iso]
                + rng.normal(0.0, scenario.residual_sd)
            )
    return y


def analyze_dataset(y: np.ndarray) -> Dict[str, object]:
    # Primary complete-block contrast; common block shifts cancel.
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
    g9 = delta > SESOI

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
        "G9_block_robustness": bool(g9),
        "decision": decision,
        **{f"mean_{iso}": means[str(iso)] for iso in ISOTOPES},
    }


def audit_scenario(rng: np.random.Generator, scenario: Scenario, reps: int) -> Dict[str, object]:
    rows = [analyze_dataset(simulate_dataset(rng, scenario)) for _ in range(reps)]

    def rate(key: str) -> float:
        return float(np.mean([bool(r[key]) for r in rows]))

    decisions = [r["decision"] for r in rows]
    deltas = np.array([r["delta_spin"] for r in rows], dtype=float)

    return {
        "scenario": scenario.name,
        "description": scenario.description,
        "reps": reps,
        "true_spin_contrast": (
            (scenario.effects[129] + scenario.effects[131]) / 2.0
            - (scenario.effects[132] + scenario.effects[134]) / 2.0
        ),
        "mean_estimated_delta": float(np.mean(deltas)),
        "sd_estimated_delta": float(np.std(deltas, ddof=1)),
        "G5_pass_rate": rate("G5_spin0_no_red_flag"),
        "G6_pass_rate": rate("G6_primary"),
        "G7_pass_rate": rate("G7_directional_consistency"),
        "G9_pass_rate": rate("G9_block_robustness"),
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
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    summaries = [audit_scenario(rng, s, args.reps) for s in SCENARIOS.values()]
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
                "protocol_version": "1.1",
                "seed": args.seed,
                "reps_per_scenario": args.reps,
                "n_blocks": N_BLOCKS,
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

    print("H_QC Phase 1 synthetic design audit v1.1")
    print("WARNING: DESIGN AUDIT ONLY — NOT BIOLOGICAL EVIDENCE")
    for row in summaries:
        print(
            f"{row['scenario']:>18s} | true Δ={row['true_spin_contrast']:5.2f} | "
            f"G6={row['G6_pass_rate']:.3f} | G5={row['G5_pass_rate']:.3f} | "
            f"G7={row['G7_pass_rate']:.3f} | strong={row['strong_replication_rate']:.3f}"
        )
    print("Acceptance checks:")
    for name, passed in checks.items():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")

    if not all(checks.values()):
        raise SystemExit("Preflight design audit FAILED: revise before real-world data collection.")


if __name__ == "__main__":
    main()
