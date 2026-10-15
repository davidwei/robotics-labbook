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
