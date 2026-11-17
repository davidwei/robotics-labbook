# Unitree G1

Owner: David Wei. Project record initialized retrospectively on 2026-10-09; earlier project history is not reconstructed here.

- **Quest Pro simulation test (minimum useful result captured 2026-11-16):** [XRoboToolkit Quest → Linux → dual-UR5e MuJoCo](../../experiments/EXP-20261115-001/plan.md)
  ([operating procedure](../../experiments/EXP-20261115-001/procedure.md),
  [experiment definition](../../experiments/EXP-20261115-001/experiment.yaml)).
  The released client produced passing input evidence and bilateral motion in the stock
  simulation after a clean app/service restart. Clutch isolation had operator deviations,
  and the stop handler required timeout kill escalation; full validation remains pending.
- **Quest Pro MuJoCo video return (bounded combined run passed 2026-11-16; review pending):**
  [live desktop return during controller operation](../../experiments/EXP-20261116-001/plan.md)
  ([experiment definition](../../experiments/EXP-20261116-001/experiment.yaml)).
  A corrected local protocol-compatible sender delivered about 192 seconds of
  2560x720 H.264 return while the operator observed right, left and bimanual
  simulation control plus released-grip clutch behavior. Quantitative review,
  tracked sender packaging and latency/integrity tests remain pending.
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
- Architecture plan: [composable VR teleoperation for XRoboToolkit/CloudXR and
  G1-29/G1-23](../../ideas/IDEA-20261116-002/README.md). The first milestone is
  G1-29 MuJoCo through standard LeRobot interfaces. Software implementation
  reached the documented Commit 12 candidate on 2026-11-16: plugin
  `0d68a65848011550393ef136b2dfe187c2ec37a6` and integration harness
  `13a272a0711e39d9e736bef0577b43f500b3e137`. Automated trace/IK/native-MuJoCo,
  plugin-discovery and video-protocol gates passed; live XRoboToolkit and CloudXR
  headset acceptance remains pending. G1-23 depends on native model/IK support,
  and no physical robot motion is authorized by the plan.
- Quest diagnostic idea: [in-headset controller motion/grip status](../../ideas/IDEA-20261116-001/README.md),
  with an unbuilt local Unity source draft; baseline released-client debugging remains the current priority.
- Long-running safety research: [controlled stock-controller handover](../../ideas/IDEA-20261015-003/README.md),
  implementation began at LeRobot `a65596cb`; later candidate physical validation failed at RUN-006
  and further physical tests remain stopped pending offline analysis and a new
  operator decision.
- Sessions:
  - [2026-11-16 Quest Pro MuJoCo video return and simultaneous control](../../sessions/2026-11-16-quest-pro-mujoco-video-return/session.md).
  - [2026-11-16 Quest Pro XRoboToolkit dual-UR5e MuJoCo](../../sessions/2026-11-16-quest-pro-xrobotoolkit-mujoco/session.md).
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
