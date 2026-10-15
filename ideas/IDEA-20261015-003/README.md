# IDEA-20261015-003 — Controlled return and handover to the stock controller

- Status: validation_failed for random scenario 1 (RUN-006); further physical tests stopped by operator.
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

**RUN-006 supersedes readiness to continue:** random scenario 1 produced large speed transients during the 120-second full-authority return, no arrival and no fade. Operator requested stop and reported damp mode. Publisher closure verified. Scenarios 2–5 were not run. Next action is offline evidence review, not motion. Inspection/voice orchestration also needs correction; do not add new recovery gates or infer root cause from torso-compensation speculation.

RUN-20261016-005 subsequently reached all-zero SDK arm coordinates using a slow ordinary trajectory, producing the requested hands-forward pose. Operator approved inspection and reported a safe return. Measured arrival was already satisfied; two-second authority fade and closure completed. This validates the prepared-pose handover case, not the stalled arbitrary-pose return of RUN-004. Post-close right-wrist speed peaked at 3.09 rad/s; voice error 3104 remains. Next: retain this successful baseline and review return trajectory semantics before broadening the claim.

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

Reusable procedure: [return-to-stock physical test protocol](return-to-stock-test-protocol.md), including separate inspection and post-return operator confirmations.

RUN-006 operator follow-up: forward robot movement and progressively growing arm oscillations that did not stop. An apparent self-reinforcing loop is the operator's interpretation, not an established root cause. Preserve this observation when reviewing the return controller and whole-body interaction.
