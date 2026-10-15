# Return-to-stock physical test protocol

Operator-defined protocol, 2026-10-16. Apply separately to every pose/scenario.
This document records procedure; it does not independently authorize motion.

1. Announce the upcoming move in English voice and text, identifying the scenario.
2. Move slowly to the recorded pose. Preserve measured feedback and command evidence.
3. After measured pose arrival, announce readiness for inspection in voice and text.
   Hold the pose and wait for explicit operator inspection confirmation. Elapsed
   time, telemetry arrival, or absence of objection is not confirmation.
4. Only after that confirmation, execute the existing return-to-stock routine.
   Record measured motion, arrival result, authority weights/fade, publication
   outcome, closure, and post-close feedback. Report timeout/fault as such.
5. Wait for the operator's explicit success/failure assessment. Record it separately
   from software completion. Do not start the next scenario before this assessment.

Voice failure must be reported explicitly; text remains visible. Do not claim a
spoken announcement succeeded merely because its request was submitted.

These are experiment orchestration steps, not extra gates inside exception recovery.
Preserve the operator's decision to use Unitree return gating without additional
motion trips. Failure during recovery is covered by independent physical measures
(gantry, clear workspace, operator emergency control); do not require recovery to
validate itself recursively. Do not invent another fallback trajectory.

Record exact code/configuration and SDK joint-coordinate targets, including the
random seed when used. SDK elbow degrees are not anatomical flexion or arm elevation.
Keep trials one at a time. A safe operator observation applies to that trial and
does not prove safety for all poses or failures.
