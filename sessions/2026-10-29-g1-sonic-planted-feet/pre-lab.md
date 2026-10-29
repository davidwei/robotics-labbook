# SESSION-20261029-001 pre-lab — PICO/SONIC G1-29

Date: 2026-10-29. Owner/operator: David Wei. Status: planned and gated.

## Objective

Use tomorrow's lab access to close the highest-value readiness gaps for
[EXP-20261029-001](../../experiments/EXP-20261029-001/experiment.yaml). If and only
if all preceding gates pass and the operator separately authorizes motion, perform
the first gantry-supported subset of the planted-feet full-body demo.

This document authorizes planning, simulation and read-only robot inspection. It
does not authorize command publication or robot motion. Starting the real SONIC
deployment is itself motion because it releases the active stock motion service and
immediately interpolates all 29 joints toward a fixed default pose.

## Readiness-ranked activities

| Rank | Activity | Objective | Readiness | Prerequisites | Recommended next action |
|---:|---|---|---|---|---|
| 1 | Hardware/firmware inventory and read-only DDS preflight | Identify the exact G1 revision and establish fresh, finite 29-joint/IMU feedback without commands. | **Ready** | G1 powered in a non-commanding state; wired network; no `rt/lowcmd` publisher. | Do first; this is the minimum useful experiment. |
| 2 | Instrumented low-latency simulation | Rehearse the bounded demo and disconnect/stop cases using the exact intended physical candidate. | **Conditional** | Install and hash matching low-latency encoder, decoder, observation config and planner; review/pin source patches. | Complete before considering physical SONIC launch. |
| 3 | Fully suspended initialization and stop outcomes | Observe the automatic three-second initialization, keyboard/PICO stop, process death and post-stop behavior. | **Blocked** | Ranks 1--2 pass; rated gantry; safety operator; stale-stream response and exact source candidate reviewed; explicit motion authorization. | Do not launch real deployment while blocked. |
| 4 | Planted-feet physical demo segments 0--5 | Demonstrate arms, torso and a 3 cm symmetric pelvis lowering with both feet planted. | **Blocked** | Rank 3 passes and is reviewed; separate authorization for weight-bearing motion. | Earliest physical demo scope; optional segments 6--8 remain deferred. |

The selected thread is PICO/SONIC G1-29. If Rank 2 cannot be completed, use the lab
window for Rank 1 only rather than substituting an unplanned controller or model.

## Exact candidate and current status

| Item | Intended candidate | Current status before lab |
|---|---|---|
| Source | NVlabs revision `1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b` plus reviewed compatibility patches | Three patches remain local and uncommitted; not a physical candidate yet. |
| Model | SONIC low-latency encoder/decoder with its matching observation config | Not installed/validated locally. |
| Planner | `planner/target_vel/V2/planner_sonic.onnx` | Present; hash must be recorded with candidate. |
| TensorRT | x86_64 TensorRT 10.13 | Local 10.13.3.9 worked in simulation. |
| Teleop | XRoboToolkit PICO 1.1.1 SDK29 + PC Service 1.0.0 | Worked in simulation; stale-device behavior observed. |
| PICO | A8110, Android 10, system 5.20, build `202403120341`, two ankle trackers | Marketed variant and tracker firmware remain unknown. |
| G1 | Physical G1-29 | Firmware, manufacture date, pelvis and motor-driver revisions unknown. |

Do not mix model/config variants. Do not copy generated TensorRT engines across a
different GPU/TensorRT environment. Preserve SHA-256 hashes after generation.

## Rank 1 — minimum useful experiment, no motion

1. Photograph or transcribe the non-sensitive G1 model/revision labels. Keep serial
   numbers in the private artifact package rather than committed prose.
2. Record manufacture date, G1 system/control firmware, onboard image/OS, Unitree
   service versions, pelvis revision, motor/driver revision if exposed, ankle mode,
   `mode_machine`, hand type, battery state and hardware E-stop state.
3. Record both PICO motion-tracker firmware versions and battery state.
4. Confirm the workstation's exact wired interface and deliberate
   `192.168.123.x/24` address; do not accept `deploy.sh real` fallback selection.
5. Confirm no simulator, LeRobot, Holosoma, SDK example or stale process publishes
   `rt/lowcmd`.
6. Run a bounded read-only DDS subscriber. Require fresh CRC-valid LowState, 29
   finite q/dq states, base and torso IMUs, normal motor status/temperature, and
   stable update rate. Query the active motion mode but do not release it.
7. Preserve a machine-readable summary, command transcript and environment
   inventory. No command publisher is started in Rank 1.

Success: exact robot revision/firmware is known and the read-only feedback contract
passes. Failure: missing/ambiguous revision, non-finite/stale feedback, motor error,
unexpected publisher or unclear ankle/motion mode. A Rank 1 failure ends physical
work and proceeds to offline analysis.

## Rank 2 — instrumented simulation

1. Install/pin the low-latency model package and record all hashes.
2. Review and pin the controller-chord latch and build compatibility changes.
3. Enable PICO NPZ recording, target-motion logging, state CSV, motion recording,
   bounded console capture and synchronized viewer/operator video.
4. Run the complete
   [planted-feet protocol](../../ideas/IDEA-20261027-002/planted-feet-full-body-demo.md)
   three times from a fresh calibration.
5. Separately exercise PICO disconnect, tracker occlusion, Wi-Fi interruption,
   streamer death, keyboard stop, PICO stop and restart.
6. Require no unexplained fall, backward recovery walking, target discontinuity,
   duplicate mode event or unexplained stream gap at or above 100 ms. Require
   stream-delay p95 below 30 ms and agreement between pose, target, measured state
   and video.

The current stale-stream behavior is a failed result: `device missing`, exhausted
streamed motion and continued backward walking are not a usable degraded mode.

## Rank 3 — suspended physical initialization, only if authorized

Follow the full
[setup checklist](../../ideas/IDEA-20261027-002/g1-29-sonic-setup.md). Required
conditions include a rated gantry with limb clearance, three-meter exclusion zone,
separate PICO and safety operators, keyboard `O`, facility E-stop, fitted clothing,
private low-latency PICO network and an exact wired G1 interface.

1. Start XRoboToolkit and the PICO manager in OFF; verify fresh frames.
2. Confirm every competing DDS command publisher and MuJoCo are stopped.
3. After an explicit motion authorization, launch the pinned real deployment and
   observe only the automatic initialization trajectory.
4. Abort on wrong direction, mapping mismatch, oscillation, collision, unexpected
   speed, motor error, stale feedback or either operator's uncertainty.
5. While the feet remain unloaded, test local keyboard stop and inspect the actual
   damping/post-publication outcome. In separate restarts, test PICO stop, process
   death and the approved hardware E-stop procedure.
6. Do not enter POSE or lower the robot until each terminal outcome is understood,
   repeatable and reviewed.

## Rank 4 — first physical demo scope, only if separately authorized

The first weight-bearing run stops after segment 5:

1. PLANNER baseline, 10 seconds.
2. Matched transition to POSE, then five seconds still.
3. Symmetric elbow motion.
4. Both forearms approximately 10 cm forward and back, below shoulder height.
5. Torso yaw approximately 5 degrees left/right, feet and pelvis forward.
6. One symmetric 3 cm pelvis lowering via bilateral knee flexion, then neutral.
7. Return to neutral, switch once to PLANNER and perform the validated stop.

Both feet stay flat, parallel and inside marked footprints. No step, heel lift,
single-leg support, lunge, deep squat, kneel, rapid turn or large reach is allowed.
The optional 5 cm bend, lateral weight shifts and combined motion require later,
separately reviewed runs.

## Immediate abort criteria

The safety operator presses local keyboard `O` immediately for any uncommanded
step, persistent backward walking, foot slide/lift, gantry catch, sudden pose jump,
wrong direction, asymmetric knee response, increasing drift, tracker/device/socket
loss, frozen or completed stream, gap at or above 100 ms, sustained delay above the
30 ms demo gate, unexpected mode transition, stale LowState/IMU, motor error,
abnormal temperature, collision, unexpected rapid motion or operator uncertainty.
Use the hardware E-stop if motion continues or local stop is ineffective.

Do not chase the robot's recovery motion, use Menu pause/resume, improvise a mode
change or proceed to the next activity after an abort.

## Evidence package

Preserve:

- source revision and complete dirty patch;
- model/config/planner/engine hashes;
- workstation OS, GPU driver, CUDA, TensorRT, compiler and network interface;
- private G1 hardware/firmware inventory and public redacted summary;
- PICO/app/tracker versions and calibration state;
- exact commands, operator roles, gantry/load state and mode transitions;
- synchronized operator/robot/viewer video if motion is authorized;
- PICO pose chunks, target motion, measured q/dq/IMU, actions, motor status,
  temperature, torque estimate and timing;
- the exact result of every stop or disconnect test;
- operator observations separated from telemetry-derived findings.

## Expected end states

- **Minimum useful:** G1/PICO inventory and read-only DDS evidence captured; no
  physical commands.
- **Preferred software result:** exact low-latency candidate passes three complete
  instrumented simulations including stale-stream/stop tests.
- **Optional physical result:** suspended initialization and stop outcomes pass
  under separate authorization.
- **Stretch result:** planted-feet segments 0--5 pass once on the gantry. This is not
  a floor-control or general full-body safety validation.
