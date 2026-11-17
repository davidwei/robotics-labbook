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

The reviewable implementation sequence for that first milestone is recorded in
the [G1-29 + XRoboToolkit commit-by-commit plan](g1-29-xrobotoolkit-commit-plan.md).
The [trace-driven development plan](trace-driven-development.md) makes recorded
raw and normalized headset trajectories the primary input for headset-free IK,
clutch, simulator and regression work.

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

### 1a. Record/replay boundary for development efficiency

Treat capture and replay as part of the architecture, not an experiment-only
utility. Every live `XRInputSource` must support a recorder decorator, and a
`TraceReplaySource` must implement the same source contract:

```text
live source -> raw recorder -> normalization -> normalized recorder -> control
                                             ^
                                             |
                                  TraceReplaySource
```

Preserve both raw source values and normalized XR samples. Raw traces allow
coordinate/timestamp conversion to be corrected without recapturing the headset;
normalized traces are portable inputs for clutch, retargeting and simulator
regressions. Commanded and observed robot joints remain downstream evidence and
must not replace controller-intent traces.

Control time must be injectable. Deterministic replay advances a trace clock
without sleeping; real-time replay maps recorded elapsed time to the current host
clock. Freshness and reconnect logic must use the injected clock so old absolute
monotonic timestamps do not make valid replay data stale.

The normal development loop is therefore:

1. implement and fake-test a source adapter;
2. use the headset briefly to capture a small raw/normalized trace suite without
   MuJoCo or a robot backend;
3. develop clutching, IK and simulation primarily from deterministic trace
   replay;
4. use the headset again only for a bounded live integration comparison;
5. add video return after input-only live control passes.

This separation reduces headset dependency but does not replace final live tests
of transport latency, SDK lifecycle, device coordinate behavior, UI or operator
comfort. The detailed schema, capture suite, clocks and evidence rules are in the
[trace-driven development plan](trace-driven-development.md).

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

## Ownership boundary: LeRobot upstream versus Moissan extensions

Use a two-stage ownership model: broadly reusable robot capability belongs in
LeRobot and its model repository, while source-specific VR integration incubates
as a normal third-party LeRobot plugin under MoissanClub. Do not require a forked
LeRobot control loop to run the plugin.

### What should be part of LeRobot upstream

LeRobot should own behavior that is intrinsic to the supported robot or required
by every control source:

| Upstream responsibility | Rationale |
| --- | --- |
| `UnitreeG1` robot lifecycle, simulation/hardware transport, observations, command publication and shutdown | These are robot responsibilities independent of whether commands come from VR, a leader device or a policy. |
| Explicit G1-29/G1-23 embodiment selection and startup validation | The selected robot model, action space and observation space must be authoritative for every LeRobot user. |
| Joint enums/names, controlled-DoF metadata, limits and action/observation features for each embodiment | Source adapters must not carry private copies of the robot contract. |
| MuJoCo environment plumbing for each supported embodiment and end effector | Simulation model selection must not depend on a VR plugin. |
| Native G1 model assets in the established `lerobot/unitree-g1-mujoco` Hub repository, with version/provenance information | Large robot assets already have a separate upstream distribution path; they should not be duplicated in the plugin. |
| Reusable G1 forward/inverse kinematics and dynamics utilities that accept explicit embodiment profiles | IK needed by multiple teleoperators, policies or diagnostics is a robot capability, not an XR transport feature. |
| Existing `Teleoperator`, config registry, plugin discovery and standard teleoperation loop | These are the stable extension points the Moissan package should consume. |
| Small generic interface improvements proven necessary by more than this plugin | Examples could include better action-processor configuration or standardized device-health reporting, but only after a concrete gap is demonstrated. |

The upstream G1-23 contribution should be useful without a headset: a program
should be able to select a native G1-23 robot/simulator, inspect the correct
features, run its kinematics and reject incompatible actions using only LeRobot.
This work remains coordinated with
[IDEA-20261027-001](../IDEA-20261027-001/README.md).

Do not put XRoboToolkit or CloudXR SDK dependencies, Quest/PICO UI behavior,
headset reconnect rules, desktop streaming, experiment launchers or site-specific
network defaults into the upstream `UnitreeG1` robot.

### What should live under MoissanClub

Use the dedicated
[`MoissanClub/lerobot_teleoperator_g1_vr`](https://github.com/MoissanClub/lerobot_teleoperator_g1_vr)
repository for the reusable plugin. It was confirmed reachable on 2026-11-16
with default branch `main` at initial observed revision `a257fe5b7311e36c910e4e240e3ba9d3caff2707`. Keep
[`MoissanClub/unitree_g1_lerobot`](https://github.com/MoissanClub/unitree_g1_lerobot)
as the integration harness, installer/evidence runner and reference for the
known-working CloudXR path. The plugin should remain installable against an
unmodified supported LeRobot revision.

MoissanClub should initially own:

- `XRInputSource` and the normalized XR sample contract;
- `XRoboToolkitSource` and `CloudXRSource`, including optional SDK dependencies,
  lifecycle, source-specific timestamps and coordinate conversion;
- the shared clutch/rebase/freshness/fail-hold/re-clutch state machine;
- `G1VRTeleoperator`, which composes source, interaction controller and retargeter;
- VR retargeting policy: controller-to-end-effector scaling, workspace policy,
  reference-pose behavior, IK seeding and target-hold semantics;
- thin G1-29 and G1-23 retargeter adapters over upstream kinematics and embodiment
  metadata;
- source conformance fixtures, recorded XR traces, simulation acceptance tests,
  diagnostics and launch configurations;
- headset-facing status integration and the separate video-return tool or
  sidecar configuration;
- compatibility declarations identifying supported LeRobot, SDK and model-asset
  revisions.

If G1-23 IK does not yet exist upstream, it may be implemented in the Moissan
repository to unblock simulation research, but it must use an explicit G1-23
model/profile and remain clearly marked as an extension candidate. Avoid copying
the same solver into both repositories. Once the solver is independently tested
and no longer depends on XR semantics, propose it upstream and reduce the
Moissan retargeter to a thin adapter.

An illustrative Moissan package layout is:

```text
src/lerobot_teleoperator_g1_vr/
  config.py
  teleoperator.py
  xr/
    base.py
    sample.py
    xrobotoolkit.py
    cloudxr.py
  interaction/
    clutch.py
    health.py
  retargeting/
    base.py
    g1_29.py
    g1_23.py
  diagnostics.py
tests/
  fixtures/xr_traces/
  test_source_contract.py
  test_clutch_and_stale_input.py
  test_g1_29_retargeting.py
  test_g1_23_retargeting.py
  test_lerobot_plugin.py
```

The video sender can remain in the same repository during incubation, but as a
separate process and dependency group. It must not be imported by the command
loop or be required for headless simulation tests.

### Promotion rule

Move a component from MoissanClub to LeRobot only when all of the following are
true:

1. it is useful beyond one headset SDK or one Moissan experiment;
2. its API has survived both XRoboToolkit and CloudXR integration, or another
   comparably independent caller;
3. it has deterministic unit tests plus simulation evidence;
4. optional proprietary/vendor dependencies can remain outside LeRobot core;
5. upstream maintainers agree with the public interface and maintenance burden;
6. moving it eliminates duplication rather than creating a second implementation.

Likely promotion candidates are native G1-23 model selection, embodiment metadata
and source-independent G1 kinematics. The XR SDK adapters, clutch UX and video
return are likely to remain Moissan extensions. A generic XR schema or health
interface should not be proposed upstream until two independent sources expose a
stable common contract.

### Dependency direction

Dependencies must point in one direction:

```text
Moissan VR plugin -> public LeRobot interfaces -> G1 robot/model implementation
```

LeRobot must never import the Moissan plugin, XRoboToolkit, CloudXR or the video
sender. The Moissan plugin may use only public LeRobot behavior or narrowly scoped
upstream additions; it should not monkey-patch private classes or carry a forked
copy of `lerobot-teleoperate`.

## Phased plan

### Phase 0 — Pin current interfaces and prove the baseline

1. Record the exact LeRobot revision and inspect the current `UnitreeG1`,
   `UnitreeG1Config`, teleoperator plugin discovery and G1 IK interfaces.
2. Run a bounded upstream G1-29 MuJoCo baseline without a headset or external VR
   source; preserve command, model and shutdown evidence.
3. Inventory the existing CloudXR G1-29 operator and the successful XRoboToolkit
   Quest/dual-UR5e path as behavior references, not as architecture to copy.
4. Decide the external plugin repository/package location and dependency boundary.
5. Produce an upstream-versus-Moissan ownership manifest for every proposed
   module and identify any missing public LeRobot interface before implementation.

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

Target code location: the tracked external `MoissanClub/lerobot_teleoperator_g1_vr`
repository; do not leave the reusable adapter only in the existing
integration harness or an untracked experiment directory. Likely dependencies include current LeRobot,
XRoboToolkit SDK, the existing G1 kinematics stack and the CloudXR input client.
Keep transport SDKs optional so installing one source does not require the other.
The integration consumer remains `MoissanClub/unitree_g1_lerobot`; reusable
adapter and retargeter code belongs in the dedicated plugin repository from the
first implementation commit.

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
to the existing XRoboToolkit/CloudXR reference implementations. Follow the
linked commit plan and stop at Live Gate A for evidence review before adding
combined headset video.
