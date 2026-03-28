import json
import platform
import subprocess
from pathlib import Path

from nodewatch.collectors.system_info import (
    get_host_system_info,
    get_runtime_system_info,
)
from nodewatch.collectors.cpu import (
    get_host_cpu_info,
    get_runtime_cpu_info,
)
from nodewatch.collectors.memory import (
    get_host_memory_info,
    get_runtime_memory_info,
)
from nodewatch.collectors.disk import (
    get_host_disk_info,
    get_runtime_disk_info,
)


def run_go_probe(probe_filename):
    project_root = Path(__file__).resolve().parent.parent
    bin_dir = project_root / "bin"

    if platform.system().lower() == "windows":
        probe_path = bin_dir / f"{probe_filename}.exe"
    else:
        probe_path = bin_dir / probe_filename

    try:
        result = subprocess.run(
            [str(probe_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    except FileNotFoundError:
        return {
            "error": "go probe executable not found"
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
            "stdout": result.stdout.strip(),
        }


def get_node_data():
    system_probe_data = run_go_probe("system_probe")
    memory_probe_data = run_go_probe("memory_probe")

    return {
        "host": {
            "system": get_host_system_info(),
            "cpu": get_host_cpu_info(),
            "memory": get_host_memory_info(),
            "disk": get_host_disk_info(),
            "go_probe": {
                "system_probe": system_probe_data.get("system_probe", system_probe_data),
                "memory_probe": memory_probe_data.get("memory_probe", memory_probe_data),
            },
        },
        "runtime": {
            "system": get_runtime_system_info(),
            "cpu": get_runtime_cpu_info(),
            "memory": get_runtime_memory_info(),
            "disk": get_runtime_disk_info(),
        },
    }