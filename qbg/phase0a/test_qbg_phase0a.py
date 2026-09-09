#!/usr/bin/env python3
"""Deterministic unit tests for QICQ QBG Phase 0A v0.1."""

from __future__ import annotations

import sys
import unittest
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
