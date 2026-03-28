import psutil
from pathlib import Path


HOST_ROOT = Path("/host")

_prev_total = None
_prev_idle = None


def get_runtime_cpu_info():
    return {
        "usage_percent": psutil.cpu_percent(interval=1),
    }


def get_host_cpu_info():
    global _prev_total, _prev_idle

    stat_path = HOST_ROOT / "proc" / "stat"

    try:
        with open(stat_path, "r") as f:
            first_line = f.readline()
    except FileNotFoundError:
        return {
            "error": "host cpu stat not available"
        }

    parts = first_line.split()

    if len(parts) < 5 or parts[0] != "cpu":
        return {
            "error": "invalid host cpu stat format"
        }

    try:
        values = [int(x) for x in parts[1:]]
    except ValueError:
        return {
            "error": "invalid cpu stat values"
        }

    idle = values[3]
    total = sum(values)

    # First sample — can't calculate yet
    if _prev_total is None or _prev_idle is None:
        _prev_total = total
        _prev_idle = idle
        return {
            "usage_percent": None,
            "note": "requires second sample"
        }

    total_delta = total - _prev_total
    idle_delta = idle - _prev_idle

    _prev_total = total
    _prev_idle = idle

    if total_delta <= 0:
        return {
            "usage_percent": 0.0
        }

    usage_percent = (1 - (idle_delta / total_delta)) * 100

    return {
        "usage_percent": round(usage_percent, 1)
    }