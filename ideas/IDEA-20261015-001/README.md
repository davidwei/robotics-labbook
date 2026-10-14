# IDEA-20261015-001 — Camera-aware certificate redirect link

Status: proposed; implementation deferred at operator request.
Project: Unitree G1 / PC2 Isaac Teleop. Physical validation: not started.
Target repositories: `MoissanClub/unitree_g1_dev` PC2 integration and the
CloudXR certificate-page integration in local `/home/dwei/IsaacCapture`.
Related evidence: [camera streaming analysis](../../sessions/2026-10-15-g1-vr-camera/analysis.md).

## Task

Minimize headset keyboard entry by prefilling streaming dimensions in the
certificate-accepted page's NVIDIA client button. The PC2 integration should read
actual dimensions from fresh camera-frame metadata (not just requested capture
settings), derive supported per-eye dimensions, and supply URL parameters to the
redirect server. Avoid copying RGB pixels for metadata discovery. Keep the generic
CloudXR redirect implementation independent of LeRobot's frame-channel format.

For the current 640x480 source, the proposed test setting is perEyeWidth=640,
perEyeHeight=512, codec=h264. This is a per-eye rendering choice, not a guarantee
of pixel-for-pixel camera mapping or a 640x480 packed encoder output. Verify client
alignment constraints and parameter support against the deployed client.

## Acceptance

- Actual fresh camera dimensions drive optional, configurable streaming settings.
- Preserve existing host/port prefill; retain explicit operator overrides.
- Show selected dimensions; recalculate on page load. Missing/stale metadata falls
  back to normal client defaults without blocking access.
- Verify escaping/URL construction and the hosted client's application of parameters.
- Verify negotiated encoder dimensions in logs and repeat a camera-only headset
  comparison of FPS, encoding duration, and loss; no robot motion required.
- No headset typing in the normal path; prefer laptop configuration for overrides.

Next agent action: inspect PC2 cert-page patch and upstream redirect interfaces,
then implement metadata-to-client-parameter plumbing when this task is selected.
Prerequisites: frame-channel path supplied to PC2 integration, readable metadata,
and confirmation of hosted client query parameters. Ready for design/implementation,
not yet implemented or validated. Do not change defaults during the current test.
