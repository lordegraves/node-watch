from nodewatch.collectors.system_info import get_system_info
from nodewatch.collectors.cpu import get_cpu_info
from nodewatch.collectors.memory import get_memory_info
from nodewatch.collectors.disk import get_disk_info
from nodewatch.host_info import get_host_uptime_seconds


def get_node_data():
    system = get_system_info()

    host_uptime = get_host_uptime_seconds()
    if host_uptime is not None:
        system["host_uptime_seconds"] = host_uptime

    return {
        "system": system,
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
    }