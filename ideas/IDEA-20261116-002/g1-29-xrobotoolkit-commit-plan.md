# G1-29 + XRoboToolkit implementation — commit-by-commit plan

Date: 2026-11-16. Status: software implementation complete through Commit 12;
simulation-lab headset validation pending. All implementation branches were
pushed. Manual gates were assumed only to permit development sequencing and are
not recorded as observed results.
Scope: simulation only. Primary target: the MoissanClub third-party
LeRobot plugin repository `MoissanClub/lerobot_teleoperator_g1_vr`, confirmed on
2026-11-16 with default branch `main` at initial observed revision
`a257fe5b7311e36c910e4e240e3ba9d3caff2707`.
`MoissanClub/unitree_g1_lerobot` remains the integration harness and evidence
runner. Target result: the released XRoboToolkit Quest app controls both G1-29
arms in MuJoCo while preserving a source-independent path for later CloudXR and
G1-23 work.

## Implementation progress

Commit 1 completed on 2026-11-16:

- Repository: `MoissanClub/unitree_g1_lerobot`
- Branch: `integration/g1-29-xrobotoolkit`
- Commit: `02d79efe293e33ecb84f4fc3b4a10bf207300987`
- Baseline: 100 synthetic frames, `0.2631 rad` maximum motion and 54 distinct
  camera frames; clean launcher completion
- Contract: pinned LeRobot revision, Python/key dependency versions, G1-29 URDF
  SHA-256 and 14-arm-DoF expectation recorded in
  `configs/g1_29_vr_compatibility.json`
- Verification: 20 diagnostic unit tests passed; the focused installed-contract
  and G1-29 replay tests passed; the broader gate passed 29 tests with the
  intentionally excluded G1-23 replay case deselected
- Physical scope: no headset, live CloudXR, XRoboToolkit, DDS or physical robot
  used

Commit 2 completed on 2026-11-16:

- Repository: `MoissanClub/lerobot_teleoperator_g1_vr`
- Branch: `feat/xr-input-contract`
- Commit: `c7ad3da92b6caebd0bff54fc68177f43a3845456`
- Package: installable typed `lerobot_teleoperator_g1_vr` distribution with the
  exact prefix used by LeRobot third-party teleoperator discovery
- Contract: immutable normalized poses/controllers/samples, explicit metres and
  `[x, y, z, w]` quaternions, host/source timestamps, source status and structural
  `XRInputSource` lifecycle
- Dependency boundary: base installation has no LeRobot, XRoboToolkit, CloudXR,
  GPU, MuJoCo or device runtime dependency
- Verification: 22 tests passed under Python 3.12; Ruff lint/format checks passed;
  source distribution and wheel builds passed; metadata/discovery name verified
- Physical scope: no headset, vendor SDK, simulator, DDS or physical robot used

The existing untracked `tests/test_dev_workspace.py` and `tools/dev_workspace/`
in the integration harness were preserved and not included in Commit 1.

Commit 3 completed on 2026-11-16:

- Repository: `MoissanClub/lerobot_teleoperator_g1_vr`
- Branch: `feat/xr-trace-replay`, stacked on Commit 2
- Commit: `2c8e7fbba5a800bcde16cc033de02abeb8bdccf6`
- Format: versioned manifest plus raw, normalized and source-event JSONL streams;
  per-file SHA-256 values and an independent checksum file
- Replay: `TraceReplaySource` uses the same `XRInputSource` contract with
  deterministic trace-time or real-time pacing; old host timestamps are replaced
  by the injected replay clock while source timestamps/status are preserved
- Development safety: replay currently rejects non-simulation targets; rate
  conversion is explicitly not implemented and exact captures are marked
  untransformed
- Fixtures: synthetic idle, right, left, bimanual, release, stale and reconnect
  sequences cover round trips, status transitions and lifecycle behavior
- Verification: 41 tests passed under Python 3.12; Ruff lint/format checks passed;
  source distribution, wheel build and isolated base-wheel import passed
- Physical scope: no headset, vendor SDK, LeRobot runtime, GPU, simulator, DDS or
  physical robot used

Commit 4 completed on 2026-11-16:

- Repository: `MoissanClub/lerobot_teleoperator_g1_vr`
- Branch: `feat/cloudxr-source`, stacked on Commit 3
- Commit: `de5ad6c17ec82c0a2d04a59c37785649e4874d78`
- Adapter: `CloudXRSource` wraps the established LeRobot `XRControllers` lifecycle
  and optional `VideoControllerSession` construction behind `XRInputSource`
- Dependency boundary: LeRobot, Isaac Teleop, OpenXR, CUDA and video imports are
  delayed until the default reader factory is used during `connect()`; injected
  readers keep unit tests vendor-free
- Behavior: one backend read per sample; acquisition timestamp preserved for
  freshness; cached/future/missing frames become stale; invalid controller data
  is isolated to the affected side; raw actions are copied into JSON-compatible
  trace input
- Verification: 58 plugin tests passed under Python 3.12; 17 focused adapter
  tests also passed in the pinned G1/CloudXR environment; Ruff lint/format,
  source/wheel builds and isolated base-wheel import passed; actual pinned
  input-only and video-backed `XRControllers` objects constructed without opening
  OpenXR
- Physical scope: no headset, live CloudXR session, GPU rendering, simulator,
  DDS or physical robot used

Commit 5 completed on 2026-11-16:

- Repository/branch: `MoissanClub/lerobot_teleoperator_g1_vr`,
  `feat/g1-29-retargeter`
- Commit: `a1d18e6c79b4658e4b7dc18b1c0ab193f8325dc7`
- Added the source-independent `G129Retargeter` over pinned LeRobot
  `G1ArmKinematics`/`G1XRControl`, with measured-state seeding, named 14-joint
  actions and IK/clutch diagnostics
- Verification: 67 vendor-free tests passed with one expected skip; two actual
  pinned G1-29 IK integration tests passed

Commit 6 completed on 2026-11-16:

- Repository/branch: plugin, `feat/xr-freshness-reclutch`
- Commit: `1d490996c3b261e667f2fafa918e51712a6d87df`
- Added shared fail-hold behavior for stale/disconnected/frozen/backward source
  timestamps and independent release/new-grip recovery latches
- Verification: 80 tests passed with one expected pinned-environment skip

Commit 7 completed on 2026-11-16:

- Repository/branch: plugin, `feat/xrobotoolkit-source`
- Commit: `b73c8a948be7ee1f0c6b957c76d6ec2c2fee95e3`
- Added the lazy XRoboToolkit SDK 1.1.0 adapter and capture-only trace CLI;
  malformed hand data is isolated and stale/restarted SDK timestamps fail closed
- Verification: 93 vendor-free tests passed with one expected skip; two pinned
  G1 IK tests passed; actual SDK initialize/close succeeded beside Pinocchio
  3.9.0, MuJoCo 3.12.0 and NumPy 2.2.6 without dependency shadowing
- Headset trace capture remains pending

Commit 8 completed on 2026-11-16:

- Repository/branch: plugin, `feat/xr-source-selection`
- Commit: `bf73e60e332b818f3db5d2e94d4c086fa964f807`
- Added explicit mutually exclusive `trace`, `cloudxr` and `xrobotoolkit` source
  selection; construction is lazy and does not probe unselected vendors
- Verification: 103 tests passed with one expected pinned-environment skip

Commit 9 completed on 2026-11-16:

- Repository/branch: `MoissanClub/unitree_g1_lerobot`,
  `feat/g1-29-vr-supervisor`
- Commit: `2bdabacbb78b27eca7773b2c2c7c08a5787451b7`
- Added the simulation-only supervised source → guard → retargeter → robot loop,
  stable telemetry and a trace-driven native LeRobot G1-29 MuJoCo gate
- Verification: five lifecycle/fail-hold supervisor tests and one real recorded
  trace → pinned G1 IK → native MuJoCo test passed; no DDS/headset was used
- Existing user-owned untracked development-workspace files were preserved

Commit 10 completed on 2026-11-16:

- Repository/branch: plugin, `feat/lerobot-g1-vr-teleoperator`
- Commit: `b0928d0ddbccb7a4e9caf6e322c37267b8395453`
- Added registered `g1_vr` standard LeRobot `Teleoperator` composition with
  measured robot feedback and an enforced simulation-only configuration
- Verification: three pinned framework/plugin tests and two real G1 IK tests
  passed; built wheel installation and LeRobot third-party auto-discovery
  registered `g1_vr`

Commit 11 completed on 2026-11-16:

- Repository/branch: integration harness, `feat/g1-29-quest-video`
- Commit: `13a272a0711e39d9e736bef0577b43f500b3e137`
- Reconciled the XRoboToolkit Quest `OPEN_CAMERA`/length-framed H.264 sender as an
  optional sidecar with readiness, independent failure status, ordered shutdown,
  `sender.log` and `metadata.json`
- Verification: Quest protocol/mock sidecar tests, supervisor regressions and a
  real bounded sender-process ready/stop lifecycle passed (`10 passed` total)
- No Quest decoder or visible-video observation was performed

Commit 12 completed on 2026-11-16:

- Repository/branch: plugin, `docs/g1-29-xr-simulation-workflow`
- Commit: `0d68a65848011550393ef136b2dfe187c2ec37a6`
- Published exact candidate revisions, install/capture/replay/standard LeRobot
  commands, recovery behavior, compatibility limits and an efficient manual
  acceptance plan covering both sources in two headset sessions plus replay
- Verification: Ruff passed; 103 vendor-free tests passed with two expected
  optional skips; five pinned LeRobot/G1 tests passed; source and wheel builds
  passed

Software evidence supports the trace-driven G1-29 simulation architecture and
its failure-state contracts. It does not yet support claims of live G1-29 motion
from either headset source, visible video in the headset, source equivalence,
G1-23 support, latency/reliability, or physical-robot safety.

Next action: execute the simulation-lab plan in
`docs/simulation-lab-acceptance.md` at plugin Commit 12 and integration-harness
Commit 11, preserving source traces, telemetry, status transitions, video logs
and operator observations. Physical validation status remains not authorized.

## Repository and branching strategy

Develop in the dedicated plugin repository from the start. Do not build a large
mixed project branch and attempt to extract upstream LeRobot commits afterward.

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

## Commit 3 — Add trace recording, replay and deterministic clocks

Suggested subject:

```text
feat(vr): record and replay normalized XR traces
```

Changes:

- Implement the versioned manifest, raw envelope and normalized JSONL trace
  format described in the
  [trace-driven development plan](trace-driven-development.md).
- Add `TraceRecorder`, `TraceReader`, an injected control clock and
  `TraceReplaySource` implementing `XRInputSource`.
- Provide exact deterministic trace-time and real-time replay; keep rate
  conversion explicitly optional and labeled as transformed data.
- Add synthetic idle, right, left, bimanual, release, stale and reconnect
  fixtures plus round-trip/schema/checksum/fake-clock tests.
- Make replay default to simulation-only and reject a physical backend without a
  separately reviewed override path.

Gate: unit tests only; no vendor SDK, GPU, simulator or headset. Identical trace
input and dependency revisions produce identical normalized samples and status
transitions.

## Commit 4 — Put existing CloudXR behind the contract

Suggested subject:

```text
refactor(vr): adapt CloudXR controllers to XRInputSource
```

Changes:

- Wrap the existing `XRControllers`/`VideoControllerSession` construction in a
  `CloudXRSource` implementation.
- Keep the adapter independent of the bridge; make the bridge consume only
  `XRInputSource` in the later source-selection/integration commit.
- Keep CloudXR process startup, video session and shutdown behavior unchanged.
- Add a fake CloudXR reader test proving field mapping, one read per loop,
  bimanual independence and cleanup.
- Add a golden comparison showing the refactored source produces the same sample
  and G1 action as the pre-refactor path for representative frames.

Gate: Commit 1 tests plus existing live-shutdown tests when a CloudXR runtime is
available. No live headset is required. A behavior change belongs in a later
commit, not this refactor.

## Commit 5 — Isolate the G1-29 retargeter

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

## Commit 6 — Add shared freshness and reconnect behavior

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

## Commit 7 — Implement the XRoboToolkit source adapter

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

## Headset Capture Gate — Record traces without MuJoCo

This is the first headset use. Run only the XRoboToolkit PC Service, Quest app and
capture-only CLI. Capture the `idle-released`, right, left, bimanual, rebase,
buttons/head and reconnect traces defined in the trace-driven plan. Validate and
hash raw and normalized data before ending the session. No simulator or robot
backend runs at this gate.

## Commit 8 — Add explicit source selection to the bridge

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

## Commit 9 — Replay and supervise XRoboToolkit G1-29 simulation

Suggested subject:

```text
feat(vr): supervise G1-29 XRoboToolkit simulation sessions
```

Changes:

- In `MoissanClub/unitree_g1_lerobot`, consume the plugin from its pinned local or
  Git revision rather than copying its source modules into the harness.
- Run the captured normalized traces through `G129Retargeter` and G1-29 MuJoCo in
  deterministic and real-time modes before enabling a live source.
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

This is an experimental run, not a code commit. It is the first point that uses
the Quest as a live G1 control source; the earlier capture gate used the headset
only to create reusable traces:

1. Start the PC Service and released Quest app with controller sending enabled.
2. Start G1-29 MuJoCo with `--input-source xrobotoolkit`, video return disabled.
3. Verify advancing timestamps and both grips released before movement.
4. Test small right-only, release/hold, left-only, release/hold, then bimanual
   movements.
5. Force one app reconnect and verify hold plus explicit re-clutch without a jump.
6. Preserve normalized samples, source health, commanded/observed joints and logs.

Do not continue to video integration if stale/reconnect behavior fails.

## Commit 10 — Run the composition through standard LeRobot interfaces

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

## Commit 11 — Add independent video-return orchestration and evidence capture

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

After Commit 11:

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

## Commit 12 — Document the reviewed candidate and retain extension seams

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

1. Commit 1 in the integration harness, then Commits 2–5 as sequential plugin
   PRs: baseline, plugin/trace contracts and architecture-preserving refactor.
2. Commits 6–7, then the capture-only headset gate: freshness behavior,
   XRoboToolkit source and reusable traces.
3. Commits 8–9 and Live Gate A: headset-free trace simulation before live input.
4. Commit 10: standard LeRobot runtime boundary, with any necessary upstream fix
   reviewed in its own repository and PR.
5. Commit 11 and Live Gate B: optional video and combined experiment.
6. Commit 12: reproducible handoff.

Do not squash the source-neutral refactors together with the SDK implementation;
their separate history makes CloudXR regressions and future G1-23 work easier to
review or revert. No commit in this series authorizes physical G1 connection or
motion.
