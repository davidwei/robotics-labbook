# Procedure: Quest video return plus MuJoCo control

## Agent preflight (no headset required)

1. Create a unique evidence directory and record UTC/local start times.
2. Snapshot and hash `quest_video_sender.py`, its tests, and the exact command.
3. Confirm TCP 13579 and 12345 are free; confirm the existing PC Service owns
   tracking ports 63901/60061 and no simulator/SDK probe is active.
4. Run sender unit tests and preserve the result.
5. Start desktop recording and verify its file grows.
6. Start the sender on `0.0.0.0:13579` and verify the listener.
7. Start the stock dual-UR5e MuJoCo example with scale 0.5 and no Placo view.

## Operator stages

1. Put on the Quest with both grips released.
2. Confirm the released app is WORKING with Controller and Send enabled.
3. In Camera, select `ZEDMINI`, press **Listen**, enter `10.9.0.149`, and confirm.
4. Report whether the MuJoCo desktop view appears and remains live.
5. Make one small right-grip motion, release, and reposition while released.
6. Make one small left-grip motion, then release.
7. If comfortable and all prior stages pass, make one short bimanual motion.
8. Release both grips and report any freeze, image breakup, discomfort or
   unexpected arm motion.

## Stop and preserve

1. Close the remote camera window or exit the Quest app.
2. Stop the simulator and independently check its recorded PID.
3. Stop the sender and desktop recording.
4. Hash logs/video/code snapshot and record the operator observation without
   upgrading it to a quantitative latency or stereo claim.
