# Quest Pro MuJoCo video return and simultaneous control

**Session:** SESSION-20261116-002 · **Experiment:** [EXP-20261116-001](../../experiments/EXP-20261116-001/plan.md) · **Status:** ended; bounded combined run passed, review pending

## Objective and result

Test whether the released XRoboToolkit Quest v1.0.1 app could display a live
Linux MuJoCo desktop return while its independent controller path operated the
stock dual-UR5e simulation.

The bounded combined run passed. After a sender protocol correction, the
operator saw the desktop in the headset. The sender then sustained a 2560x720
H.264 stream at approximately 60 fps for about 192 seconds, ending on the
headset's explicit `CLOSE_CAMERA`. While viewing the return stream, the operator
reported deliberate right, left and bimanual simulated-arm motion. With the grip
released, the corresponding arm did not follow controller repositioning.

This demonstrates duplicated monoscopic desktop return and qualitative
simultaneous control in one bounded setup. It does not establish calibrated
stereo, numerical latency, long-run reliability or physical-robot safety.

## Failures and recovery

- The first sender candidate rejected three real Quest control connections and
  the headset showed a green square with “data reception error.” The candidate
  had omitted the four-byte big-endian wrapper used by the Android TCP layer and
  explicitly removed by the upstream Orin sender. No video access unit reached
  the headset in those attempts.
- The corrected candidate passed three unit tests and a local wrapped-control
  mock that received ten H.264 access units. Its first physical connection sent
  one access unit and then received a broken pipe; the headset sent
  `CLOSE_CAMERA`. Reopening Listen produced the sustained successful stream.
- Controller motion was initially absent even though the socket had appeared
  connected. Operator reconnect restored control. The simulator recorded device
  missing/found transitions and JSON parse warnings around that recovery.
- The released app's `WORKING` label reflects socket state, not verified
  end-to-end tracking flow. A stale-data/reconnect prompt is proposed in
  [IDEA-20261116-001](../../ideas/IDEA-20261116-001/README.md).

## Evidence limits

The desktop recording and operator observation support visible arm motion, but
the simulator console did not emit hand-activation lines in this run and no
synchronized controller/joint telemetry was captured. No Quest-side recording
was obtained. Stream-rate evidence comes from sender frame counts, not an
independent headset presentation-rate measurement.

## Next action

Review the desktop recording around the successful stream/control stages. If the
result is to become a reusable tool, place the sender in a tracked repository,
add fragmented/multiple control-packet tests and a repeatable run wrapper, then
perform a separate latency/integrity experiment. The client health prompt needs
an end-to-end PC acknowledgment rather than controller-motion heuristics alone.
