# Pivot Mechanism — Design Notes

## Overview

The spring-pivot mechanism allows a dog in a rear wheelchair to sit and lie down naturally without being removed from the chair. The pivot arms are spring-tensioned to return to standing position, and collapse when the dog backs into contact stoppers.

This design is inspired by commercially available sit/lie-down wheelchair mechanisms. Chopper Chair is an independent open-source implementation built from first principles.

---

## States

```
  STANDING (0°)
  ─────────────────────────────────────────────────
  Rail:    ════════════════════════════
  Arm:     ════════╗ (level)
  Wheel:           ○  (floor contact)


  SITTING (~25°)
  ─────────────────────────────────────────────────
  Rail:    ════════════════════════════
  Arm:      ═══╗
               ╲ (~25°)
  Wheel:         ○  (still rolling, rear lowered)


  LYING DOWN (~45°, stoppers engaged)
  ─────────────────────────────────────────────────
  Rail:    ════════════════════════════
  Arm:      ═╗
              ╲╲ (~45°)
  Wheel:        ○  (off ground or grazing)
  Rear:             ▓▓▓ (dog's rear rests on ground)
  Stoppers:   ▌ (rail-mounted, hold arm at angle)


  STANDING UP
  ─────────────────────────────────────────────────
  Springs return arms from ~45° → 0° as dog pushes
  forward off the stoppers. Return time: ~1 second.
```

| State | Pivot angle | What happens |
|-------|-------------|---------------|
| Standing | 0° | Springs hold arms level, wheels flat on ground |
| Sitting | ~25° | Dog shifts weight back, rear lowers naturally |
| Lying down | ~45° | Dog backs into stoppers, arms collapse to floor |
| Standing up | 0° | Springs return arms to level as dog pushes forward |

---

## Key Components

### Pivot Arms (`PivotArm_Left` / `PivotArm_Right`)
- Hinged at the rear rail junction via the 10mm stainless axle rod
- Spring-tensioned at the Spring Boss post
- Wheel assembly (axle caps + wheels) mounted at the outboard end
- **Print orientation:** 45° on the bed — layer lines run perpendicular to the hinge bore for maximum fatigue resistance

### Spring Boss (`SpringBoss_Left` / `SpringBoss_Right`)
- 18mm OD cylindrical post on top of each pivot arm
- Torsion spring seats over the boss; press-fit (no glue — must be swappable)
- Spring torque should be approximately 50–60% of the dog's estimated rear body weight
- Too stiff = dog can't initiate a sit. Too loose = arms sag under the dog's standing weight.

### Contact Stoppers (`Stopper_Left` / `Stopper_Right`)
- Snap into slots at the rear-most point of each side rail
- When the dog backs into them, contact force overcomes spring tension
- Arms collapse to the configured `collapse_angle` and hold there
- Line with 2mm craft foam or neoprene strip to absorb impact and reduce noise

---

## Spring Selection by Dog Weight

| Dog Weight | Recommended Spring Rate | Typical Collapse Angle |
|------------|------------------------|------------------------|
| Under 10 lbs | 1.0 lb/in | 40° |
| 10–20 lbs | 1.5 lb/in | 45° (default) |
| 20–35 lbs | 2.5 lb/in | 50° |
| Over 35 lbs | 3.5 lb/in | 55° |

**Sourcing:** Search **"torsion spring 10mm ID"** on Amazon. Buy a 2-pack. The spring rate is printed on the packaging. Century Spring Corp and Smalley are reliable brands; avoid unmarked packs that don't list rate.

**Tuning after assembly:**  
- Arms sag or don't return → go up one rate  
- Dog strains to sit or arms never collapse fully → go down one rate  
- Spring rate is the primary tuning lever — adjust this before reprinting anything

---

## Pivot Point Geometry

The axle is located at approximately 60% of rail length measured from the front. This ratio ensures:
- The wheel arc doesn't lift the dog uncomfortably when sitting
- The rear of the chair drops far enough to contact the ground at full collapse
- The spring return force is mechanically advantaged for standing (shorter moment arm on the spring side)

Do not move the axle position without recalculating the arm geometry. The 60% ratio is baked into the parametric model — changing `torso_length` adjusts it proportionally.

---

## Future Improvements

- **Dampener channel:** A slot in the stopper for a small silicone bumper would replace foam padding with a proper dashpot effect for larger dogs
- **Angle-adjust:** A set of notched stopper positions (40°/45°/50°/55°) would allow angle tuning without reprinting stoppers
- **M4 set-screw bores in axle caps:** Currently require manual drilling or post-process — parametric bore placement is a planned improvement
