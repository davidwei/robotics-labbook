# SESSION-20261029-001 in-lab plan — PICO/SONIC G1-29

Date: 2026-10-29. Owner/operator: David Wei. Status: planned and gated.

This is an operator checklist and evidence-capture plan. It does not authorize
robot motion. Physical command publication requires a separate explicit motion
authorization after the applicable gates pass.

## Readiness order

| Rank | Activity | Readiness | Required before starting | Next action |
|---:|---|---|---|---|
| 1 | Hardware/firmware inventory and read-only DDS preflight | **Ready** | Powered G1 in a non-commanding state; no `rt/lowcmd` publisher | Execute and preserve evidence. |
| 2 | Exact-candidate instrumented simulation | **Conditional** | Pinned source/model/config/engine and fresh PICO stream | Complete three clean rehearsals and terminal-outcome tests. |
| 3 | Gantry-suspended initialization and stop/handover | **Blocked** | Ranks 1--2 pass; stale-input response fixed/validated; rated gantry; two operators; explicit motion authorization | Do not execute while blocked. |
| 4 | Loaded planted-feet segments 0--5 | **Blocked** | Rank 3 outcomes reviewed and repeatable; separate weight-bearing authorization | Defer until all gates pass. |

Current hard blockers include the unbounded stale-PICO behavior and the unvalidated
post-stop handover. The current SONIC deployment releases the stock motion service
at launch. Both the scripted stop and local `O` ultimately emit one damping-only
command (`Kp=0`, `Kd=8`) and then cease publication; they do not demonstrate that
the stock controller resumes.

## Run record header

At each run boundary record:

- local start/end time and run ID;
- physical versus simulation, gantry/load state and authorization given;
- operator and safety-operator names;
- source revision and complete dirty patch;
- model, observation config, planner and TensorRT engine hashes;
- launch command and exact Ethernet interface;
- G1 hardware/firmware/motion-mode inventory;
- PICO/app/tracker versions and calibration state;
- telemetry, console, PICO NPZ and synchronized-video paths;
- one short operator observation and pass/fail/abort outcome.

## Rank 1 — read-only physical preflight

1. Establish the three-meter exclusion zone. Inspect robot, feet, connectors,
   battery, temperature and gantry clearance.
2. Record G1 model/revision, manufacture date, system/control firmware, onboard
   image, service versions, pelvis and motor-driver revision, ankle mode,
   `mode_machine`, hand type and hardware E-stop state.
3. Record both motion-tracker firmware versions and charge state.
4. Configure the deliberate `192.168.123.x/24` workstation address and record the
   exact wired interface.
5. Confirm no simulator, SDK example, LeRobot/Holosoma or stale process publishes
   `rt/lowcmd`.
6. Run only the bounded read-only DDS subscriber. Require fresh CRC-valid LowState,
   29 finite q/dq entries, base/torso IMUs, normal motor status and temperatures,
   and stable rate.
7. Query the active stock motion mode without releasing it. Preserve the output and
   stop. A failure ends physical activity for this experiment.

## Pre-command PICO gate

1. Fit and calibrate both ankle trackers; verify laterality in read-only
   visualization.
2. Start XRoboToolkit PC Service and the PICO application; require `WORKING`, Full
   Body high-accuracy and Send enabled.
3. Run and stop an input-only probe: finite fresh 24-joint poses, both trackers and
   correct laterality.
4. Start the PICO manager in `OFF`. Require at least 30 continuous seconds at 50 Hz
   or better with no gap at or above 100 ms, `device missing`, socket error,
   relocalization or frozen timestamp.
5. Do not use a robot command or A+B+X+Y to make a sparse stream become healthy.

## Physical startup sequence — motion begins at launch

Execute only after all prior gates pass and a new explicit physical-motion
authorization is recorded.

1. Mount G1 on the rated gantry with feet unloaded and clearance for every limb and
   the initialization trajectory. Assign separate PICO and safety operators.
2. Safety operator takes the deployment keyboard and hardware E-stop. PICO operator
   assumes the exact neutral calibration pose.
3. Reconfirm fresh telemetry, no competing `rt/lowcmd` publisher, and that MuJoCo
   and every other DDS command process are stopped.
4. Compare measured q with SONIC's fixed default standing angles. A material
   mismatch is a launch blocker.
5. Start XRoboToolkit and the PICO manager first, remaining in `OFF`, and repeat the
   30-second freshness gate.
6. Launch the pinned deployment with the exact interface and matched model/config;
   do not rely on automatic `real` interface selection. Launch releases the stock
   motion service, starts `rt/lowcmd`, and immediately interpolates all 29 joints
   toward SONIC's default pose over approximately three seconds.
7. Observe only initialization. Abort for wrong direction, rapid motion, mapping
   mismatch, oscillation, collision, motor error or uncertainty.
8. Require `Init Done`, stable posture and reviewed live telemetry. The message
   alone is not a pass.
9. Before POSE or loading the feet, execute the suspended terminal-outcome test
   below. Each terminal outcome requires a fresh run from the beginning.
10. Only after those outcomes are understood and approved, stand in the exact
    calibration pose and briefly press and fully release A+B+X+Y once:
    `OFF -> PLANNER`. Confirm exactly one transition.
11. Hold PLANNER IDLE for ten seconds. Require upright, stationary behavior and a
    continuously fresh stream.
12. Briefly press and release A+X once: `PLANNER -> POSE`. Hold still for five
    seconds before any bounded motion.

## Bounded first-demo sequence

Advance only after returning neutral and remaining stable for three seconds:

1. symmetric elbow flex/restore;
2. both hands approximately 10 cm forward and back, below shoulder height;
3. torso yaw approximately 5 degrees left/neutral/right/neutral while pelvis stays
   forward;
4. one symmetric 3 cm pelvis lowering, hold and return neutral;
5. return to the exact matched standing pose and remain still.

Both feet remain flat, parallel and inside marked footprints. No foot lift, step,
lunge, kneel, deep squat, rapid turn, large reach or recovery-motion imitation is
allowed. Segments beyond the 3 cm lowering require a later reviewed run.

## Planned normal stop

1. Return to the exact matched neutral pose and require three stable seconds.
2. Briefly press and release A+X once: `POSE -> PLANNER`.
3. Require stationary PLANNER behavior, fresh telemetry and fresh PICO input.
4. Briefly press and fully release A+B+X+Y once: `PLANNER -> OFF`.
5. Verify the manager sent one stop event and exited, and verify the deployment
   emitted its damping-only command and ceased publication.
6. Keep the robot supported. Do not infer that the stock controller resumed and do
   not load the feet.
7. Record LowState, active motion mode and actual post-publication behavior. Restore
   stock control only through a separately reviewed and validated handover
   procedure. That procedure is not yet established for this stack.

## Immediate abort

The safety operator presses local keyboard `O` immediately for an unexpected step,
foot motion, drift, pose jump, wrong direction, oscillation, collision, motor/IMU
error, stream gap at or above 100 ms, delay violation, `device missing`, socket
loss, frozen/completed stream, tracker relocalization, duplicate transition or
operator uncertainty. Use the facility hardware E-stop if motion continues or `O`
is ineffective.

After `O`, keep G1 supported and verify the actual damping/publication/motion-mode
outcome. Do not rely on the PICO chord during a PICO/network failure. Do not use
Menu pause/resume, chase recovery motion, improvise a mode switch, or assume process
death returns control to stock. Preserve the failed run and restart only after
offline diagnosis and a new authorization.

## Terminal-outcome matrix — suspended only

Run each case separately from a clean startup and preserve telemetry/video:

| Case | Trigger | Required observation before any loaded test |
|---|---|---|
| Scripted stop | POSE -> PLANNER with A+X, then A+B+X+Y | One transition per chord; damping/publication end and subsequent motion mode measured. |
| Local abort | Keyboard `O` | Prompt process stop; damping/publication end and subsequent motion mode measured. |
| PICO loss | Deliberate disconnect | Independent monitor causes a bounded local outcome; no stale continued motion. |
| Streamer/process loss | Kill only under approved suspended protocol | Hardware outcome is bounded and understood; never inferred from simulation. |
| Hardware E-stop | Facility-approved procedure | Motion ceases as documented and recovery/restart procedure is understood. |

No terminal outcome passes merely because the process exits. A pass requires the
physical motor behavior, DDS publication state and post-stop controller ownership
to be observed and recorded.

