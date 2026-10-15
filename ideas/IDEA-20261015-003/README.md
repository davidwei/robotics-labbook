# IDEA-20261015-003 — Controlled return and handover to the stock controller

- Status: validation_pending; RUN-20261016-004 reached inspection pose but return stalled.
- Target: MoissanClub/lerobot, work/g1-vr-physical; PC2/G1-29 guarded arm controller.
- Physical validation: pending; RUN-20261015-009/010 expose current fault/exit gaps.
- Operator requirement: return to stock requires much more care to avoid a dangerous trajectory.

## Implementation checkpoint

Code revision `a65596cb` (`Safely return G1 arm authority to stock controller`)
was pushed to `MoissanClub/lerobot:work/g1-vr-physical` on 2026-10-14. Normal
close and publisher faults now use one idempotent handover function: command zero
pose at a configurable velocity, require measured arrival, and fade the current
Arm SDK weight to zero over two seconds. Cleanup failures are recorded and shutdown
continues; there is no second fallback trajectory. A repository-local pre-commit
check rejects additional Arm SDK publishers and direct zero-weight release paths.

Software validation passed: 293 Unitree-focused tests passed and 16 skipped; the
focused handover suite passed 59 tests. Ruff, the architectural checker, targeted
mypy, Bandit and formatting checks passed. A negative checker test rejected a
synthetic direct shutdown publisher. This is software evidence only; no DDS or
physical robot execution was performed for this revision.

## Latest physical evidence

RUN-20261016-004 reached inspection hold; return timed out after 120 seconds with no fade. Voice failed with SDK 3104. Elbow readings are SDK coordinates, not anatomical flexion; zero is not a straight elbow. Physical offset calibration remains unverified. Next action: reconcile coordinate convention with operator observation and review the small measured-relative return target offset before another motion run. The prepared experiment below records the procedure just tested, not a pending successful handback claim.

## Prepared procedure

Run the prepared elbow-only 65-degree inspection experiment with operator participation,
gantry, clear workspace, regular action mode and independent emergency control.
Use the preserved `final-readiness` harness and patch over ca04051f; target rate
0.05 rad/s, `unitree_gating=true`. Announce measured arrival, hold for inspection,
then accept a separate handover request. The earlier near-zero starting-pose
prerequisite is superseded by the operator's fixed inspection-pose experiment.
Do not reintroduce extra gates or require recovery to validate its own fallback.

Software: 246 G1 tests passed, 14 skipped; capture mock and live read-only checks
passed. Physical attempts RUN-20261016-001/002/003 tripped during preparation and
did not establish successful handback. Latest preparation removes those custom
trips; physical validation of this candidate remains pending. Reference:
[Oct 16 session](../../sessions/2026-10-16-g1-handover/session.md).

## Required checks before physical E2E

1. Offline: bounded target progression and authority weight changes; fresh-feedback
   requirements; return interruption; arrival residuals; faults/timeouts; no unintended
   reference-controller selection; normal shutdown versus pause behavior.
2. Pre-lab: confirm current physical robot state, gantry, clear workspace, regular
   action mode and independent emergency control. Preserve exact patch/config.
3. Separate physical return test: observe and log actual joint speeds, errors,
   authority weight and operator-visible trajectory. Test cancellation/hold before
   attempting recovery faults. Establish stock handback behavior rather than infer it.
4. Complete actual bent-ready pose, then guarded VR pickup/pause/recovery and E2E.

Related evidence: [session](../../sessions/2026-10-15-g1-vr-camera/session.md),
[analysis](../../sessions/2026-10-15-g1-vr-camera/analysis.md), RUN-009 and RUN-010.
Preparation speed increase and removal of the reference path remain deferred.
