# G1 VR teleop performance fixes — execution plan

Repo: `MoissanClub/lerobot`, branch `work/g1-vr-physical` (diff vs `huggingface/lerobot:main`).
Target: Unitree G1 onboard Jetson Orin, physical arm mode with XR controllers + live camera.

## Symptoms
1. Camera stream in the headset sometimes falls behind and never catches up.
2. Controller tracking sometimes lags or briefly drops out.

## Ground rules for the agent
- Work in the order below (P1 → P5). One commit per task; keep each commit self-contained and revertible.
- **Do not weaken any safety check.** Keep every existing validation in `g1_motion.py`, `g1_arm_sdk.py`, `g1_vr_processor.py`, `g1_vr_control.py` (staleness limits, torque/displacement/workspace limits, mode checks, `read_only`, lease locks). If a change seems to require relaxing one, stop and leave a `TODO(review)` note instead.
- Do not change public config field names or CLI flags; only add new optional fields with defaults that preserve current behavior where noted.
- Run `pytest tests/robots tests/teleoperators tests/cameras tests/utils tests/scripts tests/integration -q` after each task; all existing tests must pass. Add the new tests listed per task.
- Run `ruff check` and `ruff format` on touched files.
- Hardware-only validation steps are listed under "Manual check"; do not attempt them, just keep them in the PR description.

---

## P1 — Camera publisher can't drain its V4L2 backlog (very low complexity)

**Files:** `examples/unitree_g1/validate_xr_readonly.py` (`camera()`), `src/lerobot/cameras/opencv/camera_opencv.py`, `src/lerobot/cameras/opencv/configuration_opencv.py`

**Problem:** loop is blocking `source.read()` → `publish` → JSON record+flush → `time.sleep(1/fps - elapsed)`. After any stall, the V4L2 queue (default ~4 buffers; `CAP_PROP_BUFFERSIZE` is never set) holds stale frames; `read()` then returns immediately and the sleep pads every iteration back to 1/fps, so the backlog drains at exactly the production rate and never shrinks. `captured_monotonic_ns` is stamped *before* `read()`, so a buffered stale frame looks fresh and `camera_age_ms` hides the problem.

**Steps:**
1. Add optional `buffer_size: int | None = None` to `OpenCVCameraConfig`. In `OpenCVCamera.connect`, if set, call `self.videocapture.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)` (ignore failure, log at debug).
2. In `validate_xr_readonly.py camera()`:
   - Construct the config with `buffer_size=1`.
   - Remove the trailing `time.sleep(...)`; the blocking `read()` paces the loop.
   - Stamp `captured_monotonic_ns = time.monotonic_ns()` **after** `read()` returns (still never restamp a cached frame).
3. Leave `g1_motion.py` camera mode as-is (it already uses `async_read`, which is latest-frame).

**Tests:** in `tests/cameras/`, a unit test with a mocked `cv2.VideoCapture` asserting `set(CAP_PROP_BUFFERSIZE, 1)` is called when configured and not called when `None`.

**Manual check:** run the publisher, `kill -STOP` it for 2 s, `kill -CONT`; `camera_age_ms` in the display report must return to ≤ ~1 frame period within 1 s.

---

## P2 — XR worker does heavy camera work on the 90 Hz controller thread (low–medium)

**Files:** `src/lerobot/cameras/frame_channel.py`, `src/lerobot/teleoperators/xr_controllers/camera_display.py`, `src/lerobot/teleoperators/xr_controllers/video_session.py`

**Problems:**
- `read_frame` slices `mapping[HEADER_BYTES:]` (a full ~921 KB copy) on every call at 90 Hz, even when the sequence is unchanged, while holding `LOCK_SH`. The writer's `LOCK_NB` then fails and the frame is dropped (`publish` returns `False`).
- `_upload` allocates a new RGBA array, runs PIL `thumbnail` even when sizes match, and does a pageable host→GPU copy per frame.
- `video_worker` sleeps `stop.wait(1/90 - elapsed)` after `render()`, which likely already blocks on `xrWaitFrame` → double pacing.
- A missed XR frame sets `frame_deadline_miss`, and `IsaacControllerSession.read()` then reports both controllers `tracked=False`. So camera upload spikes show up as controller dropouts.

**Steps:**
1. `frame_channel.py`:
   - Add `read_frame_if_new(path, last_key, max_age_s, *, raise_on_busy=False)` that parses the header first and returns `None` (distinguishable from "unavailable", e.g. a sentinel `UNCHANGED`) when `(session_id, sequence) == last_key`, **without** touching pixel bytes. Only copy pixels for a new frame, using `np.frombuffer(mapping, dtype=np.uint8, count=w*h*3, offset=HEADER_BYTES).copy()` (single copy, no intermediate bytes object).
   - Keep `read_frame` behavior unchanged for existing callers/tests (it may delegate).
   - Optional, behind a new `VERSION = 2` only if tests stay green: replace flock with a seqlock (even/odd sequence in header, reader retries on mismatch) so neither side ever drops. If this is not straightforward, skip it and note it in the PR.
2. `camera_display.py`:
   - Use `read_frame_if_new` with `self.last_key`; on `UNCHANGED`, update `camera_age_ms` from `last_captured_ns` and return.
   - In `_upload`: if `pixels.shape[:2] == (height, width)`, skip PIL entirely. Preallocate once a pinned host tensor (`torch.empty(..., pin_memory=True)`) of shape HxWx3; copy pixels into it, `self.gpu[..., :3].copy_(host, non_blocking=True)`, keep alpha channel pre-filled with 255 (fill once at init). Keep the PIL letterbox path only for mismatched sizes.
   - Cache the rendered placeholder image per status string instead of redrawing.
3. `video_session.py` `video_worker`: add `VideoConfig.extra_pacing: bool = False`; when `False`, drop the trailing `stop.wait(...)` and only check `stop.is_set()`. Add a tiny `stop.wait(0.001)` fallback only when `render()` returns `should_render == False` and returned in < 1 ms (to avoid a busy spin if the runtime doesn't block).
4. Add timing stats to `CameraDisplay.stats`: `upload_ms_last`, `upload_ms_max`.

**Tests:** extend `tests/teleoperators/test_unitree_g1_xr_video.py` / `tests/robots/test_unitree_g1_camera.py`:
- `read_frame_if_new` returns `UNCHANGED` for the same sequence and does not read pixel bytes (patch `np.frombuffer` to assert not called).
- Writer `publish` succeeds while a reader polls an unchanged frame in a tight loop (no drops over N iterations).
- Same-size upload path does not call `Image.fromarray`.

**Manual check:** in the display report, `frame_loops ≈ render_requested`, `publish` never `False`, controller `tracked` stays `True` continuously while the camera runs.

---

## P3 — IK solve + moving-average filter inline at 30 Hz (medium)

**Files:** `src/lerobot/robots/unitree_g1/g1_vr_control.py` (`G1VRKinematics.solve`), `src/lerobot/robots/unitree_g1/g1_kinematics.py` (`G1_29_ArmIK`), `src/lerobot/robots/unitree_g1/g1_vr_processor.py`

**Problems:** IPOPT runs with `max_iter=50, tol=1e-6` every tick in the teleop loop; `solve()` deep-copies the smoothing filter each call; `WeightedMovingFilter([0.4,0.3,0.2,0.1])` adds a mean delay of exactly 1 tick (33 ms at 30 Hz).

**Steps:**
1. `G1_29_ArmIK.__init__`: add keyword args `ipopt_tol=1e-6, ipopt_max_iter=50, filter_weights=(0.4,0.3,0.2,0.1)` (defaults = current behavior, so upstream users are unaffected). Pass them into the solver options / filter.
2. `G1VRKinematics.__init__`: accept `tracking: bool = False`. When `True`, construct `G1_29_ArmIK(..., ipopt_tol=1e-4, ipopt_max_iter=15, filter_weights=(1.0,))` (filter disabled; smoothing comes from the arm SDK's velocity/accel limits plus step 4).
3. Replace `copy.deepcopy(self.solver.smooth_filter)` with saving/restoring only the filter's internal data array (`.copy()` of the ndarray(s)).
4. Add an optional one-pole low-pass on the IK output in `G1VRKinematics` with `cutoff_hz` (default `None` = off). Implement `alpha = 1 - exp(-2π·fc·dt)` using the actual dt between calls.
5. In `g1_vr_processor.py`, use a separate `G1VRKinematics(tracking=True)` instance for per-tick tracking solves (`_test_target`, `action` following path). Keep the existing high-accuracy instance for activation/reference solves (`_reference_action` with `max_step=None`, warm-up solves). Do not change `max_step` clipping or any bounds checks.
6. Wrap the per-tick solve in `timer.section("ik")` if a timer is reachable; otherwise record `ik_ms` in the processor's status dict.
7. Optional (separate commit): a damped-least-squares Pinocchio IK (`J^T (J J^T + λ²I)^-1 e`, 1–3 iterations, joint-limit clamp) as `G1VRKinematics.solve_fast`, selectable via processor config `ik_backend: "ipopt" | "dls"` defaulting to `"ipopt"`.

**Tests:** in `tests/robots/test_unitree_g1_vr_pipeline.py` / `test_unitree_g1_reference.py`:
- Default `G1_29_ArmIK()` options unchanged (tol 1e-6, max_iter 50, 4-tap filter).
- Tracking instance reaches a target within 5 mm on the existing synthetic inputs.
- Failed solve still restores the filter state (behavioral equivalent of the old deepcopy test).
- Low-pass with `cutoff_hz=None` is identity.

**Manual check:** `ik` p99 < 5 ms on Orin; then try `--fps=60`, and `--fps=90` if the cadence summary shows no budget overruns.

---

## P4 — Controller mailbox keeps the oldest sample (low)

**Files:** `src/lerobot/teleoperators/xr_controllers/video_session.py`

**Problem:** mailbox is `Queue(1)` written with `put_nowait` and `queue.Full` suppressed, so the **newest** sample is discarded. Producer 90 Hz, consumer 30 Hz → each read gets a sample ~22–33 ms old instead of ≤ ~11 ms.

**Steps (do 1; do 2 if time allows):**
1. Minimal fix in `video_worker`: before `put_nowait(sample)`, `with suppress(queue.Empty): frames.get_nowait()` to evict the stale sample; keep the `suppress(queue.Full)` around the put for races.
2. Better: replace the queue with a shared-memory latest-value slot:
   - `LatestSlot` class in a new `src/lerobot/teleoperators/xr_controllers/latest_slot.py`: fixed-layout `mp.Array('d', N)` holding `captured_at`, per-side `tracked, grip_pos[3], grip_quat[4], squeeze, trigger` and, when `full_input`, `stick_x, stick_y, stick_click, primary, secondary` and head `tracked, pos[3], quat[4]`, plus a `mp.Value('Q')` sequence counter.
   - Writer: increment seq to odd, write, increment to even. Reader: read seq, copy, re-read seq; retry (max 3) if odd or changed.
   - `VideoControllerSession.read()` returns the same dict schema and the same "never tracked" fallback when nothing has been written yet. `captured_at` must remain the worker's acquisition time.

**Tests:** new `tests/teleoperators/test_xr_latest_slot.py`:
- With a producer writing seq 1..100 rapidly and a consumer reading once, the consumer gets the last written sample (for the queue fix: put 3 samples, read once → gets the 3rd).
- Round-trip of every field for both `full_input` settings; dtype/shape match `action_features`.
- Fallback dict when empty is identical to the current one.

**Manual check:** log `time.monotonic() - action["captured_at"]` in `get_action()`; p95 should be ≤ ~12 ms.

---

## P5 — GIL contention and per-tick I/O (medium–high)

**Files:** `src/lerobot/robots/unitree_g1/g1_arm_sdk.py` (`_run`), `src/lerobot/robots/unitree_g1/g1_motion.py` (`_record`), `examples/unitree_g1/validate_xr_readonly.py` (`record`)

**Problems:** the 250 Hz arm watchdog is a Python thread using `stop.wait(period_s)` (period drifts by step duration) and shares the GIL with the main loop's IPOPT solve and the voice thread. `_record` writes a JSON row with the full observation and calls `flush()` every tick.

**Step A (do now):**
1. `G1ArmSDK._run`: pace to absolute deadlines: `next_t += period_s; stop.wait(max(0, next_t - clock()))`; if behind by more than 2 periods, resync `next_t = clock()` and increment a `missed_periods` counter exposed in `observation()` under a new key `arm.missed_periods` **only if** adding the key doesn't break `action_features`/observation contracts; otherwise expose via an attribute and log every 5 s.
2. Add `AsyncJsonlWriter` (new `src/lerobot/utils/async_jsonl.py`): background thread, bounded `queue.Queue(maxsize=10000)`, `json.dumps` done on the writer thread, flush every 1 s and on close; on overflow drop and count. Use it in `G1Motion._record` and `validate_xr_readonly.record`. `close()` must drain and flush; wire it into the existing `ExitStack` so reports are complete on Ctrl-C.

**Step B (separate PR, design note only unless asked):** run the arm publisher in its own process (spawned), exchanging target/state via shared memory (reuse the seqlock pattern from P4), with the parent still enforcing all existing checks before writing a target. Write `docs/design/g1_arm_process.md` describing the split; do not implement.

**Tests:**
- `AsyncJsonlWriter`: all rows written in order after `close()`; overflow counts; close is idempotent.
- `_run` pacing: with a fake clock and a step that takes 0.6 × period, command count over 1 s simulated ≈ 250 (± 1).
- Existing `test_unitree_g1_arm_sdk.py` stays green.

**Manual check:** distribution of intervals between arm `lowcmd` writes (from DDS timestamps) under full teleop load: p99 < 6 ms at 250 Hz.

---

## PR description checklist
- Per task: what changed, measured before/after (or "needs on-robot measurement"), and the Manual check steps.
- Explicit statement that no safety limits or validations were relaxed.