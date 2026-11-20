# G1-29 XRoboToolkit script 05 physical preflight

**Session:** SESSION-20261121-001 · **Related experiment:** EXP-20261115-001 · **Status:** physical motion blocked at reviewed-contract and starting-state gates

## Objective and result

Prepare the robot-side host for the first `05a` static-posture validation from the published 2026-11-20 handoff. The handoff hashes passed and a passive Arm SDK read-only diagnostic received fresh G1-29 feedback without creating a command publisher. No physical motion was commanded.

The planned `calibration-down-inward` posture is not currently within the executor's example `0.05 rad` displacement envelope. The maximum measured-to-plan difference was `0.365003 rad` at `kLeftWristPitch.q`; several other joints also exceeded the envelope. Waist yaw was approximately `0.424 rad`, while the enabled reduced-model gravity path requires all three waist joints within `0.05 rad`. The executor would therefore reject activation even if a contract were approved.

## Readiness and next action

The exact published sources were checked out cleanly at integration `f7d951ede82ddb7a5b2ed0ed835a11b8c25bee79`, calibration plugin `e29a85b543bf4495223d403317afa7fd557a66a6`, and Arm SDK `39e02d7d2f2bc06353683a612ccca5b82733ea40`. The handoff posture, trajectory, and URDF hashes all matched `SHA256SUMS`.

Physical motion remains blocked because no site-reviewed arm-only hardware contract was found. The generated template remains explicitly unreviewed, with all approval fields false and `physical_stop_verified` false. Before rerunning `05a`, the operator must use the stock controller to place the waist near neutral and bring the arms near the reviewed down/inward plan, then repeat passive feedback. Separately review the robot identity/firmware, lower-body owner, exclusive publisher, waist semantics, independent stop/support procedure, packet-loss/process-death behavior, release behavior, payload, gains, limits, gravity model, expected mode byte, and exact plan digest. Do not expand the displacement envelope merely to bypass the starting-state gate.

`05b` remains downstream of a reviewed and observed `05a` result.

## Guarded replay control update

Integration revision `cd8d7cdf52a1c448b8f38e1ad2913c16760f342a` adds three operator controls to both physical replay executors. English speech now explicitly selects `spd-say -l en`, gives a blocking pre-motion warning and repeats from a background worker during authority/motion so TTS cannot block the 20 ms command loop. An interactive terminal is mandatory: `Q` latches a pause, freezes plan time and commands a hold near the latest measured pose; `R` explicitly resumes. `Ctrl+C` retains the existing request to release through three weight-zero packets. The `Q` path keeps arm torque active and is not an independent or verified emergency stop.

The first-target approach now defaults to seven seconds, separate from the reviewed Arm SDK velocity ceiling. With the current `0.05 rad` displacement envelope, a seven-second cubic approach peaks near `0.011 rad/s`; `0.1 rad/s` remains a ceiling for faults or larger future reviewed plans. The two-second authority blend and one-second final hold are additional. Safety-derived velocity/acceleration minima can only lengthen the requested approach.

Software validation passed 23 focused tests, Ruff, shell syntax and diff checks. No physical motion, audible-in-lab acceptance, keyboard pause under real authority, hold behavior, release behavior or tracking response was validated by this development update. The starting-state and contract blockers above remain unchanged.

## Passive recheck after operator preparation

A second passive diagnostic retained 176 samples with mode `(5, 0)`, weight `0.0`, maximum state age `0.008863 s` and no structured errors. Waist yaw improved to `0.0102 rad` and waist roll was `0.0344 rad`, but waist pitch was `-0.0526 rad`, just outside the `0.05 rad` reduced-gravity-model gate. The maximum arm difference from `calibration-down-inward` remained `0.3634 rad`, now at the left elbow, versus the unchanged `0.05 rad` reviewed displacement envelope. No command publisher or physical motion was used. `05a` remains blocked; do not widen the envelope merely to bypass the starting-state check.

## Separately reviewed initial-positioning implementation

Integration revision `bfbf9c7cb0a49ebdfd9e761cc7ef43ec0298adae` adds `05a --stage-from-current` as a single continuous arm-only phase from the live measured pose to the selected static posture. It defaults to a 10-second cubic approach and is lengthened when the reviewed velocity or acceleration ceiling requires more time. For the latest `0.3634 rad` gap, the nominal peak command speed would be about `0.0545 rad/s`, below the existing `0.1 rad/s` ceiling. The existing English alarms, `Q` hold, `R` resume, torque/tracking checks and release request remain active.

The feature does not control the waist, legs or hands and does not authorize a larger envelope. It requires a named, label-specific `physical_replay_staging` review with a maximum live start delta, minimum duration and explicit path/clearance review. The Arm SDK `max_displacement` must independently cover the full path; the executor rejects either mismatch. This avoids treating repeated small activations as a way around the total-displacement gate. Software validation passed 25 focused tests, Ruff, shell syntax, CLI-help and diff checks. No physical staging, clearance, pause, tracking or release behavior was tested.

## Stock-balance correction

The operator clarified that the stock controller owns the waist and legs and moves them as needed for self-balancing; the waist cannot and should not be forced neutral for this test. The earlier neutral-waist next action is superseded. The current reduced arm gravity feedforward is fixed-waist and not dynamically compatible with that operating mode.

Integration revision `65ebefbb1e573f30960a4f54133d6d802e32fbc3` therefore makes `lower_body_mode: stock_balance` explicit and rejects `05a` staging unless the reviewed Arm SDK profile uses `gravity_urdf: null` and the reviewer accepts no arm gravity feedforward. Stock lower-body commands remain untouched. The first physical gate becomes a supported no-displacement arm-authority hold with tracking, torque, lower-body behavior and release review; staging follows only if that passes. Twenty-six focused tests, Ruff, shell syntax and diff checks passed. This is software validation only.

## Upstream `xr_teleoperate` coordinate-frame comparison

Upstream `unitreerobotics/xr_teleoperate` revision `7e5026e4732cf166bcd1210d7958a75575d5fc95`, with `televuer` submodule `766de45e74373ae0ea66321d942ce538385655a5`, defaults to `arm_reference_mode="head_yaw"`. Each XR wrist translation subtracts the live operator-head translation and is rotated by inverse operator-head yaw; head pitch and roll are ignored. A fixed `+0.15 m` forward and `+0.45 m` vertical offset then maps the result to a nominal waist-origin frame for IK.

This is not an absolute XR-world target, but it is also not measured robot-head/waist-relative control. The G1-29 IK model locks hips, legs and all three waist joints at zero and does not consume the physical robot's live waist transform. Stock-balance waist motion therefore changes the physical hand pose relative to the world/head without being compensated by that IK. The method is best described as **operator-head-yaw-relative input mapped into a nominal fixed robot-waist frame**.

Current `05a` differs: it executes stored local arm joint angles, not a Cartesian world target. Stock waist motion carries the arms and hands with the torso; `05a` does not chase a world point or counteract balance. This is appropriate for the initial static staging/validation goal. Future live XR control under stock balance should preserve operator-head-relative input but solve arms against the measured robot torso/waist transform, rather than reuse a fixed-waist IK assumption.

## First-actuation request and passive gate

The operator reported the robot on the gantry, the environment clear and the emergency control clear, and requested the first physical move. The selected first actuation remains the no-displacement arm-authority hold rather than the larger `05a` staging path. No actuation occurred because no reviewed hardware contract exists.

A third passive diagnostic retained 174 samples with mode `(5, 0)`, arm weight `0.0`, maximum state age `0.006711 s`, maximum observed arm velocity `0.01228 rad/s` and no structured errors. Waist motion continued under stock balance. The English `spd-say -l en` preflight command completed. No competing LeRobot/G1 arm process was found, and the execution and Arm SDK checkouts matched their published revisions. The sole local contract remains explicitly unreviewed, lacks robot identity/firmware and procedure approvals, and still names the prohibited fixed-waist gravity model. Physical stop behavior remains unverified by execution evidence.

## Operator-reported model identity

The operator reported that the physical robot is the same Unitree G1 EDU 29-DoF body configuration represented by the transferred `g1_29.urdf` simulation model (`SHA256 8bbf006633fc50b616f665c7a970780cc296577a0adfd7d28b049e751c238735`). The operator supplied robot SN `E21D6000Q1M76781`, Unitree software `v1.5.4`, and hardware `v1.0`. Stock balance is owned by robot PC1 at `192.168.123.161`; the present host is PC2 `unitree-g1-nx`.

The physical end effectors are asymmetric: a BrainCo Revo2 hand is installed on the right and a dummy hand on the left. The transferred URDF contains bilateral articulated hand links and inertial data and does not explicitly identify a BrainCo/dummy composition. The body kinematics can therefore match while the end-effector mass/inertia model remains unverified. This does not change `05a` joint targets, but it is relevant to gains, torque limits, tracking, and any future gravity compensation.

A subscriber-only PC1 check received fresh `rt/lowstate` with version words `[0, 0]`, mode `(5, 0)`, and advancing ticks. A read-only RPC query reported live loco server API `1.0.0.0`; the arm-action service did not answer its version query. PC2 reports `/etc/user_release_version` `0.0`, Ubuntu `22.04.5`, and BrainCo service SDK `v1.1.9`. These interface/host values were not substituted for the operator-reported Unitree software version. The stock-lower-body-owner confirmation was recorded; the overall contract and all other approval gates remain unchanged, and no motion was authorized.

## First no-displacement authority hold

Reviewer `dwei` explicitly approved one supported no-displacement authority hold, accepted the documented process-death, payload-model and software-torque limitations, and confirmed presence at the physical emergency control. Arm SDK revision `90bdd40b4c4b3a66d75f499118ca8afe9fcd3e9b` preserved unverified waist and failure behavior as hold-test limitations rather than promoting them to verified findings. Thirty-seven focused tests passed, four optional physics tests were skipped, and Ruff passed. The exact approved contract is preserved with SHA256 `ce6540c8fb99a6fd3e3a68e1cddb591227641f99062f9c6f233c8a69d6c74712`.

The final passive gate retained 178 samples, mode `(5, 0)`, maximum state age `0.005679 s`, and maximum observed arm velocity `0.03682 rad/s`. No competing arm process or held local lease was found. English speech warned before authority and again while the hold was active.

The hold acquired arm authority and continuously requested the measured arm pose with gravity feedforward disabled. It faulted after 27 reported samples with `Measured displacement limit exceeded` while the reported authority weight had reached at most `0.18`. The report loop's retained samples show only `0.000084 rad` maximum start-relative arm change, so the state that crossed the `0.05 rad` envelope was not captured in those samples. Three weight-zero release packets were reported sent. This establishes neither a physical stop nor successful handover.

A subsequent passive run retained 172 samples in mode `(5, 0)`, with maximum state age `0.009224 s` and maximum observed arm velocity `0.04295 rad/s`. The final arm pose was within `0.01812 rad` of the final pre-hold sample, limited by the left elbow; stock waist motion continued. This is evidence of live feedback after cleanup, not proof of the transient cause or physical release semantics. The one-run approval was consumed and suspended. Do not retry the hold or execute `05a` until the transient is diagnosed and a new review is completed.

The operator subsequently reported **nothing visibly moved or changed** during the hold. A 20-second subscriber-only monitor then retained 862 samples in mode `(5, 0)` and found only `0.000240 rad` maximum arm-position span and `0.000120 rad` maximum consecutive-sample jump. No persistent or repeated feedback spike was observed. Offline evaluation of the transferred model predicted maximum gravity torque near `1.87 Nm` at the right shoulder roll; the transition from stock support to a no-feedforward arm controller is a plausible contributor, particularly with the asymmetric physical end effectors, but is not a validated cause. See `analysis.md`; authorization remains suspended.

Arm SDK revision `c130b0b145fa1c3dff429a0075016cb8445fd709` adds a 64-state bounded history and structured displacement-fault evidence: joint name, measured/initial/previous-command positions, delta and limit, velocity, torque estimate, tick, mode, authority weight and state age. The physical diagnostic report now preserves that context. Thirty-seven focused tests passed, four optional physics tests were skipped, and Ruff passed. No physical command was sent for this development update.

The operator requested to self-run physical `05a`. That request was not enabled because the prerequisite hold faulted at authority weight `0.18`, while the planned posture remains approximately `0.36 rad` from the measured start. The suspended contract continues to fail closed. Only read-only/offline validation is appropriate until the authority transition is diagnosed and a new explicit review is completed.

## Evidence limits

The passive report contained 175 samples, advancing ticks `751647` through `755093`, maximum reported state age `0.006525 s`, mode `(5, 0)`, weight `0.0`, and no structured report errors. Two console-level `Reader take sample error` messages occurred around the run boundary; continuous samples were still retained. Mode bytes and a passing software report do not establish hardware acceptance, safe handover, or physical stop behavior.
