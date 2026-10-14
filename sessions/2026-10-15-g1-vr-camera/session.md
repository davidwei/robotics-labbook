# SESSION-20261015-001 — G1 VR camera validation

2026-10-15 · PC2 / G1-29 · live capture · in progress.

**Objective:** validate P1 camera baseline and pause recovery before headset tests,
using LeRobot `45f49d460fb5395ebcee615c47f72e597b22f356` (P1 and P4).
No DDS connection or motor commands were used.

**Observed:** RealSense D435i RGB `/dev/video4`, 640×480 at 30 FPS, accepted and
reported a one-frame V4L2 buffer. The 20-second baseline read 600 frames, published
570 and skipped 30 publications. Three two-second publisher pauses recovered a
live offscreen frame with delivery age at most one frame period in **78.7, 78.6,
and 87.0 ms** after continuation. Recovery read 1,169 frames, published 1,097,
dropped three backlog frames and skipped 69 publications. Both runs ended normally
with `draining_at_exit=false`.

**Unmet criterion:** publication skips violate the checklist's strict zero-failure
criterion. FrameWriter returns false when its nonblocking write lock is busy.
A separate ten-second diagnostic without a reader published **300/300** frames
with zero failures, supporting reader contention as the source of skips. This
is partial validation, not a full P1 pass. Delivery timestamps do not establish
hardware exposure age or end-to-end headset latency.

**Next:** camera-only headset viewing has been prepared as a diagnostic. Operator
confirmation of live video and disconnect/reconnect behavior is pending. Do not
mark P1 fully validated or advance to physical-arm validation on this evidence.
The next engineering decision is whether to remove publication contention or
review the zero-skips acceptance criterion explicitly; it was not relaxed here.

[Run records](runs/) preserve metrics; [evidence registry](evidence.json) lists
locally stored artifacts and hashes. No LeRobot source changes were made; the
branch was fast-forwarded to the published revision. No controller or arm test
was performed.
