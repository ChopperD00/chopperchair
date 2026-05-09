# Chopper Chair APEX — Ultra Deluxe Tier

> *Because Chopper deserves a mech suit.*

APEX is the fully motorized, SBC-powered, IMU-aware tier of Chopper Chair. Where Build 2 uses passive torsion springs, APEX uses brushless hub motors. Where Build 2 fits a dog, APEX fits a dog *and* knows what it's doing.

The architecture is directly inspired by the [Diablo wheeled-leg robot](https://shop.directdrive.com/products/diablo-world-s-first-direct-drive-self-balancing-wheeled-leg-robot) (open SDK, six direct-drive motors, Raspberry Pi onboard, four-bar linkage legs) and the [Ascento ETH Zürich jumping robot](https://www.ascento.ethz.ch/) (topology-optimized legs, spring-in-knee energy storage, decoupled stabilization). APEX miniaturizes that architecture for a dog-scale application.

---

## What changes vs Build 2

| Feature | Build 2 — Hybrid | APEX |
|---------|-----------------|------|
| Pivot actuation | Passive torsion springs | Brushless hub motors |
| Sit/lie control | Dog backs into stoppers | IMU-detected posture, motor-controlled |
| Electronics | None | SBC + IMU + motor controllers + BLE |
| Adjustability | Reprint rails to change geometry | App/BLE real-time tuning |
| Ground clearance | Fixed at print time | Actively adjustable |
| Aesthetic | Functional | Ascento-inspired topology-optimized panels |
| Cost | ~$55 hardware | ~$280–420 hardware (see BOM) |
| Skill level | Any maker | Comfortable with electronics + Python |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    APEX SPINE POD                       │
│  ┌──────────────┐  ┌──────────┐  ┌───────────────────┐ │
│  │ Raspberry Pi │  │ MPU-6050 │  │  BLE / WiFi       │ │
│  │ Zero 2W / CM4│  │   IMU    │  │  (app control)    │ │
│  └──────┬───────┘  └────┬─────┘  └───────────────────┘ │
│         │               │                               │
│  ┌──────▼───────────────▼───────────────────────────┐  │
│  │              Motor Control Layer                  │  │
│  │         ODrive Mini  ×2  (CAN bus)               │  │
│  └──────┬────────────────────────────┬──────────────┘  │
└─────────┼────────────────────────────┼─────────────────┘
          │                            │
   ┌──────▼──────┐              ┌──────▼──────┐
   │ Hub Motor L │              │ Hub Motor R │
   │ T-Motor MN  │              │ T-Motor MN  │
   │ (pivot arm) │              │ (pivot arm) │
   └─────────────┘              └─────────────┘
          │                            │
   ┌──────▼──────┐              ┌──────▼──────┐
   │  Wheel L    │              │  Wheel R    │
   │ (passive,   │              │ (passive,   │
   │  free spin) │              │  free spin) │
   └─────────────┘              └─────────────┘

Optional:
  ├── RGB LED ring × 2 (wheel hubs, NeoPixel)
  ├── Pi Camera Module 3 (dog's-eye view)
  └── LiPo 3S 2200mAh (spine pod, 2–3h runtime)
```

---

## Control Modes

Mirroring Diablo's standing/crouching/creeping modes, APEX has three states:

| Mode | Pivot angle | Use case |
|------|------------|----------|
| **STAND** | 0° | Normal walking, forward motion |
| **SIT** | ~25° | Dog initiates sit, motors assist smoothly |
| **REST** | ~45° | Full floor contact, motors hold position |

The IMU (MPU-6050) reads chassis tilt. When tilt exceeds the sit threshold (~15°), the motor controller smoothly drives the pivot arms to the SIT angle. When the dog stands and pushes forward, motors return to STAND. No stoppers needed — the motors ARE the stoppers.

### Posture Detection (Gemma 4 integration)

The Gemma 4 pipeline doesn't stop at measurement. APEX adds a second inference pass:

```
Pi Camera → Gemma 4 E2B (edge, runs on Pi Zero 2W)
         → posture classification: STAND / SIT / REST / DISTRESS
         → motor controller command
```

This closes the full loop: the dog's posture is *seen* by the AI, interpreted, and the chair *responds*. Not just a passive frame — an active assist system.

---

## Hardware BOM

### SBC (pick one)

| Option | Part | Why | Cost |
|--------|------|-----|------|
| Good | Raspberry Pi Zero 2W | Lightest, cheapest, runs Gemma E2B via Ollama | ~$15 |
| Better | Raspberry Pi CM4 (2GB) | More RAM for vision pipeline, PCIe for NVMe | ~$40 |
| Best | NVIDIA Jetson Orin Nano (8GB) | 1024 CUDA cores, runs E4B locally at speed | ~$250 |

*For the article demo: Pi Zero 2W is sufficient. Jetson Orin Nano is the sovereign APEX vision node.*

### Motors (pivot arm actuation)

| Option | Part | Why | Cost |
|--------|------|-----|------|
| Good | T-Motor MN1005 KV90 | Lightweight, adequate torque for <20lb dogs | ~$45 ×2 |
| Better | T-Motor MN3510 KV360 | Higher torque, suits 20–40lb dogs | ~$65 ×2 |
| Best | Cubemars AK10-9 | Quasi-direct-drive, built-in position control, Diablo-grade | ~$180 ×2 |

### Motor Controllers

| Option | Part | Why | Cost |
|--------|------|-----|------|
| Good | VESC 4.12 (×2) | Open source, well-documented, huge community | ~$35 ×2 |
| Better | ODrive Mini (×2) | CAN bus native, cleaner integration with Pi | ~$65 ×2 |
| Best | Moteus r4.11 (×2) | Field-oriented control, mjbots ecosystem, Python SDK | ~$110 ×2 |

### IMU

| Option | Part | Cost |
|--------|------|------|
| Good | MPU-6050 breakout | ~$4 |
| Better | ICM-42688-P | ~$12 |
| Best | VectorNav VN-100 | ~$400 (overkill, but Ascento-grade) |

*Use the MPU-6050 for v1. It's what Arduino tutorials run on and perfectly adequate for posture detection.*

### Power

| Part | Spec | Cost |
|------|------|------|
| LiPo battery | 3S 2200mAh 30C | ~$18 |
| XT60 connectors | ×4 | ~$5 |
| 5V BEC / regulator | For Pi + logic | ~$8 |
| Power switch | Latching, rated 10A | ~$6 |

### Accessories

| Part | Cost |
|------|------|
| NeoPixel LED ring (16px) ×2 | ~$12 |
| Pi Camera Module 3 | ~$25 |
| M3 brass standoffs (assorted) | ~$8 |
| CAN bus termination resistors | ~$2 |

### Total Hardware Cost

| Build | SBC | Motors | Controllers | IMU | Power | Extras | Total |
|-------|-----|--------|-------------|-----|-------|--------|-------|
| APEX Good | $15 | $90 | $70 | $4 | $37 | $47 | **~$263** |
| APEX Better | $40 | $130 | $130 | $12 | $37 | $47 | **~$396** |
| APEX Best | $250 | $360 | $220 | $12 | $37 | $47 | **~$926** |

---

## Software Stack

```
OS:          Raspberry Pi OS Lite (64-bit)
Runtime:     Python 3.11
Motor SDK:   python-moteus / ODrive Python / VESC Tool
IMU:         smbus2 + MPU6050 library
BLE:         BlueZ + bleak
Vision:      Ollama → gemma4:e2b (posture classification)
Control:     Custom PID loop, 100Hz
Comms:       CAN bus @ 1Mbit/s
```

### Boot sequence
```python
# apex_controller.py (simplified)
1. Init IMU, calibrate zero angle
2. Home motors to STAND position
3. Start BLE advertising
4. Loop:
   a. Read IMU tilt
   b. Every 2s: run Gemma posture classification on Pi Camera frame
   c. Fuse IMU + vision → posture state
   d. Command motors to target angle
   e. Update LED color (green=STAND, amber=SIT, blue=REST)
```

---

## Printed Parts — APEX additions

All Build 2 structural parts carry over. APEX adds:

| Part | Material | Note |
|------|----------|------|
| SpinePod.stl | PETG | Houses SBC + battery + BEC. Mounts to crossbar top. |
| MotorMount_Left.stl | PETG | Replaces SpringBoss — bolts hub motor to pivot arm |
| MotorMount_Right.stl | PETG | Same |
| WheelHub_LED_Left.stl | PETG | Diffuser ring for NeoPixel |
| WheelHub_LED_Right.stl | PETG | Same |
| CameraArm.stl | PETG | Pi Camera forward-facing mount on crossbar front |

Total APEX-only parts: 6 STLs  
Total APEX build: 13 (Build 2 structural) + 6 (APEX) = **19 STLs**

---

## Evolutionary Timeline

```
BUILD 1 ──── BUILD 2 ──── BUILD 3 ──── APEX
Full print    Hybrid       Slick         Mech suit
Passive       Passive      Passive       Active
$0 hardware   $55          $90           $263–926
Any printer   Any printer  Any printer   Any printer + electronics

● ────────────●────────────●──────────────●
Stone tools   Bronze age   Industrial     Cyberpunk
```

---

## What's Next

- [ ] Fusion 360 motor mount geometry (replaces SpringBoss parametric)
- [ ] SpinePod enclosure design with cable routing channels
- [ ] apex_controller.py v0.1 — IMU-only posture detection, no vision
- [ ] apex_controller.py v0.2 — Gemma 4 vision posture fusion
- [ ] BLE companion app (React Native, Inferis-style dark UI)
- [ ] APEX Spline scene for the configurator

Contributions welcome. If you build an APEX, open a PR and document your dog's measurements.
