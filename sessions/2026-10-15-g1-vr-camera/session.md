# SESSION-20261015-001 — G1 VR validation and physical preparation

2026-10-15 · PC2 / G1-29 · session ended; validation incomplete.

## What was learned

- Camera baseline and injected-pause recovery worked, with publication skips from
  nonblocking shared-frame locking. A no-reader diagnostic had no skips. Contention
  is an improvement opportunity; it is not established as the dominant E2E bottleneck.
- Operator accepted video and controller behavior without an observed regression.
  Selected camera capture: **1280×720 at 15 FPS** on USB 2, full frame downscaled
  without cropping. 1080p had no visible additional viewpoint. Client per-eye
  640×512 produces a packed 1280×1152 stream; capture, texture and encoding sizes differ.
- Ten-minute endurance completed with three camera and three controller-publication
  interruptions. Recovery worked; 160 stale reads were rejected. Normal accepted
  controller-age p95 was **31.9 ms**, exceeding the 12 ms target. This age starts
  after PC2 acquisition, not headset capture. Operator HUD Pose-to-Render was ~100 ms;
  the two metrics are not disjoint stages to add or subtract.
- Latest-value input can miss short button presses. Live B+Y tests distinguished a
  ~0.61 s press from a ~1.89 s hold; only the latter latched pause. Four virtual pickup
  entries and 1,295 following samples showed no target jumps at transitions and no
  stop/damp outputs. Operator accepted tracking. This did not validate physical hold.

## Physical tests and failures

Operator confirmed gantry, clear arm workspace, regular action mode and emergency
control. Fresh feedback and sampled preparation-workspace checks passed.

- **RUN-009:** preparation stopped after ~7 s of publication on a 0.03 rad
  position-error guard. Last right-elbow error was 0.0311 rad. VR following had not
  started. SDK cleanup released authority; operator confirmed the robot stationary.
- **RUN-010:** enabled gravity feedforward and a preparation-only 0.08 rad error
  allowance, keeping following/hold at 0.03 rad. Zero-angle target was reached, but
  a ~0.0206 rad wrist residual blocked the separate 0.02 rad arrival gate. Operator
  reported that the arm raised successfully and very slowly; software never marked
  the configured bent-ready pose complete. These observations must remain distinct.
  After pausing, normal quit tripped at right-shoulder speed −0.1166 rad/s against
  a 0.10 rad/s guard and released authority. Post-second-fault stationary confirmation
  was requested but not received. Startup/paused TTS returned status 3104.

## Changes and validation limits

Guarded pause/pickup/fault handling, English voice prompts, preparation feedforward
and phase-specific error limits were edited. Preparation arrival was subsequently
changed to 0.025 rad; offline tests passed, but that arrival change was not run on
hardware. Test batches passed (110, 50, 87, 100; overlapping coverage); Ruff passed
for checked files. Unitree-reference pickup behavior was preserved; further work on
that path is deferred and eventual removal is anticipated. LeRobot changes were subsequently committed and pushed to
`MoissanClub/lerobot:work/g1-vr-physical`: `4d9d9724` (VR pause/pickup) and
`355ac624` (preparation feedforward/tolerances). The final tree passed 148 targeted
tests and Ruff. The end-of-session patch remains preserved. MUJOCO_LOG.TXT was
left untouched. Per-run patches preserve the actual physical execution states.

## First priority next session

**Return to stock control requires much more care to avoid dangerous trajectories.**
Upstream normal exit fades authority after homing; our guarded cleanup drops it
immediately, including on faults. A guard trip is not necessarily a safe stop, and
slower blending alone does not bound the stock controller's motion. Resolve this
before further E2E motion. See [IDEA-20261015-003](../../ideas/IDEA-20261015-003/README.md).

Next: offline handover/fault-policy review and tests → separate gantry return/hold
validation → complete bent-ready preparation → physical pickup, pause and recovery
→ E2E endurance. Controlled post-pickup camera/stale-input tests were deferred.

## Shutdown and evidence

End-of-day process check found no matching teleoperation, ready-pose test, camera,
audio-sidecar or CloudXR processes. No further motion is authorized by this record.
Robot's final physical posture was not independently verified after the last fault.
Detailed evidence: [analysis](analysis.md), [runs](runs/), and timeline.jsonl.
Artifacts: `~/robotics/artifacts/2026-10-15-g1-vr-camera/`, including manifests,
per-run logs/code snapshots and end-of-session patch. Capture is partial; artifacts
are local, without remote backup. Original incremental session notes are preserved
as `end-of-session/session-before-close.md`.
