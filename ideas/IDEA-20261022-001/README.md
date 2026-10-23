# IDEA-20261022-001 — Warn when an SO follower trails its leader

Project: SO-101 / LeRobot. Status: in development; software implementation complete locally.
Target: `MoissanClub/lerobot`, branch `so101demo`.
Physical validation: pending; no SO-101 hardware was moved or tested.

Objective: during SO leader/follower teleoperation and recording, warn the operator when any of the
five commanded arm joints exceeds its configured tracking-error threshold. Exclude the gripper because
contact can intentionally prevent convergence. Emit the text `slow down` and speak `Please slow down`
immediately, then at most once every five seconds while the condition persists.

Implementation state: the local branch adds a generic normalized joint-error monitor with hysteresis,
enabled initially for the shared SO-100/SO-101 runtime family. It reads the existing observation and final
processed target without extra hardware I/O or action modification. A latest-only background notifier
serializes blocking speech, allowing one active and one replaceable pending warning without delaying the
control loop. Teleoperation and recording share the monitor; recording retains it across episode and reset
phases. The default SO threshold is 10 degrees and is configurable per joint.

Software evidence: 35 focused catch-up-monitor, teleoperation/recording integration, and `CycleTimer`
tests passed. Ruff check and formatting passed. Targeted mypy passed for the new monitor, teleoperation
integration, and monitor tests; checking `lerobot_record.py` also reports two pre-existing unused-ignore
errors on unchanged lines. This is software evidence only.

Next agent action: review and commit the code change, then prepare a physical SO-101 validation plan that
measures actual joint tracking error, warning timing, control-loop cadence, false prompts near the threshold,
and behavior with speech enabled/disabled. Validate or tune the 10-degree default before treating it as a
reusable operating threshold.

Prerequisites: powered and calibrated SO-101 leader/follower pair, clear workspace, operator control,
audible host speech, and captured control/cadence logs. Labbook updates do not authorize robot motion.
