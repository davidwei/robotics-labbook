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

RUN-20261103-002 repeated the physical workflow after a fresh read-only preflight.
The first accepted arm was invalidated when tracking became intermittent; the
gate correctly blocked start until a new upright/fresh/moving window and A+B arm.
After start, the packet record contains six PLANNER-to-POSE entries and six
POSE-to-PLANNER returns rather than the requested single cycle. Local `O` stopped
SONIC when the repeated toggles exceeded the authorized sequence; the deployment
reached its normal stop path. The PICO manager later emitted OFF and shut down
cleanly. The operator confirmed only that the run was done; no separate physical-
behavior assessment was recorded, so this repeat is a protocol deviation rather
than a second successful-run claim.

The repeat retained 15,690 PICO input samples and 11,433 outgoing packets. The
600-second whole-body recorder expired 96.999 seconds before the manager's final
OFF packet, so it does not continuously cover the final run interval or stop.
A later 50-second post-stop capture retained 14,636 LowState and 13,931 torso-IMU
samples, zero LowCmd, zero drops and zero callback failures. Treat the intervening
DDS interval as a known evidence gap; SONIC CSV and PICO packet logs still cover
their own processes.

Cleanup explicitly restored the stock controller. Motion-switcher initially
reported no active service. Selecting `normal` failed (`7004`) and the associated
damp request failed (`3102`), so that attempt was not treated as restoration.
Selecting the documented G1 stock `ai` service then returned `0`, and requesting
FSM 1 damp returned `0`. A later readback had fallen to FSM 0; a final FSM 1
reassertion returned `0`, five timed readbacks through 5 seconds remained at FSM 1,
and the final independent query reported service `ai`, FSM 1. The final 20-second
capture had 3,736 LowState, 6,061 torso-IMU and 3,540 LowCmd samples, no CRC or
finite-value failures, no motor-status errors, no drops/callback failures and
maximum measured joint speed 0.084 rad/s. Its sampled LowCmd had zero Kp, Kd and
feed-forward torque at both the first and last samples; this is recorded without
inferring undocumented FSM semantics.

All SONIC, PICO manager, capture and XRoboToolkit RoboticsService processes were
stopped. Ports 5556, 5557 and 60061 were no longer listening. The robot stock
controller remained active in verified FSM 1 damp for physical lab shutdown.

Mandatory operating rule: whenever the PICO headset is removed from the
operator's head, recalibrate the foot/ankle trackers. Before every physical policy
start, reconfirm that the PICO-reported skeleton matches the operator's actual
standing posture and that the existing freshness/motion gate passes. Prior arm
acceptance does not survive headset removal, mismatch, stale/frozen tracking or
reconnection.

Next: perform post-lab alignment of PICO packets, SONIC CSV logs and available
whole-body telemetry, with explicit treatment of the recorder gap and repeated
mode transitions. Preserve the gantry-only restriction: SONIC stop does not
restore stock control automatically, and stale-input behavior remains unvalidated.
