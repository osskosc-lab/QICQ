#!/usr/bin/env python3
"""QICQ QBG Phase 0B-I v0.1.

Deterministic bipartite process-matrix causal-nonseparability SDP
qualification. Synthetic gold cases only.

This module intentionally does NOT implement the Quantum Switch or a
particular operational witness. B0-B6 must qualify first.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import cvxpy as cp
import numpy as np

VERSION = "0.1"
PARENT_PHASE0AR_HEAD = "d2bf56534c314f922c874ac9efa38b5e6f559fa8"

DIMS = (2, 2, 2, 2)
AI, AO, BI, BO = range(4)
N = int(np.prod(DIMS))
D_OUT = DIMS[AO] * DIMS[BO]
TRACE_NORM = float(D_OUT)

PROCESS_TOL = 1e-8
FREE_ROBUSTNESS_TOL = 5e-5
CNS_POS_TOL = 1e-4
SOLVER_CERT_TOL = 1e-5
REPRESENTATION_TOL = 5e-5
FREE_MIXING_TOL = 5e-5

SCS_EPS_ABS = 1e-7
SCS_EPS_REL = 1e-7
SCS_MAX_ITERS = 200000

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I16 = np.eye(N, dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(np.kron(a, b), c), d)


def replacement_superoperator(axis: int) -> np.ndarray:
    """Return S_X with vec(_X W) = S_X vec(W), column-major vec.

    _X W replaces subsystem X by I_X/d_X times its partial trace.
    The implementation is explicit in frozen tensor indices to avoid
    relying on library-specific partial-trace conventions.
    """
    d = DIMS[axis]
    s = np.zeros((N * N, N * N), dtype=float)
    for i in range(N):
        mi = list(np.unravel_index(i, DIMS))
        for j in range(N):
            mj = list(np.unravel_index(j, DIMS))
            if mi[axis] != mj[axis]:
                continue
            out_index = i + N * j
            for k in range(d):
                ii = mi.copy()
                jj = mj.copy()
                ii[axis] = k
                jj[axis] = k
                i_in = int(np.ravel_multi_index(tuple(ii), DIMS))
                j_in = int(np.ravel_multi_index(tuple(jj), DIMS))
                in_index = i_in + N * j_in
                s[out_index, in_index] += 1.0 / d
    return s


REPLACERS = tuple(replacement_superoperator(axis) for axis in range(4))


def replace_np(w: np.ndarray, axis: int) -> np.ndarray:
    v = np.asarray(w, dtype=complex).reshape(-1, order="F")
    return (REPLACERS[axis] @ v).reshape((N, N), order="F")


def replace_expr(w: cp.Expression, axis: int) -> cp.Expression:
    v = cp.vec(w, order="F")
    return cp.reshape(REPLACERS[axis] @ v, (N, N), order="F")


def replace_many_np(w: np.ndarray, axes: Tuple[int, ...]) -> np.ndarray:
    out = np.asarray(w, dtype=complex)
    for axis in axes:
        out = replace_np(out, axis)
    return out


def replace_many_expr(w: cp.Expression, axes: Tuple[int, ...]) -> cp.Expression:
    out = w
    for axis in axes:
        out = replace_expr(out, axis)
    return out


def homogeneous_process_residuals_np(w: np.ndarray) -> Dict[str, float]:
    aiaow = replace_many_np(w, (AI, AO))
    bibow = replace_many_np(w, (BI, BO))
    c1 = aiaow - replace_np(aiaow, BO)
    c2 = bibow - replace_np(bibow, AO)
    c3 = w - replace_np(w, AO) - replace_np(w, BO) + replace_many_np(w, (AO, BO))
    return {
        "c1_Bo_AiAo": float(np.linalg.norm(c1, ord="fro")),
        "c2_Ao_BiBo": float(np.linalg.norm(c2, ord="fro")),
        "c3_Ao_Bo": float(np.linalg.norm(c3, ord="fro")),
    }


def process_validity_report(w: np.ndarray, normalized: bool = True) -> Dict[str, object]:
    h = (w + w.conj().T) / 2
    eigs = np.linalg.eigvalsh(h)
    residuals = homogeneous_process_residuals_np(w)
    herm = float(np.linalg.norm(w - w.conj().T, ord="fro"))
    trace_value = complex(np.trace(w))
    trace_error = abs(trace_value - TRACE_NORM) if normalized else 0.0
    ok = (
        herm <= PROCESS_TOL
        and float(np.min(eigs)) >= -PROCESS_TOL
        and (not normalized or trace_error <= PROCESS_TOL)
        and max(residuals.values()) <= PROCESS_TOL
    )
    return {
        "pass": bool(ok),
        "hermiticity_residual": herm,
        "min_eigenvalue": float(np.min(eigs)),
        "trace_real": float(trace_value.real),
        "trace_imag": float(trace_value.imag),
        "trace_error": float(trace_error),
        "linear_residuals": residuals,
    }


def order_residual_np(w: np.ndarray, order: str) -> float:
    if order == "AtoB":
        delta = w - replace_np(w, BO)
    elif order == "BtoA":
        delta = w - replace_np(w, AO)
    else:
        raise ValueError(order)
    return float(np.linalg.norm(delta, ord="fro"))


def homogeneous_process_constraints(w: cp.Expression) -> List[cp.Constraint]:
    aiaow = replace_many_expr(w, (AI, AO))
    bibow = replace_many_expr(w, (BI, BO))
    c1 = aiaow - replace_expr(aiaow, BO)
    c2 = bibow - replace_expr(bibow, AO)
    c3 = w - replace_expr(w, AO) - replace_expr(w, BO) + replace_many_expr(w, (AO, BO))
    return [c1 == 0, c2 == 0, c3 == 0]


def ordered_cone_constraints(w: cp.Expression, order: str) -> List[cp.Constraint]:
    constraints: List[cp.Constraint] = [w >> 0]
    constraints.extend(homogeneous_process_constraints(w))
    if order == "AtoB":
        constraints.append(w == replace_expr(w, BO))
    elif order == "BtoA":
        constraints.append(w == replace_expr(w, AO))
    else:
        raise ValueError(order)
    return constraints


def gold_cases() -> Dict[str, np.ndarray]:
    term_ab = kron4(I2, Z, Z, I2)
    term_ba = kron4(Z, I2, X, Z)
    term_offdiag_ab = kron4(I2, X, X, I2)

    w_ab = (I16 + term_ab) / 4.0
    w_ba = (I16 + term_ba) / 4.0
    w_mix = 0.5 * w_ab + 0.5 * w_ba
    w_offdiag = (I16 + 0.8 * term_offdiag_ab) / 4.0
    w_ocb = (I16 + (term_ab + term_ba) / np.sqrt(2.0)) / 4.0
    w_white = I16 / 4.0
    return {
        "definite_order_A_to_B": w_ab,
        "definite_order_B_to_A": w_ba,
        "causally_separable_equal_mixture": w_mix,
        "definite_order_offdiagonal_mimic": w_offdiag,
        "OCB_causally_nonseparable_reference": w_ocb,
        "maximally_mixed_free_process": w_white,
    }


def offdiag_frobenius(w: np.ndarray) -> float:
    return float(np.linalg.norm(w - np.diag(np.diag(w)), ord="fro"))


def solve_generalized_causal_robustness(w: np.ndarray) -> Dict[str, object]:
    xa = cp.Variable((N, N), hermitian=True, name="X_AtoB")
    xb = cp.Variable((N, N), hermitian=True, name="X_BtoA")
    xsep = xa + xb

    constraints: List[cp.Constraint] = []
    constraints.extend(ordered_cone_constraints(xa, "AtoB"))
    constraints.extend(ordered_cone_constraints(xb, "BtoA"))
    noise_psd = xsep - w >> 0
    constraints.append(noise_psd)

    objective = cp.Minimize(cp.real(cp.trace(xsep)) / TRACE_NORM - 1.0)
    problem = cp.Problem(objective, constraints)
    value = problem.solve(
        solver=cp.SCS,
        eps_abs=SCS_EPS_ABS,
        eps_rel=SCS_EPS_REL,
        max_iters=SCS_MAX_ITERS,
        verbose=False,
    )

    raw = float(value) if value is not None else float("inf")
    robustness = max(0.0, raw) if np.isfinite(raw) else raw

    info: Dict[str, object] = {}
    extra = problem.solver_stats.extra_stats
    if isinstance(extra, dict) and isinstance(extra.get("info"), dict):
        info = extra["info"]

    def info_float(key: str) -> float:
        try:
            return float(info[key])
        except (KeyError, TypeError, ValueError):
            return float("inf")

    xa_v = None if xa.value is None else np.asarray(xa.value, dtype=complex)
    xb_v = None if xb.value is None else np.asarray(xb.value, dtype=complex)
    primal_checks: Dict[str, float] = {
        "xa_min_eig": float("-inf"),
        "xb_min_eig": float("-inf"),
        "noise_min_eig": float("-inf"),
        "xa_order_residual": float("inf"),
        "xb_order_residual": float("inf"),
        "xa_process_residual": float("inf"),
        "xb_process_residual": float("inf"),
    }
    if xa_v is not None and xb_v is not None:
        noise = xa_v + xb_v - w
        primal_checks = {
            "xa_min_eig": float(np.min(np.linalg.eigvalsh((xa_v + xa_v.conj().T) / 2))),
            "xb_min_eig": float(np.min(np.linalg.eigvalsh((xb_v + xb_v.conj().T) / 2))),
            "noise_min_eig": float(np.min(np.linalg.eigvalsh((noise + noise.conj().T) / 2))),
            "xa_order_residual": order_residual_np(xa_v, "AtoB"),
            "xb_order_residual": order_residual_np(xb_v, "BtoA"),
            "xa_process_residual": max(homogeneous_process_residuals_np(xa_v).values()),
            "xb_process_residual": max(homogeneous_process_residuals_np(xb_v).values()),
        }

    return {
        "status": str(problem.status),
        "raw_robustness": raw,
        "robustness": robustness,
        "solver": "SCS",
        "num_iters": int(problem.solver_stats.num_iters or 0),
        "solve_time": float(problem.solver_stats.solve_time or 0.0),
        "scs_res_pri": info_float("res_pri"),
        "scs_res_dual": info_float("res_dual"),
        "scs_gap": abs(info_float("gap")),
        "primal_checks": primal_checks,
    }


def solver_certificate_pass(result: Dict[str, object]) -> bool:
    return bool(
        result["status"] == "optimal"
        and float(result["scs_res_pri"]) <= SOLVER_CERT_TOL
        and float(result["scs_res_dual"]) <= SOLVER_CERT_TOL
        and float(result["scs_gap"]) <= SOLVER_CERT_TOL
    )


def permute_parties(w: np.ndarray) -> np.ndarray:
    """Swap A and B: AI,AO,BI,BO -> BI,BO,AI,AO."""
    tensor = w.reshape(DIMS + DIMS)
    perm = (BI, BO, AI, AO)
    full_perm = perm + tuple(p + 4 for p in perm)
    return tensor.transpose(full_perm).reshape((N, N))


def run_qualification() -> Dict[str, object]:
    cases = gold_cases()
    swapped_ocb = permute_parties(cases["OCB_causally_nonseparable_reference"])
    eta = 0.5
    mixed_ocb = (
        eta * cases["OCB_causally_nonseparable_reference"]
        + (1.0 - eta) * cases["maximally_mixed_free_process"]
    )

    validity = {name: process_validity_report(w) for name, w in cases.items()}
    validity["party_swapped_OCB"] = process_validity_report(swapped_ocb)
    validity["OCB_free_mixture_eta_0.5"] = process_validity_report(mixed_ocb)

    order_checks = {
        "AtoB": order_residual_np(cases["definite_order_A_to_B"], "AtoB"),
        "BtoA": order_residual_np(cases["definite_order_B_to_A"], "BtoA"),
        "offdiag_AtoB": order_residual_np(cases["definite_order_offdiagonal_mimic"], "AtoB"),
    }

    solve_names = [
        "definite_order_A_to_B",
        "definite_order_B_to_A",
        "causally_separable_equal_mixture",
        "definite_order_offdiagonal_mimic",
        "OCB_causally_nonseparable_reference",
    ]
    solves = {name: solve_generalized_causal_robustness(cases[name]) for name in solve_names}
    solves["party_swapped_OCB"] = solve_generalized_causal_robustness(swapped_ocb)
    solves["OCB_free_mixture_eta_0.5"] = solve_generalized_causal_robustness(mixed_ocb)

    b0 = bool(
        all(report["pass"] for report in validity.values())
        and max(order_checks.values()) <= PROCESS_TOL
    )

    free_names = [
        "definite_order_A_to_B",
        "definite_order_B_to_A",
        "causally_separable_equal_mixture",
    ]
    b1 = bool(
        all(
            -FREE_ROBUSTNESS_TOL <= float(solves[name]["raw_robustness"]) <= FREE_ROBUSTNESS_TOL
            for name in free_names
        )
    )

    target_r = float(solves["OCB_causally_nonseparable_reference"]["robustness"])
    b2 = bool(target_r > CNS_POS_TOL)

    mimic_r = float(solves["definite_order_offdiagonal_mimic"]["raw_robustness"])
    b3 = bool(-FREE_ROBUSTNESS_TOL <= mimic_r <= FREE_ROBUSTNESS_TOL)

    swapped_r = float(solves["party_swapped_OCB"]["robustness"])
    representation_delta = abs(target_r - swapped_r)
    b4 = bool(representation_delta <= REPRESENTATION_TOL)

    mixed_r = float(solves["OCB_free_mixture_eta_0.5"]["robustness"])
    b5 = bool(mixed_r <= target_r + FREE_MIXING_TOL)

    b6 = bool(all(solver_certificate_pass(solves[name]) for name in solves))

    gates = {
        "B0_PROCESS_VALIDITY": b0,
        "B1_FREE_SET_CALIBRATION": b1,
        "B2_CNS_RESOURCE_CERTIFICATION": b2,
        "B3_ADVERSARIAL_FREE_MIMIC_EXCLUSION": b3,
        "B4_REPRESENTATION_ROBUSTNESS": b4,
        "B5_TESTED_FREE_MIXING_NONINCREASE": b5,
        "B6_SDP_NUMERICAL_CERTIFICATION": b6,
    }
    failed = [name for name, ok in gates.items() if not ok]
    core = all(gates.values())

    if core:
        decision = "P0BI_DETERMINISTIC_CNS_SDP_QUALIFIED"
    elif any(not gates[name] for name in ("B0_PROCESS_VALIDITY", "B4_REPRESENTATION_ROBUSTNESS", "B6_SDP_NUMERICAL_CERTIFICATION")):
        decision = "STOP_IMPLEMENTATION_OR_CERTIFICATION_FAILURE"
    else:
        decision = "STOP_RESOURCE_QUALIFICATION_FAILURE"

    return {
        "warning": (
            "DETERMINISTIC SYNTHETIC BIPARTITE PROCESS-MATRIX SDP QUALIFICATION ONLY. "
            "NOT A QUANTUM-SWITCH RUN; NOT EXPERIMENTAL, BIOLOGICAL, OR CONSCIOUSNESS EVIDENCE."
        ),
        "protocol": "QICQ-QBG-P0BI",
        "version": VERSION,
        "parent_phase0ar_head": PARENT_PHASE0AR_HEAD,
        "tensor_order": ["A_I", "A_O", "B_I", "B_O"],
        "dimensions": list(DIMS),
        "trace_normalization": TRACE_NORM,
        "gates": gates,
        "core_gates_pass": bool(core),
        "failed_core_gates": failed,
        "decision": decision,
        "summary": {
            "OCB_R_CNS_g": target_r,
            "party_swapped_OCB_R_CNS_g": swapped_r,
            "representation_abs_delta": representation_delta,
            "OCB_free_mixture_eta_0.5_R_CNS_g": mixed_r,
            "offdiag_mimic_R_CNS_g_raw": mimic_r,
            "offdiag_mimic_C_off": offdiag_frobenius(cases["definite_order_offdiagonal_mimic"]),
            "free_case_R_CNS_g_raw": {name: float(solves[name]["raw_robustness"]) for name in free_names},
            "max_order_residual": max(order_checks.values()),
            "quantum_switch_executed": False,
            "particular_operational_witness_executed": False,
        },
        "validity": validity,
        "order_checks": order_checks,
        "solves": solves,
        "thresholds": {
            "process_tol": PROCESS_TOL,
            "free_robustness_tol": FREE_ROBUSTNESS_TOL,
            "cns_positive_tol": CNS_POS_TOL,
            "solver_cert_tol": SOLVER_CERT_TOL,
            "representation_tol": REPRESENTATION_TOL,
            "free_mixing_tol": FREE_MIXING_TOL,
            "scs_eps_abs": SCS_EPS_ABS,
            "scs_eps_rel": SCS_EPS_REL,
            "scs_max_iters": SCS_MAX_ITERS,
        },
    }


def write_outputs(result: Dict[str, object], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "qualification_summary.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    with (outdir / "decision.txt").open("w", encoding="utf-8") as f:
        f.write(str(result["decision"]) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("artifacts/qbg_phase0bi"))
    args = parser.parse_args()

    result = run_qualification()
    write_outputs(result, args.outdir)

    print(f"QICQ QBG Phase 0B-I v{VERSION}")
    print(result["warning"])
    for name, ok in result["gates"].items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    for key, value in result["summary"].items():
        print(f"{key}: {value}")
    print("DECISION:", result["decision"])

    if not result["core_gates_pass"]:
        raise SystemExit("QBG Phase 0B-I core qualification failed.")


if __name__ == "__main__":
    main()
