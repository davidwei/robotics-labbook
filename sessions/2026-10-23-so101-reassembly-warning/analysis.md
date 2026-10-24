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

## Follow-up: zero-velocity cases 6–9

Inspecting contiguous identical elbow encoder readings around each event gives
plateaus of 0.400/0.167/3.879/0.801 seconds for events 6/7/8/9 respectively.
Case 8 held the reported follower elbow at -38.286 degrees for 117 samples while
the requested leader target ranged from -48.923 to -47.956 degrees. This is
sustained residual tracking error, not only an artifact of the short velocity
window. Cases 6, 7 and 9 show resumed motion after their plateaus. Encoder
quantization still limits the meaning of exactly zero motion.

The monitor never pauses commands. The driver requests position goals with
P=16, I=0, D=32 in this candidate. Load/static-friction equilibrium under that
tuning is one hypothesis; command acceptance, torque/protection state and other
motor/controller limits are alternatives. The operator reports no obstruction.
No cause is established: actual motor Goal_Position, torque-enabled state, load,
current and temperature were not recorded. A software target is not proof of the
motor's stored goal or torque production. Proposed next diagnostic: short,
supervised stationary comparison of requested and motor-stored goal/position and
controller status before tuning gains, changing thresholds or inferring a stall.
No controller settings or hardware execution were changed for this analysis.

## Initial alignment check

The first instrumented loop sample, after connection and before the first loop
Goal_Position write, was not aligned. Absolute errors (degrees) were shoulder
pan 6.901, shoulder lift 9.670, elbow 4.220, wrist flex 1.890 and wrist roll 10.022.
Four of five monitored joints exceeded the 2-degree limit; the first warning was
therefore due immediately. Gripper alignment cannot be assessed from this trace.
At approximately 0.5 seconds the other four arm-joint errors were below 0.4
degrees, but the elbow error was still 3.604 degrees, also present at 1 second.
These are tracking-error observations; the trace does not establish why the
elbow retained that offset. Pickup alignment could gate initial engagement but
would not, by itself, resolve a motor's persistent position-tracking residual.

## Two physical alignment checks

Run 006 timed out after 30.046 s; the leader changed during this run, so fixed
snapshot tracking and current-leader matching are distinct. Run 007 ended by
operator input after 13.511 s, never reporting ALIGNED. In run 007 all six
leader readings remained unchanged. Its final elbow target and motor-stored
goal both read 93.407 degrees, but actual position was 96.835 degrees: 3.429
degrees of residual error. Wrist flex target was 74.022 degrees, stored goal
73.978 and actual 73.011: 1.011 degrees from the requested target, slightly over
the 1-degree gate. That borderline wrist result includes goal rounding; the
elbow error is much larger and not explained by encoder rounding. Other arm
joints met 1 degree; gripper met its 3-unit opening tolerance.

The preceding longer run ended at the same elbow and wrist residuals. The latest
elbow moved only one observed encoder increment (~0.088 degree). These checks
show the goal is reaching the motor register at this pose; they do not establish
why actual position remains offset. Standard configuration writes P=16/I=0/D=32.
Load/friction/tuning is a hypothesis, alongside torque/protection, limits/dead
zones or physical contact. Do not infer the obstruction-free context of the
earlier moving test applies to these later stationary runs without confirmation.
No current/load/torque/protection telemetry was captured, and no gains or
tolerances were changed. Proposed next step: a supervised stationary register
diagnostic before controller changes. Raising the tolerance would mask rather
than explain the elbow residual.

## Motor-state run 008 and competing hypotheses

Run 008 ended by operator input after 29.119 s, not aligned. There were 559
position samples and 173 staggered diagnostic updates, with no diagnostic read
errors. Elbow goal remained 93.407 degrees and actual 96.835 degrees (3.429
degrees error). Torque-enable stayed 1; sampled status stayed 0; velocity/moving
feedback stayed 0. Elbow current was nonzero after startup (typically 7–12 raw),
and load settled at 152 raw. P/I/D read back 16/0/32; dead zones 1/1. Configured
torque limit was 1000; temperature was 26–28 raw versus limit 80. No sampled
status flag establishes a fault, but staggered sampling cannot exclude transients.

The operator proposes that persistent error plus constant load identifies an
end-of-freedom condition. This is a candidate explanation, not a demonstrated
cause. Feetech describes load as the motor control-output duty-cycle scale
(1000 full scale), not a force/contact sensor. A constant output can balance
load/friction with I=0. Actual position 2871 is near calibrated maximum 2875,
but requested/stored goal 2832 is inside limits 664..2875 and away from that
upper endpoint. This supports inspecting binding/geometry but does not prove
a simple upper-stop explanation.

Another material observation is elbow voltage 50–51 raw. Feetech documents
0.1 V/count, giving about 5.0–5.1 V. Operator says the follower should be 12 V;
actual adapter/servo labels and the power path remain unconfirmed. SO101
voltage variants differ, so do not prescribe a new supply voltage before
confirming the exact build. No supply, gain or control changes were performed.

Open hypotheses, which may coexist:
1. Static gravity/friction equilibrium under current proportional drive/I=0.
2. Supply-path/voltage mismatch if this is indeed the 12 V build.
3. Mechanical binding/contact/end-of-travel interference after reassembly.
4. Controller/protection/firmware behavior, less directly supported by sampled
   torque/status/temperature but not excluded.

Prioritize adapter/servo-label and power-path confirmation plus physical clearance
inspection before supervised pose comparisons or tuning. Pickup mode can detect
sustained tracking failure without claiming its cause is a hard stop.

Primary sources: https://www.feetechrc.com/20210430-56680.html (feedback scales
and operating mode); https://github.com/huggingface/lerobot/blob/main/AGENT_GUIDE.md
(voltage variants). These are interpretation references, not measurements of
this physical unit. Raw evidence remains in motor-state-review.json references.

## Operator assessment and confirmed PD settings

Operator reports successful raising/lowering in more stretched poses and would
rule out insufficient voltage/internal protection as the explanation. Preserve
this as operator assessment: it supports deprioritizing complete drive failure,
while pose/load-dependent effects are not conclusively excluded by that report.

Latest follower elbow register readback is P=16, I=0, D=32, matching the driver's
configure() writes. The motor has PID parameters but this configuration enables
P and D with no integral contribution. For a stationary fixed target, the
derivative contribution tends to zero; a persistent proportional error can
therefore coexist with constant output balancing gravity/friction. This is a
plausible mechanism for the residual, not proof of its cause. No gains changed.
