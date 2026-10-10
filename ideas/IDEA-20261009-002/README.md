# GPU-assisted G1 camera pipeline

**Status:** proposed; deferred until camera-path profiling justifies it.  
**Owner:** David Wei  
**Date:** 2026-10-09  
**Project:** Unitree G1 VR teleoperation  
**Related idea:** [IDEA-20261009-001](../IDEA-20261009-001/README.md)

## Question

Would a GPU-assisted camera pipeline reduce camera-to-headset latency or CPU contention on the G1 onboard Jetson Orin?

## Motivation

The current diagnostic path captures through OpenCV/V4L2 and publishes CPU `uint8` NumPy frames through shared memory. A naive GPU conversion would add host-to-device and device-to-host copies without removing the V4L2 backlog mechanism, and it could contend with CloudXR/OpenXR for Jetson GPU resources.

GPU acceleration may become useful if profiling shows that CPU video decode (for example MJPEG/H.264) or YUV-to-RGB conversion dominates and the frame can remain in NVMM/CUDA/EGL memory through the renderer.

## Proposed investigation

1. Complete and physically validate IDEA-20261009-001 P1/P2 as the CPU-path baseline.
2. Instrument `source.read()` and `FrameWriter.publish()` separately, including CPU utilization, frame age, dropped publications, and end-to-end camera-to-headset latency.
3. Identify the camera's actual pixel format and whether Jetson GStreamer/NVMM decode or conversion is available without a CPU round trip.
4. Prototype a direct GStreamer/NVMM-to-CUDA/EGL path only if decode or conversion is a measured bottleneck.
5. Compare latency, jitter, CPU load, GPU load, and CloudXR/OpenXR stability against the validated CPU baseline.

## Decision criteria

- Proceed only if profiling identifies CPU decode/conversion or memory copies as a material bottleneck.
- Prefer an end-to-end zero-copy or single-copy design; do not add a GPU upload/download stage around the existing CPU shared-memory contract.
- Do not weaken camera freshness checks, controller tracking checks, or any robot safety validation.

## Current evidence and interpretation

- **Evidence:** the current `FrameWriter.publish` interface consumes CPU NumPy pixel arrays.
- **Interpretation:** GPU use alone will not fix a V4L2 queue backlog and may increase contention if frames return to CPU memory before publication.
- No implementation, benchmark, headset test, or physical robot test has been performed for this idea.

## Next action

Defer implementation. Revisit after P1/P2 baseline measurements and per-stage camera profiling are available.
