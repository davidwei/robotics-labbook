# G1-29 XRoboToolkit calibration-suite capture and replay split

**Session:** SESSION-20261119-001 · **Related experiment:** [EXP-20261115-001](../../experiments/EXP-20261115-001/plan.md) · **Architecture:** [IDEA-20261116-002](../../ideas/IDEA-20261116-002/README.md) · **Status:** calibration observations and motion traces captured; transform not solved

## Objective and result

Exercise the grouped Meta Quest Pro / Touch Pro calibration workflow, preserve static controller poses without requiring grip engagement, and separate their review from dynamic G1-29 MuJoCo trajectory replay. No physical robot or physical DDS process was used.

The complete suite passed. It contains ten static calibration anchors covering four arm-position units and six unilateral motion traces. Every selected static anchor contains about 299 samples over five seconds at about 59.7 Hz, including headset and left/right controller position, quaternion orientation and tracking state. Grip remained released for static anchors by design. The immutable anchor set stores representative poses for all ten anchors and explicitly reports `complete_observation_set_transform_not_yet_solved`.

All six dynamic traces passed a later independent validation: left/right forward, outward and upward motion were 0.470–0.949 m on the instructed side, with the opposite side limited to 0.025–0.040 m. These checks establish usable recorded XR observations and trajectories, not a calibrated mapping to G1 end-effectors.

## Development and diagnostics

The original script 3 replayed static no-grip anchors through the normal clutch guard, so the MuJoCo robot correctly remained still. A passive-viewer shutdown race also produced `corrupted double-linked list` after a completed static replay. Integration commit `7e60a7a` waits for the MuJoCo passive-viewer thread before disconnecting the simulation target; the exact previously failing visible replay then exited normally.

Integration commit `f4393fc` replaces the combined replay command with:

- `03a_view_calibration.sh`: one 4×6 posture/orientation matrix. Ten available cells show both controllers relative to the headset and their RGB local axes; fourteen combinations not present in the plan remain blank. The view is also saved as SVG.
- `03b_replay_trajectories.sh`: selects only the six dynamic traces by default and replays them through the normal grip guard and G1-29 MuJoCo path.

Software verification passed: shell syntax, 16 focused tests, rendering the real ten-anchor set to SVG, and independent validation of all six selected motion traces. The generated view was inspected for matrix population and OpenXR Y-up projection. Operator visual acceptance of the interactive window remains pending.

## 2026-11-20 offline G1 retargeting preview

Integration commit `785629f` extends script 3a with a second tab and saved SVG
for native G1-29 robot views. The diagnostic uses
`calibration-down-inward` as the clutch-relative reference, applies a virtual
two-hand grip only inside the offline preview, repeatedly evaluates each static
anchor through the production retargeter/IK until convergence or a stable
bounded result, and renders the resulting joint target in native MuJoCo. A JSON
report preserves joint targets, iteration counts, IK status and residuals.

The real ten-anchor set produced one converged cell: the reference anchor with
effectively zero residual. All nine other cells ended `bounded_best_effort`.
Their maximum per-hand position residuals ranged from 0.633 m to 1.015 m. This
is direct software evidence that the raw static observations cannot be treated
as calibrated robot targets under the present unit-scale, uncorrected-frame
mapping. It does not distinguish the contributions of scale, axis/frame,
controller-to-palm offset and robot reachability. Seventeen focused tests,
headless native rendering, embedded-image SVG conversion and the interactive
two-tab launch path passed; operator visual review remains pending.

Subsequent quantitative review found that the rendered postures do not match
their annotations. Forward maps mainly down/left, horizontal is asymmetric, and
upward remains below the shoulders while shifting left. Palm directions cannot
be validated because neither the XR-to-robot rotation basis nor palm-frame
offsets are implemented. The reference convergence is only a zero-relative-
motion result. Measurements, proposed axis mapping and isolation tests are in
[analysis.md](analysis.md).

## Evidence-supported interpretation and next action

The data needed for a human/XR calibration solve is present: time-series and representative headset/controller positions and orientations. The current visualization verifies recorded posture distinctions, but it does not solve the headset/body frame, controller-to-palm offset, workspace scale, or human-to-robot transform; it therefore does not validate G1 IK pose correspondence.

Next: run `03a_view_calibration.sh` interactively for operator review of both
tabs, then implement and quantitatively test the human/XR calibration solve
against the preserved residual report. Continue using
`03b_replay_trajectories.sh` for dynamic replay. Physical G1 motion remains
unauthorized and outside this session.

## 2026-11-20 shared calibration and offline hardware replay verification

The [plugin calibration implementation](https://github.com/MoissanClub/lerobot_teleoperator_g1_vr/commit/e29a85b) now supplies the shared profile for [03a, 03b, 04 and the new 05 replay scripts](https://github.com/MoissanClub/unitree_g1_lerobot/commit/f7d951e). Each script can reconstruct the profile from the accepted anchor set and robot model independently. 05a and 05b generate offline plans by default.

On the recorded suite, all ten static anchors produced identical Cartesian and joint targets in the simulation and physical-plan paths. All 598 frames of right-up agreed for Cartesian targets, joint commands and grip state. Motion plans were generated for all six trajectories. The focused lab suite passed 29 tests and the plugin suite passed 111. The executor was exercised with a simulated SDK backend.

These comparisons establish reproducibility of desired targets. Operator review of anatomical correspondence in 03a, live headset verification in 04, and measured tracking on physical hardware remain pending. No physical motion was performed.
