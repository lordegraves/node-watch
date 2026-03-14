# Node Watch

Node Watch is a lightweight infrastructure monitoring agent built as a learning and engineering exercise.

The project simulates a simplified node monitoring service similar to components used in real infrastructure platforms such as node exporters, kubelet statistics endpoints, or internal monitoring agents.

The focus of the project is clean architecture, modular design, and infrastructure-oriented engineering practices.

---

## Overview

Node Watch collects system telemetry and exposes that data through multiple interfaces.

The project demonstrates how infrastructure tooling evolves from simple scripts into structured services that can be deployed across environments.

Current interfaces include:

- CLI output
- HTTP API
- Docker container runtime

Future stages will introduce Kubernetes deployment and cloud infrastructure integration.

Lifecycle: Collectors → Service Layer → HTTP API → Docker → Kubernetes

---

## Features

Current functionality includes:

- Modular system collectors
- Aggregation service layer
- CLI interface for local inspection
- HTTP API endpoint exposing node metrics
- JSON output suitable for machine consumption
- Containerized runtime using Docker
- Structured architecture separating collectors, services, and interfaces

---

## Architecture

Node Watch separates responsibilities into three layers.

Collectors gather system information from the runtime environment.

The service layer aggregates that information into a unified node representation.

Interfaces expose the data through CLI or HTTP.

Architecture flow:

Collectors
    ↓
Service Layer (`service.py`)
    ↓
Interfaces
    ├─ CLI (`main.py`)
    └─ HTTP API (`nodewatch/api.py`)

This layered structure mirrors how many real infrastructure agents are designed.

Examples of similar patterns exist in:

- Prometheus node_exporter
- Kubernetes kubelet statistics endpoints
- internal infrastructure monitoring agents

---

## Project Structure

```
node-watch
│
├── README.md
├── Dockerfile
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
├── tests/
│
└── main.py
```

---

## Running Locally

Activate the virtual environment:

```
.venv\Scripts\Activate.ps1
```

Run the CLI interface:

```
python main.py
```

Start the HTTP API service:

```
python -m nodewatch.api
```

Query the node metrics endpoint:

```
curl.exe http://localhost:8080/node
```

---

## Running with Docker

Build the container image:

```
docker build -t node-watch:dev .
```

Run the container:

```
docker run --rm -p 8080:8080 --name node-watch node-watch:dev
```

Test the service:

```
curl.exe http://localhost:8080/health
curl.exe http://localhost:8080/node
curl.exe http://localhost:8080/
```

---

## Container Runtime Behavior

When Node Watch runs inside Docker, telemetry reflects the container runtime environment rather than the Windows host system.

Example differences include:

- hostname becomes the container ID
- OS appears as Linux (Docker runtime via WSL2)
- memory and disk reflect container-visible resources

This behavior mirrors how infrastructure agents behave when deployed inside container orchestration systems such as Kubernetes.

---


## Example Output

Example JSON response from the API:

```json
{
  "system": {...},
  "cpu": {...},
  "memory": {...},
  "disk": [...]
}
```
The exact fields depend on the current system state.

---

## Roadmap

Planned development stages include:

- Container hardening (non-root execution)
- Kubernetes deployment manifests
- Health probes and readiness checks
- Prometheus-style metrics endpoint
- Multi-node monitoring aggregation
- AWS deployment experiments

---

## Purpose

This project is designed as a practical infrastructure engineering exercise focused on:

- Python for infrastructure tooling
- modular service design
- system telemetry collection
- API exposure of node metrics
- container packaging
- orchestration readiness

The goal is to build a realistic infrastructure component through incremental improvements rather than a single monolithic implementation.

---

## License

This project is provided for educational and demonstration purposes.