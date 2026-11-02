# PICO 4 loan evaluation

Owner: David Wei. Status: time-boxed discovery and validation. A friend lent the
operator a PICO 4-family headset with two foot trackers; the equipment must be
returned by Friday, 2026-10-30. The headset regulatory model is `A8110`. Published
regulatory evidence uses A8110 for both PICO 4 and PICO 4 Pro, so the marketed
variant remains unresolved. Direct device inspection reports Android 10 and software
version/build `202403120341`, with PICO system version `5.20`. No eye-tracking or
face-tracking setting was visible,
which is evidence consistent with standard PICO 4 but is not conclusive model
identification. The device shows one pair of motion trackers (two trackers).
Controller inventory and tracker firmware remain to be recorded.

The headset reports no system update beyond PICO system version `5.20`, and its
Library/Updates view offers no application updates. The installed PICO Browser remains
Chromium 105, below NVIDIA's current CloudXR client requirement of Chrome 125. Treat
the Isaac Teleop browser path as blocked for this loan window unless an owner-approved,
official PICO update path becomes available.

Objectives:

1. [Verify NVIDIA SONIC with PICO whole-body and foot tracking](../../ideas/IDEA-20261027-002/README.md).
2. [Evaluate PICO compatibility with NVIDIA Isaac Teleop](../../ideas/IDEA-20261027-003/README.md).

Priority is driven by the temporary hardware window. Preserve device/firmware
inventory and raw tracking evidence early, because software work can continue after
the headset is returned. Discovery, input inspection and simulation do not authorize
physical robot motion. Any real-G1 test requires a separate pre-lab plan and explicit
operator authorization.

Time-box: treat Thursday, 2026-10-29 as the evidence deadline and retain Friday as
recovery, final inventory and return buffer. Minimum useful evidence is the exact
device identity plus a calibrated tracking/schema capture; do not consume the loan
window on real-robot preparation before that evidence is secured.

## Recorded session progress

The October 30 return deadline above is the original plan. Later session labels extend through November 3; a revised loan/return date is not documented. This index reports the checked-in evidence, not current equipment availability.

- [October 29 SONIC readiness/demo plan](../../sessions/2026-10-29-g1-sonic-planted-feet/pre-lab.md): planned only.
- [October 30 PC2 bring-up and physical diagnostics](../../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md): input transport and gantry-protected tests; unexpected POSE leg tuck, no automatic stock handover, later bent/frozen PICO capture.
- [November 3 voice/controller dry rehearsal](../../sessions/2026-11-03-g1-sonic-pico-voice-dryrun/session.md): input-only arming sequence; posture must match the operator.
- [November 3 physical workflow](../../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md): one completed sequence, repeat protocol deviation and recorder gap; stock damp restored explicitly at cleanup.

The Isaac Teleop October 27–28 attempts are documented inside [IDEA-20261027-003](../../ideas/IDEA-20261027-003/README.md), with no standalone session found. SONIC simulation/input evidence does not resolve that browser compatibility boundary. Next: align the physical input/command/state evidence; reconfirm loan availability and recalibrate after headset removal before any later authorized test. Gantry-only restrictions remain.
