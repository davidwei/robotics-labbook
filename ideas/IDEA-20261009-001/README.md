# G1 VR teleoperation performance improvements

**Status:** in development; P1 and P4 implemented in software, manual validation pending.
**Owner:** David Wei  
**Date:** 2026-10-09  
**Last updated:** 2026-10-10
**Code target:** `MoissanClub/lerobot`, branch `work/g1-vr-physical`.

## Research motivation

The headset camera stream sometimes falls behind without recovering, and XR controller tracking sometimes lags or briefly drops out.

## Original plan

The complete original proposal is preserved verbatim in [g1-vr-perf-plan.md](g1-vr-perf-plan.md). It defines P1–P5 in order: camera V4L2 backlog; camera/XR thread contention; IK latency; latest-controller-sample mailbox; and watchdog/recording overhead.

These proposed explanations and performance targets are **hypotheses**, not yet validated findings.

## Next Codex action — development / pre-lab

1. Pull the latest lab book and follow `skills/labbook/SKILL.md` in Development and Pre-Lab modes.
2. Read the complete [execution plan](g1-vr-perf-plan.md).
3. Work in the specified `MoissanClub/lerobot` branch, one revertible commit per P1–P5 task, preserving every safety constraint in the plan.
4. Run the requested automated tests and lint after each task; record actual results and commit SHAs.
5. Prepare baseline-versus-changed measurements and the plan's manual checks for supervised hardware testing.
6. Do not autonomously execute hardware-only validation. Keep untested claims marked as such.
7. Update this record with implementation status and link physical experiments/sessions/runs when they occur.

## Pending lab-validation checklist

Use code revision `45f49d460fb5395ebcee615c47f72e597b22f356` on `work/g1-vr-physical`. The branch contains P4 commit `126349e2` immediately below P1. Both commits were pushed to `MoissanClub/lerobot:work/g1-vr-physical` on 2026-10-10, with P1 as the remote branch head. Preserve the exact executed revision and any dirty-tree patch in the session record.

### Readiness order

1. **P1 camera-only baseline and pause recovery — ready for lab.** Requires the Jetson, the real G1 camera, a working CUDA/Isaac Teleop offscreen environment, and no robot connection or controller.
2. **P1 headset delivery and reconnect — ready after the camera-only gate.** Requires CloudXR/OpenXR and the headset, but still no DDS connection or robot motion.
3. **P4 controller freshness under camera load — ready after stable video delivery.** Requires the headset/controllers and controller-age instrumentation; keep robot motion disabled.
4. **Combined supervised physical-arm regression — gated.** Requires explicit operator authorization and the ordinary G1 physical preflight. Run only after the read-only P1/P4 gates pass.
5. **GPU-assisted camera investigation (`IDEA-20261009-002`) — deferred.** Requires P1/P2 baseline profiles showing that CPU decode/conversion or copies are a material bottleneck.

### Gate 0 — preflight and evidence readiness

- [ ] Record host, Jetson, camera model/device path, pixel format, requested resolution/FPS, headset/runtime versions, exact code revision, and command lines.
- [ ] Confirm the working tree and installed checkout correspond to the recorded revision; preserve any patch if dirty.
- [ ] Confirm the real camera is visible and can sustain the requested mode. Record OpenCV backend and `/dev/video` path.
- [ ] Use new, non-overwriting JSONL output paths for every camera and display run; verify available disk space and readable debug logging.
- [ ] Confirm the offscreen Vulkan/CUDA display works before involving the headset.
- [ ] Confirm no robot/DDS process or motor publisher is started for Gates 1–3.
- [ ] Prepare screen/video capture or a timestamped operator log. Preserve camera JSONL, display JSONL, controller-age logs, warnings, and failure reports.
- [ ] Rollback/isolation path: P1 and P4 are separate commits and can be reverted independently; the minimum useful experiment is Gate 1 camera-only recovery.

### Gate 1 — P1 real-camera configuration and baseline

- [ ] Start the read-only camera publisher and offscreen display with the same channel and source ID; do not connect to DDS or a robot.
- [ ] Confirm the first `camera_config` record reports `buffer_size_requested=1`, `buffer_size_set=true`, `buffer_size_actual=1`, and `buffer_size_honored=true`.
- [ ] If the backend rejects or misreports `CAP_PROP_BUFFERSIZE`, preserve the warning and debug log and mark the mitigation unverified; do not treat the run as a P1 pass.
- [ ] Confirm the live display receives fresh frames at the requested dimensions and approximate cadence, with `publish_failures=0`.
- [ ] Confirm `timestamp_semantics=opencv_delivery` is present. Interpret `camera_age_ms` only as a lower bound on the frame's true hardware age.
- [ ] End one normal baseline run and confirm `frames_published>0`, `backlog_frames_dropped=0` or an explained small count, `publish_failures=0`, and `draining_at_exit=false`.

### Gate 2 — P1 pause/backlog recovery

- [ ] During a stable camera/display run, send `SIGSTOP` to the actual camera publisher process for 2 seconds, then `SIGCONT` it.
- [ ] Confirm the camera report records `dropped_reason=draining_backlog` after continuation and identifies the trigger (`slow_read` or `fast_read`).
- [ ] Confirm publication resumes rather than remaining permanently behind.
- [ ] Confirm display `camera_age_ms` returns to approximately one frame period within 1 second of continuation.
- [ ] Confirm the final summary has `frames_published>0`, `backlog_frames_dropped>0`, `publish_failures=0`, and `draining_at_exit=false`.
- [ ] Repeat the stop/continue check at least three times. Preserve each recovery time; do not generalize reliability from a single success.
- [ ] Negative criteria: no publication recovery, `draining_at_exit=true`, zero published frames, buffer negotiation unconfirmed, or camera age remaining elevated. Preserve the full failed/cancelled report.

### Gate 3 — P1 camera/headset loss and recovery

- [ ] Run the same source through the live headset display after the offscreen gate passes.
- [ ] Confirm the headset view is live, correctly oriented, and visually current before inducing faults.
- [ ] Stop or disconnect the camera publisher and confirm a stale/unavailable indication appears rather than a frozen frame being presented as live.
- [ ] Restart/reconnect the publisher and confirm a new camera session is accepted and live delivery resumes.
- [ ] Exercise a source-ID mismatch and confirm the display reports `Camera source mismatch` rather than displaying it as the expected feed.
- [ ] Confirm display shutdown/restart and headset reconnect do not require starting any robot-control process.

### Gate 4 — P4 latest-controller-sample validation, robot motion disabled

- [ ] Run the normal headset/controller plus video path with robot motion disabled and log `time.monotonic() - action["captured_at"]` at the controller consumer.
- [ ] Measure controller sample age while camera rendering is active. Acceptance target: approximately `p95 <= 12 ms`; also preserve sample count, p50, p99, and maximum.
- [ ] Confirm both controllers remain continuously tracked during stable operation; correlate any tracking loss with camera/upload/render timing.
- [ ] Exercise grip pose/quaternion, squeeze, trigger, and—when full input is enabled—sticks, stick clicks, primary/secondary buttons, and head pose. Confirm schema, shapes, and values remain plausible.
- [ ] Confirm stop-button handling and neutral/fallback behavior for missing or malformed head/controller input.
- [ ] Disconnect and reconnect the headset/controllers. Confirm the worker exits or reports loss cleanly, no consumer hangs on a lock, and fresh samples resume after reconnect.
- [ ] Confirm stale-sample checks still reject old input; do not relax any existing freshness or safety limit to obtain a pass.

### Gate 5 — combined P1/P4 endurance, robot motion disabled

- [ ] Run camera, headset display, and controller acquisition together for at least 10 minutes.
- [ ] Repeat camera `SIGSTOP`/`SIGCONT` while logging controller age and tracking; camera recovery must not cause persistent controller lag or loss.
- [ ] Confirm camera publication/recovery criteria and controller `p95` target simultaneously.
- [ ] Preserve CPU/GPU utilization, camera/display/controller reports, warnings, and operator observations. Note that one successful endurance run demonstrates only that run's conditions.

### Gate 6 — supervised physical-arm regression, separate authorization required

- [ ] Obtain explicit operator approval for robot motion and complete the standard G1 physical preflight, safe workspace, stop controls, mode/lease checks, and known-safe baseline.
- [ ] Before enabling following, re-confirm live video, current controller samples, continuous tracking, and working stop buttons.
- [ ] At a conservative posture and speed, verify arm following remains smooth and current while video is active; watch for lag, jumps, stale targets, or tracking dropouts.
- [ ] Exercise the operator stop path, controller/headset disconnect, and reconnect behavior under the existing safety procedure. Existing staleness, torque, displacement, workspace, mode, read-only, and lease checks must remain unchanged.
- [ ] Stop immediately on unexpected motion, stale input, loss of tracking, instability, safety-check failure, or unexplained camera/controller latency.
- [ ] Record this as a physical run only if meaningful evidence is produced: exact revision/config, run boundary, telemetry/video references, operator observations, and whether each acceptance criterion passed.

### Completion criteria

- P1 may be marked physically validated only after Gates 1–3 pass on the real Jetson camera path with preserved reports.
- P4 may be marked physically validated only after Gate 4 meets the controller-age/tracking criteria. Gate 5 provides combined-load evidence.
- Gate 6 is required before claiming the changes are validated for physical-arm teleoperation, but it is not authorized by this checklist.
- Record failures and contradictory evidence; do not upgrade a software or offscreen result into physical validation.

## Handoff status

- Original plan captured: yes.
- P1 code commit: `45f49d460fb5395ebcee615c47f72e597b22f356` (`perf(unitree_g1): drain stale camera frames after stalls`) on `work/g1-vr-physical`; pushed to `MoissanClub/lerobot:work/g1-vr-physical` on 2026-10-10 and verified as the remote branch head.
- P1 implementation evidence: `OpenCVCameraConfig` has an optional, backward-compatible capture buffer depth; the read-only publisher requests one buffer, records backend acceptance/readback, timestamps OpenCV delivery explicitly, detects slow or abnormally fast post-stall reads, drains queued frames until live cadence resumes, and emits a summary on normal or abnormal exit. No robot-control or safety file changed.
- P1 software validation: focused OpenCV/read-only suite `66 passed, 1 skipped`; final broad available suite `585 passed, 41 skipped` with the two separately installed Unitree SDK modules excluded; Ruff check, Ruff format check, and `git diff --check` passed. A real Isaac Teleop offscreen Vulkan/CUDA frame-delivery smoke test passed.
- P1 review evidence: Claude review was repeated through five rounds. Findings about unverified buffer negotiation, optimistic timestamp semantics, stale-frame recovery, incomplete summaries, drain convergence, deterministic clocks, and positional config compatibility were addressed. The fifth-round verdict was `No actionable findings.`
- P1 environment limitations: this development host has no `/dev/video` device, so V4L2 negotiation and stop/continue recovery remain physically unverified. An expanded suite reached `587 passed, 41 skipped`, then the SDK/reference modules produced `6 failed, 38 errors` because `unitree_sdk2py` is not installed. Targeted mypy reaches a pre-existing OpenCV stub error for `cv2.VideoWriter_fourcc` on an unchanged line.
- P1 interpretation: software evidence supports backward-compatible configuration, non-fatal unsupported-backend behavior, observable buffer negotiation, conservative backlog draining, and preserved failure evidence. It does not establish camera freshness or recovery time on the Jetson camera driver.
- Manual P1 validation TODO (camera/headset only; no robot motion): on the G1 Jetson, confirm `camera_config.buffer_size_honored=true`; run the read-only publisher and offscreen/headset display; stop the publisher with `SIGSTOP` for 2 seconds and continue it with `SIGCONT`; confirm `camera_age_ms` returns to approximately one frame period within 1 second, queued frames are reported as dropped, publication resumes, and the summary reports `draining_at_exit=false`. Preserve the JSONL reports and debug logs, including any buffer-size warning.
- P4 code commit: `126349e2` (`perf(unitree_g1): keep the latest XR controller sample`) on `work/g1-vr-physical`; pushed to `MoissanClub/lerobot:work/g1-vr-physical` on 2026-10-10 immediately below the P1 commit.
- P4 implementation evidence: the XR video subprocess now publishes controller input through a fixed-schema shared-memory latest-value slot instead of `multiprocessing.Queue(1)`. Lock acquisition is bounded to 1 ms, and malformed full-input head poses fall back to neutral values.
- Software validation: relevant G1/VR suite `191 passed, 19 skipped`; focused XR input/video suite `20 passed, 2 skipped` in the final run, with the XR video file also passing three consecutive contention-test runs; targeted mypy, Ruff check, Ruff format check, and `git diff --check` passed.
- Review evidence: Claude review was repeated after each revision. It identified the multiprocessing queue feeder race, lock-holder liveness risk, insufficient concurrent-test overlap, and malformed head-pose handling. The final implementation and post-mypy verification both received `No actionable findings.`
- Environment limitation: an exploratory expanded suite reached `200 passed, 19 skipped`, then the two SDK/reference modules produced `6 failed, 38 errors` because `unitree_sdk2py` is not installed in the test environment. These are not counted as P4 validation passes.
- Interpretation: software evidence supports last-write-wins behavior, consistent cross-process snapshots for both schemas, bounded read/write waiting, and preservation of the last valid timestamped sample. It does not establish headset-to-consumer latency on the real XR path.
- Manual P4 validation TODO: run the normal supervised G1 VR headset/video path, record `time.monotonic() - action["captured_at"]` at the consumer, and confirm approximately `p95 <= 12 ms` while camera rendering is active. Also verify tracking, stop buttons, head pose, disconnect, and reconnect behavior before enabling robot motion.
- Physical validation performed for P1 or P4 by these lab-book additions: none.
