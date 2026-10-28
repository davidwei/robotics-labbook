# IDEA-20261027-002 — Verify SONIC with PICO 4 foot tracking

Status: time-sensitive; ready for hardware inventory and input-only bring-up.
Project: PICO 4 loan evaluation / Unitree G1. Physical robot validation: not
started and not authorized. Loan deadline: Friday, 2026-10-30; target completion of
tracking evidence by Thursday, 2026-10-29.

## Objective and scope

Verify NVIDIA's released GEAR-SONIC whole-body teleoperation path with the borrowed
PICO headset, regulatory model `A8110`, and two confirmed foot trackers. A8110 is
used for both standard PICO 4 and PICO 4 Pro, so the exact marketed variant, OS,
controller inventory and tracker firmware are not yet confirmed. First establish
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

1. **Inventory before installation:** record the marketed variant and OS from device
   settings; determine whether eye/face tracking identifies a Pro variant; record
   controller inventory, the two tracker firmware versions, battery/charger state,
   available cables, installed apps and Wi-Fi topology. Confirm both trackers pair
   and appear in the headset UI.
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

Next agent action: identify the exact headset model/OS and remaining device
inventory, then prepare the input-only XRoboToolkit bring-up and evidence capture.
Prerequisites: borrowed PICO/controllers/trackers charged and available, compatible
workstation, private low-latency Wi-Fi and permission to install the documented PICO
application.
