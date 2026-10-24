# Discussion closeout and return-to-lab handoff

## Observations and interpretation boundaries

LeRobot maps calibrated absolute leader joint positions into follower position goals. The servo closes its own position loop; no outer loop guarantees convergence. Startup following can begin from a mismatch. The added alignment helper freezes a leader snapshot, ramps a target and waits for a tolerance/dwell test; it does not implement automatic teleop handoff.

RUN-005 began with several mismatched joints. Nine announcements were warning requests, not nine independent physical stalls. Cases 6–9 had no measurable closing velocity over the short analysis window despite error; one elbow plateau lasted 3.879 seconds. A finite “distance/speed” prediction is unavailable for stationary or moving-away joints. Later motion resumed. The operator explicitly described that moving run as free motion without obstruction; this does not establish the cause of every subsequent fixed-pose residual.

RUN-008 elbow target/stored goal was 93.4066°, actual 96.8352°, error 3.4286°: raw goal 2832, actual 2871, calibrated upper bound 2875. The goal points inside the calibrated range. P=16, I=0, D=32 is effectively PD at the configured settings. Present_Load is a control-output indicator, not a calibrated contact-force sensor.

## Competing hypotheses

| Hypothesis | Evidence and limits | Next discriminating evidence |
|---|---|---|
| Gravity/static friction with finite P and zero I produces equilibrium error | Persistent error with enabled torque and steady output is compatible; cause not established | Compare settled errors in multiple clear poses, approach directions and loads before bounded per-joint tuning |
| Mechanical limit, binding, self-contact or tabletop contact after reassembly | Actual elbow near calibrated endpoint; constant load alone cannot prove contact and target is inside range | Inspect clearance and usable range with operator; compare clear poses without forcing a stop |
| Power path or supply mismatch | Voltage register approximately 50–51 raw (0.1 V/count); operator expects 12 V but label unverified | Confirm exact servo variant, adapter rating and actual voltage if discrepancy remains relevant |
| Internal protection or controller limiting | Sampled torque=1, status=0 and temperatures 26–28 weaken sustained protection explanation; staggered polls cannot exclude transients | Correlate diagnostics with a repeatable failing pose if needed |

Operator assessment: deprioritize power/protection because motors moved in more stretched poses. Working assumption for design discussion: gravity/PD residual plus occasional hard limits. This is not a validated root-cause conclusion. One-count dead zones do not directly explain the observed 39-count error.

## Proposed behavior and implementation status

1. **Threshold measurement:** telemetry and offline estimates implemented. Real-time warning currently uses angular error, not a validated catch-up-time prediction. Preserve unknown estimates instead of treating stationary joints as zero lag. Characterize static residual and dynamic lag separately; never hide a persistent elbow error merely by loosening thresholds. A global speech cooldown should be independent of hysteresis rearming: replay showed larger angular thresholds can produce more announcements.
2. **Reachable targets and tracking:** map into verified follower limits with margins and relevant workspace constraints; calibration extrema are not a complete collision-free workspace. Add explicit time-based velocity/acceleration shaping if needed; a relative-position cap alone is not a speed limit. Characterize before tuning P/D. Consider gravity compensation or bounded integral only with a supported actuator interface, anti-windup/reset behavior and separate validation. Do not apply a universal 3.43° offset.
3. **Pickup recovery — proposed, not implemented:** distinguish dynamic lag (“slow down”), configured limit, sustained nonprogress and communication/protection faults. Disengage leader command forwarding; define a validated hold policy that does not retain an unreachable target or drop an unsupported arm. Ask the operator to bring the leader near the measured follower pose; require relevant joints within tolerance for a dwell, then explicit resume with command continuity. Do not automatically force/reverse an obstacle. G1 reference: sessions/2026-10-15-g1-vr-camera showed virtual pickup transitions; physical hold/recovery was not validated there.
4. **Operator-controlled recording — planned:** continuous teleop with keyboard start/finish/discard; optional microphone and pre-start buffer later. Log raw leader intent, mapped desired target, sent command, measured follower and control mode. Define dataset action semantics and whether pickup intervals pause, mark or discard recording. Existing timed recording is not this proposed interaction; physical recording remains untested in this session.

## Next session order

- Review this handoff and exact calibration/config archive; reconnect and inspect hardware with the operator before any motion.
- Confirm clear workspace and characterize static tracking error across selected poses; inspect near-endpoint behavior. No gain or supply change is preapproved by this documentation.
- Revisit warning tolerance, velocity estimation window and nonprogress classification; repeat a threshold measurement only after defining what constitutes acceptable alignment.
- Specify and implement pickup state transitions/hold policy, then recording gates, with software checks before physical validation. Original priority remains threshold understanding before pickup.

## Preservation

All eight run records and detailed analysis remain in this session. Source checkpoint: MoissanClub/lerobot `102be54dfdba03ea11505ef345790d34ff370489`, branch `lab/so101-intel-warning-20261023`. Workbench helpers are under `workbench/so101_intel_mac`; retain the documented parent-workspace layout. No merge into the newer Python/torch-dependent `so101demo` branch was performed.

Manufacturer register reference: https://www.feetechrc.com/20210430-56680.html . Register interpretation does not identify the installed motor's exact voltage variant. Evidence archive SHA256: `430cccd8e0cee993e63d80e85b4aa0526e9dde96149006b6ff2e3c108000ab43`.
