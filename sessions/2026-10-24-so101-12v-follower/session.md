# SO-101 follower 12 V motor replacement — 2026-10-24

The operator returned to the lab and reported completing replacement of the SO-101 follower motors so that every follower joint now uses a 12 V motor variant. This is a hardware-maintenance milestone following the 2026-10-23 session, where the installed motor variants were unresolved and diagnostic voltage readings were approximately 4.7–5.1 V.

Read-only register inspection found 12.2–12.3 V at all six follower motors and 5.1–5.2 V at all six leader motors. Torque was disabled and status was zero throughout the audit. The follower motors shared 4.0–14.0 V configured limits. Five leader motors reported a 12.0 V upper limit while `wrist_roll` reported 8.0 V; this is a configuration observation, not proof of either motor variant. No commanded motion occurred.

The operator identified both saved leader and follower calibration records as stale and recalibrated both arms interactively. The exact before/after JSON files are archived and hashed. All six motor IDs remained 1–6 on both arms. The follower offsets changed substantially after motor replacement; captured spans changed by +50, −16, −116, −309, 0 and −83 counts in joint order. These are calibration observations, not evidence that tracking or recovery behavior is validated.

The controlled repeat is now ready for an operator-started physical trial. The exact revision `3cb506d168e4a36d580ac33a70f1711d7b98459e` is checked out cleanly in an isolated LeRobot 0.4.4 environment. Forty-nine focused tests and Ruff passed. Frozen calibration files match motor-side registers; read-only hardware checks found zero status, disabled torque, follower P/I/D 16/0/32 and the expected voltages. The intended folded rest pose was captured and the final offline runner check passed. See [repeat-preflight.md](repeat-preflight.md).

Next: start one supervised minimum-useful trial, inspect initial state before Space, move gently without deliberate obstruction, and preserve the generated telemetry. The first powered motion remains a separate operator action.

Capture is partial and live. The replacement itself was not observed by the recording agent, and there are no photos, serial-number inventory, or post-replacement motion artifacts yet.

