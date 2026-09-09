#!/usr/bin/env python3
"""QICQ Quantum Behavior Qualification Gate (QBG) Phase 0A v0.1.

Synthetic two-qubit resource-proxy qualification only.

This module does NOT implement a full process-matrix / quantum-comb causal
nonseparability test and MUST NOT be interpreted as evidence for indefinite
causal order, quantum consciousness, biology, or any ontology.

Purpose:
- prove that the gate mechanics distinguish coherence from a stronger
  quantum resource in a controlled synthetic setting;
- stress basis robustness, monotonicity under frozen local channels, and
  separable/classical mimic exclusion;
- create a reproducible bridge from a generic intervention/resource framework
  to a future full QICQ process-matrix implementation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

VERSION = "0.1"
DEFAULT_SEEDS = 100
DEFAULT_BASE_SEED = 20260909
PHYSICAL_TOL = 1e-10
MIMIC_TOL = 1e-9
BASIS_TOL = 1e-9
MONOTONICITY_TOL = 1e-9
TARGET_NEGATIVITY_MIN = 0.20
CHSH_MARGIN = 1e-6
WERNER_P_MIN = 0.75
WERNER_P_MAX = 1.00

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = (X, Y, Z)


def ket(*amps: complex) -> np.ndarray:
    v = np.asarray(amps, dtype=complex)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("zero ket")
    return v / n


ZERO = ket(1, 0)
ONE = ket(0, 1)
PLUS = ket(1, 1)
PHI_PLUS = ket(1, 0, 0, 1)


def projector(v: np.ndarray) -> np.ndarray:
    return np.outer(v, np.conjugate(v))


def is_physical_density(rho: np.ndarray, tol: float = PHYSICAL_TOL) -> bool:
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (4, 4):
        return False
    if not np.allclose(rho, rho.conj().T, atol=tol, rtol=0):
        return False
    if abs(np.trace(rho).real - 1.0) > tol or abs(np.trace(rho).imag) > tol:
        return False
    eigs = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    return float(np.min(eigs)) >= -tol


def q_delta(rho: np.ndarray) -> float:
    """Basis-dependent off-diagonal Frobenius norm; diagnostic only."""
    off = rho - np.diag(np.diag(rho))
    return float(np.linalg.norm(off, ord="fro"))


def partial_transpose_b(rho: np.ndarray) -> np.ndarray:
    r = np.asarray(rho, dtype=complex).reshape(2, 2, 2, 2)
    return r.transpose(0, 3, 2, 1).reshape(4, 4)


def negativity(rho: np.ndarray) -> float:
    """Two-qubit entanglement negativity.

    For 2x2 states, PPT is necessary and sufficient for separability, so
    negativity > 0 excludes the separable free set in this toy proxy.
    """
    eigs = np.linalg.eigvalsh(partial_transpose_b(rho))
    return float(np.sum(np.maximum(-eigs, 0.0)))


def random_unitary_2(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conjugate(phases))


def random_pure_qubit(rng: np.random.Generator) -> np.ndarray:
    v = rng.normal(size=2) + 1j * rng.normal(size=2)
    return ket(*v)


def apply_local_unitary(rho: np.ndarray, ua: np.ndarray, ub: np.ndarray) -> np.ndarray:
    u = np.kron(ua, ub)
    return u @ rho @ u.conj().T


def apply_local_channel_a(rho: np.ndarray, kraus: Iterable[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(rho, dtype=complex)
    for k in kraus:
        op = np.kron(k, I2)
        out += op @ rho @ op.conj().T
    return out


def math_sqrt(x: float) -> float:
    return float(np.sqrt(max(x, 0.0)))


def dephasing_kraus(lam: float) -> Tuple[np.ndarray, ...]:
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lam must be in [0,1]")
    return (math_sqrt(1.0 - lam) * I2, math_sqrt(lam) * Z)


def depolarizing_kraus(lam: float) -> Tuple[np.ndarray, ...]:
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lam must be in [0,1]")
    return (
        math_sqrt(1.0 - lam) * I2,
        math_sqrt(lam / 3.0) * X,
        math_sqrt(lam / 3.0) * Y,
        math_sqrt(lam / 3.0) * Z,
    )


def chsh_smax(rho: np.ndarray) -> float:
    """Horodecki maximal CHSH value for a two-qubit state."""
    t = np.zeros((3, 3), dtype=float)
    for i, a in enumerate(PAULIS):
        for j, b in enumerate(PAULIS):
            t[i, j] = float(np.real(np.trace(rho @ np.kron(a, b))))
    evals = np.linalg.eigvalsh(t.T @ t)
    evals = np.sort(np.maximum(evals, 0.0))
    return float(2.0 * np.sqrt(evals[-1] + evals[-2]))


def reference_states() -> Dict[str, np.ndarray]:
    bell = projector(PHI_PLUS)
    coherent_product = projector(np.kron(PLUS, ZERO))
    common_cause = (
        0.5 * projector(np.kron(ZERO, ZERO))
        + 0.5 * projector(np.kron(ONE, ONE))
    )
    maximally_mixed = np.eye(4, dtype=complex) / 4.0
    product_mixed = np.kron(projector(PLUS), I2 / 2.0)
    return {
        "target_bell_proxy": bell,
        "fixed_order_coherent_product_mimic": coherent_product,
        "classical_common_cause_mimic": common_cause,
        "product_mixed_mimic": product_mixed,
        "maximally_mixed_mimic": maximally_mixed,
    }


def werner_target(rng: np.random.Generator) -> np.ndarray:
    p = float(rng.uniform(WERNER_P_MIN, WERNER_P_MAX))
    rho = (
        p * projector(PHI_PLUS)
        + (1.0 - p) * np.eye(4, dtype=complex) / 4.0
    )
    ua, ub = random_unitary_2(rng), random_unitary_2(rng)
    return apply_local_unitary(rho, ua, ub)


def random_product_state(rng: np.random.Generator) -> np.ndarray:
    a, b = random_pure_qubit(rng), random_pure_qubit(rng)
    return projector(np.kron(a, b))


def random_separable_mixture(
    rng: np.random.Generator, components: int = 4
) -> np.ndarray:
    weights = rng.dirichlet(np.ones(components))
    rho = np.zeros((4, 4), dtype=complex)
    for w in weights:
        rho += float(w) * random_product_state(rng)
    return rho


def random_classical_diagonal(rng: np.random.Generator) -> np.ndarray:
    p = rng.dirichlet(np.ones(4))
    return np.diag(p.astype(complex))


def stochastic_cases(seed: int) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    return {
        "target_werner_proxy": werner_target(rng),
        "product_coherence_mimic": random_product_state(rng),
        "separable_memory_mimic": random_separable_mixture(
            rng, components=5
        ),
        "classical_common_cause_mimic": random_classical_diagonal(rng),
    }


def monotonicity_audit(rho: np.ndarray) -> Tuple[bool, float]:
    base = negativity(rho)
    max_increase = -np.inf
    channels = [
        dephasing_kraus(0.25),
        dephasing_kraus(0.50),
        depolarizing_kraus(0.10),
        depolarizing_kraus(0.30),
        depolarizing_kraus(0.60),
    ]
    for ks in channels:
        out = apply_local_channel_a(rho, ks)
        inc = negativity(out) - base
        max_increase = max(max_increase, inc)
    return max_increase <= MONOTONICITY_TOL, float(max_increase)


def basis_invariance_audit(
    rho: np.ndarray,
    rng: np.random.Generator,
    trials: int = 8,
) -> Tuple[bool, float]:
    base = negativity(rho)
    max_abs_delta = 0.0
    for _ in range(trials):
        ua, ub = random_unitary_2(rng), random_unitary_2(rng)
        rotated = apply_local_unitary(rho, ua, ub)
        max_abs_delta = max(
            max_abs_delta, abs(negativity(rotated) - base)
        )
    return max_abs_delta <= BASIS_TOL, float(max_abs_delta)


def run_qualification(seeds: int, base_seed: int) -> Dict[str, object]:
    refs = reference_states()
    ref_rows = []
    for name, rho in refs.items():
        ref_rows.append(
            {
                "name": name,
                "physical": is_physical_density(rho),
                "q_delta": q_delta(rho),
                "negativity": negativity(rho),
                "chsh_smax": chsh_smax(rho),
            }
        )

    ref_by_name = {r["name"]: r for r in ref_rows}
    coherence_insufficiency = (
        ref_by_name["target_bell_proxy"]["q_delta"] > 0.1
        and ref_by_name[
            "fixed_order_coherent_product_mimic"
        ]["q_delta"] > 0.1
        and ref_by_name["target_bell_proxy"]["negativity"]
        > TARGET_NEGATIVITY_MIN
        and ref_by_name[
            "fixed_order_coherent_product_mimic"
        ]["negativity"] <= MIMIC_TOL
    )

    rows: List[Dict[str, object]] = []
    basis_max = 0.0
    monotonicity_max = -np.inf
    all_physical = all(r["physical"] for r in ref_rows)
    all_basis = True
    all_mono = True

    for i in range(seeds):
        seed = base_seed + i
        cases = stochastic_cases(seed)
        for case_name, rho in cases.items():
            all_physical = (
                all_physical and is_physical_density(rho)
            )
            rng = np.random.default_rng(seed ^ 0x5A5A5A5A)
            basis_ok, basis_delta = basis_invariance_audit(
                rho, rng
            )
            mono_ok, mono_inc = monotonicity_audit(rho)
            all_basis = all_basis and basis_ok
            all_mono = all_mono and mono_ok
            basis_max = max(basis_max, basis_delta)
            monotonicity_max = max(monotonicity_max, mono_inc)

            n = negativity(rho)
            s = chsh_smax(rho)
            is_target = case_name.startswith("target_")
            rows.append(
                {
                    "seed": seed,
                    "case": case_name,
                    "is_target": is_target,
                    "physical": is_physical_density(rho),
                    "q_delta": q_delta(rho),
                    "negativity": n,
                    "chsh_smax": s,
                    "resource_pass": (
                        n >= TARGET_NEGATIVITY_MIN
                        if is_target
                        else n <= MIMIC_TOL
                    ),
                    "operational_witness_pass": (
                        s > 2.0 + CHSH_MARGIN
                        if is_target
                        else s <= 2.0 + CHSH_MARGIN
                    ),
                    "basis_invariance_pass": basis_ok,
                    "basis_max_abs_delta": basis_delta,
                    "monotonicity_pass": mono_ok,
                    "monotonicity_max_increase": mono_inc,
                }
            )

    target_rows = [r for r in rows if r["is_target"]]
    mimic_rows = [r for r in rows if not r["is_target"]]

    g0 = bool(all_physical)
    g1 = bool(coherence_insufficiency)
    g2 = bool(
        all(
            r["negativity"] >= TARGET_NEGATIVITY_MIN
            for r in target_rows
        )
    )
    g3 = bool(all_basis)
    g4 = bool(all_mono)
    g5 = bool(
        all(r["negativity"] <= MIMIC_TOL for r in mimic_rows)
    )
    g6 = bool(
        all(
            r["chsh_smax"] > 2.0 + CHSH_MARGIN
            for r in target_rows
        )
        and all(
            r["chsh_smax"] <= 2.0 + CHSH_MARGIN
            for r in mimic_rows
        )
    )

    core = g0 and g1 and g2 and g3 and g4 and g5
    if core and g6:
        decision = (
            "P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS"
        )
    elif core:
        decision = "P0A_PROXY_QUALIFIED_RESOURCE_ONLY"
    else:
        failed = [
            name
            for name, ok in {
                "G0_PHYSICAL_VALIDITY": g0,
                "G1_COHERENCE_NOT_SUFFICIENT": g1,
                "G2_TARGET_RESOURCE_EXCLUSION": g2,
                "G3_LOCAL_BASIS_ROBUSTNESS": g3,
                "G4_FREE_OPERATION_MONOTONICITY": g4,
                "G5_MIMIC_EXCLUSION": g5,
            }.items()
            if not ok
        ]
        decision = "STOP_" + "_".join(failed)

    gates = {
        "G0_PHYSICAL_VALIDITY": g0,
        "G1_COHERENCE_NOT_SUFFICIENT": g1,
        "G2_TARGET_RESOURCE_EXCLUSION": g2,
        "G3_LOCAL_BASIS_ROBUSTNESS": g3,
        "G4_FREE_OPERATION_MONOTONICITY": g4,
        "G5_MIMIC_EXCLUSION": g5,
        "G6_OPTIONAL_CHSH_OPERATIONAL_WITNESS": g6,
    }

    return {
        "warning": (
            "SYNTHETIC TWO-QUBIT RESOURCE-PROXY QUALIFICATION ONLY. "
            "NOT A PROCESS-MATRIX CNS/QCO TEST; NOT BIOLOGICAL OR "
            "CONSCIOUSNESS EVIDENCE."
        ),
        "protocol": "QICQ-QBG-P0A",
        "version": VERSION,
        "seeds": seeds,
        "base_seed": base_seed,
        "thresholds": {
            "target_negativity_min": TARGET_NEGATIVITY_MIN,
            "mimic_tol": MIMIC_TOL,
            "basis_tol": BASIS_TOL,
            "monotonicity_tol": MONOTONICITY_TOL,
            "chsh_threshold": 2.0 + CHSH_MARGIN,
            "werner_p_min": WERNER_P_MIN,
            "werner_p_max": WERNER_P_MAX,
        },
        "gates": gates,
        "core_gates_pass": core,
        "decision": decision,
        "summary": {
            "target_min_negativity": float(
                min(r["negativity"] for r in target_rows)
            ),
            "mimic_max_negativity": float(
                max(r["negativity"] for r in mimic_rows)
            ),
            "target_min_chsh": float(
                min(r["chsh_smax"] for r in target_rows)
            ),
            "mimic_max_chsh": float(
                max(r["chsh_smax"] for r in mimic_rows)
            ),
            "basis_max_abs_delta": float(basis_max),
            "monotonicity_max_increase": float(
                monotonicity_max
            ),
            "reference_target_q_delta": float(
                ref_by_name["target_bell_proxy"]["q_delta"]
            ),
            "reference_coherent_mimic_q_delta": float(
                ref_by_name[
                    "fixed_order_coherent_product_mimic"
                ]["q_delta"]
            ),
            "reference_target_negativity": float(
                ref_by_name["target_bell_proxy"]["negativity"]
            ),
            "reference_coherent_mimic_negativity": float(
                ref_by_name[
                    "fixed_order_coherent_product_mimic"
                ]["negativity"]
            ),
        },
        "reference_cases": ref_rows,
        "rows": rows,
    }


def write_outputs(
    result: Dict[str, object], outdir: Path
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = dict(result)
    rows = summary.pop("rows")

    with (
        outdir / "qualification_summary.json"
    ).open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    fieldnames = list(rows[0].keys())
    with (
        outdir / "qualification_rows.csv"
    ).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    with (
        outdir / "decision.txt"
    ).open("w", encoding="utf-8") as f:
        f.write(str(result["decision"]) + "\n")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, default=DEFAULT_SEEDS)
    p.add_argument(
        "--base-seed",
        type=int,
        default=DEFAULT_BASE_SEED,
    )
    p.add_argument(
        "--outdir",
        type=Path,
        default=Path("artifacts/qbg_phase0a"),
    )
    args = p.parse_args()

    if args.seeds <= 0:
        raise SystemExit("--seeds must be positive")

    result = run_qualification(args.seeds, args.base_seed)
    write_outputs(result, args.outdir)

    print("QICQ QBG Phase 0A v0.1")
    print(result["warning"])
    for name, ok in result["gates"].items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    for k, v in result["summary"].items():
        print(f"{k}: {v}")
    print("DECISION:", result["decision"])

    if not result["core_gates_pass"]:
        raise SystemExit(
            "QBG Phase 0A core qualification failed."
        )


if __name__ == "__main__":
    main()
