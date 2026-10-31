"""Generate Linux config without connecting devices or modifying calibration."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--follower-port", required=True)
p.add_argument("--leader-port", required=True)
p.add_argument("--high-camera", type=int, required=True)
p.add_argument("--gripper-camera", type=int, required=True)
p.add_argument("--fps", type=int, choices=[10, 30], default=10)
a = p.parse_args()
root = Path(__file__).resolve().parent
cfg = json.loads((root / "record-template.json").read_text())
for role, kind, port in [("robot", "follower", a.follower_port), ("teleop", "leader", a.leader_port)]:
    cfg[role]["port"] = port
    cfg[role]["calibration_dir"] = str(root / "calibration" / kind)
for key, index in [("camera_0", a.high_camera), ("camera_1", a.gripper_camera)]:
    cfg["robot"]["cameras"][key]["index_or_path"] = index
cfg["dataset"]["fps"] = a.fps
cfg["dataset"]["root"] = str(root / "recordings" / "unused_launcher_overrides")
cfg["catch_up_warning"]["telemetry_path"] = str(root / "outputs" / "unused_launcher_overrides.jsonl")
path = root / "record-linux.json"
if path.exists():
    raise SystemExit("record-linux.json already exists; preserve/rename it before generating a replacement")
path.write_text(json.dumps(cfg, indent=2) + "\n")
print(path)
