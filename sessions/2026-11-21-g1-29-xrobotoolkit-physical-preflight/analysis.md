# Initial authority-hold fault analysis

## Reviewed observations

- The operator reported **no visible movement or disturbance** during the failed hold.
- The hold faulted with `Measured displacement limit exceeded` after 27 report-loop samples and at reported authority weight no greater than `0.18`.
- Retained hold samples show only `0.000084 rad` maximum start-relative arm motion; the state that crossed the `0.05 rad` guard was not retained by the slower report loop.
- Three weight-zero packets were reported sent, but physical handover was not independently established.
- A post-fault passive run showed live mode `(5, 0)` and a final pose within `0.01812 rad` of the pre-hold pose.
- A subsequent 20-second passive monitor retained 862 samples with only `0.000240 rad` total arm-position span and `0.000120 rad` maximum consecutive-sample jump. It found no persistent or repeated feedback spike.

## Candidate explanations

1. **Torque/support transition during authority blending is plausible but unproven.** Gravity feedforward was deliberately disabled because the current reduced model assumes a fixed waist while PC1 stock balance moves the waist. As authority weight rises, stock arm support is reduced. At a measured-pose target, the new PD controller initially contributes almost no position torque. The transferred URDF predicts a maximum arm gravity torque of approximately `1.87 Nm` at the post-run pose, at the right shoulder roll. At weight `0.18`, the nominal unsupported component is approximately `0.34 Nm`, while the authority-weighted effective proportional stiffness is `10.8 Nm/rad`. The nominal reduced model alone predicts roughly `0.031 rad` equilibrium error, below the `0.05 rad` guard, but the physical BrainCo/dummy-hand inertia mismatch and moving waist can increase this. This evidence supports investigation; it does not establish root cause.
2. **A brief feedback outlier remains possible.** The guard evaluates every control-thread state while the report loop samples separately, so a one-sample excursion can fault without appearing in retained report rows. The 20-second passive monitor found no such outlier, reducing but not eliminating this explanation.
3. **A small physical transient below easy visual detection remains possible.** The operator's observation rules out obvious motion, not a brief joint change near the `0.05 rad` threshold.
4. **A stale activation baseline is less supported by code inspection.** Activation resets `initial`, `target`, and `previous` from a fresh state after the publisher becomes ready.

## Next high-information work

- Add a bounded recent-state ring buffer and structured fault snapshot containing joint name, initial/measured/previous position, delta, tick, timestamp, authority weight, measured velocity and torque estimate.
- Exercise the new fault evidence path with fake transport and physics tests before any new physical authority request.
- Review an arm-gravity strategy that uses live torso orientation and the actual asymmetric end-effector inertias. Do not simply restore the fixed-waist feedforward model or widen the displacement envelope.
- Require a new explicit operator review before any repeat hold. `05a` remains blocked.
