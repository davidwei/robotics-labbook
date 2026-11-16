# IDEA-20261116-001 — Add in-headset controller motion diagnostics to XRoboToolkit Quest

Status: proposed; local source draft exists, but it has not been compiled, installed, or tested.
Project: [Unitree G1](../../projects/unitree-g1/README.md). Related experiment: [EXP-20261115-001](../../experiments/EXP-20261115-001/plan.md).
Target: `XR-Robotics/XRoboToolkit-Unity-Client-Quest`; Meta Quest Pro and Touch Pro controllers.
Physical validation: not started. No physical robot is in scope.

## Objective

Make the Quest client itself show whether it considers each controller pose valid and whether the pose is changing, without requiring a competing Python SDK client on the PC. Also show each side-grip analog value and the current Controller/Send toggle states. This should separate headset-side tracking/UI faults from Quest-to-PC transport and simulator-consumer faults during XR teleoperation bring-up.

Proposed compact Status display:

```text
L:MOVING g1.00   R:STILL g0.00
Tracking:ON   Send:ON
```

Use `LOST` when the Quest tracking source reports an invalid controller pose. Keep `MOVING` visible briefly after a small pose change so the operator can read it while wearing the headset.

## Follow-on: end-to-end tracking health and reconnect prompt

During `EXP-20261116-001`, the released app showed a connected state while the
simulator received no controller operation; operator reconnect restored control.
The current `WORKING` display reflects the headset TCP socket state. The existing
heartbeat code sends every 10 seconds but does not maintain a server-response age
or prove that tracking reaches an SDK consumer.

Add a distinct transport-health display only after defining an end-to-end
acknowledgment, preferably a PC Service acknowledgment carrying the latest
tracking sequence/source timestamp:

```text
CONNECTED — DATA FLOWING
CONNECTED — DATA STALE: RECONNECT
DISCONNECTED — RECONNECTING
```

When Send is on and acknowledgment age exceeds a reviewed threshold (initial
candidate: 2–3 seconds), present a prominent **Reconnect now** action using the
existing `TcpHandler.Reconnect()` path. Do not infer PC receipt merely from local
controller motion; that would reproduce the same false-positive boundary this
diagnostic is intended to expose. This follow-on likely requires a compatible PC
Service change and version negotiation, not only a Unity UI edit.

## Local draft

A source-only draft was made on 2026-11-16 from upstream commit `07a28333341629008187e988b73b48bced316092` at `/home/dwei/meta_quest_xrobotoolkit/XRoboToolkit-Unity-Client-Quest`. It:

- updates the existing Tracking Status field at 10 Hz;
- reads the same `QuestTrackingDataSource` poses used by outgoing tracking data;
- classifies motion at 2 mm or 1 degree and holds `MOVING` for 0.4 seconds;
- displays left/right grip values from the XR input devices;
- hardens controller-validity checks against missing serialized references;
- uses a separate product/package identity, `XRoboToolkit-Quest-MotionDiag` / `com.xrobotoolkit.client.quest.motiondiag`, so it can coexist with the released app.

The dirty local draft is not a durable code revision and is not evidence of a working APK. Static whitespace and delimiter-balance checks passed. No Unity compilation, Android build, installation, or headset validation was performed.

## Prerequisites and next action

Prerequisites: Unity `2021.3.45f2`, its Android build module, a valid Unity license, resolved Meta XR packages, authorized Quest ADB installation, and a preserved released-app fallback. The current desktop has no Unity editor or detected license.

Next agent action: defer toolchain installation until this diagnostic is explicitly prioritized. Before building, specify the PC acknowledgment/version contract for the stale-data prompt. Then build the separate package, inspect compile/build reports, install alongside the released app, and validate `LOST`/`STILL`/`MOVING`, grip values, Send-off behavior, acknowledgment loss, stale-data prompting and manual reconnect recovery. Do not replace the released APK or generalize local UI motion into transport/simulator validation.
