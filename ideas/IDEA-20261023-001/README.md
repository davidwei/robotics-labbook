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

## Trial observation and speech updates — 2026-10-23

Operator reported unexpected Awaiting alignment. Inspection of the available live log `outputs/lab/so101-20261023/state-machine-1792808388992959000.jsonl` found Lagging → Awaiting alignment at monotonic 5899.917826466, reason `nonprogress:elbow_flex`, boundary=null. Elbow measured 34.6813° unchanged for 101 samples / 3.690s preceding transition; leader and last pre-transition sent goal were 27.7363° (6.9451° error). Thus this was the nonprogress guard, not calibrated-boundary detection. Other joints were still moving; the operator did not perceive a stall. This discrepancy requires review; the log does not establish contact or cause. Available capture was partial/live and is not yet archived as a complete new physical run.

Speech changes pushed through `61b785b` on `lab/so101-intel-warning-20261023`: announce “Tracking” once on entry to Tracking, and “Stopping” once on entry to Idle, including initial Idle and completion of return-to-rest. Entry prompts bypass the repeating-warning cooldown, wait for current speech to finish and cancel/replace on state change. 21 controller/runner tests passed; Ruff passed. Restart runner to load changes. Physical audibility of these new prompts remains unverified. Next action: review the reported nonprogress discrepancy and capture complete run provenance before claiming a physically validated recovery detector.

## Pre-transition motor history — 2026-10-23

At operator request, `fc5040e4c4d0024d3251a6865f6348b1561054c9` adds a rolling 3s buffer for every follower motor: torque enable, current, load, temperature, voltage, velocity, status and moving. One register per eligible control iteration, minimum .05s spacing, same serial owner, no retries; timestamped errors preserved. Each Lagging → Awaiting alignment writes `pre_alignment_motor_history` in session JSONL with all buffered reads plus reason, positions, errors and previous command. Individual reads are also logged continuously. Snapshots perform no serial I/O; incomplete startup history is marked. Values are raw driver-decoded register units, not measured torque. No new physical validation; 27 focused history/diagnostic/controller/runner tests and Ruff passed. Next action: restart supervised runner and reproduce the unexpected transition gently; inspect elbow current/load and goal/position history before changing thresholds. Missing earlier current/load readings cannot be reconstructed.

## Latest completed trial review — 2026-10-23

Log `state-machine-1792809011865027000.jsonl`, executed revision `fc5040e4c4d0024d3251a6865f6348b1561054c9`: 2,061 samples over 76.35s; writer summary 3,270 submitted/written, zero dropped. Idle → Lagging .91s, Tracking 8.26s, Lagging 14.23s, Awaiting alignment 45.57s. Trigger was `nonprogress:shoulder_lift`, not elbow or calibrated boundary. Shoulder actual 11.8681°, requested 6.5055° (5.3626° error); pre-transition shaped goal 6.4181°. Shoulder position was exactly unchanged for the last 2.932s (79 samples); its progress window was insufficient for the sustained timeout before that exact plateau began. Bounds ±105.2308°, far from either endpoint.

The buffered 3s motor evidence contains five reads per dynamic register, no read errors. Shoulder torque-enable=1, status=0, velocity=0, Moving=0 throughout sampled reads; load 248–264, current 22–29, voltage 47–49, temperature 25–26, all raw driver-decoded units. Elbow was still approaching: approximately -34.24° to -52.70° over 3s; leader -83.12° and last goal -61.60° at transition. Elbow current 53–101, load 416–552, voltage 47–48, temperature 29; no sampled disabled torque or status fault. Wrist flex also progressed approximately 56.13° → 41.19°. Whole-arm disengagement was caused by one joint's nonprogress despite others moving.

Interpretation: consistent with a static load/friction/PD residual at the shoulder, but not a confirmed cause or obstruction. Large leader/follower error in moving joints also includes deliberate 5°/s setpoint shaping; distinguish leader-vs-command backlog from command-vs-follower servo error before tuning the detector. No software changes or new actuation during this review. Next action: inspect the shoulder pose/clearance and characterize its settled residual before choosing per-joint thresholds or altering recovery rules.

## Simulation inputs: online servo documentation — 2026-10-23

Operator states assembly matches the public SO101 version. Nominal URDF provides inertial properties: https://github.com/TheRobotStudio/SO-ARM100/blob/main/Simulation/SO101/so101_new_calib.urdf . Joint mapping/calibration offsets still require verification.

Primary online references checked: FEETECH STS memory table https://ftservo.github.io/ftservo-wiki/en/reference/parameter/memory-sts/ ; manufacturer evaluation https://www.feetechrc.com/20210430-56680.html ; supplier specifications https://docs.waveshare.com/ST3215_Servo . FEETECH table describes position P coefficient with 1/4 scaling, D with 1/8, I and integral limit; this does not establish SI torque gains or the controller sample period. Manufacturer describes load as motor voltage duty-cycle output, full scale 1000; current 6.5mA/count and voltage .1V/count. PWM is not measured joint torque. Supplier lists separate 12V/7.4V variants: stall torque 30/19.5kg.cm, no-load speed .222/.192s per 60°, stall current 2.7/2.5A, torque constants 11/7.8kg.cm/A and backlash ≤.5°. These are nominal specifications at rated conditions, not guaranteed performance for this motor/firmware or ~5V logged operation.

Available information supports an approximate voltage/effort-limited PD actuator with uncertainty sweeps. Exact digital control law, timing/filtering, friction and installed variant remain unverified; do not use register P=16,D=32 directly as Nm/rad and Nm·s/rad, or multiply load percentage by stall torque as a calibrated torque estimate. Next agent action: pin public model/document revisions, confirm coordinate mapping and parameter uncertainty before gravity/no-gravity replay. No simulation or physical test performed in this lookup.

## Four-model gravity simulation completed — 2026-10-23

[Simulation report](gravity-simulation.md) preserves the four nominal voltage/gravity combinations, parameter sensitivity, plots/artifacts, source revision and limitations. Gravity-on produces a shoulder offset in the observed direction and improves trajectory agreement under assumed actuator dynamics; gravity causality and servo identity remain unvalidated. Software tests passed. Next action: review results and verify coordinate/actuator assumptions before physical model identification or threshold changes.

## Advisory monitor and pickup guidance — 2026-10-23

Implemented/pushed through `cd7bb94` (`8668136` feature checkpoint): NumPy URDF gravity torque at measured/requested poses, nominal continuous-torque utilization and static-error predictions for both servo variants, calibrated-boundary proximity and empirical effort/response detector. Advisory only: commands and transition rules unchanged. Logs retain model disagreement, voltage mismatch, raw evidence and pre-alignment prediction. No extra serial reads beyond existing diagnostics. Settings/model hash recorded in metadata; per-joint errors compare sent target to measured pose to avoid treating leader backlog as motor failure.

Effort detector requires growing same-direction command error, increasing corrective command demand, insufficient follower progress and flat/nonzero fresh load or current over a window plus dwell. A constant-effort/constant-error plateau alone does not prove saturation. Stale/error readings suppress evidence. Initial thresholds are empirical and configurable, not validated physical limits.

Validation: 44 focused robot-environment tests and five simulation tests pass; Ruff passes. Direct real-time COM gravity calculation agrees with MuJoCo bias-gravity at three test poses within 2e-6 Nm. Offline replay emits 687 predictions; timing median 1.63ms / p95 1.97ms / max 8.85ms (one local run), default update ~10Hz alongside 30Hz control. Before the prior recovery: estimated measured-pose shoulder gravity .5325Nm, requested-pose .2802Nm; 12V utilization .543 / predicted error 3.98°, 7.4V utilization 1.086 / error 6.12°. Prediction `possible_load_boundary`, models disagree, measured voltage 4.9V mismatches both nominal models. Empirical limiting detector correctly does not flag this plateau: corrective demand was not increasing. No prediction is proof of safe/reachable operation or saturation. Results local under `outputs/development/so101-capability-final`; replay script is committed.

Operator reports difficulty matching leader to follower in pickup. Added display of aligned-joint count, live follower targets and signed leader movement for each failing joint; hold-still cue when all pass. Alignment tolerances and automatic-resume dwell unchanged. No hardware validation of this display/monitor yet; restart runner to load updates.

## Recovery discussion: “Retrace slowly” — proposed, not implemented

Operator proposes keeping follower following while leader retraces toward operational space, instead of exact frozen-pose matching. Plausible for load-related tracking limits if retraction reduces demand and follower can converge, but leader-path reversal does not guarantee retracing follower path or restoring reachability. A possible implementation requires explicit operator-held recovery enable, bounded current leader target with no accumulated target backlog, low speed, fresh feedback, and sustained alignment before normal Tracking. Suspected contact/fault must not automatically keep following. Current Awaiting alignment still holds measured entry pose; no retrace-following mode was enabled. Next action: agree recovery authority, entry reasons and motion envelope before coding/physical test.

## Stationary advisory display correction — 2026-10-23

Operator reported repeated shoulder/elbow/gripper advisories without leader motion. Latest available log `state-machine-1792818807007752000.jsonl` showed setup_hold, not active tracking: shoulder margin .7033°, elbow modeled 7.4V utilization .8379, gripper nearly closed. Monitor displayed static estimates each .5s and used the broader 2-unit proximity margin for an overly strong calibrated-boundary label. Through `9b9f15e`, console advisories are shown only during Tracking/Lagging, on classification changes; static estimates continue in telemetry. Calibrated outward-boundary advisory now uses .5-unit tolerance, while 2-unit proximity remains separate. No motion transitions or tolerances changed. 31 focused tests and Ruff pass. Source history preserves a corrected test-file editing mistake; original runner regression coverage restored. Physical validation pending; restart required. setup_hold means saved rest pose has not been reached; S explicitly returns to rest with a clear path before Space can Start.

## Outward-only position advisory — 2026-10-23

Operator requests no position-boundary advisory absent an outward tracking request. Implemented `9cd3ff0`: active Tracking/Lagging, near upper bound with requested target > measured +.1, or near lower bound with target < measured -.1. Proximity alone and inward/holding requests remain silent; proximity/margin still logged independently. Motion-state boundary trigger unchanged. 30 focused tests and Ruff passed; code pushed. Restart runner for validation.
