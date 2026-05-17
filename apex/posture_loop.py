#!/usr/bin/env python3
"""
ChopperChair APEX — Posture Loop
Runs on Pi5 (PITRON) with Pi Camera Module 3.

Pipeline:
  Pi Camera → gemma4:e2b (Ollama, local) → STAND/SIT/REST/DISTRESS
  → ODrive Mini x2 (CAN bus) → motor angle
  → NeoPixel ring x2 → status color

Requirements:
  pip install picamera2 requests canopen neopixel RPi.GPIO

ODrive Mini CAN IDs (default):
  Left motor:  node_id=0
  Right motor: node_id=1

Run:
  python3 apex/posture_loop.py
  python3 apex/posture_loop.py --ollama http://localhost:11434  # local Pi5 Ollama
  python3 apex/posture_loop.py --dry-run                        # no hardware, print states only
"""

import argparse
import base64
import io
import json
import logging
import struct
import sys
import time
from datetime import datetime
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [APEX] %(levelname)s %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("apex")

# ── Posture states ─────────────────────────────────────────────────────────────
class Posture(Enum):
    STAND    = "STAND"    # upright, all legs bearing weight — motor angle 0°
    SIT      = "SIT"      # rear down, front up — motor angle 25°
    REST     = "REST"     # lying down — motor angle 45°
    DISTRESS = "DISTRESS" # irregular posture / flag — motor hold + alert
    UNKNOWN  = "UNKNOWN"  # inference failed — hold current state

# Motor angles per posture (degrees — maps to ODrive position turns)
POSTURE_ANGLES = {
    Posture.STAND:    0.0,
    Posture.SIT:      25.0,
    Posture.REST:     45.0,
    Posture.DISTRESS: None,   # hold — do not move
    Posture.UNKNOWN:  None,   # hold
}

# NeoPixel colors per posture (R, G, B)
POSTURE_COLORS = {
    Posture.STAND:    (0,   80,  0),    # green
    Posture.SIT:      (80,  40,  0),    # amber
    Posture.REST:     (0,   0,   80),   # blue
    Posture.DISTRESS: (200, 0,   0),    # red, pulsing
    Posture.UNKNOWN:  (20,  20,  20),   # dim white
}

# ── Gemma 4 inference ───────────────────────────────────────────────────────────
POSTURE_PROMPT = """
You are a posture classifier for a dog wearing a motorized wheelchair.
Classify the dog's posture from this camera frame into exactly one of:
  STAND  — standing upright, rear legs supported, normal assisted gait
  SIT    — rear end lowered, sitting or transitioning to sit
  REST   — lying down, resting, fully reclined
  DISTRESS — abnormal position, struggling, tilted, or asymmetric alarm posture

Respond with ONLY the single word. No explanation. No punctuation.
If the frame is unclear or the dog is not visible, respond: UNKNOWN
"""

def classify_posture(frame_jpeg: bytes, ollama_host: str, model: str = "gemma4:e2b") -> Posture:
    """Send a camera frame to Gemma 4 E2B and return a Posture enum."""
    import requests
    img_b64 = base64.b64encode(frame_jpeg).decode()
    payload = {
        "model": model,
        "prompt": POSTURE_PROMPT,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 8},  # classification only
    }
    try:
        resp = requests.post(
            f"{ollama_host}/api/generate",
            json=payload,
            timeout=15
        )
        resp.raise_for_status()
        raw = resp.json()["response"].strip().upper().split()[0]
        return Posture(raw) if raw in Posture._value2member_map_ else Posture.UNKNOWN
    except Exception as e:
        log.warning(f"Inference error: {e}")
        return Posture.UNKNOWN

# ── Camera ──────────────────────────────────────────────────────────────────────
class Camera:
    def __init__(self, width=640, height=480):
        from picamera2 import Picamera2
        self.cam = Picamera2()
        cfg = self.cam.create_still_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.cam.configure(cfg)
        self.cam.start()
        time.sleep(1.0)  # warm up
        log.info(f"Camera ready ({width}x{height})")

    def capture_jpeg(self, quality=70) -> bytes:
        """Capture a frame and return JPEG bytes."""
        from PIL import Image
        array = self.cam.capture_array()
        img = Image.fromarray(array)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        return buf.getvalue()

    def close(self):
        self.cam.stop()

# ── ODrive Mini (CAN bus) ────────────────────────────────────────────────────────
DEG_PER_TURN = 360.0  # ODrive position is in turns
CAN_INTERFACE = "can0"

def deg_to_turns(deg: float) -> float:
    return deg / DEG_PER_TURN

class ODriveMini:
    """
    Minimal CAN driver for ODrive Mini.
    Uses python-can. Sends Set_Input_Pos (CAN cmd 0x00C).
    Assumes ODrive already configured with position control mode.
    """
    # ODrive CAN command IDs
    CMD_SET_INPUT_POS  = 0x00C
    CMD_SET_AXIS_STATE = 0x007
    AXIS_STATE_CLOSED_LOOP = 8

    def __init__(self, node_id: int, interface: str = CAN_INTERFACE, dry_run=False):
        self.node_id  = node_id
        self.dry_run  = dry_run
        self.position = 0.0  # current target in turns
        if not dry_run:
            import can
            self.bus = can.interface.Bus(
                interface, bustype="socketcan"
            )
            self._set_state(self.AXIS_STATE_CLOSED_LOOP)

    def _send(self, cmd_id: int, data: bytes):
        import can
        arb_id = (self.node_id << 5) | cmd_id
        msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=False)
        self.bus.send(msg)

    def _set_state(self, state: int):
        self._send(self.CMD_SET_AXIS_STATE, struct.pack("<I", state))
        time.sleep(0.1)

    def set_position(self, turns: float, vel_ff: float = 0.5, torque_ff: float = 0.0):
        """Command absolute position in turns."""
        self.position = turns
        if self.dry_run:
            log.debug(f"  [DRY] ODrive node={self.node_id} pos={turns:.4f}t")
            return
        data = struct.pack("<fhh", turns, int(vel_ff * 1000), int(torque_ff * 1000))
        self._send(self.CMD_SET_INPUT_POS, data)

    def hold(self):
        """Hold current position — resend last commanded position."""
        self.set_position(self.position)

    def close(self):
        if not self.dry_run:
            self.bus.shutdown()

# ── NeoPixel ──────────────────────────────────────────────────────────────────────
NEOPIXEL_PIN   = 18   # GPIO18 — Pi5 PWM
NEOPIXEL_COUNT = 16   # 16-LED ring
NEOPIXEL_BRIGHTNESS = 0.25  # 25% — don’t blind the dog

class NeoPixelRings:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        if not dry_run:
            import board, neopixel
            self.pixels = neopixel.NeoPixel(
                board.D18, NEOPIXEL_COUNT,
                brightness=NEOPIXEL_BRIGHTNESS,
                auto_write=False,
                pixel_order=neopixel.GRB
            )

    def set_color(self, rgb: tuple, pulse: bool = False):
        if self.dry_run:
            log.debug(f"  [DRY] NeoPixel color={rgb} pulse={pulse}")
            return
        r, g, b = rgb
        if pulse:
            # Simple brightness pulse (1 cycle, non-blocking)
            for br in [0.1, 0.25, 0.4, 0.25]:
                self.pixels.fill((int(r*br/0.4), int(g*br/0.4), int(b*br/0.4)))
                self.pixels.show()
                time.sleep(0.1)
        else:
            self.pixels.fill((r, g, b))
            self.pixels.show()

    def off(self):
        if not self.dry_run:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()

# ── Main loop ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="ChopperChair APEX Posture Loop")
    parser.add_argument("--ollama", default="http://localhost:11434",
                        help="Ollama host (default: localhost — Pi5 local)")
    parser.add_argument("--model", default="gemma4:e2b")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Seconds between frames (default: 2.0)")
    parser.add_argument("--dry-run", action="store_true",
                        help="No hardware — print states only")
    parser.add_argument("--can", default=CAN_INTERFACE,
                        help="CAN interface name (default: can0)")
    args = parser.parse_args()

    log.info("ChopperChair APEX — Posture Loop starting")
    log.info(f"  Ollama: {args.ollama} | Model: {args.model}")
    log.info(f"  Interval: {args.interval}s | Dry-run: {args.dry_run}")

    # Init hardware
    camera  = Camera() if not args.dry_run else None
    motor_l = ODriveMini(node_id=0, interface=args.can, dry_run=args.dry_run)
    motor_r = ODriveMini(node_id=1, interface=args.can, dry_run=args.dry_run)
    leds    = NeoPixelRings(dry_run=args.dry_run)

    # State tracking
    current_posture = Posture.UNKNOWN
    distress_count  = 0
    DISTRESS_THRESHOLD = 3  # 3 consecutive DISTRESS frames before alerting

    log.info("Loop running. Ctrl+C to stop.")
    leds.set_color(POSTURE_COLORS[Posture.UNKNOWN])

    try:
        while True:
            t0 = time.monotonic()

            # 1. Capture frame
            if args.dry_run:
                # Simulate alternating states for testing
                import random
                posture = random.choice([Posture.STAND, Posture.SIT, Posture.REST])
                frame_jpeg = b""  # unused in dry-run
            else:
                frame_jpeg = camera.capture_jpeg()
                posture = classify_posture(frame_jpeg, args.ollama, args.model)

            # 2. Distress debounce
            if posture == Posture.DISTRESS:
                distress_count += 1
            else:
                distress_count = 0

            real_distress = distress_count >= DISTRESS_THRESHOLD

            # 3. State change handling
            if posture != current_posture or real_distress:
                log.info(f"Posture: {current_posture.value} → {posture.value}" +
                         (" [DISTRESS]" if real_distress else ""))
                current_posture = posture

                # 4. Motor command
                angle = POSTURE_ANGLES.get(posture)
                if angle is not None:
                    turns = deg_to_turns(angle)
                    motor_l.set_position(turns)
                    motor_r.set_position(turns)
                    log.info(f"  Motors → {angle}° ({turns:.4f} turns)")
                else:
                    motor_l.hold()
                    motor_r.hold()
                    log.info("  Motors → hold")

                # 5. NeoPixel update
                color = POSTURE_COLORS[posture]
                leds.set_color(color, pulse=(real_distress))
                log.info(f"  LEDs → RGB{color}")

            # 6. Timing
            elapsed = time.monotonic() - t0
            sleep_for = max(0.0, args.interval - elapsed)
            time.sleep(sleep_for)

    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        leds.off()
        motor_l.close()
        motor_r.close()
        if camera:
            camera.close()
        log.info("Done.")


if __name__ == "__main__":
    main()
