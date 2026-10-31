# IDEA-20261027-001 — Native G1-23 MuJoCo embodiment support

Status: proposed; ready for repository and model discovery, implementation not
started. Project: Unitree G1 / LeRobot. Physical validation: not started and not
authorized by this idea.

## Objective

Extend the explicit G1-23 embodiment support merged in
[LeRobot PR #4651](https://github.com/huggingface/lerobot/pull/4651) so selecting
`g1_23` loads and controls a native 23-DoF MuJoCo body instead of silently using
the G1-29 simulation model.

## Maintainer guidance

The approving review on PR #4651 identified the intended integration direction:

1. Model changes must also land in the Hub model repository
   [`lerobot/unitree-g1-mujoco`](https://huggingface.co/lerobot/unitree-g1-mujoco/tree/main).
2. `UnitreeG1MujocoEnv` must pass the robot configuration's `embodiment` through
   to the simulator's `robot_type`, following the existing end-effector/gripper
   selection pattern. Without this plumbing, the simulator continues loading the
   29-DoF body.
3. Review [LeRobot PR #4888](https://github.com/huggingface/lerobot/pull/4888)
   for related simulation work before choosing the implementation boundary.

Source: [maintainer approval and follow-up guidance](https://github.com/huggingface/lerobot/pull/4651#pullrequestreview-5576535476).

## Proposed first pass

1. Inspect current LeRobot `main`, PR #4888 and the current Hub model contents;
   identify ownership, versioning and contribution paths for code versus assets.
2. Inventory the G1-23 model assets and establish whether a native, redistributable
   MuJoCo/URDF model already exists. Do not derive a 23-DoF model merely by hiding
   joints in the G1-29 body without documenting the dynamics consequences.
3. Define one embodiment-selection contract from `UnitreeG1Config` through
   `UnitreeG1MujocoEnv` to the simulator's `robot_type`, with an explicit error for
   missing or unsupported assets rather than fallback to G1-29.
4. Add focused tests proving that G1-23 and G1-29 select their intended model,
   joint/action mapping, controller compatibility and observation dimensions.
5. Run the existing G1-29 MuJoCo regression before proposing any physical test.

## Acceptance and evidence limits

- `g1_23` selects a native 23-DoF model end to end; `g1_29` behavior remains
  compatible.
- Missing G1-23 assets fail clearly and never load the G1-29 body silently.
- Sparse DDS/runtime mappings remain distinct from simulator model indexing.
- Tests cover embodiment plus end-effector combinations and unsupported controller
  combinations.
- Simulation validates software/model integration only. It does not establish
  hardware dynamics, controller safety or physical G1-23 behavior.

Next agent action: perform the code/Hub/PR #4888 discovery pass and produce a
minimal cross-repository implementation plan. Prerequisites: access to current
LeRobot main and the Hub model repository, confirmation of available G1-23 model
assets and their licensing/provenance. Recommended execution is offline first; no
robot or lab access is required for discovery and software validation.
