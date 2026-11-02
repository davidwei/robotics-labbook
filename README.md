# Robotics Lab Book

A private, durable research record for robotics work done with humans and AI coding agents.

## Why this exists

Physical robot access is the bottleneck. Development and analysis can happen away from the robot, while lab time is dominated by validation, sim-to-real differences, and rapid troubleshooting. During those sessions Codex and Claude may iterate faster than a human can carefully review every change.

The lab book therefore optimizes for **learning per hour of physical robot access** and for careful reconstruction and analysis afterward.

## Research workflow

1. **Ideation / development / simulation (out of lab)** — develop hypotheses, code, simulations, and test plans.
2. **Physical validation (in lab)** — validate on hardware, troubleshoot sim-to-real differences, and capture evidence with minimal interruption.
3. **Post-lab analysis (out of lab)** — carefully review agent/code changes and results; distinguish observations, hypotheses, and conclusions.
4. **Share** — turn reviewed work into videos, short posts, demos, and monthly newsletters.
5. **Publish** — rigorously prepare open-source changes, technical articles, and reproducible results.

See [docs/design.md](docs/design.md) for the design.

## Research indexes and operating synthesis

- [Session-to-idea/project audit](docs/session-reference-audit.md): every checked-in session and evidence boundaries.
- [Draft session-derived lab protocol](docs/lab-protocol.md): staged preparation, execution, stop verification and closeout.
- Projects: [Unitree G1](projects/unitree-g1/README.md), [PICO evaluation](projects/pico-4-loan/README.md), [SO-101](projects/so101/README.md).

## Source-of-truth principle

This repository is the **research index and knowledge layer**, not a copy of every artifact.

- Source code and diffs remain in their Git/GitHub repositories.
- Agent transcripts remain in their native/archive locations.
- Large videos, ROS bags, telemetry, and simulation artifacts live outside normal Git.
- The lab book records experiments, observations, analyses, findings, decisions, and stable references to the evidence.

The central relationship is:

    Project -> Experiment -> Session -> Run -> Evidence
                                          |
                                          v
                             Analysis -> Finding/Decision
                                          |
                                          v
                                Share / Publish

## Agent skill

The canonical, agent-independent Lab Book skill is in [skills/labbook/](skills/labbook/).

Start with [skills/labbook/README.md](skills/labbook/README.md) for installation and usage with Codex and Claude Code.

## Privacy and licensing

This repository is intended to remain private. No license is granted for its contents. Material intentionally promoted to public MoissanClub repositories, articles, datasets, or other publications should receive an appropriate license at publication time.
