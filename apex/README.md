# ChopperChair APEX — Motorized Build

## Hardware

| Part | Spec | Source |
|---|---|---|
| Raspberry Pi 5 | 4GB or 8GB | Pi5 (PITRON) |
| Pi Camera Module 3 | Autofocus, native Pi5 | Raspberry Pi |
| ODrive Mini × 2 | CAN bus motor controller | odriverobotics.com |
| T-Motor MN1005 × 2 | 100KV hub motor, ~80mm OD | tmotor.com |
| MPU-6050 IMU | I2C, GY-521 breakout | Amazon |
| NeoPixel Ring 16-LED × 2 | 44mm, WS2812B | Adafruit #1463 |
| SN65HVD230 CAN transceiver | 3.3V, Pi5 native | Amazon |
| 3S LiPo 2200mAh 35C | 11.1V | OVONIC (Amazon) |
| M3 hardware assortment | bolts + nuts | Amazon |

## Wiring

```
Pi5 GPIO18 ─────────────→ NeoPixel ring DATA (both rings in series)
Pi5 SPI0 (MOSI/SCK/CS) → SN65HVD230 → CAN H/L bus
CAN bus ─────────────→ ODrive Mini Left  (node_id=0)
                       → ODrive Mini Right (node_id=1)
ODrive Mini Left  → T-Motor MN1005 Left
ODrive Mini Right → T-Motor MN1005 Right
LiPo 3S ───────────→ ODrive Mini x2 power (24V max input — 3S = 11.1V nom, ok)
Pi5 USB-C ─────────→ PD power bank or BEC from LiPo (5V/3A min)
```

## ODrive Setup

Before running posture_loop.py, configure each ODrive:

```bash
# Install odrivetool
pip install odrive

# Configure (run for each ODrive, disconnect the other)
odrivetool
>>> odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL
>>> odrv0.axis0.controller.config.input_mode = InputMode.POSITION_FILTER
>>> odrv0.axis0.config.can.node_id = 0   # 1 for right motor
>>> odrv0.save_configuration()
>>> odrv0.reboot()
```

## CAN Setup on Pi5

```bash
# Load CAN modules
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mcp251x  # or gs_usb if using USB-CAN adapter

# Bring up CAN interface at 500kbps (ODrive default)
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can0 txqueuelen 1000

# Make persistent
echo 'allow-hotplug can0\niface can0 inet manual\n  pre-up ip link set can0 up type can bitrate 500000' \
  | sudo tee /etc/network/interfaces.d/can0
```

## Running

```bash
# Install dependencies
pip install picamera2 Pillow requests python-can neopixel RPi.GPIO adafruit-circuitpython-neopixel

# Pull gemma4:e2b on Pi5
ollama pull gemma4:e2b

# Dry run (no hardware needed — tests inference + state machine)
python3 apex/posture_loop.py --dry-run

# Full run
python3 apex/posture_loop.py --interval 2.0

# Run against ACIDBURN if Pi5 Ollama isn’t ready yet
python3 apex/posture_loop.py --ollama http://100.69.29.1:11434
```

## Posture States

| State | Motor Angle | LED Color | Trigger |
|---|---|---|---|
| STAND | 0° | Green | Upright, normal gait |
| SIT | 25° | Amber | Rear down, transitioning |
| REST | 45° | Blue | Lying down |
| DISTRESS | hold | Red (pulse) | 3 consecutive distress frames |
| UNKNOWN | hold | Dim white | Inference failed |
