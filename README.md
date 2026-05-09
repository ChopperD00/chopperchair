# 🦽 Chopper Chair

**AI-powered 3D-printable dog wheelchair with a spring-pivot sit/lie-down mechanism.**  
Gemma 4 vision pipeline measures your dog from photos and auto-generates a custom-fit frame.

> *In memory of Chopper — the good boy this was built for.*

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![DEV.to Gemma 4 Challenge](https://img.shields.io/badge/DEV.to-Gemma%204%20Challenge-7c6af7)](https://dev.to)

---

## What makes this different

Every dog wheelchair on the market locks you into fixed size tiers. Chopper Chair generates a **fully custom frame** from a photo of your dog — no measuring tape, no vet visit, no guessing.

The **spring-pivot mechanism** lets the dog sit and lie down naturally while in the chair. Spring-tensioned pivot arms collapse when the dog backs into contact stoppers, and return to standing position automatically. This is the feature that most open-source designs skip entirely.

---

## AI Fitting Pipeline (Gemma 4)

```
Photo of dog (side + rear)
       ↓
Gemma 4 Vision (E4B — runs locally via Ollama)
       ↓
measurements.json
  torso_length, hip_width, rear_leg_length,
  girth, ground_clearance, weight_class
       ↓
Python bridge → Fusion 360 params → STL export
       ↓
Slice → Print → Fit
```

```bash
# Pull Gemma 4 E4B
ollama pull gemma4:e4b

# Measure your dog from photos
python3 pipeline/measure.py --photo side.jpg --photo rear.jpg

# Generate STLs
python3 pipeline/generate.py --measurements measurements.json --build hybrid
```

---

## Builds

### Build 1 — Full Print (zero purchased parts)
15 STLs. Wheels included. TPU required for wheels + stoppers.

### Build 2 — Hybrid (recommended)
13 STLs + ~$55 in hardware (foam wheels, stainless rod, torsion springs, neoprene sling).  
No TPU needed. Any printer with 120mm bed works.

---

## How the pivot mechanism works

1. **Standing** — Springs hold pivot arms level, wheels flat on ground
2. **Sitting** — Dog shifts weight back, arms pivot ~25°, rear lowers naturally
3. **Lying down** — Dog backs into contact stoppers, arms collapse to ~45°, full floor contact
4. **Standing up** — Springs counterbalance rear body weight, arms return to level

See [`docs/pivot-mechanism.md`](docs/pivot-mechanism.md) for full design notes and spring selection.

---

## Parametric Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `torso_length` | 160mm | Shoulder to hip |
| `hip_width` | 90mm | Hip width |
| `rear_leg_length` | 80mm | Floor to hip |
| `girth` | 165mm | Belly circumference |
| `ground_clearance` | 45mm | Chassis height |
| `wheel_diameter` | 100mm | Wheel OD |
| `collapse_angle` | 45° | Pivot arm collapse angle |

---

## Repo Structure

```
chopperchair/
├── stl/
│   ├── build1_fullprint/    # 15 STLs, zero purchased parts
│   └── build2_hybrid/       # 13 STLs + hardware BOM
├── pipeline/
│   ├── measure.py           # Gemma 4 vision measurement
│   ├── generate.py          # Params → STL export
│   └── models.py            # Ollama node routing
├── docs/
│   ├── assembly.md          # Step-by-step build instructions
│   └── pivot-mechanism.md   # Pivot mechanism design notes
├── web/
│   └── index.html           # Parametric maker UI
└── README.md
```

---

## License

[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — Build it, modify it, share it. Keep the attribution. For Chopper.
