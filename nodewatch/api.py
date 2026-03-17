import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from nodewatch.metrics import render_prometheus_metrics
from nodewatch.service import get_node_data
from nodewatch.logging import get_logger

logger = get_logger()

HOST = os.getenv("NODEWATCH_HOST", "0.0.0.0")


def get_port() -> int:
    value = os.getenv("NODEWATCH_PORT", "8080")
    try:
        return int(value)
    except ValueError:
        return 8080


def get_log_level() -> str:
    return os.getenv("NODEWATCH_LOG_LEVEL", "info").lower()


class NodeWatchHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        response_body = json.dumps(payload, indent=2).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def _send_text(self, status_code: int, payload: str) -> None:
        response_body = payload.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_request_event(self, path: str, status: int) -> None:
        logger.info(
            "request",
            extra={
                "extra": {
                    "path": path,
                    "status": status,
                    "client": self.client_address[0],
                }
            },
        )

    def log_message(self, format, *args):
        return

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_json(
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
            self.log_request_event("/", 200)
            return

        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            self.log_request_event("/health", 200)
            return

        if self.path == "/node":
            node_data = get_node_data()
            self._send_json(200, node_data)
            self.log_request_event("/node", 200)
            return

        if self.path == "/metrics":
            metrics_output = render_prometheus_metrics()
            self._send_text(200, metrics_output)
            self.log_request_event("/metrics", 200)
            return

        self._send_json(404, {"error": "not found"})
        self.log_request_event(self.path, 404)


def run_server() -> None:
    port = get_port()
    server = HTTPServer((HOST, port), NodeWatchHandler)

    logger.info(
        "nodewatch listening",
        extra={
            "extra": {
                "host": HOST,
                "port": port,
            }
        },
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("nodewatch shutting down")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()