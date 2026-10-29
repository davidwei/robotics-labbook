# G1-29 setup checklist for PICO/SONIC

Status: pre-lab setup specification. No command in this document authorizes robot
motion. Launching the real SONIC deployment is itself a motion event because the
controller immediately performs a three-second initialization interpolation.

2026-10-30 operator update: SONIC and XRoboToolkit were installed in a local
workspace on G1 PC2 for a feet-clear initialization/stop diagnostic followed,
if separately authorized, by gantry-protected contact tests. This is a
new environment relative to the x86 topology recommended below. The current
[PC2 operating order](../../sessions/2026-10-30-g1-sonic-pc2-suspended/in-lab.md)
controls that diagnostic. Stale input and unknown stop/handover block loaded and
untethered trials; full suspension permits measuring them under separate motion
authorization and independent whole-body IMU/state/command capture.

## Recommended topology for the first trial

Use the already-tested x86_64 GPU workstation for the C++ SONIC deployment and
PICO streamer. Connect the workstation to the G1 over wired Ethernet on the
`192.168.123.0/24` robot network. Connect the PICO and workstation to the same
private low-latency Wi-Fi network for XRoboToolkit. Do not move the deployment onto
the G1 onboard computer for the first trial; that would introduce a second software
environment before the offboard path is characterized.

The G1 onboard computer only needs its normal Unitree DDS and motion-switcher
services for this offboard profile. Camera software is not required for this demo.

## Firmware and hardware compatibility

The NVIDIA repository does **not** specify a minimum or approved Unitree G1 system
firmware version. It also does not publish a matrix mapping SONIC checkpoints to G1
pelvis/motor-driver revisions. Do not update or downgrade the robot solely to match
an invented requirement.

Before physical launch, record from the Unitree UI, robot labels and onboard system:

- marketed G1 variant and 29-DOF confirmation;
- robot serial number and manufacture date;
- pelvis/hardware revision and visible mechanical differences;
- main system/control firmware version and update date;
- onboard image/OS and Unitree service versions;
- motor/driver revision if exposed;
- `mode_machine`, ankle mode and whether the robot uses the PR configuration
  expected by the deployment;
- hand type and whether Dex3 services are present;
- battery firmware/state and hardware E-stop behavior.

This is a hard compatibility gate. NVIDIA issue
[`NVlabs/GR00T-WholeBodyControl#23`](https://github.com/NVlabs/GR00T-WholeBodyControl/issues/23)
contains multiple user reports that newer G1 hardware introduced around fall 2025,
described as changed pelvis/drivers, fell backward under an earlier WBC stack. The
thread does not publish a resolved firmware or compatibility recipe. Treat it as a
risk signal requiring identification and suspended validation, not proof that this
specific robot is incompatible.

The code contains actuator comments distinguishing old and new hip motor choices,
but those comments are not a runtime hardware detector. A successful prior G1-29
run under another controller also does not establish compatibility with SONIC's
gains, action scaling and policy.

## Required workstation software — offboard profile

Use one pinned, clean physical-candidate revision. The simulation used repository
revision `1fa5f7fa3966cbd4845c4e641d13c3f0cd5b0d9b` with three local compatibility
changes; these must be reviewed, tested and committed before becoming the physical
candidate.

Required by NVIDIA's deployment documentation:

| Component | Required for this profile | Current evaluation state |
|---|---|---|
| OS | Ubuntu 20.04, 22.04 or 24.04 x86_64 | Ubuntu 24.04.5 x86_64 |
| NVIDIA GPU/driver | CUDA-capable GPU with working driver | Two RTX 5090 GPUs and driver 595.99.02 were previously observed; recheck before lab |
| CUDA toolkit | Compatible CUDA toolkit and headers | CUDA 12 toolkit is installed; exact physical-candidate runtime must be captured |
| TensorRT | **10.13 exactly** for x86_64 desktop | Local 10.13.3.9 used successfully |
| Build tools | CMake, C++ compiler, Git LFS, `just`, repository dependencies | CMake 3.28.3 and GCC 13.3 present; rerun environment check |
| Unitree transport | Bundled Unitree SDK2/CycloneDDS | C++ SDK declares 2.0.0; Python SDK declares 1.0.1 |
| Teleop Python | uv-managed Python 3.10 and `gear_sonic[teleop]` | `.venv_teleop` uses Python 3.10.21 |
| XRoboToolkit PC side | PC Service 1.0.0 plus repository Python binding | 1.0.0 service payload and built binding used successfully |
| SONIC models | Matching encoder, decoder and observation config plus planner | Default release works in sim; low-latency candidate not yet installed/validated |

NVIDIA warns that the exact TensorRT platform version matters because a mismatched
version can produce incorrect planner motion. Generated `.trt` engines are tied to
the runtime/GPU environment; regenerate and hash them on the physical-candidate
host rather than copying opaque engines from another platform.

### Alternative onboard profiles

Only use these after the offboard path is stable:

- G1/Jetson AGX Orin: JetPack 6 and TensorRT 10.7.
- Jetson AGX Thor: JetPack 7.1 and TensorRT 10.13.

Those are NVIDIA host-runtime requirements, not Unitree robot-control firmware
versions.

## Required model package

For the first responsive teleoperation candidate, evaluate NVIDIA's low-latency
package as a matched set:

- `policy/low_latency/model_encoder.onnx`;
- `policy/low_latency/model_decoder.onnx`;
- `policy/low_latency/observation_config.yaml`;
- `planner/target_vel/V2/planner_sonic.onnx`.

The low-latency SMPL reference uses four future frames at 20 ms spacing (80 ms
lookahead), versus ten frames/200 ms for the default model. This is reference
lookahead, not measured end-to-end latency. Run the complete planted-feet protocol
in simulation with this exact set before selecting it for hardware. Record SHA-256
hashes for every ONNX/config file and the generated TensorRT engines.

Do not mix the current default encoder/decoder with a low-latency or v1.1
observation config. Do not apply the SONIC v1.1 ankle gain scaling to another model
without a separately reviewed reason.

## Required PICO software and firmware inventory

The successful XRoboToolkit path used:

- PICO regulatory model `A8110`, marketed variant still unconfirmed;
- Android 10, PICO system version `5.20`, build `202403120341`;
- XRoboToolkit PICO SDK29 APK 1.1.1, package `com.xrobotoolkit.client`;
- XRoboToolkit PC Service 1.0.0;
- two paired PICO motion trackers at the ankles;
- Head + Controller tracking, Data/Control Send and Full Body high-accuracy mode.

The exact motion-tracker firmware versions remain unrecorded and must be captured
before the device is returned. No newer PICO browser is needed for this
XRoboToolkit path; the browser-version problem applied to the separate CloudXR/
Isaac Teleop experiment. USB is optional after Wi-Fi streaming works, but keep an
authorized ADB cable available for diagnostics.

## One-time software preparation

Perform these steps without a robot connection:

1. Pin the reviewed repository revision; fetch Git LFS assets and preserve the
   commit plus dirty-tree status.
2. Install the documented x86_64 TensorRT 10.13 TAR package and set
   `TensorRT_ROOT`.
3. Run the repository environment checker, deployment dependency installer and
   C++ build. Preserve compiler, CUDA, driver, TensorRT and build output.
4. Create `.venv_teleop` with `install_scripts/install_pico.sh`; verify the
   XRoboToolkit Python binding imports and the PC service runs.
5. Download the complete low-latency model package through
   `download_from_hf.py --low-latency`; hash the manifest, models and planner.
6. Generate fresh TensorRT engines and run the instrumented simulation protocol at
   least three times, including stale-stream and stop tests.
7. Package the exact executable, config, model hashes and launch command into the
   pre-lab record. Do not rebuild or auto-download during the physical session.

## Robot preparation — no command publication

1. Mount the G1 on a rated gantry with clearance for all limbs and the three-second
   initialization trajectory. Establish a three-meter exclusion zone.
2. Assign separate PICO and safety operators. Verify keyboard `O`, facility E-stop,
   communication method and stop calls before powering control.
3. Inspect the robot for damage, loose connectors, foot condition and gantry
   interference. Confirm adequate battery and normal temperature.
4. Connect the workstation by Ethernet and configure a deliberate static
   `192.168.123.x/24` address. Record the exact interface name. Do not use
   `deploy.sh real` if it falls back to an arbitrary non-loopback interface.
5. With no low-level publisher, perform a bounded read-only DDS check: fresh CRC-
   valid LowState, 29 finite body q/dq entries, base and torso IMUs, motor status,
   temperatures, torque estimates, `mode_machine` and update rate.
6. Query the active Unitree motion mode without releasing it. Confirm no competing
   simulator, stock SDK client, LeRobot/Holosoma process or stale `rt/lowcmd`
   publisher is active.
7. Compare measured joints with SONIC's fixed default standing angles. Because real
   deployment immediately interpolates toward those angles, a large mismatch is a
   launch blocker rather than something to discover after starting.

## PICO/network readiness immediately before launch

1. Fit the ankle trackers with indicators visible; use fitted pants/leggings.
2. Complete PICO tracker calibration and verify left/right laterality in a read-only
   visualization.
3. Start the XRoboToolkit PC service and PICO application; require `WORKING`.
4. Before starting the manager, run and stop a bounded input-only probe confirming
   finite fresh 24-joint frames and tracker laterality. Then run the manager in OFF
   and require at least 30 seconds of fresh PICO reader updates at 50 Hz or better.
   POSE-loop rate and end-to-end stream-delay gates cannot be measured in OFF; they
   must already have passed an instrumented simulation rehearsal using the exact
   candidate.
5. Confirm that disconnecting the PICO is detected by the independent safety
   monitor. The current tested controller continued on stale motion for minutes;
   physical launch remains blocked until a bounded local response and its
   post-stop behavior are validated while suspended.

## Authorized launch order — motion begins here

Only after a new explicit physical-motion authorization:

1. Safety operator takes the keyboard and hardware E-stop; PICO operator assumes
   the exact calibration pose.
2. Start XRoboToolkit and the PICO manager first, in OFF, with stable fresh frames.
3. Confirm MuJoCo and all other DDS command publishers are stopped.
4. Launch the pinned C++ deployment using the exact network interface and matched
   low-latency model/config. Launch itself releases the active stock motion service,
   starts `rt/lowcmd`, and interpolates all 29 joints toward SONIC's default pose.
5. Observe only initialization. Do not press the PICO start chord until `Init Done`,
   robot telemetry and posture are reviewed.
6. Perform the suspended stop/handover tests from the physical plan before entering
   POSE or loading the feet.
7. If those pass, run only segments 0--5 of the planted-feet demonstration during
   the first physical session.

## Unresolved items blocking physical readiness

- G1 system firmware, manufacture date, pelvis revision and motor-driver revision
  are not recorded.
- Compatibility of this exact G1 revision with SONIC's actuator model is not
  established.
- The low-latency model package is not yet installed and simulation-validated on
  this host.
- Local controller-latch and build compatibility patches are not reviewed/pinned as
  a physical candidate.
- Stale PICO input currently does not produce a prompt demonstrated stop.
- Normal stop sends one damping frame and then ceases publishing; subsequent
  stock-controller/hardware behavior is not validated for this stack.
- Motion-tracker firmware versions are not recorded.

Until these are closed, the setup is ready for further simulation and read-only G1
inventory, not physical SONIC motion.
