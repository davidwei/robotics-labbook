# Robotics Lab Book Skill

## Mission

Use the lab book as the durable research index and knowledge layer for robotics work. Optimize for learning per unit of scarce physical-robot time while preserving enough provenance to reconstruct and critically analyze results later.

## Determine the mode first

Classify current work as one or more of:
- **development** — ideation, implementation, simulation, debugging away from physical hardware;
- **pre-lab** — preparing a physical test session;
- **in-lab** — actively using physical robot hardware;
- **post-lab** — reviewing a completed physical session;
- **share/publish** — producing downstream communication or reusable engineering output.

Read the corresponding file in `workflows/`.

## Fundamental rules

### 1. Reference sources of truth; do not duplicate them
Code history belongs in the code repository. Record repository + exact revision/PR, not copied diffs. Large artifacts belong in artifact storage. Agent transcripts belong in their native/archive location.

### 2. Physical runs require provenance
For every meaningful physical run, preserve the exact code/configuration state that actually executed, the run boundary/time, relevant evidence references, and short operator observations. If the working tree was dirty, preserve a checkpoint or complete patch/snapshot.

### 3. Capture now; understand later
During physical lab work, minimize human interruption. Prefer automatic capture and short timestamped observations. Deep explanation belongs in post-lab review.

### 4. Separate evidence from interpretation
Maintain these distinctions:
- **raw evidence** — logs, video, telemetry, code/config state;
- **observation** — what was directly observed/measured;
- **hypothesis** — a proposed explanation/prediction;
- **proposed finding** — an interpretation the evidence appears to support;
- **reviewed/validated finding** — a conclusion that passed appropriate evidence and human review;
- **decision** — an action/choice based on findings and constraints.

Never silently upgrade an agent hypothesis into a validated finding.

### 5. Preserve uncertainty and contradictions
Record competing explanations, unexplained behavior, negative results, and conflicting evidence. Do not optimize the notebook for a clean success narrative.

### 6. Treat demos appropriately
A successful run demonstrates that behavior occurred under that run's conditions. Do not generalize reliability without supporting repeated/controlled evidence.

### 7. Lab-book automation does not authorize robot motion
Never infer permission to actuate a physical robot from permission to update the notebook. Respect independent safety and execution controls.

## Core relationships

    Project -> Experiment -> Session -> Run -> Evidence
                                          |
                                          v
                             Analysis -> Finding/Decision
                                          |
                                          v
                                Share / Publish

An experiment may span multiple sessions. A session may contribute to multiple experiments.

## Agent responsibilities by mode

### Development
Retrieve relevant prior findings/decisions; associate substantial work with a project/experiment; simulate what can be learned without robot time; preserve assumptions requiring physical validation.

### Pre-lab
State what each physical test is intended to learn; prioritize by information value and physical necessity; define success/failure criteria; ensure evidence capture is ready; prepare fallback/isolation tests and a minimum useful experiment; flag unreviewed/high-risk control changes.

### In-lab
Reduce documentation burden; preserve run boundaries, code/config state, evidence, brief observations, and material agent changes; troubleshoot rapidly without presenting guesses as facts; preserve unresolved questions.

### Post-lab
Reconstruct chronology; audit material changes; distinguish tested from untested; compare runs/evidence; separate observations from explanations; identify contradictions/missing evidence; propose high-information next tests; seek human review before promoting consequential conclusions.

### Share / Publish
Trace claims to reviewed evidence. Lightweight sharing should not overstate generality. Rigorous publication should clean experimental code, add tests/docs, and preserve reproducibility/provenance.

## Writing style

Lab records should be concise, factual, and useful months later. Prefer explicit uncertainty over persuasive prose.

## Multi-agent behavior

Codex, Claude, and future agents use this same protocol. Do not create agent-specific versions of scientific conclusions. Record agent/session provenance where useful, but organize knowledge around projects/experiments/runs rather than conversations.

## Human authority

Agents may draft observations, hypotheses, analyses, and proposed findings. Consequential or reusable findings retain review status until explicitly reviewed/accepted by the researcher.
