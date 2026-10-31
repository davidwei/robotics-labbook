# PICO/SONIC diagnosis and proposed G1-29 physical plan — 2026-10-28

Status: analysis and pre-lab design only. No physical motion is authorized by this
document. The current simulation evidence includes one unexplained fall and is not
yet sufficient for a floor trial.

## Operator scope update — 2026-10-30

The operator selected a **gantry-protected diagnostic** on G1-29. The first
initialization and local-stop run keeps the feet clear. Later walking-policy
tests need controlled foot contact while the gantry remains ready to catch the
robot; an unloaded policy may step repeatedly while seeking contact. The
unresolved stale-input response and stock-controller handover remain hard
blockers for **untethered** work, but may be measured under gantry protection.
This supersedes the earlier blanket block on suspended commissioning
in this document and the October 29 checklist. It does not make a stale stream or
one damping-only stop safe, and it does not authorize command publication by
itself. The first PC2 run is a new deployment environment relative to the
previously tested x86 workstation.

Before any suspended launch, identify this robot's 29-DOF hardware/firmware and
the existing `rt/lowcmd` publisher, inspect clearance and the gantry, assign
separate PICO and safety operators, review local `O` and facility E-stop, pin the
exact PC2 model/config/engine candidate, and record explicit motion authorization.
Start an independent read-only capture **before** SONIC and leave it running
through shutdown and post-stop observation. Capture receipt wall/monotonic times,
CRC-valid LowState, all 29 body q/dq/estimated torque/motor status/temperature,
base quaternion/gyro/accelerometer, torso quaternion/gyro/accelerometer,
`rt/lowcmd` q/dq/Kp/Kd/tau and mode, PICO source/arrival timestamps, deployment
action/mode/stream-age logs, synchronized video and operator observations.
Record logger coverage and sample gaps; a capture that drops or omits material
signals is not a reproducible failure record.

For the first suspended motion run, keep both feet unloaded and observe only
SONIC's automatic initialization, then a local `O` stop and the measured
post-publication state. Test PICO stop, stale input, streamer/process loss and
hardware E-stop as **separate** gantry-protected runs after reviewing the
preceding run. The INIT state moves to the default pose and then
WAIT_FOR_CONTROL; the walking policy starts only on a separate start signal.
The safety operator stops immediately at an unexpected motion, tracking loss or
stream warning; do not wait for autonomous recovery. Mode transitions and POSE
motion remain later steps after fresh-input and controller-latch checks and
require controlled foot contact under the gantry. Untethered planted-feet
segments wait until stop and stale-input outcomes are reviewed.

## Why the full-body path worked in the successful run

The earlier failures occurred at several different layers; they were not one SONIC
decoder defect.

1. Initially, XRoboToolkit reported `body_available=false`, zero body-timestamp
   updates and no motion trackers. PICO logs reported `NoTracker`. Head and
   controller transport worked, but there was no 24-joint body frame for the
   streamer to consume.
2. The operator synchronized and calibrated both ankle trackers, selected Full Body
   high-accuracy mode, enabled Data/Control Send, and relaunched/reconnected the
   XRoboToolkit app after its socket became stale. The next bounded probes returned
   finite 24-by-7 poses and advancing global stream timestamps.
3. The workstation service, Python binding, compatible TensorRT runtime, model
   engines, MuJoCo DDS simulator and native deployment were all present together
   only in the successful run. vLLM had also been stopped so the two RTX 5090 GPUs
   had capacity for deployment.
4. The manager had to own the XRoboToolkit stream and be in `POSE`. Its reader only
   updates when `is_body_data_available()` is true and the global timestamp
   advances. It then derives SMPL data, fills a five-frame buffer and publishes the
   `pose` topic at a nominal 50 Hz. `OFF` and `PLANNER` do not send those SMPL pose
   chunks to the active streamed-motion controller.
5. An observed controller-edge bug made one held A+B+X+Y chord look like two events
   after a transient dropped-button sample, causing OFF-to-PLANNER and then an
   immediate PLANNER-to-OFF. The local latch change requires complete release of all
   four buttons before rearming. After this change, OFF-to-PLANNER remained active;
   A+X then selected POSE and the deployment decoded continuous protocol-v3 chunks
   in SMPL encoder mode `2`.

The logs prove those layer transitions. They do not prove that every earlier failed
attempt had the same cause. `get_body_timestamp_ns()` remained zero even in the
working configuration; this implementation succeeds because `PicoReader` uses the
advancing global `get_time_stamp_ns()` instead.

## What the available logs say about unstable poses

The simulator emitted repeated fall warnings after one PLANNER-to-POSE transition;
MuJoCo base height was approximately 0.19--0.20 m and its fall handler reset the
model. A later operator-reported full-body trial kept the manager, deployment and
simulator alive without a new warning in the sampled interval. PICO input was about
56--66 Hz, pose processing about 49 Hz, and one deployment sample reported roughly
24 ms mean stream delay with about 11 ms standard deviation.

No target-motion file, state CSV, PICO NPZ sequence or synchronized video was
enabled. Therefore the fall cannot be aligned to an exact human pose or frame. The
following risk ranking combines the observed transition timing with the repository's
documented behavior; only the first item is strongly supported by this run.

1. **Pose mismatch at entry to POSE — highest confidence.** POSE applies the live
   SMPL reference immediately. Entering while the operator is crouched, leaning,
   reaching or facing differently from the planner's standing robot can demand a
   discontinuous whole-body correction. NVIDIA explicitly warns that this can cause
   sudden aggressive motion.
2. **Low-pelvis or deeply flexed poses.** Deep crouch, kneel, sitting, crawling and
   lying poses reduce margin and should not be part of initial commissioning. The
   observed fall height establishes a low-base outcome, not which low pose caused it.
3. **Asymmetric support.** High foot lift, single-leg stance, crossed feet, a long
   lunge or abrupt lateral weight transfer gives little recovery margin and depends
   most on correct ankle tracking.
4. **Large torso lean/twist combined with leg motion.** Root orientation changed
   materially in captured streamed frames, but the logs cannot label a particular
   angle unstable. Avoid using an inferred quaternion threshold until synchronized
   trials establish one.
5. **Tracking discontinuity rather than a biomechanical pose.** Occlusion, loose
   clothing, stale sockets, tracker relocalization or a mode resume from a different
   human pose can create a target jump that looks like an unstable pose.
6. **Interrupted or hesitant dynamic motion.** Repository guidance says natural,
   smooth weight transfer is more stable than artificially slow mid-stride motion.
   This does not justify fast initial tests; start with static poses, and only later
   test a natural step under restraint.
7. **High/jittery transport delay.** The documented acceptable band is 10--30 ms and
   poor is above 30 ms. A 24 ms mean with about 11 ms standard deviation is usable
   simulation evidence but too close to the boundary to infer a safe physical tail.

Until better evidence exists, the initial allowed envelope should be upright,
feet parallel and planted, small smooth arm motions, small torso rotations and small
bilateral knee flexion. Avoid foot lift, lunges, deep squat/kneel, rapid turns,
crossed feet, large reaches and any POSE transition made while human and robot poses
do not visually match.

## Code-level physical risks that need explicit disposition

- Starting the real executable is itself motion authorization: `InitControl()`
  interpolates measured joints to fixed 29-DOF default angles over three seconds
  before a PICO start command.
- The source releases the stock motion service, publishes `rt/lowcmd`, and controls
  all 29 joints. Confirm the actual robot is the matching 29-DOF embodiment, ankle
  mode and motor configuration before launch.
- LowState older than 500 ms stops control. The joint-velocity check is only
  `body_dq[i] > 35` in current source, not absolute magnitude; negative overspeed is
  not caught by that condition.
- Stream age above 150 ms drives a debounced audio warning, not a demonstrated stop.
  Token age above 200 ms warns and retains the last token. A frozen or stale human
  target therefore must not be assumed fail-safe.
- Normal stop waits for the publishing threads, sends one damping-only frame
  (`kp=0`, `kd=8`, zero feed-forward), then ceases publication. What the G1 does
  next, and whether/when stock control resumes, is not established by this run.
- The A+B+X+Y latch fix and TensorRT/build compatibility changes are local and
  uncommitted. They need review, tests and a pinned physical-candidate revision.
- The simulation used the default `policy/release` encoder/decoder with a 10-frame
  SMPL reference configuration. The repository documents a separate low-latency
  checkpoint for teleoperation. Select one physical candidate deliberately and rerun
  the complete simulation protocol with that exact model/config pair.

## Gated physical G1-29 plan

Every gate requires an explicit pass record. A failure returns to offline analysis;
it does not authorize improvising the next gate.

### Gate 0 — close the simulation evidence gap

1. Pin a clean source revision plus reviewed patches; record hashes for encoder,
   decoder, observation config, planner and generated TensorRT engines.
2. Choose the physical model candidate. Prefer evaluating the documented
   low-latency teleoperation checkpoint first; never mix an encoder/decoder with a
   different observation config.
3. Repeat at least three complete simulation sessions with PICO NPZ recording,
   target-motion logging, state CSV, motion recording, bounded console logs and
   synchronized viewer/operator video.
4. In each session test: neutral calibration, OFF-to-PLANNER, visually aligned
   PLANNER-to-POSE, planted-feet arm motion, small bilateral knee flexion, small
   weight shift, left/right foot motion, POSE-to-PLANNER, stop and restart.
5. While simulation is restrained, deliberately test controller release/repress,
   PICO app disconnect, Wi-Fi interruption, tracker occlusion and streamer death.
   Record actual behavior; do not infer it from warning text.
6. Pass only if there are no unexplained falls or target discontinuities, all mode
   transitions are single events, stop/restart is repeatable, mean and tail latency
   remain acceptable, and pose/video/logs agree. Proposed transport gate: p95 below
   30 ms, no unexplained gap at or above 100 ms. These are conservative trial gates,
   not validated hardware limits.

### Gate 1 — pre-lab, read-only robot and facility check

1. Obtain separate authorization for a suspended G1 motion trial. Launching the
   deployment counts as motion because of the automatic initialization ramp.
2. Confirm G1-29 identity, installed joint/motor variant, firmware, ankle mode,
   battery state, hand configuration and the expected 29 finite LowState slots.
   Verify CRC, IMUs, joint positions/velocities, motor status and temperature without
   publishing low-level commands.
3. Confirm the exact network interface instead of accepting `deploy.sh real`'s
   fallback to an arbitrary non-loopback interface.
4. Stop MuJoCo and any competing DDS/low-level controller. Confirm no stale process
   can publish `rt/lowcmd`. Keep PICO and deployment on a private low-latency network.
5. Use a rated gantry, clear three-meter zone, physical barriers where appropriate,
   fitted clothing and visible ankle trackers. Assign separate people as PICO
   operator and safety operator. The safety operator owns the deployment terminal
   (`O`) and hardware E-stop and does not wear the headset.
6. Write down the expected result of keyboard `O`, PICO A+B+X+Y, process death,
   network loss and hardware E-stop. Do not proceed if any terminal outcome is
   unknown or cannot be safely observed on the gantry.

### Gate 2 — suspended commissioning, feet unloaded

1. Put the G1 in the documented loose standing configuration on the gantry, with
   sufficient clearance for the three-second default-pose interpolation. Match the
   measured pose to SONIC's default pose as closely as practical before launch.
2. Start XRoboToolkit and the PICO manager first, remain in OFF, and require stable
   fresh 24-joint frames, both trackers, neutral calibration pose and acceptable
   latency. Then launch the pinned real deployment with the explicit interface and
   full logging enabled.
3. Observe only the initialization ramp. Abort on an unexpected joint direction,
   mapping mismatch, motor error, stale feedback, excessive velocity, oscillation,
   collision or operator/safety disagreement.
4. Before full-body motion, test keyboard `O` and inspect the actual damping and
   post-publication behavior. Restart and test A+B+X+Y stop. Test hardware E-stop
   according to the facility procedure. No loaded-leg trial proceeds until all
   three outcomes are understood and repeatable.
5. Do not enter PLANNER/POSE with both feet clear. Move policy, dropout and
   occlusion tests to a separately authorized gantry-protected contact run.

### Gate 3 — controlled foot contact under gantry protection

1. Review Gate 2 telemetry/video before lowering. Start with bilateral foot contact
   and the gantry carrying enough load to arrest a fall; do not begin on an
   unrestricted floor.
2. Repeat initialization and PLANNER idle. Require stable base/torso attitude,
   normal motor status/temperature, fresh LowState/IMU and stable latency.
3. Enter POSE only after visual pose alignment. Progress one category per run:
   planted-feet arms; small torso rotation; shallow symmetric knee flexion; small
   lateral weight transfer with both feet planted.
4. Test planned PICO stop, dropout and occlusion in separate runs with the safety
   operator ready to stop at the first stale warning or unexpected motion.
5. Stop and review after each category. Any slip, oscillation, unexpected direction,
   repeated correction, tracker jump, delay warning or need for a catch is a failed
   gate.

### Gate 4 — restrained stepping

1. Under full gantry protection, test a single natural in-place weight transfer,
   then one low foot lift, then one in-place step. Do not combine stepping with a
   turn or large arm reach.
2. Repeat separately left and right. Confirm tracker laterality, target/measured
   agreement, base attitude, joint velocity, contact behavior and stop response.
3. Only after repeatable in-place steps test one short forward step. Deep squat,
   kneel, lunge, running, jumping, crawling and lying modes remain out of scope.

### Gate 5 — floor trial, separately authorized

A floor trial is a new physical authorization, not an automatic continuation. It
requires repeatable Gates 0--4, no unexplained simulator or gantry fall, reviewed
stop/handover behavior, acceptable latency tails, a preserved evidence package and
agreement from the operator and safety lead. Begin again with PLANNER idle,
planted-feet arm motion and a single small step inside the clear zone. Advanced
poses remain prohibited until a separate envelope-expansion protocol is reviewed.

## Evidence required from every physical run

Record the source revision and dirty patch, all model/config/engine hashes, robot
identity and firmware, network/interface, command line, operator roles, gantry state,
PICO/tracker status, calibration and mode transitions. Preserve synchronized video,
PICO pose chunks, target motion, measured q/dq/IMU, actions, motor status,
temperature, torque estimate, stream/LowState age and the exact stop outcome. Record
operator observations separately from telemetry-derived findings.

## Post-run stale-stream observation

After the initial full-body test, the operator observed the simulated robot
continually walking backward as if trying to maintain balance. Concurrent logs
showed the PICO manager reporting `device missing`, the deployment repeatedly
printing `Motion streamed completed and waiting following motion`, and a streaming
data mean delay of approximately `538489 ms` with about `5773 ms` standard
deviation. The deployment remained in SMPL encode mode `2` and continued control on
an exhausted/stale streamed reference.

Classify this state as unstable/degraded even though the policy was still producing
balance-recovery motion and MuJoCo had not emitted a new fall warning. It is not
evidence of valid live teleoperation. This directly confirms that loss of the PICO
body stream does not automatically produce a prompt safe stop in the tested path.
Gate 0 must therefore demonstrate an explicit bounded stale-stream response before
any physical launch; audio warning or continued tracking of the last reference is
not an acceptable physical pass condition.

## Final simulation mode-transition rehearsal

On 2026-10-28, a fresh simulation-only deployment reached `Init Done` using source
revision `1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b`, the repository's
`policy/release` encoder/decoder, `planner/target_vel/V2/planner_sonic.onnx`,
MuJoCo on loopback DDS, XRoboToolkit PC Service and the PICO manager with NPZ
recording enabled. This was a mode-transition rehearsal, not a complete pass of
the planted-feet protocol and not validation of the intended low-latency physical
candidate.

Before the operator chords, sampled PICO device timestamp intervals were erratic:
the reported EMA was approximately 14--36 Hz and individual sampled intervals were
approximately 100--610 ms. The operator then fully pressed and released A+B+X+Y,
waited in PLANNER, pressed and released A+X to enter POSE, and later returned with
A+X. The logs recorded exactly one transition for each action:

- `OFF -> PLANNER`;
- `PLANNER -> POSE`;
- `POSE -> PLANNER`.

After the first transition, PICO device intervals became approximately 13--21 ms
(about 59--69 Hz). During POSE, the pose loop sustained approximately 47.7--50.0
Hz. The deployment reported streaming-data delay mean 17.477 ms and standard
deviation 10.263 ms. These measurements show that the host pipeline was capable
of the target rate during the active interval. They do not identify why input was
sparse beforehand. Candidate explanations are PICO body-pipeline warm-up,
tracker/body reacquisition, or headset/application scheduling; the evidence does
not distinguish them.

Operational implication: do not treat entering PLANNER as a remedy for a sparse
stream on hardware. The physical pre-command gate remains at least 30 seconds of
fresh input at 50 Hz or better with no 100 ms gap. If that gate is not satisfied,
reacquire/restart tracking without publishing robot commands. A later diagnostic
run should record every source timestamp and host arrival time continuously so
device generation, transport batching and host scheduling can be separated.
