#!/usr/bin/env python3
"""
ChopperChair — Parametric STL Generator
Reads measurements.json, drives Fusion 360 via MCP file bridge, exports STLs.

Usage:
  python3 generate.py --measurements measurements.json --build hybrid
"""

import argparse, json, sys, time
from pathlib import Path

BODIES = {
    "fullprint": [
        "Rail_Left","Rail_Right","Crossbar_Front","Crossbar_Rear",
        "PivotArm_Left","PivotArm_Right","SpringBoss_Left","SpringBoss_Right",
        "AxleCap_Left","AxleCap_Right","Wheel_Left","Wheel_Right",
        "BellySling_Mount","Stopper_Left","Stopper_Right"
    ],
    "hybrid": [
        "Rail_Left","Rail_Right","Crossbar_Front","Crossbar_Rear",
        "PivotArm_Left","PivotArm_Right","SpringBoss_Left","SpringBoss_Right",
        "AxleCap_Left","AxleCap_Right","BellySling_Mount","Stopper_Left","Stopper_Right"
    ],
}

def run(params, build, output_dir):
    cmd_file = Path.home() / "Documents" / "fusion_command.txt"
    resp_file = Path.home() / "Documents" / "fusion_response.txt"
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    commands = []
    for name, value in params.items():
        commands.append({"tool_name": "set_user_parameter",
                         "arguments": {"name": name, "value": float(value), "units": "mm"}})
    for body in BODIES.get(build, BODIES["hybrid"]):
        commands.append({"tool_name": "export_stl",
                         "arguments": {"file_path": str(out/f"{body}.stl"),
                                       "body_name": body, "refinement": "high"}})

    cmd_file.write_text(json.dumps({"tool_name": "execute_macro",
                                    "arguments": {"commands": commands}}))
    print("  Waiting for Fusion 360...")
    for _ in range(60):
        time.sleep(1)
        if resp_file.exists():
            resp = json.loads(resp_file.read_text())
            resp_file.unlink()
            return resp
    raise TimeoutError("Fusion 360 timeout — is fusion_mcp_server add-in running?")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--measurements", required=True)
    parser.add_argument("--build", default="hybrid", choices=["fullprint","hybrid"])
    parser.add_argument("--output", default="./output_stl")
    args = parser.parse_args()

    data = json.loads(Path(args.measurements).read_text())
    params = data["params"]
    print(f"ChopperChair — STL Generator | build={args.build} | torso={params['torso_length']}mm")
    try:
        run(params, args.build, args.output)
        print(f"\n✓ STLs in {args.output}/")
    except Exception as e:
        print(f"\n✗ {e}"); sys.exit(1)

if __name__ == "__main__":
    main()
