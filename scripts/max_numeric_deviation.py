#!/usr/bin/env python3
"""Max absolute numeric deviation between two artifact dirs (JSON leaves + CSV cells).

Ignores wall-clock fields. Prints per-file max deviation and whether decision.txt matches.
Usage: python scripts/max_numeric_deviation.py DIR_REF DIR_OTHER
"""
import csv, json, sys
from pathlib import Path

VOLATILE = {"solve_time", "setup_time", "runtime", "elapsed", "timestamp"}

def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in VOLATILE:
                yield from leaves(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{p}[{i}]")
    else:
        yield p, o

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def compare(a, b):
    worst, where, nonnum = 0.0, "", 0
    pairs = []
    if a.suffix == ".json":
        pairs = zip(leaves(json.loads(a.read_text())), leaves(json.loads(b.read_text())))
    elif a.suffix == ".csv":
        ra, rb = list(csv.reader(a.open())), list(csv.reader(b.open()))
        pairs = (((f"r{i}c{j}", x), (f"r{i}c{j}", y)) for i, (r1, r2) in enumerate(zip(ra, rb)) for j, (x, y) in enumerate(zip(r1, r2)))
    for (k, x), (_, y) in pairs:
        fx, fy = num(x), num(y)
        if fx is not None and fy is not None and not isinstance(x, bool):
            d = abs(fx - fy)
            if d > worst:
                worst, where = d, k
        elif x != y:
            nonnum += 1
    return worst, where, nonnum

def main(ra, rb):
    ra, rb = Path(ra), Path(rb)
    for fa in sorted(ra.rglob("*")):
        if not fa.is_file():
            continue
        fb = rb / fa.relative_to(ra)
        if not fb.exists():
            continue
        if fa.name == "decision.txt":
            print(f"{fa.relative_to(ra)}: decision {'SAME' if fa.read_text() == fb.read_text() else 'DIFFERENT'}")
        elif fa.suffix in (".json", ".csv"):
            w, k, n = compare(fa, fb)
            print(f"{fa.relative_to(ra)}: max_abs_dev={w:.3e} at {k or '-'}; non-numeric mismatches={n}")

if __name__ == "__main__":
    main(*sys.argv[1:3])
