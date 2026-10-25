# Directional-advisory repeat preflight

Status: blocked after an operator-started powered preflight fault; the directional experiment did not begin.

## Powered preflight result

The runner entered `Idle` and commanded the saved folded rest pose. About 2.1 seconds later the follower `elbow_flex` motor reported status 32; the runner latched `fault` before the operator entered Tracking. The supplier register definition identifies status bit 5 (value 32) as load overload. All other motor status values remained zero.

Immediately before the fault, the saved elbow rest command was 94.46 degrees while the measured elbow was 103.34 degrees, beyond the calibrated upper bound of 94.90 degrees. This supports a direct observation that powered holding was attempting to reduce an approximately 8.9-degree rest error at the folded endpoint. It does not yet establish whether the cause is rest-pose capture, calibration/end-stop geometry, assembly orientation, or another mechanical issue.

The operator stopped the runner. The closed telemetry contains 3,024 records, a writer summary of 3,022 submitted/written and zero dropped records, and is archived as `state-machine-repeat-01.jsonl`. Do not restart this trial until the elbow can be checked unloaded and a rest pose safely inside the calibrated/mechanical boundary is established.

## Controlled comparison

- Reference: 2026-10-23 directional-advisory physical trial.
- Exact source: `MoissanClub/lerobot` revision `3cb506d168e4a36d580ac33a70f1711d7b98459e`, detached clean checkout at `/Users/davidwei/robotics/lerobot-so101-experiment`.
- Intended hardware difference: all follower motors were replaced with operator-reported 12 V variants and the follower now receives 12.2–12.4 V instead of the prior approximately 4.7–5.1 V.
- Required setup changes: fresh leader and follower calibrations and a newly captured rest pose. Their hashes are part of run provenance, so these changes are explicit rather than hidden experimental differences.

## Readiness evidence

- Isolated environment: `/Users/davidwei/miniforge3/envs/lerobot-so101-3cb506d`, LeRobot 0.4.4 editable from the exact checkout; dependency check passes.
- Software: 49 focused supervised-runner, state-machine, telemetry, capability-monitor, motor-history and diagnostic tests passed; focused Ruff check passed.
- Frozen calibration hashes: leader `37c2595a0b03f5225793fb7f2cb793313a62eb79ac9802f6313c774f5018611d`; follower `8a59e3d2c64201a30e4a9bd51dc365f59fb8782139978f300d87a8e84d9082b0`.
- Exact-revision read-only hardware check: both frozen files match the motor registers; all torque-enable values were zero; all status values were zero. Follower voltage was 12.2–12.4 V and leader voltage 5.1–5.2 V. Follower P/I/D was 16/0/32 on every motor.
- Rest pose was captured read-only in the intended folded configuration. Shoulder lift and elbow are inside but within 0.5° of their calibrated limits; proximity alone is expected at rest, but outward commands at those joints require particular care.
- Final offline runner check passed: configuration, calibration, rest-pose hash and controller settings.

## Minimum useful physical trial

1. Support the follower and start the runner; connection seeds measured-pose holding.
2. Confirm expected `Idle` if still at rest, or `setup_hold` if the pose changed. Do not press Space until the displayed pose/state is understood.
3. Keep leader/follower close, press Space once, and move gently without deliberate obstruction.
4. Observe whether Tracking is reached and whether direction-specific advisories occur under the new follower voltage.
5. If recovery occurs naturally, attempt pickup alignment once; do not deliberately jam the arm.
6. Exit on unexpected motion, nonzero status, inaccessible recovery, or telemetry failure. Support the follower before Q/Enter releases torque.

Success is a complete telemetry file with zero drops that permits comparison of tracking, nonprogress/recovery and advisory behavior. A successful demo does not establish reliability. Failure still produces useful evidence if the telemetry and exact run boundary are preserved.

