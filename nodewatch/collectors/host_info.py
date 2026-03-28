from pathlib import Path


HOST_ROOT = Path("/host")


def get_host_uptime_seconds() -> float | None:
    uptime_path = HOST_ROOT / "proc" / "uptime"

    try:
        content = uptime_path.read_text(encoding="utf-8").strip()
        return float(content.split()[0])
    except (FileNotFoundError, ValueError, OSError, IndexError):
        return None