# SESSION-20261009-001 — G1-29 embodiment regression check

2026-10-09 · David Wei + Codex · onboard Unitree G1-29 · retrospective capture; post-lab review pending.

**Objective:** check whether [LeRobot's G1-23 embodiment change](https://github.com/huggingface/lerobot/commit/dd3d74b82832673666d6a2adb71bec18ea509219) preserves G1-29 hardware locomotion before later G1-23 testing. This record covers one Codex session, approximately 01:23–01:37 Asia/Shanghai, plus later capture and operator clarification; it does not cover the complete lab day.

## Physical activity and results

A five-second read-only DDS preflight received 2,170 samples with finite feedback for all 29 body joints. One supervised [experimental run](runs/RUN-20261009-002.yaml) connected the bridge and Holosoma controller, interpolated to the startup pose, then teleoperated for 120 seconds (approximately 01:28:18–01:30:18).

**Operator observation:** David reported that the robot and remote axes worked, clarifying the sequence as forward/back first, then sideways, then turning. **Recorded evidence:** all 29 body command slots were active; the client exited successfully, and its final DDS command had zero gains and torque on all 29 joints. The teleop loop measured 58.54 Hz against a 60 Hz target; the controller's 200 Hz value was a target, not a measured rate. All 75 focused software tests, Ruff and whitespace checks passed. This single demonstration supports the recorded behavior, not general reliability.

## Changes and important limitations

The run used exact upstream commit `dd3d74b82832673666d6a2adb71bec18ea509219` in an isolated checkout. No tracked robot source changed; the existing branch stayed unchanged. Runtime selected hardware `g1_29`, Holosoma, localhost bridge and remote-only operation, without cameras or display. Two temporary capture helpers were added and preserved externally.

The observer decoded `ly` from the wrong byte offset. My earlier claim that forward/back was unverified is superseded by the operator's explicit report; its timing still cannot be recovered independently from that field. Earlier joint-feedback inspection did not establish the forward/back interval. The production teleop used the SDK decoder, not the observer.

Bridge shutdown raised `ContextTerminated` and required SIGTERM after the client's passive disconnect. Native control was not restored. No unexpected physical motion was reported.

## Pending review and evidence

Review the decoder/capture correction, bridge cleanup and mode restoration, timing metrics, and how much this one run establishes about compatibility. Next-test questions: can corrected raw remote capture and video align axis inputs with motion, and can repeated G1-29 checks reproduce the result before sparse-slot G1-23 validation?

Gaps include exact axis timing/amplitudes, quantitative stability, achieved controller frequency, full dependency state and activity outside this agent session. No G1-23 hardware test occurred here. Detailed chronology, commands, warnings and corrections are in [timeline.md](timeline.md); capture coverage is in [session.yaml](session.yaml). [Evidence registry](evidence.json) references the original transcript and locally preserved artifacts with hashes; artifacts are outside Git and have no recorded remote backup. No reviewed findings or full post-lab analysis have been added.
