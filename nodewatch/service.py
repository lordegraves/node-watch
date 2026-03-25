import json
import subprocess
from pathlib import Path

from nodewatch.collectors.system_info import get_system_info
from nodewatch.collectors.cpu import get_cpu_info
from nodewatch.collectors.memory import get_memory_info
from nodewatch.collectors.disk import get_disk_info
from nodewatch.host_info import get_host_uptime_seconds


def run_go_probe():
    project_root = Path(__file__).resolve().parent.parent
    probe_path = project_root / "go-probes" / "system_probe.go"

    try:
        result = subprocess.run(
            ["go", "run", str(probe_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    except FileNotFoundError:
        return {
            "error": "go executable not found"
        }

    except subprocess.CalledProcessError as exc:
        return {
            "error": "go probe execution failed",
            "stderr": exc.stderr.strip(),
            "stdout": exc.stdout.strip(),
    }
    
    except json.JSONDecodeError:
        return {
            "error": "go probe returned invalid JSON",
            "stdout": result.stdout.strip() if "result" in locals() else "",
        }


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
        "go_probe": run_go_probe(),
    }