import psutil

def get_disk_info():
    disks = []

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)

        disk_info = {
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "total_gb": round(usage.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(usage.used / 1024 / 1024 / 1024, 2),
            "percent_used": usage.percent,
        }

        disks.append(disk_info)

    return disks