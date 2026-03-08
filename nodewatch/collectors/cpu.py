import psutil

def collect_cpu():
    data = {
        "usage_percent": psutil.cpu_percent(interval=1),
    }

    return data