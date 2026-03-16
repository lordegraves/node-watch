# nodewatch/metrics.py
from nodewatch.service import get_node_data


def render_prometheus_metrics() -> str:
    node_data = get_node_data()
    lines = []

    cpu = node_data.get("cpu", {})
    memory = node_data.get("memory", {})
    system = node_data.get("system", {})
    disks = node_data.get("disk", [])

    lines.append("# HELP nodewatch_cpu_usage_percent CPU usage percentage")
    lines.append("# TYPE nodewatch_cpu_usage_percent gauge")
    lines.append(f"nodewatch_cpu_usage_percent {cpu.get('usage_percent', 0)}")

    lines.append("# HELP nodewatch_memory_total_mb Total memory in MB")
    lines.append("# TYPE nodewatch_memory_total_mb gauge")
    lines.append(f"nodewatch_memory_total_mb {memory.get('total_mb', 0)}")

    lines.append("# HELP nodewatch_memory_used_mb Used memory in MB")
    lines.append("# TYPE nodewatch_memory_used_mb gauge")
    lines.append(f"nodewatch_memory_used_mb {memory.get('used_mb', 0)}")

    lines.append("# HELP nodewatch_memory_percent_used Memory used percentage")
    lines.append("# TYPE nodewatch_memory_percent_used gauge")
    lines.append(f"nodewatch_memory_percent_used {memory.get('percent_used', 0)}")

    lines.append("# HELP nodewatch_uptime_seconds Container/system uptime in seconds")
    lines.append("# TYPE nodewatch_uptime_seconds gauge")
    lines.append(f"nodewatch_uptime_seconds {system.get('uptime_seconds', 0)}")

    lines.append("# HELP nodewatch_host_uptime_seconds Host uptime in seconds")
    lines.append("# TYPE nodewatch_host_uptime_seconds gauge")
    host_uptime = system.get("host_uptime_seconds")
    if host_uptime is not None:
        lines.append(f"nodewatch_host_uptime_seconds {host_uptime}")

    lines.append("# HELP nodewatch_disk_used_percent Disk used percentage")
    lines.append("# TYPE nodewatch_disk_used_percent gauge")
    for disk in disks:
        device = str(disk.get("device", "")).replace("\\", "\\\\").replace('"', '\\"')
        mountpoint = str(disk.get("mountpoint", "")).replace("\\", "\\\\").replace('"', '\\"')
        value = disk.get("percent_used", 0)
        lines.append(
            f'nodewatch_disk_used_percent{{device="{device}",mountpoint="{mountpoint}"}} {value}'
        )

    return "\n".join(lines) + "\n"