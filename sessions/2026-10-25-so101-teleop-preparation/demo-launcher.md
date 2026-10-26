# Demo launcher preparation — 2026-10-25

Operator plans a demonstration on October26: live camera views, record/replay two episodes, repeated replay, then25 manually bounded demonstrations. All activity should remain in one session, with the last successfully saved episode as current after interruption.

Implemented source [45531de](https://github.com/MoissanClub/lerobot/commit/45531deb7210761f384a65d238ce4120728b05da) on `lab/so101-intel-warning-20261023`. User-facing instructions: [DEMO_RUNBOOK.md](https://github.com/MoissanClub/lerobot/blob/45531deb7210761f384a65d238ce4120728b05da/workbench/so101_intel_mac/DEMO_RUNBOOK.md). Local convenience script `/Users/dwei/lerobot/demo_so101.sh` is copied from the committed workbench helper.

## Agreed controls and behavior

Ready screen has Start(S), Replay last(R), Quit(Q). Camera-only preview opens automatically at Ready, with no arm connection. Start stops preview, connects the regular recorder and records the next episode. Right Arrow/F finishes and saves. Left Arrow discards the active attempt and returns to Ready for manual reset; it does not return the follower home or automatically restart motion. Q during recording saves then quits. A five-minute maximum ends/saves an episode; idle waiting is unlimited and never starts recording automatically. No task-success detection.

Terminal-local keys avoid pynput/macOS Accessibility permissions. Launcher uses a private command file polled by the existing record loop; no competing serial reader. Normal timed recording remains available and unchanged by default. Each recording/replay uses a separate process and disconnects afterward. Regular record saving holds the last goal until encoding/finalization completes, then releases torque; operator support/reset is required. Physical effects during process failure/power loss are not guaranteed by data recovery.

Replay selects the most recent committed episode and does not advance the record index. Operator positions follower near the recorded first target and confirms before replay; there is no automatic alignment ramp. Two live camera views and two recorded-reference views are shown. Replay can repeat as desired.

## Organization and recovery

Each launch creates a unique session folder (timestamp/UUID), unless an explicit saved --session is supplied. One logical LeRobot dataset contains all successful episodes. Each attempt gets a unique stage, config, control file, console log and joint telemetry. The last complete dataset is cloned into the next stage; APFS copy-on-write or independent copy prevents changes to earlier checkpoints. Only completed saves are promoted and exposed through the session/dataset symlink. Failed/discarded stages are retained; completed orphan saves can be recovered from readable metadata after a launcher interruption. Calibration hashes prevent silent appends after recalibration. A session file lock, inherited by the child, prevents concurrent writers.

Validation is save integrity, not data quality: readable metadata, expected appended episode, action metadata consistency and referenced video presence. It does not reject low FPS, timing jitter, missing expected samples, poor tracking or task failure. Later quality review/interpolation remains separate. Filesystem corruption/lost storage is outside the recovery guarantee.

## Validation and readiness

24 focused tests passed, plus Ruff and CLI/config preflight. Coverage includes explicit start/finish/discard/Q, five-minute-style timed return, split arrow sequences, unique attempt paths, clone isolation, calibration-change rejection, locking, partial-save rejection, pointer recovery, complete-orphan-save recovery, two real synthetic camera episodes appended to one dataset, action/video selection for episode1, real record entry with mocked motors/writer finalization and a failed second launcher recording retaining episode0 for replay. Existing camera/replay and malformed-packet regression tests also passed.

No physical launcher test or robot actuation occurred during implementation. Readiness: ready for supervised rehearsal, not physically validated. Remaining risks include existing serial startup intermittency, video-save latency, current/future camera-index changes and holding/release behavior during cleanup. Next agent action: operator rehearses one brief recording, finish, repeat replay, discard/reset and explicit session reopen before the demo.

## Commands

```sh
cd /Users/dwei/lerobot
bash demo_so101.sh check
bash demo_so101.sh launch --label tomorrow_demo --episodes 27
bash demo_so101.sh list
bash demo_so101.sh launch --session EXACT_PRINTED_SESSION_NAME
```

27 is two demo episodes plus25 collection episodes; use25 for25 total. The recording limit counts successful saves, not attempts. Replay remains available after reaching it.
