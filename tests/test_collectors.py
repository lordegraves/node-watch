from nodewatch.collectors.cpu import (
    get_runtime_cpu_info,
    get_host_cpu_info,
)
from nodewatch.collectors.disk import (
    get_runtime_disk_info,
    get_host_disk_info,
)
from nodewatch.collectors.memory import (
    get_runtime_memory_info,
    get_host_memory_info,
)
from nodewatch.collectors.system_info import (
    get_runtime_system_info,
    get_host_system_info,
)


def test_runtime_system_info_returns_expected_keys():
    data = get_runtime_system_info()

    assert "hostname" in data
    assert "os" in data
    assert "uptime_seconds" in data


def test_host_system_info_returns_expected_keys():
    data = get_host_system_info()

    assert "hostname" in data
    assert "os" in data
    assert "uptime_seconds" in data


def test_runtime_cpu_returns_expected_key():
    data = get_runtime_cpu_info()

    assert "usage_percent" in data


def test_host_cpu_returns_expected_key_or_error():
    data = get_host_cpu_info()

    if "error" in data:
        assert isinstance(data["error"], str)
    else:
        assert "usage_percent" in data


def test_runtime_memory_returns_expected_keys():
    data = get_runtime_memory_info()

    assert "total_mb" in data
    assert "used_mb" in data
    assert "percent_used" in data


def test_host_memory_returns_expected_keys_or_error():
    data = get_host_memory_info()

    if "error" in data:
        assert isinstance(data["error"], str)
    else:
        assert "total_mb" in data
        assert "used_mb" in data
        assert "percent_used" in data


def test_runtime_disk_returns_list():
    data = get_runtime_disk_info()

    if data:
        first_disk = data[0]

        assert "device" in first_disk
        assert "mountpoint" in first_disk
        assert "total_gb" in first_disk
        assert "used_gb" in first_disk
        assert "percent_used" in first_disk


def test_host_disk_returns_list_or_error():
    data = get_host_disk_info()

    if isinstance(data, dict) and "error" in data:
        assert isinstance(data["error"], str)
    elif data:
        first_disk = data[0]

        assert "device" in first_disk
        assert "mountpoint" in first_disk
        assert "total_gb" in first_disk
        assert "used_gb" in first_disk
        assert "percent_used" in first_disk