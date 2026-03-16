from unittest.mock import patch

from nodewatch.api import NodeWatchHandler


def make_handler(path):
    handler = NodeWatchHandler.__new__(NodeWatchHandler)
    handler.path = path
    handler.log_message = lambda format, *args: None
    return handler


def test_root_endpoint_returns_service_info():
    handler = make_handler("/")

    with patch.object(handler, "_send_json") as mock_send_json:
        handler.do_GET()

    mock_send_json.assert_called_once_with(
        200,
        {
        "service": "node-watch",
        "version": "0.1.0",
        "description": "Lightweight node telemetry service",
        "endpoints": [
            "/",
            "/health",
            "/node",
            "/metrics",
            ],
        },
    )


def test_health_endpoint_returns_ok():
    handler = make_handler("/health")

    with patch.object(handler, "_send_json") as mock_send_json:
        handler.do_GET()

    mock_send_json.assert_called_once_with(200, {"status": "ok"})


@patch("nodewatch.api.get_node_data")
def test_node_endpoint_returns_telemetry(mock_get_node_data):
    mock_get_node_data.return_value = {
        "system": {"hostname": "test-node"},
        "cpu": {"usage_percent": 10.5},
        "memory": {"percent_used": 42.0},
        "disk": [],
    }

    handler = make_handler("/node")

    with patch.object(handler, "_send_json") as mock_send_json:
        handler.do_GET()

    mock_send_json.assert_called_once_with(200, mock_get_node_data.return_value)


def test_unknown_route_returns_404():
    handler = make_handler("/does-not-exist")

    with patch.object(handler, "_send_json") as mock_send_json:
        handler.do_GET()

    mock_send_json.assert_called_once_with(404, {"error": "not found"})