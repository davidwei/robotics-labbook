# G1 stock-controller handover validation plan — 2026-10-15

Planned for the day after the 2026-10-14 review in America/Los_Angeles. Record the
actual local and robot-site timestamps when execution begins. This plan does not
authorize robot motion.

## Question and candidate

Does revision `a65596cb` return the G1-29 arms toward zero under measured feedback
and fade Arm SDK authority without the abrupt stock-controller trajectory observed
with the previous direct release?

- Repository: `MoissanClub/lerobot`
- Branch: `work/g1-vr-physical`
- Candidate revision: `a65596cb`
- Initial profile: guarded arm controller, no headset, no camera, gantry attached
- Initial override: `robot.arm_sdk.return_velocity=0.05` rad/s. Do not begin with
  the 0.5 rad/s default; increase only after reviewing a clean slow return.
- Physical status: unvalidated

## Prerequisites and evidence readiness

1. Confirm the checkout is clean at the recorded revision. Record the full command,
   configuration, host, SDK version, network interface, robot mode and start pose.
2. Confirm gantry support, clear arm workspace, regular action mode, independent
   emergency control and an operator positioned to stop motion. Verify no competing
   Arm SDK publisher or stale process.
3. Run read-only feedback first. Require fresh monotonic ticks, mode `(5, 0)`, finite
   arm position/velocity and a stationary or explained baseline.
4. Before motion, verify non-actuating capture of monotonic timestamp, handover phase,
   measured `q/dq`, commanded `q`, and Arm SDK weight through return, fade and at least
   five seconds after publisher closure. If revision `a65596cb` cannot expose this,
   add logging-only instrumentation, review it, and record the new exact revision.
5. Start an independent read-only low-state observer before the control process so
   stock-controller motion remains observable after the Arm SDK publisher closes.
6. Use new, non-overwriting artifact paths. Preserve terminal logs, structured
   telemetry, video of both arms, exact revision/configuration and operator notes.

The unsafe earlier direct-release revision is not a physical rollback candidate.
If this candidate cannot be validated, stop the test and return control using the
ordinary operator/robot procedure rather than rerunning the old cleanup path.

## Staged execution

### Gate 1 — no-motion lifecycle and preflight

- Exercise configuration parsing, connect/read-only/close, duplicate close and
  process cleanup without enabling the writer.
- Confirm the architectural pre-commit check passes at the exact candidate.
- Success: no publisher is created, feedback remains fresh and all processes close.
- Failure: unexpected writer, mode mismatch, stale/invalid state or residual process.

### Gate 2 — minimum useful physical experiment: normal near-zero handover

- Obtain explicit authorization for motion.
- Begin at or very near zero pose. Take authority and command only a small reviewed
  offset that remains inside all existing workspace, displacement and torque limits.
- Request normal close once measured motion has settled.
- Success requires all of the following evidence:
  - return commands progress toward zero without a command discontinuity and respect
    the 0.05 rad/s initial return setting;
  - measured absolute joint error is below the configured 0.05 rad tolerance before
    weight reduction begins;
  - weight is non-increasing through the approximately two-second fade and reaches zero;
  - no unexpected direction reversal, oscillation, collision risk or operator-visible
    jump occurs during return or stock takeover;
  - the independent observer captures at least five seconds after handover and the
    operator confirms the resulting posture is acceptable.
- Stop immediately on unexpected motion, rising error, stale feedback, mode change,
  excessive measured speed, write failure or any need for operator intervention.

Gate 2 is the minimum useful experiment. If it cannot pass, do not proceed to fault
injection or VR/E2E work.

### Gate 3 — repeatability and larger-but-bounded offset

- Repeat Gate 2 at least three times from the same small offset.
- Only after reviewing all traces, repeat from one larger reviewed offset still within
  the existing guarded envelope. Do not increase return velocity in the same run that
  changes displacement.
- Compare return duration, peak measured speed, maximum tracking error, arrival
  residual, fade duration and post-handover displacement across runs.
- Treat repeatability as condition-specific evidence, not a general safety proof.

### Gate 4 — fresh-feedback caller-timeout path

- Keep the robot near zero and the gantry attached. With feedback and DDS publication
  healthy, deliberately stop caller updates long enough to trigger the existing
  command-fault timeout.
- Success: the same central return sequence runs once, measured arrival precedes the
  fade, the original timeout remains recorded, and shutdown completes without a
  second direct-release path.
- Do not combine this gate with headset loss, camera load or network disruption.

### Gate 5 — separately authorized degraded-feedback isolation

- Consider stale-feedback or transport-loss injection only after Gates 2–4 pass and
  after a new operator review. Keep the arms at zero with the gantry attached.
- Expected software behavior is best-effort failure recording followed by publisher
  closure; measured-arrival fade cannot be claimed when feedback or writes are absent.
- The purpose is to observe stock-controller behavior and bound the residual risk,
  not to claim that software can guarantee a trajectory after transport loss or
  process death. Stop after the first unexplained result.

## Decision gate before further E2E

Proceed to bent-ready preparation and guarded VR pickup/pause/recovery only if the
operator accepts Gates 2–4 and the evidence shows measured arrival before every fade.
Keep physical validation pending if telemetry is incomplete, any handover trajectory
is surprising, stock-controller acceptance is ambiguous, or only Gate 1 passes.

After the session, create run records for meaningful motion tests with exact code and
configuration provenance, link all evidence, and keep observations separate from
interpretation. Record negative and aborted runs rather than optimizing for a pass.

## 2026-10-16 operator-reviewed amendment

When validating a recovery/failure-handling procedure, do not require that same
unvalidated procedure to be a proven-safe fallback for its own test. Failure during
recovery must be covered by an independent lower-level layer appropriate to the
experiment: gantry/support, clear workspace, and an operator with emergency control.
Define the recovery behavior being tested, its assumptions and abort conditions,
and the independent coverage before execution. Keep existing software guards and
record faults; do not recursively add unvalidated software recovery layers as a
prerequisite. This does not establish safety after transport/process failure or
prove that the recovery works; physical results remain pending until observed.

For this session, validate normal slow lowering, measured arrival/inspection hold,
and then separately confirmed authority fade. A fault aborts the experiment and
requires operator intervention under the independent physical coverage. The prior
claim that preparation fault/exit behavior must first be redesigned is superseded:
it imposed circular validation. Existing fault-triggered return remains a disclosed
residual risk, not a newly validated behavior. Operator accepted this principle and
instructed proceeding with experiments. Normal completion must not auto-fade before
inspection; fault behavior is distinct from normal completion.
