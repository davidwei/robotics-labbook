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

Camera-aware redirect prefill is deferred as [IDEA-20261015-001](../../ideas/IDEA-20261015-001/README.md). Next: repeat step 3 with manually selected 640×512 per eye, H.264, unchanged frame-rate setting, at least 60 seconds. This comparison has not yet been verified.

Lower-resolution step 3 was subsequently run: verified encoded output 1280×1152, about 43.2 FPS over a 52-second live prefix versus 17.9 FPS baseline. Zero encoder-input drops and packet-loss feedback in this sample. A first resolution-switch connection failed; the next succeeded. See analysis and RUN-20261015-004.

Operator confirmed low-resolution image quality and same-resolution disconnect/reconnect. A five-minute continuous streaming stability window is now pending; no stability pass claimed yet.

Extended stream: 6.5 minutes averaged 42.8 FPS with zero encoder-input drops, but slowed to ~31 FPS late in the sample. 720p capture works at 15 FPS on the current USB 2 connection; 30 FPS was rejected. Wider peripheral framing observed; viewer still scales into its 640×480 texture. Left running for operator review; details in analysis.

Operator clarified priority: preserve maximum camera field of view while allowing lower-resolution VR delivery. 1920×1080 capture at 8 FPS verified and left running; the entire frame is downscaled to 640×360 within the existing viewer texture, without cropping. 720p/1080p scene boundaries appear similar; exact angular FOV remains unmeasured.

Operator reported 1080p viewpoint identical to 720p and selected 720p. Active capture restored to 1280×720 at 15 FPS, with full-frame downscaling for VR and unchanged headset encoding settings. Evidence: /tmp/g1-resolution-check/camera720-final.jsonl (live). This is a configuration selection, not a new performance validation.

Gate 4 controller/video test started through XRControllers at 30 Hz consumer polling. Camera remains 1280×720@15; no robot object or DDS/motor connection. Tracking, input fields, sample age, and read duration are logged. Operator exercise and final analysis pending (RUN-20261015-007).

Controller exercise: 1,015 samples over ~34 seconds had head and both controllers tracked continuously. Positions, both sticks, A/B/X/Y, left grip and right trigger observed. Left trigger, right grip and both stick clicks were not observed and need a deliberate repeat. Sample-age p95 ~32 ms exceeds the ~12 ms target; reads themselves p95 ~0.37 ms. Gate 4 is not a full pass. Disconnect/recovery pending.

Repeated exercise confirmed the remaining left trigger, right grip and both thumbstick clicks. Operator states earlier motions were deliberately fast to test limits. Repeat tracked-sample p95 age ~27.3 ms still exceeds 12 ms; no causal attribution to fast movement. All requested raw input fields observed; disconnect/reconnect and downstream stop semantics remain unverified.

On operator-reported disconnect, controller consumer stayed responsive and both controllers became untracked with neutral inputs. Head remained marked tracked with zero position/identity orientation; this flag alone does not establish headset connectivity. Reconnect verification pending.

Controller reconnect recovered without restarting the harness: 955 fully tracked samples over ~32 seconds, both controller poses moving; server resumed video. Post-reconnect sample-age p95 33.5 ms (max 73.0), so the 12 ms target still fails. Raw inputs and reconnect work, but Gate 4 remains partial; downstream robot-stop behavior was not tested.

Code review identified a short-press loss risk: latest-value button states can be overwritten before consumption. One-second holds are an aid, not a guarantee; acknowledgment and preserved discrete events are proposed improvements. Upstream loss behavior remains unverified. See analysis and IDEA-20261015-002.

Gate 5 prepared: 10-minute combined camera/controller run with three 2-second camera pauses and three 2-second controller-publication pauses, stage timing and tegrastats. Begins after 2 seconds of full tracking. Tests original stale-timestamp rejection with no robot connection; modified temporary worker is preserved. Completion and operator observations pending.

During endurance, operator observed approximately 100 ms Pose-to-Render in the Isaac Teleop headset HUD. This is operator-reported, without raw client percentile capture. NVIDIA defines it from pose transmission to rendering the returned frame; it differs from local controller sample age and does not measure camera exposure-to-display or physical motion-to-photon latency.

**Gate 5 complete, partial pass:** 600.02 seconds, 17,938 consumer reads (15,065 fully tracked). Three camera recoveries 138–176 ms; three controller recoveries ~33 ms; 160 stale reads rejected. Normal fully tracked accepted samples had age p95 31.9 ms, exceeding 12 ms. Camera totals including startup: 9,593 reads, 9,133 publications, 454 lock skips, 6 drained frames; draining false at exit. Test processes cleaned up automatically. No physical robot commands were sent.

**Control-policy decision:** Pause must retain arm authority rather than trigger a potentially colliding stock-controller return trajectory. Requested headset gesture is B+Y held for one second, with no headset exit/handback. Guarded-path input loss/invalidity should hold immediately (250 ms stale threshold), require pickup on recovery, and report lost tracking after a continuous one-second gap. Camera loss alone must not pause control. Implementation is in progress; software and physical validation are pending.

**Scope correction:** Operator requested no further iteration on the Unitree-reference path and anticipates eventual removal because of potentially unsafe trajectories. Drafted reference-path pickup changes were reverted; upstream behavioral fidelity has not been fully established. Current development should focus on the guarded path, followed by software tests and controlled physical validation. Reference-path removal is deferred, not implemented.
