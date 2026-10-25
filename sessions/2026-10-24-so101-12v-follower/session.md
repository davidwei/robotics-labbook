# SO-101 follower 12 V motor replacement — 2026-10-24

The operator returned to the lab and reported completing replacement of the SO-101 follower motors so that every follower joint now uses a 12 V motor variant. This is a hardware-maintenance milestone following the 2026-10-23 session, where the installed motor variants were unresolved and diagnostic voltage readings were approximately 4.7–5.1 V.

Read-only register inspection found 12.2–12.3 V at all six follower motors and 5.1–5.2 V at all six leader motors. Torque was disabled and status was zero throughout the audit. The follower motors shared 4.0–14.0 V configured limits. Five leader motors reported a 12.0 V upper limit while `wrist_roll` reported 8.0 V; this is a configuration observation, not proof of either motor variant. No commanded motion occurred.

The operator identified both saved leader and follower calibration records as stale and will recalibrate both arms interactively. The stale files are preserved as pre-calibration baselines. The exact new calibration JSON files must be archived and hashed before repeating the 2026-10-23 directional-advisory experiment. Recalibration is a required setup change, not evidence that tracking or recovery behavior is validated.

Next: complete both calibrations, archive the generated files, and verify their motor IDs/ranges. Then reproduce the prior experiment at source revision `3cb506d168e4a36d580ac33a70f1711d7b98459e`, preserving the new calibration hashes and the 12 V follower setup as provenance. Treat the first powered motion as a separate, explicitly authorized run.

Capture is partial and live. The replacement itself was not observed by the recording agent, and there are no photos, serial-number inventory, or post-replacement motion artifacts yet.

