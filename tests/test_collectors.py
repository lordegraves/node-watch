from nodewatch.collectors.cpu import collect_cpu
from nodewatch.collectors.disk import collect_disk
from nodewatch.collectors.memory import collect_memory
from nodewatch.collectors.system_info import collect_system_info

def test_collect_system_info_returns_expected_keys():
    data = collect_system_info()

    assert "hostname" in data
    assert "os" in data
    assert "uptime_seconds" in data


def test_collect_cpu_returns_expected_key():
    data = collect_cpu()

    assert "usage_percent" in data


def test_collect_memory_returns_expected_keys():
    data = collect_memory()

    assert "total_mb" in data
    assert "used_mb" in data
    assert "percent_used" in data


def test_collect_disk_returns_list():
    data = collect_disk()

    if data:
        first_disk = data[0]

        assert "device" in first_disk
        assert "mountpoint" in first_disk
        assert "total_gb" in first_disk
        assert "used_gb" in first_disk
        assert "percent_used" in first_disk
