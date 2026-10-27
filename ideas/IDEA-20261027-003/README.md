# IDEA-20261027-003 — Evaluate PICO 4 with NVIDIA Isaac Teleop

Status: time-sensitive; ready for compatibility discovery and input-only connection
test. Project: PICO 4 loan evaluation / NVIDIA Isaac Teleop. Physical robot
validation: not started and not authorized. Related:
[SONIC foot-tracking evaluation](../IDEA-20261027-002/README.md).

## Objective and uncertainty

Determine whether the borrowed PICO 4 can connect to the installed NVIDIA Isaac
Teleop/CloudXR path and expose usable headset/controller tracking. Then determine
whether that input can drive NVIDIA's SONIC PICO streamer in simulation through
`--input-source isaac-teleop`.

Do not initially assume Isaac Teleop exposes the PICO ankle trackers. NVIDIA's
current Isaac Capture device table explicitly lists PICO 4 Ultra controller and hand
tracking, while the GR00T whole-body stack separately documents PICO foot tracking
through XRoboToolkit and also provides an Isaac Teleop input backend. The borrowed
device is described only as PICO 4. Exact model, OS, WebXR/CloudXR client behavior
and foot-tracker availability through DeviceIO must therefore be measured.

Primary references:

- [NVIDIA Isaac Capture supported devices](https://docs.nvidia.com/isaaclab/features/isaac-capture)
- [GR00T Whole-Body Control Isaac Teleop setup](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/tutorials/isaac_teleop_publisher_setup.md)
- Local bring-up notes: `unitree_g1_lerobot/docs/Rung0_isaac-teleop-install-notes.md`

## Validation ladder

1. Record exact headset model and OS, browser/client version, controllers, tracker
   inventory, workstation Isaac Teleop/CloudXR versions and network topology.
2. Start CloudXR/Isaac Teleop without a robot. Confirm HTTPS/client connection,
   rendered stream and finite head/controller poses. Record reconnect, controller
   buttons, tracking loss and shutdown behavior.
3. Inspect the actual DeviceIO/output schema. Explicitly record whether ankle/foot
   trackers appear, how they are labeled and whether their transforms update. Absence
   is a compatibility result, not a reason to synthesize foot poses.
4. If basic input works, run the GR00T PICO streamer with
   `--input-source isaac-teleop` and visualization only. Compare pose coverage,
   coordinate frames and latency with the XRoboToolkit path.
5. If the full SONIC reference is available through this backend, exercise Sim2Sim
   only. Keep the standalone Isaac Teleop compatibility result separate from SONIC
   controller validation.

## Success criteria for the loan window

- Establish and preserve a reproducible yes/no result for PICO 4 CloudXR connection
  and head/controller input.
- Enumerate the actual tracking schema, including a definitive observation about
  foot-tracker exposure through Isaac Teleop.
- Preserve exact versions, client URL/profile, logs and a minimal reconnect test.
- Prefer input-only and simulation evidence; real robot motion is unnecessary.

Next agent action: reuse the existing Isaac Teleop/CloudXR installation to run a
no-robot PICO connection and DeviceIO schema capture. Prerequisites: exact headset
OS/model, HTTPS-capable PICO browser/client, charged controllers, same-network access
and current CloudXR firewall/certificate setup. If plain PICO 4 is unsupported by the
current client, preserve the failure boundary and prioritize XRoboToolkit/SONIC
tracking before the loan ends.
