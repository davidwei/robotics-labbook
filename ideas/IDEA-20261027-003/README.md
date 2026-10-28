# IDEA-20261027-003 — Evaluate PICO 4 with NVIDIA Isaac Teleop

Status: time-sensitive; blocked on PICO browser/firmware update for valid video/WebXR
testing. Project: PICO 4 loan evaluation / NVIDIA Isaac Teleop. Physical robot
validation: not started and not authorized. Related:
[SONIC foot-tracking evaluation](../IDEA-20261027-002/README.md).
Loan deadline: Friday, 2026-10-30; preserve compatibility evidence by Thursday.

## Objective and uncertainty

Determine whether the borrowed PICO 4 can connect to the installed NVIDIA Isaac
Teleop/CloudXR path and expose usable headset/controller tracking. Then determine
whether that input can drive NVIDIA's SONIC PICO streamer in simulation through
`--input-source isaac-teleop`.

Do not initially assume Isaac Teleop exposes the PICO ankle trackers. NVIDIA's
current Isaac Capture device table explicitly lists PICO 4 Ultra controller and hand
tracking, while the GR00T whole-body stack separately documents PICO foot tracking
through XRoboToolkit and also provides an Isaac Teleop input backend. The borrowed
device has regulatory model `A8110`, used for standard PICO 4 and PICO 4 Pro, and
has two foot trackers. It is not identified as the currently documented PICO 4
Ultra. Direct inspection reports Android 10 and software version/build
`202403120341`, with PICO system version `5.20`. No eye-tracking or face-tracking
setting was visible, so standard
PICO 4 is the leading but unconfirmed variant inference. The device shows one paired
motion-tracker set (two trackers). Controller inventory, WebXR/CloudXR client
behavior and motion-tracker availability through DeviceIO must therefore be measured.

Primary references:

- [NVIDIA Isaac Capture supported devices](https://docs.nvidia.com/isaaclab/features/isaac-capture)
- [GR00T Whole-Body Control Isaac Teleop setup](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/tutorials/isaac_teleop_publisher_setup.md)
- Local bring-up notes: `unitree_g1_lerobot/docs/Rung0_isaac-teleop-install-notes.md`

## Validation ladder

1. Record exact headset model and OS, browser/client version, controllers, tracker
   inventory, workstation Isaac Teleop/CloudXR versions and network topology.
2. Start CloudXR/Isaac Teleop without a robot. Confirm HTTPS/client connection,
   rendered stream and finite head/controller poses. Record reconnect, controller
   buttons, tracking loss and shutdown behavior.
3. Inspect the actual DeviceIO/output schema. Explicitly record whether ankle/foot
   trackers appear, how they are labeled and whether their transforms update. Absence
   is a compatibility result, not a reason to synthesize foot poses.
4. If basic input works, run the GR00T PICO streamer with
   `--input-source isaac-teleop` and visualization only. Compare pose coverage,
   coordinate frames and latency with the XRoboToolkit path.
5. If the full SONIC reference is available through this backend, exercise Sim2Sim
   only. Keep the standalone Isaac Teleop compatibility result separate from SONIC
   controller validation.

## Success criteria for the loan window

- Establish and preserve a reproducible yes/no result for PICO 4 CloudXR connection
  and head/controller input.
- Enumerate the actual tracking schema, including a definitive observation about
  foot-tracker exposure through Isaac Teleop.
- Preserve exact versions, client URL/profile, logs and a minimal reconnect test.
- Prefer input-only and simulation evidence; real robot motion is unnecessary.

Current next action: preserve Chrome 105 as the compatibility boundary and prioritize
the XRoboToolkit/SONIC path rather than bypassing NVIDIA's browser gate. Reopen this
Isaac Teleop path only if an owner-approved, official PICO update raises the browser to
Chrome 125 or later; then repeat the H.264 G1-29 MuJoCo test.

## 2026-10-27 development evidence — G1-29 MuJoCo launch

The selected path was the supervised `unitree_g1_lerobot` G1-29 simulator rather
than the SO-101 example: repository `MoissanClub/unitree_g1_lerobot` at
`f6ad0248b99fed639a371ad26d59ec41e4f12b6f`, using its isolated LeRobot checkout at
`d5e400bcefeccc93ba956ce876530e5283512df1`. The integration working tree was dirty
in `tools/g1_vr_operator.py`, `tools/g1_vr_service.py`, the focused operator test,
and coworker documentation; those pre-existing changes add CloudXR startup-timeout
monitoring/retries and were the code actually executed.

Software observations:

- The focused operator suite passed: `20 passed`.
- A bounded synthetic G1-29 MuJoCo replay passed 100 frames with `0.2630 rad` motion
  and 54 distinct camera frames. Evidence remains at
  `/home/dwei/lerobot-dev/unitree_g1_lerobot/outputs/vr-sim-20261027-214156-flegcb8v`.
- Live startup brought the simulator and CloudXR to ready, and the 25-second CloudXR
  signaling check passed. The OpenXR bridge then failed before headset connection:
  Vulkan device creation returned `VK_ERROR_OUT_OF_DEVICE_MEMORY` /
  `xrCreateVulkanDeviceKHR ... VkResult=-2`. Evidence remains at
  `/home/dwei/lerobot-dev/unitree_g1_lerobot/outputs/vr-sim-20261027-214207-7ywe47lg`.
- At failure, each RTX 5090 had about 30.3 GiB of 32.6 GiB allocated by the two
  tensor-parallel workers of a Qwen3-VL vLLM server on port 8000. This is direct
  resource evidence and the leading explanation for Vulkan allocation failure;
  headset compatibility and controller input were not tested by this attempt.
- The supervisor stopped bridge, simulator and CloudXR after failure. No physical
  robot was connected or moved.

Next agent action: with operator approval, temporarily stop the vLLM server, verify
GPU memory was released, rerun `g1_29` headless live XR, connect the PICO CloudXR web
client, and record headset/controller connection, bilateral clutch motion, tracking
continuity and shutdown. Test tracker exposure separately; this G1 bridge consumes XR
controllers and does not establish ankle-tracker support.

## 2026-10-28 development evidence — PICO connection and browser boundary

The Qwen3-VL vLLM user service was stopped temporarily, releasing both RTX 5090s,
and restored after the test. The G1-29 supervised MuJoCo/CloudXR path then created
Vulkan/OpenXR successfully. NVIDIA IsaacCapture PR 1170's manual connection-helper
behavior was adapted to the installed `isaacteleop` 1.3.132rc1 environments (whose
WSS source is byte-identical to NVIDIA tag `v1.3.131`). The certificate page and
`/connect/` helper passed direct route tests and live HTTPS checks. This was an
environment patch, not a source-repository commit, and will be lost if either virtual
environment is reinstalled.

Direct observations and boundaries:

- The helper eliminated manual server entry and successfully reached an active PICO
  CloudXR stream. The server recorded its first video frame.
- The current NVIDIA client negotiated AV1 initially; the headset showed a dark
  screen. The helper was extended to prefill H.264, and the next native CloudXR log
  confirmed `H264 video format selected` and first-frame delivery.
- The headset reports PICO system version `5.20`; its PICO browser reported Chromium
  105, and NVIDIA's client reported that Chrome 125 or later is required. NVIDIA's
  current client source encodes
  `MIN_PICO_CHROME_MAJOR = 125` and directs the operator to update headset firmware.
- The headset's System Update view reports version `5.20` with no newer update, and
  Library/Updates offers no updates for PICO Browser or any other application. No
  supported on-device update path was available during this evaluation.
- With H.264, the control screen flashed and disappeared into a black screen. The
  final G1 simulator run nevertheless recorded `0.0993 rad` of arm motion over 6412
  frames, which is evidence that some controller input reached the bridge. It is not
  a passing visual, controller-semantics, continuity or safety result.
- The final run evidence is
  `/home/dwei/lerobot-dev/unitree_g1_lerobot/outputs/vr-sim-20261028-120402-a7hf139m`.
  No physical robot was connected or moved.

Next agent action: stop spending the remaining loan window on CloudXR browser bypasses
and proceed with XRoboToolkit/SONIC input-only bring-up. If an official PICO update
later provides Chrome 125 or newer, repeat the H.264 test and validate one
controller/arm at a time, release-to-freeze, bilateral control, tracking loss and clean
shutdown. Motion-tracker exposure through Isaac Teleop remains unanswered.
