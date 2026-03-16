from pathlib import Path


def get_host_uptime_seconds() -> float | None:
    uptime_path = Path("/host/proc/uptime")
    if not uptime_path.exists():
        return None
    
    try:
        content = uptime_path.read_text(encoding="utf-8").strip()
        return float(content.split()[0])
    except (ValueError, OSError, IndexError):
        return None