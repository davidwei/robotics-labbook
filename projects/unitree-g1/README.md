# Unitree G1

Owner: David Wei. Project record initialized retrospectively on 2026-10-09; earlier project history is not reconstructed here.

- Experiment: [G1 embodiment compatibility](../../experiments/EXP-20261009-001/experiment.yaml).
- **Next lab visit (planned 2026-11-11):** [CloudXR no-ADB client-first bookmark experiment](../../experiments/EXP-20261111-001/plan.md)
  ([experiment definition](../../experiments/EXP-20261111-001/experiment.yaml)).
  Test whether the NVIDIA-hosted client remembers each server IP across certificate acceptance,
  browser restart, and a second server, versus bookmarking each server's locally hosted
  `https://HOST:48322/client/` page. Success means entering each server IP no more than
  once during setup and never retyping it on subsequent bookmarked visits. Browser/headset
  connectivity only; no physical robot motion. Record actual results before deciding
  whether [IsaacCapture PR #1170](https://github.com/NVIDIA/IsaacCapture/pull/1170)
  adds value over NVIDIA's documented client-first flow.
- Follow-up idea: [native G1-23 MuJoCo embodiment support](../../ideas/IDEA-20261027-001/README.md),
  based on the maintainer guidance after PR #4651 approval.
- Long-running safety research: [controlled stock-controller handover](../../ideas/IDEA-20261015-003/README.md),
  implementation began at LeRobot `a65596cb`; later candidate physical validation failed at RUN-006
  and further physical tests remain stopped pending offline analysis and a new
  operator decision.
- Sessions:
  - [2026-11-03 PICO voice/controller physical run](../../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md).
  - [2026-11-03 PICO voice/controller input-only dry rehearsal](../../sessions/2026-11-03-g1-sonic-pico-voice-dryrun/session.md).
  - [2026-10-30 PC2 SONIC bring-up and four gantry-protected physical diagnostics](../../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md).
  - [2026-10-29 planned PICO/SONIC G1-29 readiness and planted-feet demo](../../sessions/2026-10-29-g1-sonic-planted-feet/pre-lab.md).
  - [2026-10-16 handover trials, RUN-006 failure and stopped series](../../sessions/2026-10-16-g1-handover/session.md).
  - [2026-10-15 G1 VR camera/input validation and physical preparation faults](../../sessions/2026-10-15-g1-vr-camera/session.md).
  - [2026-10-08 G1-29 MuJoCo regression](../../sessions/2026-10-08-g1-29-mujoco-regression/session.md).
  - [2026-10-09 G1-29 physical regression](../../sessions/2026-10-09-g1-29-regression/session.md).

Source code remains in huggingface/lerobot and MoissanClub/lerobot. No reviewed findings recorded yet.

## Embodiment validation history

On 2026-10-15, David Wei reported that a peer verified G1-23 with both **Holosoma**
and **GR00T** controllers. Treat this as peer-reported verification, separate from
locally captured G1-29 runs. Peer identity, actual test dates, code/configuration,
test environment and raw evidence references have not yet been supplied. Details
are recorded in the [experiment](../../experiments/EXP-20261009-001/experiment.yaml).
Initial G1-23 validation is therefore no longer listed as unperformed; attaching
peer provenance remains open. The earlier G1-29 session record remains historical
and its post-lab review is still pending.

PR #4651 merged into `huggingface/lerobot:main` on 2026-10-19 at merge commit
`3991580a5673f5f0219a4e8835a5f973eeccf9a7`. The maintainer-endorsed simulation
follow-up is tracked separately in IDEA-20261027-001; it requires coordinated
LeRobot and Hub-model changes and does not extend the physical-validation claim.

## Session review status

The dated embodiment update above describes PR #4651; it is not the latest result across all G1 work. SONIC/PICO physical progress is indexed in [IDEA-20261027-002](../../ideas/IDEA-20261027-002/README.md) and [the PICO project](../pico-4-loan/README.md). October 30 includes an unexpected POSE leg tuck and loss of standing after stop. The November 3 physical record reports one completed sequence, a repeat protocol deviation, a recorder gap and verified stock damp cleanup. None validates untethered use or the failed October 16 Arm SDK handover.

All eight G1 session directories are linked above, including the October 29 planned-only record. Next: offline input/command/state alignment for SONIC and separate RUN-006 handover review. Session labels through November 3 are retained as recorded; see [audit scope/date caveat](../../docs/session-reference-audit.md).
