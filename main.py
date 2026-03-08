from pprint import pprint

from nodewatch.collectors.cpu import collect_cpu
from nodewatch.collectors.system_info import collect_system_info
from nodewatch.collectors.memory import collect_memory
from nodewatch.collectors.disk import collect_disk


def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"


def main():
    print("Node Watch starting...")

    system_info = collect_system_info()
    system_info["uptime"] = format_uptime(system_info["uptime_seconds"])
    disk_info = collect_disk()

    cpu_info = collect_cpu()
    memory_info = collect_memory()

    node_data = {
        "system": system_info,
        "cpu": cpu_info,
        "memory": memory_info,
        "disk": disk_info,
    }

    pprint(node_data)


if __name__ == "__main__":
    main()