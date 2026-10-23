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

## Instrumented run 005: threshold measurement

Operator reports free motion without obstruction. Capture completed with 1,347
samples, zero dropped records and nine matched warnings over approximately 45 s.
The warning state remained active throughout; these were repeated notifications,
not nine independent lag episodes. Shoulder lift and elbow dominated the errors.

Only event 2 has a finite full-arm constant-speed projection (11.475 s). That
shoulder estimate changes to 40.035/80.127 s with 250/500 ms velocity windows,
and the full-arm estimates at those windows become unavailable due to other
non-closing joints. The finite number is not a reliable measured recovery time.
Eight events have no finite arm projection because of startup warmup or a joint
with zero/wrong-direction short-window velocity outside tolerance. This does not
establish a stall or obstruction; operator reports no obstruction.

Offline replay on the same trace: 2/5/10/15/20-degree limits produce 9/13/19/12/7
requests. Recovery resets the warning interval, so raising the threshold alone
can increase announcements. This replay does not predict how operator movement
would change with different live prompts. No threshold or cooldown was changed.

Proposed next step: establish stationary-pose residuals and agree on warning
tolerances/debounce/global audio cooldown before selecting a reusable threshold.
Pickup mode remains separate and deferred. Detailed review is referenced by
evidence.json; per-event joint-only projections must not be confused with arm ETA.
