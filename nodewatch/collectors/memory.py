import psutil

def get_memory_info():
    memory = psutil.virtual_memory()

    data = {
        "total_mb": round(memory.total / 1024 / 1024,  2),
        "used_mb": round(memory.used / 1024 / 1024, 2),
        "percent_used": memory.percent,
    }

    return data