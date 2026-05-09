#!/usr/bin/env python3
"""
ChopperChair — Gemma 4 Vision Measurement Pipeline
Extracts dog dimensions from photos using local Gemma 4 E4B via Ollama.

Usage:
  python3 measure.py --photo side.jpg --photo rear.jpg
  python3 measure.py --photo side.jpg --output measurements.json
"""

import argparse
import base64
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

OLLAMA_HOST = "http://100.69.29.1:11434"  # ACIDBURN via Tailscale
MODEL = "gemma4:e4b"

MEASUREMENT_PROMPT = """
You are a precise veterinary measurement assistant.
Analyze this dog photo and extract wheelchair fitting measurements.

For a SIDE VIEW photo, estimate:
- torso_length_mm: distance from shoulder joint to hip joint
- rear_leg_length_mm: distance from hip joint to ground
- ground_clearance_mm: suggested chassis clearance (usually 40-60% of rear leg length)

For a REAR VIEW photo, estimate:
- hip_width_mm: distance between hip joints
- shoulder_width_mm: distance between shoulder joints
- girth_mm: estimated belly circumference at widest point

If you cannot determine a measurement with confidence, use null.
Respond ONLY with valid JSON. No explanation, no markdown.

Example:
{
  "torso_length_mm": 165,
  "rear_leg_length_mm": 82,
  "ground_clearance_mm": 45,
  "hip_width_mm": 88,
  "shoulder_width_mm": 76,
  "girth_mm": 170,
  "confidence": 0.82,
  "notes": "Small breed, good joint visibility"
}
"""

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def measure_from_photo(photo_path, host=OLLAMA_HOST, model=MODEL):
    img_b64 = encode_image(photo_path)
    payload = {
        "model": model,
        "prompt": MEASUREMENT_PROMPT,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 512}
    }
    resp = requests.post(f"{host}/api/generate", json=payload, timeout=60)
    resp.raise_for_status()
    text = resp.json()["response"].strip()
    if text.startswith("```"):
        text = "\n".join(text.split("\n")[1:-1])
    return json.loads(text)

def merge_measurements(*dicts):
    merged = {}
    for d in dicts:
        for k, v in d.items():
            if v is not None and k not in merged:
                merged[k] = v
    return merged

def measurements_to_params(m):
    return {
        "torso_length": m.get("torso_length_mm", 160),
        "hip_width": m.get("hip_width_mm", 90),
        "shoulder_width": m.get("shoulder_width_mm", 80),
        "rear_leg_length": m.get("rear_leg_length_mm", 80),
        "ground_clearance": m.get("ground_clearance_mm", 45),
        "girth": m.get("girth_mm", 165),
        "wheel_diameter": 100,
        "axle_diameter": 10,
        "collapse_angle": 45,
        "sit_angle": 25,
        "spring_boss_od": 18,
        "stopper_width": 22,
        "wall_thickness": 4,
        "rail_width": 16,
        "rail_height": 20,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--photo", action="append", required=True)
    parser.add_argument("--output", default="measurements.json")
    parser.add_argument("--ollama", default=OLLAMA_HOST)
    parser.add_argument("--model", default=MODEL)
    args = parser.parse_args()

    print(f"ChopperChair — Gemma 4 Measurement Pipeline")
    print(f"Model: {args.model} @ {args.ollama}")

    raw = []
    for photo in args.photo:
        try:
            m = measure_from_photo(photo, args.ollama, args.model)
            print(f"  ✓ {photo}")
            raw.append(m)
        except Exception as e:
            print(f"  ✗ {photo}: {e}")

    if not raw:
        print("No measurements. Check photos and Ollama.")
        sys.exit(1)

    merged = merge_measurements(*raw)
    params = measurements_to_params(merged)
    output = {
        "generated_at": datetime.now().isoformat(),
        "model": args.model,
        "photos": args.photo,
        "raw_measurements": merged,
        "params": params,
    }
    Path(args.output).write_text(json.dumps(output, indent=2))
    print(f"\n✓ Saved to {args.output}")
    print(f"Next: python3 pipeline/generate.py --measurements {args.output}")

if __name__ == "__main__":
    main()
