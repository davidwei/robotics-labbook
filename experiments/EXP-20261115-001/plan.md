# Quest Pro to Linux MuJoCo: first controller-teleoperation test

**Experiment:** EXP-20261115-001 · **Status:** Proposed; no installation or tests have been executed.  
**Prepared:** 2026-11-15, America/Los_Angeles · **Execution date:** TBD  
**Owner:** David Wei · **Project:** [Unitree G1](../../projects/unitree-g1/README.md)  
**Mode:** development / simulation with a physical headset; no physical robot.

## Decision and minimum useful result

Determine whether the released XRoboToolkit-Quest application on David's **Meta Quest Pro**, using its two **Touch Pro controllers**, can send usable tracking/control data through XRoboToolkit PC Service on a Linux desktop and control an actual MuJoCo simulation.

The first target is the upstream **dual UR5e MuJoCo example**. This isolates headset, transport, SDK, calibration, and clutch behavior before introducing G1-specific integration. The upstream G1 Placo example is a visualization, and is not a substitute for this MuJoCo test. Passing this experiment does not establish G1, Revo2, whole-body, or physical-robot compatibility.

**Minimum useful result:** the app launches on Quest Pro; head and both controller poses change with deliberate movement; source timestamps advance; each grip changes from released to fully squeezed; one simulated arm follows only during its grip-enabled interval; the simulation process stops deliberately. A partial result at an earlier gate is useful and must be recorded as partial.

## Read before operating

Use the complete [numbered lab procedure](procedure.md) for commands, installation checks, terminal roles, evidence capture, troubleshooting, and shutdown. The [experiment definition](experiment.yaml) records scope, candidate versions, readiness, and next action.

The visible result for this first experiment is the **MuJoCo window on the Linux desktop**. Streaming simulated camera video back into the headset is a separate follow-up. A desktop observer should provide audible readiness and action prompts while the headset operator holds the controllers.

### Control card

| Control | Meaning in this exact test |
| --- | --- |
| Left side grip held above 0.9 | Enable relative control of the left simulated arm |
| Right side grip held above 0.9 | Enable relative control of the right simulated arm |
| Release side grip while Send remains on | Deliver released state and reset that arm's reference for the next clutch |
| Index trigger | Select headset UI; the selected demo has no configured gripper |
| A button | Toggles Send only when Switch w/ A Button is enabled; leave that option off for the baseline |
| B button | Does not start recording in this MuJoCo example |
| Thumbsticks | Keep centered during the baseline; investigate the reported world-frame rotation separately |
| Ctrl+C in foreground simulation terminal | End the simulation; verify actual process exit |
| Send Off / headset removal / network interruption | Stops or interrupts input delivery; does not prove the receiver has cleared cached control state |

## Lab sequence and checkpoints

All outcomes below are **pending**. Durations, small-motion bounds, and repeat counts are proposed experiment settings, not prior measurements or certified limits.

| Step | Activity | Operation | Required checkpoint / evidence |
| --- | --- | --- | --- |
| P0 | Preflight | Identify Linux host, headset, controllers, network, roles, and new evidence directory. | Confirm Ubuntu 24.04 x86_64 for the provided package; record actual OS/build/GPU/Python/IP and headset build. |
| P1 | Preparation | Download and hash the Quest APK and matching PC Service package. Create a fresh simulation-only Python environment and pin the sample source. | Asset SHA-256 matches; exact source revision and resolved dependency list captured. Avoid legacy setup scripts and latest unpinned Placo. |
| P2 | Preflight | Check imports, sample CLI help, bundled model loading, and the standalone desktop MuJoCo viewer without headset control. | Two UR5e arms render; dependency and graphics failures are isolated before networking. |
| P3 | Preflight | Install the released APK with ADB; verify package/version and launch on Quest Pro. | Intended device is authorized; install succeeds; v1.0.1 panel and controller UI work. |
| P4 | Preflight | Start one PC Service instance; connect the Quest app to the desktop's reachable LAN IPv4 address. | Service process exists; TCP 63901 and local SDK endpoint are available; correct PC IP and WORKING shown. |
| R1 | Run | Input-only observation capture. Head + Controller on; Hand/Body/Remote Vision off. Enable Send with no simulator running. | Deliberate head/controller motion changes finite poses; timestamps advance; left/right grip release and squeeze are distinct. Do not accept advancing timestamps alone. |
| P5 | Rehearsal | Observer and operator practice start, grip/clutch, release, stop, and re-entry callouts. | Prompts are audible; both know the next action; grips are released and the observer can reach the simulator terminal. |
| R2 | Run | Start dual UR5e MuJoCo at scale 0.5. Check neutral behavior, right arm, clutch/reposition, left arm, then a small bimanual sequence. | Same-side arm response and released-hand independence are visible; record unexpected jumps, coupling, direction errors, warnings, and stop behavior. |
| R3 | Run | Repeat one short left/right clutch sequence after a clean simulator restart. | Startup does not require accidental button state; fresh input and zero grips are rechecked before enabling. Do not call one successful sequence reliable. |
| D1 | Optional diagnostic | With the simulator stopped, turn Send off/on or restart the Quest app and observe input recovery. | Record stale/cache/reconnect behavior; no automatic-disarm claim. Stop and reverify fresh zero-grip input before a later simulator run. |
| C0 | Cleanup | Release grips while sending, stop the simulator, turn Send off, then close only processes started for the test. | Actual PID/port state checked, recording continued through cleanup, artifacts preserved and hashed. |
| C1 | Closeout | Create actual session/run records and update this experiment from captured evidence. | Separate observation, hypothesis, and conclusion; record missing telemetry/video and next action. |

## Bounded motion sequence

After startup settles and fresh released grips are verified:

1. Move each controller gently with both grips released; check that controller movement does not command arm tracking.
2. Hold only the right side grip fully. Translate about 5–10 cm along one axis at a time, then make a small rotation. Record the visible response; do not infer measured end-effector accuracy from video.
3. Release the right grip **while Send stays on**. Move the controller to a comfortable position. Regrip and check that a new relative reference avoids a large target jump.
4. Repeat on the left.
5. After each side passes, hold both grips for one short, slow bimanual sequence.
6. Release both grips; the observer ends the run with Ctrl+C and checks process exit.

Unexpected tracking mismatch, cross-arm response, large jumps, repeated IK errors, MuJoCo instability warnings, loss of capture, or an operator stop request ends the current run. Preserve the failed attempt. Troubleshoot one factor at a time without silently changing the baseline or expanding the motion sequence.

## Candidate and known boundaries

- Quest APK: **v1.0.1**, hash-verified release asset. Upstream developed the app on Quest 3; Quest Pro compatibility is the subject of this experiment.
- PC Service: **v1.0.0 Ubuntu 24.04 amd64** release artifact.
- Python sample: **79e5cb8a56e3455515ce1b476e993c764ec58739**.
- Proposed Python baseline: Python 3.12, **xrobotoolkit-sdk 1.1.0**, **MuJoCo 3.3.7**, **Placo 0.9.18**; save the full resolved package set before running.
- Use a new venv and the selected simulation import path. The sample's legacy setup scripts refer to a removed SDK installer and can replace an existing environment/dependency directory.
- Placo 0.9.18 retains the Pinocchio/MeshCat interfaces used by this sample. This is a source-reviewed candidate combination, not a previously executed validation.
- Controller poses are visual-world transforms; validity is not fully exposed in the payload. The known joystick rotation issue makes sticks-off and explicit recenter/recalibration checks important.
- The receiver can retain cached grip/pose state. A Send toggle, disconnect, or apparent frozen image is not a verified stop.
- The stock demo has no built-in recording path for B and no automatically returned headset video. The procedure captures SDK snapshots, terminal output, and desktop video/observations; it does not establish numerical tracking accuracy, transport packet loss, or end-to-end latency.

## Result sheet — fill only after execution

| Item | Observed result / evidence reference |
| --- | --- |
| Actual date/time/timezone; operator; observer | Pending |
| Host OS/architecture/GPU/driver/Python; headset/controller build | Pending |
| Package/source/model hashes; dependency lock; dirty source state | Pending |
| P0–P4 preflight outcomes and failed starts | Pending |
| R1 timestamps, pose changes, per-side grips, invalid/frozen samples | Pending |
| R2 right/left/bimanual response; clutch/regrip behavior | Pending |
| R3 restart/repeat result | Pending / not attempted |
| D1 input-only reconnect result | Pending / not attempted |
| Simulation stop message, exit status, and process verification | Pending |
| Desktop video and terminal logs; SDK snapshot path | Pending |
| Known evidence gaps, including live simulator state telemetry | Pending |
| Overall outcome: success / partial / failure / blocked | Pending |
| Proposed finding and next action; review status | Pending |

## Record placement and next action

At execution, create a session using the **actual execution date** and the next unused IDs in the canonical notebook. Use `session.md` for a short human summary, `session.yaml` for identity/provenance, a timeline for exact commands and failed starts, and simulation run records for R1/R2/R3 only when they produce meaningful evidence. Keep large captures outside Git and register durable paths/hashes. Do not precreate completed sessions from this plan.

The existing CloudXR bookmark experiment remains a separate planned task. The G1/SONIC physical and handover questions remain separate unresolved work; this simulation does not close them.

**Next agent action:** prepare the isolated Linux environment and pass the offline dependency/model/viewer gates, then conduct R1 with the actual Quest Pro. If the main path blocks, retain the highest completed gate and its evidence. Any G1 adapter or headset video-return work should become a subsequent bounded experiment.

## Provenance and sources

Plan follows the refreshed [Lab Book skill](../../skills/labbook/SKILL.md), [development workflow](../../skills/labbook/workflows/development.md), and the operational-rehearsal/evidence/stop principles in the [draft lab protocol](../../docs/lab-protocol.md), reviewed at labbook revision `0d10331006ba6b453aa1d81e52542511f626646d`. The draft protocol is not promoted to a validated safety standard by this plan.

Primary upstream links and exact artifact hashes are in [procedure.md](procedure.md). Source/release and operational review was performed; the procedure's 18 Bash blocks and 3 embedded Python snippets passed syntax checks, and the experiment YAML parsed. No procedure commands were executed. Installation, simulator execution, Quest Pro compatibility, and timing remain untested.
