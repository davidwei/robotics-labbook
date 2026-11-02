# G1-29 PICO voice/controller dry rehearsal — 2026-11-03

The session added a headset-first PICO workflow so calibration and controller
rehearsal no longer require returning to the terminal. SONIC revision
`20105809c6339ea1215542615e146f975c94081c` provides ten-second tracking prompts,
an upright/fresh/moving input gate, A+B arming with full release, and spoken
next actions for four-button start/stop and A+X POSE transitions. Unitree English
TTS uses the G1 head speaker through DDS on `enP8p1s0` with speaker ID 1.

No SONIC deployment, whole-body recorder or robot policy process ran. Dry-run
suppressed manager-state, policy, planner and POSE output; `packets.jsonl` and
`packets.bin` remained zero bytes. The operator completed the full controller
sequence: A+B arm, A+B+X+Y start, A+X enter POSE, A+X leave POSE and A+B+X+Y
stop. Focused software tests passed (5 tests).

The PICO stream repeatedly initialized with tracked knees bent while the operator
reported physically straight knees. Other intervals were frozen, intermittent or
disconnected. After recalibration, the gate passed. The five seconds immediately
before the accepted A+B chord contained 320 samples over 4.988 seconds, maximum
device gap 35.634 ms, minimum left/right tracked knee angles 163.77/160.71 degrees
and changing pose content. The full capture combines multiple attempts and has a
25.264-second maximum gap; it must not be treated as one continuous passing window.

This supports a mandatory rule for every physical policy run: confirm that the
tracked skeleton matches the operator's physical posture immediately before
arming. Bent, frozen, stale, disconnected or mismatched tracking invalidates the
arm state and requires recalibration. The observation strengthens an input-side
explanation for the earlier unexpected leg tuck but does not prove the cause of
RUN-20261030-004 because that run lacked aligned raw PICO input.

Next: run a new timestamped input-only capture with the revised prompt wording
(`PICO tracking reports...`). Review the gate evidence, then separately prepare
and authorize any gantry-protected robot policy run.
