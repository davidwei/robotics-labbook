# In-Lab

Goal: preserve evidence while consuming as little operator attention as possible.

For each meaningful run:
1. mark the run boundary/time;
2. capture exact code/config state actually executed;
3. associate relevant experiment(s);
4. capture references to telemetry/log/video evidence;
5. accept a very short operator observation;
6. record material agent changes made since the previous run.

Prefer timestamped facts over explanations.

When troubleshooting, agents may propose hypotheses and make authorized code changes, but must not record guesses as findings.

Preserve failed runs and negative evidence.

Do not let lab-book automation authorize robot actuation. Physical execution follows the robot project's separate safety controls and human authorization.
