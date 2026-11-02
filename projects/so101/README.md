# SO-101 teleoperation, recovery and demo recording

Owner: David Wei. Source code: `MoissanClub/lerobot`; executed revisions, configuration and calibration hashes belong to each session/run. Status: standard teleoperation and recording/replay demonstrated; pickup recovery, warning-threshold accuracy and installed overload causes remain unresolved. No model training is established by these records.

## Objectives and ideas

- [Tracking-error warning](../../ideas/IDEA-20261022-001/README.md): audible warning demonstrated; distinguish settled servo error, dynamic lag and nonprogress before selecting thresholds.
- [Pickup/recovery and capability advisories](../../ideas/IDEA-20261023-001/README.md): prototype physically exercised, pickup incomplete; nominal gravity models and direction advisories remain approximate.
- Preserve reproducible recording/replay and a source-aware dataset inventory across host migration and camera changes.

## Sessions

- [October 23 reassembly, warning and recovery diagnostics](../../sessions/2026-10-23-so101-reassembly-warning/session.md): recalibration, audible warning, static residual and incomplete pickup; no physical recording test.
- [October 24 12 V follower maintenance/diagnostics](../../sessions/2026-10-24-so101-12v-follower/session.md): 12.2–12.3 V follower audit, pre-Tracking elbow overload, unloaded motor-3 success, failed reduced-torque spare tests and reinstallation/recalibration. Installed folded-pose hold unvalidated at closeout.
- [October 25 recording/replay preparation and rehearsal](../../sessions/2026-10-25-so101-teleop-preparation/session.md): camera-role confirmation, startup transport faults, committed 30 FPS episodes and episode-0 replay; separate 10 FPS configuration prepared. Standard launcher evidence does not validate the recovery state machine.
- [October 31 Linux migration and venue demo](../../sessions/2026-10-31-so101-linux-migration/session.md): native Linux calibration/teleop/record/replay, USB camera re-enumeration, gripper overload, later one-camera workflow and inventory of 126 committed episodes across 16 sessions (50 two-camera, 76 one-camera). Episode count is not child count, successful-pickup count or training readiness.

## Next action and limits

Preserve/back up raw recordings, audit episode/video/frame integrity and task quality, and create a separate processed dataset with an explicit strategy for missing camera views before training. Confirm mechanical freedom, fresh arm/camera identities and current calibration at the next setup. Track warning/pickup validation separately from standard demo success. Final October 31 closeout found no active demo processes; the latest recorded readback and remaining gaps are in that session, not a guarantee of present hardware state.

Use the [draft session-derived lab protocol](../../docs/lab-protocol.md) and the [session-reference audit](../../docs/session-reference-audit.md) for evidence boundaries.
