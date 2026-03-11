import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from nodewatch.service import get_node_data


class NodeRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/node":
            node_data = get_node_data()
            response_body = json.dumps(node_data, indent=2).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
            return
        
        not_found = json.dumps({"error": "not found"}).encode("utf-8")
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(not_found)))
        self.end_headers()
        self.wfile.write(not_found)

    def log_message(self, format, *args):
        return
    
def run_server(host = "localhost", port=8080):
    server = HTTPServer((host, port), NodeRequestHandler)
    print(f"Node Watch API listening on HTTP://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()