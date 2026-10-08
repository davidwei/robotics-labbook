# Robotics Lab Book Design

## Purpose

The lab book is research infrastructure: a durable, searchable record connecting ideas, experiments, physical robot runs, code revisions, evidence, analysis, decisions, and eventual publications. Documentation is a consequence of this infrastructure, not the primary goal.

## Primary constraint: robot time is scarce

### 1. Prepare — out of lab
Ideation, development, simulation, and experiment design. Arrive at the robot with test-ready code, explicit questions, success criteria, instrumentation, and fallback plans.

### 2. Execute — in lab
Human attention stays on the robot, safety, and physical observations. Codex/Claude may iterate rapidly. The system behaves like a flight recorder: capture what happened without demanding extensive documentation.

### 3. Analyze — out of lab
Reconstruct what agents changed, compare runs, inspect evidence, identify sim-to-real differences, challenge proposed explanations, and decide what was actually learned.

### 4. Share
Create accessible videos, short posts, demos, and newsletter material without implying stronger validation than the evidence supports.

### 5. Publish
Prepare maintainable open-source code, PRs, technical articles, and reproducible results. Lab-tested experimental code is not automatically publication-ready.

Findings and unresolved questions feed the next preparation cycle.

## Core entities

- **Project** — a long-lived capability or research direction.
- **Experiment** — a question or hypothesis; may span multiple sessions.
- **Session** — a bounded period of physical robot access; may serve multiple experiments.
- **Run** — a specific execution on hardware or in simulation.
- **Evidence** — logs, telemetry, ROS bags, videos, measurements, code revisions, timestamped observations.
- **Finding** — an interpretation supported by evidence, with review/confidence state.
- **Decision** — a consequential choice and rationale linked to evidence/findings.
- **Publication** — downstream video, post, newsletter, PR, article, tutorial, etc.

## Evidence model

    raw evidence
      -> observation
        -> hypothesis
          -> experiment
            -> proposed finding
              -> reviewed/validated finding
                -> decision / reusable knowledge

An agent explanation is not a validated finding merely because it is plausible. A successful demo proves what occurred in that run; it does not by itself establish general reliability.

## Source-of-truth boundaries

| Information | Source of truth | Lab book role |
|---|---|---|
| Source/code history | Git/GitHub | repo + exact revision/PR references |
| Agent sessions | Codex/Claude native/archive | references + useful summaries |
| Simulation artifacts | simulator/artifact store | config/results + references |
| Robot telemetry/ROS bags | artifact store | run association + references/hashes |
| Videos | artifact store/YouTube | references + timestamps/annotations |
| Experiments | Lab book | canonical |
| Research conclusions | Lab book | canonical |
| Decisions | Lab book | canonical |
| Publications | destination platform/repo | provenance links |

## Exact code state for physical runs

A Git commit is sufficient only when it represents exactly what ran. Rapid lab iteration may involve uncommitted modifications. Prefer either automatic local/checkpoint commits on an experiment branch/worktree, or record the base commit plus a complete patch/snapshot including relevant untracked files.

Never claim a later clean commit was the code tested if the actual run used a different working tree.

## In-lab design rule

**Capture now; understand later.**

During physical testing:
- minimize questions and documentation overhead;
- preserve timestamps and run boundaries;
- record code/config state;
- capture telemetry/video/log references;
- allow very short human observations;
- preserve agent-session provenance;
- never promote a speculative explanation to a validated finding.

Robot-motion authorization and safety controls remain separate from notebook automation.

## Post-lab review

A review should produce:
1. **Change audit** — what agents changed; tested vs untested; reviewed vs unreviewed.
2. **Run comparison** — differences in code/config/evidence across runs.
3. **Interpretation** — observations, candidate explanations, findings, uncertainties, contradictions.
4. **Next experiments** — high-information tests, especially those distinguishing competing hypotheses.
5. **Human review** — accept/correct/reject conclusions and decide what is ready for reuse/publication.

## Publication tracks

**Share:** fast and accessible — videos/Shorts, posts, demos, newsletters.

**Publish:** rigorous and reusable — PRs, open-source releases, technical articles, reproducible experiment reports.

## Storage principles

The durable format is Git containing primarily Markdown plus small YAML/JSONL metadata. Large artifacts should not normally be committed here. Store stable logical references and, where useful, content hashes.

Prefer append-only raw event/timeline records. Analysis and conclusions may evolve. Validated findings preserve provenance and record when superseded.

The schema should support multiple researchers even though this is currently a personal lab book: records may contain owner, authors, and participants.

## Initial logical layout

    projects/       long-lived goals/status/roadmaps
    experiments/    hypotheses, plans, analyses, conclusions
    sessions/       physical-lab timelines and run records
    knowledge/      reviewed findings, decisions, troubleshooting, procedures
    journal/        generated chronological views
    publications/   provenance/planning for shared and published outputs
    skills/         agent-independent lab-book protocol

Do not over-structure before real usage establishes what is valuable.

## Long-term goal

The defining workflow is to review everything that happened in a physical robot session, explain every material code/configuration change, link changes to runs and evidence, distinguish what was observed from what is merely hypothesized, identify what was actually learned and what remains uncertain, and propose the highest-value tests for the next scarce period of robot access.
