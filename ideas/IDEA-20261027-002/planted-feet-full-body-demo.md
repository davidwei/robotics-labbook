# Planted-feet PICO/SONIC full-body demo

Status: proposed simulation protocol. Physical execution requires separate
authorization and completion of the physical gates in
`g1-29-physical-plan-20261028.md`. “Relatively safe” means deliberately reduced
exposure; it does not mean safe or physically validated.

## Demonstration objective

Show live full-body control using arms, torso, pelvis and both legs while retaining
a broad support polygon. The operator keeps both feet planted throughout. The demo
excludes locomotion, single-leg support and low-pelvis actions.

The defining lower-body action is a shallow, symmetric knee bend that lowers the
operator pelvis slightly and returns to calibrated standing. This demonstrates
lower-body mapping without requiring a step.

## Provisional movement envelope

These are conservative choreography limits for the first demo, not validated G1
stability limits. Measure them relative to the operator's calibrated standing pose.

| Quantity | Initial target | Do not exceed in this demo |
|---|---:|---:|
| Pelvis lowering | 3 cm | 5 cm |
| Pelvis lateral shift | 1--2 cm | 3 cm |
| Pelvis fore/aft shift | approximately zero | 2 cm |
| Torso pitch/roll | approximately zero | 5 degrees |
| Torso yaw | 5 degrees each side | 10 degrees each side |
| Arm elevation | below chest/shoulder level | 45 degrees from the side |
| Movement time | 2 seconds out, 2-second hold, 2 seconds back | no abrupt reversal |

Feet remain hip-width, parallel and flat inside marked footprints. Neither heel nor
toe intentionally lifts. Feet do not translate, rotate, cross or narrow the stance.
Knee flexion is bilateral and visually symmetric; the torso remains upright rather
than hinging forward. Hands remain inside a comfortable envelope near the torso and
never make a large overhead, downward or cross-body reach.

Excluded actions: stepping, marching, heel raises, single-leg stance, lunge, deep
squat, kneel, sit, crawl, lie down, jump, run, rapid turn, crossed feet, large torso
lean, large reach, floor pickup and mode changes while the operator and robot poses
do not match.

## Roles and controls

- **PICO operator:** follows the choreography, watches tracking status, and does not
  imitate or chase a robot recovery step.
- **Safety operator:** watches the robot/simulator and deployment logs, keeps a hand
  on keyboard `O`, and owns the stop decision. On hardware this person also owns the
  facility E-stop and does not wear the headset.
- **Recorder/caller, if available:** calls each segment and records pass/fail so the
  PICO operator does not divide attention.

PICO A+B+X+Y is the normal scripted mode command. Keyboard `O` is the primary abort
because it remains local when PICO/XRoboToolkit is disconnected. Do not use Menu
pause/resume in this demo; releasing pause from a mismatched pose can create a jump.

## Entry gates

1. Use the exact pinned model/config/engine candidate already passed in simulation.
2. XRoboToolkit reports `WORKING`; both ankle trackers are paired, calibrated,
   visible and adequately charged; Full Body high-accuracy and Send are enabled.
3. A prior instrumented POSE-mode simulation rehearsal with the same candidate has
   pose-loop rate at least 45 Hz, PICO input at least 50 Hz, stream-delay p95 below
   30 ms, and no unexplained gap at or above 100 ms. Immediately before the demo,
   a 30-second stationary input check confirms finite fresh body frames and at least
   50 Hz PICO input. These are operational demo gates, not established hardware
   safety limits.
4. No `device missing`, socket error, tracker relocalization, `Motion streamed
   completed`, delay warning, duplicate mode transition or simulator fall appears.
5. The robot/simulator remains still and upright in PLANNER idle for ten seconds.
6. Before POSE, the operator visually matches the robot: upright, feet parallel,
   upper arms down, elbows bent approximately 90 degrees and palms inward.
7. For physical execution only: rated gantry, clear three-meter zone, separate
   safety operator, read-only robot preflight, validated local stop and validated
   post-stop/handover behavior are mandatory. The observed stale-stream behavior is
   a hard blocker until an independently tested bounded response exists.

## Scripted demonstration

The caller advances only after the previous segment returns to neutral and remains
stable for three seconds. One unexpected recovery step fails the run.

| Segment | Duration | Operator action | Pass observation |
|---|---:|---|---|
| 0. PLANNER baseline | 10 s | Stand in matched calibration pose; no joystick input. | Robot remains upright and stationary; stream is fresh. |
| 1. Enter POSE | 5 s | Brief A+X while holding the matched pose; then remain still. | One mode transition, no snap, step or drift. |
| 2. Elbows | 12 s | Symmetrically reduce and restore elbow bend once. | Arms follow smoothly; feet and pelvis remain still. |
| 3. Hands forward | 12 s | Move both forearms/hands forward about 10 cm and return; no shoulder-height reach. | Symmetric response without trunk compensation. |
| 4. Small torso yaw | 18 s | Rotate torso about 5 degrees left, neutral, then right, neutral; pelvis faces forward. | No foot rotation, step or accumulating lean. |
| 5. Pelvis minus 3 cm | 9 s | Symmetric shallow knee bend: 2 s down, 2 s hold, 2 s up, then neutral. | Both feet flat; torso upright; no correction step. |
| 6. Pelvis minus 5 cm | 9 s | Repeat to at most 5 cm only if segment 5 was clean. | Same criteria; otherwise skip. |
| 7. Small weight shifts | 18 s | Shift pelvis 1--2 cm left, neutral, right, neutral; both feet remain fully planted. | No foot unloading, sliding or recovery step. |
| 8. Integrated symmetric motion | 12 s | Lower pelvis about 3 cm while moving both forearms forward slightly; return together. | Smooth coordinated response with broad support. |
| 9. Neutral verification | 5 s | Return exactly to matched standing pose and remain still. | Robot settles without drift or repeated correction. |
| 10. Exit | 5 s | Brief A+X to PLANNER, remain still, then scripted stop. | Single transition to stationary PLANNER; expected stop outcome. |

Segments 6--8 are optional escalation, not required for a successful first demo. A
clean run through segment 5 already demonstrates upper and lower full-body control.

## Immediate abort criteria

The safety operator presses local keyboard `O` immediately for any of the following;
on physical hardware use the facility E-stop if motion continues or `O` is
ineffective:

- any uncommanded step, including persistent backward balance stepping;
- foot slide, heel/toe lift, gantry catch, fall warning or obvious loss of balance;
- sudden pose jump, wrong direction, asymmetric knee response or increasing drift;
- `device missing`, socket disconnect, tracker loss/relocalization, frozen frame,
  `Motion streamed completed`, or stream gap at or above 100 ms;
- sustained stream delay above the 30 ms demo gate or pose rate below 45 Hz;
- duplicate/unexpected mode transition;
- stale LowState/IMU, motor error, abnormal temperature, collision or unexpected
  rapid joint motion;
- either operator is uncertain about the state or next action.

Do not attempt to “save” the run by stepping, matching the robot's drift, pressing
Menu pause, or rapidly switching modes. Stop, preserve evidence, diagnose offline,
reset and begin a new run from calibration.

## Pass criteria and evidence

A pass requires a single uninterrupted fresh stream, no abort condition, no
uncommanded foot motion, clean neutral returns after every segment, and a single
expected POSE-to-PLANNER transition. Preserve synchronized operator/viewer video,
PICO pose recording, target motion, measured state/action logs, stream timing and
mode transitions. Report subjective smoothness separately from telemetry.

Simulation passing does not authorize hardware. For an initial physical gantry run,
perform segments 0--5 only. Add segments 6--8 in separate runs after reviewing the
prior telemetry and video.
