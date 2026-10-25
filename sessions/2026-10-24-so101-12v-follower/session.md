# SO-101 follower 12 V motor replacement — 2026-10-24

The operator returned to the lab and reported completing replacement of the SO-101 follower motors so that every follower joint now uses a 12 V motor variant. This is a hardware-maintenance milestone following the 2026-10-23 session, where the installed motor variants were unresolved and diagnostic voltage readings were approximately 4.7–5.1 V.

Read-only register inspection found 12.2–12.3 V at all six follower motors and 5.1–5.2 V at all six leader motors. Torque was disabled and status was zero throughout the audit. The follower motors shared 4.0–14.0 V configured limits. Five leader motors reported a 12.0 V upper limit while `wrist_roll` reported 8.0 V; this is a configuration observation, not proof of either motor variant. No commanded motion occurred.

The operator identified both saved leader and follower calibration records as stale and recalibrated both arms interactively. The exact before/after JSON files are archived and hashed. All six motor IDs remained 1–6 on both arms. The follower offsets changed substantially after motor replacement; captured spans changed by +50, −16, −116, −309, 0 and −83 counts in joint order. These are calibration observations, not evidence that tracking or recovery behavior is validated.

The controlled repeat reached a powered preflight but is now blocked. The runner entered `Idle` while commanding the saved folded rest pose, then latched a follower `elbow_flex` status 32 load-overload fault about 2.1 seconds later, before Tracking or directional testing began. Immediately before the fault, the elbow measured 103.34 degrees while the saved rest command was 94.46 degrees and the calibrated upper bound was 94.90 degrees. All other motor statuses remained zero. The runner was stopped and its complete zero-drop telemetry is archived. See [repeat-preflight.md](repeat-preflight.md).

Next: with torque off and the arm supported, inspect elbow mechanical freedom and calibration/end-stop geometry, then capture a rest pose with margin inside the safe boundary before any powered retry. The fault cause remains unresolved; do not restart the directional trial yet.

Capture is partial and live. The replacement itself was not observed by the recording agent, and there are no photos or serial-number inventory. The powered preflight is captured in telemetry, but no Tracking-phase experiment occurred.

