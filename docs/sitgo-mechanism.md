# SitGo Mechanism — Design Notes

## Overview

The SitGo mechanism allows a dog in a rear wheelchair to sit and lie down naturally.
No other open-source dog wheelchair design has this capability.

## States

1. **Standing** — Springs hold pivot arms level, wheels at ground
2. **Sitting** — Dog shifts weight back, arms pivot ~25°, rear lowers naturally  
3. **Lying down** — Dog backs into rubber stoppers, arms collapse to ~45°, full floor contact
4. **Standing up** — Springs counterbalance rear body weight, arms return to level

## Key Components

### Pivot Arms
- Hinged at rear rail junction via 10mm stainless axle rod
- Spring-tensioned at SpringBoss post
- Wheel assembly mounted at front end

### Spring Boss
- 18mm OD post on pivot arm
- Torsion spring seats over boss
- Spring torque ≈ 50-60% of dog's rear body weight

### Rubber Stoppers
- Mounted at rear-most point of each rail
- Contact force overcomes spring tension → arms collapse
- TPU 95A or craft foam lined for shock absorption

## Spring Rate by Dog Weight

| Dog Weight | Spring Rate | Collapse Angle |
|------------|-------------|----------------|
| < 10 lbs | 1.0 lb/in | 40° |
| 10-20 lbs | 1.5 lb/in | 45° (default) |
| 20-35 lbs | 2.5 lb/in | 50° |
| > 35 lbs | 3.5 lb/in | 55° |

## Assembly Order

1. Thread axle rod through PivotArm_Left → Crossbar_Rear bore → PivotArm_Right
2. Seat torsion springs over SpringBoss posts
3. Attach AxleCaps, tighten M4 set screws
4. Mount wheels on axle rod outboard of caps
5. Test collapse: push stoppers manually, arms should drop and spring back
6. Attach belly sling to BellySling_Mount strap slots
