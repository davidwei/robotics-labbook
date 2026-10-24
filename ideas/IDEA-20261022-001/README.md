# IDEA-20261022-001 — Warn when an SO follower trails its leader

Project: SO-101 / LeRobot. Status: ready for lab.
Target: `MoissanClub/lerobot`, branch `so101demo`.
Physical validation: pending; no SO-101 hardware was moved or tested.

Objective: during SO leader/follower teleoperation and recording, warn the operator when any of the
five commanded arm joints exceeds its configured tracking-error threshold. Exclude the gripper because
contact can intentionally prevent convergence. Emit the text `slow down` and speak `Please slow down`
immediately, then at most once every five seconds while the condition persists.

Implementation state: commit `5da2b7467fc736260dcc5e148894d7a8f5525599` adds a generic normalized joint-error monitor with hysteresis,
enabled initially for the shared SO-100/SO-101 runtime family. It reads the existing observation and final
processed target without extra hardware I/O or action modification. A latest-only background notifier
serializes blocking speech, allowing one active and one replaceable pending warning without delaying the
control loop. Teleoperation and recording share the monitor; recording retains it across episode and reset
phases. The default SO threshold is 10 degrees and is configurable per joint.

Software evidence: 35 focused catch-up-monitor, teleoperation/recording integration, and `CycleTimer`
tests passed. Ruff check and formatting passed. Targeted mypy passed for the new monitor, teleoperation
integration, and monitor tests; checking `lerobot_record.py` also reports two pre-existing unused-ignore
errors on unchanged lines. This is software evidence only.

Lab start plan: follow [`lab-test-2026-10-23.md`](./lab-test-2026-10-23.md). Begin with revision and audio
preflight, then a gentle log-only teleoperation run at a deliberately low 2-degree threshold, followed by
speech-enabled teleoperation and a short local recording test. Do not restrain or obstruct the follower to
create persistent lag. Validate or tune the 10-degree default before treating it as a reusable operating
threshold.

Next agent action: assist the operator with the 2026-10-23 preflight and capture the exact run boundary,
configuration, logs, video reference, cadence summary, and brief operator observations in a physical session
record. Robot motion still requires explicit operator authorization at lab time.

Prerequisites: powered and calibrated SO-101 leader/follower pair, clear workspace, operator control,
audible host speech, and captured control/cadence logs. Labbook updates do not authorize robot motion.

## 2026-10-23 Intel Mac lab preparation

Session: [SO101 reassembly and warning validation](../../sessions/2026-10-23-so101-reassembly-warning/session.md).
The operator selected recalibration after reassembly, then camera-free teleoperation
and recording. A separate v0.4.4-compatible local port passed 44 focused software tests;
see the session for exact revision and deviations. Physical calibration/validation
remains pending. Next action: operator completes interactive leader/follower ranges,
then performs the gentle text-warning phase before voice and recording.

## Threshold measurement instrumentation

The operator confirmed audible warning operation and requests per-event catch-up
time estimates. Prior logs count notifications but lack joint telemetry. Local
Intel candidate `f6f59ca3cf8396dc8a254ce4c056f8593a88c8fc` now captures raw joint samples and correlates warning
IDs; 55 focused software tests and synthetic capture/analysis passed. Next action:
operator reruns the unchanged 2-degree test with telemetry. Hardware capture and
projection accuracy remain unverified. Pickup recovery is deferred to
[IDEA-20261023-001](../IDEA-20261023-001/README.md) after this experiment.

## Session closeout — 2026-10-23

See [session handoff](../../sessions/2026-10-23-so101-reassembly-warning/handoff.md). Audible angular-error warning physically confirmed; catch-up-time accuracy and threshold selection unresolved. Pickup recovery and manual recording gates remain proposed/unimplemented. Next agent action: review static PD residual and reachable limits before threshold decisions, then specify pickup hold/resume policy. Target: MoissanClub/lerobot, SO101; prerequisites: operator, verified setup/calibration and clear workspace. Physical validation remains incomplete.
