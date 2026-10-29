# G1-29 PICO/SONIC PC2 preparation — 2026-10-30

The operator selected a gantry-protected diagnostic. Stale PICO input and
unknown stock-controller handover remain blockers for untethered trials; the
operator wants those outcomes measured under gantry protection
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

The operator then questioned whether feet-clear suspension would make SONIC
keep stepping. Source inspection found an INIT default-pose ramp followed by
WAIT_FOR_CONTROL; the walking policy is entered only on a separate start signal.
The operating order now limits feet-clear operation to the short INIT/local-O
diagnostic. Later PLANNER/POSE tests call for controlled foot contact under the
gantry, each separately authorized. The operator reported that both feet are
now clear, limb clearance is established and an E-stop is at hand. A distinct
safety operator and the current LowCmd publisher have not yet been confirmed.

PC2 TensorRT 10.7 built and deserialized the low-latency encoder, decoder and
planner ONNX models offline with `--skipInference`. This checks parser/build
compatibility only; it is not a SONIC runtime inference or motion validation.

In [RUN-20261030-001](runs/RUN-20261030-001.md), the operator explicitly
authorized a feet-clear INIT/local-`O` diagnostic. SONIC used keyboard input and
PICO never started policy control. The default-pose transition settled in about
three seconds without sampled motor errors. Terminal polling delayed `O`, leaving
the default pose commanded for about 26 additional seconds. The operator described
the motion as smooth. `O` was accepted and
the process exited normally. Independent capture saw command publication stop,
but no damping frame or resumed stock LowCmd during 5.37 seconds of post-stop
capture. Suspended joints relaxed by as much as 0.406 rad. A delayed three-second
check still received zero LowCmd, confirming the prior stock stream had not
resumed. This does not validate the stop/handover path. Further motion testing
requires a fresh setup. The operator recognized this as prior development-mode
behavior and accepted the missing automatic mode restoration for gantry-only
work. Untethered testing remains blocked.

An input-only PICO manager preflight then ported the previously missing
A+B+X+Y full-release latch to PC2. Unit tests passed (2 tests), and no SONIC
deployment subscribed to the manager during either live check. At source revision
`dc86407cb94e3b335671677ece90b6fdae401471`, the first chord produced exactly one
OFF-to-PLANNER transition and remained there after release; a second chord reached
the shutdown path once. PICO samples during the chord interval were approximately
72 Hz. The process nevertheless aborted after printing `Shutdown complete`
(exit 134), so that attempt is preserved as a latch pass but teardown failure.

Inspection found that the stop branch raised `SystemExit` and the manager never
closed XRoboToolkit. Revision `632b6b71f974a3a9fe24eb920c210084bda44989`
returns normally after publishing stop and explicitly closes the SDK. A second
input-only live check produced exactly one OFF-to-PLANNER and one
PLANNER-to-OFF transition, printed `Shutdown complete`, uninitialized the SDK and
exited 0. This validates the chord latch and normal manager teardown in a live
headset-only preflight. It does not validate stale-input behavior, robot stop,
stock-controller handover or policy motion. Both local SONIC commits are two
commits ahead of the NVlabs remote and were not pushed upstream.

The operator then narrowed the active work to gantry-tethered experiments.
Watchdogs and other complexity needed only for untethered use are deferred. The
next experiment may therefore measure stale-input and stop behavior while fully
suspended, with independent whole-body state/IMU/LowCmd capture and an E-stop
operator; its result must not be generalized to untethered operation.

Before [RUN-20261030-002](runs/RUN-20261030-002.md), the planner TensorRT engine
was inadvertently built only after the operator had donned PICO and the robot had
been authorized for initialization. The operator corrected the ordering: model
engines must be built before headset-dependent physical work. The first initialized
instance was stopped without a policy chord, then a clean launch loaded the saved
engine and reached `Init Done` before the operator wore PICO.

RUN-20261030-002 exercised the live PICO start and stop path with G1 fully
suspended. Exactly one OFF-to-PLANNER and one PLANNER-to-OFF transition occurred;
SONIC entered IDLE planner control and exited normally on the PICO stop. The
chord-to-chord interval lasted 22.54 seconds; the operator later clarified that
this extra length was expected, correcting the initial protocol-miss
interpretation. The operator observed stepping attempts and feet tapping toward
the floor, as expected from simulation. Telemetry measured a
peak left-knee speed of 8.12 rad/s, a maximum right-shoulder-yaw range of 0.821
rad and no sampled motor error/status or CRC failure. No damping or resumed stock
LowCmd was captured after stop. This is a suspended PICO start/stop observation,
not a stale-input test.

For the next suspended validation, the operator proposed placing the feet close
to, but still clear of, the floor because a larger gap might cause harder stepping
attempts. The current enabled policy observations do not directly include foot
clearance or contact force, so that causal explanation remains a hypothesis. The
setup refinement is to record clearance after `Init Done` and preserve clearance
through the expected downward foot excursion. Any intentional or actual floor
tap changes the activity to a controlled-contact test and requires separate
preparation and authorization.

Next: prepare a separately authorized fully suspended stale-input test with a
locally controlled stop and the same independent capture. Retain the measured
knee-speed evidence when bounding the next run, and record foot clearance after
`Init Done`. G1 hardware/firmware identity remains incomplete. Ground-contact and
untethered work remain deferred.
