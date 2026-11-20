# Initial authority-hold fault analysis

## Reviewed observations

- The operator reported **no visible movement or disturbance** during the failed hold.
- The hold faulted with `Measured displacement limit exceeded` after 27 report-loop samples and at reported authority weight no greater than `0.18`.
- Retained hold samples show only `0.000084 rad` maximum start-relative arm motion; the state that crossed the `0.05 rad` guard was not retained by the slower report loop.
- Three weight-zero packets were reported sent, but physical handover was not independently established.
- A post-fault passive run showed live mode `(5, 0)` and a final pose within `0.01812 rad` of the pre-hold pose.
- A subsequent 20-second passive monitor retained 862 samples with only `0.000240 rad` total arm-position span and `0.000120 rad` maximum consecutive-sample jump. It found no persistent or repeated feedback spike.

## Candidate explanations

1. **The custom gradual startup blend is a material deviation from upstream and must be investigated first.** Review of official `xr_teleoperate` revision `7e5026e4732cf166bcd1210d7958a75575d5fc95` corrected the earlier interpretation of startup takeover. The stock controller and `rt/arm_sdk` command are mixed by slot-29 weight, but the current G1-29 implementation sets startup weight directly to `1.0`; it bounds the commanded arm position with `clip_arm_q_target` on every 4 ms cycle. The gradual `0 -> 1` blend used by the failed hold is therefore not an upstream-style acquisition sequence. Upstream uses the gradual `1 -> 0` fade after returning the arms to its home pose. This does not prove that the custom blend caused the fault, but the failed run cannot be treated as a validation of Unitree's takeover method.
2. **Controller gains and feedforward also differ materially from upstream.** The failed hold used uniform `Kp=60`, `Kd=1.5` and zero feedforward. Upstream G1-29 uses `Kp/Kd=80/3` for shoulder/elbow joints and `40/1.5` for wrists, and its teleoperation loop passes IK-derived feedforward torque. The transferred URDF predicts a maximum arm gravity torque of approximately `1.87 Nm` at the post-run pose, while the actual asymmetric BrainCo/dummy payload inertia is unverified. These differences make the earlier gravity/support explanation plausible but underdetermined; it must not be presented as the leading established mechanism.
3. **A brief feedback outlier remains possible.** The guard evaluates every control-thread state while the report loop samples separately, so a one-sample excursion can fault without appearing in retained report rows. The 20-second passive monitor found no such outlier, reducing but not eliminating this explanation.
4. **A small physical transient below easy visual detection remains possible.** The operator's observation rules out obvious motion, not a brief joint change near the `0.05 rad` threshold.
5. **A stale activation baseline is less supported by code inspection.** Activation resets `initial`, `target`, and `previous` from a fresh state after the publisher becomes ready.

## Prior related physical evidence

The operator's recollection is supported by [RUN-20261015-009](../2026-10-15-g1-vr-camera/runs/RUN-20261015-009.yaml). That preparation run also used no gravity feedforward, enabled arm publication, stopped after approximately seven seconds on a small joint-error guard (`0.0311 rad` right-elbow error versus a `0.03 rad` limit), did not preserve the exact watchdog sample, and ended with the operator reporting the robot stationary. It differs from the present run because it commanded preparation motion toward zero angles and faulted on target-versus-measured tracking error; the present run commanded a measured-pose hold and faulted on start-relative displacement during authority blending.

The following October 15 run, `RUN-20261015-010`, enabled gravity feedforward and increased the preparation-only tracking allowance to `0.08 rad`. It reached the zero-angle target slowly, then stopped on separate arrival/velocity criteria. Because feedforward and tolerances changed together, it does not isolate gravity compensation as the causal difference. It nevertheless increases the value of explicitly testing the authority/feedforward transition in simulation.

The October 16 series provides additional handover context, not a direct recurrence. `RUN-20261016-005` completed a supervised fade from a selected pose but recorded a `3.09 rad/s` right-wrist-yaw peak after closure. `RUN-20261016-006` produced growing arm oscillations and forward motion during a full-authority return publication and required operator emergency-stop intervention. Those events involved return/handover trajectories rather than initial measured-pose acquisition. They show that authority transitions have repeatedly been the dominant unresolved physical risk and argue against bypassing today's failed hold to run `05a`.

## Next high-information work

- Use the newly added bounded state history and structured fault snapshot on any future reviewed diagnostic; its software path has passed focused fake-transport tests but has not captured a physical fault.
- Reproduce and instrument the exact upstream takeover semantics offline: `rt/arm_sdk`, current-state-bounded target, immediate startup weight `1.0`, upstream joint-group gains, and explicit feedforward choice. Compare it with the custom gradual blend before proposing another physical contract.
- Review an arm-gravity strategy that uses live torso orientation and the actual asymmetric end-effector inertias. Do not simply restore the fixed-waist feedforward model or widen the displacement envelope.
- Require a new explicit operator review before any repeat hold. `05a` remains blocked.

## 05a-to-05b readiness audit

The current executor still assumes the custom two-second startup weight blend and releases with three immediate weight-zero packets. Before another physical run, replace and test those semantics: measured-pose target continuity with full startup arm weight, then a controlled move to a stock-compatible arm pose followed by a `1 -> 0` release fade. A newly reviewed no-displacement acquisition-and-release run remains the first physical gate.

The existing `05a` posture artifact remains suitable only as a reviewed static target. The `calibration-down-inward` target is approximately `0.36 rad` from the latest measured pose, so its complete path, gains, payload assumptions, torque limits and approximately 10-second staging duration require explicit review after the takeover implementation changes.

The existing `05b` artifact is not eligible for physical replay. Across its six approximately 10-second segments, timestamp-derived peak joint velocity is `5.41–11.35 rad/s` and peak acceleration is `357–717 rad/s^2`, versus the current reviewed ceilings of `0.1 rad/s` and `0.5 rad/s^2`. Meeting the velocity ceiling by global stretching would require roughly `54–114x`, which is not a useful repair. The trajectories require continuity-preserving IK/replanning, velocity/acceleration validation, start-pose matching, and static validation of the selected segment's start pose before one single-arm dynamic run.

## Preserved implementation result

Published Arm SDK revision `87e29c26` implements the corrected upstream-style acquisition direction and controlled release. Near-limit feedback violations now require three fresh samples for the same joint; repeated reads of one tick and alternating one-sample excursions on different joints cannot combine into a trip. Excursions at twice the limit still trip immediately. This directly addresses the plausible one-sample false-guard mechanism while retaining a bounded hard-fault path; it does not prove the earlier physical event was an outlier.

The exact G1-29 model produced a successful full-weight simulated hold with live pelvis/waist gravity and a normal release, but a larger subprocess physics suite retained timing/resource intermittency. Therefore the implementation is preserved for continued validation, not promoted to physical readiness. Published integration revision `0eb6d34` exposes the next test as `--authority-only`; it must remain behind a fresh contract and offline validation gate.
