# SO101 teleoperation state machine

Status: proposed design, updated 2026-10-23 from operator discussion. Not implemented or physically validated. Target: MoissanClub/lerobot, SO101 leader/follower.

This design supersedes the earlier requirement for an explicit resume key after pickup: alignment plus dwell now resumes tracking automatically. “Pick up” is an operator action while Awaiting alignment, not a separate state.

## States and continuous actions

| State | Controller action | Operator guidance |
|---|---|---|
| Idle | Follower is at the configured initial rest pose with holding torque enabled. Ignore leader motion. | “Press Space to start.” |
| Lagging | Follow leader targets through a velocity/acceleration-limited trajectory. This state also handles initial catch-up after Start. | “Slow down” on entry, including startup; repeat at a bounded interval. No startup grace period. |
| Tracking | Follow leader targets within configured motion limits. | None. |
| Awaiting alignment | Suspend leader target forwarding and apply a defined follower holding policy. Continue measuring both arms for alignment. | “Pick up”: move the leader close to the measured follower pose. |
| Returning to rest | Execute a controlled trajectory to the configured initial rest pose. | “Returning to rest.” |
| Fault | Cancel normal following and apply fault-specific handling. Do not automatically return home. | Identify fault and required intervention. |

The initial rest pose is a configured, verified pose, not the pose measured arbitrarily at program launch. Returning to rest is an active movement phase; Idle is reached only after arrival. Startup from another pose requires an initialization policy, still to be specified.

## Transitions, triggers and entry actions

| From → To | Trigger | Transition action |
|---|---|---|
| Idle → Lagging | Keyboard **Space — Start** | Begin bounded following; announce “Slow down.” |
| Lagging → Tracking | All relevant joint errors stay within alignment tolerance for a dwell period | Continue following; stop slowdown prompts. |
| Tracking → Lagging | Joint tracking error exceeds the lag threshold for a sustained interval | Continue bounded following; announce “Slow down.” |
| Tracking → Awaiting alignment | A follower motor is at its calibrated boundary and the requested tracking direction points outward | Suspend leader target forwarding; log joint/boundary; announce “Pick up.” |
| Lagging → Awaiting alignment | Excessive error persists and measured progress is insufficient for a timeout | Suspend leader target forwarding; log nonprogress; announce “Pick up.” |
| Lagging → Awaiting alignment | A follower motor is at its calibrated boundary and the requested tracking direction points outward | Suspend leader target forwarding; log joint/boundary; announce “Pick up.” |
| Tracking or Lagging → Awaiting alignment | Keyboard **P — Disengage** | Suspend leader target forwarding; announce “Pick up.” |
| Awaiting alignment → Tracking | Leader aligns with measured follower pose on all relevant joints for a dwell period | Automatically resume without a target jump. |
| Lagging, Tracking or Awaiting alignment → Returning to rest | Keyboard **S — Stop** | Stop leader following; begin controlled return to rest. |
| Returning to rest → Idle | Rest pose reached within tolerance for a dwell period | Hold rest pose; wait for Start. |
| Any state → Fault | Communication/actuator fault, or blocked return to rest | Cancel normal motion; report cause; require explicit recovery. |

**Esc** requests an immediate software halt under a defined holding policy, with no automatic return home. Its destination state/recovery path remains unspecified; it is not a hardware emergency stop. Start during Returning to rest, repeated Stop, and Fault reset behavior must be resolved before implementation.

## Exact calibrated-boundary condition

For joint j, let q be measured follower position, t the leader-derived requested position in the same follower coordinate system, [L, U] its calibrated bounds, and epsilon a boundary tolerance. Trigger when either:

- **Upper boundary:** q >= U - epsilon and t > q.
- **Lower boundary:** q <= L + epsilon and t < q.

Any joint satisfying either condition requests Awaiting alignment from Tracking or Lagging. Being near a boundary alone is insufficient. A target pointing inward does not trigger this condition. Compare direction before clipping the requested target; log the request and actual sent command separately. Direction noise tolerance and boundary persistence, if needed, remain parameters to define without changing this intended condition.

This is specifically calibrated motor-boundary detection, not a general workspace/collision detector. Contact or binding away from calibrated boundaries is covered by sustained nonprogress from Lagging. Calibration extrema do not establish that every multi-joint configuration is collision-free.

## Tracking versus lagging recovery

The two routes to Awaiting alignment are intentionally distinct:

- **Tracking → Awaiting alignment:** a measured outward-boundary condition establishes a specific reason to disengage immediately; P also disengages directly.
- **Tracking → Lagging → Awaiting alignment:** unexplained tracking error first permits catch-up and prompts slowing down. Only persistent excessive error with insufficient progress triggers automatic disengagement.

A single large error does not prove nonprogress or a hard stop. Per-joint thresholds, signed progress windows, timeouts, alignment dwell and hysteresis must account for the measured static residual (approximately 3.43° elbow error in the prior fixed-pose checks). No numeric values are approved here. A velocity-based catch-up estimate may be unknown for stationary/moving-away joints and is not a validated transition trigger.

## Holding, continuity, logging and recording

Awaiting alignment holding behavior remains an implementation prerequisite: retaining an unreachable goal can sustain contact; torque-off can drop an unsupported arm. Specify the holding target and how to establish it, rather than treating suspension of new leader commands as sufficient. Entry from Fault may require a different policy.

Resume must avoid a target discontinuity despite alignment tolerance; the precise interpolation/handover rule remains to be designed. Stop/return must also handle an obstructed path rather than assume the rest pose can always be reached.

Log each transition with timestamp, reason, triggering joint, leader/follower positions, calibrated bounds, errors/progress, requested/sent commands and keyboard event. Record prompt requests/delivery separately.

Recording is an independent state machine. Starting/stopping recording must not implicitly start/stop teleoperation. Decide whether alignment/fault intervals pause, mark or discard data, and preserve control mode in telemetry. Recording keys must not conflict with Space/P/S/Esc above.

## Next agent action

Review and resolve holding policy, Esc destination, startup initialization, fault reset, transition priority, continuous resume and quantitative guards. Then implement and test transitions with mocked motors before a separate operator-supervised physical test. Prerequisites: verified calibration/rest pose, fresh feedback, clear workspace and defined recording semantics. No robot motion or controller changes are authorized by this document.
