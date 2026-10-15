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
