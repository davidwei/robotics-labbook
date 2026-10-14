# IDEA-20261015-002 — Preserve discrete XR button commands

Project: Unitree G1 / LeRobot. Status: proposed, not implemented.
Target: MoissanClub/lerobot, XR controller acquisition and LatestSlot consumers.
Physical validation: pending; no short-pulse delivery test yet.

Problem: current button booleans share latest-value delivery with continuous poses.
A press followed by release before the next consumer read can be lost. A fixed
one-second hold reduces risk under ordinary conditions but cannot guarantee delivery.

Next agent action: inspect button acquisition semantics and downstream stop/start
mapping; design discrete transition preservation alongside latest-value poses.
Prerequisites: choose acknowledgment/consumption ownership, reconnect/reset rules,
and distinguish ordinary controls from safety-critical commands.

Acceptance: deterministic tests cover press/release between consumer polls, delayed
consumer, duplicate delivery, release, disconnect and reconnect. Add clear user
acknowledgment; preserve stop-related events until handled without accidental replay
of start commands after reconnect. Verify real headset transitions at acquisition
and consumption. Do not infer end-to-end reliability from a PC2-only queue test.
No robot motion is authorized by this task record.

Evidence: [session analysis](../../sessions/2026-10-15-g1-vr-camera/analysis.md).
