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

## Evidence limits

The passive report contained 175 samples, advancing ticks `751647` through `755093`, maximum reported state age `0.006525 s`, mode `(5, 0)`, weight `0.0`, and no structured report errors. Two console-level `Reader take sample error` messages occurred around the run boundary; continuous samples were still retained. Mode bytes and a passing software report do not establish hardware acceptance, safe handover, or physical stop behavior.
