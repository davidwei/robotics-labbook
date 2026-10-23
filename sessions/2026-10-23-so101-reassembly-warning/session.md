# SO101 recalibration and warning validation — 2026-10-23

Status: in progress; recalibration completed; text warnings observed in one completed
physical teleoperation run. Voice and recording validation remain pending.

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
