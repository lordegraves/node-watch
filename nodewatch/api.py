import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from nodewatch.service import get_node_data


HOST = "0.0.0.0"
PORT = 8080


class NodeWatchHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        response_body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

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
                    ]
                }
            )
            return
        
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        
        if self.path == "/node":
            node_data = get_node_data()
            self._send_json(200, node_data)
            return
        
        self._send_json(404, {"error": "not found"})

    
def run_server() -> None:
    server = HTTPServer((HOST, PORT), NodeWatchHandler)
    print(f"Node Watch API listening on HTTP://{HOST}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Node Watch API...")
        server.server_close()

if __name__ == "__main__":
    run_server()