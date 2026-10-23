#!/usr/bin/env bash
# Run every frozen QICQ qualification exactly as the CI workflows do.
# Does not change any seed, threshold, or decision logic.
#
# Usage: scripts/run_all.sh [LOGDIR]
#   PY_SIM, PY_0A, PY_0AR, PY_0BI : python interpreters (default: python)
#     each should be Python 3.12.14 with that phase's requirements-lock.txt
#   OPENBLAS_CORETYPE : optional; see docs/REPRODUCIBILITY.md
set -euo pipefail
cd "$(dirname "$0")/.."
LOG="${1:-artifacts/run_logs}"; mkdir -p "$LOG"
PY_SIM="${PY_SIM:-python}"; PY_0A="${PY_0A:-python}"; PY_0AR="${PY_0AR:-python}"; PY_0BI="${PY_0BI:-python}"
{
  echo "commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "date: $(date -Iseconds)"
  echo "OPENBLAS_CORETYPE: ${OPENBLAS_CORETYPE:-<auto>}"
  for v in PY_SIM PY_0A PY_0AR PY_0BI; do echo "$v: $(${!v} -c 'import sys,numpy,scipy;print(sys.version.split()[0],"numpy",numpy.__version__,"scipy",scipy.__version__)')"; done
} > "$LOG/env.txt"

"$PY_SIM" simulations/hqc_phase1_design_audit.py --reps 3000 --seed 20260809 > "$LOG/hqc_phase1_design_audit.log" 2>&1

{ "$PY_0A" qbg/phase0a/test_qbg_phase0a.py
  "$PY_0A" qbg/phase0a/qbg_phase0a.py --seeds 100 --base-seed 20260909 --outdir artifacts/qbg_phase0a
} > "$LOG/qbg_phase0a.log" 2>&1

{ "$PY_0AR" -m unittest qbg.phase0ar.test_qbg_phase0ar -v
  "$PY_0AR" -m qbg.phase0ar.qbg_phase0ar --seeds 256 --base-seed 20260910 --outdir artifacts/qbg_phase0ar
} > "$LOG/qbg_phase0ar.log" 2>&1

{ "$PY_0BI" -m unittest qbg.phase0bi.test_qbg_phase0bi -v
  "$PY_0BI" -m qbg.phase0bi.qbg_phase0bi --outdir artifacts/qbg_phase0bi
} > "$LOG/qbg_phase0bi.log" 2>&1

grep -h "DECISION" "$LOG"/qbg_*.log
grep -h -A7 "Acceptance checks" "$LOG/hqc_phase1_design_audit.log"
