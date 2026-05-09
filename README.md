# 🦽 Chopper Chair

**AI-powered 3D-printable dog wheelchair with a spring-pivot sit/lie-down mechanism.**  
Gemma 4 vision pipeline measures your dog from photos and generates a custom-fit frame in minutes.

> *In memory of Chopper — the good boy this was built for.*

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![DEV.to Gemma 4 Challenge](https://img.shields.io/badge/DEV.to-Gemma%204%20Challenge-7c6af7)](https://dev.to)

---

## What makes this different

Every dog wheelchair on the market locks you into fixed size tiers. Chopper Chair generates a **fully custom frame** from a photo of your dog — no measuring tape, no vet visit, no guessing.

The **spring-pivot mechanism** lets the dog sit and lie down naturally while in the chair. Spring-tensioned pivot arms collapse when the dog backs into contact stoppers and return to standing position automatically. This is the feature most open-source designs skip entirely.

---

## AI Fitting Pipeline (Gemma 4)

Gemma 4's vision model reads the dog's silhouette from side and rear photos to extract skeletal measurements. It outputs a structured JSON that drives the parametric model directly — no manual input needed.

```
Photo of dog (side + rear)
       ↓
Gemma 4 Vision E4B — runs locally via Ollama
       ↓
measurements.json
  torso_length, hip_width, rear_leg_length,
  girth, ground_clearance, weight_class
       ↓
Python bridge → Fusion 360 parametric model → STL export
       ↓
Slice → Print → Fit
```

```bash
# Pull Gemma 4 E4B (runs locally, no API key needed)
ollama pull gemma4:e4b

# Measure your dog from photos
python3 pipeline/measure.py --photo side.jpg --photo rear.jpg

# Generate STLs for your build
python3 pipeline/generate.py --measurements measurements.json --build hybrid
```

---

## Builds

### Build 1 — Full Print
15 STLs. Wheels and stoppers are printed. TPU required for wheel tires and stopper pads.  
Good if you have a multi-material printer or don't mind ordering TPU filament.

### Build 2 — Hybrid (recommended for most makers)
13 STLs + ~$55 in hardware. Foam-fill wheels and stainless axle are purchased.  
No TPU. Any printer with a 120mm × 120mm bed works. Better durability on the rolling parts.

---

## Hardware BOM — Build 2

| Part | Spec | Search term | Est. cost |
|------|------|-------------|----------|
| Foam-fill wheels × 2 | 100mm OD, 10mm bore | "10mm bore wheelchair wheel 100mm" | ~$14 |
| Stainless axle rod | 10mm OD × 300mm | "10mm stainless steel rod 300mm" | ~$8 |
| Torsion springs × 2 | 10mm ID, rate matched to dog weight* | "torsion spring 10mm ID" | ~$8 |
| Neoprene belly sling | Adjustable, small-dog size | "dog wheelchair belly sling adjustable" | ~$16 |
| M4 × 20mm socket bolts × 2 | For axle cap set screws | M4 × 20mm socket head | ~$5 |
| Craft foam strip (optional) | 2mm, any color | For stopper padding | ~$2 |

**Total: ~$53–$55**

*Spring rate by dog weight: under 10 lbs → 1.0 lb/in · 10–20 lbs → 1.5 lb/in · 20–35 lbs → 2.5 lb/in · over 35 lbs → 3.5 lb/in. See [`docs/pivot-mechanism.md`](docs/pivot-mechanism.md) for the full table.*

---

## Print Settings

All parts are designed for standard FDM. No supports needed on any part.

| Material | Use for | Notes |
|----------|---------|-------|
| PLA | All structural parts | Fine indoors. Avoid leaving in hot cars. |
| PETG | Rails + crossbars | Better impact resistance, good for active dogs |
| ASA | Rails + crossbars | Best UV/outdoor resistance |
| TPU 95A | Wheels + stoppers (Build 1 only) | Flexible, shock-absorbing |

| Part group | Layer height | Infill | Walls |
|------------|-------------|--------|-------|
| Rails, crossbars | 0.2mm | 40% gyroid | 4 |
| Pivot arms | 0.2mm | 50% gyroid | 4 |
| Spring bosses, axle caps | 0.2mm | 60% gyroid | 5 |
| Belly sling mount | 0.2mm | 30% gyroid | 3 |
| Stoppers | 0.2mm | 60% gyroid | 5 |

Print pivot arms at 45° on the bed — this aligns layer lines perpendicular to the hinge bore, the highest-stress axis.

---

## How the pivot mechanism works

```
Standing:    Arms level ──────── wheels flat on ground

Sitting:     Arms pivot ~25°  ╲
                                ╲  dog weight shifts rearward

Lying down:  Arms at ~45°  ╲╲   → rear contacts ground
             (stoppers hold position)

Standing up: Springs return arms to level in ~1 second
```

See [`docs/pivot-mechanism.md`](docs/pivot-mechanism.md) for full design notes, component specs, and spring selection.

---

## Parametric Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `torso_length` | 160mm | Shoulder to hip |
| `hip_width` | 90mm | Hip width at widest point |
| `rear_leg_length` | 80mm | Floor to hip joint |
| `girth` | 165mm | Belly circumference |
| `ground_clearance` | 45mm | Chassis height off ground |
| `wheel_diameter` | 100mm | Wheel OD |
| `collapse_angle` | 45° | Pivot arm full collapse angle |
| `wall_thickness` | 4mm | Structural wall thickness |

All parameters are driven by the Gemma 4 pipeline automatically. You can also set them manually in `pipeline/generate.py` or via the [web configurator](web/index.html).

---

## Repo Structure

```
chopperchair/
├── stl/
│   ├── build1_fullprint/    # 15 STLs — wheels included, TPU required
│   └── build2_hybrid/       # 13 STLs — buy wheels/rod/springs/sling
├── pipeline/
│   ├── measure.py           # Gemma 4 vision measurement from photos
│   ├── generate.py          # measurements.json → Fusion 360 → STL export
│   └── models.py            # Ollama node routing (local inference)
├── docs/
│   ├── assembly.md          # Step-by-step build instructions
│   └── pivot-mechanism.md   # Pivot mechanism design notes + spring table
├── web/
│   └── index.html           # Parametric maker UI (sliders + 3D preview)
└── README.md
```

---

## License

[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — Build it, modify it, share it with attribution. For Chopper.
