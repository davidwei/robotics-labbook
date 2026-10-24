# SO101 gravity comparison — 2026-10-23

Status: exploratory simulation completed; physical cause remains unvalidated. Operator requested two servo models, 12 V and 7.4 V, each with gravity on/off. No robot actuation or controller change occurred.

## Reproducibility

- Source: [MoissanClub/lerobot 30518ef](https://github.com/MoissanClub/lerobot/commit/30518efaf3926dc4f830639c5882ede8221e3b97), branch `lab/so101-intel-warning-20261023`, directory `simulation/so101_gravity`. Four model/config pairs, pinned upstream URDF/license, dependency lock, script and tests are committed there.
- Separate Intel-Mac environment `/Users/dwei/lerobot/.venv-sim`: Python 3.11.17, MuJoCo 3.2.7, NumPy 1.26.4, Matplotlib 3.9.4. Existing robot-control environment unchanged.
- Physical input: `state-machine-1792809011865027000.jsonl`, executed controller `fc5040e`; simulation uses recorded sent position commands from Start to just before first Awaiting alignment, with all six joints dynamic. Initial positions measured, initial velocities assumed zero. The transition hold command is excluded.
- Public model revision `a758567c3978dfeefe282ede0500085a48fe8f78`. Operator states assembly matches public SO101. Joint-coordinate alignment remains an assumption despite matching LeRobot kinematics example conventions.
- Local artifacts: `/Users/dwei/lerobot/outputs/development/so101-gravity-final/` (`comparison.png`, `comparison.pdf`, CSV, NPZ, JSON, XML and numerical check).
- [Private artifact archive](https://github.com/davidwei/robotics-labbook/releases/download/so101-session-20261023/so101-gravity-four-cases-20261023.tar.gz): includes results, original physical input log, follower calibration and saved rest. SHA256 `47cfcf3a578322f6e9ede858e116941c4f8816967da4dc6a80d25806a17d12f4`. Individual input hashes and script hash are in summary.json.

## Models and assumptions

Nominal 12 V: stall torque 30 kg·cm, no-load .222s/60°, stall current 2.7 A. Nominal 7.4 V: 19.5 kg·cm, .192s/60°, 2.5 A. [Supplier reference](https://docs.waveshare.com/ST3215_Servo).

Actuator model approximates a DC motor with saturated PWM drive and linear back-EMF; position PD is translated to duty using an exploratory interpretation of documented P/4 and D/8 scaling. P=16/I=0/D=32, assumed derivative period 1ms, reflected rotor inertia .0001 kg·m², mechanical friction zero. Gain mapping/sample time are not identified firmware behavior. Current specifications are not a fitted current-sensor model. Original rigid-body inertias retained; visual/contact meshes and active joint constraints removed for a free-space causality comparison. No obstacle/contact/protection/backlash model. Model XML is a passive plant; companion JSON plus Python implement its control law.

Both variants operate at their nominal rated voltage. **Neither reproduces the approximately 4.7–4.9 V reported in the physical run.** This comparison cannot identify the installed servo or its actual supply/effort.

## Results

Last pre-transition sent shoulder goal: **6.4181°**. Measured shoulder: **11.8681°** (5.4500° above that goal). This differs slightly from the 5.3626° error against the next leader target at the transition.

| Model | Final shoulder | Offset above final sent goal | Shoulder RMSE, final 4s | Whole-replay shoulder RMSE |
|---|---:|---:|---:|---:|
| 12 V, gravity off | 6.4427° | .0246° | 5.5645° | 2.5286° |
| 12 V, gravity on | 10.0646° | 3.6465° | 1.7954° | .8834° |
| 7.4 V, gravity off | 6.4668° | .0487° | 5.5568° | 2.5192° |
| 7.4 V, gravity on | 12.4156° | 5.9975° | .9919° | .9325° |

Evaluating gravity along the **measured** whole-arm configuration predicts **+.5325 to +.5714 Nm** shoulder torque during the final four seconds. Positive torque pushes toward increasing shoulder angle, opposite the negative position correction requested in that interval. This sign is checked against the negative gradient of gravitational potential energy.

Gravity-off runs approach the sent goal closely. Gravity-on runs retain an offset in the observed direction and have smaller final-four-second mismatch. The nominal 7.4 V model is closer at the endpoint, while 12 V has slightly lower whole-run RMSE; these are model comparisons, not variant identification.

## Sensitivity and interpretation

36 additional four-second simulations vary gain scale .5/1/2 and shoulder joint-zero offset -5/0/+5°, for both variants and gravity settings. Each short simulation restarts from measured state at the beginning of that interval, unlike the four full replays.

- 12 V gravity-on final shoulder spans approximately **7.91–15.46°**.
- 7.4 V gravity-on spans approximately **8.79–21.78°**.
- Gravity-off endpoints stay near **6.37–6.47°** across those tested settings.

These parameter ranges are illustrative, not measured uncertainty bounds. Remaining friction, zero alignment and actuator dynamics can change conclusions. Exact plateau timing is not reproduced or validated. The sent shoulder goal itself rises during this window: even gravity-off models increase their angle, so angle increase alone is not proof of gravitational sag. The stronger evidence is the pose-dependent offset relative to the sent goal and the predicted gravity direction.

Proposed interpretation: the nominal rigid-body model makes gravity/PD residual a plausible explanation for this run. It does not establish that gravity alone caused the event or exclude friction, binding, power limitations or servo behavior. Curve agreement must not be promoted to a reviewed physical finding.

## Validation and next action

Four meaningful simulation tests passed: full imported joint order and nominal mass/XML round-trip; gravity torque versus finite-difference potential-energy gradient; gravity-off zero-error equilibrium versus gravity-on drift; PD polarity/saturation and rated variant differences. Ruff passed. Reducing integration timestep from 1ms to .5ms over the last four seconds changed shoulder results by at most **.0052° (12 V)** / **.0095° (7.4 V)**. This establishes numerical consistency under the chosen model, not model accuracy.

Next agent action: review plots with the operator; independently verify coordinate mapping and installed servo/power conditions; compare clear static poses with elbow/wrist fixed versus changing. Only then consider identifying gains/friction or revising nonprogress detection. Physical validation pending; no automatic gain, supply or state-machine threshold changes.
