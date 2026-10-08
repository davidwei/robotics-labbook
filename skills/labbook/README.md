# Lab Book Skill

This directory contains the canonical, agent-independent protocol for the Robotics Lab Book. Codex, Claude Code, and future agents should follow the same methodology rather than maintaining separate note-taking systems.

## Canonical source

The canonical skill is:

    skills/labbook/SKILL.md

Supporting mode-specific guidance is under `workflows/`. Minimal record examples are under `schemas/`.

Keep one canonical copy here. Agent-specific installations should point to or copy this directory, not fork its contents.

## Get the skill on a development machine

Because this repository is private, first make sure the machine/user has GitHub access, then:

    mkdir -p ~/robotics
    git clone git@github.com:davidwei/robotics-labbook.git ~/robotics/robotics-labbook

To update later:

    git -C ~/robotics/robotics-labbook pull --ff-only

## Use with Codex

Make `skills/labbook` available through the skill-discovery mechanism supported by your installed Codex version. Prefer a symbolic link when filesystem skills are supported so pulling this repository updates the skill automatically.

If Codex is working in another robotics repository, add a thin project instruction such as:

    ## Robotics Lab Book
    For experiment planning, physical robot testing, post-lab analysis,
    or publication provenance, follow:
    ~/robotics/robotics-labbook/skills/labbook/SKILL.md

    The lab book is a separate repository. Do not copy code diffs into it;
    reference exact revisions in this repository.

## Use with Claude Code

Make the same canonical `skills/labbook` directory available through the skill/instruction mechanism supported by the installed Claude Code version. Prefer a symlink or thin wrapper rather than a second copy of the protocol.

A robotics project's `CLAUDE.md` can contain:

    ## Robotics Lab Book
    For experiment planning, physical robot testing, post-lab analysis,
    or publication provenance, follow:
    ~/robotics/robotics-labbook/skills/labbook/SKILL.md

    Treat the lab book as the research index; this repository remains
    the source of truth for its code history.

Exact Codex/Claude skill installation paths and commands can change across releases. Use the current agent's documented discovery mechanism while keeping this repository as the source of truth.

## Expected multi-repository layout

    ~/robotics/
      robotics-labbook/       private durable research record + canonical skill
      unitree_g1_lerobot/     code repository
      lerobot/                code repository
      demos/                  code repository

The lab book references code repositories; it does not replace them.

## Five operating modes

1. **Development** — retrieve prior knowledge, develop/simulate, preserve experiment context.
2. **Pre-lab** — create a prioritized, instrumented physical test plan.
3. **In-lab** — minimize interruption; capture runs, observations, code state, and evidence.
4. **Post-lab** — deeply audit changes/evidence; produce proposed findings and next tests.
5. **Share/Publish** — create downstream outputs whose claims match the evidence.

## Updating installed copies

If the agent installation uses a symlink, simply pull this repository. If it uses a copied skill, reinstall/copy from the canonical directory after pulling.

## Safety

This skill governs research records and reasoning. It does **not** grant an agent permission to actuate a physical robot. Robot execution, safety limits, emergency stops, and human authorization remain independent controls.
