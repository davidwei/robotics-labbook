# Retrospective Capture

Use when meaningful physical lab activity already happened but was not recorded live, especially before an agent session/context is closed.

The goal is **preservation and reconstruction**, not deep post-lab analysis.

## Sources

Reconstruct from available sources, in roughly this priority:
1. current/native agent session history;
2. commands, outputs, errors, and test results;
3. Git commits/status/diffs/reflog and exact repository state;
4. filesystem timestamps and created/modified files;
5. telemetry/logs/video/artifacts;
6. operator observations/recollection.

Do not invent missing history.

## Capture provenance

Record:
- method: retrospective;
- which sources were used;
- whether coverage is complete, partial, or unknown;
- known gaps;
- approximate/uncertain timestamps and sequence explicitly.

One carefully reconstructed agent session is not automatically a complete record of the lab day.

## Output layers

### session.md
Keep this to a roughly 1–2 minute human read:
- objective;
- meaningful physical tests;
- key observations/results;
- important failures/sim-to-real differences;
- material code/config changes;
- current evidence-supported state;
- uncertainties/unreviewed items;
- next review/test questions.

### session.yaml
Store identity, status, participants, experiments/runs, agent-session provenance, and capture coverage.

### timeline.jsonl or timeline.md
Put detailed chronology here: commands, setup/tool failures, warnings, timestamps, intermediate corrections, and other forensic detail worth preserving.

### runs/
Create full run records for meaningful experimental executions. Preflights, diagnostics, and cleanup may stay as timeline activities unless their evidence materially supports the experiment.

### evidence.json
Reference preserved artifacts, hashes/storage, transcript/session archive, and known missing evidence.

## Corrections

If reconstruction discovers an earlier measurement/decoder/interpretation error, preserve the original evidence and explicitly record the correction. Do not silently rewrite historical evidence.

## Stop boundary

Do not perform a broad root-cause analysis during retrospective capture. Once the session is safely preserved, leave deeper reasoning for post-lab review and `analysis.md`.
