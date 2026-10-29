# G1-29 PICO/SONIC PC2 preparation — 2026-10-30

The operator selected a fully unloaded gantry-suspended diagnostic. Stale PICO
input and unknown stock-controller handover remain blockers for loaded and
untethered trials; the operator wants those outcomes measured under suspension
with whole-body IMU/state capture. No SONIC motion was run in this capture.
The [operating order](in-lab.md) records the revised suspended protocol.

On G1 PC2 (`aarch64`, Ubuntu 22.04, Jetson L4T 36.4.3), NVlabs SONIC revision
`1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b` was checked out. The
low-latency encoder, decoder, matched observation config and planner were
downloaded. TensorRT 10.7, CUDA 12.6 runtime/development files and ONNX Runtime
1.16.3 were placed in the local workspace, and `g1_deploy_onnx_ref` built. The
ARM64 XRoboToolkit PC Service was unpacked as a local installation because a
system `dpkg` installation required an unavailable sudo password. Its five-second
startup check stayed alive; the Python binding and PICO manager imported. PICO
connection, TensorRT engine generation, exact-candidate simulation and full
SONIC runtime behavior are not validated on PC2.

A new independent **read-only** DDS recorder captured five seconds of G1
LowState, base IMU, torso IMU and LowCmd on `enP8p1s0` (192.168.123.164).
Counts were 962 LowState, 1,549 torso IMU and 911 LowCmd samples, with zero
application queue drops and callback failures. Captured LowState and LowCmd
CRC checks passed; 29 body q/dq and sampled base/torso quaternions were finite;
all sampled body motor status codes were zero. A CRC-valid `rt/lowcmd` stream
was already present, with zero Kp/Kd/tau in the sampled body slots. No PC2
robot-controller process was found in the process inspection, but the publisher
has not been identified. The recorder's LowState capture rate was about 192 Hz,
so it does not claim every DDS message was preserved.

At 01:17, a second 15-second read-only preflight received 2,924 LowState,
4,834 torso IMU and 2,767 LowCmd samples. Every captured LowState and LowCmd
passed CRC; all sampled 29-body q/dq and base/torso IMU values were finite,
and all sampled body motor status codes were zero. Recorder drops and callback
failures were zero. XRoboToolkit PC Service is running locally on PC2; a
20-minute read-only DDS capture began at 01:18:39 for the PICO preflight.
The PICO app has not yet connected, and SONIC has not commanded the robot.

The operator then connected PICO (`192.168.0.171`) to PC2 XRoboToolkit
(`192.168.0.201`). The first input checks were inconclusive because the probe
omitted the SDK's `init()` call; after that correction, a service-side device
disconnect left the SDK with no body frames despite a TCP socket still
receiving bytes. Restarting the local XR service and reconnecting PICO cleared
the condition. A subsequent **input-only** check passed: 2,160 finite 24-by-7
body frames over 30.02 continuous seconds (71.96 Hz), maximum device frame
gap 29.09 ms, maximum receive gap 48.03 ms, zero restarts. This is one passing
window, not a stale-input or reconnection reliability result.

The long read-only DDS capture was interrupted after the PICO check and has no
closing summary line. Its intact JSONL records contain 176,249 LowState,
285,636 torso IMU and 167,081 LowCmd messages; all captured LowState/LowCmd
CRC checks passed. No SONIC deployment, control handover or motion occurred.

Next: identify the existing command publisher and G1 hardware/firmware;
verify the exact PC2 candidate and repeat PICO freshness before motion; arrange an operator
and separate safety operator, full unloading and clearance, local `O` and E-stop,
independent capture through the post-stop period, and explicit authorization
before a suspended initialization/stop diagnostic. Loaded or untethered motion
waits for review of stale-input and stop/handover outcomes.
