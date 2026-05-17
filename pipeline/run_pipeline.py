#!/usr/bin/env python3
"""ChopperChair — Gemma 4 three-pass measurement pipeline. Run on ACIDBURN."""
import base64, json, re, io, time, urllib.request
from pathlib import Path
from PIL import Image

OLLAMA = "http://localhost:11434/api/generate"

ANATOMY = (
    "Look at this dog photo. You are a veterinary anatomy specialist.\n"
    "Identify anatomical landmarks and estimate body dimensions in millimeters.\n"
    "Think step by step: identify landmarks, then estimate distances.\n"
    "Use any harness, leash, or hand visible as a scale reference.\n"
    "Return ONLY valid JSON, no markdown, no explanation:\n"
    '{"torso_length_mm":0,"rear_leg_length_mm":0,"hip_width_mm":0,'
    '"ground_clearance_mm":0,"girth_mm":0,"weight_class":"M","confidence":0.5,"notes":""}\n'
    "weight_class: S=under10lbs M=10-35lbs L=35-70lbs XL=over70lbs"
)

GEOMETRY = (
    "Look at this dog photo. You are a photogrammetry expert.\n"
    "Estimate dog body dimensions in millimeters, correcting for camera angle and perspective.\n"
    "Think step by step: assess viewing angle, find scale references, correct foreshortening.\n"
    "Return ONLY valid JSON, no markdown, no explanation:\n"
    '{"torso_length_mm":0,"rear_leg_length_mm":0,"hip_width_mm":0,'
    '"ground_clearance_mm":0,"girth_mm":0,"weight_class":"M","confidence":0.5,"notes":""}\n'
    "weight_class: S=under10lbs M=10-35lbs L=35-70lbs XL=over70lbs"
)


def load_img(path, max_dim=512):
    img = Image.open(path)
    img.thumbnail((max_dim, max_dim))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def query(prompt, img_b64=None, retries=3):
    payload = {
        "model": "gemma4:e4b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 2048},
    }
    if img_b64:
        payload["images"] = [img_b64]
    last_raw = ""
    for attempt in range(retries):
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            OLLAMA, data=data, headers={"Content-Type": "application/json"}
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        raw = resp.get("response", "")
        last_raw = raw
        if not raw.strip():
            print(f"  attempt {attempt+1}: empty response, retrying...", flush=True)
            continue
        cleaned = raw.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        m = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError as e:
                print(f"  attempt {attempt+1}: JSON parse error: {e}", flush=True)
        else:
            print(f"  attempt {attempt+1}: no JSON found in: {repr(raw[:150])}", flush=True)
    raise ValueError(f"Failed after {retries} retries. Last: {repr(last_raw[:200])}")


def merge(a, b):
    ca, cb = a.get("confidence", 0.5), b.get("confidence", 0.5)
    t = ca + cb or 1
    fields = ["torso_length_mm", "rear_leg_length_mm", "hip_width_mm", "ground_clearance_mm", "girth_mm"]
    m = {f: round((a.get(f, 0) * ca + b.get(f, 0) * cb) / t) for f in fields}
    m["weight_class"] = a.get("weight_class", "M")
    m["confidence"] = round((ca + cb) / 2, 2)
    return m


def check(m):
    issues = []
    if m.get("hip_width_mm", 0) > m.get("torso_length_mm", 9999):
        issues.append("hip_width > torso_length")
    if m.get("ground_clearance_mm", 0) > m.get("rear_leg_length_mm", 9999):
        issues.append("ground_clearance > rear_leg_length")
    for k, (lo, hi) in {
        "torso_length_mm": (80, 700),
        "rear_leg_length_mm": (40, 400),
        "hip_width_mm": (40, 300),
        "ground_clearance_mm": (20, 200),
    }.items():
        v = m.get(k, 0)
        if not lo <= v <= hi:
            issues.append(f"{k}={v} out of range [{lo},{hi}]")
    m["_issues"] = issues
    m["_valid"] = len(issues) == 0
    return m


def run_photo(photo):
    print(f"\n=== {photo} ===", flush=True)
    t0 = time.time()
    img = load_img(photo)

    print("ANATOMIST...", flush=True)
    anat = query(ANATOMY, img)
    print(f"  conf={anat.get('confidence',0):.2f}  torso={anat.get('torso_length_mm')}  hip={anat.get('hip_width_mm')}", flush=True)

    print("GEOMETRIST...", flush=True)
    geom = query(GEOMETRY, img)
    print(f"  conf={geom.get('confidence',0):.2f}  torso={geom.get('torso_length_mm')}  hip={geom.get('hip_width_mm')}", flush=True)

    merged = merge(anat, geom)

    val_prompt = (
        "Validate these dog wheelchair measurements. Correct obvious outliers.\n"
        "Return ONLY valid JSON, no markdown:\n"
        '{"torso_length_mm":0,"rear_leg_length_mm":0,"hip_width_mm":0,'
        '"ground_clearance_mm":0,"girth_mm":0,"weight_class":"M",'
        '"confidence":0.0,"validation_passed":true,"issues":[]}\n\n'
        "Input measurements: " + json.dumps(merged)
    )
    print("VALIDATOR...", flush=True)
    try:
        validated = query(val_prompt)
        result = {**merged, **{k: v for k, v in validated.items() if k not in merged}}
    except Exception as e:
        print(f"  VALIDATOR failed: {e} — using merged", flush=True)
        result = merged

    result = check(result)
    result["_time_s"] = round(time.time() - t0, 1)
    result["_photo"] = str(photo)

    out = Path(photo).with_suffix(".measurements.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    photos = [
        "pipeline_inputs/side_01_IMG_2553.jpeg",
        "pipeline_inputs/rear_01_IMG_2755.jpeg",
    ]
    results = [run_photo(p) for p in photos]

    s, r = results
    fields = ["torso_length_mm", "rear_leg_length_mm", "hip_width_mm", "ground_clearance_mm", "girth_mm"]
    final = {f: round((s.get(f, 0) + r.get(f, 0)) / 2) for f in fields}
    final["weight_class"] = s.get("weight_class", "M")
    final["confidence"] = round((s.get("confidence", 0) + r.get("confidence", 0)) / 2, 2)
    final["_method"] = "three_pass_side_rear_average"
    final["_valid"] = s.get("_valid", False) and r.get("_valid", False)
    final["_issues"] = s.get("_issues", []) + r.get("_issues", [])

    with open("pipeline_inputs/measurements_final.json", "w") as f:
        json.dump(final, f, indent=2)

    print("\n=== FINAL AVERAGED MEASUREMENTS ===")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
