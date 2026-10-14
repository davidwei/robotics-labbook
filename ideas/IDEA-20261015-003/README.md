# IDEA-20261015-003 — Controlled return and handover to the stock controller

- Status: proposed; first-priority prerequisite for further physical E2E.
- Target: MoissanClub/lerobot, work/g1-vr-physical; PC2/G1-29 guarded arm controller.
- Physical validation: pending; RUN-20261015-009/010 expose current fault/exit gaps.
- Operator requirement: return to stock requires much more care to avoid a dangerous trajectory.

## Next agent action

Review guarded G1ArmSDK lifecycle and front-box exit together. Design separate
normal return, pause/hold, recoverable-input-loss and hardware/transport-fault
policies before implementation. Preserve no headset handback and pickup on recovery.
Normal return should have an explicit slow trajectory, appropriate phase-specific
arrival/velocity/error criteria, and monitored gradual authority reduction after
arrival. Define timeout/cancellation behavior without silently turning every failure
into immediate stock release. Do not promise retained authority across process death
or lost transport. Upstream's ~2-second fade is a reference mechanism, not a safety proof.

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
