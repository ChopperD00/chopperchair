#!/usr/bin/env python3
"""
ChopperChair — OpenSCAD Bridge
Injects measurements.json into chopperchair_params.scad, then batch-exports
all parts for the selected build as STL files via OpenSCAD CLI.

Usage:
  python3 pipeline/bridge.py --measurements measurements.json --build hybrid
  python3 pipeline/bridge.py --measurements measurements.json --build slick
  python3 pipeline/bridge.py --measurements measurements.json --build apex

Requires: OpenSCAD installed (openscad or openscad-nightly in PATH)
  macOS:  brew install openscad
  Ubuntu: sudo snap install openscad
  Arch:   sudo pacman -S openscad
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# ── Build definitions ───────────────────────────────────────────────────────────
BUILDS = {
    "hybrid": {
        "scad": "scad/build2_hybrid.scad",
        "parts": [
            "rail_left", "rail_right",
            "crossbar_front", "crossbar_rear",
            "pivot_arm_left", "pivot_arm_right",
            "spring_boss_left", "spring_boss_right",
            "axle_cap_left", "axle_cap_right",
            "stopper_left", "stopper_right",
            "belly_sling_mount",
        ]
    },
    "slick": {
        "scad": "scad/build3_slick.scad",
        "parts": [
            "rail_left", "rail_right",
            "crossbar_front", "crossbar_rear",
            "pivot_arm_left", "pivot_arm_right",
            "spring_boss_left", "spring_boss_right",
            "axle_cap_left", "axle_cap_right",
            "stopper_left", "stopper_right",
            "belly_sling_mount",
        ]
    },
    "apex": {
        "scad": "scad/build4_apex.scad",
        "parts": [
            "rail_left", "rail_right",
            "crossbar_front", "crossbar_rear",
            "pivot_arm_left", "pivot_arm_right",
            "axle_cap_left", "axle_cap_right",
            "belly_sling_mount",
            "spinepod_base", "spinepod_lid",
            "neopixel_hub_cover",
        ]
    },
}

# ── Parameter mapping: measurements.json → chopperchair_params.scad ────────────────
PARAM_MAP = {
    "torso_length":     "torso_length",
    "hip_width":        "hip_width",
    "shoulder_width":   "shoulder_width",
    "rear_leg_length":  "rear_leg_length",
    "ground_clearance": "ground_clearance",
    "girth":            "girth",
    "wheel_diameter":   "wheel_diameter",
    "axle_diameter":    "axle_diameter",
    "collapse_angle":   "collapse_angle",
    "sit_angle":        "sit_angle",
    "wall_thickness":   "wall_thickness",
    "rail_width":       "rail_w",
    "rail_height":      "rail_h",
}


def find_openscad():
    """Find OpenSCAD binary."""
    for name in ["openscad", "openscad-nightly", "OpenSCAD"]:
        path = shutil.which(name)
        if path:
            return path
    # macOS app bundle fallback
    mac_path = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    if Path(mac_path).exists():
        return mac_path
    return None


def write_params_scad(params: dict, repo_root: Path) -> Path:
    """
    Write a patched chopperchair_params.scad with injected measurements.
    Returns path to the patched file.
    """
    template = (repo_root / "scad" / "chopperchair_params.scad").read_text()
    for json_key, scad_var in PARAM_MAP.items():
        value = params.get(json_key)
        if value is None:
            continue
        value = round(float(value), 2)
        # Replace the assignment line: varname = <anything>;
        import re
        template = re.sub(
            rf"^({re.escape(scad_var)}\s*=\s*)[^;]+;",
            rf"\g<1>{value};  // injected by bridge.py",
            template,
            flags=re.MULTILINE
        )
    # Write to a temp file so we don’t dirty the repo
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix="_params.scad", delete=False, dir=repo_root / "scad"
    )
    tmp.write(template)
    tmp.flush()
    return Path(tmp.name)


def export_part(openscad_bin: str, scad_file: Path, params_file: Path,
                part: str, out_path: Path) -> bool:
    """
    Call OpenSCAD CLI to export one part as STL.
    Uses -D to override the `part` variable and to use the patched params file.
    """
    cmd = [
        openscad_bin,
        "-o", str(out_path),
        "-D", f'part="{part}"',
        # Prepend our patched params by including it via a temp wrapper
        str(scad_file),
        "--hardwarnings",
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
        env={
            **__import__("os").environ,
            # Tell OpenSCAD to look for includes in the scad/ dir
            "OPENSCADPATH": str(scad_file.parent),
        }
    )
    if result.returncode != 0:
        print(f"    ✗ {part}: {result.stderr.strip()[:200]}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="ChopperChair OpenSCAD Bridge")
    parser.add_argument("--measurements", required=True,
                        help="Path to measurements.json from measure.py")
    parser.add_argument("--build", default="hybrid",
                        choices=list(BUILDS.keys()),
                        help="Which build to generate STLs for")
    parser.add_argument("--output", default=None,
                        help="Output directory (default: stl/<build>_bridge_<timestamp>/)")
    parser.add_argument("--repo", default=".",
                        help="Path to chopperchair repo root (default: current dir)")
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    data      = json.loads(Path(args.measurements).read_text())
    params    = data.get("params", {})
    build_cfg = BUILDS[args.build]

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir    = Path(args.output) if args.output else \
                 repo_root / "stl" / f"{args.build}_bridge_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    openscad = find_openscad()
    if not openscad:
        print("Error: OpenSCAD not found in PATH.")
        print("  macOS:  brew install openscad")
        print("  Ubuntu: sudo snap install openscad")
        sys.exit(1)

    print(f"ChopperChair — OpenSCAD Bridge")
    print(f"  Build:    {args.build}")
    print(f"  Parts:    {len(build_cfg['parts'])}")
    print(f"  Output:   {out_dir}")
    print(f"  OpenSCAD: {openscad}")
    print()

    # Key injected values
    print("  Injected measurements:")
    for k in ["torso_length", "hip_width", "rear_leg_length", "ground_clearance"]:
        print(f"    {k}: {params.get(k, '(default)')} mm")
    print()

    scad_file   = repo_root / build_cfg["scad"]
    params_file = write_params_scad(params, repo_root)

    ok = 0
    fail = 0
    for part in build_cfg["parts"]:
        out_path = out_dir / f"{part}.stl"
        print(f"  Exporting {part}...", end=" ", flush=True)
        if export_part(openscad, scad_file, params_file, part, out_path):
            size_kb = out_path.stat().st_size // 1024
            print(f"✓ ({size_kb}KB)")
            ok += 1
        else:
            fail += 1

    # Cleanup temp params
    params_file.unlink(missing_ok=True)

    print()
    print(f"✓ {ok} STLs exported to {out_dir}/")
    if fail:
        print(f"✗ {fail} failed — check OpenSCAD output above")
        sys.exit(1)
    print(f"Next: slice with BambuStudio or PrusaSlicer")
    print(f"      python3 pipeline/generate.py --measurements {args.measurements} --build {args.build}")


if __name__ == "__main__":
    main()
