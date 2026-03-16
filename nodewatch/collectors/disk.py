import psutil

IGNORED_MOUNTS = {
    "/etc/hosts",
    "/etc/hostname",
    "/etc/resolv.conf",
    "/dev/termination-log",
    "/host/etc/hosts",
    "/host/etc/hostname",
    "/host/etc/resolv.conf",
}


def get_disk_info():
    disks = []

    for partition in psutil.disk_partitions():
        mount = partition.mountpoint

        if mount in IGNORED_MOUNTS:
            continue

        try:
            usage = psutil.disk_usage(mount)
        except PermissionError:
            continue

        disk_info = {
            "device": partition.device,
            "mountpoint": mount,
            "total_gb": round(usage.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(usage.used / 1024 / 1024 / 1024, 2),
            "percent_used": usage.percent,
        }

        disks.append(disk_info)

    return disks