#!/usr/bin/env python3
"""QICQ QBG Phase 0A-R v0.1 — Adversarial Generalization Challenge.

Synthetic two-qubit gate-mechanics stress test only.

This module does NOT implement process matrices, causal-nonseparability
certification, the Quantum Switch, indefinite causal order, biology, or
consciousness. C_off is an independently motivated state-level structural
diagnostic and is not an estimator, bound, restriction, monotone, or
certificate of the historical process-level Q_delta(W) or M_CNS.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

from qbg.phase0a import qbg_phase0a as p0a


VERSION = "0.1"
DEFAULT_SEEDS = 256
DEFAULT_BASE_SEED = 20260910
PHYSICAL_TOL = 1e-10
MIMIC_TOL = 1e-9
BASIS_TOL = 1e-9
CHANNEL_TOL = 1e-9
TARGET_NEGATIVITY_MIN = 0.20
PRIMARY_MARGIN_FLOOR = TARGET_NEGATIVITY_MIN - MIMIC_TOL
CHSH_THRESHOLD = 2.0 + 1e-6
LOCAL_UNITARY_TRIALS = 16
RANDOM_CPTP_CHANNELS = 4
WERNER_TARGET_P_MIN = 0.61
WERNER_TARGET_P_MAX = 1.00
SCHMIDT_LAMBDA_MIN = 0.05
SCHMIDT_LAMBDA_MAX = 0.50
WERNER_MIMIC_P_MIN = 0.30
WERNER_MIMIC_P_MAX = 1.0 / 3.0
BASELINE_MARGIN = 0.31254751364720484 - 3.409409165475825e-16


def c_off(rho: np.ndarray) -> float:
    """Basis-dependent scalar off-diagonal Frobenius norm; diagnostic only."""
    rho = np.asarray(rho, dtype=complex)
    return float(np.linalg.norm(rho - np.diag(np.diag(rho)), ord="fro"))


def midpoint_schedule(index: int, total: int, low: float, high: float) -> float:
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0 <= index < total:
        raise ValueError("index out of range")
    return float(low + (high - low) * ((index + 0.5) / total))


def werner_state(p: float) -> np.ndarray:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0,1]")
    return (
        p * p0a.projector(p0a.PHI_PLUS)
        + (1.0 - p) * np.eye(4, dtype=complex) / 4.0
    )


def schmidt_state(lam: float) -> np.ndarray:
    if not 0.0 < lam < 1.0:
        raise ValueError("lam must be in (0,1)")
    v = p0a.ket(np.sqrt(lam), 0.0, 0.0, np.sqrt(1.0 - lam))
    return p0a.projector(v)


def random_local_rotate(rho: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    return p0a.apply_local_unitary(
        rho,
        p0a.random_unitary_2(rng),
        p0a.random_unitary_2(rng),
    )


def amplitude_damping_kraus(gamma: float) -> Tuple[np.ndarray, ...]:
    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be in [0,1]")
    k0 = np.array(
        [[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]],
        dtype=complex,
    )
    k1 = np.array(
        [[0.0, np.sqrt(gamma)], [0.0, 0.0]],
        dtype=complex,
    )
    return (k0, k1)


def random_cptp_kraus(
    rng: np.random.Generator, rank: int = 4
) -> Tuple[np.ndarray, ...]:
    """Generate a qubit CPTP channel from a random isometry.

    QR gives an isometry V: C^2 -> C^(2*rank). Partitioning V into rank
    2x2 blocks K_i guarantees sum_i K_i^dagger K_i = I up to numerical
    precision.
    """
    if rank <= 0:
        raise ValueError("rank must be positive")
    z = rng.normal(size=(2 * rank, 2)) + 1j * rng.normal(
        size=(2 * rank, 2)
    )
    q, _ = np.linalg.qr(z)
    return tuple(q[2 * i : 2 * (i + 1), :] for i in range(rank))


def kraus_completeness_error(kraus: Iterable[np.ndarray]) -> float:
    acc = np.zeros((2, 2), dtype=complex)
    for k in kraus:
        acc += k.conj().T @ k
    return float(np.linalg.norm(acc - p0a.I2, ord="fro"))


def random_separable_mixture(
    rng: np.random.Generator, components: int
) -> np.ndarray:
    if components < 2:
        raise ValueError("components must be >=2")
    weights = rng.dirichlet(np.ones(components))
    rho = np.zeros((4, 4), dtype=complex)
    for w in weights:
        rho += float(w) * p0a.random_product_state(rng)
    return rho


def random_rotated_classical_common_cause(
    rng: np.random.Generator,
) -> np.ndarray:
    rho = p0a.random_classical_diagonal(rng)
    return random_local_rotate(rho, rng)


def cases_for_seed(
    seed: int, index: int, total: int
) -> List[Tuple[str, bool, np.ndarray]]:
    rng = np.random.default_rng(seed)

    p_target = midpoint_schedule(
        index, total, WERNER_TARGET_P_MIN, WERNER_TARGET_P_MAX
    )
    lam = midpoint_schedule(
        index, total, SCHMIDT_LAMBDA_MIN, SCHMIDT_LAMBDA_MAX
    )
    p_mimic = midpoint_schedule(
        index, total, WERNER_MIMIC_P_MIN, WERNER_MIMIC_P_MAX
    )

    target_werner = random_local_rotate(werner_state(p_target), rng)
    target_schmidt = random_local_rotate(schmidt_state(lam), rng)

    product_coh = p0a.projector(np.kron(p0a.PLUS, p0a.PLUS))
    product_coh = random_local_rotate(product_coh, rng)

    components = int(rng.integers(2, 13))
    separable_mix = random_separable_mixture(rng, components)
    rotated_cc = random_rotated_classical_common_cause(rng)
    boundary_werner = random_local_rotate(werner_state(p_mimic), rng)

    return [
        ("target_werner_bell", True, target_werner),
        ("target_schmidt_pure", True, target_schmidt),
        ("mimic_maximal_product_coherence", False, product_coh),
        ("mimic_variable_rank_separable_mixture", False, separable_mix),
        ("mimic_rotated_classical_common_cause", False, rotated_cc),
        ("mimic_werner_separability_boundary", False, boundary_werner),
    ]


def basis_invariance_audit(
    rho: np.ndarray, rng: np.random.Generator
) -> Tuple[bool, float]:
    base = p0a.negativity(rho)
    max_delta = 0.0
    for _ in range(LOCAL_UNITARY_TRIALS):
        out = random_local_rotate(rho, rng)
        max_delta = max(max_delta, abs(p0a.negativity(out) - base))
    return max_delta <= BASIS_TOL, float(max_delta)


def fixed_channel_family() -> List[Tuple[np.ndarray, ...]]:
    return [
        p0a.dephasing_kraus(0.25),
        p0a.dephasing_kraus(0.50),
        p0a.depolarizing_kraus(0.10),
        p0a.depolarizing_kraus(0.30),
        p0a.depolarizing_kraus(0.60),
        amplitude_damping_kraus(0.15),
        amplitude_damping_kraus(0.50),
        amplitude_damping_kraus(0.85),
    ]


def tested_channel_audit(
    rho: np.ndarray, rng: np.random.Generator
) -> Dict[str, object]:
    base = p0a.negativity(rho)
    channels = list(fixed_channel_family())
    for _ in range(RANDOM_CPTP_CHANNELS):
        channels.append(random_cptp_kraus(rng, rank=4))

    all_complete = True
    all_outputs_physical = True
    max_increase = -np.inf

    for kraus in channels:
        all_complete = (
            all_complete and kraus_completeness_error(kraus) <= 1e-10
        )
        for apply_channel in (
            p0a.apply_local_channel_a,
            p0a.apply_local_channel_b,
        ):
            out = apply_channel(rho, kraus)
            all_outputs_physical = (
                all_outputs_physical
                and p0a.is_physical_density(out, tol=PHYSICAL_TOL)
            )
            max_increase = max(
                max_increase, p0a.negativity(out) - base
            )

    nonincrease = max_increase <= CHANNEL_TOL
    passed = all_complete and all_outputs_physical and nonincrease
    return {
        "pass": bool(passed),
        "kraus_complete": bool(all_complete),
        "outputs_physical": bool(all_outputs_physical),
        "nonincrease_only_pass": bool(nonincrease),
        "max_increase": float(max_increase),
    }


def quantiles(values: List[float]) -> Dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {
        "min": float(np.min(arr)),
        "q25": float(np.quantile(arr, 0.25)),
        "median": float(np.quantile(arr, 0.50)),
        "q75": float(np.quantile(arr, 0.75)),
        "max": float(np.max(arr)),
    }


def run_qualification(seeds: int, base_seed: int) -> Dict[str, object]:
    if seeds <= 0:
        raise ValueError("seeds must be positive")

    bell = p0a.projector(p0a.PHI_PLUS)
    product = p0a.projector(np.kron(p0a.PLUS, p0a.PLUS))
    g1 = bool(
        c_off(bell) > 0.1
        and c_off(product) > 0.1
        and p0a.negativity(bell) >= TARGET_NEGATIVITY_MIN
        and p0a.negativity(product) <= MIMIC_TOL
    )

    rows: List[Dict[str, object]] = []
    all_state_physical = True
    all_basis = True
    all_channel = True
    all_channel_outputs_physical = True
    all_kraus_complete = True
    basis_max = 0.0
    channel_max = -np.inf
    paired_margins: List[float] = []

    for index in range(seeds):
        seed = base_seed + index
        seed_rows: List[Dict[str, object]] = []
        for case_index, (name, is_target, rho) in enumerate(
            cases_for_seed(seed, index, seeds)
        ):
            physical = p0a.is_physical_density(rho, tol=PHYSICAL_TOL)
            all_state_physical = all_state_physical and physical

            basis_rng = np.random.default_rng(
                seed ^ (0x13579BDF + case_index * 0x101)
            )
            basis_ok, basis_delta = basis_invariance_audit(rho, basis_rng)
            all_basis = all_basis and basis_ok
            basis_max = max(basis_max, basis_delta)

            channel_rng = np.random.default_rng(
                seed ^ (0x2468ACE0 + case_index * 0x211)
            )
            channel = tested_channel_audit(rho, channel_rng)
            all_channel = all_channel and bool(channel["pass"])
            all_channel_outputs_physical = (
                all_channel_outputs_physical
                and bool(channel["outputs_physical"])
            )
            all_kraus_complete = (
                all_kraus_complete and bool(channel["kraus_complete"])
            )
            channel_max = max(
                channel_max, float(channel["max_increase"])
            )

            n = p0a.negativity(rho)
            s = p0a.chsh_smax(rho)
            row = {
                "seed": seed,
                "case": name,
                "is_target": is_target,
                "physical": physical,
                "c_off": c_off(rho),
                "negativity": n,
                "chsh_smax": s,
                "resource_pass": (
                    n >= TARGET_NEGATIVITY_MIN
                    if is_target
                    else n <= MIMIC_TOL
                ),
                "chsh_witness_pass": (
                    s > CHSH_THRESHOLD
                    if is_target
                    else s <= CHSH_THRESHOLD
                ),
                "basis_invariance_pass": basis_ok,
                "basis_max_abs_delta": basis_delta,
                "tested_channel_kraus_complete": channel[
                    "kraus_complete"
                ],
                "tested_channel_outputs_physical": channel[
                    "outputs_physical"
                ],
                "tested_channel_nonincrease_only_pass": channel[
                    "nonincrease_only_pass"
                ],
                "tested_channel_pass": channel["pass"],
                "tested_channel_max_increase": channel["max_increase"],
            }
            rows.append(row)
            seed_rows.append(row)

        seed_targets = [r for r in seed_rows if r["is_target"]]
        seed_mimics = [r for r in seed_rows if not r["is_target"]]
        paired_margins.append(
            min(float(r["negativity"]) for r in seed_targets)
            - max(float(r["negativity"]) for r in seed_mimics)
        )

    targets = [r for r in rows if r["is_target"]]
    mimics = [r for r in rows if not r["is_target"]]
    target_n = [float(r["negativity"]) for r in targets]
    mimic_n = [float(r["negativity"]) for r in mimics]
    target_s = [float(r["chsh_smax"]) for r in targets]
    mimic_s = [float(r["chsh_smax"]) for r in mimics]

    resource_margin = min(target_n) - max(mimic_n)
    g0 = bool(
        all_state_physical
        and all_channel_outputs_physical
        and all_kraus_complete
    )
    g2 = bool(all(n >= TARGET_NEGATIVITY_MIN for n in target_n))
    g3 = bool(all_basis)
    g4 = bool(all_channel)
    g5 = bool(all(n <= MIMIC_TOL for n in mimic_n))
    g6 = bool(
        all(s > CHSH_THRESHOLD for s in target_s)
        and all(s <= CHSH_THRESHOLD for s in mimic_s)
    )

    gates = {
        "G0_PHYSICAL_VALIDITY": g0,
        "G1_STRUCTURAL_DIAGNOSTIC_INSUFFICIENT": g1,
        "G2_TARGET_RESOURCE_EXCLUSION": g2,
        "G3_LOCAL_BASIS_ROBUSTNESS": g3,
        "G4_TESTED_CHANNEL_NONINCREASE": g4,
        "G5_ADVERSARIAL_MIMIC_EXCLUSION": g5,
        "G6_OPTIONAL_CHSH_WITNESS": g6,
    }
    core_names = list(gates.keys())[:6]
    failed_core = [name for name in core_names if not gates[name]]
    core_pass = len(failed_core) == 0
    primary_pass = resource_margin >= PRIMARY_MARGIN_FLOOR

    if core_pass and primary_pass and g6:
        decision = "P0AR_CORE_GENERALIZES_WITH_CHSH"
    elif core_pass and primary_pass:
        decision = "P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED"
    else:
        failures = list(failed_core)
        if not primary_pass:
            failures.append("PRIMARY_RESOURCE_MARGIN")
        decision = "STOP_P0AR_" + "_".join(failures)

    return {
        "warning": (
            "SYNTHETIC TWO-QUBIT ADVERSARIAL GATE-MECHANICS TEST ONLY. "
            "NOT A PROCESS-MATRIX CNS/QCO TEST; NOT PHYSICAL-MECHANISM, "
            "BIOLOGICAL, OR CONSCIOUSNESS EVIDENCE."
        ),
        "protocol": "QICQ-QBG-P0AR",
        "version": VERSION,
        "parent_phase0a_head": (
            "bdc3dce5f7d4b8dce73a34f6c0f91e76e5ace613"
        ),
        "seeds": seeds,
        "base_seed": base_seed,
        "primary_metric": {
            "name": "resource_separation_margin_gN",
            "value": float(resource_margin),
            "pass_floor": PRIMARY_MARGIN_FLOOR,
            "pass": bool(primary_pass),
            "phase0a_baseline_margin": BASELINE_MARGIN,
        },
        "gates": gates,
        "core_gates_pass": bool(core_pass),
        "failed_core_gates": failed_core,
        "decision": decision,
        "summary": {
            "target_negativity": quantiles(target_n),
            "mimic_negativity": quantiles(mimic_n),
            "target_chsh": quantiles(target_s),
            "mimic_chsh": quantiles(mimic_s),
            "paired_negativity_margin": quantiles(paired_margins),
            "basis_max_abs_delta": float(basis_max),
            "tested_channel_max_increase": float(channel_max),
            "all_tested_channel_outputs_physical": bool(
                all_channel_outputs_physical
            ),
            "all_tested_channel_kraus_complete": bool(all_kraus_complete),
            "reference_bell_c_off": c_off(bell),
            "reference_product_c_off": c_off(product),
            "reference_bell_negativity": p0a.negativity(bell),
            "reference_product_negativity": p0a.negativity(product),
        },
        "rows": rows,
    }


def write_outputs(result: Dict[str, object], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = dict(result)
    rows = summary.pop("rows")

    with (outdir / "qualification_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with (outdir / "qualification_rows.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (outdir / "decision.txt").open("w", encoding="utf-8") as f:
        f.write(str(result["decision"]) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--base-seed", type=int, default=DEFAULT_BASE_SEED)
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("artifacts/qbg_phase0ar"),
    )
    args = parser.parse_args()

    result = run_qualification(args.seeds, args.base_seed)
    write_outputs(result, args.outdir)

    print(f"QICQ QBG Phase 0A-R v{VERSION}")
    print(result["warning"])
    for name, ok in result["gates"].items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(
        "resource_separation_margin_gN:",
        result["primary_metric"]["value"],
    )
    for key, value in result["summary"].items():
        print(f"{key}: {value}")
    print("DECISION:", result["decision"])

    if not result["core_gates_pass"] or not result["primary_metric"]["pass"]:
        raise SystemExit("QBG Phase 0A-R core qualification failed.")


if __name__ == "__main__":
    main()
