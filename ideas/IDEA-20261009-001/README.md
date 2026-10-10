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

## Handoff status

- Original plan captured: yes.
- P1 code commit: `45f49d46` (`perf(unitree_g1): drain stale camera frames after stalls`) on `work/g1-vr-physical`; local only at the time of this record.
- P1 implementation evidence: `OpenCVCameraConfig` has an optional, backward-compatible capture buffer depth; the read-only publisher requests one buffer, records backend acceptance/readback, timestamps OpenCV delivery explicitly, detects slow or abnormally fast post-stall reads, drains queued frames until live cadence resumes, and emits a summary on normal or abnormal exit. No robot-control or safety file changed.
- P1 software validation: focused OpenCV/read-only suite `66 passed, 1 skipped`; final broad available suite `585 passed, 41 skipped` with the two separately installed Unitree SDK modules excluded; Ruff check, Ruff format check, and `git diff --check` passed. A real Isaac Teleop offscreen Vulkan/CUDA frame-delivery smoke test passed.
- P1 review evidence: Claude review was repeated through five rounds. Findings about unverified buffer negotiation, optimistic timestamp semantics, stale-frame recovery, incomplete summaries, drain convergence, deterministic clocks, and positional config compatibility were addressed. The fifth-round verdict was `No actionable findings.`
- P1 environment limitations: this development host has no `/dev/video` device, so V4L2 negotiation and stop/continue recovery remain physically unverified. An expanded suite reached `587 passed, 41 skipped`, then the SDK/reference modules produced `6 failed, 38 errors` because `unitree_sdk2py` is not installed. Targeted mypy reaches a pre-existing OpenCV stub error for `cv2.VideoWriter_fourcc` on an unchanged line.
- P1 interpretation: software evidence supports backward-compatible configuration, non-fatal unsupported-backend behavior, observable buffer negotiation, conservative backlog draining, and preserved failure evidence. It does not establish camera freshness or recovery time on the Jetson camera driver.
- Manual P1 validation TODO (camera/headset only; no robot motion): on the G1 Jetson, confirm `camera_config.buffer_size_honored=true`; run the read-only publisher and offscreen/headset display; stop the publisher with `SIGSTOP` for 2 seconds and continue it with `SIGCONT`; confirm `camera_age_ms` returns to approximately one frame period within 1 second, queued frames are reported as dropped, publication resumes, and the summary reports `draining_at_exit=false`. Preserve the JSONL reports and debug logs, including any buffer-size warning.
- P4 code commit: `126349e2` (`perf(unitree_g1): keep the latest XR controller sample`) on `work/g1-vr-physical`; local only at the time of this record.
- P4 implementation evidence: the XR video subprocess now publishes controller input through a fixed-schema shared-memory latest-value slot instead of `multiprocessing.Queue(1)`. Lock acquisition is bounded to 1 ms, and malformed full-input head poses fall back to neutral values.
- Software validation: relevant G1/VR suite `191 passed, 19 skipped`; focused XR input/video suite `20 passed, 2 skipped` in the final run, with the XR video file also passing three consecutive contention-test runs; targeted mypy, Ruff check, Ruff format check, and `git diff --check` passed.
- Review evidence: Claude review was repeated after each revision. It identified the multiprocessing queue feeder race, lock-holder liveness risk, insufficient concurrent-test overlap, and malformed head-pose handling. The final implementation and post-mypy verification both received `No actionable findings.`
- Environment limitation: an exploratory expanded suite reached `200 passed, 19 skipped`, then the two SDK/reference modules produced `6 failed, 38 errors` because `unitree_sdk2py` is not installed in the test environment. These are not counted as P4 validation passes.
- Interpretation: software evidence supports last-write-wins behavior, consistent cross-process snapshots for both schemas, bounded read/write waiting, and preservation of the last valid timestamped sample. It does not establish headset-to-consumer latency on the real XR path.
- Manual P4 validation TODO: run the normal supervised G1 VR headset/video path, record `time.monotonic() - action["captured_at"]` at the consumer, and confirm approximately `p95 <= 12 ms` while camera rendering is active. Also verify tracking, stop buttons, head pose, disconnect, and reconnect behavior before enabling robot motion.
- Physical validation performed for P1 or P4 by these lab-book additions: none.
