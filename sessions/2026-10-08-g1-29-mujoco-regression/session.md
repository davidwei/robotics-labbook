# SESSION-20261008-001 — G1-29 MuJoCo regression

2026-10-08 · David Wei + Codex · development workstation · simulation/development; review pending.

**Objective:** validate that the G1-23 embodiment changes in [LeRobot PR #4651](https://github.com/huggingface/lerobot/pull/4651) preserve the existing G1-29 MuJoCo path before further G1-23 hardware validation.

## Development state

The feature branch was reduced to one commit, rebased onto Hugging Face upstream `b863b422`, and pushed to `MoissanClub/lerobot` as `dd3d74b82832673666d6a2adb71bec18ea509219`. The implementation keeps the 29-slot DDS layout, adds sparse G1-23 embodiment mappings, shares gains by joint name, leaves G1-29 as the default, and explicitly rejects G1-23 simulation until a native model exists. Focused validation reported 75 passing tests plus clean Ruff and whitespace checks. Physical G1-23 Holosoma validation remains a TODO.

## Simulation validation

[RUN-20261008-001](runs/RUN-20261008-001.yaml) launched the real G1-29 MuJoCo environment headlessly with the DDS bridge and GR00T balance controller at zero joystick input. It completed 1,480 simulation steps in 7.807 seconds. All 29 joint position, velocity and estimated-torque observations were present and finite; all 15 GR00T lower-body outputs were finite; MuJoCo `qpos`, `qvel`, `qacc`, and `ctrl` remained finite. The controller and subscription threads stopped, and the test process exited successfully.

This supports G1-29 simulation compatibility for a short zero-input balance smoke test. It does not establish walking behavior, camera/viewer behavior, long-duration stability, or physical G1-23 behavior.

## Unresolved shutdown behavior

With image publishing disabled, disconnect logged `Error closing sim_env: 'NoneType' object has no attribute 'process'`. Inspection found the same unguarded image-publisher dereference in upstream `b863b422`; this embodiment change did not introduce it. The exception prevented confirmation that the environment's normal `close()` completed, although threads stopped and the process exited. Track this as a pre-existing cleanup defect rather than evidence against G1-29 embodiment compatibility.

## Next checks

- Repeat G1-29 simulation with a small commanded walk and quantitative base-stability criteria.
- Exercise camera publishing and viewer modes separately.
- Fix or separately report the headless disconnect guard and verify normal simulator close.
- Perform the planned tethered physical G1-23 Holosoma test with the Unitree wireless remote; no native G1-23 MuJoCo claim is possible yet.

No physical robot was actuated in this session.
