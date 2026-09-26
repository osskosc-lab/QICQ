#!/usr/bin/env python3
"""Unit tests for the H_QC Phase 1 v1.2 design-audit analysis logic.

Synthetic checks of the analysis code only; not biological evidence.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hqc_phase1_design_audit as audit  # noqa: E402


def _dataset(effects, n_blocks=20, sd=6.0, seed=123):
    rng = np.random.default_rng(seed)
    scen = audit.Scenario("t", dict(zip(audit.ISOTOPES, effects)), residual_sd=sd)
    y = audit.simulate_dataset(rng, scen, n_blocks)
    cov = audit.simulate_covariates(np.random.default_rng(seed + 1), n_blocks)
    return y, cov


class HQCDesignAuditV12Tests(unittest.TestCase):
    def test_protocol_version(self):
        self.assertEqual(audit.PROTOCOL_VERSION, "1.2")

    def test_primary_ci_is_paired_t_with_b_minus_1_df(self):
        y, cov = _dataset((7.0, 7.0, 0.0, 0.0))
        r = audit.analyze_dataset(y, cov)
        d = (y[:, 0] + y[:, 1]) / 2.0 - (y[:, 2] + y[:, 3]) / 2.0
        lo, hi = stats.t.interval(0.95, df=len(d) - 1, loc=d.mean(), scale=stats.sem(d))
        self.assertAlmostEqual(r["delta_spin"], d.mean(), places=12)
        self.assertAlmostEqual(r["ci95_low"], lo, places=10)
        self.assertAlmostEqual(r["ci95_high"], hi, places=10)

    def test_additive_estimate_equals_paired_mean_for_complete_blocks(self):
        for n_blocks in (20, 22):
            y, cov = _dataset((5.0, 9.0, -1.0, 1.0), n_blocks=n_blocks, seed=7)
            r = audit.analyze_dataset(y, cov)
            self.assertAlmostEqual(r["additive_estimate"], r["delta_spin"], places=10)
            self.assertEqual(r["additive_df"], 3 * (n_blocks - 1))
            self.assertEqual(r["covariate_adjusted_df"], 3 * (n_blocks - 1) - len(audit.COVARIATES))

    def test_g9_requires_both_models(self):
        y, cov = _dataset((12.0, 12.0, 0.0, 0.0), sd=3.0)
        r = audit.analyze_dataset(y, cov)
        self.assertTrue(r["G9_additive"])
        self.assertTrue(r["G9_covariate_adjusted"])
        self.assertTrue(r["G9_robustness"])
        # Without covariates the covariate-adjusted component cannot pass.
        r_nocov = audit.analyze_dataset(y, None)
        self.assertTrue(r_nocov["G9_additive"])
        self.assertFalse(r_nocov["G9_covariate_adjusted"])
        self.assertFalse(r_nocov["G9_robustness"])

    def test_g9_fails_below_sesoi_estimate(self):
        y, cov = _dataset((1.0, 1.0, 0.0, 0.0), sd=0.5)
        r = audit.analyze_dataset(y, cov)
        self.assertGreater(r["additive_ci95_low"], 0.0)  # resolved but small
        self.assertLess(r["additive_estimate"], audit.G9_ESTIMATE_MIN)
        self.assertFalse(r["G9_robustness"])

    def test_g9_fails_when_ci_includes_zero(self):
        y, cov = _dataset((4.0, 4.0, 0.0, 0.0), n_blocks=3, sd=15.0, seed=11)
        r = audit.analyze_dataset(y, cov)
        if r["additive_estimate"] > 3.0:
            self.assertLessEqual(r["additive_ci95_low"], 0.0)
        self.assertFalse(r["G9_robustness"])

    def test_strong_requires_g9(self):
        y, cov = _dataset((12.0, 12.0, 0.0, 0.0), sd=3.0)
        self.assertEqual(audit.analyze_dataset(y, cov)["decision"], "STRONG_REPLICATION_STATISTICAL_CORE")
        self.assertEqual(audit.analyze_dataset(y, None)["decision"], "CONDITIONAL_SIGNAL")

    def test_covariates_shape_and_run_position_balance(self):
        cov = audit.simulate_covariates(np.random.default_rng(0), 22)
        self.assertEqual(cov.shape, (22, 4, len(audit.COVARIATES)))
        for b in range(22):
            self.assertEqual(sorted(cov[b, :, 2].tolist()), [-1.5, -0.5, 0.5, 1.5])

    def test_default_outcome_stream_unchanged_from_v11(self):
        # v1.1 simulate_dataset used a module-level 20-block loop with the same
        # draw order; the default-argument path must reproduce it exactly.
        rng_a = np.random.default_rng(20260809)
        rng_b = np.random.default_rng(20260809)
        scen = audit.SCENARIOS["target"]
        y_new = audit.simulate_dataset(rng_a, scen)
        block = rng_b.normal(0.0, scen.block_sd, size=20)
        y_ref = np.zeros((20, 4))
        for b in range(20):
            for j, iso in enumerate(audit.ISOTOPES):
                y_ref[b, j] = 20.0 + block[b] + scen.effects[iso] + rng_b.normal(0.0, scen.residual_sd)
        np.testing.assert_array_equal(y_new, y_ref)


if __name__ == "__main__":
    unittest.main(verbosity=2)
