# Sintrones DAS Edge Node (v0.1)

Distributed Acoustic Sensing (DAS) + Edge AI node for subsea cable security,
designed to run on rugged Sintrones edge computing platforms.

This v0.1 repository focuses on:
- Directory structure
- Initial documentation
- Skeleton Python modules for future integration
- A simple simulated DAS event pipeline (placeholder)

## Project Goals

- Ingest vibration data from a DAS optical front-end over PCIe/Ethernet/USB
- Run low-level DSP and ML inference on a Sintrones edge computer
- Detect and classify subsea cable interference (anchor drag, ROV, grapnel, etc.)
- Provide real-time alerts, dashboards, and APIs
- Support OTA updates of ML models and configuration

## Repo Layout

```text
sintrones-das-edge-node/
├── README.md
├── SPEC_SHEET.md
├── ARCHITECTURE.md
├── diagrams/
│   ├── function-diagram.txt
│   └── dataflow-diagram.txt
├── src/
│   ├── ingest/
│   ├── dsp/
│   ├── ml/
│   ├── rules/
│   ├── ui/
│   ├── api/
│   └── storage/
├── config/
│   ├── cable_map.sample.json
│   ├── thresholds.sample.yaml
│   └── ml_models/
└── ota/
    ├── update_manifest.sample.json
    └── scripts/
```

## Status: v0.1

This is a **concept + skeleton** implementation:

- No real DAS SDK integration yet
- Contains a toy simulator of DAS events for development
- Ready to be extended in v0.2 with:
  - Simulated data pipeline end-to-end
  - Basic REST API
  - Minimal web UI

## Quickstart (development)

```bash
git clone <your-repo-url> sintrones-das-edge-node
cd sintrones-das-edge-node

# Optional: create virtualenv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # (to be defined in v0.2)

# Run the demo simulator (placeholder)
python -m src.api.demo_server
```

## License

TBD (Apache-2.0 is recommended for open collaboration).
