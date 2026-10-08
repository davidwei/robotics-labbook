# Robotics Lab Book Skill

## Mission

Use the lab book as the durable research index and knowledge layer for robotics work. Optimize for learning per unit of scarce physical-robot time while preserving enough provenance to reconstruct and critically analyze results later.

The default reading path must remain concise. Preserve forensic detail without forcing a researcher to read it during ordinary review.

## Determine the mode first

Classify current work as one or more of:
- **development** — ideation, implementation, simulation, debugging away from physical hardware;
- **pre-lab** — preparing a physical test session;
- **in-lab** — actively using physical robot hardware;
- **retrospective capture** — reconstructing a session that already happened from agent history, Git, files, artifacts, and operator recollection;
- **post-lab** — deeply reviewing a completed physical session;
- **share/publish** — producing downstream communication or reusable engineering output.

Read the corresponding file in `workflows/`. Retrospective capture follows `retrospective-capture.md` and is distinct from post-lab analysis.

## Fundamental rules

### 1. Reference sources of truth; do not duplicate them
Code history belongs in the code repository. Record repository + exact revision/PR, not copied diffs. Large artifacts belong in artifact storage. Agent transcripts belong in their native/archive location.

### 2. Physical experimental runs require provenance
For every meaningful physical experimental run, preserve the exact code/configuration state that actually executed, the run boundary/time, relevant evidence references, and short operator observations. If the working tree was dirty, preserve a checkpoint or complete patch/snapshot.

Do not inflate every lab activity into an experimental run. Classify activities when useful as:
- **preflight** — readiness, connectivity, read-only checks, instrumentation validation;
- **run** — execution intended to generate evidence about an experiment/question;
- **diagnostic** — targeted troubleshooting/measurement;
- **cleanup** — shutdown, restoration, artifact preservation.

Only `run` activities normally need full run records. Promote a preflight/diagnostic to a full run record when its evidence materially supports an experiment.

### 3. Capture now; understand later
During physical lab work, minimize human interruption. Prefer automatic capture and short timestamped observations. Deep explanation belongs in post-lab review.

### 4. Separate the human view from the forensic record
A session should normally have layers:

- **session.md** — concise human summary, readable in roughly 1–2 minutes;
- **session.yaml** — structured identity, status, capture provenance/coverage, experiment/run references;
- **timeline.jsonl** (or timeline.md when more practical) — detailed chronology, commands, setup/tool failures, warnings, low-level timestamps worth preserving;
- **runs/** — structured evidence for meaningful experimental runs;
- **evidence.json** — artifact registry, hashes, storage references, known missing evidence;
- **analysis.md** — deep post-lab reasoning, created during post-lab review rather than capture.

Do not put the full forensic chronology or long command listings into `session.md`. Do not duplicate information already present in run records unless needed to understand the session quickly.

### 5. Separate evidence from interpretation
Maintain these distinctions:
- **raw evidence** — logs, video, telemetry, code/config state;
- **observation** — what was directly observed/measured;
- **hypothesis** — a proposed explanation/prediction;
- **proposed finding** — an interpretation the evidence appears to support;
- **reviewed/validated finding** — a conclusion that passed appropriate evidence and human review;
- **decision** — an action/choice based on findings and constraints.

Never silently upgrade an agent hypothesis into a validated finding.

### 6. Preserve uncertainty, contradictions, and corrections
Record competing explanations, unexplained behavior, negative results, and conflicting evidence. Do not optimize the notebook for a clean success narrative.

If later inspection reveals that earlier evidence or interpretation was wrong, preserve the historical record and explicitly document the correction/supersession. Do not silently rewrite history.

### 7. Treat demos appropriately
A successful run demonstrates that behavior occurred under that run's conditions. Do not generalize reliability without supporting repeated/controlled evidence.

### 8. Record capture provenance and coverage
Every physical session should say how the record was captured and what it may be missing. This is especially important for retrospective reconstruction and multi-agent lab days.

Prefer structured fields such as:

    capture:
      method: retrospective        # live|retrospective|mixed
      sources:
        - codex_session
        - git
        - filesystem
        - operator_recollection
        - telemetry
      coverage: partial            # complete|partial|unknown
      known_gaps:
        - activity before this agent session
        - video not captured

Do not claim complete-day coverage merely because one agent session was reconstructed carefully.

### 9. Lab-book automation does not authorize robot motion
Never infer permission to actuate a physical robot from permission to update the notebook. Respect independent safety and execution controls.

## Core relationships

    Project -> Experiment -> Session -> Run -> Evidence
                                          |
                                          v
                             Analysis -> Finding/Decision
                                          |
                                          v
                                Share / Publish

An experiment may span multiple sessions. A session may contribute to multiple experiments. A session also contains non-run activities such as preflights, diagnostics, and cleanup.

## Agent responsibilities by mode

### Development
Retrieve relevant prior findings/decisions; associate substantial work with a project/experiment; simulate what can be learned without robot time; preserve assumptions requiring physical validation.

### Pre-lab
State what each physical test is intended to learn; prioritize by information value and physical necessity; define success/failure criteria; ensure evidence capture is ready; prepare fallback/isolation tests and a minimum useful experiment; flag unreviewed/high-risk control changes.

### In-lab
Reduce documentation burden; preserve activity/run boundaries, code/config state, evidence, brief observations, and material agent changes; troubleshoot rapidly without presenting guesses as facts; preserve unresolved questions. Keep the human-facing summary lightweight.

### Retrospective capture
Reconstruct what happened from available sources before context is lost. Preserve provenance and uncertainty. Create a concise session summary plus forensic timeline/evidence references. Do not perform a long root-cause analysis unless necessary to correct factual evidence. Explicitly record coverage and known gaps.

### Post-lab
Use the preserved capture as input. Audit material changes; distinguish tested from untested; compare runs/evidence; separate observations from explanations; identify contradictions/missing evidence; propose high-information next tests; seek human review before promoting consequential conclusions. Put substantial reasoning in `analysis.md`, not the capture timeline.

### Share / Publish
Trace claims to reviewed evidence. Lightweight sharing should not overstate generality. Rigorous publication should clean experimental code, add tests/docs, and preserve reproducibility/provenance.

## What belongs in session.md

Optimize `session.md` for a researcher returning days or months later. It should normally answer:

1. What were we trying to learn/accomplish?
2. What did we physically test?
3. What happened — including important failures or sim-to-real differences?
4. What material code/config changes mattered?
5. What does the evidence support so far?
6. What remains uncertain or unreviewed?
7. What should receive attention in post-lab analysis / the next lab session?

Detailed shell commands, routine dependency/tool setup failures, exhaustive warnings, and low-level timestamps belong in the forensic timeline unless they materially affected the experiment.

## Writing style

Lab records should be concise, factual, and useful months later. Prefer explicit uncertainty over persuasive prose. The existence of detailed evidence is not a reason to make the default human view long.

## Multi-agent behavior

Codex, Claude, and future agents use this same protocol. Do not create agent-specific versions of scientific conclusions. Record agent/session provenance where useful, but organize knowledge around projects/experiments/runs rather than conversations.

A physical lab session may span multiple agent sessions. Merge their evidence at the lab-session level while preserving which source supplied each reconstructed fact when material.

## Human authority

Agents may draft observations, hypotheses, analyses, and proposed findings. Consequential or reusable findings retain review status until explicitly reviewed/accepted by the researcher.
