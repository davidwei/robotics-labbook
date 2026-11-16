# Procedure — Quest Pro to XRoboToolkit to MuJoCo

**Experiment:** EXP-20261115-001  
**Prepared:** 2026-11-15, America/Los_Angeles  
**Execution date / session:** TBD  
**Status:** Planned and unexecuted. Source inspection only; no package install, Quest test, or simulator run has been completed for this procedure.

## 1. Question, scope, and operator roles

Determine whether a Meta Quest Pro running the existing XRoboToolkit-Quest app can send head/controller input to the Linux PC Service and control both arms in the stock dual-UR5e MuJoCo simulation.

This procedure uses a desktop MuJoCo window. It does not implement headset video return, a G1 simulator, physical robot control, dexterous-hand control, voice recognition, or TTS. Placo supplies inverse kinematics inside the MuJoCo demo; its separate browser visualization is disabled.

Use two roles:

- **Headset operator:** wears Quest Pro, uses both Touch Pro controllers, follows callouts, and reports tracking/UI state.
- **Desktop observer:** runs commands, watches SDK/simulation output, records evidence, speaks the next action aloud, and operates the terminal stop path.

Before starting, the observer says “Can you hear the instructions?” and waits for an audible acknowledgment. Human callouts are the planned interface. Their audibility must be observed; no automated speech feature is implied.

Use an isolated simulation workspace. Do not launch hardware scripts, ROS/DDS command publishers, G1 control, or a physical policy. If an existing robot-control process or hardware connection makes that separation unclear, resolve it before proceeding. Do not terminate unrelated processes automatically.

**Proposed minimum useful result:** fresh data from both controllers plus one bounded single-arm MuJoCo control sequence, clutch release/re-engagement, and verified process exit. Both arms and a clean-restart repetition are the fuller success criteria. Installation, a running service, connected UI, or model rendering alone do not establish this result.

## 2. Freeze the candidate and allocate evidence

### 2.1 Candidate versions

| Component | Candidate | Evidence / boundary |
| --- | --- | --- |
| Quest APK | XRoboToolkit-Quest 1.0.1 | Release asset pinned by SHA256 below; Quest Pro operation remains to be tested |
| PC Service | v1.0.0, Ubuntu 24.04 amd64 package | Release asset pinned by SHA256 |
| Python SDK | xrobotoolkit-sdk 1.1.0 | Published Linux x86_64 wheel for CPython >=3.10 |
| Python | Ubuntu 24.04 Python 3.12 in a new venv | Confirm actual interpreter; do not alter an existing environment |
| MuJoCo | 3.3.7 | Proposed prebuilt baseline, not an upstream certified combination |
| Placo | 0.9.18 | Retains Pinocchio/MeshCat interfaces used by the sample |
| Teleop sample | 79e5cb8a56e3455515ce1b476e993c764ec58739 | Exact source revision; dual-UR5e MJCF and URDF included |

Placo 0.11 changed its model/visualization architecture. Do not silently upgrade the pin during this experiment. Other resolved dependencies will be captured before headset testing. These pins make the candidate reviewable; they do not constitute a successful environment test.

### 2.2 Terminal A: create a unique workspace

Run these commands on the actual Linux desktop, not in a remote assistant workspace. Stop on an unexpected command failure; preserve its output. Explicitly expected diagnostic outcomes, such as an absent prior package or service, are described below. The following directory is new for each attempt.

~~~bash
set -o pipefail
export XRBT_WORK=$(mktemp -d "$HOME/xrbt-quest-mujoco.XXXXXXXX")
export XRBT_EVIDENCE="$XRBT_WORK/evidence"
export XRBT_DOWNLOADS="$XRBT_WORK/downloads"
export XRBT_REPO="$XRBT_WORK/XRoboToolkit-Teleop-Sample-Python"
export XRBT_VENV="$XRBT_WORK/venv"
export XRBT_ENV="$XRBT_WORK/session.env"
mkdir -p "$XRBT_EVIDENCE" "$XRBT_DOWNLOADS"
printf 'export XRBT_WORK=%q\nexport XRBT_EVIDENCE=%q\nexport XRBT_DOWNLOADS=%q\nexport XRBT_REPO=%q\nexport XRBT_VENV=%q\nexport XRBT_ENV=%q\n' \
  "$XRBT_WORK" "$XRBT_EVIDENCE" "$XRBT_DOWNLOADS" "$XRBT_REPO" "$XRBT_VENV" "$XRBT_ENV" > "$XRBT_ENV"
printf 'source %q\n' "$XRBT_ENV"
~~~

Copy the printed `source /absolute/path/session.env` command into the session timeline. Every additional terminal must source that exact file. After the venv exists, also run:

~~~bash
source "$XRBT_VENV/bin/activate"
cd "$XRBT_REPO"
set -o pipefail
~~~

Do not create a second workspace just to open another terminal. Later input captures and simulation runs get their own non-overwriting subdirectories.

### 2.3 Record the actual host and execution time

~~~bash
date -u -Iseconds | tee "$XRBT_EVIDENCE/start-utc.txt"
TZ=America/Los_Angeles date -Iseconds | tee "$XRBT_EVIDENCE/start-pacific.txt"
cat /etc/os-release | tee "$XRBT_EVIDENCE/os-release.txt"
uname -a | tee "$XRBT_EVIDENCE/uname.txt"
dpkg --print-architecture | tee "$XRBT_EVIDENCE/debian-architecture.txt"
python3.12 --version 2>&1 | tee "$XRBT_EVIDENCE/python-system.txt"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  printf '%s\n' 'nvidia-smi unavailable; record the actual GPU/driver separately.'
fi 2>&1 | tee "$XRBT_EVIDENCE/nvidia-smi.txt"
printf 'DISPLAY=%s\nWAYLAND_DISPLAY=%s\nXDG_SESSION_TYPE=%s\n' \
  "$DISPLAY" "$WAYLAND_DISPLAY" "$XDG_SESSION_TYPE" | tee "$XRBT_EVIDENCE/display-session.txt"
df -h "$XRBT_WORK" | tee "$XRBT_EVIDENCE/disk-before.txt"
~~~

**Gate P0:** confirm Ubuntu 24.04, amd64/x86_64, Python 3.12, and a local graphical session. Record GPU/driver details; an AMD/Intel host need not have `nvidia-smi`. Do not change the working driver as a preparation step. The stock single-instance simulation uses desktop OpenGL, not a CUDA training workload. A different Ubuntu release/architecture requires its own matching package and recorded environment choice; do not install this 24.04 amd64 artifact blindly.

If a prerequisite command is missing, install only the relevant package. The normal preparation tools are `git`, `curl`, `adb`, and `python3.12-venv`:

~~~bash
sudo apt update
sudo apt install git curl adb python3.12-venv
~~~

Record package changes. No compiler, Qt development kit, CUDA toolkit, or source build is required by the proposed prebuilt route.

## 3. Download, verify, and install the native components

### 3.1 Download the two pinned release assets

~~~bash
cd "$XRBT_DOWNLOADS"
curl -fL -o XRoboToolkit-Quest-1.0.1.apk \
  https://github.com/XR-Robotics/XRoboToolkit-Unity-Client-Quest/releases/download/v1.0.1/XRoboToolkit-Quest-1.0.1.apk
curl -fL -o XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb \
  https://github.com/XR-Robotics/XRoboToolkit-PC-Service/releases/download/v1.0.0/XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb
printf '%s\n' \
  'c8a077451e7f6b66ca688668d7b32f5a6a6c19a8c0fa4657f2e1344493c174df  XRoboToolkit-Quest-1.0.1.apk' \
  'bce661f0be0b8a246ceecb2e5f1675a81c26b834648dc7fdf23f8c0bfe2a5d19  XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb' \
  > "$XRBT_EVIDENCE/release-SHA256SUMS.txt"
sha256sum --check "$XRBT_EVIDENCE/release-SHA256SUMS.txt" \
  | tee "$XRBT_EVIDENCE/release-checksums-check.txt"
~~~

Both lines must report `OK`. A mismatch is a download/provenance failure; do not install that file or substitute an unrecorded version.

### 3.2 Install the PC Service package

Inspect any existing installation first:

~~~bash
dpkg-query -W roboticsservice 2>&1 | tee "$XRBT_EVIDENCE/pc-service-before.txt"
dpkg-deb --info "$XRBT_DOWNLOADS/XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb" \
  | tee "$XRBT_EVIDENCE/pc-service-package-info.txt"
sudo apt install "$XRBT_DOWNLOADS/XRoboToolkit_PC_Service_1.0.0_ubuntu_24.04_amd64.deb"
dpkg-query -W roboticsservice | tee "$XRBT_EVIDENCE/pc-service-after.txt"
~~~

An absent prior package is expected on first install. Preserve an existing different-version/configuration record before changing it. The package bundles runtime files; it does not prove that graphics and all system libraries work.

### 3.3 Identify and install on the actual Quest Pro

Enable developer mode using Meta's current device setup if it is not already enabled. Connect the headset by USB and accept this PC's USB debugging request in the headset. The USB connection is for installation/diagnostics; the experiment's tracking path is the local network.

~~~bash
adb devices -l | tee "$XRBT_EVIDENCE/adb-devices.txt"
~~~

Select the exact Quest device serial shown, not an arbitrary first device:

~~~bash
export QUEST_SERIAL="REPLACE_WITH_THE_VERIFIED_QUEST_SERIAL"
printf 'export QUEST_SERIAL=%q\n' "$QUEST_SERIAL" >> "$XRBT_ENV"
adb -s "$QUEST_SERIAL" shell getprop ro.product.model \
  | tee "$XRBT_EVIDENCE/quest-model.txt"
adb -s "$QUEST_SERIAL" shell getprop ro.build.fingerprint \
  | tee "$XRBT_EVIDENCE/quest-build.txt"
adb -s "$QUEST_SERIAL" shell dumpsys package com.xrobotoolkit.client.quest \
  > "$XRBT_EVIDENCE/quest-package-before.txt"
adb -s "$QUEST_SERIAL" install -r "$XRBT_DOWNLOADS/XRoboToolkit-Quest-1.0.1.apk" \
  | tee "$XRBT_EVIDENCE/apk-install.txt"
adb -s "$QUEST_SERIAL" shell pm path com.xrobotoolkit.client.quest \
  | tee "$XRBT_EVIDENCE/quest-package-path.txt"
adb -s "$QUEST_SERIAL" shell dumpsys package com.xrobotoolkit.client.quest \
  > "$XRBT_EVIDENCE/quest-package-after.txt"
~~~

Confirm the physical headset is Quest Pro, controllers are paired/charged, and the installed version is 1.0.1. Record the Horizon OS version visible in Settings as well. On signature mismatch, stop and inspect; do not automatically uninstall and erase existing app data.

**Native-installation checkpoint:** both release checksums pass, package installation is recorded, and the intended app exists on the intended headset. An absent prior Quest package is expected on first install. This is installation evidence only; P1 is completed after the source and Python environment are prepared below.

## 4. Prepare the simulation-only Python environment

### 4.1 Clone and pin the upstream source

~~~bash
git clone https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python.git "$XRBT_REPO"
git -C "$XRBT_REPO" checkout --detach 79e5cb8a56e3455515ce1b476e993c764ec58739
git -C "$XRBT_REPO" rev-parse HEAD | tee "$XRBT_EVIDENCE/sample-commit.txt"
git -C "$XRBT_REPO" status --short | tee "$XRBT_EVIDENCE/sample-status-before.txt"
git -C "$XRBT_REPO" diff --binary > "$XRBT_EVIDENCE/sample-diff-before.patch"
~~~

Verify the printed commit exactly. The required UR5 assets are checked in; do not replace them with separately downloaded robot models.

### 4.2 Install only the imports used by this demo

~~~bash
python3.12 -m venv "$XRBT_VENV"
source "$XRBT_VENV/bin/activate"
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: "xrobotoolkit-sdk==1.1.0" \
  2>&1 | tee "$XRBT_EVIDENCE/sdk-install.txt"
python -m pip install "mujoco==3.3.7" "placo==0.9.18" numpy meshcat tyro \
  2>&1 | tee "$XRBT_EVIDENCE/simulation-dependencies-install.txt"
python -m pip check 2>&1 | tee "$XRBT_EVIDENCE/pip-check.txt"
python -m pip freeze | tee "$XRBT_EVIDENCE/requirements-resolved.txt"
python -m pip list --format=json > "$XRBT_EVIDENCE/packages-resolved.json"
~~~

This route runs the source via `PYTHONPATH` and deliberately does **not** install the teleop project distribution. Its upstream pyproject also declares unrelated hardware/hand packages, including Torch, UR RTDE, Dynamixel, RealSense and dex_retargeting. Therefore `pip check` remains a check of the installed simulation environment; it is not a claim that every upstream hardware demo is installed.

Do not run legacy `setup.sh` or `setup_conda.sh`: they remove local directories/environments and call the SDK's removed `setup_ubuntu.sh`. Placo 0.9.18 supplies robotics Pinocchio through the package `pin==3.8.0`; do not install the unrelated package named `pinocchio` as a repair.

If pip proposes a source build or dependency resolution fails, preserve the output and stop this preparation gate. Prefer resolving the exact wheel/interpreter issue before adding compilers or changing pins.

**Gate P1:** the release hashes, installed native versions, exact source commit, and resolved Python package set are recorded. A dependency change after this gate creates a revised candidate and requires repeating P2.

### 4.3 Verify imports and model loading without XR input

~~~bash
cd "$XRBT_REPO"
PYTHONPATH="$XRBT_REPO" python - <<'PY' 2>&1 | tee "$XRBT_EVIDENCE/import-and-model-check.txt"
import os
import mujoco
import mujoco.viewer
import numpy
import meshcat
import placo
import pinocchio
import tyro
import xrobotoolkit_sdk
from placo_utils.visualization import frame_viz, robot_frame_viz, robot_viz
from xrobotoolkit_teleop.simulation.mujoco_teleop_controller import MujocoTeleopController
from xrobotoolkit_teleop.utils.path_utils import ASSET_PATH
xml = os.path.join(ASSET_PATH, "universal_robots_ur5e/scene_dual_arm.xml")
urdf = os.path.join(ASSET_PATH, "universal_robots_ur5e/dual_ur5e.urdf")
model = mujoco.MjModel.from_xml_path(xml)
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)
mujoco.mj_forward(model, data)
for _ in range(10):
    mujoco.mj_step(model, data)
robot = placo.RobotWrapper(urdf)
print("Imports OK")
print("MJCF:", xml, "nq:", model.nq, "nu:", model.nu, "simulated_seconds:", data.time)
print("URDF:", urdf, "Placo joints:", list(robot.joint_names()))
print("Finite simulated state:", bool(numpy.isfinite(data.qpos).all()))
PY
PYTHONPATH="$XRBT_REPO" python scripts/simulation/teleop_dual_ur5e_mujoco.py --help \
  2>&1 | tee "$XRBT_EVIDENCE/demo-help.txt"
sha256sum assets/universal_robots_ur5e/scene_dual_arm.xml \
  assets/universal_robots_ur5e/dual_ur5e.xml \
  assets/universal_robots_ur5e/dual_ur5e.urdf \
  > "$XRBT_EVIDENCE/model-SHA256SUMS.txt"
~~~

Expected: imports succeed, model dimensions are 12 positions/12 actuators, finite simulated state, both arms' Placo joints, and CLI help including `--scale-factor` and `--no-visualize-placo`. This check never instantiates the teleop controller and does not connect the SDK.

### 4.4 Verify the local graphics window

~~~bash
python -m mujoco.viewer \
  --mjcf=assets/universal_robots_ur5e/scene_dual_arm.xml
~~~

Observe two UR5e arms and capture a desktop screenshot. Close this standalone viewer before proceeding. Missing display/GLFW errors are a graphics failure, not a headset connection failure. Use a local desktop terminal. An EGL/offscreen setting does not supply the stock visible GUI. If inherited `MUJOCO_GL` or `PYOPENGL_PLATFORM` overrides are present, record them and use a clean terminal without those overrides for this desktop check.

**Gate P2:** imports, model loading, CLI, and actual desktop rendering pass. Freeze the resolved environment now; no additional package changes during the headset sequence.

## 5. Establish the local network and PC Service

Record the desktop's actual LAN address/interface and the Quest's Wi-Fi address. Prefer the desktop's wired connection to the same LAN as the headset; being on the same SSID name is not proof of mutual reachability. Avoid a guest network with client isolation.

~~~bash
ip -brief address | tee "$XRBT_EVIDENCE/desktop-addresses.txt"
ip route | tee "$XRBT_EVIDENCE/desktop-routes.txt"
export XRBT_QUEST_IP="REPLACE_WITH_THE_VERIFIED_QUEST_WIFI_IPV4"
printf 'export XRBT_QUEST_IP=%q\n' "$XRBT_QUEST_IP" >> "$XRBT_ENV"
ip route get "$XRBT_QUEST_IP" | tee "$XRBT_EVIDENCE/route-to-quest.txt"
pgrep -af RoboticsServiceProcess | tee "$XRBT_EVIDENCE/service-processes-before.txt"
~~~

No match from `pgrep` means no service was found. If one already exists, identify its path/version and use that recorded instance or stop it deliberately before substitution. Do not launch duplicate instances.

Use the `src` address in `ip route get` to identify the desktop interface selected for the Quest. Verify it is the intended LAN interface; a VPN or container address is not automatically the correct address to enter in the headset.

| Path | Source-reviewed endpoint | Check |
| --- | --- | --- |
| Quest tracking → PC Service | TCP **63901** on the desktop | PC listener and a connection from the headset |
| Automatic service discovery → Quest | UDP **29888** destination port | Discovery can fail independently; manual IP entry bypasses it |
| Python SDK → local PC Service | **127.0.0.1:60061**, gRPC default | Local service availability; no external firewall opening is needed for this client |

The Quest networking source still has a field initialized to 8888, but its connection method replaces that value with 63901. Use the actual connection constant. The service's local address/port defaults can be overridden in `setting.ini`. Record observed listeners if the installed binary/configuration differs; do not silently assume source and release binary behavior match.

In Terminal B, source `session.env` and start the service outside the venv/Conda environment where possible:

~~~bash
bash /opt/apps/roboticsservice/runService.sh \
  > "$XRBT_EVIDENCE/pc-service-console.txt" 2>&1
pgrep -af RoboticsServiceProcess | tee "$XRBT_EVIDENCE/service-processes-started.txt"
ss -ltnp | tee "$XRBT_EVIDENCE/tcp-listeners-started.txt"
~~~

The upstream script changes to its installation directory, adds bundled directories to `LD_LIBRARY_PATH` and Qt paths, then backgrounds `RoboticsServiceProcess`. A returned prompt is expected. Record the selected service PID and whether this procedure started it. Do not export those library paths into the Python terminal. A process/listener check is readiness evidence, not proof of live headset input.

Open **XRoboToolkit-Quest** in the headset. Select the correct PC address from discovery; if necessary use **Network → PC Service → Enter** to enter the recorded LAN IP as a **bare IPv4 address**, without a URL scheme or appended port. Never enter `127.0.0.1` as the remote PC address.

Set the initial UI state:

| Setting | Initial value |
| --- | --- |
| Tracking → Head | On |
| Tracking → Controller | On |
| Tracking → Hand | Off for this controller baseline |
| Body Tracking | Off / unavailable |
| Send | Off until the observer requests it |
| Switch w/ A Button | Off |
| Remote Vision / Listen | Off |
| Data Collection / Record | Off |

The A-button option, when enabled, toggles Send as a latched state; it is not a hold-to-run control. Leave it disabled for this procedure. Record a headset screenshot or a literal UI-state note. The app's Network/FPS display is not the measured SDK update rate.

**Gate P3:** the released app launches on the identified Quest Pro, its version/settings are verified, and the Touch Pro controllers can operate its UI. This is the first direct compatibility observation; development on Quest 3 does not establish it in advance.

**Gate P4:** one identified PC Service process is present, expected listeners are observed, the headset shows the intended PC address and `WORKING`, and initial Send is Off. If a listener appears only after connection, record that sequence. `WORKING` indicates a socket connection; fresh usable poses are evaluated in R1.

## 6. Input-only capture and operator rehearsal

No simulator or hardware controller is running in this stage. The observer says: “Input check only. Hold both controllers comfortably; both side grips released.” The operator confirms. Then enable **Send** in the app.

### 6.1 Capture approximately 120 seconds at a target polling rate of 20 Hz

In Terminal A, source the shared environment, activate the venv, and allocate a new capture:

~~~bash
export XRBT_INPUT=$(mktemp -d "$XRBT_EVIDENCE/input-XXXXXXXX")
printf '%s\n' "$XRBT_INPUT" | tee -a "$XRBT_EVIDENCE/input-capture-index.txt"
timeout --signal=INT --kill-after=5s 135s python -u - <<'PY' \
  2>&1 | tee --ignore-interrupts "$XRBT_INPUT/console.txt"
import json, math, os, time
from pathlib import Path
import xrobotoolkit_sdk as xrt

output = Path(os.environ["XRBT_INPUT"]) / "sdk-snapshots.jsonl"
start = time.monotonic()
deadline = start + 120.0
next_poll = start
samples = 0
source_changes = 0
previous_source = None
initialized = False
reason = "duration_complete"

def pose_info(values):
    raw = [float(v) for v in values]
    finite = all(math.isfinite(v) for v in raw)
    return {
        "pose": [v if math.isfinite(v) else None for v in raw],
        "finite": finite,
        "length": len(raw),
        "quaternion_norm": math.sqrt(sum(v*v for v in raw[3:7]))
            if finite and len(raw) == 7 else None,
    }

with output.open("x", encoding="utf-8") as stream:
    def emit(record):
        stream.write(json.dumps(record, allow_nan=False) + "\n")
        stream.flush()
    emit({
        "kind": "metadata", "schema": "xrbt-sdk-snapshot-v1",
        "target_poll_hz": 20, "duration_target_seconds": 120,
        "source": "xrobotoolkit_sdk cached getter snapshots",
        "atomic_snapshot": False, "per_controller_validity": "not exposed here",
        "clock_sync_established": False,
    })
    try:
        xrt.init()
        initialized = True
        while time.monotonic() < deadline:
            begin_mono = time.monotonic_ns()
            begin_wall = time.time_ns()
            source_before = int(xrt.get_time_stamp_ns())
            record = {
                "kind": "sample", "index": samples,
                "host_wall_time_ns": begin_wall,
                "host_monotonic_ns_begin": begin_mono,
                "source_timestamp_ns_before": source_before,
                "head": pose_info(xrt.get_headset_pose()),
                "left": pose_info(xrt.get_left_controller_pose()),
                "right": pose_info(xrt.get_right_controller_pose()),
                "left_grip": float(xrt.get_left_grip()),
                "right_grip": float(xrt.get_right_grip()),
                "left_trigger": float(xrt.get_left_trigger()),
                "right_trigger": float(xrt.get_right_trigger()),
                "a_button": bool(xrt.get_A_button()),
                "b_button": bool(xrt.get_B_button()),
            }
            source_after = int(xrt.get_time_stamp_ns())
            record["source_timestamp_ns_after"] = source_after
            record["host_monotonic_ns_end"] = time.monotonic_ns()
            record["source_changed_since_previous_poll"] = (
                previous_source is not None and source_after != previous_source)
            for key in ("left_grip", "right_grip", "left_trigger", "right_trigger"):
                if not math.isfinite(record[key]):
                    record[key] = None
            source_changes += int(record["source_changed_since_previous_poll"])
            emit(record)
            if samples % 20 == 0:
                print("sample", samples, "source_ns", source_after,
                      "grips", record["left_grip"], record["right_grip"],
                      "head_xyz", record["head"]["pose"][:3],
                      "left_xyz", record["left"]["pose"][:3],
                      "right_xyz", record["right"]["pose"][:3], flush=True)
            previous_source = source_after
            samples += 1
            next_poll += 0.05
            time.sleep(max(0.0, next_poll - time.monotonic()))
    except KeyboardInterrupt:
        reason = "interrupted"
    except Exception as exc:
        reason = "error"
        emit({"kind": "error", "type": type(exc).__name__, "message": str(exc),
              "host_wall_time_ns": time.time_ns()})
        raise
    finally:
        emit({"kind": "summary", "reason": reason, "samples": samples,
              "source_changes": source_changes,
              "host_elapsed_seconds": time.monotonic() - start})
        print("Saved", output, "samples", samples, "reason", reason, flush=True)
        if initialized:
            xrt.close()
PY
XRBT_CAPTURE_RC=$?
printf '%s\n' "$XRBT_CAPTURE_RC" > "$XRBT_INPUT/pipeline-exit-status.txt"
~~~

The outer timeout bounds shutdown as well as observation. Preserve timeout/error/incomplete files; do not relabel them as a full capture. Twenty Hz is a target **getter polling rate**, not a demonstrated transport, source tracking, or robot control rate. Calls are sequential and may span updates. This is not raw packet capture and does not expose reliable per-controller tracked/valid flags. Advancing global timestamps and finite poses alone do not prove each controller is being tracked.

### 6.2 Rehearse these actions during the capture

The observer calls each action aloud and writes actual times in the session timeline:

1. Both controllers still, grips released; verify near-zero grip values.
2. Move only the right controller slowly along three directions and rotate it; confirm corresponding pose changes.
3. Fully squeeze right side grip, hold briefly, then release; verify values exceed 0.9 and return near zero.
4. Repeat movement and grip test on the left.
5. Move the head gently; observe head data separately.
6. Return to the neutral stance, both grips released, and say “ready for simulation.”

Do not use index triggers as the arm clutch. Do not use A as a stop control. This baseline does not assign B to simulator recording.

**R1 checkpoint:** the relevant poses respond to the corresponding deliberate movements, source timestamps advance, both grips cross 0.9 and release, and there are no unexplained frozen/invalid values. Inspect the JSONL and observation notes together. A successful SDK initialization message alone is insufficient. Record missing evidence or a failed gate rather than guessing.

If the headset is removed, recenters, changes tracking mode, sleeps, or reconnects, repeat this input check with a new evidence path before simulation. No PICO body-tracker calibration applies to this controller-only test.

### 6.3 P5 — rehearse the operator workflow

With no simulator running, agree the comfortable neutral stance and forward direction. The observer calls “right grip,” “release,” “reposition,” “left grip,” and “stop”; the operator repeats the meaning and actions. Recenter only at this stopped stage if needed, then repeat the fresh-input check. During the simulated run, grip engagement captures the relative hand/arm reference; it is not a measured geometric calibration.

**Gate P5:** callouts are audible, both participants know which grip enables which arm, the observer can reach Terminal C, and both can state the stop sequence: release while Send remains On, Ctrl+C, verify process exit, then Send Off. Finish with fresh input and both grips released.

## 7. Run the bounded MuJoCo control sequence

### 7.1 Prepare independent observation

The observer remains at the desktop. Start a desktop screen recording showing the MuJoCo window and, where possible, terminal output. Verify a short saved preview before the actual run, then use a new recording file. Include audible callouts if the capture tool supports microphone audio; otherwise timestamp the spoken instructions in the timeline.

The stock simulation has no telemetry logger configured here. Screen recording plus console output establishes only qualitative control behavior. Numerical tracking error, robot-state rates, synchronized input-to-motion latency, and loss/recovery safety are not established by this procedure.

### 7.2 Launch from Terminal C

Source the same `session.env`, activate the venv, and `cd "$XRBT_REPO"`. Confirm P0–P5 and R1, Send On, both grips released, observer ready, and recording active. This first simulated-motion run is R2.

~~~bash
export XRBT_RUN=$(mktemp -d "$XRBT_EVIDENCE/simulation-XXXXXXXX")
printf '%s\n' "$XRBT_RUN" | tee -a "$XRBT_EVIDENCE/simulation-run-index.txt"
timeout --signal=INT --kill-after=10s 240s bash -c '
  printf "%s\n" "$$" > "$XRBT_RUN/simulator.pid"
  exec env PYTHONPATH="$XRBT_REPO" python -u \
    "$XRBT_REPO/scripts/simulation/teleop_dual_ur5e_mujoco.py" \
    --scale-factor 0.5 --no-visualize-placo
' 2>&1 | tee --ignore-interrupts "$XRBT_RUN/console.txt"
XRBT_RUN_RC=$?
printf '%s\n' "$XRBT_RUN_RC" > "$XRBT_RUN/pipeline-exit-status.txt"
~~~

The PID file identifies the shell that `exec` replaces with Python. The 240-second cap is a proposed experiment bound, not a verified shutdown guarantee. An expired cap or forced kill is recorded as such. Do not claim normal stop from exit status alone.

Expected initialization includes MuJoCo and Placo joint lists, mocap IDs for `right_target`/`left_target`, then a desktop window. A MeshCat browser view should not open with `--no-visualize-placo`. The selected source uses actual MuJoCo dynamics and joint actuators.

### 7.3 Observer-led sequence

| Step | Spoken instruction / action | Proposed observation |
| --- | --- | --- |
| S0 | “Both grips released; move the controllers gently.” | No commanded following caused by those movements; note any settling/drift separately |
| S1 | “Hold right side grip fully; make one small translation, then one small rotation.” | Right target and arm respond; left arm does not mirror the right |
| S2 | “Release right grip; move your hand to a comfortable position.” | Controller repositioning no longer updates that arm's target |
| S3 | “Hold right grip again; make one small translation.” | A new relative reference is established without a large re-engagement jump |
| S4 | Repeat S1–S3 using left side grip | Corresponding left-arm behavior |
| S5 | “Hold both grips; make one small coordinated movement; release both.” | Independent bimanual response, followed by release |
| S6 | “Both grips released. Keep Send on. Stopping the simulator now.” | Follow the stop procedure below |

Use roughly 5–10 cm controller translations and modest rotations within comfortable tracking visibility. These are proposed first-test motions, not calibrated robot limits. Translation scale 0.5 applies to the requested relative target displacement; do not interpret approximate visible movement as a measured gain.

Grip activation is `> 0.9`. Release/re-engagement implements relative clutching. The selected dual-UR5e configuration has no grippers: index triggers have no gripper task, head motion is not mapped to a robot neck, and B does not start a simulator dataset recording.

End the run on operator request, unexpected direction/large jump, frozen input, repeated IK errors, lost observation, or app/tracking failure. Preserve the failed attempt; do not modify transforms, thresholds or software mid-run to obtain a pass.

## 8. Stop, verify exit, and only then test recovery

### 8.1 Normal stop

1. While **Send remains On**, release both side grips. Allow the observer to see deactivation/settled target behavior and record that observation.
2. The observer presses **Ctrl+C in Terminal C**. The stock loop catches KeyboardInterrupt and prints `Teleoperation stopped.` when that handler runs.
3. Verify the exact simulation process is gone using the saved PID. A closed window or stop message is not sufficient.
4. Only after termination is verified, toggle **Send Off** and leave both grips released.
5. Keep screen recording through the stop check and a short post-stop observation; then save it under the run's evidence location.

After the launch pipeline returns:

~~~bash
XRBT_SIM_PID=$(cat "$XRBT_RUN/simulator.pid")
if kill -0 "$XRBT_SIM_PID" 2>/dev/null; then
  ps -p "$XRBT_SIM_PID" -o pid,lstart,args | tee "$XRBT_RUN/stop-process-check.txt"
  printf '%s\n' 'PID still present: inspect; normal stop is not verified.' \
    | tee -a "$XRBT_RUN/stop-process-check.txt"
else
  printf '%s\n' 'Recorded simulator PID is absent.' \
    | tee "$XRBT_RUN/stop-process-check.txt"
fi
date -u -Iseconds | tee "$XRBT_RUN/stop-check-utc.txt"
~~~

The stock loop does not check `viewer.is_running()`; clicking the window's close button is not the specified stop. If the process remains, inspect its command line and the timeout result, preserve the anomaly, and deliberately terminate only that verified simulation PID. Do not use a broad kill command or stop the PC Service as a substitute for verifying simulator exit.

If Terminal C does not return after Ctrl+C, use Terminal A and the latest path in `simulation-run-index.txt` to read that run's `simulator.pid`. Inspect it with `ps -p PID -o pid,lstart,args`; after confirming it is this simulation, send `kill -TERM PID` and recheck. Record escalation as an abnormal stop. The input logger and console `tee` ignore/handle interruption only to preserve evidence; they are not a stale-input watchdog.

### 8.2 R3 — clean-restart repeat

After R2 has stopped, retain its separate evidence directory. With Send On and no simulator running, repeat the input check into a new capture directory; confirm fresh poses and released grips. Repeat the ready callout, allocate a new simulation directory using section 7.2, and run one short right-grip/release/regrip sequence followed by the left equivalent. End with the full stop check in section 8.1. Record whether behavior repeats without unexplained jumps or a hidden button-state requirement. A failed R2 can remain a useful partial result; do not mark R3 passed or imply reliability if it was not performed.

### 8.3 D1 — optional recovery rehearsal, simulator stopped

Recovery is a separate diagnostic, not a requirement for claiming basic nominal control. Do not induce loss while a grip is held or while the simulator is running.

With the simulator PID absent and Send Off, close/reopen the Quest app or perform one agreed network reconnect. Record which disruption was tested. Re-establish the known PC address and UI settings, especially **Switch w/ A Button Off**. Repeat section 6 into a new input-capture directory. Record whether user action, IP re-entry or recalibration/recentering was needed.

A later simulation repeat is a new run with a new evidence path and a fresh ready acknowledgment. Successful manual recovery does not establish automatic stale-input rejection or reconnect disarming.

## 9. Troubleshooting checkpoints

| Symptom | Next bounded check |
| --- | --- |
| APK install fails / device unauthorized | Inspect exact ADB serial and headset USB-debug prompt; preserve install output; do not uninstall automatically |
| PC address not discovered | Verify actual LAN IP/subnet and guest/client isolation; use manual PC Service IP; inspect the recorded service process/log |
| Linux connection still fails | Upstream suggests starting its 3D demo before reopening the headset app; if tried, record it as a separate diagnostic and close it before the MuJoCo run |
| Service exits / Qt error | Inspect `pc-service-console.txt`; run bundled launcher in a clean local desktop terminal; install a specifically missing runtime library such as `libxcb-cursor0` only when the error supports it |
| No display / GLFW / OpenGL error | Resolve local graphical-session access first; inspect relevant `libgl1`/`libglfw3` runtime availability if reported missing; do not infer a headset failure |
| SDK import/library error | Confirm Python 3.12, venv and 1.1.0 wheel; record traceback; do not reuse an old manually built SDK via `PYTHONPATH` |
| Placo/Pinocchio/MeshCat mismatch | Confirm Placo 0.9.18 and resolved `pin` dependency; do not mix latest Placo with this frozen sample |
| All-zero/nonadvancing input | Check Head/Controller/Send settings, real PC IP, service and controller pairing; do not proceed to IK |
| Global timestamps advance but a controller is frozen | Repeat deliberate isolated controller motion; cached getters do not prove per-controller validity |
| Fresh poses but arm does not respond | Check full side-grip squeeze >0.9, not index trigger; inspect activation messages |
| Mirrored/wrong-direction or jumpy motion | Stop simulation; retain input/video/config evidence; investigate mapping as a later changed candidate |
| Simulator window closes but process persists | Use the exact-PID stop verification; record that window closure was not process termination |
| pip begins an unexpected source build | Stop preparation, preserve resolution/build output, inspect wheel/Python compatibility before adding build tools |

If network policy blocks tracking, inspect the actual TCP 63901 listener and scope any necessary firewall rule to the verified Quest address and desktop LAN interface; record the change. Leave the local SDK connection local. Manual IP entry can bypass discovery. Do not disable the firewall globally or assume optional video uses the tracking endpoint.

## 10. Evidence review, closeout, and handoff

For each gate and run, enter **pass / fail / blocked / not tested**, the actual date/time, operator/observer, and evidence links. Criteria above are proposed; do not backfill results from source inspection.

Retain:

- Host OS/architecture, Python/GPU/driver, headset model/OS/controller state, LAN topology and UI settings.
- Release files or durable download references, verified checksums, installed versions, sample commit/dirty patch, model hashes and resolved package list.
- Every input capture, console/error output, start/end/timeout status, sample counts and observed gaps. State that these are sampled cached getters with unsynchronized clocks.
- Desktop screenshot/recording, audible-callout capture or timed operator notes, qualitative per-arm response, clutch observations, stop request/handler/PID verification, and app/service final state.
- Failed starts and recovery attempts under their own paths. No numerical latency/tracking claim is justified without additional synchronized telemetry.

Stop only the PC Service instance started for this experiment if it is no longer needed; verify its identity before acting. Leave pre-existing unrelated services alone. Record whether the headset app was closed and Send was Off. No physical robot state or authority restoration claim belongs to this simulation-only test.

Capture the final source state and hash the evidence files:

~~~bash
git -C "$XRBT_REPO" status --short > "$XRBT_EVIDENCE/sample-status-after.txt"
git -C "$XRBT_REPO" diff --binary > "$XRBT_EVIDENCE/sample-diff-after.patch"
python - <<'PY'
import hashlib, os
from pathlib import Path
root = Path(os.environ["XRBT_EVIDENCE"])
manifest = root / "evidence-SHA256SUMS.txt"
with manifest.open("x", encoding="utf-8") as out:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path != manifest:
            with path.open("rb") as source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            out.write(f"{digest}  {path.relative_to(root)}\n")
print(manifest)
PY
~~~

Run the final manifest once after captures finish; if more evidence is added, create a separately named new manifest rather than overwriting the previous one. Preserve raw evidence and copy it to the project's durable artifact destination; verify the copied files/hashes. A local path or an intention to upload is not a completed backup.

Create the actual session record on its execution date, link it to this experiment, and register run/evidence references using the labbook's canonical skill. Keep large video/telemetry outside normal Git. Report separately: installed, connected, input verified, simulation controlled, stop verified, recovery tested, and unresolved. A successful result supports the next integration decision; it does not certify G1/Revo2 readiness.

## 11. Source references and evidence boundaries

- [Quest source README at 07a2833](https://github.com/XR-Robotics/XRoboToolkit-Unity-Client-Quest/blob/07a28333341629008187e988b73b48bced316092/README.md): UI/Send/A-button behavior, Linux startup, known rendering issues.
- [Quest v1.0.1 release](https://github.com/XR-Robotics/XRoboToolkit-Unity-Client-Quest/releases/tag/v1.0.1): APK identity; asset SHA256 retrieved from GitHub release metadata.
- [PC Service v1.0.0 release](https://github.com/XR-Robotics/XRoboToolkit-PC-Service/releases/tag/v1.0.0): Ubuntu-specific packages; binary hashes do not prove a reproducible build from a particular source commit.
- [PC launcher source](https://github.com/XR-Robotics/XRoboToolkit-PC-Service/blob/85bac4dbc1fd5cef42c74a160d9c30aa3491f122/RoboticsService/Package/debPack/runService.sh): working directory, runtime paths, background launch.
- [PC network constants](https://github.com/XR-Robotics/XRoboToolkit-PC-Service/blob/85bac4dbc1fd5cef42c74a160d9c30aa3491f122/RoboticsService/DeviceConnectionManager/Manage/Manage_global.h), [local gRPC defaults](https://github.com/XR-Robotics/XRoboToolkit-PC-Service/blob/85bac4dbc1fd5cef42c74a160d9c30aa3491f122/RoboticsService/PXREAGRPCServer/PXREAGRPCServer.cpp), and [Quest v1.0.1 TCP connection](https://github.com/XR-Robotics/XRoboToolkit-Unity-Client-Quest/blob/05ad3f081e64c400d8eda34c0efdf711c47f6b3a/Assets/Scripts/Network/TcpHandler.cs): tracking/discovery/SDK endpoints and the overwritten 8888 initializer.
- [SDK 1.1.0](https://pypi.org/project/xrobotoolkit-sdk/1.1.0/) and [inspected binding](https://github.com/XR-Robotics/XRoboToolkit-PC-Service-Pybind/blob/8941e1dbbf4313fe83846f82984eaa8c992690bf/bindings/py_bindings.cpp): getter API and cached state.
- [Sample dependencies](https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python/blob/79e5cb8a56e3455515ce1b476e993c764ec58739/pyproject.toml), [legacy setup](https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python/blob/79e5cb8a56e3455515ce1b476e993c764ec58739/setup_conda.sh), and [UR5e entry point](https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python/blob/79e5cb8a56e3455515ce1b476e993c764ec58739/scripts/simulation/teleop_dual_ur5e_mujoco.py).
- [Control/clutch source](https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python/blob/79e5cb8a56e3455515ce1b476e993c764ec58739/xrobotoolkit_teleop/common/base_teleop_controller.py) and [MuJoCo loop/stop source](https://github.com/XR-Robotics/XRoboToolkit-Teleop-Sample-Python/blob/79e5cb8a56e3455515ce1b476e993c764ec58739/xrobotoolkit_teleop/simulation/mujoco_teleop_controller.py).
- [Placo 0.9.18 dependencies](https://github.com/Rhoban/placo/blob/v0.9.18/pyproject.toml), [available wheels](https://pypi.org/project/placo/0.9.18/), and [0.11.0 architecture changes](https://github.com/Rhoban/placo/releases/tag/v0.11.0).
- [MuJoCo 3.3.7 package](https://pypi.org/project/mujoco/3.3.7/) and [Python viewer documentation](https://mujoco.readthedocs.io/en/3.3.7/python.html).
- [Lab protocol](../../docs/lab-protocol.md): staged readiness, operator rehearsal, independent evidence, verified stop, and honest closeout.

All runtime expectations remain hypotheses until recorded on the intended hardware. The diagnostic snippet is an inspection aid embedded in the procedure, not a production watchdog or robot controller.

