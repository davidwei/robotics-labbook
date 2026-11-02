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

## Session evidence index

- [October 15 VR session](../../sessions/2026-10-15-g1-vr-camera/session.md): measured short-press versus held-chord loss motivates discrete-event preservation.
- [October 30 SONIC/PICO session](../../sessions/2026-10-30-g1-sonic-pc2-suspended/session.md): separate backend's full-release latch and sampled stop-ordering issue are comparative evidence, not implementation of the LeRobot event queue.
- [November 3 physical session](../../sessions/2026-11-03-g1-sonic-pico-voice-physical/session.md): repeat contains six POSE cycles; event/input alignment is pending. Do not attribute them to lost/duplicated button events without analysis. Next: retain proposed status for the LeRobot change and review acquisition-to-consumption traces.
