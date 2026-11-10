# November 11, 2026 — CloudXR client-first bookmark experiment

**Experiment:** EXP-20261111-001 · **Status:** Planned; no tests have run.  
**Decision to make:** Which URL should be bookmarked so a headset operator enters **each server IP only once**, with no ADB and no IP re-entry on repeat sessions?

## The two options

1. **NVIDIA-hosted web client:** bookmark the exact client/version used (candidate: `https://nvidia.github.io/IsaacCapture/client/v1.6.152/#/generic`; strip the incidental `utm_source` parameter). Open the client first, enter host A once, follow its certificate link, return to the original client tab, and connect. Determine whether the saved host persists across reload, full browser restart, and headset reboot.
2. **Server-hosted web client:** if the installed service supports local hosting, bookmark `https://HOST_A:48322/client/` (with a distinct bookmark for HOST_B). Opening that URL already names the host in the address bar, but **does not prove** the client auto-selects the WSS host. Observe whether the connection form still asks for an IP, whether it remembers host/port, and whether this remains true across restarts.

**Do not confuse these URLs:** `https://HOST:48322/` is the certificate-acceptance page, **not** the web client; use `/client/` only when the service hosts it. Do not use the pending PR #1170 `/connect/` shortcut for the main comparison.

## Preconditions / controlled variables

- Prefer a current **Meta Quest** browser. The October 28 labbook PICO 4 had Chromium 105, below NVIDIA's Chrome 125 requirement: a PICO version failure is not evidence against the connection flow. Test PICO only after verifying a compatible browser.
- Use an unmodified NVIDIA client-first flow and a reachable CloudXR WSS server. Record exact hosted client URL/version, installed IsaacCapture/CloudXR version/commit, headset firmware/browser, `--host-client` state, and server IP/port. Note any locally patched `isaacteleop` environment and avoid relying on its `/connect/` modification.
- Use connection-only or simulation. **No physical robot connected, actuated, or commanded.** If streaming is enabled, Jetson Orin tests select **H.264** per NVIDIA's current quick-start. A successful TLS/WebSocket connection, a video stream, and reliable VR controls are separate outcomes.
- Count *manual typing* (server IP, port, and navigation URL separately). Bookmark creation/setup is a one-time action; record any URL typing required at setup. Never assume IP persistence means “cookies”: it might be localStorage/IndexedDB/browser profile or URL parameters.
- Do not clear existing browser data just to produce a clean state. If an isolated browser profile/private window is available, it can provide a fresh-state trial; otherwise document the existing stored-state baseline.

## Run sheet (record actual results; do not fill from assumptions)

| ID | Action | Pass criterion | Result / evidence |
| --- | --- | --- | --- |
| T0 | Record environment; open web client; note existing host field *before editing*. | Baseline and version captured. | Pending |
| T1 | Client-first on server A: enter IP once; follow the client's cert link (`https://A:48322/`), accept self-signed certificate in the new tab, return to original client tab, connect. | IP remains in client, no second IP entry; observe certificate/connection outcome. | Pending |
| T2a | Bookmark hosted client; reload its tab, then reopen bookmark. | Host A and port preserved without retyping. | Pending |
| T2b | Fully close and reopen headset browser; open hosted-client bookmark. | Host A and port preserved without retyping. | Pending |
| T2c | Reboot headset (if practical), open hosted-client bookmark. | Host A and port preserved without retyping. | Pending / not tested |
| T3 | Confirm local hosting; open and bookmark `https://A:48322/client/`; repeat reload and browser restart. | Record whether host is inferred, restored, or requires typing; connect only to A. | Pending / unsupported |
| T4 | With independent server B available, connect to B once, then use A and B bookmarks alternately (A → B → A). | Each server requires no second typed IP; no silent wrong-host connection. | Pending / B unavailable |
| T5 | Where safely inspectable (e.g., desktop browser devtools on the same client origin), check URL query/hash, cookies, localStorage and IndexedDB. | Report observed storage location; otherwise “mechanism unverified.” | Pending / not inspectable |

When a certificate is already trusted on the headset, mark the certificate branch as **not exercised**, rather than claiming a fresh certificate test. To test a new certificate, use a separate permitted test server/profile instead of removing unrelated trusted-site state.

## Minimum useful experiment

Complete **T0, T1, T2a, and T2b on one compatible headset and server A**. This determines whether the client's documented flow avoids duplicate entry and whether a hosted-client bookmark survives a browser restart. T2c, T3, T4, and T5 add confidence and compare bookmark approaches; they are not prerequisites for a useful result.

## Result capture (fill in on Nov 11)

| Field | Observation |
| --- | --- |
| Date/time/timezone, operator, headset/browser/version | |
| Server A label / IP:port; server B if available | |
| Hosted-client exact URL/version; local client available? | |
| T1 manual IP count / repeated after cert? | |
| T2a/T2b/T2c IP restored? / manual IP count | |
| T3 local /client/ behavior / manual IP count | |
| T4 A → B → A correct host restored? | |
| Storage observation: cookies / localStorage / IndexedDB / URL / unknown | |
| Codec, TLS, WebSocket, first frame / errors (separate) | |
| Recommended bookmark for **each** server + reason | |
| Links to screenshots, logs and operator notes | |

**Decision rule:** Prefer the simplest bookmark with zero repeat typing **and correct server selection after browser restart**. If hosted-client storage keeps only one *last used* host, it fails the independent per-server bookmark objective even if it works well for one server. A bookmark embedding the host in its URL (local `/client/` or a validated client deep link) may be better for multiple servers, but verify the actual connection form and cert flow before adopting it.

**Stop / limitations:** Any incompatibility gate (e.g., unsupported PICO browser), incorrect server selection, unexpected certificate issue, or client failure should be recorded separately from the manual-entry question. Stop after collecting diagnostic evidence; do not bypass browser security or connect to a physical robot.

**Context:** [Reviewer's comment on PR #1170](https://github.com/NVIDIA/IsaacCapture/pull/1170#issuecomment-6665746778) · [NVIDIA quick start](https://github.com/NVIDIA/IsaacCapture/blob/main/docs/source/teleop/quick_start.rst) · [October 28 PICO connection test](../../ideas/IDEA-20261027-003/README.md) · [Certificate-page proposal](../../ideas/IDEA-20261015-001/README.md)
