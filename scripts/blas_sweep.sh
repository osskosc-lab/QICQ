#!/usr/bin/env bash
# Re-run 0A, 0A-R, 0B-I under several forced OpenBLAS kernels and report decisions + max numeric deviation
# against a reference artifact dir. Frozen commands/seeds only.
# Usage: scripts/blas_sweep.sh REF_ARTIFACT_DIR OUT_DIR [CORETYPES...]
set -euo pipefail
cd "$(dirname "$0")/.."
REF=$1; OUT=$2; shift 2
TYPES=("${@:-Haswell SkylakeX Sandybridge Zen Nehalem Prescott Core2}")
PY_0A="${PY_0A:-python}"; PY_0AR="${PY_0AR:-python}"; PY_0BI="${PY_0BI:-python}"
for c in ${TYPES[@]}; do
  d=$OUT/$c; mkdir -p "$d"
  OPENBLAS_CORETYPE=$c "$PY_0A" qbg/phase0a/qbg_phase0a.py --seeds 100 --base-seed 20260909 --outdir "$d/qbg_phase0a" > "$d/0a.log" 2>&1
  OPENBLAS_CORETYPE=$c "$PY_0AR" -m qbg.phase0ar.qbg_phase0ar --seeds 256 --base-seed 20260910 --outdir "$d/qbg_phase0ar" > "$d/0ar.log" 2>&1
  OPENBLAS_CORETYPE=$c "$PY_0BI" -m qbg.phase0bi.qbg_phase0bi --outdir "$d/qbg_phase0bi" > "$d/0bi.log" 2>&1
  echo "== $c"; python3 scripts/max_numeric_deviation.py "$REF" "$d"
done
