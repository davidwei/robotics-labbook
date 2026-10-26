# Demo rehearsal and next visit

## Observed rehearsal — October 25

Operator reports two episodes tested and seeming good; saving and replay preparation were slow. Local launcher session `20261025_230140_21361d8b_demo_pretrial`, source MoissanClub/lerobot branch `lab/so101-intel-warning-20261023` revision `2bdbf48787b62e128e2950c21d6cdc9707def402`.

| Episode | Frames | Nominal duration at 30 FPS | Save interval | Result |
|---|---:|---:|---|---|
| 0 | 4157 | 138.6 s | 23:04:35–23:06:01 (~86 s, before cleanup) | committed, child exit 0 |
| 1 | 2623 | 87.4 s | 23:13:36–23:14:39 (~63 s, before cleanup) | committed, child exit 0 |

Both telemetry writers report zero drops/errors. Occasional instantaneous control-loop slow-rate warnings remain; zero writer drops does not prove perfect camera/control sampling. Current episode index 1, committed count 2, cumulative 6780 frames. Episode 0 replay exit 0; reference preparation started23:06:31 and reached4100frames23:09:04 (~153s), robot connected23:09:11, disconnected23:11:33. No episode1 replay result found at inspection. Manual discard and failure recovery remain software-tested, not established by this rehearsal.

Evidence remains local: `/Users/dwei/lerobot/outputs/demo/so101/20261025_230140_21361d8b_demo_pretrial/`. `attempts/ep000_7c75653779` and `attempts/ep001_e4989face1` contain configs, recording logs, telemetry, committed markers and cumulative dataset snapshots; `logs/` contains preview/replay evidence. Dataset upload disabled. Raw videos/telemetry have not been uploaded to the labbook or release storage; local retention is required. Calibration hashes are recorded in session.json and match this lab session's installed calibration provenance.

## Interpretation and decision

Non-streaming H264 encoding occurs after recording; replay decodes/resizes/JPEG-encodes reference images frame by frame before motor connection. These code paths explain substantial work in both delays; no profiling yet apportions exact cost. No performance optimization or streaming-encoding change was applied. A 10 FPS experiment is planned for October26. Estimates of 2–3x shorter save/preparation times are unmeasured projections, not validated results. Reduced rate also changes follower command rate to10Hz in the current recorder. Camera acquisition remains30FPS. Slower manipulation may remain suitable training data; responsiveness and replay timing need physical checking.

## Next visit — try 10 FPS, then demo

1. Connect the existing leader/follower and both cameras. Confirm index0 is high-mount and index1 gripper in Ready preview. Confirm ports and stable initial pose; do not recalibrate unless necessary.
2. Run the config-only check and start a separate trial session using the commands below. A new session preserves the existing30FPS dataset.
3. S starts; run a short representative task; Right Arrow (or F) finishes. Keep launcher Terminal focused. Wait for COMMITTED, then R and align follower near the first recorded pose before confirming replay. Check control smoothness, camera views, save/preparation delays and replay pacing.
4. If10Hz is satisfactory, launch a fresh demo session with27 slots (two demonstration episodes plus25 collection episodes). If unsatisfactory, use original30FPS config. Keep each session's FPS fixed.
5. Ready S starts next, R replays last saved, Q quits. Left Arrow discards current attempt and returns Ready for manual reset; no auto-home. Cap300s; finish primarily with Right Arrow. Support arm when processes disconnect/release torque.
6. If interrupted: `bash demo_so101.sh list`, then `bash demo_so101.sh launch --session EXACT_SESSION_NAME`. Resume the desired session rather than creating another one. Do not assume a still-running launcher adopts config edits.

```bash
cd /Users/dwei/lerobot
bash demo_so101.sh check --config outputs/lab/so101-20261025-12v/record-10fps.json
bash demo_so101.sh launch --config outputs/lab/so101-20261025-12v/record-10fps.json --label trial_10fps --episodes 2
# After the trial, quit and start the actual demonstration session:
bash demo_so101.sh launch --config outputs/lab/so101-20261025-12v/record-10fps.json --label demo_10fps --episodes 27
# 30 FPS fallback, creates a separate session:
bash demo_so101.sh launch --label demo_30fps --episodes 27
```

10FPS config parsing/calibration-file preflight passed without hardware connection. Five-minute cap is imposed by the launcher. Physical10FPS trial is pending. Operator announced departure; actual launcher shutdown, torque release, motor power-off and final resting pose were not independently observed.
