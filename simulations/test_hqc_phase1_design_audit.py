"""Deterministic tests for the H_QC Phase 1 design audit v1.1.

Tests only; they import the frozen script and do not modify any threshold,
seed, scenario, or decision logic. Run:  python -m unittest simulations.test_hqc_phase1_design_audit -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hqc_phase1_design_audit as A  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Fixed-seed table recorded in simulations/PREFLIGHT_AUDIT_2026-08-09.md (rounded to 3 dp there).
RECORDED = {
    "null": (0.949, 0.000, 0.297, 0.000),
    "target": (0.948, 0.812, 1.000, 0.771),
    "spin0_confound": (0.017, 0.813, 1.000, 0.014),
    "one_spin_artifact": (0.949, 0.818, 0.107, 0.101),
    "weak_effect": (0.953, 0.006, 0.819, 0.006),
}


def run_frozen(seed=20260809, reps=3000):
    rng = np.random.default_rng(seed)
    return {s.name: A.audit_scenario(rng, s, reps) for s in A.SCENARIOS.values()}


class FrozenConstants(unittest.TestCase):
    def test_constants_match_preregistration(self):
        self.assertEqual(A.ISOTOPES, (129, 131, 132, 134))
        self.assertEqual(A.SESOI, 3.0)
        self.assertEqual(A.SPIN0_RED_FLAG_MARGIN, 3.0)
        self.assertEqual(A.N_BLOCKS, 20)
        self.assertEqual(list(A.SCENARIOS), ["null", "target", "spin0_confound", "one_spin_artifact", "weak_effect"])
        for s in A.SCENARIOS.values():
            self.assertEqual((s.residual_sd, s.block_sd), (6.0, 2.0))


class AnalyzeDatasetLogic(unittest.TestCase):
    def _y(self, effects, noise=None):
        y = np.tile(np.array([20.0 + effects[i] for i in A.ISOTOPES]), (A.N_BLOCKS, 1))
        if noise is not None:
            y = y + noise
        return y

    def test_clear_signal_is_strong(self):
        rng = np.random.default_rng(1)
        y = self._y({129: 10, 131: 10, 132: 0, 134: 0}, rng.normal(0, 0.5, (A.N_BLOCKS, 4)))
        r = A.analyze_dataset(y)
        self.assertTrue(r["G6_primary"]); self.assertTrue(r["G5_spin0_no_red_flag"])
        self.assertEqual(r["decision"], "STRONG_REPLICATION_STATISTICAL_CORE")

    def test_effect_below_sesoi_not_replicated(self):
        rng = np.random.default_rng(2)
        y = self._y({129: 2, 131: 2, 132: 0, 134: 0}, rng.normal(0, 0.5, (A.N_BLOCKS, 4)))
        r = A.analyze_dataset(y)
        self.assertFalse(r["G6_primary"]); self.assertEqual(r["decision"], "NOT_REPLICATED")

    def test_spin0_divergence_raises_red_flag(self):
        rng = np.random.default_rng(3)
        y = self._y({129: 10, 131: 10, 132: -4, 134: 4}, rng.normal(0, 0.5, (A.N_BLOCKS, 4)))
        r = A.analyze_dataset(y)
        self.assertTrue(r["spin0_red_flag"]); self.assertEqual(r["decision"], "CONDITIONAL_SIGNAL")

    def test_one_spin_artifact_fails_g7(self):
        rng = np.random.default_rng(4)
        y = self._y({129: 20, 131: -2, 132: 0, 134: 0}, rng.normal(0, 0.5, (A.N_BLOCKS, 4)))
        r = A.analyze_dataset(y)
        self.assertFalse(r["G7_directional_consistency"]); self.assertNotEqual(r["decision"], "STRONG_REPLICATION_STATISTICAL_CORE")

    def test_zero_variance_input_is_handled(self):
        r = A.analyze_dataset(self._y({129: 5, 131: 5, 132: 0, 134: 0}))
        self.assertAlmostEqual(r["ci95_low"], 5.0); self.assertTrue(r["G6_primary"])

    def test_wrong_shape_rejected(self):
        with self.assertRaises(Exception):
            A.analyze_dataset(np.zeros((A.N_BLOCKS, 3)))

    def test_block_shift_cancels(self):
        rng = np.random.default_rng(5)
        y = self._y({129: 7, 131: 7, 132: 0, 134: 0}, rng.normal(0, 1, (A.N_BLOCKS, 4)))
        shifted = y + rng.normal(0, 50, (A.N_BLOCKS, 1))
        self.assertAlmostEqual(A.analyze_dataset(y)["delta_spin"], A.analyze_dataset(shifted)["delta_spin"], places=9)


class FrozenRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = run_frozen()

    def test_determinism_same_seed(self):
        self.assertEqual(run_frozen(), self.a)

    def test_different_seed_differs(self):
        self.assertNotEqual(run_frozen(seed=20260810), self.a)

    def test_null_strong_is_zero(self):
        self.assertEqual(self.a["null"]["strong_replication_rate"], 0.0)
        self.assertEqual(self.a["null"]["G6_pass_rate"], 0.0)

    def test_matches_recorded_table(self):
        for name, (g5, g6, g7, strong) in RECORDED.items():
            r = self.a[name]
            for got, want in ((r["G5_pass_rate"], g5), (r["G6_pass_rate"], g6), (r["G7_pass_rate"], g7), (r["strong_replication_rate"], strong)):
                self.assertAlmostEqual(got, want, delta=0.0005 + 1e-12, msg=name)

    def test_acceptance_checks_pass(self):
        self.assertTrue(all(A.validate_operating_characteristics(self.a).values()))


class CommandLine(unittest.TestCase):
    def _run(self, *args):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, str(ROOT / "simulations/hqc_phase1_design_audit.py"), "--outdir", d, *args],
                               capture_output=True, text=True)
            out = json.loads((Path(d) / "audit_summary.json").read_text()) if p.returncode == 0 else None
            return p, out

    def test_cli_small_run_writes_outputs(self):
        p, out = self._run("--reps", "20", "--seed", "1")
        self.assertEqual(p.returncode, 0, p.stderr); self.assertIsNotNone(out)

    def test_cli_rejects_non_integer_reps(self):
        p, _ = self._run("--reps", "abc")
        self.assertNotEqual(p.returncode, 0)

    def test_cli_zero_reps_fails(self):
        # Documents current behaviour: --reps 0 is not a valid audit and must not exit successfully.
        p, _ = self._run("--reps", "0")
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
