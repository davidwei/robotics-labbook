# SESSION-20261008-001 — G1-29 MuJoCo regression

2026-10-08 · David Wei + Codex · development workstation · simulation/development; review pending.

**Objective:** validate that the G1-23 embodiment changes in [LeRobot PR #4651](https://github.com/huggingface/lerobot/pull/4651) preserve the existing G1-29 MuJoCo path before further G1-23 hardware validation.

## Development state

The feature branch was reduced to one commit, rebased onto Hugging Face upstream `b863b422`, and pushed to `MoissanClub/lerobot` as `dd3d74b82832673666d6a2adb71bec18ea509219`. The implementation keeps the 29-slot DDS layout, adds sparse G1-23 embodiment mappings, shares gains by joint name, leaves G1-29 as the default, and explicitly rejects G1-23 simulation until a native model exists. Focused validation reported 75 passing tests plus clean Ruff and whitespace checks. Physical G1-23 Holosoma validation remains a TODO.

## Simulation validation

[RUN-20261008-001](runs/RUN-20261008-001.yaml) launched the real G1-29 MuJoCo environment headlessly with the DDS bridge and GR00T balance controller at zero joystick input. It completed 1,480 simulation steps in 7.807 seconds. All 29 joint position, velocity and estimated-torque observations were present and finite; all 15 GR00T lower-body outputs were finite; MuJoCo `qpos`, `qvel`, `qacc`, and `ctrl` remained finite. The controller and subscription threads stopped, and the test process exited successfully.

[RUN-20261008-002](runs/RUN-20261008-002.yaml) then exercised the documented `lerobot-teleoperate` path with the interactive MuJoCo viewer enabled, DDS on loopback, GR00T, and zero joystick input. It ran for 92.8 seconds and 5,532 teleoperation ticks at 59.63 Hz effective cadence; measured GR00T rates were 49.7–49.8 Hz against a 50 Hz target. David visually confirmed that the graphics were working. The process exited with code 0 after Ctrl-C. MuJoCo nevertheless wrote a numerical-instability warning at simulation time 48.4160: `NaN, Inf or huge value in QACC at DOF 0`.

[RUN-20261008-003](runs/RUN-20261008-003.yaml) repeated the graphical zero-input configuration on exact parent `b863b422`, without the embodiment diff. The baseline emitted the same QACC instability class at simulation time 88.2920 and later emitted a CTRL instability warning at actuator 0 after simulation time restarted. It completed 6,261 teleoperation ticks over 105.0 measured seconds at 59.63 Hz, then returned code 1 while reproducing the existing disconnect warning.

The matched baseline establishes that the QACC instability warning predates this PR and was not introduced by the embodiment diff. It does not establish the instability's root cause or numerical stability. Commanded walking, camera publishing, long-duration stability, and physical G1-23 behavior also remain unestablished.

## Unresolved shutdown behavior

With image publishing disabled, the headless run and both graphical revisions logged `Error closing sim_env: 'NoneType' object has no attribute 'process'`. Inspection found the same unguarded image-publisher dereference in upstream `b863b422`; this embodiment change did not introduce it. The exception prevented confirmation that the environment's normal `close()` completed. Track this as a pre-existing cleanup defect rather than evidence against G1-29 embodiment compatibility.

## Next checks

- Repeat G1-29 simulation with a small commanded walk and quantitative base-stability criteria.
- Diagnose the pre-existing QACC/CTRL instability independently of this embodiment PR.
- Exercise camera publishing separately.
- Fix or separately report the headless disconnect guard and verify normal simulator close.
- Perform the planned tethered physical G1-23 Holosoma test with the Unitree wireless remote; no native G1-23 MuJoCo claim is possible yet.

No physical robot was actuated in this session.
