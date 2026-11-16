# MuJoCo video return to Quest Pro during control

Experiment: `EXP-20261116-001`

## Purpose

Test the full closed operator loop: Quest controllers drive the stock dual-UR5e
MuJoCo example while the released Quest app displays a live view returned from
the Linux desktop.

The candidate preserves the released headset app. A local sender implements the
upstream control and framing protocol, captures the X11 desktop, scales the view
to 1280x720, and duplicates it into a 2560x720 side-by-side H.264 stream. The
result is monoscopic duplication in both eyes, not calibrated stereo.

## Readiness

- Controller transport and bilateral simulated motion were observed in
  `EXP-20261115-001`.
- X11 capture and RTX 5090 FFmpeg NVENC produced valid 2560x720 H.264.
- A local mock Quest sent the real `OPEN_CAMERA` protocol shape and received ten
  length-prefixed H.264 access units from the candidate sender.
- The physical Quest decoder/display path remains untested and is the reason for
  this experiment.

## Bounded stages

1. Stream-only recognition and continuity for at least 30 seconds.
2. Small right-arm motion while watching the returned view.
3. Both grips released and right controller repositioned; arm should stay still.
4. Small left-arm motion and released-grip pause.
5. Optional short bimanual motion only after the first four stages pass.

Stop for discomfort, a frozen/black view, tracking loss, or unexpected sustained
motion. This experiment cannot start any physical robot path.

## Interpretation

A pass demonstrates that a single bounded setup produced concurrent qualitative
video return and controller-driven simulation. It does not establish true stereo,
quantitative latency, long-run reliability, or physical-robot safety.
