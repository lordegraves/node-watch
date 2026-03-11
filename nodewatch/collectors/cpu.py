import psutil

def get_cpu_info():
    data = {
        "usage_percent": psutil.cpu_percent(interval=1),
    }

    return data