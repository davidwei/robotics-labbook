# Commit publication audit — 2026-11-19

Scope: commit-shaped references in `sessions/`, `ideas/`, `experiments/`,
`projects/`, and `docs/` at labbook revision
`24c2a1e33ac22956d9f365cb87429d52d5f11ac6`. Artifact SHA-256 values and
non-Git model/package revisions were excluded. Historical statements such as
"local" and "not pushed" were preserved because they describe state at the
time of the recorded session.

Verification used clean remote-only clones or exact GitHub branch refs. A
commit counts as published only when the exact object is reachable from a
remote branch tip.

## Published by this audit

The four-commit SONIC chain cited by the October 29–November 3 G1 records is now
reachable from
`MoissanClub/GR00T-WholeBodyControl:archive/labbook-g1-sonic-20261030`:

- `dc86407cb94e3b335671677ece90b6fdae401471`
- `632b6b71f974a3a9fe24eb920c210084bda44989`
- `8d916d4384864aa3417bbe4eaa1944bfe4793c20`
- `20105809c6339ea1215542615e146f975c94081c` (remote branch head)

This is an archival publication of the exact recorded history, not an upstream
merge or a claim that the experimental control changes are generally ready.

## Already published

- The G1 XRoboToolkit plugin implementation branches are published in
  `MoissanClub/lerobot_teleoperator_g1_vr`, including Commit 12
  `0d68a65848011550393ef136b2dfe187c2ec37a6` and follow-up fix
  `5017cc3cf521b32ca01b4f7b9abb2fe20de0c473`.
- `MoissanClub/unitree_g1_lerobot:feat/g1-29-vr-lab-scripts` at
  `df545c3e4db529803a5c300a8b4a77f39c1ef164` contains the cited integration
  commits from `02d79ef` through `dcdc0d1`, `cb57454`, `21fe96f`, `77120ad`,
  `7d5c888`, and `c7912d1`.
- The cited SO-101 history is remotely reachable from
  `MoissanClub/lerobot:lab/so101-intel-warning-20261023` or
  `lab/so101-venue-voice-20261031`, including `3cb506d`, `7197d0c`, `a08f19c`,
  `bd49580`, `45531de`, `6107246`, `cae94f7`, and `546d61b`. See the
  follow-up below for the October 24 commits.
- G1 handover revision `ca04051f570e4df1fa1d49f84ce39fd623ecbc2f`
  is reachable through `MoissanClub/lerobot:archive/g1-vr-physical-failure`.
  The earlier G1 revisions explicitly described as pushed are likewise
  reachable from their recorded remote branches.
- The reviewed `xr_teleoperate` revision
  `278a3dcc669eb54b0fd5ed26031e420bc7f42e88` is reachable from
  `davidwei/xr_teleoperate:fix/controller-damping-shortcut`.

## SO-101 publication follow-up

Both exact commits were recovered from the original macOS experiment checkout
and published on `MoissanClub/lerobot:lab/so101-monitor-report-only-20261024`:

- `c5ce05ec2e649132f5546631f108b02fa7d23c37` — report-only motor monitor;
- `c779a6c23cdc00694fe99243d874f60a916c193a` — 15-degree rotary pickup-exit tolerance.

The verified remote branch tip is `c779a6c23cdc00694fe99243d874f60a916c193a`,
whose parent is `c5ce05ec2e649132f5546631f108b02fa7d23c37`.

## Superseded historical reference

The October 8 timeline also names superseded abbreviated merge tip `a734e000`.
It was replaced by `bdd78d348cdbd4d0147c3b685f7131fabba25e09`, is not recorded as
execution provenance, and is absent from current local and remote object sets.
Recovering and archiving that exact historical object would require the original
reflog or another checkout that retained it.
