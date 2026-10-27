# Unitree G1

Owner: David Wei. Project record initialized retrospectively on 2026-10-09; earlier project history is not reconstructed here.

- Experiment: [G1 embodiment compatibility](../../experiments/EXP-20261009-001/experiment.yaml).
- Follow-up idea: [native G1-23 MuJoCo embodiment support](../../ideas/IDEA-20261027-001/README.md),
  based on the maintainer guidance after PR #4651 approval.
- Long-running safety research: [controlled stock-controller handover](../../ideas/IDEA-20261015-003/README.md),
  software candidate at LeRobot `a65596cb`; physical validation failed at RUN-006
  and further physical tests remain stopped pending offline analysis and a new
  operator decision.
- Sessions:
  - [2026-10-16 handover validation preparation](../../sessions/2026-10-16-g1-handover/session.md).
  - [2026-10-15 G1 VR camera validation (partial pass; headset pending)](../../sessions/2026-10-15-g1-vr-camera/session.md).
  - [2026-10-08 G1-29 MuJoCo regression](../../sessions/2026-10-08-g1-29-mujoco-regression/session.md).
  - [2026-10-09 G1-29 physical regression](../../sessions/2026-10-09-g1-29-regression/session.md).

Source code remains in huggingface/lerobot and MoissanClub/lerobot. No reviewed findings recorded yet.

## Latest validation update

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
