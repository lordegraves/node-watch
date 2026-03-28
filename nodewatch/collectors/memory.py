import psutil
from pathlib import Path


HOST_ROOT = Path("/host")


def get_runtime_memory_info():
    memory = psutil.virtual_memory()

    return {
        "total_mb": round(memory.total / 1024 / 1024, 2),
        "used_mb": round(memory.used / 1024 / 1024, 2),
        "percent_used": memory.percent,
    }


def get_host_memory_info():
    meminfo_path = HOST_ROOT / "proc" / "meminfo"

    try:
        with open(meminfo_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return {
            "error": "host meminfo not available"
        }

    values = {}

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue

        key = parts[0].rstrip(":")
        try:
            values[key] = int(parts[1])
        except ValueError:
            continue

    total_kb = values.get("MemTotal")
    available_kb = values.get("MemAvailable")

    if not total_kb or available_kb is None:
        return {
            "error": "required host memory fields missing"
        }

    used_kb = total_kb - available_kb

    total_mb = round(total_kb / 1024, 2)
    used_mb = round(used_kb / 1024, 2)
    percent_used = round((used_kb / total_kb) * 100, 1)

    return {
        "total_mb": total_mb,
        "used_mb": used_mb,
        "percent_used": percent_used,
    }