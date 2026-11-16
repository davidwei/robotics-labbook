# Quest Pro XRoboToolkit to dual-UR5e MuJoCo

**Session:** SESSION-20261116-001 · **Experiment:** [EXP-20261115-001](../../experiments/EXP-20261115-001/plan.md) · **Status:** ended; minimum useful result met, clutch/repeat review pending

## Objective and result

Determine whether the released XRoboToolkit Quest client can deliver Meta Quest Pro head, Touch Pro controller and grip input through the Linux PC Service to the stock dual-UR5e MuJoCo example.

The minimum useful result was met. A 120-second input capture recorded advancing timestamps, finite independently changing head/controller poses, and both side grips reaching 1.0 and returning to zero. After a clean Quest-app and PC-Service restart, the stock MuJoCo example logged right- and left-hand activation and both simulated arms visibly changed pose. A 204.6-second desktop recording and stage screenshots preserve the repeat.

This does not yet pass the full VR-control experiment. During the repeat, several brief unintended left/right grip activations occurred while the operator repositioned the controllers, so clutch independence and regrip behavior need a cleaner review or repeat. Separately, Ctrl+C printed `Teleoperation stopped.` and the recorded simulator PID became absent, but the timeout wrapper reported 137 after its 10-second kill escalation. Clean process shutdown is not established, but that lifecycle defect occurred after successful VR control and does not negate the observed motion.

## Important diagnostics and deviations

- The first full input capture contained only zeros because Head/Controller/Send were not yet enabled. It is retained as setup evidence, not a compatibility failure.
- The passing R1 capture later stopped changing for its final 31 seconds after the requested sequence; all required motion and grip events occurred before that freeze.
- R2 was compromised by opening additional SDK clients while the simulator was running; its console never logged a valid hand activation. Its planned video file was also missing. Preserve it as a diagnostic, not a control verdict.
- Repeated pre-run zero streams were reproduced while the Quest panel still showed WORKING. Force-stopping/relaunching the released app and restarting the exact PC Service process restored live timestamps and poses. This supports stale transport/forwarding state as the immediate recovery boundary, not a reviewed root cause.
- The verified PC Service Debian payload was extracted and run from the evidence workspace because system installation required interactive sudo.
- The initial Python candidate needed transitive pins `cmeel-urdfdom==4.0.1` and `cmeel-tinyxml2==10.0.0`; `pip check` then passed.
- A source-only in-headset motion-status draft was deferred to [IDEA-20261116-001](../../ideas/IDEA-20261116-001/README.md). It was not built or executed in this session.

## Evidence-supported interpretation

Observed evidence supports nominal Quest Pro controller transport and bilateral grip-enabled motion in the released dual-UR5e MuJoCo sample under this single setup. It does not establish quantitative latency/accuracy, repeatability, clean reconnect semantics, reliable clutch isolation, clean process shutdown, G1 compatibility, or any physical-robot behavior.

## Next action

Review the R3 video against activation timestamps. If full clutch validation is desired, perform one short no-probe simulation repeat with deliberate fingers-off-grips pauses. Investigate the non-exiting SDK/native thread separately without requiring the headset.

