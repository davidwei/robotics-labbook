# IDEA-20261116-002 — Composable VR teleoperation for G1-29 and G1-23

Status: proposed; architecture drafted, implementation not started. Project:
Unitree G1 / LeRobot. Readiness: ready for an interface-and-baseline development
pass using G1-29 simulation. Physical validation: not started and not authorized
by this idea.

## Objective

Create one LeRobot-compatible VR teleoperation architecture in which the VR input
source and G1 embodiment are independent configuration choices. The intended
matrix is:

| VR input source | Retargeter | Robot backend |
| --- | --- | --- |
| XRoboToolkit | G1-29 IK | MuJoCo first; physical robot only under a later plan |
| CloudXR | G1-29 IK | MuJoCo first; physical robot only under a later plan |
| XRoboToolkit | G1-23 IK | Native G1-23 MuJoCo first; physical robot later |
| CloudXR | G1-23 IK | Native G1-23 MuJoCo first; physical robot later |

The first milestone is deliberately narrower: XRoboToolkit controller input to
the upstream-compatible G1-29 MuJoCo simulation through the standard LeRobot
robot and teleoperator interfaces.

## Proposed architecture

```text
                         VR input source
                 +---------------+---------------+
                 |                               |
        XRoboToolkit adapter              CloudXR adapter
                 +---------------+---------------+
                                 |
                    normalized XR state
       poses, buttons, grip, timestamps and tracking validity
                                 |
              shared interaction and safety state machine
       clutch, relative rebase, freshness, hold and reconnect state
                                 |
                         G1 retargeting API
                 +---------------+---------------+
                 |                               |
              G1-29 IK                        G1-23 IK
                 +---------------+---------------+
                                 |
                   named LeRobot RobotAction
                                 |
                    LeRobot Unitree G1 robot
                 +---------------+---------------+
                 |                               |
              MuJoCo                         physical G1
```

Video return is a parallel operator-visualization path, not part of IK or the
robot command loop:

```text
MuJoCo viewer or robot camera -> video sender -> headset display
```

## Component contracts

### 1. VR input source

Define an `XRInputSource` contract and source-specific implementations such as
`XRoboToolkitSource` and `CloudXRSource`. Each implementation owns only transport,
SDK lifecycle and conversion into a shared XR sample. The shared sample should
include:

- monotonically captured host time and, where available, source timestamp;
- left and right controller poses in a documented normalized coordinate frame;
- grip, trigger and relevant buttons;
- per-controller tracking validity;
- source connection and freshness status.

Source adapters must not contain G1 joint names, G1 IK or robot command logic.
Coordinate-frame conversion at this boundary must be explicit and tested; it is
not yet established that XRoboToolkit and CloudXR expose identical pose semantics.

### 2. Shared interaction and safety state machine

Implement clutch and failure behavior once for every source and embodiment:

- a grip press captures controller and end-effector reference poses;
- held grip applies relative motion from those references;
- releasing grip holds the corresponding arm target;
- stale, invalid or disconnected input cannot advance a target;
- recovery requires fresh samples and a new grip edge, preventing a reconnect
  jump from an old reference;
- status exposes `disconnected`, `stale`, `ready`, `clutched-left`,
  `clutched-right` and IK failure/saturation for logs and eventual headset UI.

The stale threshold and grip threshold are configuration, while the fail-hold and
re-clutch rules are invariant safety behavior.

### 3. G1 retargeting API

Define a source-independent `G1Retargeter` contract. It consumes desired left and
right end-effector targets plus current robot state and returns named LeRobot
joint targets and diagnostics. Provide separate `G129Retargeter` and
`G123Retargeter` implementations or one implementation parameterized by an
explicit, tested embodiment profile.

Each embodiment profile owns:

- URDF/model identity and link/frame names;
- controlled joint names and order;
- joint limits, neutral posture and frozen-joint policy;
- solver configuration and seed behavior;
- mapping from solver output to LeRobot action keys;
- compatibility with end-effector variants.

The retargeter must report infeasible targets and limit saturation. It must not
silently substitute the G1-29 model for a requested G1-23 embodiment.

### 4. LeRobot integration

Expose the composition through a third-party LeRobot teleoperator plugin, with a
working name such as `lerobot_teleoperator_g1_vr`. A `G1VRTeleoperator` composes
one `XRInputSource`, the shared interaction controller and one `G1Retargeter`, and
returns ordinary named `RobotAction` values. The implementation should follow the
existing upstream `UnitreeG1Teleoperator` pattern rather than patching the core
teleoperation loop.

The LeRobot `UnitreeG1` robot remains responsible for simulation or hardware
transport, observations, command publication, timing and shutdown. The app and
input adapters remain robot-agnostic. Reject a retargeter/robot embodiment
mismatch at startup unless a deliberate mapping policy has been configured and
tested.

Illustrative configuration, subject to the current upstream config schema:

```yaml
teleop:
  type: g1_vr
  source:
    type: xrobotoolkit       # later: cloudxr
  retargeter:
    embodiment: g1_29       # later: g1_23
  clutch_button: grip
  stale_timeout_s: 0.5

robot:
  type: unitree_g1
  embodiment: g1_29
  is_simulation: true
```

Current LeRobot `main` may not expose the historical `embodiment` field in this
exact form. The discovery pass must reconcile the merged embodiment work with the
current `UnitreeG1Config` and avoid designing against an obsolete constructor.

## Phased plan

### Phase 0 — Pin current interfaces and prove the baseline

1. Record the exact LeRobot revision and inspect the current `UnitreeG1`,
   `UnitreeG1Config`, teleoperator plugin discovery and G1 IK interfaces.
2. Run a bounded upstream G1-29 MuJoCo baseline without a headset or external VR
   source; preserve command, model and shutdown evidence.
3. Inventory the existing CloudXR G1-29 operator and the successful XRoboToolkit
   Quest/dual-UR5e path as behavior references, not as architecture to copy.
4. Decide the external plugin repository/package location and dependency boundary.

Exit: one recorded, reproducible G1-29 simulation baseline and a versioned set of
interfaces. No VR implementation begins against an unverified source tree.

### Phase 1 — Normalized XR input and safety behavior

1. Specify the normalized XR sample and coordinate conventions.
2. Implement `XRoboToolkitSource` with fake-SDK tests for lifecycle, field mapping,
   timestamps, stale input and disconnect/reconnect.
3. Implement and test the shared clutch/rebase/fail-hold state machine with
   deterministic pose sequences.
4. Add structured diagnostics suitable for logs and eventual headset status.

Exit: recorded controller samples can be replayed without MuJoCo, and stale or
invalid samples never advance an arm target.

### Phase 2 — G1-29 retargeting and LeRobot simulation

1. Adapt or wrap the established G1-29 arm IK behind `G1Retargeter`.
2. Test neutral pose, relative translations/rotations, joint limits, infeasible
   targets and left/right isolation using deterministic fixtures.
3. Package `G1VRTeleoperator` as a third-party LeRobot plugin and verify factory
   discovery without modifying LeRobot core.
4. Run simulation-only stages: replay input, live input without headset video,
   then live XRoboToolkit input with the independent video-return sidecar.
5. Confirm right-only, left-only, bimanual and released-grip hold behavior while
   preserving source timestamps and commanded/observed joints.

Exit: the released XRoboToolkit Quest app controls G1-29 arms in MuJoCo through
the LeRobot interfaces, with explicit reconnect/freshness behavior and no physical
robot command path.

### Phase 3 — CloudXR source substitution on G1-29

1. Implement `CloudXRSource` against the same normalized XR contract.
2. Use common recorded-pose conformance tests to compare axes, handedness,
   quaternion convention, button semantics, freshness and reconnect behavior.
3. Run the same G1-29 simulation acceptance sequence without changing the
   retargeter or LeRobot robot layer.

Exit: source selection is configuration, and both sources pass the same shared
interaction and G1-29 retargeting tests.

### Phase 4 — Native G1-23 retargeting and simulation

1. Complete the native G1-23 model/asset discovery and simulator plumbing tracked
   in [IDEA-20261027-001](../IDEA-20261027-001/README.md).
2. Define and test the G1-23 kinematic profile and IK implementation without
   altering either VR source adapter.
3. Reject model/action dimension and embodiment mismatches explicitly.
4. Run recorded input and then live XRoboToolkit and CloudXR acceptance sequences
   against native G1-23 MuJoCo.

Exit: both VR sources operate the actual selected G1-23 simulation model through
the same LeRobot integration. Hidden-joint use of a G1-29 body does not count as
native G1-23 validation.

### Phase 5 — Physical validation, separately authorized

Physical G1-29 or G1-23 work requires a new pre-lab plan, matching hardware and
firmware provenance, guarded command limits, independent stop authority and
simulation evidence at the exact candidate revision. Nothing in this architecture
plan authorizes DDS connection or physical robot motion.

## Acceptance criteria

- Adding a VR source requires no edits to either G1 retargeter.
- Adding an embodiment requires no edits to either VR source adapter.
- Identical recorded normalized XR samples produce source-independent retargeter
  outputs within documented numerical tolerances.
- Released grip, stale tracking, disconnect and reconnect never produce an
  uncommanded target jump.
- G1-23 and G1-29 profiles expose explicit model, joint and action identities;
  incompatible combinations fail before command publication.
- The plugin is discoverable by standard LeRobot tooling without a LeRobot-core
  patch.
- Video failure does not block safe command-loop shutdown, and command failure is
  visible even if video continues.
- Simulation evidence remains distinct from any later physical validation claim.

## Repository and evidence plan

Target code location: choose or create a tracked external LeRobot teleoperator
plugin repository during Phase 0; do not leave the reusable adapter only in an
untracked experiment directory. Likely dependencies include current LeRobot,
XRoboToolkit SDK, the existing G1 kinematics stack and the CloudXR input client.
Keep transport SDKs optional so installing one source does not require the other.

For each phase preserve the code revision, environment lock, model/asset revision,
configuration, normalized input trace, IK diagnostics, commanded and observed
joint telemetry, logs and bounded video where useful. Treat headset observations
as operator observations rather than quantitative latency or reliability evidence.

## Dependencies and related work

- [IDEA-20261027-001](../IDEA-20261027-001/README.md): native G1-23 MuJoCo model
  and embodiment-selection plumbing; prerequisite for Phase 4 simulation claims.
- [EXP-20261115-001](../../experiments/EXP-20261115-001/plan.md): successful
  XRoboToolkit Quest controller path to dual-UR5e MuJoCo.
- [EXP-20261116-001](../../experiments/EXP-20261116-001/plan.md): successful
  bounded XRoboToolkit desktop-video return during simulation control.
- [IDEA-20261027-003](../IDEA-20261027-003/README.md): prior CloudXR G1-29
  simulation and headset-client evidence, with recorded browser/client limits.
- LeRobot PR #4651: historical explicit embodiment support; current-main API must
  be verified before implementation.

## Next action

When work resumes, perform Phase 0 only: pin the current LeRobot revision, run the
bounded G1-29 MuJoCo baseline, and write the normalized XR and `G1Retargeter`
interface definitions before changing the live operator. Recommended target is
G1-29 simulation with no physical DDS path. Prerequisites are a clean tracked
plugin workspace, current LeRobot source, the known G1-29 model assets and access
to the existing XRoboToolkit/CloudXR reference implementations.
