# Pivot Mechanism — Design Notes

## Overview

The spring-pivot mechanism allows a dog in a rear wheelchair to sit and lie down naturally without being removed from the chair. The pivot arms are spring-tensioned to return to standing position, and collapse when the dog backs into contact stoppers.

This design is inspired by commercially available sit/lie-down wheelchair mechanisms. Chopper Chair is an independent open-source implementation built from first principles.

---

## States

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
- Wheel assembly (axle caps + wheels) mounted at the front end of each arm
- Print at 45° orientation for maximum layer-direction strength at the hinge bore

### Spring Boss (`SpringBoss_Left` / `SpringBoss_Right`)
- 18mm OD cylindrical post on top of each pivot arm
- Torsion spring seats over the boss
- Spring torque should be approximately 50–60% of the dog's rear body weight
- Too stiff = dog can't sit. Too loose = chair collapses under dog's weight.

### Contact Stoppers (`Stopper_Left` / `Stopper_Right`)
- Mounted at the rear-most point of each side rail
- When the dog backs into them, the contact force overcomes spring tension
- Arms collapse to the configured `collapse_angle`
- Line with craft foam or neoprene strip for shock absorption

---

## Spring Selection by Dog Weight

| Dog Weight | Recommended Spring Rate | Collapse Angle |
|------------|------------------------|----------------|
| Under 10 lbs | 1.0 lb/in | 40° |
| 10–20 lbs | 1.5 lb/in | 45° |
| 20–35 lbs | 2.5 lb/in | 50° |
| Over 35 lbs | 3.5 lb/in | 55° |

Search: **torsion spring 10mm ID** on Amazon. Buy a 2-pack. The rate is printed on the packaging.

---

## Pivot Point Geometry

The axle is located at ~60% of rail length from the front. This ratio ensures:
- The wheel arc doesn't lift the dog uncomfortably when sitting
- The rear of the chair stays low enough to contact the ground at full collapse
- The spring return force is mechanically advantaged for standing

Do not move the axle position without recalculating the arm geometry.
