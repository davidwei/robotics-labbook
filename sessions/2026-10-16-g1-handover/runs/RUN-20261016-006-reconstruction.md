# RUN-006 reconstruction handoff

Status: data collection only. User explicitly deferred simulation work until after the lab. No simulation implementation or execution occurred.

## Direct Git checkout

- Remote branch: [archive/g1-vr-physical-failure](https://github.com/MoissanClub/lerobot/tree/archive/g1-vr-physical-failure).
- Exact archived commit: [75911f64cee1c9b365fffc25914a5ddd9145731e](https://github.com/MoissanClub/lerobot/commit/75911f64cee1c9b365fffc25914a5ddd9145731e).

The executed code is now archived in `MoissanClub/lerobot` on branch
`archive/g1-vr-physical-failure`, commit
`75911f64cee1c9b365fffc25914a5ddd9145731e`.
Its diff from base `ca04051f570e4df1fa1d49f84ce39fd623ecbc2f` was verified
byte-for-byte equal to RUN-006's `code.patch`.

```bash
git clone git@github.com:MoissanClub/lerobot.git lerobot-run006
cd lerobot-run006
git checkout --detach 75911f64cee1c9b365fffc25914a5ddd9145731e
```

Do not apply `code.patch` again to this archive commit. The patch is only needed
when starting from the base commit. The raw-data archive still supplies the exact
temporary `harness.py`, launch script, scenario/configuration, and traces; those
experiment files are not added to the LeRobot branch. This archives a known failed
physical experiment, not a validated fix or authorization to run it on hardware.

## Preserved inputs

- Artifact directory: `/home/dwei/robotics/artifacts/2026-10-16-g1-handover/random-return-01`.
- `commands.json`: publication time, phase, measured arm q/dq snapshot, q targets, feedforward tau, authority weight, DDS tick/sample age, write completion. Arm ordering: left seven then right seven; shoulder pitch/roll/yaw, elbow, wrist roll/pitch/yaw. Radians and rad/s.
- `feedback.jsonl`: independent arm q/dq, mode, tick, receive-age and monotonic time. `config.json`, `scenario.json`, baseline/activated plan, exact executed `harness.py`, `code.patch`, process log and closure marker.
- `reconstruction/base-source.tar`: code at ca04051f. Extract it and apply the run's `code.patch` (not a later working-tree diff) to recover the candidate. The temporary harness is separately preserved.
- `reconstruction/`: executed gravity URDF, candidate MuJoCo XML, mesh hashes, installed distribution versions, angle-excursion summary and timeline plot. Model snapshot: `lerobot/unitree-g1-mujoco` at `68459ed68f6f68e1f661091dfcb6ebce44681aec`; meshes remain in that snapshot and are hash-indexed.
- Successful comparison: RUN-005, `inspection-forward-01`; stalled comparison: RUN-004, `inspection65-unitree-01`.

## Missing / uncertain

Waist joint q/dq, IMU orientation/angular velocity/acceleration, measured torque, full leg/body feedback, stock-controller internal targets/torques and firmware blending behavior were not recorded. There is no external video or exact emergency-stop timestamp. Host receive/sample times are not sensor acquisition times. The q/dq snapshot in a publication row can be newer than the snapshot used to calculate that target. Write success is not execution acknowledgment. Model inertias, friction, saturation and motor/transport delays are not hardware-calibrated by this record.

## Later reconstruction, not implemented

First replay the command-law transition and its PD contribution using recorded signals. Then build a fixed-base arm closed-loop model to test measured-relative targets with frozen feedforward versus sustained pose hold. Treat latency, actuator limits and body posture as explicit sensitivity variables. Reproducing forward body motion additionally requires stock balance/controller behavior or measured waist/IMU input; a fixed-base model alone cannot establish that mechanism. Do not tune a simulator until it oscillates and call that proof of root cause. Keep failed RUN-006 and successful RUN-005 as separate comparison cases.

Future recorder requirement: all 29 body joint q/dq/estimated torque, full available IMU fields, robot mode, host timestamps/ticks, targets/feedforward/gains/authority, phase/event timestamps and operator intervention markers. Add logging offline; this does not authorize another physical test.

The operator requested preservation in the labbook repository itself. The complete [raw-data archive](../artifacts/RUN-20261016-006-reconstruction.tar.gz), [SHA-256 checksum](../artifacts/RUN-20261016-006-reconstruction.sha256) and [timeline plot](../artifacts/RUN-20261016-006-timeline.png) are tracked in Git alongside this index. Extract the archive to recover the raw traces and reconstruction inputs. The archive retains its original capture-time README; this repository index supersedes its local-only storage note.
