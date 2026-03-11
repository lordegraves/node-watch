from nodewatch.collectors.system_info import get_system_info
from nodewatch.collectors.cpu import get_cpu_info
from nodewatch.collectors.memory import get_memory_info
from nodewatch.collectors.disk import get_disk_info


def get_node_data():
    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
    }