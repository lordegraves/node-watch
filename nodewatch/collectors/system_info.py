import platform
import socket
import time

import psutil

def collect_system_info():
    data = {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
    }

    return data