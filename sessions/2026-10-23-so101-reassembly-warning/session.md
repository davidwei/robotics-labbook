# SO101 recalibration and warning validation — 2026-10-23

Status: in progress; recalibration completed; text warnings observed in one completed
physical teleoperation run. Voice operation is now operator-confirmed; predictive
threshold analysis and physical recording remain pending.

The operator reports that both SO101 arms were reassembled for greater rigidity.
Cameras are disconnected. The selected work is recalibration followed by supervised
teleoperation and recording validation for IDEA-20261022-001.

## Preparation and software evidence

Both previously identified USB adapters are present. Existing local calibration
files were backed up; fresh session-specific calibration directories are prepared.
Both new calibration files are present, with IDs 1..6 and positive ranges.
The leader gripper was recalibrated to a span of 1,149 ticks, resolving the earlier
105-tick capture concern; follower gripper span is 1,494 ticks. Both USB adapters
remain connected. The operator reports both calibrations complete; range-file checks
do not establish physical tracking accuracy. No motors were commanded by the agent.

The planned candidate `5da2b74` is based on newer LeRobot requiring Python >=3.12
and newer PyTorch. This Intel Mac retains its previously working v0.4.4 environment.
The joint-error monitor was ported to local branch `lab/so101-intel-warning-20261023`,
commit `acbd895405315c1e7f8f3e9d51114bf81a86ab63`. The port changes module/type locations and integrates with older
control loops; it does not include the newer CycleTimer instrumentation. This is a
separate candidate, not physical validation of the exact original revision.

Software checks: 44 focused monitor, loop-integration, mocked-follower and action
processor tests passed; focused Ruff checks passed. A camera-free config with a
2-degree threshold parsed successfully. These are software checks only.

## Physical validation and next action

Next: a supervised 30-second, camera-free, text-only teleoperation test at a
2-degree joint-error threshold, from similar starting poses.
Then run gentle text-only teleoperation, voice teleoperation and two short diagnostic
recording episodes, one phase at a time, using the session runner. Recalibration
is intentional after reassembly, unlike the routine-preflight instructions in the
original test plan. New ranges are saved; physical tracking with them is not yet validated.

The implemented warning checks angular tracking error (default 10 degrees; proposed
lab probe 2 degrees). It does not estimate one-second catch-up time. Cameras and image
recording are disabled; the planned dataset contains joint states/actions only.

Text-warning evidence is recorded below. Audible warnings and recording remain
unverified; no broad physical-validation claim is made.

Evidence and commands: `/Users/dwei/lerobot/outputs/lab/so101-20261023/`.

## Text test and audio preflight

The first text-only attempt aborted because follower motor ID 6 was not detected.
A subsequent 30-second attempt exited normally and logged seven `slow down`
messages. The operator confirmed seeing the warnings. Speech was intentionally
disabled, explaining silence in that test; smoothness and usefulness remain unconfirmed.

An agent-executed macOS `say` preflight returned success, but the operator heard
no sound. A voice-enabled attempt from the agent exited before connecting to
hardware because the sandbox denied access to the leader USB port. This is an
execution-environment limitation, not evidence of a robot or warning defect.
Next: test `say "Please slow down"` in the operator's own Terminal. If audible
and tracking was normal, run `run.sh teleop-voice` there before recording.

## Shorter speech prompt

The operator confirmed Terminal speech is audible, then requested the shorter
phrase "Slow down". Local code commit `75504316f16bb2bb50b1cebdb61986cff28dd54a` implements that wording;
12 focused monitor/integration tests and Ruff passed. A running process must
be restarted to load it. The shorter prompt is not yet physically validated.

## Warning analysis requested by the operator

The latest voice run logged 10 warnings; a preceding voice run logged one, and
the earlier completed text test logged seven (18 total notifications). The
operator reports the shorter warning works. Per-event catch-up time cannot be
calculated because joint positions, targets and velocities were not recorded.
See [analysis.md](analysis.md) for evidence limits and proposed telemetry. No
threshold or control behavior was changed during this analysis.

## Threshold-measurement logging ready

Local source commit `f6f59ca3cf8396dc8a254ce4c056f8593a88c8fc` adds opt-in raw positions/targets for all five
arm joints on every control tick, with software timestamps and warning sample IDs.
A bounded background writer reports drops/errors. No extra motor reads or target
changes are added. The session runner enables uniquely named telemetry automatically
and produces JSON/CSV catch-up projections after cleanup.

Validation: 55 focused tests and Ruff passed. A synthetic 301-cycle capture had
zero drops; event/sample matching and a known 0.25-second projection passed. These
are software checks; logging overhead and estimator accuracy on hardware remain
unverified. Next: operator reruns gentle 45-second `teleop-voice` from Terminal at
the unchanged 2-degree threshold. Catch-up values assume constant filtered follower
speed over a 100 ms window, within 0.5 degrees; unavailable/stationary/moving-away
cases are explicit, not converted into finite predictions.

Pickup recovery is the requested next feature after threshold analysis. See
IDEA-20261023-001. The G1 history provides a concept and virtual evidence, not a
validated physical hold/recovery procedure. No pickup or automatic motion changes
are implemented in this threshold-measurement candidate.

## Instrumented threshold test completed

Run 005 captured 1,347 samples with zero drops and nine warnings; operator reports
free motion without obstruction. The 2-degree monitor stayed active throughout.
Catch-up ratios are mostly unavailable and the one finite arm estimate is highly
window-sensitive. Offline threshold replay also exposed immediate rearming that
can increase announcement counts at higher thresholds. No new threshold is chosen.
See [analysis.md](analysis.md) for per-event interpretation and next checks.

Follow-up inspection found a 3.879-second elbow encoder plateau around warning
8, with approximately 10 degrees of requested error despite operator-reported
free motion. This is a sustained offset worth diagnosing; its cause is unknown.
See analysis.md. No automatic recovery or gain changes were applied.

## Supervised initial alignment diagnostic prepared

Operator requested an initial setup that waits for follower alignment and allows
inspection. Source commit `26b60dfc72cf4817326612e5a8c76091f3b9b390` adds a separate camera-free fixed-pose
alignment command. It seeds the follower's measured pose before standard holding
configuration, shows an initial difference table, and requires a second terminal
Enter before a goal ramp (5 degrees/s arm, 10 normalized units/s gripper).
It displays the frozen leader target, current leader, measured follower, motor
Goal_Position readback and error. Matching requires all arm errors <=1 degree
and gripper <=3 units for 1 second after the ramp, with the leader still close
to the snapshot. Leader movement does not retarget the follower. A 30-second
timeout or operator exit disables follower torque; operator support is required.

64 software tests and Ruff passed, including residual-error and leader-motion
nonalignment cases, seed-before-enable order and cleanup. Config files passed
the hardware-free check. No physical alignment run or seamless teleop handoff
is claimed. This diagnostic does not implement pickup recovery.

## Alignment inspection result

Two physical alignment checks did not reach the configured gate. The latest
ran 13.5 s with a stationary leader: elbow remained 3.43 degrees off despite
a matching motor-stored goal; wrist flex was borderline at 1.01 degrees.
The preceding 30-second run ended at the same residuals. The target-transmission
path is supported by readback at this pose; the cause of residual error remains
unknown. Next: stationary motor torque/load/current and configuration readback,
without changing gains or loosening the gate to conceal the elbow offset.

## Motor-state diagnostic candidate ready

Operator requested motor states in the setup/inspection workflow. Source commit
`603a7bc8bcee7619b7b2a843605239044631d051` extends the existing alignment script with startup snapshots for both
arms and timestamped, staggered follower register reads. Live display includes
torque enabled, raw current/load/temperature/status and elbow PID/dead zones.
Logs include operating mode, position/torque/protection limits, homing offset,
voltage, velocity and motion flags. Each optional diagnostic read records its
latency/error; failures are unavailable rather than substituted zeros.

One optional register read is scheduled per eligible control iteration, with a
0.15-second minimum between reads, using the owning serial thread. Fields are
not simultaneous. Values are raw register units after driver sign decoding, not
validated amperes/percentages or decoded fault flags. Alignment criteria and
range-calibration behavior are unchanged; no automatic gain tuning or fault
recovery is added. Startup goal display now uses real readback rather than the
seed value. 68 focused software tests and Ruff passed; config check passed.
Physical validation of this diagnostic candidate is pending. Next: operator
runs the same `align_so101.py` command to inspect the persistent elbow error.
