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
