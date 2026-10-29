# PC2 suspended SONIC diagnostic — operating order

Scope: fully unloaded G1-29 on a rated gantry. The objective is to measure
initialization, stale-input and stop/handover outcomes with enough state to
reconstruct an unexpected motion. Loaded and untethered trials are separate
decisions. No step here authorizes a SONIC launch by itself.

1. **Inventory and clear the area.** Record G1 hardware, firmware, 29-DOF/ankle
   mode, battery and E-stop state. Verify both feet are unloaded, every limb has
   clearance, and the three-meter zone is clear. Assign a PICO operator and a
   separate safety operator who owns keyboard `O` and the facility E-stop.
2. **Identify the existing command stream.** A read-only PC2 capture at 01:01
   already observed CRC-valid `rt/lowcmd` at about 182 Hz with zero sampled body
   Kp/Kd/tau. Determine the publisher and expected ownership before introducing
   SONIC; no source was identified by the PC2 process list alone.
3. **Pin the PC2 candidate.** Record clean source revision plus any patch, the
   matched low-latency encoder/decoder/config and planner hashes, TensorRT 10.7
   version and generated engine hashes. Review the missing controller-chord latch
   fix before PICO mode transitions. This PC2 environment has not inherited the
   earlier x86 simulation pass.
4. **Prove capture before motion.** Start the independent read-only recorder
   `/home/dwei/sonic/capture_g1_wholebody.py` on `enP8p1s0` with a new output
   file and a duration long enough to cover startup, stop and post-stop. It
   records timestamped LowState, base and torso quaternion/gyro/accelerometer,
   35 motor slots, and observed LowCmd. Confirm CRC, finite 29 body q/dq,
   normal motor status, both IMUs, acceptable receive gaps, and zero recorder
   queue drops. Record synchronized robot/operator video. Enable SONIC's
   `--enable-csv-logs` and a unique `--logs-dir`; its split CSVs include base and
   torso IMU, q/dq, actions, motor status/temperature/torque and mode data.
   Also capture PICO NPZ, target motion, deployment console and mode events.
5. **Check PICO without robot commands.** Run XRoboToolkit PC Service and the
   PICO app with both ankle trackers paired, calibrated and correctly sided.
   Require `WORKING`, Full Body high accuracy and Send. In manager `OFF`, record
   at least 30 continuous seconds of finite 24-joint body frames at 50 Hz or
   better, with no frozen timestamp or gap at or above 100 ms. A sparse stream
   is reacquired without using a robot command or controller chord.
6. **Record separate motion authorization.** Reconfirm fresh LowState and torso
   IMU, exact wired interface, no unintended competing command publisher, local
   stop and E-stop roles, measured-versus-default standing pose and full gantry
   unloading. SONIC launch itself releases stock motion control and begins a
   roughly three-second 29-joint interpolation.
7. **First suspended run: initialization and local stop only.** Keep the PICO
   manager in `OFF`. Launch the pinned real deployment only under the recorded
   authorization, observe the initialization trajectory, then use local `O`.
   Abort sooner for wrong direction, rapid motion, collision, oscillation,
   motor/IMU fault, stale data or either operator's uncertainty. Leave the G1
   supported. Record the damping frame, last observed LowCmd, LowState/IMU
   evolution, active motion mode and actual post-publication behavior. Process
   exit alone is not a handover pass.
8. **Review before the next run.** Preserve the full capture, exact times,
   video, console, source/model/engine hashes and a short operator observation.
   Test PICO stop, deliberate PICO loss, streamer/process loss and the approved
   hardware E-stop procedure in separate fresh suspended runs. Stop immediately
   at a stale-input warning or unexpected motion; do not wait for autonomous
   recovery. Advance to PLANNER/POSE motion only after the controller-latch and
   fresh-input checks pass and the preceding stop outcome is understood.

The read-only capture is an independent witness through SONIC shutdown. Its first
five-second check captured about 192 LowState samples/s, not every DDS frame;
review timing gaps and completeness for each later run. The exact G1 firmware,
current LowCmd publisher and physical stop behavior remain open.
