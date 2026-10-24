# Directional advisory trial review — 2026-10-23

Physical validation remains incomplete. Operator reports a completed round; robot motion is inferred from telemetry, with no camera/video or explicit obstruction observation. No further actuation or code changes during review.

## Provenance and run outcome

Executed code `3cb506d168e4a36d580ac33a70f1711d7b98459e` on `lab/so101-intel-warning-20261023`. Log: `state-machine-1792821195498577000.jsonl`; 3,885 samples over 144.14s, 1,295 monitor reports, 7,444 submitted/written records, zero dropped. Maximum sample gap .0385s. Configuration, calibration hashes and monitor settings embedded in metadata.

[Private complete log archive](https://github.com/davidwei/robotics-labbook/releases/download/so101-session-20261023/so101-direction-trial-1792821195498577000.tar.gz), SHA256 `b30a4bec8f1fd71d4e261d48fbc8312df23ca9ab5f0059038c24ef67ae2c9fa6`.

| Elapsed | Transition | Reason |
|---|---|---|
| 9.89s | setup_hold → Returning to rest | S |
| 20.18s | Returning to rest → Idle | Rest dwell |
| 23.95s | Idle → Lagging | Space |
| 32.22s | Lagging → Tracking | Alignment dwell |
| 38.87s | Tracking → Lagging | Sustained error |
| 63.13s | Lagging → Awaiting alignment | Elbow nonprogress |
| 126.49s | Awaiting alignment → Fault | One nonzero gripper Status reading |

There was no successful pickup resume. At the closest observed simultaneous alignment, about 67.61s, errors still included shoulder pan -5.49°, shoulder lift +4.22°, elbow -5.45°, wrist roll -2.29°, exceeding 1.5° tolerances. This supports the operator's pickup-usability concern; the held follower target can also settle under load. Normal tracking was achieved once, for approximately 6.65s.

## Before elbow recovery

| Time before recovery | Leader elbow | Sent elbow goal | Follower elbow | Follower shoulder lift |
|---|---:|---:|---:|---:|
| 8s | 30.11° | 30.15° | 40.75° | -50.37° |
| 6s | 17.63° | 21.66° | 33.10° | -39.82° |
| 4s | 11.12° | 11.70° | 22.20° | -29.19° |
| 3s | 10.77° | 10.76° | 22.20° | -24.26° |
| 2s | 10.59° | 10.60° | 22.11° | -18.02° |
| 1s | 10.51° | 10.49° | 21.76° | -13.01° |
| At recovery | 10.33° | 10.32° (previous command) | 21.67° | -8.18° |

The elbow was not entirely stationary: it improved only .527° over approximately four seconds, insufficient for the .5° per ~1s progress requirement. Error against leader was 11.34° at entry. Recovery replaced the goal with measured-pose holding; subsequent lack of convergence toward the previous goal is not evidence that it remained physically unreachable.

Last-three-second elbow readings: load 508–524, current 85–97, voltage 47–48, temperature 27 raw; torque-enable=1 and status=0 in all buffered samples. No calibrated-boundary cause. These readings show sustained effort with poor response, not confirmed physical torque saturation.

## Monitor behavior and directional-advisory limitation

Before recovery, predicted elbow gravity declined approximately .410→.371Nm as the configuration changed. Last active report: current gravity .3709Nm, requested-pose .4004Nm; nominal 7.4V holding utilization .8165, 12V .4083. Shoulder current/requested estimates .3988/.4289Nm, 7.4V utilization .8746. Both had general possible_load_boundary advisories near recovery; nominal models disagree.

**No direction-specific advisories occurred, and no independently tested direction was marked restricted.** The implemented combination of a 2° trial step and a >.01Nm increase threshold is too insensitive at this pose: the largest 2° perturbation increases shoulder demand by only .00795Nm and elbow demand by .00590Nm. Thus the absence of directional warnings does not validate reachability. A finite full requested-pose change can trigger the general load advisory while all tiny direction probes fail the increase gate.

No empirical saturation signature was established: demand did not continuously grow against flat output in the required pattern. That is distinct from nonprogress, which still triggered recovery. Gravity/PD static error remains plausible; actual ~4.7–4.8V operation and uncertain model gains prevent a torque-limit conclusion.

## Later gripper fault

At 126.49s, sampled gripper Status=1 once, with all torque-enable readings still 1. Previous and following status polls were zero. The controller latched Fault as designed. Nearby gripper voltage samples were 50–51, current 0–1, temperature25 raw. Registers were not sampled simultaneously, so this does not exclude a short transient. Specific status-bit meaning/physical cause is not established in this review; do not label it overheating, overload or confirmed undervoltage. No Tracking resume occurred before exit.

## Next actions

1. Resolve directional prediction scale: use a gravity gradient with a noise tolerance appropriate to the step, or a longer speed/time-based horizon with intermediate whole-arm checks. Preserve model uncertainty and unloading directions. Do not merely interpret zero warnings as success.
2. Improve pickup/recovery ergonomics; proposed operator-enabled retrace-following remains unimplemented. Keep fault recovery separate.
3. Investigate the single gripper status event by logging motor-side voltage limits/configuration and correlated timestamps before altering fault handling.

No thresholds or fault policies changed during this analysis. Root cause remains unvalidated.

## Status interpretation follow-up

Verified supplier ST memory-map documentation identifies address65 bit0 (Status=1) as voltage outside configured range, either overvoltage or undervoltage: https://docs.waveshare.com/Memory_Map_Explanation/ST_Servo_Memory_Map_Explanation . This supersedes the earlier statement that bit meaning was not established. The local SDK also names bit1-value voltage error, but packet error-byte semantics must not substitute for the register-specific table. One isolated gripper voltage-status reading does not identify whether the event was high/low voltage, transient or configuration-related; nearby 5.0–5.1V samples are not simultaneous.

Recommended future policy, not implemented: distinguish faults by decoded type; first voltage event immediately suspends tracking/new target advancement and triggers prompt fresh status/voltage confirmation; isolated cleared event remains logged, persistent/repeated events latch Fault. Do not continue unrestricted following while confirming, automatically return home, disable torque indiscriminately, or silently ignore repeated transients. Confirm actual min/max voltage registers and installed variant before tuning thresholds. Current controller still latches on any nonzero sampled status.
