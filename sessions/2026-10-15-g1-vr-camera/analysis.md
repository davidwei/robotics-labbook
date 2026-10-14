# Camera streaming performance — 2026-10-15

Operator reported no regression. Log analysis qualifies this as functional validation,
not validation of a 30/60/90 FPS stream. No older session was quantitatively compared.

The two connections began at 00:28:58 and 00:30:04 local time. Their complete
ServerFrameData traces contain 1,078 and 176 consecutive frame numbers, respectively.
Decoding uses each ETLI file's embedded schema, little-endian packed fields and
two-byte type/version headers; every blob decoded without unknown types or trailing
bytes. SDK capture totals are 1,080 and 177: the final 2/1 captured frames lack
ServerFrameData records, so their transmission cannot be established at teardown.

| Metric | First connection (~60 s) | Reconnect (~9 s) |
|---|---:|---:|
| Server transmit cadence from timestamp deltas | 17.93 FPS | 18.88 FPS |
| Encode duration mean / p95 | 70.68 / 86.53 ms | 68.72 / 77.23 ms |
| Transmit interval p95 / max | 88.90 / 250.19 ms | 82.35 / 97.09 ms |
| Encoder input drops reported | 0 | 0 |
| Packet loss feedback maximum | 0.85% | 0% |
| RTT feedback mean / max | 8.09 / 48 ms | 13.85 / 32 ms |

First-session complete five-second windows range from 15.8 to 19.0 FPS. The rm_fps
field stays at 90 despite observed transmission cadence; it must not be interpreted
as achieved FPS. Encoder resolution is 4096x4032 in both traces, despite the source
camera being 640x480. StreamSDK initializes V4L2VideoEncoder on Orin.

No gaps occur within recorded server frame-number sequences, and encoder input drop
counters are zero. These do not prove that every captured camera frame reaches the
headset or that every transmitted frame is decoded/displayed. Packet feedback shows
low loss, not globally zero loss. Reader-side latest-frame replacement, final frames
at disconnect, and headset presentation losses are separate mechanisms.

Hypothesis: server rendering/encoding/scheduling at this large output resolution
limits throughput more than Wi-Fi loss in this run. Encoding duration can include
pipeline/queue time; it does not isolate pure hardware encoder execution. The
one-second encode waits in the runtime log occur around disconnect, so they are
not evidence of one-second stalls during ordinary connected playback.

Recommended next experiment: reduce requested streaming resolution, keep camera and
codec fixed, and compare sustained transmit cadence and encode durations over a
longer connected run. No settings changed during this analysis. Long-run thermal
sustainability and headset end-to-end latency remain unmeasured.

Raw logs and analysis scripts are preserved locally; hashes are in
[streaming-evidence.json](streaming-evidence.json).

## Lower-resolution follow-up

Operator ran the lower-resolution test. The successful connection at 00:40:41
negotiated 1280x1152 encoded output with target 90 FPS. A 52.15-second live prefix
contains 2,253 consecutive ServerFrameData records: 43.18 transmit FPS, encode
mean/p95 20.29/22.16 ms, transmit interval p95/max 31.64/94.72 ms. Complete five-second
windows range 37.4–45.8 FPS (42.6–45.8 excluding the first window). Encoder input
drops and packet-loss feedback are zero in this prefix. This is about 2.4x the
baseline throughput; it supports a resolution-dependent server-side bottleneck.
It does not establish 90 FPS, headset displayed FPS, or long-run sustainability.

At 00:40:35, an earlier connection failed with an old 4096x4032 input exceeding the
new 1280x1152 encoder maximum. Preserve this resolution-switch failure separately
from successful steady playback. Exact per-eye UI entries were not observed.
The parser encountered a partial last record while the trace was being written;
metrics exclude that record. See lowres-evidence.json and RUN-20261015-004.

## Extended low-resolution stability and 720p capture

A complete-record snapshot spanning 390.54 seconds (~6.5 minutes) of the same
1280x1152 encoded connection contains 16,708 consecutive ServerFrameData records,
with no decoder/parser errors or frame-number gaps. Mean transmit rate 42.78 FPS;
encode mean/p95/max 20.29/22.33/31.93 ms; transmit interval p95/max 32.57/94.72 ms.
Encoder-input drops remain zero. Packet-loss feedback mean is 0.0041%, max 1.39%
(sampled feedback values, not an aggregate packet-loss calculation); mean/max RTT
7.54/31 ms. First six complete minute rates are 43.18,40.72,44.13,44.55,46.23,43.83
FPS. The last ~40 seconds fall to ~31 FPS; therefore continuous streaming is
verified but uniformly sustained 43 FPS is not. No thermal cause established.
No headset presentation counter or quantitative end-to-end latency was measured.

After preserving the baseline, camera publisher PID 6625 was stopped with SIGINT.
1280x720@30 was rejected by LeRobot because the device reported 15 FPS. V4L2
advertises only YUYV: 640x480 up to 30, 1280x720 up to 15, 1920x1080 up to 8 FPS.
USB topology reports this camera on bus 1 port 3 at 480M (USB 2 speed). This limits
the current connection; it is not the camera's maximum capability on USB 3.

1280x720@15 subsequently started successfully on the same frame channel; metadata
and saved image confirm actual dimensions. Viewer reports live. Visual comparison
shows more peripheral scene at left/right in 720p, consistent with a wider FOV;
this is not a calibrated angular measurement, and captures are not simultaneous.
The viewer retains a 640x480 texture and aspect-preserving letterboxing, scaling
720p to 640x360. Thus this is a capture/framing check, not full-720p headset detail.
Camera and viewer are left running for operator inspection; no DDS/motion used.

Next: operator review of wider framing; for 720p30 or higher, verify a USB 3
connection and re-enumerate camera modes. Full-detail streaming also requires
reviewing viewer texture dimensions independently of per-eye encoded resolution.

## Discrete button delivery through the latest-value slot

Code-derived finding: controller buttons are held/not-held states in the same
latest-value sample as continuous poses. If the producer writes pressed=True and
then False before the consumer reads, the intervening press is overwritten and
may never be observed. The validation consumer polls at 30 Hz; this does not
impose a universal minimum press duration because scheduling and producer cadence
vary. No deliberate short-pulse loss experiment has been performed.

Potential losses before PC2 acquisition (headset polling, transport, runtime
buffering) remain unverified; do not attribute every missed press to LatestSlot.
Locating losses requires transition traces at headset, local acquisition, and
consumer. captured_at is assigned on PC2 after session.step returns, so sample-age
statistics cannot measure headset sensing/network/runtime delay before retrieval.

Proposed guidance: a one-second hold gives repeated opportunities for ordinary
button state delivery, but is not a delivery guarantee. Prefer “hold until
acknowledged” with clear visual/audio feedback. For stop or other safety-critical
commands, preserve discrete events until handled (latched event or acknowledged
queue) rather than rely solely on hold duration. Continuous poses should retain
latest-value semantics. Event transport itself does not replace independent stop
and fault handling. This is a proposed design improvement, not implemented or
physically validated by the current exercise.

## Headset HUD observation during endurance

Operator reports Pose-to-Render ~100 ms. SDK definition: interval between sending a pose to the server and rendering the received frame. Source: https://docs.nvidia.com/cloudxr-sdk/apis/cloudxr-js/latest/api/CloudXR/enumerations/MetricsName.html#posetorendertime . This includes the streaming/rendering round trip, unlike PC2 post-acquisition sample age. Do not add the two metrics or subtract one from the other as disjoint stages. Does not establish camera exposure-to-display latency, actuator response, or physical screen scan-out. Local client source smooths this metric through MetricsTracker (default window 20); deployed exact averaging configuration was not independently verified. No screenshot or raw HUD samples captured.

## Completed 10-minute combined endurance

See RUN-20261015-008 and endurance-final-evidence.json. All six 2-second faults
recovered; timestamp validation rejected stale samples during controller publication
suppression. This does not validate downstream actuator stop behavior. 15,065 of
17,938 reads were fully tracked; continuous all-device tracking for the entire run
is not established, and untracked intervals must not be silently excluded from
reliability claims. Freshness percentiles explicitly select fully tracked, accepted,
non-injected-fault samples: median/p95/p99/max 13.57/31.94/38.50/58.99 ms.

Worker interval median/p95 22.72/37.81 ms. Stage p95: camera update 22.59 ms,
render 23.42 ms, controller acquisition 13.22 ms; consumer read 0.44 ms. Stage
percentiles must not be added. These observations support investigating coupled
video/acquisition scheduling rather than blaming shared-memory read cost alone.
GPU utilization median 60%, p95 96.5%, max 99%; GPU temperature max 49.41 C over
the telemetry capture (includes startup). No thermal throttling diagnosis follows
from temperature alone. Camera totals include pre-run waiting. The camera's final
KeyboardInterrupt is expected SIGINT cleanup, and XR session cleanup logged
XR_ERROR_SESSION_NOT_STOPPING before successful harness cleanup.


## Physical preparation and return review (end of session)

### Observations and change audit

RUN-009 failed before VR following: commanded-versus-measured joint error, not
headset tracking. Preparation then had no gravity feedforward and a 0.03 rad guard.
RUN-010 changed both feedforward and preparation tolerance, so the repeat does not
isolate their individual effects. PD load offsets and transient lag are plausible;
no steady-state model fit or torque calibration establishes the cause conclusively.
Planned model gravity torque peaked at 4.35 Nm, below the 5 Nm feedforward cap.
The successful zero-target progression did not prove completion of bent-ready pose.

Preparation/following state was decoupled from the feedforward flag so gravity
compensation can remain enabled without selecting the following velocity guard.
The later 0.025 rad preparation arrival tolerance is software-tested only. A proposed
0.05 rad/s preparation rate was discussed but **not implemented**; target progression
remains 0.02 rad/s. Normal quit still uses non-preparation guards, and tripped the
0.10 rad/s velocity threshold on the return attempt. This requires a transition
review, not automatic widening of every guard encountered. The exact physical
response to the final stock handback has no operator confirmation in this record.

### Upstream source check

Reviewed live upstream G1_29_ArmController.ctrl_dual_arm_go_home in
https://github.com/unitreerobotics/xr_teleoperate/blob/main/teleop/robot_control/robot_arm.py
and the caller in teleop_hand_and_arm.py. Local checkout inspected at
278a3dcc669eb54b0fd5ed26031e420bc7f42e88. Home targets are zero joint angles;
it waits for all measured angles below 0.05 rad, checking up to 100 times at
50 ms intervals. In motion mode, authority weight then decreases from 1 to 0 in
101 increments separated by 20 ms (~2 s). The torque-zero assignment is commented
out. Home target movement uses the existing clipping limit; the fade alone is not
an explicitly slow, collision-checked home trajectory. If home tolerance is never
met, that loop does not execute its fade. The main application invokes home return
in finally. This is source review, not physical validation of upstream behavior.

Our guarded G1ArmSDK._release_authority writes zero authority immediately (three
messages); the watchdog reaches this path on guard faults. Our separate reference
adapter already has a normal-home/fade implementation, but no further development
of that adapter is requested. The required improvement belongs in the guarded
lifecycle. Normal requested exit, tracking pause, recoverable input loss, hardware
fault and process/transport loss need explicit, distinct policies. Do not assume
that slower authority fading limits stock-controller speed or preserves clearance.

### Operator decision and next verification

Operator emphasized return to stock as a recurring safety concern. Promote this
above new VR features and performance tuning. Define observable criteria for a slow
return path, settled arrival, monitored authority fade, cancellation/holding, and
what to do when valid feedback is unavailable. Test normal and interrupted handover
in software first, then as a separate gantry experiment. Retain independent emergency
control. Hardware E2E stays pending until the transition is validated. TTS status
3104 also needs investigation; audio-service acceptance alone does not establish
operator audibility. No new physical test is authorized by the labbook task.
