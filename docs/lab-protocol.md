# Session-derived robotics lab protocol

Status: draft synthesis for researcher review, based on the 12 checked-in sessions at `0cb4f24`. It consolidates operating lessons; it is not a validated safety standard, authorization for motion, or a change to controller/skill rules. Use the exact robot-specific plan and current operator instructions for execution. Numerical values from past runs are observations or candidate-specific criteria, not universal limits.

The [complete session crosswalk](session-reference-audit.md) defines coverage, including the unresolved date discrepancy for records labeled November 3. This protocol introduces no controller implementation and does not revive the stopped October 16 handover series.

## 1. Before the lab: choose one question and freeze the candidate

- Sync the canonical labbook fast-forward-only after checking local changes. Read the project, idea, experiment and previous session's failures/next action.
- State the question, one bounded sequence, controlled variables, expected observation, success/failure criteria, abort conditions and minimum useful result. Distinguish readiness checks, diagnostics, runs and cleanup. A planned session is not an executed test.
- Do offline review, mocks and simulation first where informative. Test actual shutdown/exception paths as well as the nominal path. Preserve exact source revision, full dirty patch, dependency/platform information and config/model/engine hashes. Build/download engines and verify imports before the headset-dependent portion of the session.
- Use a matched baseline when attributing a regression. A simulation warning found on both feature and parent revisions predates the diff; it does not become a solved instability.

Sources: [Oct 8 baseline comparison](../sessions/2026-10-08-g1-29-mujoco-regression/session.md), [Oct 16 continuity audit](../sessions/2026-10-16-g1-handover/session.md), [Oct 29 plan](../sessions/2026-10-29-g1-sonic-planted-feet/pre-lab.md), [Oct 30 engine-order correction](../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md).

### Rehearse the operator workflow in simulation

The operator should design and try as much of the complete operational flow as possible in simulation before the lab. Rehearse how the person actually starts, calibrates, arms, changes modes, performs the bounded task, stops and recovers—not only whether the control algorithm runs. Use the real headset/controllers and intended prompts where possible; use input-only or mocked runs for steps that do not need robot dynamics. Resolve workflow friction before spending physical robot time.

- Design for the operator's actual constraints. With a VR headset on and controllers in hand, keyboard and terminal access are ineffective for routine operation. Provide audible status and next-action prompts, with headset/controller commands or suitable voice commands, so the operator can complete the sequence without repeatedly removing the headset. Verify that speech is audible and understandable; a successful TTS call alone is insufficient.
- Make controller and tracker calibration an explicit part of the operational flow and rehearse it with the actual input devices where possible: pairing/connection, reference or neutral pose, calibration actions, prompts, and verification that the reported pose and motion match the operator. Define when calibration must be repeated, including headset removal or tracking reset where applicable, and rehearse returning from recalibration to a verified ready state before arming.
- Walk through the full sequence with the operator: startup readiness, controller/tracker calibration and verification, explicit arming, mode transitions, task execution, stop, restart and cleanup. Include delayed initialization, missed or repeated button presses, tracking loss/reconnection and prompt failures. Confirm who acts at each step and how completion is acknowledged. Rehearse the safety operator's separate local-stop role as well.
- Record the rehearsed source/configuration, input devices, prompts, sequence and remaining lab-only checks. Carry the same flow into the physical plan; changes to controls, prompts or startup order should be rehearsed again where possible. Keep simulation/input-only results separate from physical stop, handover and hardware validation.

Operator guidance added during protocol review: operational rehearsal before the lab should improve the use of scarce in-lab time. Session evidence supporting this emphasis includes [October 30's headset/engine startup ordering](../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md), [November 3's voice-guided input-only rehearsal](../sessions/2026-11-03-g1-sonic-pico-voice-dryrun/session.md) and [the subsequent physical launch-order failure](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md). These records motivate rehearsal; they do not establish a measured efficiency improvement.

## 2. At the robot: re-establish identity and readiness

- Confirm actual robot/embodiment, host, firmware known/unknown, network interface and current controller/mode. Inspect existing processes and command publishers. Record uncertainty; a valid command stream does not identify its publisher.
- Re-identify leader/follower adapters and camera views physically. Preview each lens and verify role, orientation, exposure and actual capture node. Transport, reconnects and USB faults invalidate old numeric camera indices. A stable device path is useful only if the pinned launcher actually accepts it.
- After motor/horn/reassembly work, recalibrate as appropriate, archive/hash the files and compare them with motor registers. Saved identities/calibrations are starting points. Record torque/status/voltage/temperature readback and the mechanical assembly assumptions.
- For physical runs, confirm operator roles, workspace, support/gantry geometry, emergency control and a local stop path. Record which checks are operator-reported and which are instrumented. Define the exact motion scope before separate explicit authorization.

Sources: [Oct 9 DDS preflight](../sessions/2026-10-09-g1-29-regression/session.md), [Oct 23 reassembly](../sessions/2026-10-23-so101-reassembly-warning/session.md), [Oct 24 motor/calibration audit](../sessions/2026-10-24-so101-12v-follower/session.md), [Oct 25 camera identification](../sessions/2026-10-25-so101-teleop-preparation/session.md), [Oct 31 venue/USB re-enumeration](../sessions/2026-10-31-so101-linux-migration/session.md).

### In-lab dry run before physical execution

Before the physical experiment, conduct a dry run of the complete operational flow with physical movement disabled. Use the actual lab setup, operator roles, headset/controllers, calibration sequence, voice prompts and intended controls so the operator knows what to expect during the real run. Suppress robot actuation explicitly—for example, use an input-only/mock mode with no motor-command publisher or physical policy output. Do not rely on the operator staying still to prevent movement.

Rehearse readiness announcements, controller/tracker calibration and verification, arming, start, mode transitions, the bounded task sequence, stop and cleanup. Confirm that prompts are audible, actions and acknowledgments are clear, and the operator and safety operator know their next steps. Represent any step that cannot be exercised without movement with a clearly identified simulated acknowledgment; record what remains untested.

After the walkthrough, review surprises or unclear steps with the operator, correct the flow and repeat the affected portion as needed. Then explicitly distinguish the transition from dry-run mode to the separately authorized physical run, confirming the intended configuration and capture readiness. Completing the dry run establishes familiarity with the workflow; physical response, stop and handover still require their own evidence.

Basis: operator-requested addition to this protocol, informed by the [input-only PICO rehearsal](../sessions/2026-11-03-g1-sonic-pico-voice-dryrun/session.md) and [physical startup-ordering failure](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).

## 3. Prepare independent capture before control

- Allocate new non-overwriting run/artifact paths. Confirm storage headroom and that analyzers write to a distinct destination; retain raw inputs unchanged. October 31's analyzer overwrote its own telemetry because the input filename lacked the expected suffix.
- Start and verify independent capture before initialization/authority takeover. On G1 capture whole-body q/dq, base/torso IMU, LowCmd, mode/authority and relevant status; on SO-101 retain processed targets, measured state, warning/state transitions and available status/load/current. Record timestamps, time basis, sample counts, gaps, drops, CRC/finite checks and capture boundaries.
- For PICO/SONIC, retain continuous raw body/controller/button input plus exact outgoing packet bytes, timestamps, hashes and mode tags alongside SONIC CSV/console. Capture synchronized operator/robot video when needed to resolve physical posture and event timing. State explicitly when video is absent.
- Keep recording through stop, verified publisher closure and the planned post-stop observation window. Budget the recorder beyond the full experiment plus cleanup; monitor remaining duration and do not let a silent timeout remove stop coverage. The October 30 session requested at least 45 seconds post-stop; use the current run plan, not a universal duration.
- A close request or marker is not proof of closure. Verify actual process/publisher termination and continue independent feedback afterward. Preserve interrupted captures and gaps rather than calling them continuous.

Sources: [Oct 16 false closure marker and post-close observation](../sessions/2026-10-16-g1-handover/session.md), [Oct 30 missing input then packet capture](../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md), [Oct 31 overwritten telemetry](../sessions/2026-10-31-so101-linux-migration/session.md), [Nov 3 recorder expiry](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).

## 4. Run progressively and stay inside the agreed sequence

1. Read-only connectivity/state checks.
2. Camera/headset/input-only checks, without a policy subscriber or motor publisher where applicable.
3. Confirm pre-lab offline/mock/simulation results for the exact candidate, then conduct the in-lab operational dry run with physical movement disabled. Review the sequence with the operator before enabling physical execution.
4. Separately authorized, supported physical initialization/hold, then one small motion or mode transition with measurable criteria.
5. Stop, inspect results and obtain the required operator decision before expanding the sequence or repeating after a fault.

Change one factor when possible; record unavoidable differences. Preserve failed starts and protocol deviations. Do not substitute SIGINT/cleanup for an agreed inspection/handover step or silently expand a one-cycle experiment into multiple cycles. A fault, unexpected motion, tracking mismatch, capture failure or operator stop request ends the current experiment scope; further work needs a fresh decision under the applicable plan. Do not relax thresholds simply to obtain a pass.

When the recovery procedure itself is under test, use independent physical coverage rather than requiring that unvalidated recovery to serve as its own proven fallback. This does not authorize adding recovery gates: the October 16 operator specifically rejected additional non-Unitree return gates. Keep those controller-specific decisions in the original record.

Sources: [Oct 15 phase-specific failures](../sessions/2026-10-15-g1-vr-camera/session.md), [Oct 16 independent coverage and RUN-006 deviation](../sessions/2026-10-16-g1-handover/session.md), [Nov 3 repeated-cycle deviation](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).

## 5. SO-101 procedure: separate mechanical health, tracking and data collection

- After assembly/calibration changes, establish current mechanical freedom with support and torque off, then plan the appropriate short monitored powered check before tracking. Keep parked/folded rest geometry distinct from the conservative powered envelope. Crossing a deliberately conservative calibration boundary alone does not prove a hard stop.
- If an installed motor overloads, preserve target/state/load/current/status and stop under the agreed procedure. A cleared status after torque-off does not resolve the load condition. Use an explicitly authorized unloaded isolated comparison to distinguish motor function from linkage/loading. Do not raise torque automatically. In the recorded motor-3 test, hold at measured position -> torque enable -> target worked after target-before-enable produced no motion; preserve this as servo-path evidence, not an instruction to bypass limits.
- Distinguish leader request, processed/sent command and measured follower pose. Shaping/backlog, static PD residual, gravity coupling, obstruction and hardware fault can produce different errors. Raw load/PWM or nominal gravity models are not calibrated joint torque, and high error alone does not prove collision or saturation.
- Standard teleop begins following immediately in the recorded launcher: align poses and plan arm support at torque-off. Pickup state-machine hold/resume is a separate experiment; standard recording/replay success cannot close it.
- Rehearse record/save/discard/replay and actual keyboard/voice behavior before a demo. Confirm Accessibility/input permissions, exact task label, selected camera schema, FPS, episode cap and non-overwriting dataset destination. Voice requests are not proof of audible output or operator action.
- Replay sends stored processed action targets at dataset FPS, not the measured historical follower path. Start near the first action; the recorded replay had no initial ramp or path guarantee. Confirm a finalized episode and prepare reference views before motor connection.
- On camera dropout, stop and inspect USB/capture identity, preview both required views, update config and restart any launcher caching old indices. A brief recovered stream is evidence of recovery, not proof the cable/hub fault cannot recur.

Sources: [Oct 23 warning/static residual](../sessions/2026-10-23-so101-reassembly-warning/session.md), [Oct 24 isolated tests](../sessions/2026-10-24-so101-12v-follower/session.md), [Oct 25 action/replay semantics and permissions](../sessions/2026-10-25-so101-teleop-preparation/session.md), [Oct 31 migration, overload and camera faults](../sessions/2026-10-31-so101-linux-migration/session.md).

## 6. G1/PICO/SONIC procedure: verify the input, then the physical outcome

- Retain gantry protection and two operators for the recorded SONIC workflow. Fully suspended INIT, suspended policy operation and ground-contact/fall-catch operation are distinct conditions; changing contact/load requires a revised setup and authorization. Suspended stepping does not establish ground behavior.
- Recalibrate foot/ankle trackers whenever the headset is removed. Immediately before arming, compare the reported skeleton with the operator's real posture and inspect live motion/freshness. Connected status, advancing timestamps or finite arrays alone are insufficient: the recorded stream included anatomically bent, bit-identical poses with advancing timestamps.
- Headset removal, reconnection, stale/frozen/intermittent input or posture mismatch invalidates prior arming. Use the deployed candidate's input-only gate/rehearsal and full-release button semantics; do not copy thresholds or button maps into a different backend without checking it.
- Separate readiness gates: first pass an input-only rehearsal; for the authorized physical launch start/verify the recorder, wait for SONIC `Init Done`, then enable the XR/PICO manager/control sequence. Do not send policy-start events while TensorRT initializes. Keep local `O` and independent emergency control available under the run plan.
- Bound the requested mode sequence and motions. Treat unexpected lower-body movement or repeated mode toggles as an abort/deviation, preserving raw input, converted packets, commands and measured state for alignment. Similar input anomalies from a later capture suggest a hypothesis; they do not prove the cause of an earlier uncaptured incident.
- Do not use one successful sequence as evidence of stale-input safety, general reliability, or untethered readiness. Stale-input behavior remains unvalidated in the checked-in latest physical record.

Sources: [Oct 30 four runs and frozen tracking](../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md), [Nov 3 dry-run gate](../sessions/2026-11-03-g1-sonic-pico-voice-dryrun/session.md), [Nov 3 launch order and physical runs](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).

## 7. Verify stop, handover and final hardware state separately

- Distinguish stop request, manager OFF, control-loop stop, last command, publisher closure, stock-controller restoration and physical settling. RPC/DDS write success and exit code zero do not establish physical stop or restored authority.
- Maintain physical support through and after SONIC stop. October 30 captured no resumed stock commands and loss of standing. SONIC stop does not automatically restore stock control in this recorded configuration.
- If stock restoration is part of cleanup, use the documented candidate-specific procedure and verify service/FSM over timed readbacks plus independent telemetry. November 3's failed `normal` selection/damp requests were not restoration; later `ai`/FSM 1 success was rechecked after a readback fell to FSM 0. This is evidence for that setup, not a generic command recipe or undocumented FSM guarantee.
- For SO-101, verify current calibration/status/torque state after shutdown where possible. Record missing readback or unobserved power/support state explicitly. Process absence alone does not establish torque-off.
- Check test processes and relevant ports after capture finalizes. Record final robot posture/support, stock mode or torque state, operator confirmation, remaining anomalies and what was independently verified.

Sources: [Oct 9 passive disconnect without native restoration](../sessions/2026-10-09-g1-29-regression/session.md), [Oct 15 missing final posture confirmation](../sessions/2026-10-15-g1-vr-camera/session.md), [Oct 16 post-close dynamics](../sessions/2026-10-16-g1-handover/session.md), [Oct 30 loss of standing](../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md), [Nov 3 explicit stock cleanup](../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).

## 8. Close out, audit data and hand off

- Write a short session summary with objective, actual tests, failures, material revisions, evidence limits, final state and next action. Keep commands/chronology in the timeline and run provenance in run records; register artifacts/hashes and capture coverage/gaps.
- Separate operator report, instrumented observation, hypothesis and reviewed conclusion. Preserve corrections. Targets are not achieved rates; estimated catch-up is not measured recovery; a nominal model is not identified hardware dynamics.
- Before cleanup/training, preserve and back up raw data, verify manifests/hashes and report backup status honestly. Audit committed metadata, episode rows, video frames, timestamps, telemetry drops and task quality. Keep failed/uncommitted attempts distinguishable from committed episodes.
- Treat camera loss as a schema change: October 31's 50 two-camera and 76 one-camera episodes require an explicit missing-view strategy before combining for training. The count of 126 episodes does not establish 126 participants, successful pickups, integrity of every frame or a trained model.
- Update linked idea/project descriptions with the actual readiness, session references, unresolved question, target, prerequisites and next agent action. Check record syntax/diff, commit intended changes, push and verify synchronization.

Sources: [Oct 8/9 provenance limits](../sessions/2026-10-09-g1-29-regression/session.md), [Oct 25 rehearsal saving/finalization](../sessions/2026-10-25-so101-teleop-preparation/session.md), [Oct 31 closeout/inventory](../sessions/2026-10-31-so101-linux-migration/session.md). Record organization follows the [existing labbook skill](../skills/labbook/SKILL.md).

## Review items before treating this as an accepted protocol

Researcher review remains needed for each robot's current stop/emergency procedure, candidate-specific acceptance thresholds, support/contact configuration and evidence-capture duration. Outstanding research includes Arm SDK RUN-006 causality, SONIC stale-input behavior and repeated POSE transitions, SO-101 pickup/threshold/installed overload behavior, and dataset integrity/schema reconciliation. This draft does not mark any of those resolved.
