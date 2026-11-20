# Post-lab analysis — annotation versus retargeted G1 posture

Reviewed 2026-11-20 from the accepted anchor set and the retargeting report
generated at integration `785629f`. This analysis distinguishes direct
measurements from proposed causes and corrections.

## Direct observations

The preview does not reproduce the requested posture labels:

| Requested row | Actual G1 end-effector result relative to each shoulder | Assessment |
| --- | --- | --- |
| Arms down | Reference joint pose points about 0.250 m forward and 0.197 m down, with only about 0.048 m lateral displacement per arm. | A diagonal zero pose, not an independently solved or verified natural-down/palms-inward pose. |
| Arms forward | Across all four palm subphases, X displacement falls to 0.022–0.093 m, both hands move toward robot-left by 0.194–0.289 m, and hands remain 0.331–0.349 m below the shoulders. | Not forward; predominantly down and left, with the right arm crossing inward. |
| Arms horizontal | Left-hand shoulder-relative X is -0.222 to -0.206 m while right-hand X is +0.275 to +0.284 m; both Y values are positive and Z remains -0.256 to -0.159 m. | Not a symmetric horizontal T-pose; left/right behavior is asymmetric and both hands are left-biased. |
| Arms upward | Both hands remain below the shoulders by 0.171–0.176 m and are displaced 0.341–0.419 m toward robot-left. | Not upward. |

Only the down/inward reference cell converged, with effectively zero residual,
because the clutch-relative controller assigned that observation to the current
zero-joint robot pose. The remaining nine cells were `bounded_best_effort`, with
maximum per-hand position residuals from 0.633 m to 1.015 m and substantial
orientation residuals. Convergence of the reference does not validate its
annotation.

Palm direction is not currently assessable as correct. The implementation
applies controller relative rotation directly to the robot end-effector without
an XR-to-robot basis conversion or a controller-to-palm / robot-EE-to-palm
offset. The G1 solver controls an abstract frame 0.05 m beyond wrist yaw; a
semantic palm normal has not been defined and calibrated.

## Proposed explanation

The code directly adds XR translation deltas to the G1 base-frame target. The
recorded data follows the expected XR convention: X is right, Y is up and
forward motion is predominantly negative Z. The G1 base convention is X
forward, Y left and Z up. Direct addition therefore maps human upward motion to
robot-left and human forward motion to robot-down, matching the observed
failure.

The likely basis conversion is:

```text
g1_x = -xr_z
g1_y = -xr_x
g1_z =  xr_y
```

This remains a candidate until checked against all anchors and the model frame.
Rotation deltas require the corresponding basis conjugation, followed by
explicit controller-to-palm and robot-end-effector-to-palm offsets. Position
also requires a calibrated human-to-G1 scale: raw changes reach roughly 0.6–1.3
m while G1 arm reach is much smaller, so unit scale is not viable. Finally, the
down/inward observation must be associated with an explicitly chosen G1
reference posture rather than assuming zero joints semantically matches the
human annotation.

## Next high-information checks

1. Apply only the candidate XR-to-G1 translation basis and inspect the four
   position rows, retaining scale 1 temporarily so axis correctness is isolated.
2. Fit and validate translation scale/offset from the four position units,
   reporting left/right symmetry and reach-limit residuals.
3. Define the robot palm frame and solve controller-to-palm offsets from the
   forward/horizontal orientation subphases; validate direction signs before IK.
4. Regenerate the same 4×6 robot grid and require row-direction agreement,
   orientation-sign agreement, bounded reach, and materially reduced residuals.

These are simulation/offline corrections only. No physical G1 motion is
authorized by this analysis.
