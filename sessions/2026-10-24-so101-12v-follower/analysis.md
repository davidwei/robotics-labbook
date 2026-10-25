# Post-lab review

## Direct observations

- All six follower motors received 12.2–12.4 V; the leader received 5.1–5.2 V. Initial torque was disabled and status was zero.
- The first post-replacement powered hold reproduced follower `elbow_flex` status 32 before Tracking. A report-only repeat reproduced the condition: the flag cleared with torque off, returned after power-on and persisted until shutdown.
- Motor ID 3 passed repeated unloaded isolated tests at torque limit 200, including two approximately 45-degree moves with correct encoder direction, low current and status zero.
- Two operator-provided spare model-777 servos did not move at torque limit 200. Their status remained zero; higher-torque comparison was not performed.
- After motor 3 reinstallation, the operator observed elbow movement during full follower recalibration. The new file matched all six motor registers; the final read-only snapshot had torque disabled and status zero.

## Change audit

- Revision `c5ce05ec2e649132f5546631f108b02fa7d23c37` changed the experimental motor monitor from state-changing to report-only. Sixty focused tests and Ruff passed. This control/safety-sensitive change was exercised during a powered diagnostic but has not been validated during post-reinstall Tracking.
- Revision `c779a6c23cdc00694fe99243d874f60a916c193a` separated pickup-exit tolerance from startup/tracking alignment and set rotary pickup exit to 15 degrees. Sixty-two focused tests and Ruff passed; physical validation remains pending.
- The full follower calibration changed after motor 3 horn reinstallation. Its current hash is `5de187e0901e4f394eae8affdacca9388f60f013b824dd7067a1bfc5eab8f4df`. The prior rest pose is invalid because it is bound to the previous calibration hash.

## Interpretation

The evidence strongly supports that motor ID 3 is capable of normal unloaded motion and was not simply a dead servo. The earlier installed-joint overload correlated with the old horn/calibration geometry and preferred folded pose. Successful motion during recalibration after reinstallation is encouraging, but it does not establish that sustained powered holding in the folded pose is safe.

Crossing the old 94.90-degree calibrated elbow boundary was not proof of geometric hard-stop contact because the operator intentionally used a conservative calibration endpoint. The preferred folded rest remains a design constraint that may need separate parked-rest behavior, mechanical support or torque management.

The two spare failures at reduced torque do not establish that both spares are defective. Breakaway torque, stored condition, internal configuration or mechanical stiffness remain competing explanations because normal-torque tests were not performed.

## Next lab tests

1. Inspect and confirm the reinstalled elbow horn/coupler is tight and the linkage moves freely with torque off.
2. Capture a new preferred rest pose using calibration hash `5de187e...`; verify all stored positions against the new bounds.
3. Run a short powered hold with status/current/load telemetry and no Tracking. Stop on status 32 or increasing sustained effort.
4. If the hold remains clear, perform a brief low-speed upstream or supervised teleoperation away from the folded pose, then recheck status and temperature.
5. Review whether folded parking should explicitly disable elbow torque rather than serve as an ordinary powered target.

## Review status

The observations and proposed interpretation are agent-drafted and await operator review. Post-reinstall teleoperation remains unvalidated.
