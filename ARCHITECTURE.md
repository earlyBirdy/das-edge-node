# Sintrones DAS Edge Node — Architecture (v0.1)

This document captures the initial functional diagram and dataflow for the
Sintrones DAS Edge Node concept.

## 1. Functional Block Diagram

```txt
        ┌───────────────────────────────────────────────────────────┐
        │                   SEAFLOOR / PHYSICAL LAYER               │
        │                                                           │
        │  Subsea Cable  ── Dark Fiber (sensor fiber) ──────────┐   │
        └───────────────────────────────────────────────────────┴───┘
                                                                │
                     Landing Station / Cable Hut                │
┌───────────────────────────────────────────────────────────────┴──────────────────────-─────────┐
│                               DAS + EDGE AI SECURITY NODE (RACK)                               │
│                                                                                                │
│  ┌──────────────────┐          ┌────────────────────────────────────────────────────────────┐  │
│  │  DAS FRONT-END   │  Fiber   │            SINTRONES EDGE AI COMPUTING (BOX)               │  │
│  │ (Optical module) ├─────────►│   (CPU + GPU + NVMe + Multi-LAN, rugged/24×7)              │  │
│  └──────────────────┘          └────────────────────────────────────────────────────────────┘  │
│         ▲                           │                    │                    │                │
│         │                           │                    │                    │                │
│   Laser pulses &                    │                    │                    │                │
│   backscatter ADC                   │                    │                    │                │
│                                     │                    │                    │                │
│                                     ▼                    ▼                    ▼                │
│          ┌──────────────────────────────┐   ┌───────────────────────────┐  ┌────────────────┐  │
│          │  DAS SDK & LOW-LEVEL DSP     │   │  SIGNAL PROC & FEATURES   │  │  ML INFERENCE  │  │
│          │  (vendor library / driver)   │   │  (FFT, filters, feature   │  │  ENGINE        │  │
│          │  - range binning             │   │   vectors per distance)   │  │  - classifiers │  │
│          │  - phase/amplitude calc      │   │                           │  │  - anomaly det.│  │
│          └───────────────┬──────────────┘   └───────────────┬───────────┘  └─────────┬──────┘  │
│                          │                                  │                        │         │
│                          ▼                                  ▼                        ▼         │
│          ┌───────────────────────────────┐   ┌───────────────────────────┐  ┌────────────────┐ │
│          │ EVENT & RULES ENGINE         │   │  DATA STORAGE & LOGGING   │  │  UI + API LAYER │ │
│          │ - severity levels            │   │  - raw/processed traces   │  │  - web dashboard│ │
│          │ - alarm logic (L1/L2/L3)     │   │  - alerts history         │  │  - REST/gRPC    │ │
│          │ - correlation windows        │   │  - forensics export       │  │  - map view     │ │
│          └───────────────┬──────────────┘   └───────────────┬───────────┘  └─────────┬────-──┘ │
│                          │                                  │                          │       │
│                          │                                  │                          │       │
│                          ▼                                  │                          ▼       │
│       ┌───────────────────────────────┐                     │        ┌──────────────────────┐  │
│       │ EXTERNAL FEEDS / CONTEXT      │                     │        │ MGMT / OTA / SECURITY│  │
│       │ - AIS / radar / weather       │                     │        │ - model updates      │  │
│       │ - maintenance schedules       │                     │        │ - config / policies  │  │
│       │ - “known operations” windows  │                     │        │ - health monitoring  │  │
│       └───────────────────────────────┘                     │        └──────────────────────┘  │
│                          │                                  │                                  │
└──────────────────────────┴──────────────────────────────────┴────────────────────────── ───────┘
```

## 2. End-to-End Dataflow

```txt
[1] PHYSICAL WORLD
────────────────────────────────────────────────────────────────────────
  • Ship anchor, grapnel, ROV, diver, or cutter interacts with cable
  • Cable and embedded fiber experience micro-strain / vibration

            │
            ▼
[2] FIBER AS SENSOR
────────────────────────────────────────────────────────────────────────
  • Dark fiber in subsea cable carries:
      - DAS laser pulses (from landing station)
      - Rayleigh backscatter returning to shore

            │
            ▼
[3] DAS OPTICAL FRONT-END (MODULE)
────────────────────────────────────────────────────────────────────────
  • Sends coherent laser pulses into fiber
  • Receives backscatter, converts to electrical
  • High-speed ADC digitizes signal
  • Streams raw backscatter samples → Sintrones (PCIe/Eth/USB)

            │
            ▼
[4] DAS SDK + LOW-LEVEL DSP (on SINTRONES)
────────────────────────────────────────────────────────────────────────
  • Vendor SDK + wrapper:
      - Time alignment of pulses
      - Compute phase/amplitude changes
      - Map to distance bins (e.g. every 5 m)
  • Output: time-series array: Vibration[distance_bin, time]

            │
            ▼
[5] SIGNAL PROCESSING & FEATURE EXTRACTION
────────────────────────────────────────────────────────────────────────
  • For each distance bin / time window:
      - Band-pass filtering
      - FFT / spectral features
      - RMS, kurtosis, envelope
      - Short-time energy, slope, etc.
  • Output: FeatureVector[distance_bin, time_window, features...]

            │
            ▼
[6] ML INFERENCE ENGINE
────────────────────────────────────────────────────────────────────────
  • 1D-CNN / RNN / LSTM / transformer or anomaly model:
      - Input: feature vectors per bin
      - Output for each active bin:
          • class: {anchor_drag, grapnel, ROV, diver, cutter, wave, quake}
          • confidence score
          • anomaly score
  • Creates "events":
      - {time, distance_km, class, confidence, raw snippet ref}

            │
            ▼
[7] EVENT & RULES ENGINE
────────────────────────────────────────────────────────────────────────
  • Combine ML events + rules:
      - Check persistence (X seconds)
      - Combine adjacent bins (spatial cluster)
      - Correlate with external feeds:
          • AIS (ship here? identity?)
          • radar / patrol reports
          • planned maintenance windows
  • Assign severity level:
      - Level 1: suspicious vibration
      - Level 2: likely interference (anchor/ROV)
      - Level 3: probable sabotage / cutting

            │
            ▼
[8] UI + API + ALERTING
────────────────────────────────────────────────────────────────────────
  • Web UI (hosted on Sintrones):
      - Map of cable, highlight km of event
      - Timeline & waveform viewer
      - Event list with class + severity
  • APIs:
      - REST/gRPC → NOC/SOC, Coast Guard, Navy
  • Alerts:
      - Syslog / SIEM, SMS, email, chat bots
      - Can push to central monitoring nodes

            │
            ▼
[9] DATA STORAGE & OFFLINE ANALYTICS
────────────────────────────────────────────────────────────────────────
  • Sintrones NVMe:
      - Raw/processed segments for X days
      - Labels (operator feedback: true/false)
  • Optional periodic upload to central data lake:
      - Model retraining
      - Long-term forensics

            │
            ▼
[10] MGMT / OTA / MODEL LIFECYCLE
────────────────────────────────────────────────────────────────────────
  • OTA server:
      - Push updated ML models (better detection)
      - Update config (thresholds, rules, cable maps)
      - Monitor health of all landing-station nodes
  • Feedback loop:
      - Operator labels → central training → new model → OTA → Sintrones
```

This architecture is intentionally technology-agnostic. Future versions of this
repo (v0.2+) will provide reference implementations for the key blocks.
