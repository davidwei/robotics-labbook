# SESSION-20261009-001 — forensic capture timeline

Retrospective in-lab capture; review pending. Owner/operator: David Wei. Agent: Codex, session `01a11c8a-0182-73d2-9891-d0b6d876e822`. Date: 2026-10-09, Asia/Shanghai (UTC+08:00). Physical robot: Unitree G1-29, onboard Jetson host `unitree-g1-nx`. Linked experiment: [EXP-20261009-001](../../experiments/EXP-20261009-001/experiment.yaml).

## Scope and provenance

This record reconstructs only the activity visible in this Codex session, beginning approximately 01:23. It does not assert that this was the whole day's lab activity. The native session metadata starts 01:22:48.911; user request arrived 01:23:14.456. Times below are local wall-clock times converted from native archive UTC timestamps unless specified. Tool-call timestamps describe invocation/receipt, not necessarily the exact execution instant. File timestamps and application log timestamps give additional bounds. Operator axis sequence is retrospective and has no exact per-axis time.

Goal: run the test plan for [huggingface/lerobot commit dd3d74b82832673666d6a2adb71bec18ea509219](https://github.com/huggingface/lerobot/commit/dd3d74b82832673666d6a2adb71bec18ea509219), which adds explicit G1-23 embodiment support while retaining the 29-slot body transport layout. User clarified that this robot is G1-29 and requested regression validation on it first, with G1-23 hardware testing to follow later.

- Existing checkout: `/home/dwei/lerobot`, branch `work/g1-vr-physical`, HEAD `c7bb831461495f2a2fa4db10c8b2607b6934921e` (MoissanClub/lerobot origin; huggingface/lerobot upstream). The requested cwd `/home/dwei/lerobot/lerobot-g23-branch` was an empty nested directory, not an independent checkout; Git resolved to its parent.
- Actual tested checkout: `/tmp/lerobot-g1-regression`, detached HEAD **dd3d74b82832673666d6a2adb71bec18ea509219**. Shared local clone followed by fetch from upstream and detached checkout. No tracked code edits were made. Untracked capture helpers were created before physical runs; their exact bytes are preserved in external artifact storage, not copied into this notebook. Post-run `G1_29_TEST_RESULTS.md` was created later and did not drive the robot.
- Existing checkout had untracked `MUJOCO_LOG.TXT`; recovered mtime is 2026-10-02 02:50:08, so it is not attributed to today's tests. Reflog's recent G1 VR commit is dated October 8, not a code change made today. No VR/headset/arm-exoskeleton test occurred in this session.
- Runtime: existing `/home/dwei/miniforge3/envs/lerobot-dev` via `uv run --no-project --python ...`; source selected explicitly with `PYTHONPATH=/tmp/lerobot-g1-regression/src`. This intentionally reused installed dependencies rather than running the commit's `uv run --extra test` dependency resolution. Pytest 9.1.1. No environment lock/export was captured during the run, so full dependency reproducibility is incomplete.
- Network: onboard Ethernet `enP8p1s0`, `192.168.123.164/24`; client used loopback ZMQ bridge `127.0.0.1`, ports 6000/6001. Native DDS observers explicitly used `enP8p1s0`; stock bridge used its default DDS interface selection.

## Reconstructed timeline

| Local time | Activity and evidence | Outcome / uncertainty |
| --- | --- | --- |
| 01:23:14 | User requested commit/test plan inspection. | Initial target embodiment unspecified. |
| ~01:23–01:24 | Local `git show` failed: `bad object dd3d74...`; GitHub web fetch returned cache miss. GitHub API via `curl -fL` succeeded, saved `/tmp/lerobot-requested-commit.json`. `jq` absent. Initial sandbox showed only restricted files; `lsusb` failed libusb initialization and `ip` failed netlink permissions. Zsh unmatched README glob aborted part of an inspection. | Tool/setup failures, not robot test failures. Host inspection was rerun outside sandbox with permission. |
| 01:23:46; 01:24:30 | User clarified onboard G1-29 regression first, G1-23 later. | Scope corrected before any motion. |
| ~01:24 | Host inspection: Ethernet and Wi-Fi up; RealSense 435i, FT4232H USB device visible. No serial-by-id directory visible in initial sandbox. | USB inventory only; no camera/serial physical test. |
| 01:24:47–01:25:04 | Shared clone to `/tmp/lerobot-g1-regression`, fetch exact upstream commit, detached checkout. | Existing working branch preserved; no switch/cherry-pick on it. |
| 01:25:11–01:25:30 | Focused pytest invocation; output `75 passed in 3.05s`, `Testing with DEVICE='cuda'`. Commit diff whitespace check clean. | Software tests; mocked hardware paths, not physical proof. |
| 01:25:44 | Ruff invocation failed: `No module named ruff`. | Retried via isolated `uv tool run ruff`, downloading Ruff (~9.5 MiB). |
| 01:26:04–01:26:14 | Created read-only preflight helper; installed package imports succeeded; five-second DDS subscription received 2,170 samples; 35 SDK message slots, 29 body joints checked finite; mode_machine=5. Ruff passed all six changed Python files. | RUN-20261009-001. Four contiguous remote floats read zero, but helper's fourth-field `ly` label was later found wrong; do not treat this as independent proof that ly was centered. |
| 01:26:27; ~01:26:30–01:27 | Model/driver preflight first failed (`uv ... -c`: missing executable, unexpected argument). Corrected to `uv ... python -c`. Holosoma ONNX loaded; driver default g1_29 and 29 action/observation joint features asserted. | No connection/publication; preflight successful after command correction. ONNX Runtime emitted unknown CPU vendor warning; pygame emitted pkg_resources deprecation warning. |
| 01:27:06 | User said “confirmed” to suspension/tether, spotter, reachable emergency stop, paired remote/sticks-centered prerequisites. | Operator confirmation; agent did not independently inspect the physical setup. |
| 01:27:19–01:27:36 | Started exact-commit `run_g1_server.py`; bridge reported running. Stock bridge initialization calls MotionSwitcherClient and releases active mode. | Physical control handover stage. No motion-mode return/restore verification was recorded. |
| 01:27:59–01:28:04 | Created and started read-only DDS command/state monitor; telemetry file birth 01:28:04.337. | RUN-20261009-002 evidence capture. Observer contains a remote-decoding bug; see correction below. |
| 01:28:14–01:28:18 | CLI logs: G1-29 hardware driver + Holosoma FASTSAC policy, [1,100] input → [1,29] output, 29 gains. Remote-only teleop (empty exo ports), no cameras/display. Connected 01:28:15, interpolated to default pose, “Reached default position” and 200 Hz controller thread at 01:28:18. | Startup/reset was physically executed using exact upstream commit; 200 Hz is configured target, not measured achieved cadence. |
| ~01:28:18–01:30:18 | 120-second teleoperation. All 29 body command slots active, including slots 13,14,20,21,27,28 that G1-23 omits. Snapshot near elapsed 40–55 s showed roll/pitch near zero, but transient joint speed max 7.676 rad/s in a partial summary; no causal explanation or safety conclusion established. | Single supervised run; not a controlled reliability demonstration. |
| 01:29:04 | Operator: “yes, the robot works”. | User physical observation. No separate quantitative zero-input criterion or video recorded. |
| 01:29:24 | Operator: “i moved the remote axes and they work”. | User physical observation; per-axis exact timing not captured. |
| 01:30:18 | CLI finished 7,025 ticks; measured teleop cadence 58.54 Hz vs 60 Hz target; no loop-body work exceeded 16.7 ms budget, all judged pacing intervals slipped outside loop body. Exit code 0. Driver logged zero-torque command twice. | Successful timed client completion. All 29 final DDS kp/kd/tau values later verified zero. Duplicate log noted; cause not analyzed. |
| ~01:31–01:32 | Agent read telemetry, reported lx/rx nonzero and “ly stayed zero; forward/back unverified”. | Historical interpretation is superseded by decoder correction and operator clarification below. |
| 01:35:24–01:37:01 | Sent SIGINT to bridge pid 6458 and monitor pid 6591. Bridge raised `zmq.error.ContextTerminated` in state-forward thread; both did not finish promptly. SIGTERM invoked 01:35:54, cleanup receipt/inspection by ~01:37 showed no 6000/6001 listeners; bridge briefly defunct. | Client was already passive. This is cleanup evidence; native control not restored. Stock bridge cleanup code was not changed by this embodiment commit; no root-cause attribution established. |
| 01:37:01 | Created preliminary `/tmp/lerobot-g1-regression/G1_29_TEST_RESULTS.md`. | Historical summary retained; contains now-superseded forward/back coverage statement. |
| 02:14:54 onward | User requested retrospective lab capture; canonical lab book cloned and skill read. | Documentation only; no new robot actuation. |
| 02:16:11 | Operator clarified: “i moved the robot forward and backward first; after that, sideway and turn”. | Record actual reported sequence: forward/back → sideways → turn. Exact segment times unavailable. |
| ~02:17 | Brief SDK source inspection established wrong ly offset in temporary observer, while production teleop used SDK Joystick.extract. | Corrected evidence labeling; no long root-cause analysis performed. |

## Activities and experimental run

- [PREFLIGHT-20261009-001](activities/PREFLIGHT-20261009-001.yaml): five-second read-only physical DDS preflight; originally recorded as RUN-20261009-001. Reclassified during the updated-skill revision; measurements unchanged.
- [RUN-20261009-002](runs/RUN-20261009-002.yaml): supervised two-minute G1-29 Holosoma locomotion and disconnect, plus cleanup.

### Relevant executed commands

Working directory for tests and motion: `/tmp/lerobot-g1-regression`. Installed uv/Python absolute paths below refer to the existing robot environment.

```sh
PYTHONPATH=/tmp/lerobot-g1-regression/src /home/dwei/miniforge3/envs/lerobot-dev/bin/uv run --no-project --python /home/dwei/miniforge3/envs/lerobot-dev/bin/python -m pytest tests/robots/test_unitree_g1.py tests/robots/test_unitree_g1_embodiments.py -q
git diff HEAD^ HEAD --check
UV_CACHE_DIR=/tmp/g1-regression-uv-cache /home/dwei/miniforge3/envs/lerobot-dev/bin/uv tool run ruff check src/lerobot/robots/unitree_g1/config_unitree_g1.py src/lerobot/robots/unitree_g1/g1_embodiments.py src/lerobot/robots/unitree_g1/g1_utils.py src/lerobot/robots/unitree_g1/unitree_g1.py tests/robots/test_unitree_g1.py tests/robots/test_unitree_g1_embodiments.py
PYTHONPATH=/tmp/lerobot-g1-regression/src PYTHONUNBUFFERED=1 /home/dwei/miniforge3/envs/lerobot-dev/bin/uv run --no-project --python /home/dwei/miniforge3/envs/lerobot-dev/bin/python python src/lerobot/robots/unitree_g1/run_g1_server.py
PYTHONPATH=/tmp/lerobot-g1-regression/src PYTHONUNBUFFERED=1 /home/dwei/miniforge3/envs/lerobot-dev/bin/uv run --no-project --python /home/dwei/miniforge3/envs/lerobot-dev/bin/python python -m lerobot.scripts.lerobot_teleoperate --robot.type=unitree_g1 --robot.embodiment=g1_29 --robot.is_simulation=false --robot.robot_ip=127.0.0.1 --robot.controller=HolosomaLocomotionController --teleop.type=unitree_g1 --teleop.id=g1_29_regression --display_data=false --teleop_time_s=120
kill -INT 6458 6591
kill -TERM 6458 6591
```

### Evidence correction: remote axes

The untracked monitor and preflight used `struct.unpack_from('<ffff', remote, 4)`, labeling the four floats `lx,rx,ry,ly`. Installed SDK source `/home/dwei/unitree_sdk2_python/unitree_sdk2py/utils/joystick.py`, `Joystick.extract`, instead reads lx at byte 4, rx at 8, ry at 12, **ly at 20**. Byte 16 is not ly. Thus recorded `axes_lx_rx_ry_ly[3]` is mislabeled, and ly was not retained in the helper's telemetry. It cannot be recovered from that JSONL alone, since raw remote bytes were not logged. Production teleop uses SDK Joystick.extract and did not use this helper to drive commands. The decoded maxima [1.0, 0.9139072895, 0.0, 0.0] demonstrate lx/rx input; the zero fourth field says nothing about forward/back coverage. User explicitly confirms forward/back first, then sideways and turning. Preserve the original telemetry and preliminary summary without rewriting their history.

At the user's request, earlier telemetry was rechecked during capture: 24,270 state rows and 24,270 command rows. Absolute lx >0.1 appeared at monitor elapsed 38.8476–40.8023 s; rx >0.1 at 81.2855–83.7606 s. In elapsed 15–25 s and 25–35 s, maximum per-leg-joint position ranges were 0.0012 and 0.0003 rad respectively. This does not establish forward/back movement timing or direction. Operator-reported forward/back-first remains an observation, but alignment with this recording remains unresolved. Monitor elapsed times are not the CLI loop's elapsed times; no exact clock synchronization was recorded.

Installed SDK checkout at retrospective inspection: `814556d15970dd2ecf1c9984e845ca02ab07e206`, untracked `build/` only. This revision was not captured at run start; it is retrospective environment evidence, not a guaranteed historical snapshot.

## End-of-session summary

1. **Worked on:** compatibility validation of upstream G1-23 embodiment changes on physical G1-29 before testing G1-23.
2. **Physically tested:** read-only feedback; bridge/control handover; controller initialization/default-pose interpolation; 120 seconds remote-only Holosoma locomotion; operator reports forward/back, sideways, turning; final passive command.
3. **Worked:** 75 focused software tests, Ruff, whitespace check, model/driver preflight; operator said robot and axes worked; all 29 command slots active and final 29 zero-gain/zero-torque commands observed.
4. **Failed/unexpected:** missing local commit/tooling and sandbox restrictions; malformed uv preload command; temporary monitor's ly decoder incorrect; bridge shutdown ContextTerminated and blocked cleanup required SIGTERM. Teleop achieved 58.54 Hz rather than target 60 Hz. SDK/ONNX/pygame warnings. No reported unexpected physical motion.
5. **Code/config changes:** no tracked robot source modifications. Isolated exact-commit checkout, two untracked capture helpers, later preliminary summary; temporary isolated Ruff tooling. Runtime embodiment explicitly g1_29, hardware transport, localhost bridge, Holosoma, remote-only, no camera/display, 120-second duration. Upstream commit's code was tested; locally created monitoring code was not robot control code.
6. **Uncertain:** exact per-axis timings/amplitudes and zero-input duration; quantitative physical stability; actual controller frequency; full dependency state; native mode handover details/restoration; raw ly telemetry lost; broader robot reliability. No G1-23, SONIC, GR00T, gravity-compensation, camera, headset or simulation run here.
7. **Careful later review:** remote-decoder capture bug and superseded summary; final passive behavior/operator expectations; stock bridge shutdown; pace/slip metrics; partial peak joint velocity measurement; model metadata gains; extent to which this one demonstration supports non-regression. No reviewed finding is promoted from this run.
8. **Post-lab questions:** Can corrected raw remote capture align axes with commands/feedback? Should cleanup/mode restoration be improved and tested separately? Does a repeat G1-29 run with measured controller timing and video reproduce this result? Which G1-23 sparse-slot/physical controller checks should follow? What success criteria would support a stronger compatibility claim?

## Evidence and coverage audit

See [evidence.json](evidence.json) for local artifact locations/hashes. Telemetry and helper snapshots were preserved outside Git at `/home/dwei/robotics/artifacts/2026-10-09/g1-29-regression/`; this is durable local storage, not a remote backup. Native transcript remains in Codex's archive; no transcript copied into Git. Tool output is available there, sometimes truncated; no separate full stdout log/video/ROS bag was created.

Before committing, the record was rechecked against current conversation, timestamped user messages, command results, Git state/reflog and artifact timestamps. It includes failed setup attempts, physical startup/reset, observation sequence correction, telemetry labeling error, passive disconnect, and forced bridge cleanup. Earlier daily activity outside this session remains unknown. G1-23 testing is a future plan, not a completed activity.

## Capture-format revision

After the original capture commit `1a861f1a8fd1e99fd44e40ef4d93d56fb1e782b8`, the lab book was fast-forwarded to updated skill commit `b684ac0`. This revision applies `skills/labbook/workflows/retrospective-capture.md`: the detailed original narrative is retained here; `session.md` becomes the concise human reading path; structured capture coverage is added. No additional robot run or post-lab root-cause analysis was performed.

Activity classification: repository/tool setup, focused software checks, dependency/model readiness and read-only DDS checks are **preflight**; the two-minute physical locomotion execution is **run** RUN-20261009-002; the later targeted telemetry/decoder checks are **diagnostic**; disconnect, process termination and artifact preservation are **cleanup**. Historical RUN-20261009-001 labels in the chronology refer to the read-only preflight, now PREFLIGHT-20261009-001. Its structured record is retained under `activities/` for traceability rather than counted as a second experiment execution. RUN-20261009-002 includes cleanup observations because they materially affect its outcome; cleanup was not a separate experimental run.

Original evidence and hashes in `evidence.json` are unchanged. The original long capture is recoverable from Git commit `1a861f1`; the preliminary external results file remains unchanged with its explicit supersession. Native transcript remains at its original archive location. No `analysis.md` has been created; findings remain pending review.
