# IDEA-20261027-002 — Verify SONIC with PICO 4 foot tracking

Status: time-sensitive; ready for hardware inventory and input-only bring-up.
Project: PICO 4 loan evaluation / Unitree G1. Physical robot validation: not
started and not authorized. Loan deadline: Friday, 2026-10-30; target completion of
tracking evidence by Thursday, 2026-10-29.

## Objective and scope

Verify NVIDIA's released GEAR-SONIC whole-body teleoperation path with the borrowed
PICO headset, regulatory model `A8110`, and two confirmed foot trackers. A8110 is
used for both standard PICO 4 and PICO 4 Pro, so the exact marketed variant,
controller inventory and tracker firmware are not yet confirmed. Direct device
inspection reports Android 10 and software version/build `202403120341`; this does
not by itself distinguish standard from Pro. The device reports PICO system version
`5.20`. No eye-tracking or face-tracking
setting was visible, making standard PICO 4 the leading inference, but the marketed
variant remains unconfirmed. The headset shows one paired motion-tracker set (two
trackers). First establish
calibrated full-body tracking and SONIC Sim2Sim behavior. A real-G1 attempt is a
later, separately authorized gate, not an automatic consequence of successful
streaming or simulation.

Model evidence: the [A8110 FCC test report](https://fcc.report/FCC-ID/2A5NV-A8110/6011039.pdf)
states that A8110 covers both PICO 4 and PICO 4 Pro; the Pro adds eye and face
tracking. The regulatory code alone therefore does not resolve the variant.

Use NVIDIA's full
[`GR00T-WholeBodyControl`](https://github.com/NVlabs/GR00T-WholeBodyControl)
teleoperation stack for this evaluation. LeRobot's `SonicWholeBodyController` ports
the decoder half and accepts 64-D motion tokens; by itself it does not supply the
PICO/SMPL encoder and foot-tracking pipeline required by this objective.

## Reference behavior

NVIDIA's current PICO setup documents a PICO 4/4 Pro, two controllers, two PICO
motion trackers worn at the ankles, XRoboToolkit, a low-latency private Wi-Fi path
and full-body streaming into `pico_manager_thread_server.py`. The official sequence
uses calibration, visualization and MuJoCo Sim2Sim before real hardware. Tracking
loss or latency can produce unsafe whole-body commands; the robot documentation
requires frequent recalibration, clear tracker visibility and independent emergency
control.

Primary references:

- [PICO VR setup](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/getting_started/vr_teleop_setup.md)
- [Whole-body teleoperation tutorial](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/tutorials/vr_wholebody_teleop.md)
- [Teleoperation safety guidance](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/user_guide/teleoperation.md)

## Time-boxed validation ladder

1. **Inventory before installation:** if readily available, record the marketed
   variant from the box or device settings; preserve the observation that no
   eye/face-tracking setting was visible. Record controller inventory, both tracker
   firmware versions, battery/charger state, available cables, installed apps and
   Wi-Fi topology. Confirm both members of the motion-tracker pair appear separately
   in the headset UI.
2. **Input-only tracking:** install/launch the documented XRoboToolkit PICO client
   and PC service. With no simulator or robot, verify head, both controllers and both
   feet are present, correctly labeled, finite and directionally plausible. Preserve
   avatar/video or structured pose traces, timestamps, reconnect behavior and
   deliberate tracker-occlusion behavior.
3. **Calibration and latency:** repeat the standing calibration, inspect SMPL and
   three-point visualizations, estimate stream latency/jitter/dropout on the intended
   private network and verify the controller stop gesture is observed. Do not infer
   control safety from an avatar alone.
4. **SONIC Sim2Sim:** run the released MuJoCo simulator plus C++ deployment with
   `--input-type zmq_manager`, then the PICO streamer. Begin with stationary and
   small, slow motions; validate mode transitions, foot correspondence, stop/restart
   and loss-of-tracking behavior. Preserve exact repository/checkpoint revisions and
   logs.
5. **Real G1:** defer until simulation is smooth and repeatable, emergency paths are
   rehearsed, the G1 configuration is reviewed, a gantry/clear zone and safety
   operator are available, and a separate physical protocol is explicitly approved.

## Success criteria for the loan window

- Minimum useful result: exact device inventory plus a preserved, calibrated
  full-body pose stream demonstrating whether both foot trackers are accessible.
- Preferred result: repeatable SONIC Sim2Sim motion and stop behavior using the
  borrowed hardware.
- A failed compatibility result is useful if logs distinguish headset pairing,
  XRoboToolkit transport, calibration, pose semantics and SONIC deployment stages.
- Real-robot motion is not required to complete the time-sensitive evaluation.

Next agent action: record the remaining device inventory, then prepare the input-only
XRoboToolkit bring-up and evidence capture; do not let unresolved standard-versus-Pro
labeling delay the time-sensitive tracking test.
Prerequisites: borrowed PICO/controllers/trackers charged and available, compatible
workstation, private low-latency Wi-Fi and permission to install the documented PICO
application.

## 2026-10-28 XRoboToolkit discovery

NVIDIA `NVlabs/GR00T-WholeBodyControl` main revision
`1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b` documents XRoboToolkit PICO client
`v1.1.1` and PC service `v1.0.0`. The official XRoboToolkit release includes a
dedicated `XRoboToolkit-PICO-1.1.1-SDK29.apk`; Android 10 corresponds to API 29, so
this is the conservative client candidate for the borrowed headset rather than the
generic APK. The corresponding workstation package is
`XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb`.

Both official GitHub release assets were downloaded for inspection but not installed:

- SDK29 APK: SHA-256
  `6089e1ce175cf3e292cea5919c2b97711151186ca39c4a5569786a12fc167eb2`.
- Ubuntu 24.04 PC service: SHA-256
  `bce661f0be0b8a246ceecb2e5f1675a81c26b834648dc7fdf23f8c0bfe2a5d19`;
  Debian package name `roboticsservice`, version `1.0.0.0`, architecture `amd64`.

The PICO was not connected through ADB during discovery. Installation therefore
requires either owner-approved sideloading through the headset browser/download
manager or a USB connection with headset-side ADB authorization. Before streaming,
verify both trackers in the PICO UI, calibrate them at the ankles, start the PC
service, and configure XRoboToolkit with workstation IP `10.9.0.149`, Head +
Controller tracking, Data/Control Send, and PICO Motion Tracker Full body.

Next agent action: after owner approval, install the SDK29 PICO APK and Ubuntu 24.04
PC service, then perform a no-robot connection/schema test. Record status `WORKING`,
24-joint pose shape, finite transforms, timestamp/FPS behavior, left/right ankle
response, controller buttons, disconnect/reconnect and tracker occlusion. Do not start
SONIC Sim2Sim until this input evidence is stable.

## 2026-10-28 input-only bring-up

The verified SDK29 APK was installed over authorized ADB on device serial
`PA8150MGGB090263G` and reports package `com.xrobotoolkit.client`, version `1.1.1`,
minimum SDK 29 and target SDK 32. Because installing the workstation Debian package
requires interactive sudo, its payload was extracted into the LeRobot workspace and
the official `RoboticsServiceProcess` was run directly with its packaged libraries.
This is a temporary evaluation setup, not a system installation. The official
XRoboToolkit Python binding `1.0.2` was built in an isolated Python 3.10 environment.

The operator observed XRoboToolkit status `WORKING` with workstation IP
`10.9.0.149`. A bounded, read-only 15-second probe then collected 747 samples and
636 distinct nonzero stream timestamps. Headset and both controller poses were
nonzero, establishing that PICO-to-service transport and the local Python SDK path
work. No simulator or robot was started.

The same probe reported `body_available=false`, zero body-timestamp updates and
`motion_tracker_count=0`. PICO logs concurrently repeated
`CentaurEngine AddTrackerImageData failed, can't found [NoTracker] tracker`. Treat
this as a PICO tracker-recognition/calibration boundary, not evidence that
XRoboToolkit transport or all PICO foot-tracking support has failed. Evidence JSON
is retained locally at
`/home/dwei/lerobot-dev/xrobotoolkit-evidence/probe-20261028-live.json`; it is not
copied into the labbook because it contains live device poses.

Next operator action: in the PICO Motion Tracker panel/app, unpair both trackers,
pair each again by holding its button for six seconds until red/blue flashing, and
complete both calibration sequences (controllers down at the sides, then look down
until both ankle trackers are recognized). Keep tracker lights facing up and visible.
Then reconfirm XRoboToolkit `Head`, `Controller`, `Send` and `Full body`, rerun the
bounded probe, and require two trackers plus a finite 24-by-7 body pose before any
SONIC Sim2Sim attempt.

### Tracker recovery and full-body result

The operator synchronized the two foot trackers in the PICO system UI. Returning
from the tracker UI initially left XRoboToolkit with a stale socket; relaunching the
app and restoring status `WORKING` recovered transport. A subsequent 15-second
read-only capture produced 693 distinct global stream timestamps and
`body_available=true`. The returned schemas were finite and matched the documented
shapes: body poses 24-by-7, velocities 24-by-6 and accelerations 24-by-6.

A second 15-second movement capture produced 682 distinct global timestamps. During
the operator's left-then-right foot movement sequence, reported position ranges were
nonzero for both feet and ankles: left ankle `[0.3737, 0.1766, 0.5948]` m, right
ankle `[0.2325, 0.3466, 0.5664]` m, left foot `[0.3711, 0.0924, 0.6705]` m and right
foot `[0.2910, 0.2608, 0.6628]` m. These aggregate ranges establish responsive lower
body output but do not by themselves prove left/right temporal independence; retain
that distinction for visualization or time-series review.

Two diagnostic limitations were observed: `num_motion_data_available()` remained
zero and `get_body_timestamp_ns()` remained zero even while the global stream
timestamp changed hundreds of times. The derived 24-joint full-body channel is
therefore usable for the next SONIC input/visualization gate, but consumers should
use or cross-check the advancing global timestamp rather than treating the body
timestamp as valid. Local evidence files are
`probe-20261028-fullbody.json` and `probe-20261028-foot-ranges.json` under the
workspace `xrobotoolkit-evidence` directory; they contain live pose data and remain
outside the labbook.

Next agent action: preserve the working PICO/XRoboToolkit configuration and advance
to SONIC visualization or Sim2Sim only. First verify the exact local source and
checkpoint revisions and required artifacts; do not infer real-robot authorization.

### SONIC Sim2Sim readiness check

The clean local NVIDIA checkout is at revision
`1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b`, but Sim2Sim is not yet runnable.
Neither `.venv_sim` nor `.venv_teleop` exists; the deployment policy directories
contain observation configuration only and no encoder/decoder ONNX files; no
TensorRT installation or `TensorRT_ROOT` was found; and the `just` build tool is not
installed. Docker is present but reports only `runc` runtimes, not an NVIDIA runtime.

Host-level GPU inspection succeeds: two RTX 5090 GPUs, NVIDIA driver `595.99.02`,
32,607 MiB each. At inspection time each GPU used about 30,317 MiB, consistent with
the running vLLM workload, so GPU memory must be released before SONIC deployment.
The next preparation step is therefore to stop the unrelated GPU workload, install
the documented MuJoCo/teleop environments, obtain the matching SONIC deployment
model set, install exact TensorRT 10.13 plus build dependencies, build the native
deployment, and pass a non-PICO Sim2Sim smoke test before adding the live streamer.
