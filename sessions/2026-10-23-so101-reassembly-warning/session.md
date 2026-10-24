# SO101 reassembly, warnings and tracking diagnostics — 2026-10-23

Session ended; physical validation remains incomplete. Both reassembled arms were recalibrated; cameras were disconnected. The operator confirmed the short “Slow down” warning is audible. No physical recording test or pickup recovery was completed.

The instrumented 45-second free-motion run produced 1,347 joint samples, zero drops and nine warning requests/deliveries. At the experimental 2° threshold the monitor remained slow throughout; instantaneous error exceeded 2° for 99.55% of samples. Velocity-based catch-up estimates were frequently undefined or strongly dependent on the estimation window, so a reliable one-second warning threshold has not been established.

Three fixed-target checks showed approximately 3.43° persistent elbow error. The latest diagnostic confirmed the requested goal was stored, torque enabled, P=16/I=0/D=32, nonzero output/load, sampled status zero and no high-temperature pattern. The elbow was near its calibrated endpoint. These observations establish persistent tracking error, not its physical cause.

Working hypotheses are gravity/static friction under PD control and occasional mechanical limits/binding; they may coexist. The operator deprioritized inadequate supply and protection because more stretched poses had moved successfully. Supply rating remains unverified (operator expects 12 V; reported voltage register was approximately 5 V). Constant load alone does not establish a hard stop. No gains, supply or controller changes were made.

Next: characterize static residual across clear poses and inspect reachable limits; choose tolerances and distinguish dynamic lag from stalled motion; then design pickup recovery and operator-controlled recording. See [handoff.md](handoff.md) for hypotheses, proposals and next-session priorities, and [analysis.md](analysis.md) for detailed reasoning.

Software checks previously passed: 68 focused tests and Ruff. Source and workspace helpers are committed at [102be54](https://github.com/MoissanClub/lerobot/commit/102be54dfdba03ea11505ef345790d34ff370489) on `lab/so101-intel-warning-20261023`; the newer `so101demo` branch was preserved. Exact executed revisions remain in individual run records. [Private raw evidence archive](https://github.com/davidwei/robotics-labbook/releases/tag/so101-session-20261023) includes logs, telemetry, calibration and provenance.

Capture is partial: no camera video, reassembly was not directly observed, and final power/torque state was not independently verified. Historical incremental summary is retained in session-before-closeout.md.
