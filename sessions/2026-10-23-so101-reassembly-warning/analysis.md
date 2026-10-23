# Warning count and catch-up-time analysis — 2026-10-23

Scope: review of existing logs only; no new hardware execution or control changes.

## Direct observations

- `teleop-text_20261023_134625_76973.log`: **7** logged notifications; speech disabled, threshold 2 degrees.
- `teleop-voice_20261023_135024_77207.log`: **1** logged notifications; speech enabled, threshold 2 degrees.
- `teleop-voice_20261023_135228_77311.log`: **10** logged notifications; speech enabled, threshold 2 degrees.

Total: **18** notifications in three completed tests; the latest 45-second run has **10**. The operator reports the warning works. Two aborted attempts are excluded. Full per-event timestamps and source revisions are in the local analysis artifacts referenced by evidence.json.

## Limits and interpretation

Catch-up time cannot be reconstructed for any event: these runs stored neither joint targets/positions nor velocities. No motor-speed information can be recovered from control-loop duration. Each recorded timestamp is a background-worker log time rounded to seconds, not an exact measurement or threshold-crossing timestamp.

Counts are announcements, not unique lag episodes. Persistent error can repeat at five-second intervals; recovery below 80% resets/rearms the monitor and permits a new warning sooner. The existing data cannot identify each lag onset, recovery, limiting joint, or maximum error.

These 2-degree tests do not establish a one-second catch-up threshold. The default 10-degree threshold remains physically untested. Audible operation is operator-confirmed, not a validation of predictive accuracy or tracking smoothness.

## Proposed next measurement

Record all five arm-joint follower positions and requested leader targets with monotonic sample timestamps every tick. Estimate signed follower velocity using a documented short window; retain raw samples. At a warning, conceptually freeze the leader target. For each joint outside tolerance, project time as `(abs(error)-tolerance)/(sign(error)*follower_velocity)` only when closing speed is positive. Mark stationary/moving-away/stale cases non-converging or unavailable. Arm time is the maximum joint projection; the largest positional error need not be the slowest joint.

This is a constant-speed counterfactual projection, not actual time measured after the leader stopped. Acceleration, deceleration, loads, motor saturation and measurement timing remain limitations. Validate predictions with controlled leader-stop trials before choosing a time-based warning threshold. No such telemetry or additional physical trial was implemented/executed for this analysis.

Review status: proposed analysis for operator review; no reusable performance or safety claim.
