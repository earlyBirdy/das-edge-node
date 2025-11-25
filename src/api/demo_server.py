"""Minimal placeholder demo server for v0.1.

In v0.2 this will simulate a simple DAS event stream and expose it over
an HTTP endpoint or console output.
"""

import time
import random

EVENT_TYPES = [
    "background_noise",
    "anchor_drag_suspected",
    "rov_activity_suspected",
    "grapnel_contact_suspected",
    "diver_contact_suspected",
    "cutting_attempt_suspected"
]

def generate_fake_event():
    return {
        "timestamp": time.time(),
        "distance_km": round(random.uniform(0, 80), 2),
        "type": random.choice(EVENT_TYPES),
        "severity": random.randint(1, 3),
        "confidence": round(random.uniform(0.5, 0.99), 2),
    }

def main():
    print("Sintrones DAS Edge Node demo simulator (v0.1)")
    print("Generating fake DAS events. Ctrl+C to stop.\n")
    try:
        while True:
            evt = generate_fake_event()
            print(evt)
            time.sleep(2.0)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
