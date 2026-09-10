import unittest

import numpy as np

from qbg.phase0bi import qbg_phase0bi as qbg


class TestQBGPhase0BI(unittest.TestCase):
    def test_replacement_maps_are_idempotent(self):
        rng = np.random.default_rng(20260910)
        a = rng.normal(size=(qbg.N, qbg.N)) + 1j * rng.normal(size=(qbg.N, qbg.N))
        w = a + a.conj().T
        for axis in range(4):
            once = qbg.replace_np(w, axis)
            twice = qbg.replace_np(once, axis)
            self.assertLess(np.linalg.norm(once - twice, ord="fro"), 1e-12)
            self.assertAlmostEqual(np.trace(once).real, np.trace(w).real, places=10)
            self.assertAlmostEqual(np.trace(once).imag, np.trace(w).imag, places=10)

    def test_gold_cases_are_valid_processes(self):
        cases = qbg.gold_cases()
        for name, w in cases.items():
            with self.subTest(name=name):
                report = qbg.process_validity_report(w)
                self.assertTrue(report["pass"], msg=str(report))

    def test_definite_order_calibration(self):
        cases = qbg.gold_cases()
        self.assertLess(
            qbg.order_residual_np(cases["definite_order_A_to_B"], "AtoB"),
            qbg.PROCESS_TOL,
        )
        self.assertLess(
            qbg.order_residual_np(cases["definite_order_B_to_A"], "BtoA"),
            qbg.PROCESS_TOL,
        )

    def test_offdiagonal_mimic_is_structural_but_definite_order(self):
        w = qbg.gold_cases()["definite_order_offdiagonal_mimic"]
        self.assertGreater(qbg.offdiag_frobenius(w), 0.1)
        self.assertLess(qbg.order_residual_np(w, "AtoB"), qbg.PROCESS_TOL)

    def test_ocb_reference_is_not_itself_definite_order(self):
        w = qbg.gold_cases()["OCB_causally_nonseparable_reference"]
        self.assertGreater(qbg.order_residual_np(w, "AtoB"), 1e-3)
        self.assertGreater(qbg.order_residual_np(w, "BtoA"), 1e-3)

    def test_free_mixture_has_zero_numeric_robustness(self):
        w = qbg.gold_cases()["causally_separable_equal_mixture"]
        result = qbg.solve_generalized_causal_robustness(w)
        self.assertTrue(qbg.solver_certificate_pass(result), msg=str(result))
        self.assertGreaterEqual(result["raw_robustness"], -qbg.FREE_ROBUSTNESS_TOL)
        self.assertLessEqual(result["raw_robustness"], qbg.FREE_ROBUSTNESS_TOL)

    def test_ocb_reference_has_positive_numeric_robustness(self):
        w = qbg.gold_cases()["OCB_causally_nonseparable_reference"]
        result = qbg.solve_generalized_causal_robustness(w)
        self.assertTrue(qbg.solver_certificate_pass(result), msg=str(result))
        self.assertGreater(result["robustness"], qbg.CNS_POS_TOL)

    def test_party_swap_is_involution(self):
        w = qbg.gold_cases()["OCB_causally_nonseparable_reference"]
        self.assertLess(
            np.linalg.norm(qbg.permute_parties(qbg.permute_parties(w)) - w, ord="fro"),
            1e-12,
        )


if __name__ == "__main__":
    unittest.main()
