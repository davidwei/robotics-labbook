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

**Step 3:** operator reports “verified. no regression comparing to previous commits”
after the requested headset check. Recorded as an operator-reported pass; individual
check results and quantitative latency were not separately reported. Do not
mark P1 fully validated or advance to physical-arm validation on this evidence.
Decision: proceed to step 3 before optimizing publication contention. Optimization
is provisionally lower priority, pending headset results; the strict zero-skips
criterion remains unmet and has not been relaxed.

[Run records](runs/) preserve metrics; [evidence registry](evidence.json) lists
locally stored artifacts and hashes. No LeRobot source changes were made; the
branch was fast-forwarded to the published revision. No controller or arm test
was performed.

**Discussion before step 3:** skips occur when the publisher cannot acquire the
exclusive nonblocking lock on the RGB frame file while the display holds a shared
read lock. The lock protects metadata validation and the CPU pixel copy; it is
released before GPU upload, encoding, or network delivery. The file is on
NVMe-backed ext4 under `/tmp`, accessed through mmap/page cache. Moving it to
RAM-backed storage would not remove the locking mechanism; any performance gain
is unmeasured. Both local tests used one offscreen reader, with a full 921,600-byte
copy per fresh read, including duplicate sequences; its loop sleeps 1/90 second
in addition to processing. The illustrative 0.5 ms lock duration was not measured.

**Hypothesis, unverified:** encoding/rendering load and Wi-Fi delivery may be larger
end-to-end bottlenecks than local publication contention. No stage-by-stage drop
comparison or headset latency measurement supports that ranking yet. A 30 FPS
camera repeating frames in a faster headset display is not itself frame loss.
Step 3 will check live view, orientation, visible stutter, and reconnect behavior;
subjective observations will not be presented as quantitative latency validation.

[Headset run](runs/RUN-20261015-003.yaml) and [evidence snapshot](headset-evidence.json)
preserve this verification. Camera/viewer processes remain running pending shutdown.

**Streaming log review:** functional headset verification achieved about 18 FPS at
4096×4032 encoded resolution; zero reported encoder-input drops, but low throughput
and occasional long frame intervals. See [analysis](analysis.md). Server processing
is the leading bottleneck hypothesis; this is not a quantitative regression comparison.
