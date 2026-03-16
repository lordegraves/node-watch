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
- HTTP JSON API
- Prometheus `/metrics` endpoint
- Docker container runtime

Lifecycle: Collectors → Service Layer → HTTP API → Container Runtime → Kubernetes (Namespace → Service → ConfigMap → DaemonSet)

---

## Features

Current functionality includes:

- Prometheus-style `/metrics` endpoint
- Host-aware telemetry via read-only host filesystem access
- Modular system collectors
- Aggregation service layer
- CLI interface for local inspection
- HTTP API endpoint exposing node metrics
- JSON output suitable for machine consumption
- Containerized runtime using Docker
- Structured architecture separating collectors, services, and interfaces
- Kubernetes namespace isolation
- ConfigMap-driven runtime configuration
- DaemonSet deployment model (one monitoring agent per node)

---

## Architecture

Node Watch separates responsibilities into three layers.

Collectors gather system information from the runtime environment.

When running inside Kubernetes, additional host-level telemetry can be collected through a read-only host filesystem mount, allowing the agent to observe node-level telemetry rather than only container-scoped metrics.

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

### Kubernetes Runtime Architecture

Node Watch mounts the host filesystem in read-only mode to collect node-level telemetry.

This pattern mirrors how real monitoring agents (such as Prometheus node_exporter or Datadog agents) access host resources when deployed in Kubernetes.

Runtime flow:

Each Kubernetes node automatically runs exactly one Node Watch instance.

Cluster Node
    ↓
DaemonSet
    ↓
Node Watch Pod
    ↓
Container Runtime
    ↓
HTTP API

---

## Deployment Architecture

When deployed to Kubernetes, Node Watch runs as a node-level monitoring agent.

ConfigMap
    ↓
DaemonSet
    ↓
Node Watch Pod (one per node)
    ↓
HTTP API
    ↓
Service

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
│   ├── metrics.py
│   ├── host_info.py
│   └── collectors/
│       ├── system_info.py
│       ├── cpu.py
│       ├── memory.py
│       └── disk.py
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── service.yaml
│   └── daemonset.yaml
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

Query the Prometheus metrics endpoint:

```
curl.exe http://localhost:8080/metrics
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
curl.exe http://localhost:8080/metrics
```

---

## Running in Kubernetes

Node Watch can be deployed into a Kubernetes cluster as a node monitoring agent.

The Kubernetes deployment model uses:

- Namespace isolation
- ConfigMap-based runtime configuration
- DaemonSet scheduling (one pod per node)

Apply the manifests:

```
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/daemonset.yaml
```

Verify the deployment:

```
kubectl get daemonsets -n node-watch
kubectl get pods -n node-watch
kubectl get svc -n node-watch
```

Access the API locally:

```
kubectl port-forward -n node-watch svc/node-watch 8080:8080
```

Query the Prometheus-style `/metrics` endpoint:

```
curl.exe http://localhost:8080/metrics
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

## Runtime Configuration

Node Watch supports runtime configuration through environment variables.

In Kubernetes deployments, these values are provided through a ConfigMap.

Current configurable settings:

- **NODEWATCH_PORT**  
  Controls the HTTP API listening port.  
  Defaults to `8080` if not provided.

- **NODEWATCH_LOG_LEVEL**  
  Controls application logging verbosity.  
  Defaults to `"info"`.

Example configuration (ConfigMap):

NODEWATCH_PORT=8080
NODEWATCH_LOG_LEVEL=info

The application reads these values at startup using environment variables, allowing behavior to be modified without rebuilding the container image.

---

## Example Output

Example JSON response from `/node`:

```json
{
  "system": {...},
  "cpu": {...},
  "memory": {...},
  "disk": [...]
}
```

Example Prometheus metrics output from `/metrics`:

```
# HELP nodewatch_cpu_usage_percent CPU usage percentage
# TYPE nodewatch_cpu_usage_percent gauge
nodewatch_cpu_usage_percent 0.4

# HELP nodewatch_host_uptime_seconds Host uptime in seconds
# TYPE nodewatch_host_uptime_seconds gauge
nodewatch_host_uptime_seconds 40497.65

```

The exact fields depend on the current system state.

---

## Roadmap

Planned development stages include:

- Host-level telemetry via Kubernetes host mounts
- Multi-node monitoring aggregation
- Distributed telemetry collection experiments
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

The project intentionally mirrors patterns used by real node monitoring agents such as Prometheus node_exporter, Datadog agents, and Kubernetes node-level telemetry collectors.

---

## License

This project is provided for educational and demonstration purposes.