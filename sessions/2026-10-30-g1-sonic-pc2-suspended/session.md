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

[RUN-20261030-003](runs/RUN-20261030-003.md) then tested tethered,
full-weight-bearing ground contact with the gantry configured only as a fall
catch. After ground-contact initialization, the operator executed the PICO
start/count/stop sequence independently. During the 12.28-second IDLE planner
interval, the operator reported firm standing and no gantry support. The manager
logged one start and one stop, and SONIC exited normally. No sampled motor
error/status, CRC failure or recorder drop occurred. Maximum leg range was 0.613
rad at the left knee; base roll/pitch/yaw ranges were approximately
3.8/9.5/9.0 degrees.

The stop did not preserve standing. After the second chord, LowCmd publication
ceased, no stock command resumed during 60.23 seconds of retained capture, and
the robot relaxed into the gantry. The operator identified this as the same
development-mode behavior seen previously. Thus active tethered IDLE standing
was demonstrated, while stand-preserving stop and controller handover remain
absent.

Next: review whether the next tethered experiment should isolate stale PICO input
or exercise a small bounded teleoperation motion. Every run must retain the gantry
through and after stop because the robot does not remain standing when SONIC exits.
G1 hardware/firmware identity remains incomplete; untethered work remains deferred.

The operator selected the next experiment as tethered PICO full-body control. The
first POSE run is bounded to the existing demo's segments 0--2: ten-second PLANNER
standing, visually matched A+X entry to POSE, five-second still hold, one slow
symmetric elbow bend/restore below shoulder height, return to matched neutral,
A+X back to PLANNER, standing verification, then PICO stop. Torso, pelvis,
lower-body and locomotion motions are deferred. The gantry remains engaged through
post-stop because RUN-20261030-003 showed that SONIC exit does not preserve
standing.

[RUN-20261030-004](runs/RUN-20261030-004.md) attempted that bounded POSE entry.
The robot initially stood firmly in PLANNER and the operator reported visual pose
alignment. Immediately after A+X and `PLANNER -> POSE`, both legs retracted into
the air. Within 0.50 seconds, left/right knees moved from approximately
0.249/0.208 rad to 1.960/2.200 rad and hip pitch moved from -0.085/+0.162 rad to
-1.456/-1.751 rad. POSE output was approximately 31--33 Hz, below the earlier
simulation rate.

The operator intentionally pressed A+B+X+Y directly from POSE after observing the
unexpected tuck. The resulting `POSE -> OFF` was a correct terminal stop, not a
missed A+X return; the planned elbow cycle was intentionally aborted. The manager
stopped cleanly, while SONIC timed out resetting the planner and aborted during
CycloneDDS cleanup (exit 134). The operator confirmed the robot was secured on
the gantry.

The run cannot determine whether PICO requested the tuck. The manager did not
record raw XR body joints or outgoing SMPL packets, and SONIC's console trace
prints only the pelvis entry rather than knee/ankle inputs. Lower-body tracking,
coordinate/joint-order conversion and the policy transition remain competing
hypotheses.

Local SONIC revision `8d916d4384864aa3417bbe4eaa1944bfe4793c20` adds
replay-grade capture before any repeat: exact manager ZMQ payloads across PLANNER,
POSE, command and stop traffic; packet timestamps and mode tags; per-packet
hashes; aligned raw 24-by-7 XR body poses; and continuous raw body/controller
samples across OFF, calibration, PLANNER, POSE and stop. Read-only live-input and
final-capture validators plus an explicit simulation replay tool passed four
focused tests with the existing chord latch. Dedicated next-run wrappers require
the independent robot recorder and PICO packet capture before SONIC launch.

A headset-only integration capture preserved 421 replay packets over 15.04
seconds: 167 planner, 250 pose and four command packets, with 250 aligned raw XR
frames. Raw left/right knee geometry remained approximately 168.6--170.1 and
168.6--169.9 degrees; converted SMPL knee geometry remained approximately
163.5--165.2 and 168.5--169.8 degrees. Hip-to-ankle and ankle-to-foot lengths were
stable. The captured human pose was therefore nearly straight and does not explain
the physical robot's approximately 2.0--2.2 rad knee tuck.

The final four-button stop sample briefly produced
`POSE -> PLANNER_FROZEN_UPPER_BODY -> OFF`, exposing a controller-sample ordering
issue not visible in the first physical run. The expanded logger now preserves
continuous raw buttons so any recurrence is reconstructable.

The expanded logger then received 853 input-only samples over 14.73 seconds after
another PICO reconnect. It rejected the stream: six device-timestamp gaps exceeded
100 ms (maximum 359.9 ms; 167.3 ms still occurred in the final five seconds), raw
left/right knee geometry was fixed at 45.6/61.3 degrees, and all 853 body-pose
arrays were bit-for-bit identical despite advancing timestamps. No controller
buttons were pressed. This anatomically bent, frozen stream is a credible source
for a leg-tuck response and demonstrates that connection status alone is not a
readiness signal.

An isolated PC2 MuJoCo environment was also prepared for exact replay. Loopback
simulator and deployment startup reached DDS communication, but simulator
LowState messages carried CRC zero and the deployment rejected them. Exact packet
replay was therefore not completed and no simulation conclusion was drawn.

The lab session ended with G1 secured on the gantry and no SONIC deployment,
PICO manager, simulator, replay process or independent recorder remaining.

Next: recalibrate both ankle trackers/full-body tracking and pass an input-only
upright/freshness check with one small arm motion before considering any physical
repeat. Resolve simulator LowState CRC if exact replay remains desired. For every
later physical run, keep independent DDS, exact manager packet/raw-input,
SONIC CSV/console and optional synchronized video capture active from before
initialization through at least 45 seconds after stop. Untethered work remains
blocked.
