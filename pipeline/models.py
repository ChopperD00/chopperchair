#!/usr/bin/env python3
"""
ChopperChair — Ollama Model Routing
Sovereign multi-node inference via Tailscale mesh.
"""

NODES = {
    "ACIDBURN": {
        "host": "100.69.29.1", "port": 11434,
        "gpu": "RX 6700 XT 12GB",
        "models": ["gemma4:e2b", "gemma4:e4b"],
        "role": "Fast triage, photo measurement extraction",
    },
    "GRIMLOCK": {
        "host": "TBD", "port": 11434,
        "gpu": "24GB+ target (RX 7900 XTX)",
        "models": ["gemma4:31b-it-q4_K_M"],
        "role": "Deep reasoning, complex fitting logic",
    },
}

ROUTING = {
    "measure":  ("ACIDBURN", "gemma4:e4b"),
    "validate": ("ACIDBURN", "gemma4:e4b"),
    "reason":   ("GRIMLOCK", "gemma4:31b-it-q4_K_M"),
}

def url(node): return f"http://{NODES[node]['host']}:{NODES[node]['port']}"
def model_for(task): return ROUTING.get(task, ("ACIDBURN", "gemma4:e4b"))
