#!/usr/bin/env python3
"""Deterministic unit tests for QICQ QBG Phase 0A v0.1.2."""

from __future__ import annotations

import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import qbg_phase0a as qbg


class QBGPhase0ATests(unittest.TestCase):
    def test_reference_states_are_physical(self):
        for name, rho in qbg.reference_states().items():
            self.assertTrue(qbg.is_physical_density(rho), name)

    def test_coherence_is_not_sufficient(self):
        refs = qbg.reference_states()
        target = refs["target_bell_proxy"]
        mimic = refs["fixed_order_coherent_product_mimic"]
        self.assertGreater(qbg.q_delta(target), 0.1)
        self.assertGreater(qbg.q_delta(mimic), 0.1)
        self.assertAlmostEqual(
            qbg.q_delta(target),
            qbg.q_delta(mimic),
            places=12,
        )
        self.assertGreater(
            qbg.negativity(target),
            qbg.TARGET_NEGATIVITY_MIN,
        )
        self.assertLessEqual(
            qbg.negativity(mimic),
            qbg.MIMIC_TOL,
        )

    def test_local_basis_invariance_of_negativity(self):
        rho = qbg.reference_states()["target_bell_proxy"]
        rng = np.random.default_rng(12345)
        ok, delta = qbg.basis_invariance_audit(
            rho, rng, trials=20
        )
        self.assertTrue(ok)
        self.assertLessEqual(delta, qbg.BASIS_TOL)

    def test_frozen_local_channels_do_not_increase_negativity(self):
        rho = qbg.reference_states()["target_bell_proxy"]
        ok, max_increase = qbg.monotonicity_audit(rho)
        self.assertTrue(ok)
        self.assertLessEqual(
            max_increase,
            qbg.MONOTONICITY_TOL,
        )

    def test_local_channel_paths_cover_both_subsystems(self):
        rho = qbg.reference_states()["target_bell_proxy"]
        channels = (
            qbg.dephasing_kraus(0.25),
            qbg.dephasing_kraus(0.50),
            qbg.depolarizing_kraus(0.10),
            qbg.depolarizing_kraus(0.30),
            qbg.depolarizing_kraus(0.60),
        )
        base = qbg.negativity(rho)
        for apply_channel in (
            qbg.apply_local_channel_a,
            qbg.apply_local_channel_b,
        ):
            for kraus in channels:
                out = apply_channel(rho, kraus)
                self.assertTrue(qbg.is_physical_density(out))
                self.assertLessEqual(
                    qbg.negativity(out) - base,
                    qbg.MONOTONICITY_TOL,
                )

    def test_g4_rejects_non_trace_preserving_channel(self):
        rho = qbg.reference_states()["target_bell_proxy"]
        bad_out = 0.25 * rho
        self.assertFalse(qbg.is_physical_density(bad_out))

        def broken_local_channel(_rho, _kraus):
            return bad_out

        # Exercise the production G4 code path directly. If one frozen
        # local-channel implementation were malformed, G4 must fail even
        # though the reduced trace also reduces the raw negativity.
        with patch.object(
            qbg,
            "apply_local_channel_a",
            side_effect=broken_local_channel,
        ):
            details = qbg.monotonicity_audit_details(rho)
        self.assertFalse(details["outputs_physical"])
        self.assertTrue(details["monotonicity_only_pass"])
        self.assertFalse(details["pass"])

    def test_stochastic_mimics_are_ppt(self):
        for seed in range(20):
            cases = qbg.stochastic_cases(20260909 + seed)
            for name, rho in cases.items():
                if not name.startswith("target_"):
                    self.assertLessEqual(
                        qbg.negativity(rho),
                        qbg.MIMIC_TOL,
                        (seed, name),
                    )

    def test_target_proxy_exceeds_frozen_margin(self):
        for seed in range(20):
            rho = qbg.stochastic_cases(
                20260909 + seed
            )["target_werner_proxy"]
            self.assertGreaterEqual(
                qbg.negativity(rho),
                qbg.TARGET_NEGATIVITY_MIN,
            )
            self.assertGreater(
                qbg.chsh_smax(rho),
                2.0 + qbg.CHSH_MARGIN,
            )

    def test_full_qualification_smoke(self):
        result = qbg.run_qualification(
            seeds=10,
            base_seed=20260909,
        )
        self.assertTrue(result["core_gates_pass"])
        self.assertEqual(
            result["decision"],
            "P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS",
        )


    # ---- v0.1.2: manifest-vs-code consistency ---------------------------

    def _manifest(self, name="manifest.json"):
        with (HERE / name).open(encoding="utf-8") as f:
            return json.load(f)

    def test_manifest_matches_code_constants(self):
        m = self._manifest()
        self.assertEqual(m["protocol"], "QICQ-QBG-P0A")
        self.assertEqual(m["version"], qbg.VERSION)
        self.assertEqual(m["seeds"], qbg.DEFAULT_SEEDS)
        self.assertEqual(m["base_seed"], qbg.DEFAULT_BASE_SEED)
        self.assertEqual(m["target"]["werner_p_min"], qbg.WERNER_P_MIN)
        self.assertEqual(m["target"]["werner_p_max"], qbg.WERNER_P_MAX)
        self.assertEqual(
            m["target"]["negativity_min"], qbg.TARGET_NEGATIVITY_MIN
        )
        self.assertEqual(m["resource"]["mimic_tolerance"], qbg.MIMIC_TOL)
        rob = m["robustness"]
        self.assertEqual(rob["physical_tolerance"], qbg.PHYSICAL_TOL)
        self.assertEqual(rob["basis_tolerance"], qbg.BASIS_TOL)
        self.assertEqual(
            rob["monotonicity_tolerance"], qbg.MONOTONICITY_TOL
        )
        self.assertEqual(
            rob["local_unitary_trials_per_case"],
            qbg.LOCAL_UNITARY_TRIALS_PER_CASE,
        )
        self.assertEqual(
            rob["free_channels"],
            [f"{kind}_lambda_{lam:.2f}" for kind, lam in qbg.FREE_CHANNEL_SPECS],
        )
        self.assertTrue(rob["free_channel_output_validity_required"])
        wit = m["optional_operational_witness"]
        self.assertEqual(wit["target_min_strict"], 2.0 + qbg.CHSH_MARGIN)
        self.assertEqual(wit["mimic_max"], 2.0 + qbg.CHSH_MARGIN)
        self.assertEqual(
            m["mimics_reference_deterministic"], list(qbg.REFERENCE_MIMICS)
        )

    def test_manifest_gate_names_match_result(self):
        m = self._manifest()
        result = qbg.run_qualification(seeds=1, base_seed=20260909)
        self.assertEqual(
            m["core_gates"] + [m["optional_gate"]],
            list(result["gates"].keys()),
        )

    def test_basis_audit_default_trials_match_manifest(self):
        import inspect

        default = inspect.signature(
            qbg.basis_invariance_audit
        ).parameters["trials"].default
        self.assertEqual(
            default,
            self._manifest()["robustness"]["local_unitary_trials_per_case"],
        )

    def test_preserved_manifests_keep_frozen_parameters(self):
        current = self._manifest()
        for name, version in (
            ("manifest_v0.1.json", "0.1"),
            ("manifest_v0.1.1.json", "0.1.1"),
        ):
            old = self._manifest(name)
            self.assertEqual(old["version"], version)
            for key in ("seeds", "base_seed", "target", "resource"):
                self.assertEqual(old[key], current[key], (name, key))
            for key in (
                "physical_tolerance",
                "basis_tolerance",
                "monotonicity_tolerance",
                "local_unitary_trials_per_case",
                "free_channels",
            ):
                self.assertEqual(
                    old["robustness"][key],
                    current["robustness"][key],
                    (name, key),
                )
        self.assertEqual(current["lineage"]["parent_version"], "0.1.1")

    # ---- v0.1.2: reference mimics are G5/G6 gate inputs -------------------

    def test_reference_mimics_pass_g5_g6_thresholds(self):
        refs = qbg.reference_states()
        for name in qbg.REFERENCE_MIMICS:
            self.assertLessEqual(
                qbg.negativity(refs[name]), qbg.MIMIC_TOL, name
            )
            self.assertLessEqual(
                qbg.chsh_smax(refs[name]), 2.0 + qbg.CHSH_MARGIN, name
            )

    def test_entangled_reference_mimic_fails_g5_and_g6(self):
        original = qbg.reference_states

        def corrupted_reference_states():
            refs = original()
            refs["maximally_mixed_mimic"] = qbg.projector(qbg.PHI_PLUS)
            return refs

        with patch.object(
            qbg, "reference_states", side_effect=corrupted_reference_states
        ):
            result = qbg.run_qualification(seeds=2, base_seed=20260909)
        self.assertFalse(result["gates"]["G5_MIMIC_EXCLUSION"])
        self.assertFalse(
            result["gates"]["G6_OPTIONAL_CHSH_OPERATIONAL_WITNESS"]
        )
        self.assertEqual(result["decision"], "STOP_G5_MIMIC_EXCLUSION")

    def test_summary_reports_reference_mimic_maxima(self):
        result = qbg.run_qualification(seeds=2, base_seed=20260909)
        s = result["summary"]
        self.assertEqual(s["reference_mimics_gated"], list(qbg.REFERENCE_MIMICS))
        self.assertLessEqual(s["reference_mimic_max_negativity"], qbg.MIMIC_TOL)
        self.assertLessEqual(
            s["reference_mimic_max_chsh"], 2.0 + qbg.CHSH_MARGIN
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
