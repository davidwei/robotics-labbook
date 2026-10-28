# PICO 4 loan evaluation

Owner: David Wei. Status: time-boxed discovery and validation. A friend lent the
operator a PICO 4-family headset with two foot trackers; the equipment must be
returned by Friday, 2026-10-30. The headset regulatory model is `A8110`. Published
regulatory evidence uses A8110 for both PICO 4 and PICO 4 Pro, so the marketed
variant remains unresolved. Direct device inspection reports Android 10 and software
version/build `202403120341`. No eye-tracking or face-tracking setting was visible,
which is evidence consistent with standard PICO 4 but is not conclusive model
identification. The device shows one pair of motion trackers (two trackers).
Controller inventory and tracker firmware remain to be recorded.

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
