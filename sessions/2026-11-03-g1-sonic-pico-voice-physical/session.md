# G1-29 PICO voice/controller physical run — 2026-11-03

The session tested whether a calibrated PICO workflow could carry a physical
G1-29 run from headset-only arming through PLANNER, POSE, return to PLANNER and
stop without requiring the operator to return to the terminal. The robot remained
gantry-protected with two operators, local `O` and facility E-stop available.

The first launch attempt did not start policy control because controller events
were sent before SONIC completed TensorRT initialization. It was stopped with
local `O`; preserve it as a setup-ordering failure, not a policy run. The restart
used recorder -> SONIC `Init Done` -> XR/PICO manager ordering.

RUN-20261103-001 then completed A+B arm, A+B+X+Y start, A+X enter POSE, A+X
return to PLANNER and A+B+X+Y stop entirely from the headset. The manager logged
the expected PLANNER -> POSE -> PLANNER -> OFF sequence and shut down cleanly.
SONIC reached its normal stop path; CycloneDDS asserted during process cleanup
after control stopped. The operator's observation was: **“a successful run.”**
This is evidence for one successful gantry-protected execution under these
conditions, not a general reliability result.

Independent capture retained 98,021 LowState, 94,929 torso-IMU and 27,834 LowCmd
samples, with no queue drops or callback failures. Maximum receive gaps were
29.087, 28.180 and 40.725 ms respectively. PICO capture retained 3,499 raw input
samples and 1,766 outgoing packets. No synchronized operator video was captured.

Mandatory operating rule: whenever the PICO headset is removed from the
operator's head, recalibrate the foot/ankle trackers. Before every physical policy
start, reconfirm that the PICO-reported skeleton matches the operator's actual
standing posture and that the existing freshness/motion gate passes. Prior arm
acceptance does not survive headset removal, mismatch, stale/frozen tracking or
reconnection.

Next: perform post-lab alignment of PICO packets, SONIC CSV logs and whole-body
telemetry. Preserve the gantry-only restriction: SONIC stop still does not restore
self-support or stock control, and stale-input behavior remains unvalidated.
