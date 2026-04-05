from pathlib import Path

import psutil

IGNORED_RUNTIME_MOUNTS = {
    "/etc/hosts",
    "/etc/hostname",
    "/etc/resolv.conf",
    "/dev/termination-log",
}

IGNORED_HOST_MOUNTS = {
    "/host/etc/hosts",
    "/host/etc/hostname",
    "/host/etc/resolv.conf",
}

HOST_ROOT = Path("/host")


def _build_disk_info(partition, usage):
    return {
        "device": partition.device,
        "mountpoint": partition.mountpoint,
        "total_gb": round(usage.total / 1024 / 1024 / 1024, 2),
        "used_gb": round(usage.used / 1024 / 1024 / 1024, 2),
        "percent_used": usage.percent,
    }


def get_runtime_disk_info():
    disks = []

    for partition in psutil.disk_partitions():
        mount = partition.mountpoint

        if mount in IGNORED_RUNTIME_MOUNTS:
            continue

        if mount.startswith("/host"):
            continue

        try:
            usage = psutil.disk_usage(mount)
        except PermissionError:
            continue

        disks.append(_build_disk_info(partition, usage))

    return disks


def get_host_disk_info():
    disks = []

    if not HOST_ROOT.exists():
        return []

    for partition in psutil.disk_partitions():
        mount = partition.mountpoint

        if not mount.startswith("/host"):
            continue

        if mount in IGNORED_HOST_MOUNTS:
            continue

        try:
            usage = psutil.disk_usage(mount)
        except PermissionError:
            continue

        disks.append(_build_disk_info(partition, usage))

    return disks