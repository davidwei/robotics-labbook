# SO101 Linux demo migration

Source snapshot: bd49580152521e054218c1f41dd5b9bfeacc3d75, MoissanClub/lerobot branch lab/so101-intel-warning-20261023. Same launcher used in the successful children’s demo (operator report,25 children; not a verified count of25saved episodes). Source plus current arm calibration files included; no recorded videos, session datasets, credentials or Mac virtual environment included.

Linux hardware validation pending. Commands below assume Ubuntu/Debian with a graphical desktop and Python3.11 or3.12 available. Confirm target distribution/architecture before installing. Dependencies are resolved for Linux from this snapshot's pyproject, not the incompatible Mac lockfile; Linux dependency equivalence is not yet tested.

## Install on Linux

Extract so101-linux-20261031.tar.gz into an empty working directory (e.g. ~/lerobot); the directory contains this README, calibration/, configure.py, demo_so101.sh, and lerobot-source.tar.gz. Run from that directory:

```bash
sudo apt update
sudo apt install python3-venv python3-dev build-essential cmake pkg-config ffmpeg v4l-utils speech-dispatcher espeak-ng libgl1 libegl1 libxkbcommon0
# If your distro uses other serial/video groups, use its equivalent permissions.
sudo usermod -aG dialout,video "$USER"
# Log out and back in for new group membership.
tar -xzf lerobot-source.tar.gz
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e './lerobot-src[feetech]'
.venv/bin/python -m pip check
```

Use a local graphical desktop Terminal (X11/XWayland may be required by pynput imports); a plain headless SSH session does not provide the Rerun display. No GPU is required for this teleoperation/record/replay workflow. Rerun viewer is supplied by rerun-sdk; wrapper configures active virtual environment. Source path defaults assume lerobot-src is directly beneath this working directory.

## Identify devices and generate config

```bash
ls -l /dev/serial/by-id/
v4l2-ctl --list-devices
```

Identify leader/follower by unplugging one at a time. Prefer distinct /dev/serial/by-id paths if exposed; otherwise use verified /dev/ttyACM* or /dev/ttyUSB* nodes. One camera may expose multiple /dev/video* nodes; choose a capture-capable node. Camera0/1 are examples, not guaranteed bindings. Confirm high mount vs gripper by covering each lens. Existing Mac camera serial inventory is not bound to roles.

```bash
python3 configure.py --follower-port /dev/ttyACM0 --leader-port /dev/ttyACM1 --high-camera 0 --gripper-camera 2 --fps 10
bash demo_so101.sh check --config record-linux.json
spd-say --wait 'Slow down'
.venv/bin/python -c 'import lerobot, torch, cv2, av, rerun; print("Imports OK")'
.venv/bin/lerobot-record --help
.venv/bin/lerobot-replay --help
```

For camera-only confirmation before arm setup (does not command motors):
```bash
.venv/bin/python -m lerobot.scripts.lerobot_camera_views --indices 0 2 --preview-only
```

Replace example indices with actual selected indices. Preview-only does not save configuration; if identities are reversed, preserve/remove record-linux.json and regenerate with corrected mapping. OpenCV indices can change after reconnect. Camera acquisition stays30FPS; recorder and follower command rate default10Hz.

## Rehearse, then demo

```bash
bash demo_so101.sh launch --config record-linux.json --label linux_trial --episodes 2
# After a successful short record and replay, quit and create the demo session:
bash demo_so101.sh launch --config record-linux.json --label childrens_demo --episodes 27
```

Startup interactively runs follower then leader calibration. For these same unchanged arms press Enter to restore saved values; c measures new ranges. Do not reuse these files for physically different/reassembled arms without checking calibration. Support arms during setup. No automatic home. Ready S starts, Right Arrow/F saves, Left Arrow discards active attempt to Ready, R replays last saved, Q quits. Five-minute episode cap. Align follower near first recorded pose before replay. Keep launcher Terminal focused. Save can take time; wait for COMMITTED. Release/disconnect requires supporting follower.

Always pass --config record-linux.json for a NEW session: default config points to the old Mac workbench path. Resume existing session with `bash demo_so101.sh list` then `bash demo_so101.sh launch --session EXACT_SESSION_NAME`; resume uses stored config.

Logs, telemetry, camera videos and datasets are local under outputs/demo/so101/. Upload disabled. Linux uses full snapshot copies rather than the Mac APFS clones; retained checkpoints can grow approximately quadratically with episode count and staging can become slow. Plan disk space and measure this in the trial. Do not delete checkpoints during a live session.

Reference: https://huggingface.co/docs/lerobot/so101 (Feetech install/device setup). This is a historical fork snapshot; do not substitute current upstream main, whose Python/dependency requirements differ.

## Retrieve from the private labbook

Authenticate gh with access to davidwei/robotics-labbook. Download into an empty working directory:

```bash
mkdir -p ~/lerobot
cd ~/lerobot
gh release download so101-linux-20261031 --repo davidwei/robotics-labbook --pattern so101-linux-20261031.tar.gz
sha256sum so101-linux-20261031.tar.gz
# Compare SHA256 with sessions/2026-10-31-so101-linux-migration/evidence.json before extracting.
tar -xzf so101-linux-20261031.tar.gz
```

For Git provenance in future session.json files, prefer replacing the source extraction step with a pinned checkout:
```bash
git clone --branch lab/so101-intel-warning-20261023 https://github.com/MoissanClub/lerobot.git lerobot-src
git -C lerobot-src checkout --detach bd49580152521e054218c1f41dd5b9bfeacc3d75
```
Use either Git clone or source archive, not both into the same directory. The archive is an exact fallback but contains no .git; if used, retain manifest.json because launcher source_revision will be empty. mac-environment-reference.json is the working Mac package inventory, not a Linux lock. After Linux rehearsal, preserve its actual pip freeze, OS and Python versions as separate validated provenance.
