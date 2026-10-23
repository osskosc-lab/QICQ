#!/usr/bin/env python3
"""Compare two QICQ artifact directories for determinism.

Ignores wall-clock fields (e.g. SDP `solve_time`). Exits 1 on any other difference.
Usage: python scripts/compare_runs.py DIR_A DIR_B
"""
import json, sys
from pathlib import Path

VOLATILE = {"solve_time", "setup_time", "runtime", "elapsed", "timestamp"}

def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o

def main(a, b):
    a, b = Path(a), Path(b)
    bad = 0
    for fa in sorted(a.rglob("*")):
        if not fa.is_file():
            continue
        rel = fa.relative_to(a)
        fb = b / rel
        if not fb.exists():
            print(f"MISSING {rel}"); bad += 1; continue
        if fa.suffix == ".json":
            same = strip(json.loads(fa.read_text())) == strip(json.loads(fb.read_text()))
        else:
            same = fa.read_bytes() == fb.read_bytes()
        print(("same    " if same else "DIFF    ") + str(rel))
        bad += not same
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
