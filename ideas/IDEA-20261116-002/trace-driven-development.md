# Trace-driven VR teleoperation development

Date: 2026-11-16. Status: proposed. Scope: simulation development and physical
headset input capture only; no physical robot motion.

## Decision

Split VR teleoperation development at the normalized XR input boundary:

```text
Part A — brief headset capture

Quest + controllers
        |
XRoboToolkitSource
        +----> raw source trace
        |
normalization
        +----> normalized XR trace

Part B — repeatable headset-free development

normalized XR trace
        |
TraceReplaySource
        |
freshness + clutch + rebase
        |
G1-29 retargeter / IK
        |
LeRobot G1-29 MuJoCo
```

`TraceReplaySource` implements the same `XRInputSource` contract as
`XRoboToolkitSource` and `CloudXRSource`. The simulation, safety state machine and
retargeter therefore do not know whether samples are live or recorded.

This should be the primary development path. Live headset sessions become short
capture and final-integration gates rather than a requirement for every IK,
clutch, simulator or regression change.

## Record two layers, not one

Preserve both layers from each capture:

1. **Raw source trace:** the closest practical representation of XRoboToolkit SDK
   values and status before coordinate normalization. This permits later fixes to
   handedness, axes, quaternion ordering, timestamp interpretation or validity
   logic without repeating the headset session.
2. **Normalized XR trace:** the versioned, source-independent samples consumed by
   the shared interaction layer. This is the main replay and regression fixture.

Do not treat G1 joint commands as the input trace. Commanded and observed joints
are downstream evidence and should be recorded separately during simulation.
Keeping controller intent separate from robot output allows the same trace to be
replayed against later IK versions and eventually a G1-23 retargeter.

## Trace contents

Each normalized sample should contain:

- sequence number;
- elapsed trace time in nanoseconds from the first sample;
- host capture monotonic timestamp as capture provenance, not as the portable
  replay clock;
- source timestamp and whether it advanced;
- source connection/freshness state;
- optional head tracking validity, position and quaternion;
- left and right controller tracking validity, position and quaternion;
- left and right grip/squeeze, trigger and any buttons needed by the interaction
  contract;
- explicit status events rather than inferred gaps where possible.

Conventions must be in the manifest and schema: metres; quaternion order
`[x, y, z, w]`; normalized coordinate-frame definition; button ranges; missing
and invalid-value behavior. Head pose should be retained even though the first
G1-29 arm controller does not consume it, because it is useful for video/headset
diagnostics and later control designs.

Recommended capture directory:

```text
trace-<UTC timestamp>-<short label>/
  manifest.json
  raw.jsonl
  normalized.jsonl
  events.jsonl
  checksums.sha256
  notes.md                 # optional operator observation
```

Use a small, readable, versioned JSONL schema initially. Short curated fixtures
can be committed to the plugin repository. Full-rate or long captures should be
stored as external evidence with hashes; compression or a columnar format can be
added later without changing the in-memory contract. Never commit network
credentials or unrelated room/user data.

The manifest should identify:

- trace schema version;
- XR source type and adapter revision;
- XRoboToolkit SDK, PC Service and Quest app versions;
- headset/controller model;
- coordinate conventions and normalization revision;
- capture sample count, duration and observed rate;
- whether head/controllers/buttons were enabled;
- known drops, reconnects or operator deviations;
- raw and normalized file hashes.

## Replay clocks

Wall-clock time must not be hard-coded into the control logic. Inject a clock so
freshness, clutch and reconnection tests are deterministic.

Provide three replay modes:

1. **Deterministic trace-time:** advance the test clock to each recorded sample
   timestamp and step the simulator a configured number of steps. No sleeping.
   This is the primary CI and debugging mode.
2. **Real-time:** map trace elapsed time onto the current host monotonic clock and
   preserve recorded pacing. This checks process scheduling and operator-like
   timing without a headset.
3. **Rate-converted diagnostic:** optionally resample positions and orientations
   to a target control rate. Use linear position interpolation, quaternion SLERP
   and zero-order hold for buttons. Label this as transformed data; it must not
   replace exact-sample replay.

Deterministic replay should reproduce source status and timestamp progression,
including gaps. It must not accidentally mark every old recorded absolute
timestamp stale merely because replay occurs on a later day.

## Fault injection from valid traces

Generate most failure cases offline rather than spending headset time reproducing
them:

- freeze one source timestamp while getters continue returning cached poses;
- drop samples or one controller;
- invalidate a quaternion or position;
- force disconnect/reconnect events;
- restart source sequence/timestamp values;
- reconnect at a large absolute controller offset while grip remains held;
- delay simulator feedback or duplicate a sample;
- release only one grip during bimanual motion.

Derived traces must record their parent trace hash and transformation. They are
test fixtures, not claims that the headset produced the injected fault.

## Minimal headset capture suite

Capture small, comfortable controller motions with no simulator or robot command
path active:

| Trace | Content | Suggested duration |
| --- | --- | --- |
| `idle-released` | Head/controllers tracked, grips released | 5–10 s |
| `right-clutch` | Right grip edge, small translations on three axes, small rotations, release | 15–25 s |
| `left-clutch` | Left equivalent | 15–25 s |
| `bimanual` | Both grips, small independent motions, release one side then the other | 20–30 s |
| `rebase` | Move while released, press grip at a new absolute pose, make a small relative motion | 10–20 s |
| `buttons-head` | Trigger/button changes and modest head motion while controllers remain visible | 10–20 s |
| `reconnect` | One intentional app/PC Service reconnect with grips released | As required |

One good capture set should support many days of headset-free development. Avoid
aggressive or workspace-edge movements during capture; solver boundary cases are
better generated synthetically.

## Development sequence

### Stage 1 — No headset: schema and synthetic fixtures

1. Define the normalized XR schema, raw-envelope convention and trace manifest.
2. Implement `TraceRecorder`, `TraceReader`, injected clock and
   `TraceReplaySource`.
3. Prove record/read round trips, schema-version rejection, checksums and exact
   deterministic timing with synthetic samples.
4. Add synthetic clutch/release/reconnect traces before either vendor SDK is
   needed.

### Stage 2 — No headset: source and retargeter development

1. Put the existing CloudXR reader behind `XRInputSource` and record fake-source
   traces in tests.
2. Implement G1-29 retargeting against synthetic normalized traces.
3. Run deterministic trace replay through IK and G1-29 MuJoCo, recording
   commanded/observed joints and diagnostics.
4. Establish regression metrics: finite actions, joint limits, same-side motion,
   released-side hold, no reconnect jump, IK status and deterministic output
   tolerance.

### Stage 3 — Brief headset use: capture only

1. Implement and fake-test `XRoboToolkitSource` and a capture-only CLI.
2. Start the PC Service and Quest app, but do not start MuJoCo or a robot backend.
3. Capture the minimal suite above, validate it immediately, hash it and stop the
   headset session.
4. Preserve raw and normalized traces plus source/app versions.

This gate answers only whether controller/head/button data were captured with the
expected shape, timestamps and transitions. It does not test G1 control.

### Stage 4 — No headset: replay real traces through G1-29

1. Replay each captured normalized trace through the health/clutch controller and
   `G129Retargeter` without MuJoCo; inspect action and diagnostic summaries.
2. Replay accepted traces through G1-29 MuJoCo deterministically and in real time.
3. Add selected short, privacy-reviewed normalized segments as committed
   regression fixtures; retain full traces as hashed evidence.
4. Compare new commits against a golden summary rather than requiring bitwise IK
   output where solver/library versions legitimately differ.
5. Run derived fault traces and require fail-hold/re-clutch behavior.

### Stage 5 — Brief headset use: live integration

Only after trace replay passes, connect the live XRoboToolkit source to the same
pipeline. Run small right, left and bimanual stages, then one reconnect test.
Compare live diagnostics and joint response with the corresponding trace replay.
Add independent video return only after input-only live control passes.

## Evidence and comparison outputs

For every simulation replay preserve or summarize:

- input trace hash and schema version;
- plugin, LeRobot, model/asset and solver revisions;
- replay mode and clock parameters;
- source/interaction status transitions;
- IK convergence/error/saturation diagnostics;
- named commanded and observed G1 joints;
- maximum motion per arm while engaged;
- maximum drift per arm while released/stale;
- any dropped, duplicated or transformed samples;
- process exit and shutdown status.

Use tolerance-based summaries for regression review. A visual MuJoCo recording is
useful supporting evidence but does not replace numeric input/action/state traces.

## Limits

Trace replay substantially reduces headset time, but it cannot validate live
transport latency/jitter, network discovery, current device coordinate behavior,
SDK lifecycle, headset UI/status, video decoding or operator comfort. Retain one
short capture gate and one short final live-integration gate for each supported
source/app release.

Recorded controller traces are development inputs, not authorization to command a
physical robot. Replay tools must default to simulation and require a separately
reviewed physical plan before any hardware backend can consume a trace.
