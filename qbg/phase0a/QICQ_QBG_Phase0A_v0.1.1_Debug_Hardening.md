# QICQ QBG Phase 0A — v0.1.1 Debug Hardening

**Parent:** QICQ-QBG-P0A v0.1  
**Class:** implementation / reproducibility hardening only  
**Claim ceiling change:** none

## Why this patch exists

The v0.1 qualification passed, but a post-qualification code audit found two implementation-hardening gaps:

1. G4 described local free-channel monotonicity while the implementation applied the frozen channel family to subsystem A only.
2. The QBG workflow installed broad dependency ranges, so a future dependency release could change a supposedly frozen numerical qualification.

## Frozen scientific content retained

No target family, threshold, seed schedule, resource definition, mimic family, gate decision rule, or Claim Firewall is relaxed.

The v0.1 result remains historical evidence for the original frozen execution. This v0.1.1 run is a stricter reproducibility/debug qualification and does not retroactively rewrite the v0.1 artifacts.

## Debug changes

### D1 — bilateral local-channel coverage

For every frozen G4 channel, the audit now checks the channel independently on subsystem A and subsystem B.

Pass condition remains:

$
N(\Lambda_{A/B}(\rho)) - N(\rho) \le 10^{-9}.
$

### D2 — numerical environment lock

The QBG workflow is pinned to Python 3.12.14 and:

- NumPy 2.5.3
- SciPy 1.18.1

These are the versions observed in the successful v0.1 main qualification run.

### D3 — CI trigger hardening

The QBG lockfile is itself a workflow trigger path. A numerical-environment change can no longer bypass QBG CI.

## Claim Firewall

A v0.1.1 PASS still establishes only two-qubit synthetic resource-proxy gate mechanics. It does not establish causal nonseparability, a Quantum Switch, indefinite causal order, a biological quantum mechanism, consciousness, or ontology.


### D4 — free-channel output validity

G4 now treats physical output validity as a prerequisite for monotonicity.
Every frozen local channel output must remain Hermitian, unit-trace, and PSD
within the existing physical tolerance. A malformed or non-trace-preserving
would-be free operation can no longer pass merely because it lowers
negativity.


## Amendment log (修正履歴)

All times are JST (UTC+9). Direction describes the effect on gate strictness relative to the parent version. No row changes a seed, threshold, tolerance, target family, mimic family, decision label, or the Claim Firewall.

| Version | Date (JST) | Commit(s) | Change | Direction | Rationale | CI run(s) |
|---|---|---|---|---|---|---|
| 0.1 | 2026-09-09 22:06 | `b37f825` (merge of PR #4) | Original frozen Phase 0A qualification | — (parent) | Initial freeze | main push run 34355035990: success (G0–G6 PASS, `P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS`) |
| 0.1.1 D1 | 2026-09-09 23:42 | `48e1fdc`, `9e22616` | G4 applies every frozen local channel independently to subsystem A **and** subsystem B (v0.1 audited A only) | stricter | Spec §5 says "local … channels"; the v0.1 implementation covered only one subsystem | 34365414760, 34365418922: success |
| 0.1.1 D2/D3 | 2026-09-09 23:42 | `5a8d7e1`, `3a7e61b` | CI pinned to Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1 via `qbg/phase0a/requirements-lock.txt`; lockfile added as a workflow path trigger | provenance only (no gate change) | Broad dependency ranges could silently change a frozen numerical qualification | **34365423881: FAILURE** on `5a8d7e1`: the workflow referenced the lockfile before the commit that added it (`No such file or directory: 'qbg/phase0a/requirements-lock.txt'`). This was a commit-order failure at the install step, before any scientific evaluation. Resolved by `3a7e61b` (run 34365428129: success). |
| 0.1.1 provenance | 2026-09-09 23:42 | `c7345c4`, `cc3e502` | Original manifest preserved byte-identical as `manifest_v0.1.json`; manifest version 0.1.1 with a `debug_hardening` block | none | Lineage preservation | 34365432450, 34365435388: success |
| 0.1.1 note | 2026-09-09 23:42 → 2026-09-10 07:09 | `cc3e502` → `1cd6afb` | `cc3e502` inadvertently respelled the manifest value `werner_p_max` from `1.0` to `1` (numerically identical). `1cd6afb` restored the frozen spelling `1.0`. | none (numeric value never changed) | Avoid meaningless manifest drift from the frozen v0.1 spelling | 34410785887: success |
| 0.1.1 docs | 2026-09-09 23:42–23:44 | `1fe2fd4`, `7ce41bf`, `4674c59`, `085c772`, `5e7bc8e` | Hardening record, README lineage, implementation header, and runtime banner derived from `VERSION` | none | Documentation and traceability | 34365602920 (push) / 34365609976 (PR): success |
| 0.1.1 D4 | 2026-09-10 07:08–07:10 | `94e4f64`, `dd1adf2`, `7922423`, `cddcac9`, `683bd2b`, `d87440d`, `557aa50`, `bdc3dce` | G4 requires every frozen-channel output to be Hermitian, unit-trace, and PSD within the existing physical tolerance before monotonicity can pass. Output validity and non-increase are recorded separately. Malformed-channel regression tests added. | stricter | A malformed or non-trace-preserving would-be free operation could lower negativity and produce a false monotonicity PASS | Final head `bdc3dce`: push 34410852101 and **PR 34410854079: success** (9 tests; G0–G6 PASS; `free_channel_outputs_all_physical = true`; `P0A_PROXY_QUALIFIED_WITH_OPERATIONAL_WITNESS`) |
| 0.1.1 docs | 2026-09-26 | this commit | This Amendment log, plus a cross-reference note under the §5 gate table of `QICQ_QBG_Phase0A_v0.1.md` pointing to v0.1.1 (v0.1 thresholds and text otherwise unchanged) | none (docs only) | Make the post-freeze amendment lineage explicit before freezing v0.1.1 on `main` | to be recorded by the PR CI run |

The v0.1 artifacts (run 34355035990) remain the historical record of the original freeze and are not rewritten. The tag `qbg-p0a-v0.1.1-frozen` marks the `main` merge commit of this version.
