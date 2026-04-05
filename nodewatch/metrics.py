from nodewatch.service import get_node_data


def _escape_label(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _safe_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _safe_disk_list(value: object) -> list[dict]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def render_prometheus_metrics() -> str:
    node_data = get_node_data()
    lines = []

    host = _safe_dict(node_data.get("host", {}))
    runtime = _safe_dict(node_data.get("runtime", {}))

    # --- CPU ---
    lines.append("# HELP nodewatch_cpu_usage_percent CPU usage percentage")
    lines.append("# TYPE nodewatch_cpu_usage_percent gauge")

    host_cpu = _safe_dict(host.get("cpu", {}))
    runtime_cpu = _safe_dict(runtime.get("cpu", {}))

    if host_cpu.get("usage_percent") is not None:
        lines.append(f'nodewatch_cpu_usage_percent{{scope="host"}} {host_cpu.get("usage_percent")}')

    if runtime_cpu.get("usage_percent") is not None:
        lines.append(f'nodewatch_cpu_usage_percent{{scope="runtime"}} {runtime_cpu.get("usage_percent")}')

    # --- MEMORY ---
    lines.append("# HELP nodewatch_memory_total_mb Total memory in MB")
    lines.append("# TYPE nodewatch_memory_total_mb gauge")

    host_mem = _safe_dict(host.get("memory", {}))
    runtime_mem = _safe_dict(runtime.get("memory", {}))

    lines.append(f'nodewatch_memory_total_mb{{scope="host"}} {host_mem.get("total_mb", 0)}')
    lines.append(f'nodewatch_memory_total_mb{{scope="runtime"}} {runtime_mem.get("total_mb", 0)}')

    lines.append("# HELP nodewatch_memory_used_mb Used memory in MB")
    lines.append("# TYPE nodewatch_memory_used_mb gauge")

    lines.append(f'nodewatch_memory_used_mb{{scope="host"}} {host_mem.get("used_mb", 0)}')
    lines.append(f'nodewatch_memory_used_mb{{scope="runtime"}} {runtime_mem.get("used_mb", 0)}')

    lines.append("# HELP nodewatch_memory_percent_used Memory used percentage")
    lines.append("# TYPE nodewatch_memory_percent_used gauge")

    lines.append(f'nodewatch_memory_percent_used{{scope="host"}} {host_mem.get("percent_used", 0)}')
    lines.append(f'nodewatch_memory_percent_used{{scope="runtime"}} {runtime_mem.get("percent_used", 0)}')

    # --- UPTIME ---
    lines.append("# HELP nodewatch_uptime_seconds Uptime in seconds")
    lines.append("# TYPE nodewatch_uptime_seconds gauge")

    host_sys = _safe_dict(host.get("system", {}))
    runtime_sys = _safe_dict(runtime.get("system", {}))

    if host_sys.get("uptime_seconds") is not None:
        lines.append(f'nodewatch_uptime_seconds{{scope="host"}} {host_sys.get("uptime_seconds")}')

    if runtime_sys.get("uptime_seconds") is not None:
        lines.append(f'nodewatch_uptime_seconds{{scope="runtime"}} {runtime_sys.get("uptime_seconds")}')

    # --- DISK (host only) ---
    lines.append("# HELP nodewatch_disk_used_percent Disk used percentage")
    lines.append("# TYPE nodewatch_disk_used_percent gauge")

    disks = _safe_disk_list(host.get("disk", []))
    for disk in disks:
        device = _escape_label(disk.get("device", ""))
        mountpoint = _escape_label(disk.get("mountpoint", ""))
        value = disk.get("percent_used", 0)

        lines.append(
            f'nodewatch_disk_used_percent{{device="{device}",mountpoint="{mountpoint}"}} {value}'
        )

    return "\n".join(lines) + "\n"