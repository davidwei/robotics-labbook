# IDEA-20261023-001 — SO101 pickup mode after loss of synchronization

Status: proposed; implement after the current threshold-measurement experiment.
Target: MoissanClub/lerobot, SO101 leader/follower. Physical validation: pending.

The operator requests a pickup mode when the follower is stuck or out of sync:
disengage following, prompt the operator to align the leader with the measured
follower pose, then explicitly resume without a target jump. Do not implement or
physically test this during the current threshold experiment.

Reference: [G1 VR session](../../sessions/2026-10-15-g1-vr-camera/session.md),
code reference `4d9d9724` on `work/g1-vr-physical`. It reports four virtual pickup
entries and 1,295 following samples without target jumps; physical hold was not
validated and physical preparation failed before pickup. Reuse the alignment
concept, not unverified physical-stop or authority-handover assumptions.

Next agent action: after reviewing threshold telemetry, design the SO101 pickup
state machine and follower hold policy, inspect G1 code/evidence at exact revisions,
and add mocked/simulation transition tests before supervised physical validation.
Prerequisites: fresh feedback, defined per-joint alignment tolerances and dwell,
explicit resume, and a distinction between lag, an obstacle and hardware fault.
Do not assume large position error proves a collision. Never keep commanding an
unreachable leader target or automatically force/reverse through an obstruction.
Torque-off can drop an unsupported arm; holding can sustain contact force. The
recovery policy and operator support/obstacle-clearance steps need explicit design.
Recording must mark or pause/discard interrupted episodes during pickup.

Current threshold logging is observational and does not implement pickup or any
automatic motion/stop behavior. No physical pickup validation is claimed.
