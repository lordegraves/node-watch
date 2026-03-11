# Node Watch

Node Watch is a lightweight infrastructure monitoring agent built as a learning and engineering exercise.

The project simulates a simplified node monitoring service similar to components used in real infrastructure platforms such as node exporters, kubelet statistics endpoints, or internal monitoring agents.

The focus of the project is clean architecture, modular design, and infrastructure-oriented engineering practices.

---

## Overview

Node Watch collects system information from the host machine and exposes that data through multiple interfaces.

The project demonstrates how infrastructure tooling can evolve from simple scripts into structured services.

Current interfaces include:

- CLI output
- HTTP API endpoint

Future stages will introduce containerization, Kubernetes deployment, and cloud adaptation.

---

## Features

Current functionality includes:

- Modular system collectors
- Aggregation service layer
- CLI interface for local inspection
- HTTP API endpoint exposing node metrics
- JSON output suitable for machine consumption
- Structured architecture separating collectors, services, and interfaces

---

## Architecture

Node Watch separates responsibilities into three layers.

Collectors gather system information from the host.

The service layer aggregates that information into a single node representation.

Interfaces expose the data through CLI or HTTP.

Architecture flow:

Collectors  
↓  
Service Layer (`service.py`)  
↓  
Interfaces  
- CLI (`main.py`)  
- HTTP API (`nodewatch/api.py`)

This layered structure mirrors how many real infrastructure agents are designed.

---

## Project Structure

node-watch  
│  
├── README.md  
├── main.py  
├── requirements.txt  
├── .gitignore  
│  
├── nodewatch/  
│   ├── api.py  
│   ├── service.py  
│   └── collectors/  
│       ├── system_info.py  
│       ├── cpu.py  
│       ├── memory.py  
│       └── disk.py  
│  
└── tests/  

---

## Running Locally

Activate the virtual environment:

.venv\Scripts\Activate.ps1

Run the CLI interface:

python main.py

Start the HTTP API service:

python -m nodewatch.api

Query the node metrics endpoint:

curl http://localhost:8080/node

---

## Example Output

Example JSON response from the API:

{
  "system": {...},
  "cpu": {...},
  "memory": {...},
  "disk": [...]
}

The exact fields depend on the current system state.

---

## Roadmap

Planned development stages include:

- Health endpoint (`/health`)
- Root API endpoint documentation
- Docker containerization
- Kubernetes deployment
- Prometheus-style metrics output
- AWS deployment adaptation

---

## Purpose

This project is designed as a practical infrastructure engineering exercise focused on:

- Python for infrastructure tooling
- modular service design
- system telemetry collection
- API exposure of node metrics
- container and orchestration readiness

The goal is to build a realistic infrastructure component through incremental improvements rather than a single monolithic implementation.

---

## License

This project is provided for educational and demonstration purposes.