# ChopperChair — OpenSCAD Source Files

Parametric source for all three printable builds. All driven by shared parameters in `chopperchair_params.scad`.

## Files

| File | Build | Parts |
|---|---|---|
| `chopperchair_params.scad` | All | Shared parameters — injected by `pipeline/bridge.py` |
| `build2_hybrid.scad` | Build 2 | 13 printed parts + ~$55 hardware |
| `build3_slick.scad` | Build 3 | Topology-optimized redesign, drop-in upgrade from Build 2 |
| `build4_apex.scad` | Build 4 | Motorized APEX — motor pockets, SpinePod, NeoPixel hubs |

## Exporting STLs

### Manual (OpenSCAD GUI)
1. Open the `.scad` file
2. Set `part = "part_name"` at the bottom of the file
3. Render (`F6`) → Export STL (`F7`)

### Automated (via pipeline)
```bash
python3 pipeline/measure.py --photo side.jpg --photo rear.jpg
python3 pipeline/bridge.py --measurements measurements.json --build hybrid
```

The bridge script injects your dog's measurements into `chopperchair_params.scad`, then calls OpenSCAD CLI to batch-export all parts.

## Part Selectors per Build

### Build 2 Hybrid
`rail_left` · `rail_right` · `crossbar_front` · `crossbar_rear` · `pivot_arm_left` · `pivot_arm_right` · `spring_boss_left` · `spring_boss_right` · `axle_cap_left` · `axle_cap_right` · `stopper_left` · `stopper_right` · `belly_sling_mount`

### Build 3 Slick
Same parts as Build 2, redesigned geometry. Drop-in compatible.

### Build 4 APEX
`rail_left` · `rail_right` · `crossbar_front` · `crossbar_rear` · `pivot_arm_left` · `pivot_arm_right` · `axle_cap_left` · `axle_cap_right` · `belly_sling_mount` · `spinepod_base` · `spinepod_lid` · `neopixel_hub_cover`

## Print Settings

| Part | Material | Infill | Notes |
|---|---|---|---|
| Rails | PETG | 40% | Gyroid infill |
| Pivot arms | PETG | 50% | Print at 45° orientation |
| Motor mount arms (APEX) | PETG | 60% | Higher infill for motor loads |
| Axle caps | PLA+ | 50% | — |
| Stoppers | TPU 95A | 20% | Flexible contact pad |
| SpinePod | PLA | 25% | Cosmetic tolerances |
| NeoPixel cover | PETG or clear PETG | 15% | Clear PETG diffuses LEDs |
