# SESSION-20261016-001 — G1 handover validation preparation

2026-10-16 · PC2 / G1-29 · pre-lab, in progress; no motor commands issued.

Labbook refreshed from GitHub at `fffced8`; installed skill matches canonical
SKILL.md. LeRobot physical branch fast-forwarded to `a65596cb`, the handover
candidate identified by the new validation plan. Tracked code is clean;
pre-existing untracked MUJOCO_LOG.TXT left untouched.

## Completed no-motion checks

- 59 focused SDK/reference tests passed; architectural handover check passed.
- Network interfaces up: wired 192.168.123.164, Wi-Fi 192.168.0.201; RGB video4 exists.
- No matching previous teleoperation/camera/voice/CloudXR test process found.
- Read-only connect/observe/close/duplicate-close passed: 100 distinct feedback ticks,
  mode (5,0), finite observations, maximum sampled age 9.67 ms and arm speed
  0.0307 rad/s. Writer never created, arm authority never activated.
- SDK emitted `[Reader] take sample error` at cleanup; operation completed successfully.

## Recommended next task

[IDEA-20261015-003](../../ideas/IDEA-20261015-003/README.md): handover validation.
Use the existing [staged plan](../../ideas/IDEA-20261015-003/validation-plan-2026-10-15.md),
starting with a separately authorized near-zero handover at return_velocity=0.05 rad/s
(default is 0.5). Later stages need separate operator authorization.

Before motion, complete command/weight/phase telemetry and an independent feedback
observer extending five seconds beyond publisher close. Source review also found
that the fade begins with an exact-zero target after measured arrival below 0.05 rad;
check this transition against the plan's no-command-discontinuity criterion. The
return limit clips relative to measured position, not the previous command, so it
must not be described as a proven bound on consecutive command or measured speed.
No motion-ready claim is made yet.

Operator selected stage 2 (offline telemetry/continuity audit) and reported gantry
fitted, workspace clear, emergency control in hand, and standard mode.
VR E2E is dependent on handover validation. Camera performance, button-event capture,
and camera-aware redirect improvements remain lower-priority/deferred work.

Evidence and hashes: `~/robotics/artifacts/2026-10-16-g1-handover/`.
Read-only feedback is a preflight, not a physical motion run. No control process remains.

## Stage 2 — continuity failure, no physical motion

Offline execution of the actual return method at a65596cb with synthetic fresh
feedback fixed at 0.04 rad produced 102 captured commands. At return_velocity=0.05
rad/s and period=0.02 s, the return target was 0.039 rad, followed immediately by
zero at fade entry: a 0.039 rad jump versus the 0.001 rad per-period budget.
The mocked clock does not model computation time. Authority weight decreased
monotonically to zero, and the method reported success despite this target jump.
This is command-generation evidence, not measured robot motion or a physical
velocity prediction. No DDS connection or hardware transport was created.

Physical handover remains blocked on target-continuity correction and regression
coverage. Live command/phase telemetry and an independent feedback observer
lasting five seconds beyond publisher closure still need completion before motion.
LeRobot control code was not modified in this diagnostic.

## Upstream comparison — return command semantics

Reviewed current GitHub xr_teleoperate main robot_arm.py and local revision
278a3dcc669eb54b0fd5ed26031e420bc7f42e88 (same relevant G1-29 behavior).
In motion_mode, go_home sets the shared goal to zero, waits up to 100 x 50 ms
for all measured arm angles below 0.05 rad, then changes weight 1 to 0 in 101
steps with 20 ms sleeps. Its separate 250 Hz publisher continues measured-relative
position clipping during the fade. The feedforward-zero assignment is commented
out: previous feedforward is retained. go_home returns None even on timeout;
its return is not a physical completion acknowledgement.

Our a65596cb fade instead writes exact-zero targets and zero feedforward.
The reproduced 0.039 rad target discontinuity remains valid, but 39x denotes a
comparison with the configured per-period target offset, NOT 39x measured motor
speed. Both measured-relative limiters bound command-to-measurement offset rather
than consecutive commanded position or physical joint speed.

Unitree's G1 arm7 SDK example identifies motor_cmd[29].q as weight (1 enables,
0 disables arm_sdk), distinct from arm motor q position targets. The examples do
not expose the firmware blending equation or guarantee a collision-free stock
trajectory. SDK Write success indicates a local DDS write without a caught error,
not motor execution or handover acknowledgement. No robot commands issued.

Sources: https://github.com/unitreerobotics/xr_teleoperate/blob/main/teleop/robot_control/robot_arm.py
and https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm7_sdk_dds_example.py.
Next: preserve continuous target generation through fade, explicitly decide
feedforward behavior, then test and instrument before physical execution.

## Implemented correction — offline validated, physical validation pending

At operator request, changed the working tree over a65596cb to keep measured-relative
position clipping throughout the authority fade, publish at the control cadence,
and retain the last successfully published feedforward during return/fade. The
reference publisher only gains feedforward bookkeeping for this shared handover;
its tracking behavior is unchanged. Updated user documentation clarifies that the
velocity parameter limits target offset, not actual joint speed.

63 focused SDK/reference tests passed (two CUDA/pygame environment warnings), Ruff
and architectural checks passed. Coverage includes 50/250 Hz fade timing, nonzero
residuals, retained feedforward, changing feedback, stale feedback and idempotence.
The same diagnostic now reports zero fade-entry target jump and 20 ms separation,
with monotonic weight to zero. This supersedes the offline continuity blocker for
this patch only, not the remaining physical validation requirements. Snapshot:
`stage2-fixed/implementation.patch`; code remains uncommitted. No motor commands.

Next: complete live command/phase telemetry and independent post-close feedback
capture before a separately authorized near-zero physical return. Retaining the
last feedforward is upstream-compatible but is not recomputed gravity compensation
for changing posture; actual handover motion remains unverified.

## Committed revision retest

Committed code/docs/tests as `ca04051f570e4df1fa1d49f84ce39fd623ecbc2f`
on work/g1-vr-physical. Retested this exact revision: 63 focused tests passed,
two CUDA/pygame warnings; Ruff lint/format and architecture checks passed.
Offline reproduction again measured zero fade-entry target jump, 20 ms write
separation and monotonic authority decay to zero. Tracked tree clean; existing
MUJOCO_LOG.TXT left untracked. Code commit remains local (push not requested).
No hardware motion test; instrumentation/physical validation remain pending.

## Capture readiness and physical starting-pose prerequisite

Prepared temporary capture/observer harness over ca04051f plus a five-line
logging-only handover-phase patch (uncommitted, preserved). The phase field is
telemetry, not a new VR state-machine state. Mock capture passed with 102 commands,
return/fade phase, measured q/dq, commanded q/tau, weight and publication outcome.
63 focused tests, Ruff and architecture checks passed. Command capture is bounded
in memory; an independent read-only process writes feedback and continues five
seconds after controller closure. Motion is disabled by default and requires both
--motion and an operator typing MOVE. No headset/camera or new SDK publishing path.

First read-only attempt failed on a temporary harness str/Path conversion, before
control connection; fixed and rerun. Second attempt passed: 269 distinct feedback
ticks, maximum sampled age 12.07 ms, maximum sampled arm speed 0.0368 rad/s, and
5.013 seconds captured after closure. No writer created; no authority activation.
SDK Reader cleanup warning occurred, exit status zero. No competing control process
was found before the check.

The robot is NOT at the near-zero entry pose: elbow angles 1.218/1.228 rad, versus
<0.04 rad required for every arm joint. The harness correctly reports not ready
and will refuse activation. Operator reported standard mode, gantry, clear workspace
and emergency control earlier. These do not establish the required starting pose.
Next manual intervention: establish a reviewed near-zero pose with the normal robot
procedure, or separately plan/authorize a slow preparation from the current bent
pose. Do not silently expand the near-zero experiment to include that trajectory.
Also record video of both arms for physical handover. Initial physical experiment
is a measured-pose hold with a five-second authority blend, then normal return at
0.05 rad/s; deliberate offsets remain subsequent tests. Physical motion untested.

Harness: `/tmp/g1-handover-ready/run.sh`; use a new --root for each attempt.
Full scripts, exact configuration, patch, failed/successful logs, and sample traces
preserved under the readiness artifact directory. No control process remains.

## Lowering preparation — offline feasibility, execution blocked

Operator accepted the proposed slow lowering/hold flow and reported ready.
A fresh read-only check captured 262 distinct ticks, max sampled feedback age
9.65 ms, and 5.031 s after closure; no writer or activation. Sampled maximum
arm speed over the entire observation window was 0.0552 rad/s.

Offline quintic interpolation from the measured bent pose to joint zero requires
115.1 s at peak target speed 0.02 rad/s; sampled targets satisfy model joint limits,
and peak modeled gravity torque is 3.643 Nm (<5 Nm). This is feasibility evidence,
not collision certification or a physical tracking result.

Source review identified a limitation in the proposed hold-for-inspection flow:
G1ArmSDK._run invokes return_to_stock in finally after a fatal fault, and close
can also initiate return. A normal zero-pose hold does not prevent those paths
from requesting handover before operator inspection. The prior recommendation
omitted this distinction. No lowering or authority takeover was attempted.

Next: resolve preparation-specific fault/exit behavior before executing the new
lowering flow. Preserve fresh-feedback and torque guards; do not bypass them or
claim a guaranteed software hold after feedback/transport loss. Physical emergency
behavior and unexpected stock takeover remain material residual risks. No new
motion authorization is inferred from this record.

## Operator-reviewed principle: avoid circular failure-handling validation

When validating a recovery/failure-handling procedure, do not require that same
unvalidated procedure to be a proven-safe fallback for its own test. Failure during
recovery must be covered by an independent lower-level layer appropriate to the
experiment: gantry/support, clear workspace, and an operator with emergency control.
Define the recovery behavior being tested, its assumptions and abort conditions,
and the independent coverage before execution. Keep existing software guards and
record faults; do not recursively add unvalidated software recovery layers as a
prerequisite. This does not establish safety after transport/process failure or
prove that the recovery works; physical results remain pending until observed.

For this session, validate normal slow lowering, measured arrival/inspection hold,
and then separately confirmed authority fade. A fault aborts the experiment and
requires operator intervention under the independent physical coverage. The prior
claim that preparation fault/exit behavior must first be redesigned is superseded:
it imposed circular validation. Existing fault-triggered return remains a disclosed
residual risk, not a newly validated behavior. Operator accepted this principle and
instructed proceeding with experiments. Normal completion must not auto-fade before
inspection; fault behavior is distinct from normal completion.

## RUN-20261016-001 — takeover abort, no planned lowering

Operator-authorized lowering attempt aborted during initial measured-pose hold.
14 unchanged-position commands ramped authority from 0.004 to 0.056. The left-elbow
velocity guard reported -1.9374 rad/s (>0.1); fallback published 250 return commands,
timed out before arrival, and closed. No fade commands. Independent feedback
continued 5.031 s after closure; all experiment/observer processes exited.
Operator reported stationary afterward, no clear arm movement seen, and arms never
raised to level. No raise was commanded; the initial pose was the measured posture,
with elbow flexion about 70 degrees, not the predefined raised ready pose.

Encoder samples from first command to closure (~7.17 s) show left elbow 69.80 to
58.85 degrees (10.95 degrees excursion) and right elbow 70.35 to 58.40 degrees
(11.96 degrees). About 6.5 degrees per elbow was observed in the ~0.40 s takeover
window. These are encoder measurements, not IMU-derived travel or Cartesian hand
distance. Phase-boundary sampling gaps limit exact attribution. Preserve the
operator observation alongside these measurements; takeover dynamics remain
unexplained. No automatic retry and no guard relaxation. Next: investigate the
low-authority takeover behavior before another physical attempt.

## Prepared 65-degree inspection pose and voice cue (offline only)

Operator accepted the fixed-pose experiment and requested a voice cue at inspection.
Temporary inspect65.py fixes both elbows at 65 degrees and the other twelve joints
at the exact recorded initial hold targets from RUN-001. This specifies the whole
pose without inventing a raised-arm posture. It checks positioning and zero-return
paths against model joint/workspace/feedforward bounds before activation.
Return deadline is 120 s for the 0.05 rad/s setting, rather than the unsuitable
five-second deadline; this is a timeout, not a physical-speed guarantee.

English voice and matching terminal message: "Arms at the inspection position.
Holding. Please inspect." Emitted once after all measured joints are within
0.04 rad of the inspection target and all speeds below 0.05 rad/s for one second,
after the target interpolation completes. SDK language flag is 1 (English).
Normal inspection hold waits for explicit handover. Mock test passed: initial
measured-pose target continuity, <=0.02 rad/s target speed, five seconds of hold
without auto-close, explicit handover, and exactly one inspection voice cue.
No new physical test or speaker audibility verification was performed. Previous
takeover fault remains unresolved; this preparation does not mark it validated.

## RUN-20261016-002 — positioning interrupted; cleanup capture limitation

Takeover reached full authority, then the right wrist yaw velocity guard tripped
at -0.1227 rad/s against 0.1. Last positioning progress was 6.14/18.44 seconds;
elbows around 60 degrees. No inspection prompt or normal fade occurred. Operator
reported stationary, barely visible movement, and requested higher speed for visual
validation. Saved trace contains 445 normal and 4608 return commands; zero fades.

The 120 s configured return uses a step count, while close joins with a wall-clock
timeout. The publisher was still returning when close raised "Arm publisher did
not stop; operator intervention required". Process subsequently exited; no matching
test/observer processes remain. The harness wrote its publisher-closed marker even
though close failed, and captured commands continued after that marker. Therefore
five-seconds-after-actual-closure capture is NOT established for this run. Preserve
this instrumentation defect; do not reuse the marker as physical closure evidence.
Next: fix timeout accounting and closure reporting; assess target speed and the
wrist guard separately before another run. No automatic retry or guard relaxation.

Upstream comparison refreshed: G1-29 go_home uses target clipping, a measured
absolute-angle arrival threshold of 0.05 rad, roughly five seconds of arrival
polling, and then a two-second authority fade. That Python path has no measured
speed trip, torque trip, tracking-error trip or stale-feedback guard. Our observed
0.1 rad/s trip is local controller behavior during normal positioning, not an
upstream go_home guard. Firmware-level protections are outside this source review.

## Operator constraint — no additional return-to-stock gates

Operator instructed: "do not add any other gate outside the unitree return-to-stock
guard." Do not introduce additional speed, torque, tracking-error, pose, dwell or
inspection requirements inside the return/fade routine beyond the Unitree reference
behavior. The inspection hold belongs to the normal experiment before an explicit
handover request, not inside return-to-stock. Preserve the independent physical
coverage principle rather than inventing recursive software prerequisites.

No controller change made in response to this instruction. Existing code still
contains missing/stale/nonfinite feedback checks in _return_snapshot; these were
already present and must not be misrepresented as upstream-equivalent. The 0.1
rad/s trip from RUN-002 is in normal positioning, not the return path. Any proposal
to remove existing checks must explicitly distinguish that from adding no new gates.

## RUN-20261016-003 and operator-requested gating alignment

Elbow-only trajectory speed increased to 0.05 rad/s; other twelve targets held at
activation pose. Before that trajectory began, right wrist yaw speed tripped at
0.5584 rad/s versus 0.1, at authority 0.044. Operator saw little arm movement and
noted whole-body balance adjustments may accompany raising. Independent feedback
also showed a brief wrist encoder change; its cause remains unproven. No inspection
announcement. Return sent 4455 commands over 119.998 s, timed out without arrival
or fade, then transport closure succeeded. Independent capture continued 5.006 s
past verified closure. The wall-clock timeout/closure-reporting fix worked in this
failure case; return-to-stock itself did not pass.

Operator then directed removal of all non-Unitree gates, emphasizing that recovery
normally runs during exceptions and extra gates can prevent it from functioning.
Implemented explicit arm_sdk.unitree_gating=true in the next experiment. This
bypasses added measured-speed, torque/feedforward magnitude, posture, tracking-error,
position/workspace/displacement, caller/scheduling, feedback age/gap/tick and mode
change trips. Required finite data, explicit activation and publisher ownership
remain. Normal VR pickup/pause logic is untouched. Other profiles retain existing
behavior; the prepared experiment explicitly selects Unitree gating. No new gates
were added. Model torque/path values may be recorded without vetoing recovery.

67 focused SDK/reference tests, Ruff and architecture checks passed. New tests cover
motion/feedback conditions formerly causing trips, recovery despite the initiating
fault and old feedback, and failure to fade before measured arrival. The mock
experiment retains the English inspection cue and explicit handover request.
Prepared code is uncommitted over ca04051f; exact patch/harness preserved under
unitree-gating-preparation. No physical attempt with the changed gating yet.
Next: supervised elbow-only 65-degree test with the same independent physical
coverage, then operator inspection before normal return. No claim of full upstream
trajectory/lifecycle equivalence or guaranteed safety after transport failure.

## Final experiment readiness

Software: 246 G1 tests passed, 14 skipped; focused suite 69 passed. Lint, format and architecture checks passed. Live read-only capture received 243 fresh samples without creating a command writer and continued five seconds after verified closure. Capture overflow no longer aborts control; fade timing includes publication overhead. Exact patch and harness: `final-readiness` in the artifact registry.

Next experiment is ready for supervised execution: elbow-only 65-degree pose, target rate 0.05 rad/s, Unitree gating selected, English inspection announcement and hold, followed by a separate handover request. No physical motion in this preparation pass. Previous physical return timed out; successful handback remains unverified.

## RUN-004: inspection reached; return stalled

The revised profile reached the 65-degree SDK elbow inspection pose without a guard trip. Spoken warnings failed (SDK 3104); text prompts worked. After separate operator authorization, return published for 120 seconds but elbows remained near 65 degrees. No arrival or fade occurred. Transport closure and five seconds of subsequent feedback were captured. Successful stock handback is not established.

Correction: reported elbow degrees are SDK joint coordinates, not anatomical flexion. Slots 18/25 and radians-to-degrees conversion match local upstream. Both executed and upstream URDFs have elbow axis +Y and forearm extending approximately +X at q=0; increasing elbow coordinate rotates forearm toward -Z in the parent frame. Earlier statements that zero means straight and return-to-zero lowers the arms are unsupported/incorrect. No physical encoder offset was calibrated or changed; operator visual reference is pending.

Next: reconcile observed pose with the model coordinate convention, then review the small measured-relative return target offset (0.001 rad per publication); it is not a physical velocity guarantee. Do not change offsets merely to match the earlier incorrect angle description.

Operator confirmed arms mostly lowered, hands pointing downward at the reported inspection pose. This is consistent with the SDK/model convention; no encoder calibration offset is established.

## RUN-005: forward-facing preparation and successful handover

All-zero SDK arm targets produced the requested near-right-angle, hands-forward pose. Slow preparation used 0.05 rad/s target rate; operator inspected and approved. From this pose, measured return arrival was already satisfied: 101 fade publications lowered authority to zero over 2.00 s. Publisher closure and five seconds of feedback were verified; process exited normally. Operator reported the return was safe.

This demonstrates handover from the prepared pose, not reliable return motion from arbitrary poses. Right-wrist yaw peaked at 3.09 rad/s, 0.45 s after closure; the stock trajectory is not bounded by the slow preparation target rate. Voice announcements still failed (3104). Full trace and exact code/config: `inspection-forward-01` artifacts.

Future return tests follow the [operator-defined five-step protocol](../../ideas/IDEA-20261015-003/return-to-stock-test-protocol.md), with separate confirmations before handover and before proceeding to the next scenario.

## RUN-006: random scenario 1 failed; series stopped

Near-ready targets were within ±2 SDK degrees, but shoulder residuals prevented the scripted inspection announcement. Operator confirmed position; agent used main-process SIGINT to invoke central return while preserving the observer. This bypassed scripted inspection/handover voice and is a protocol deviation.

Return published 4,431 commands at full authority for 120 s, never arrived and never faded. Right-wrist pitch reached 31.44 rad/s at 43.21 s into return. This happened during active return publication, not after stock-only handback. Publisher closure and post-close capture were verified; process exited with failure. Operator observed forward waist bending, requested publication stop and reported switching to damp mode. Known control processes were absent after closure.

Scenarios 2–5 were not started. No more actuation is authorized by the remaining series plan after the stop request. Root cause is unresolved; this result must not be presented as a safe return. Current capture lacks waist/IMU measurements and external video.

Operator follow-up for RUN-006: the robot moved forward and the arms oscillated with progressively increasing amplitude; the motion did not stop. The operator described an apparent self-reinforcing loop. Growing oscillations and forward movement are operator observations; the feedback mechanism remains an unconfirmed hypothesis. The earlier damp-mode intervention remains recorded separately.

Operator clarified the intervention sequence: after the forward movement and growing arm oscillations, the operator used the emergency stop to put the robot into damp mode. The exact time relative to publisher closure is not established; message receipt order must not be treated as physical-event timing.
