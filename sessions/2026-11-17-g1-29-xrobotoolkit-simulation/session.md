# G1-29 XRoboToolkit guided simulation workflow and live milestone

**Session:** SESSION-20261117-001 · **Related experiment:** [EXP-20261115-001](../../experiments/EXP-20261115-001/plan.md) · **Architecture:** [IDEA-20261116-002](../../ideas/IDEA-20261116-002/README.md) · **Status:** ended; high-level live milestone observed, calibration and numerical-boundary follow-up required

## Objective and result

Build a repeatable simulation-lab workflow for workstation precheck, voice-gated headset trace capture, trace validation, native G1-29 MuJoCo replay, and a timed live XRoboToolkit/controller/video test. Exercise the workflow without a physical robot and determine whether the Commit 12 candidate works end to end at a useful qualitative level.

The high-level live milestone was observed. The operator reported that controller input moved the simulated G1-29 arms and that the end-to-end control/video path worked in broad terms. The controller-to-robot calibration or frame mapping was visibly inaccurate, so pose correspondence is not accepted. The run later stopped with `ValueError: Seed exceeds joint limits`; this is a software boundary failure, not evidence against the earlier observed arm response.

The Quest video listener accepted `OPEN_CAMERA`, connected to `10.9.0.127:12345`, and sent its first H.264 access unit. The recorded stream lasted only about three seconds before the control failure and therefore does not establish sustained video reliability.

## Development completed

- Integration commit `dcdc0d1` on `feat/g1-29-vr-lab-scripts` adds five simulation-only scripts under `lab/g1_vr/`, exact terminal/headset handoff gates, slow voice guidance, trace validation, deterministic synthetic traces, native MuJoCo replay/viewer, Quest video orchestration, and continuously flushed JSONL telemetry for future failure evidence.
- Plugin commit `5017cc3` on `fix/g1-29-seed-limit-tolerance` clips a finite measured IK seed only when its joint-limit overshoot is at most `0.05 rad`, reports the clip in diagnostics, and retains a hard failure beyond that tolerance.
- The user-owned untracked integration files `tests/test_dev_workspace.py` and `tools/dev_workspace/` were preserved and excluded from the commit.

Software validation passed: 109 plugin tests with two optional skips; 14 focused real/pinned retargeter tests; 23 integration/lab tests with one optional skip; Ruff lint/format; shell syntax; real precheck including NVENC; and a 120-sample artificial bimanual trace validated at 60.0 Hz and replayed through native MuJoCo. Synthetic evidence is development evidence, not headset evidence.

## Evidence-supported interpretation

The session supports a qualitative G1-29 XRoboToolkit-to-MuJoCo milestone: input, grip-mediated control, simulated arm response, viewer, and Quest video transport were active in one guided workflow. It does not yet support calibrated pose mapping, quantitative accuracy/latency, a complete 60-second live pass, reconnect behavior, CloudXR equivalence, G1-23 support, or physical-robot safety.

The next high-information work is headset-free analysis of the recorded/raw coordinate conventions and a deliberate calibration trace suite before repeating the short live run at plugin `5017cc3` and integration `dcdc0d1`. Calibration correction and the small seed-limit tolerance are separate issues and should remain separate commits/findings.

