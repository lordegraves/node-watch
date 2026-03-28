from nodewatch.service import get_node_data


def render_prometheus_metrics() -> str:
    node_data = get_node_data()
    lines = []

    host = node_data.get("host", {})
    runtime = node_data.get("runtime", {})

    # --- CPU ---
    lines.append("# HELP nodewatch_cpu_usage_percent CPU usage percentage")
    lines.append("# TYPE nodewatch_cpu_usage_percent gauge")

    host_cpu = host.get("cpu", {})
    runtime_cpu = runtime.get("cpu", {})

    if host_cpu.get("usage_percent") is not None:
        lines.append(f'nodewatch_cpu_usage_percent{{scope="host"}} {host_cpu.get("usage_percent")}')

    if runtime_cpu.get("usage_percent") is not None:
        lines.append(f'nodewatch_cpu_usage_percent{{scope="runtime"}} {runtime_cpu.get("usage_percent")}')

    # --- MEMORY ---
    lines.append("# HELP nodewatch_memory_total_mb Total memory in MB")
    lines.append("# TYPE nodewatch_memory_total_mb gauge")

    host_mem = host.get("memory", {})
    runtime_mem = runtime.get("memory", {})

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

    host_sys = host.get("system", {})
    runtime_sys = runtime.get("system", {})

    if host_sys.get("uptime_seconds") is not None:
        lines.append(f'nodewatch_uptime_seconds{{scope="host"}} {host_sys.get("uptime_seconds")}')

    if runtime_sys.get("uptime_seconds") is not None:
        lines.append(f'nodewatch_uptime_seconds{{scope="runtime"}} {runtime_sys.get("uptime_seconds")}')

    # --- DISK (host only) ---
    lines.append("# HELP nodewatch_disk_used_percent Disk used percentage")
    lines.append("# TYPE nodewatch_disk_used_percent gauge")

    disks = host.get("disk", [])
    for disk in disks:
        device = str(disk.get("device", "")).replace("\\", "\\\\").replace('"', '\\"')
        mountpoint = str(disk.get("mountpoint", "")).replace("\\", "\\\\").replace('"', '\\"')
        value = disk.get("percent_used", 0)

        lines.append(
            f'nodewatch_disk_used_percent{{device="{device}",mountpoint="{mountpoint}"}} {value}'
        )

    return "\n".join(lines) + "\n"