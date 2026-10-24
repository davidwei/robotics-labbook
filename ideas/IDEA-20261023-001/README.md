# IDEA-20261023-001 — SO101 pickup mode after loss of synchronization

Status: ready_for_lab for a supervised state-machine prototype; physical validation pending. Dataset recording integration remains planned.
Target: MoissanClub/lerobot, SO101 leader/follower. Physical validation: pending.

The operator requests a pickup mode when the follower is stuck or out of sync:
disengage following, prompt the operator to align the leader with the measured
follower pose, then resume without a target jump. The updated proposal uses alignment plus dwell for automatic resume; see the state-machine specification. Do not implement or
physically test this during the current threshold experiment.

Reference: [G1 VR session](../../sessions/2026-10-15-g1-vr-camera/session.md),
code reference `4d9d9724` on `work/g1-vr-physical`. It reports four virtual pickup
entries and 1,295 following samples without target jumps; physical hold was not
validated and physical preparation failed before pickup. Reuse the alignment
concept, not unverified physical-stop or authority-handover assumptions.

Next agent action: after reviewing threshold telemetry, design the SO101 pickup
state machine and follower hold policy, inspect G1 code/evidence at exact revisions,
and add mocked/simulation transition tests before supervised physical validation.
Prerequisites: fresh feedback, defined per-joint alignment tolerances and dwell,
a defined continuous resume policy, and a distinction between lag, an obstacle and hardware fault.
Do not assume large position error proves a collision. Never keep commanding an
unreachable leader target or automatically force/reverse through an obstruction.
Torque-off can drop an unsupported arm; holding can sustain contact force. The
recovery policy and operator support/obstacle-clearance steps need explicit design.
Recording must mark or pause/discard interrupted episodes during pickup.

Current threshold logging is observational and does not implement pickup or any
automatic motion/stop behavior. No physical pickup validation is claimed.

## Session closeout — 2026-10-23

See [session handoff](../../sessions/2026-10-23-so101-reassembly-warning/handoff.md). Audible angular-error warning physically confirmed; catch-up-time accuracy and threshold selection unresolved. Pickup recovery and manual recording gates remain proposed/unimplemented. Next agent action: review static PD residual and reachable limits before threshold decisions, then specify pickup hold/resume policy. Target: MoissanClub/lerobot, SO101; prerequisites: operator, verified setup/calibration and clear workspace. Physical validation remains incomplete.

## State-machine design update — 2026-10-23

[State-machine specification](state-machine.md) records Idle, Lagging, Tracking, Awaiting alignment, Returning to rest and Fault; keyboard triggers; distinct boundary/nonprogress transitions; automatic alignment-dwell resume; and unresolved holding/initialization/fault policies. This supersedes earlier explicit-resume wording. Status: design proposed, implementation and physical validation pending. Next agent action: resolve the specification’s open policies before coding.

## Implementation checkpoint — 2026-10-23

Implemented the isolated supervised prototype at [c253a77](https://github.com/MoissanClub/lerobot/commit/c253a774f4d791f03bd47a6dfff0ded7ff009246), branch `lab/so101-intel-warning-20261023`. [Test guide](https://github.com/MoissanClub/lerobot/blob/c253a774f4d791f03bd47a6dfff0ded7ff009246/workbench/so101_intel_mac/STATE_MACHINE_TEST.md) contains setup, commands, parameters and limitations. Existing teleoperate/record entry points remain unchanged; shared Controller is available for future recording integration.

Software validation: 54 focused tests passed, including fake-motor trajectory/state tests, real runner with mocked buses and serial-failure cleanup; Ruff passed; CLI help started locally. Historical replay processed 1,347 samples, entered Lagging at sample 1 and Awaiting alignment at sample 1073 for shoulder/elbow nonprogress. Replay is classification of fixed recorded measurements, not a counterfactual physical simulation. It excludes unrecorded gripper and used a synthetic zero rest solely for offline initialization. The first recorded elbow exceeded the calibrated endpoint but target pointed inward, so no outward-boundary transition was expected.

Resolved prototype policies: Awaiting alignment captures and holds measured follower pose; automatic resume after dwell is seeded from current follower pose. Esc latches Halted, requiring restart. Fault latches. Startup away from rest holds position in setup_hold until S explicitly requests return; Space is ignored outside Idle. Return blocks/timeouts fault; no automatic home on fault. Serial exceptions attempt a fresh measured-pose hold only if available, then wait for operator support before disconnect/release. Physical effectiveness remains unverified; holding may sustain force and feedback loss may leave the old servo goal in place.

Initial arm alignment tolerance 1.5° deliberately does not hide the known 3.43° elbow residual; inspect pose/error if alignment never clears. Settings are explicit trial parameters, not established safe limits or validated obstacle detection.

Next agent action: guide operator through rest-pose capture, config check and supervised gentle trial. Prerequisites: operator present, verified calibration/ports, clear swept space/rest path, no cameras required. No hardware was actuated during implementation. First validate P/pickup and S/Esc behavior without deliberate obstruction; assess nonprogress/boundary behavior separately. Dataset gates/cameras remain future work.

Replay evidence: [private compressed decisions](https://github.com/davidwei/robotics-labbook/releases/download/so101-session-20261023/historical-replay.jsonl.gz), SHA256 `ccd418d9354a4132a54f0ba142612d0e8d1683fc1ef7d55c45c1d6bc6974b6e4`. Original telemetry remains in the session evidence archive.
