# SO101 demo-location handoff

Preparation closed with no LeRobot process running. The last post-replay readback showed matching leader/follower calibration, zero motor status and torque disabled. Trial data remains local under `outputs/demo/so101/20261031_122309_001c2b60_run_5`, with one committed episode. Do not delete it during transport or venue setup.

Transport changes the physical evidence. At the venue, before any motion:

1. Secure arm power, serial, USB-camera and hub cabling; establish a child exclusion zone and operator-accessible power/stop control.
2. Confirm the venue's guardian/organizer consent and data-retention rules before recording video.
3. Run `v4l2-ctl --list-devices`; identify high/wide and gripper views again. Numeric indices can change after every reconnect. Update `record-linux.json` if needed and run the config check.
4. Confirm the exact task wording in `dataset.single_task`. Do not collect production training data under the placeholder camera-comparison task.
5. Perform read-only arm calibration/status/torque verification, then one short operator-authorized record/save/replay rehearsal with the workspace clear.
6. Confirm both videos, Parquet row count, telemetry drop count, camera roles and clean disconnect. Stop on any USB reset, motor status, abnormal motion, unexpected heat or save failure.

For 100 recorded children, prefer five new 20-episode sessions (`childrens_demo_batch01` through `batch05`) instead of one 100-episode session. This bounds Linux full-copy checkpoint growth and creates inspection/break points. After each batch verify exactly 20 committed episodes, preserve the session folder, inspect disk usage and motor/camera health, then start the next batch. Aggregate only after collection and schema/calibration audit.

Known venue risks: the high/wide camera previously disconnected on USB path 5-1.2 with protocol error `-71`; the pinned preview CLI requires integer camera indices; one leader motor-6 calibration read previously returned a transient input-voltage error. The successful later replay does not establish 100-child endurance.
