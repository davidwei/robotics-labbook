# SO101 recalibration and warning validation — 2026-10-23

Status: in progress; physical recalibration and warning tests are pending.

The operator reports that both SO101 arms were reassembled for greater rigidity.
Cameras are disconnected. The selected work is recalibration followed by supervised
teleoperation and recording validation for IDEA-20261022-001.

## Preparation and software evidence

Both previously identified USB adapters are present. Existing local calibration
files were backed up; fresh session-specific calibration directories are prepared.
The new leader calibration file is now present. Its gripper span is only 105 ticks
versus 1,171 in the prior file; full-travel capture is awaiting operator confirmation.
Follower recalibration remains pending. No motors were commanded by the agent.

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

The operator must confirm or redo the leader gripper range and complete follower recalibration first.
Then run gentle text-only teleoperation, voice teleoperation and two short diagnostic
recording episodes, one phase at a time, using the session runner. Recalibration
is intentional after reassembly, unlike the routine-preflight instructions in the
original test plan. New ranges are not yet validated.

The implemented warning checks angular tracking error (default 10 degrees; proposed
lab probe 2 degrees). It does not estimate one-second catch-up time. Cameras and image
recording are disabled; the planned dataset contains joint states/actions only.

No warning has been observed or heard in this session, and no physical test result
is claimed. Operator observations, actual run boundaries and errors remain to capture.

Evidence and commands: `/Users/dwei/lerobot/outputs/lab/so101-20261023/`.
