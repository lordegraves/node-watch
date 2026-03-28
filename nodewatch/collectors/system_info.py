import platform
import socket
import time
from pathlib import Path

import psutil

from nodewatch.collectors.host_info import get_host_uptime_seconds


HOST_ROOT = Path("/host")


def _read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        return None


def get_runtime_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
    }


def get_host_system_info():
    hostname = _read_text(HOST_ROOT / "etc" / "hostname")
    if not hostname:
        hostname = _read_text(HOST_ROOT / "proc" / "sys" / "kernel" / "hostname")

    os_name = None
    os_release = _read_text(HOST_ROOT / "etc" / "os-release")
    if os_release:
        values = {}
        for line in os_release.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
        os_name = values.get("PRETTY_NAME") or values.get("NAME")

    uptime_seconds = get_host_uptime_seconds()

    return {
        "hostname": hostname,
        "os": os_name,
        "uptime_seconds": uptime_seconds,
    }