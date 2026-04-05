# Node Watch

Node Watch is a lightweight node-level telemetry agent designed to demonstrate real-world infrastructure patterns across local systems, containers, Kubernetes, and cloud environments.

It collects system and runtime telemetry, exposes structured data via HTTP, and publishes Prometheus-compatible metrics. The focus is on clean architecture, observability fundamentals, and practical deployment workflows rather than building a full monitoring platform.

Node Watch is built around a simple question:

> Can a small, well-structured service behave like a real infrastructure agent across environments?

This project answers that question through:

- modular Python collectors
- containerized packaging
- Kubernetes DaemonSet deployment
- container image distribution via Amazon ECR
- standalone execution on EC2
- optional host-level visibility via controlled filesystem access

---

## Overview

Node Watch collects system telemetry and exposes it through structured interfaces designed for both human inspection and machine consumption.

The service operates across two distinct perspectives:

- **host** — the underlying machine (when host access is available)
- **runtime** — the container or environment where Node Watch is executing

This reflects a core reality of modern infrastructure:

> Containers do not automatically have visibility into the host system. That access must be explicitly provided.

Node Watch makes this distinction visible by design, allowing telemetry to change based on how and where the service is deployed.

---

### Interfaces

Node Watch exposes data through:

- CLI output for local inspection
- HTTP JSON API (`/node`) for structured telemetry
- Prometheus-compatible metrics endpoint (`/metrics`)
- Health and readiness endpoints (`/health`, `/ready`)

Each interface is backed by the same service layer, ensuring consistent behavior across access methods.

---

### Deployment Progression

The project follows a deliberate infrastructure lifecycle:

```text
Collectors
  → Service Layer
  → Interfaces (CLI / API / Metrics)
  → Container Runtime (Docker)
  → Kubernetes (DaemonSet per node)
  → Cloud Distribution (ECR)
  → Standalone Cloud Runtime (EC2)
  ```

### Interfaces

Node Watch exposes data through:

- CLI output (local inspection)
- HTTP JSON API (`/node`)
- Prometheus metrics endpoint (`/metrics`)
- Health and readiness endpoints (`/health`, `/ready`)

### Deployment Progression

The project intentionally follows a realistic infrastructure lifecycle:

```text
Collectors
  → Service Layer
  → Interfaces (CLI / API / Metrics)
  → Container Runtime (Docker)
  → Kubernetes (DaemonSet per node)
  → Cloud Distribution (ECR)
  → Standalone Cloud Runtime (EC2)
```

---

## Quick Start

Run Node Watch locally and verify basic functionality.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the service

```bash
python -m nodewatch.api
```

### 3. Verify endpoints

```bash
curl http://localhost:8080/health
curl http://localhost:8080/node
curl http://localhost:8080/metrics
```

If the service is running correctly:
- `/health` returns status OK
- `/node` returns structured telemetry
- `/metrics` returns Prometheus-formatted metrics

---

## Features

Node Watch provides a focused telemetry agent with clear separation between data collection, aggregation, and exposure.

---

### Telemetry Collection

- System, CPU, memory, and disk collectors implemented in Python  
- Explicit separation between **host** and **runtime** visibility  
- Optional host-level telemetry via read-only filesystem mount (`/host`)  
- Supplemental system data via external Go probes  

---

### Data Model and Aggregation

- Central service layer aggregates all collector output into a unified node model  
- Consistent JSON structure exposed through `/node`  
- Designed to tolerate missing or partial telemetry without failing  

---

### Interfaces

- CLI interface for local inspection  
- HTTP API (`/node`) for structured telemetry  
- Prometheus-compatible metrics endpoint (`/metrics`)  
- Health and readiness endpoints (`/health`, `/ready`)  

---

### Deployment Models

- Local Python execution  
- Docker container runtime  
- Kubernetes DaemonSet (one agent per node)  
- Standalone EC2 deployment using Docker  
- Host-aware runtime mode using read-only host mount  

---

### Container and Cloud Integration

- Docker image packaging for portability  
- Amazon ECR for image distribution  
- Pull-and-run model for remote execution on EC2  

---

### Design Characteristics

- Modular collector architecture  
- Clear separation of concerns (collectors → service → interfaces)  
- Cross-language integration pattern (Python + Go)  
- Behavior changes explicitly based on runtime environment 

---

## Architecture

Node Watch is structured as a layered system that separates data collection, aggregation, and exposure.


### Core Layers

**Collectors**

Collectors gather telemetry from the environment where Node Watch is running.

- System, CPU, memory, and disk collectors implemented in Python  
- Separate collection paths for **host** and **runtime**  
- Host-level data requires explicit filesystem access (`/host` mount)  

**Service Layer**

The service layer (`service.py`) aggregates collector output into a unified node model.

- Combines Python collectors and external probe data  
- Produces a consistent structure used by all interfaces  
- Designed to tolerate incomplete or missing telemetry  

**External Probes**

External probes extend the system beyond Python.

- Go-based probes executed via subprocess  
- Return structured JSON via stdout  
- Merged into the host telemetry model  

**Interfaces**

Node Watch exposes data through multiple interfaces:

- CLI (`main.py`)  
- HTTP API (`/node`)  
- Prometheus-compatible metrics (`/metrics`)  
- Health and readiness endpoints  

### Deployment Model

```text
Application Layers
    ↓
Container Runtime (Docker)
    ↓
Deployment Targets
    ├─ Local execution
    ├─ Kubernetes (DaemonSet)
    └─ EC2 (standalone Docker runtime)
```

### Execution Flow

```text
Collectors
    ↓
Service Layer (aggregation)
    ↓
External Probes (Go)
    ↓
Interfaces (CLI / API / Metrics)
  ```

  ### Host vs Runtime Model

  A key architectural decision is the explicit separation between:

- **runtime** — the container or process environment
- **host** — the underlying machine

Without a host filesystem mount, the service can only observe runtime data.

With a read-only host mount (`-v /:/host:ro` or Kubernetes `hostPath`), Node Watch can collect node-level telemetry.

This mirrors how real infrastructure agents operate in containerized environments.

### Design Principles

- Separation of concerns (collectors → service → interfaces)
- Consistent data model across all interfaces
- Graceful degradation when telemetry is incomplete
- Explicit handling of environment-dependent visibility
- Extensibility through external probes

### Real-World Alignment

This structure reflects patterns used in:

- Prometheus `node_exporter`
- Kubernetes kubelet statistics endpoints
- internal infrastructure monitoring agents

The goal is not feature parity, but architectural similarity.

---

## Project Structure

The repository is organized to reflect the architectural layers of the system.

```text
node-watch/
├── README.md
├── Dockerfile
├── requirements.txt
├── .gitignore
│
├── main.py                  # CLI entrypoint
│
├── nodewatch/               # Core application package
│   ├── api.py               # HTTP API server
│   ├── service.py           # Aggregation layer (core logic)
│   ├── metrics.py           # Prometheus metrics renderer
│   ├── config.py            # Central configuration (env-driven)
│   ├── logging.py           # Structured logging
│   │
│   └── collectors/          # Telemetry collectors
│       ├── system_info.py   # Hostname, OS, uptime
│       ├── cpu.py           # CPU usage
│       ├── memory.py        # Memory stats
│       ├── disk.py          # Disk usage (host + runtime aware)
│       └── host_info.py     # Host-specific helpers
│
├── go-probes/               # External probes (Go)
│   ├── system_probe.go
│   ├── memory_probe.go
│   ├── go.mod
│   └── go.sum
│
├── k8s/                     # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── service.yaml
│   └── daemonset.yaml       # One agent per node
│
├── k8s/examples/            # Example workloads
│   └── cronjob.yaml
│
└── tests/                   # Unit tests
```

---

## Running Node Watch

### Locally

Run Node Watch directly using Python for development and validation.

Start the service:

```bash
python -m nodewatch.api
```

Test endpoints:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/node
curl http://localhost:8080/metrics
```

### Docker

Build the container image:

```bash
docker build -t node-watch:dev .
```

Run the container:

```bash
docker run --rm -p 8080:8080 --name node-watch node-watch:dev
```

Test endpoints:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/node
curl http://localhost:8080/metrics
```

### Kubernetes

Node Watch runs as a DaemonSet, ensuring one instance per node.

The deployment uses:

- Namespace isolation  
- ConfigMap-based runtime configuration  
- DaemonSet scheduling (one pod per node)  

Apply manifests:

```bash
kubectl apply -f k8s/
```

Verify deployment:

```bash
kubectl get daemonsets -n node-watch
kubectl get pods -n node-watch
kubectl get svc -n node-watch
```

Access locally:

```bash
kubectl port-forward -n node-watch svc/node-watch 8080:8080
```

Test endpoints:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/node
curl http://localhost:8080/metrics
```

### Why DaemonSet

A Deployment runs multiple copies across the cluster.

A DaemonSet runs exactly one copy on each node.

For a node-level monitoring agent, DaemonSet is the correct model.

---

## Operational Behavior

This section describes how Node Watch behaves at runtime, how it is configured, and what it produces.

### Container Runtime Behavior

When Node Watch runs inside `Docker` or `Kubernetes`, telemetry reflects the environment it is running in rather than the underlying host system.

The service distinguishes between two perspectives:

- **runtime** — the container or pod environment where Node Watch is executing
- **host** — the node the container is running on

Example differences include:

- runtime hostname reflects the container or pod
- host hostname reflects the node
- OS may differ between runtime and host
- memory and disk usage reflect what is visible within each scope

In Kubernetes environments, “host” refers to the node the pod is scheduled on. In local setups such as kind, that node may itself be a container, so host-level telemetry reflects the node environment rather than the physical machine.

This mirrors how real infrastructure monitoring agents operate, where node-level telemetry is collected from within the orchestration environment rather than from outside it.

### Runtime Configuration

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

```bash
NODEWATCH_PORT=8080
NODEWATCH_LOG_LEVEL=info
```

The application reads these values at startup using environment variables, allowing behavior to be modified without rebuilding the container image.

### Example Output

Example JSON response from `/node`:

```json
{
  "host": {
    "system": {...},
    "cpu": {...},
    "memory": {...},
    "disk": [...],
    "go_probe": {
      "system_probe": {
        "hostname": "...",
        "logical_cpu_count": ...,
        "os": "...",
        "arch": "..."
      },
      "memory_probe": {
        "total_mb": ...,
        "used_mb": ...,
        "percent_used": ...
      }
    }
  },
  "runtime": {
    "system": {...},
    "cpu": {...},
    "memory": {...},
    "disk": [...]
  }
}
```

Example Prometheus metrics output from `/metrics`:

```markdown
# HELP nodewatch_cpu_usage_percent CPU usage percentage
# TYPE nodewatch_cpu_usage_percent gauge
nodewatch_cpu_usage_percent{scope="host"} 0.6
nodewatch_cpu_usage_percent{scope="runtime"} 0.9

# HELP nodewatch_memory_total_mb Total memory in MB
# TYPE nodewatch_memory_total_mb gauge
nodewatch_memory_total_mb{scope="host"} 15796.19
nodewatch_memory_total_mb{scope="runtime"} 15796.19

# HELP nodewatch_memory_used_mb Used memory in MB
# TYPE nodewatch_memory_used_mb gauge
nodewatch_memory_used_mb{scope="host"} 1717.01
nodewatch_memory_used_mb{scope="runtime"} 1717.01

# HELP nodewatch_memory_percent_used Memory used percentage
# TYPE nodewatch_memory_percent_used gauge
nodewatch_memory_percent_used{scope="host"} 10.9
nodewatch_memory_percent_used{scope="runtime"} 10.9

# HELP nodewatch_uptime_seconds Uptime in seconds
# TYPE nodewatch_uptime_seconds gauge
nodewatch_uptime_seconds{scope="host"} 119296.04
nodewatch_uptime_seconds{scope="runtime"} 119296

# HELP nodewatch_disk_used_percent Disk used percentage
# TYPE nodewatch_disk_used_percent gauge
nodewatch_disk_used_percent{device="/dev/sde",mountpoint="/host/var"} 0.7
nodewatch_disk_used_percent{device="/dev/sdd",mountpoint="/host/usr/lib/modules"} 56.4

```

The exact fields depend on the current system state.

---

## Roadmap

Planned areas for future development:

### Telemetry Expansion

- Additional system metrics (temperature, network interface statistics)  
- Improved disk and hardware-level visibility  
- Broader host-level telemetry coverage via Kubernetes host mounts  

### Observability and Alerting

- Threshold-based alerting for key metrics  
- Basic alert evaluation logic within the service  
- Exploration of integration with external alerting systems  

### Interface Improvements

- Enhanced HTTP interface beyond raw JSON output  
- More structured and human-readable responses  
- Exploration of lightweight visualization or summary endpoints  

### Distributed Monitoring

- Multi-node monitoring and aggregation  
- Cross-node visibility and comparison  
- Distributed telemetry collection experiments  

### Cloud and Deployment

- Additional cloud deployment scenarios (AWS)  
- Expansion of container image distribution and runtime patterns  

These items represent natural extensions of the current architecture rather than a separate system redesign.

---

## Purpose

This project is a practical infrastructure engineering exercise focused on building a small, well-structured system that behaves like a real node-level monitoring agent.

It is designed to demonstrate:

- system telemetry collection across host and runtime boundaries  
- modular service design with clear separation of concerns  
- API-based exposure of infrastructure metrics  
- container-aware behavior and observability patterns  
- Kubernetes-native deployment using a DaemonSet model  
- portable artifact flow (build → push → pull → run)  

The goal is not to build a full monitoring platform, but to implement a realistic and explainable infrastructure component that reflects how production systems behave.

The project intentionally mirrors patterns used by real monitoring agents such as Prometheus `node_exporter`, Datadog agents, and Kubernetes node-level telemetry systems.

---

## License

This project is provided for educational and demonstration purposes.