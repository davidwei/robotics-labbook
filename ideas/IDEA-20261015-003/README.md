# IDEA-20261015-003 — Controlled return and handover to the stock controller

- Status: offline target-continuity correction implemented and tested on 2026-10-16;
  live instrumentation and physical validation pending before further physical E2E.
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

## Next agent action

The Oct 16 commit ca04051f fixes fade-entry clipping and retains last published
feedforward; retesting that exact commit passed 63 focused tests. Complete live telemetry and the
independent observer before physical gates. Exact patch and diagnostic evidence:
[Oct 16 session](../../sessions/2026-10-16-g1-handover/session.md). Physical behavior
and retained-feedforward suitability remain unverified.

Then execute the staged [2026-10-15 validation plan](validation-plan-2026-10-15.md)
only with explicit operator authorization for each motion stage. Preserve no-headset
handback and pickup behavior. Do not promise retained authority across process death
or lost transport. Upstream's measured-arrival plus approximately two-second fade
is the implemented reference mechanism, not a safety proof.

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
