import unittest

import numpy as np

from qbg.phase0ar import qbg_phase0ar as qbg
from qbg.phase0a import qbg_phase0a as p0a


class TestQBGPhase0AR(unittest.TestCase):
    def test_structural_diagnostic_can_be_large_on_separable_product(self):
        rho = p0a.projector(np.kron(p0a.PLUS, p0a.PLUS))
        self.assertGreater(qbg.c_off(rho), 0.1)
        self.assertLessEqual(p0a.negativity(rho), qbg.MIMIC_TOL)

    def test_low_p_werner_is_resource_positive_but_chsh_limited(self):
        rho = qbg.werner_state(qbg.WERNER_TARGET_P_MIN)
        self.assertGreaterEqual(
            p0a.negativity(rho), qbg.TARGET_NEGATIVITY_MIN
        )
        self.assertLessEqual(p0a.chsh_smax(rho), qbg.CHSH_THRESHOLD)

    def test_werner_boundary_mimic_is_separable(self):
        rho = qbg.werner_state(qbg.WERNER_MIMIC_P_MAX)
        self.assertTrue(p0a.is_physical_density(rho))
        self.assertLessEqual(p0a.negativity(rho), qbg.MIMIC_TOL)

    def test_random_cptp_kraus_completeness(self):
        for seed in range(20):
            rng = np.random.default_rng(seed)
            ks = qbg.random_cptp_kraus(rng, rank=4)
            self.assertLessEqual(qbg.kraus_completeness_error(ks), 1e-10)

    def test_expanded_channel_family_preserves_physicality_and_nonincrease(self):
        rho = qbg.werner_state(0.8)
        rng = np.random.default_rng(20260910)
        details = qbg.tested_channel_audit(rho, rng)
        self.assertTrue(details["kraus_complete"])
        self.assertTrue(details["outputs_physical"])
        self.assertTrue(details["nonincrease_only_pass"])
        self.assertTrue(details["pass"])

    def test_generated_mimics_remain_separable(self):
        for index in range(12):
            seed = qbg.DEFAULT_BASE_SEED + index
            for name, is_target, rho in qbg.cases_for_seed(seed, index, 12):
                self.assertTrue(p0a.is_physical_density(rho))
                if not is_target:
                    self.assertTrue(name.startswith("mimic_"))
                    self.assertLessEqual(p0a.negativity(rho), qbg.MIMIC_TOL)

    def test_small_qualification_core_survives_and_chsh_is_witness_limited(self):
        result = qbg.run_qualification(12, qbg.DEFAULT_BASE_SEED)
        self.assertTrue(result["core_gates_pass"])
        self.assertTrue(result["primary_metric"]["pass"])
        self.assertFalse(result["gates"]["G6_OPTIONAL_CHSH_WITNESS"])
        self.assertEqual(
            result["decision"],
            "P0AR_CORE_GENERALIZES_CHSH_WITNESS_LIMITED",
        )

    def test_reproducibility(self):
        r1 = qbg.run_qualification(8, qbg.DEFAULT_BASE_SEED)
        r2 = qbg.run_qualification(8, qbg.DEFAULT_BASE_SEED)
        self.assertEqual(r1["gates"], r2["gates"])
        self.assertEqual(r1["decision"], r2["decision"])
        self.assertEqual(r1["primary_metric"], r2["primary_metric"])
        self.assertEqual(r1["summary"], r2["summary"])

    def test_primary_margin_definition_matches_extrema(self):
        result = qbg.run_qualification(6, qbg.DEFAULT_BASE_SEED)
        expected = (
            result["summary"]["target_negativity"]["min"]
            - result["summary"]["mimic_negativity"]["max"]
        )
        self.assertAlmostEqual(
            result["primary_metric"]["value"], expected, places=14
        )


if __name__ == "__main__":
    unittest.main()
