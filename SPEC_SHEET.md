# Sintrones DAS Edge Node — Engineering Specification (v0.1)

## 1. Purpose

Provide a rugged, low-latency, AI-powered Distributed Acoustic Sensing (DAS)
monitoring node for subsea cable protection using Sintrones industrial edge
computers.

This document captures the initial v0.1 requirements and targets for future
implementations.

## 2. Hardware Requirements

### 2.1 Required Components

- **DAS Optical Front-End**
  - Laser source, modulator, photodiode, high-speed ADC
  - Interface: PCIe, Ethernet, or USB towards the Sintrones node

- **Sintrones Edge Computer**
  - Model: IBOX / VBOX / RBOX family (or similar)
  - CPU: x86_64 with at least 4 cores
  - GPU: NVIDIA RTX A2 / T4 / Jetson (for ML acceleration)
  - RAM: 16 GB minimum (32 GB recommended)
  - Storage: 512 GB+ NVMe SSD (for event history)

- **Dark Fiber**
  - One unused fiber pair in the subsea cable for DAS sensing

- **Time Synchronization**
  - GPS receiver or PTP/NTP source

- **Power Protection**
  - UPS, surge protection (recommended)

## 3. Software Architecture (High-Level)

Layers (top-down):

1. **UI + API Layer**
   - Web dashboard (map + timeline + events)
   - REST/gRPC APIs for NOC / Coast Guard integrations

2. **Event & Rules Engine**
   - Severity scoring (Level 1–3)
   - Temporal & spatial clustering of events
   - Context correlation (AIS, maintenance windows, weather)

3. **ML Inference Layer**
   - Models to classify signatures:
     - Anchor drag
     - Grapnel interference
     - ROV
     - Diver / manipulator
     - Cutting attempts
     - Wave / seismic noise

4. **Signal Processing Layer**
   - Filters, FFT, spectral analysis
   - Feature extraction per distance bin

5. **DAS SDK / Driver Layer**
   - Vendor-provided SDK
   - Range binning, phase & amplitude extraction

6. **Optical Front-End**
   - Laser pulsing and backscatter acquisition

## 4. Performance Targets (Conceptual)

- Minimum detectable strain: ~10 nanostrain (10⁻⁸)
- Frequency range: 1 Hz – 5 kHz
- Spatial resolution: 2–10 m
- Coverage: 40–100 km per landing station (depending on fiber/ADC)
- End-to-end detection & classification latency: < 1 second
- Alarm issuance: within 5–10 seconds of event onset

## 5. External Integrations

- AIS feed (ship locations)
- Radar / VTS (optional)
- Weather and sea-state APIs
- Maintenance schedule / planned operations feed
- Central NOC / SOC systems (via REST/Syslog/gRPC)

## 6. Security Considerations

- TLS-encrypted APIs
- Role-based access control for UI and configuration
- Signed OTA updates for ML models and config
- Local audit logs for operator actions

## 7. Roadmap Notes

- **v0.1**: Skeleton structure, documentation, DAS simulator placeholders
- **v0.2**: Simulated dataflow end-to-end + simple API and console UI
- **v0.3**: Basic web dashboard + first ML baseline model
- **v1.0**: Hardened deployment package for landing stations
