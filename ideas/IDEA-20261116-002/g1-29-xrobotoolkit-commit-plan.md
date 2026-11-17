# G1-29 + XRoboToolkit implementation — commit-by-commit plan

Date: 2026-11-16. Status: proposed; no implementation commits made by this
plan. Scope: simulation only. Primary target: a new MoissanClub third-party
LeRobot plugin repository, proposed as `MoissanClub/lerobot_teleoperator_g1_vr`.
`MoissanClub/unitree_g1_lerobot` remains the integration harness and evidence
runner. Target result: the released XRoboToolkit Quest app controls both G1-29
arms in MuJoCo while preserving a source-independent path for later CloudXR and
G1-23 work.

## Repository and branching strategy

Create the plugin now. Do not build a large mixed project branch and attempt to
extract upstream LeRobot commits afterward.

Use three repositories with one-way responsibilities:

| Repository | Role | Branch policy |
| --- | --- | --- |
| `MoissanClub/lerobot_teleoperator_g1_vr` (new) | Reusable XR source contract, source adapters, interaction state machine, G1 retargeter adapters and LeRobot teleoperator plugin | `main` stays releasable; develop through small sequential feature branches/PRs |
| `MoissanClub/unitree_g1_lerobot` (existing) | Known-working reference operator, installers, simulation orchestration, video sidecar, experiment launchers and evidence capture | One short-lived integration branch for the G1-29 experiment; do not move reusable plugin code here |
| `MoissanClub/lerobot` fork of Hugging Face LeRobot | Minimal robot-generic changes proposed upstream: embodiment metadata/model selection, reusable kinematics or a genuinely missing public hook | A separate branch per upstream contribution, always based on current Hugging Face `main`; never branch it from plugin or experiment history |

Recommended branches:

```text
MoissanClub/lerobot_teleoperator_g1_vr
  main
  feat/xr-input-contract
  feat/cloudxr-source
  feat/g1-29-retargeter
  feat/xrobotoolkit-source
  feat/g1-29-lerobot-integration

MoissanClub/unitree_g1_lerobot
  main
  integration/g1-29-xrobotoolkit

MoissanClub/lerobot
  current upstream-tracking main
  upstream/g1-<one-minimal-capability>   # create only when a proven gap exists
```

Feature branches in the plugin should normally be sequential: merge the contract
before branching the source adapters, then merge the retargeter, and so on. If a
demo temporarily needs several unmerged plugin PRs, use a disposable
`integration/g1-29-xrobotoolkit` branch in the plugin repository as a merge
preview. Do not release from it, and do not use it as the source of an upstream
LeRobot PR.

When a LeRobot gap is found, first write a failing plugin/integration test that
demonstrates it. Then author the smallest source-independent fix directly on a
fresh `MoissanClub/lerobot` branch based on Hugging Face `main`. The upstream
branch must contain no XRoboToolkit, CloudXR, Quest, video or Moissan experiment
imports. Until it merges upstream, the plugin compatibility manifest may pin the
tested fork commit explicitly; replace the pin with an upstream revision in a
separate dependency-update commit.

## Starting point and branch policy

- Start the integration harness from reviewed repository revision
  `e9891610f0779b7567e2e2637d53c8fb3a0f4d25` on a new branch such as
  `integration/g1-29-xrobotoolkit`.
- Preserve the existing untracked `tests/test_dev_workspace.py` and
  `tools/dev_workspace/`; they are not part of this series unless separately
  reviewed and intentionally added.
- Preserve the pinned known-working G1 VR dependency release at LeRobot commit
  `d5e400bcefeccc93ba956ce876530e5283512df1` until the baseline and interface
  contract are recorded. Do not combine a dependency-pin migration with the new
  input source.
- Keep existing CloudXR behavior passing throughout. XRoboToolkit is a second
  `XRInputSource`, not a replacement or a conditional branch scattered through
  G1 IK.
- Each commit includes its focused tests and must be revertible without requiring
  a later commit. Formatting-only or broad unrelated cleanup is excluded.

## Commit 1 — Record pins and lock the G1-29 baseline

Suggested subject:

```text
test(vr): lock the G1-29 operator baseline and dependency pins
```

Changes:

- Add a machine-readable compatibility manifest recording the operator revision,
  pinned LeRobot revision, G1-29 URDF/assets identity, Python version and existing
  CloudXR dependency.
- Add or tighten a G1-29-only baseline test around the existing synthetic replay:
  simulator readiness, 14 arm coordinates, changing nonblank camera frames,
  bounded motion, and clean ordered shutdown.
- Record the exact baseline command and output/evidence location. Do not change
  runtime behavior.

Gate:

```bash
G1_VR_OPERATOR_TESTS=1 .vr-sim/env/bin/python -m pytest -q \
  tests/diagnostics/test_vr_operator.py \
  tests/simulation/test_vr_operator_processes.py -k 'g1_29 or not replay_processes'
./run_g1_vr_sim.sh --embodiment g1_29 --headless
```

Expected: the pre-change G1-29 replay passes. If it does not, stop and diagnose
the baseline; do not attribute the failure to XRoboToolkit work.

## Commit 2 — Define the source-neutral XR contract

Suggested subject:

```text
refactor(vr): define a normalized XR input contract
```

Changes:

- Bootstrap the installable `lerobot_teleoperator_g1_vr` distribution in the new
  plugin repository, including license, minimal packaging, supported Python/
  LeRobot compatibility metadata and a base test environment with no vendor XR
  SDK installed.
- Add an `XRInputSource` protocol with `connect()`, `get_action()` or `sample()`,
  `status`, and `disconnect()` lifecycle.
- Define the normalized bimanual sample used by the current G1 controller:
  `captured_at`, optional source timestamp, per-hand `tracked`, `grip_pos`,
  `grip_quat`, `squeeze`, and `trigger`.
- Specify metres, quaternion order `[x, y, z, w]`, normalized input frame,
  monotonic host time and validity rules.
- Add pure validation tests for shapes, finite values, quaternion norm, missing
  hands, timestamp monotonicity and an immutable/copy boundary.
- Add a small source-status model with at least `disconnected`, `stale`, `ready`
  and a human-readable recovery hint.

Gate: unit tests only; no SDK, GPU, simulator or headset. Existing runtime remains
unchanged.

Architecture value: every later source must satisfy one contract, and the G1
retargeter never imports XRoboToolkit or CloudXR.

## Commit 3 — Put existing CloudXR behind the contract

Suggested subject:

```text
refactor(vr): adapt CloudXR controllers to XRInputSource
```

Changes:

- Wrap the existing `XRControllers`/`VideoControllerSession` construction in a
  `CloudXRSource` implementation.
- Make the bridge consume only `XRInputSource`; remove direct CloudXR reads from
  the control loop.
- Keep CloudXR process startup, video session and shutdown behavior unchanged.
- Add a fake CloudXR reader test proving field mapping, one read per loop,
  bimanual independence and cleanup.
- Add a golden comparison showing the refactored source produces the same sample
  and G1 action as the pre-refactor path for representative frames.

Gate: Commit 1 tests plus existing live-shutdown tests when a CloudXR runtime is
available. No live headset is required. A behavior change belongs in a later
commit, not this refactor.

## Commit 4 — Isolate the G1-29 retargeter

Suggested subject:

```text
refactor(vr): expose G1-29 XR retargeting behind a stable interface
```

Changes:

- Add a `G1Retargeter` protocol consuming normalized XR samples plus measured arm
  state and producing named LeRobot actions plus diagnostics.
- Implement `G129Retargeter` as a thin adapter over the established
  `G1ArmKinematics` and `G1XRControl`; do not copy the solver.
- Require the G1-29 profile, 14 arm joints and matching model identity at startup.
  Reject G1-23 for now with a clear unsupported-configuration error rather than
  silently using G1-29.
- Test neutral hold, right-only, left-only, bimanual motion, grip release,
  nonfinite inputs, joint limits and deterministic re-clutch behavior.
- Compare named action keys against the robot's advertised arm features.

Gate: deterministic IK tests plus G1-29 headless replay. CloudXR source code must
not be imported by retargeter tests.

Architecture value: G1-23 later implements the same contract without modifying
either XR source.

## Commit 5 — Add shared freshness and reconnect behavior

Suggested subject:

```text
feat(vr): hold and re-clutch on stale or reconnected XR input
```

Changes:

- Put stale detection and source-health transitions between the source and
  retargeter, reusing rather than duplicating `G1XRControl` freshness behavior.
- On stale, invalid or disconnected input: clear both clutch origins and return
  the measured/last safe arm targets.
- Require a fresh sample followed by a new grip edge before motion resumes.
- Rate-limit diagnostics and expose a recovery hint such as “reconnect the
  headset app/PC Service, then release and press grip.”
- Add deterministic sequences for freeze, disconnect, timestamp restart,
  reconnect with a large absolute pose offset, and independent hand release.

Gate: all tests use fake clocks and recorded samples. Prove no target jump across
reconnect before connecting the live SDK.

## Commit 6 — Implement the XRoboToolkit source adapter

Suggested subject:

```text
feat(vr): add XRoboToolkit controller input source
```

Changes:

- Implement `XRoboToolkitSource` using `xrobotoolkit_sdk.init()`/`close()`, the
  left/right controller pose getters, grip/trigger getters and source timestamp.
- Convert SDK pose `[x, y, z, qx, qy, qz, qw]` into the normalized sample without
  applying G1-specific transformations.
- Append the configurable XRoboToolkit site-packages directory after the pinned
  environment paths; do not prepend it and accidentally replace Pinocchio,
  MuJoCo or other pinned dependencies.
- Keep the SDK optional and import it only when this source is selected. Provide
  an actionable dependency error otherwise.
- Detect unchanged source timestamps as stale even if the SDK getters continue
  returning cached values.
- Add a fake SDK for connect/disconnect, bimanual mapping, invalid quaternion,
  partial tracking, cached timestamp, exception cleanup and reconnect tests.

Gate: unit tests and import-coexistence probe in the pinned G1 environment. Do not
open a live SDK connection in automated tests because the PC Service path is
single-client sensitive.

## Commit 7 — Add explicit source selection to the bridge

Suggested subject:

```text
feat(vr): select replay, CloudXR, or XRoboToolkit input
```

Changes:

- Add plugin configuration such as `source.type={replay,cloudxr,xrobotoolkit}`;
  preserve current defaults for existing integration-harness commands.
- Add XRoboToolkit SDK-path and stale-timeout configuration without embedding a
  workstation-specific virtualenv in application code.
- Build the source through one factory; do not add source checks inside the
  bridge loop or retargeter.
- Emit structured startup/status lines identifying source, embodiment, tracking,
  clutch and stale/reconnect state.
- Add config registry, factory, invalid-combination and lifecycle tests.

Gate: replay and mocked-source bridge tests. The same `G129Retargeter` instance
must be used for CloudXR and XRoboToolkit samples.

## Commit 8 — Supervise XRoboToolkit without starting CloudXR

Suggested subject:

```text
feat(vr): supervise G1-29 XRoboToolkit simulation sessions
```

Changes:

- In `MoissanClub/unitree_g1_lerobot`, consume the plugin from its pinned local or
  Git revision rather than copying its source modules into the harness.
- Teach `g1_vr_operator.py` to construct a process graph from the selected source:
  `simulator + bridge` for XRoboToolkit and `simulator + cloudxr + bridge` for
  CloudXR.
- Preserve consumer-before-producer shutdown. For XRoboToolkit stop the bridge
  before the simulator; do not start, probe, accept an EULA for, or stop CloudXR.
- Add child-failure, readiness, interrupt and clean-shutdown tests for both process
  graphs.
- Add a dedicated wrapper command or documented invocation for
  G1-29/XRoboToolkit simulation.
- Keep the robot path private/local and simulation-only; assert this mode cannot
  select physical DDS.

Gate: complete headless replay plus mocked XRoboToolkit process tests. Existing
CloudXR replay and shutdown tests must remain green.

## Live Gate A — Input-only headset check, no video

This is an experimental run, not a code commit. It is the first point requiring
the Quest and PC Service:

1. Start the PC Service and released Quest app with controller sending enabled.
2. Start G1-29 MuJoCo with `--input-source xrobotoolkit`, video return disabled.
3. Verify advancing timestamps and both grips released before movement.
4. Test small right-only, release/hold, left-only, release/hold, then bimanual
   movements.
5. Force one app reconnect and verify hold plus explicit re-clutch without a jump.
6. Preserve normalized samples, source health, commanded/observed joints and logs.

Do not continue to video integration if stale/reconnect behavior fails.

## Commit 9 — Run the composition through standard LeRobot interfaces

Suggested subject:

```text
feat(vr): run G1VRTeleoperator through standard LeRobot control
```

Changes:

- Implement `G1VRTeleoperator` as composition of `XRInputSource`, shared health/
  clutch behavior and `G129Retargeter`.
- Return named arm `RobotAction` values and use feedback/current observations for
  measured-state seeding and safe hold.
- Keep transport SDKs in optional dependency groups, for example
  `xrobotoolkit` and `cloudxr`; base installation and replay tests require neither.
- Add factory-discovery, lifecycle, action-feature and observation-feedback tests
  against the pinned supported LeRobot revision.
- Keep the existing supervised launcher as a diagnostic/reference path until the
  standard LeRobot path passes equivalent simulation acceptance; do not delete it
  in this commit.

Gate: install the plugin into an isolated environment, verify standard LeRobot
discovery, run deterministic actions through a simulated G1-29 robot, and confirm
that LeRobot source contains no Moissan or XR SDK import.

Decision boundary: if a missing public LeRobot hook blocks this commit, first
preserve a failing integration test, then create a separate minimal branch from
current Hugging Face LeRobot `main`. Do not cherry-pick mixed plugin commits into
LeRobot, monkey-patch LeRobot or copy `lerobot-teleoperate` into the plugin.

## Commit 10 — Add independent video-return orchestration and evidence capture

Suggested subject:

```text
feat(vr): add optional Quest video return to G1-29 sessions
```

Changes:

- Integrate the proven XRoboToolkit desktop-video sender as an optional sidecar,
  preferably from a tracked package/script with its prior successful snapshot
  reconciled.
- Keep it outside the command loop and optional dependency path.
- Add readiness, log/evidence directory, independent failure reporting and
  shutdown ordering. A video failure must not prevent the arm loop from holding
  and stopping safely.
- Add mock protocol tests for OPEN_CAMERA and framed H.264 delivery; do not make a
  live Quest decoder a normal automated-test dependency.

Gate: headless command-loop tests with sender disabled, mock sender tests, and one
bounded desktop sender test. No physical robot.

## Live Gate B — Combined G1-29 experiment

After Commit 10:

1. Repeat Live Gate A briefly to confirm no regression.
2. Enable the video sidecar and confirm a recognizable, updating MuJoCo view.
3. Repeat right-only, left-only, bimanual and released-grip hold stages.
4. Disconnect/reconnect the Quest app once while video and tracking status are
   recorded; verify the reconnect prompt and re-clutch behavior.
5. Preserve exact code/dependency/model revisions, sender snapshot, normalized
   input, command/observation telemetry, process logs and operator observations.

Passing this gate supports only the bounded G1-29/XRoboToolkit simulation claim.
It does not validate CloudXR equivalence, G1-23, quantitative latency, reliability
or physical robot safety.

## Commit 11 — Document the reviewed candidate and retain extension seams

Suggested subject:

```text
docs(vr): publish the reviewed G1-29 XRoboToolkit simulation workflow
```

Changes:

- Document installation, optional dependencies, source selection, PC Service/app
  startup, recovery hints, video sidecar and evidence locations.
- Record exact accepted revisions and remaining limitations.
- Add a compatibility matrix that marks only tested combinations as tested.
- Document the unchanged seams for `CloudXRSource` and future `G123Retargeter`.
- Update the release/pin only in a separate, reviewable decision after all gates
  pass; do not silently move the existing pinned release.

Gate: commands in the documentation are exercised from a clean isolated
environment or explicitly labeled unverified. Repository tests and `git diff
--check` pass.

## Review and merge strategy

Recommended review groups, while keeping individual commits intact:

1. Commit 1 in the integration harness, then Commits 2–4 as sequential plugin
   PRs: baseline, plugin contract and architecture-preserving refactor.
2. Commits 5–8: freshness behavior and XRoboToolkit source integration.
3. Live Gate A evidence review.
4. Commit 9: standard LeRobot runtime boundary, with any necessary upstream fix
   reviewed in its own repository and PR.
5. Commit 10 and Live Gate B: optional video and combined experiment.
6. Commit 11: reproducible handoff.

Do not squash the source-neutral refactors together with the SDK implementation;
their separate history makes CloudXR regressions and future G1-23 work easier to
review or revert. No commit in this series authorizes physical G1 connection or
motion.
