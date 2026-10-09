# G1 VR teleoperation performance improvements

**Status:** proposed; implementation and physical validation not yet recorded.  
**Owner:** David Wei  
**Date:** 2026-10-09  
**Code target:** `MoissanClub/lerobot`, branch `work/g1-vr-physical`.

## Research motivation

The headset camera stream sometimes falls behind without recovering, and XR controller tracking sometimes lags or briefly drops out.

## Original plan

The complete original proposal is preserved verbatim in [g1-vr-perf-plan.md](g1-vr-perf-plan.md). It defines P1–P5 in order: camera V4L2 backlog; camera/XR thread contention; IK latency; latest-controller-sample mailbox; and watchdog/recording overhead.

These proposed explanations and performance targets are **hypotheses**, not yet validated findings.

## Next Codex action — development / pre-lab

1. Pull the latest lab book and follow `skills/labbook/SKILL.md` in Development and Pre-Lab modes.
2. Read the complete [execution plan](g1-vr-perf-plan.md).
3. Work in the specified `MoissanClub/lerobot` branch, one revertible commit per P1–P5 task, preserving every safety constraint in the plan.
4. Run the requested automated tests and lint after each task; record actual results and commit SHAs.
5. Prepare baseline-versus-changed measurements and the plan's manual checks for supervised hardware testing.
6. Do not autonomously execute hardware-only validation. Keep untested claims marked as such.
7. Update this record with implementation status and link physical experiments/sessions/runs when they occur.

## Handoff status

- Original plan captured: yes.
- Code changes performed by this lab-book addition: none.
- Tests executed by this lab-book addition: none.
- Physical validation performed by this lab-book addition: none.
