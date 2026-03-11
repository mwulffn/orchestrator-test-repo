"""Simple HTTP request logger server.

Starts a local HTTP server that logs every incoming request to stdout and
responds with 200 OK containing the request details.
"""

import argparse
import socket
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# errno values for "address already in use" across Linux, macOS, Windows
_ADDR_IN_USE = {98, 48, 10048}


class LoggingHandler(BaseHTTPRequestHandler):
    """HTTP request handler that logs requests and echoes details back."""

    def handle_request(self) -> None:
        """Handle any HTTP method: log it and echo the request details."""
        start = time.monotonic()

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""

        lines = [
            f"Method: {self.command}",
            f"Path: {self.path}",
            f"HTTP-Version: {self.request_version}",
            "",
            "Headers:",
        ]
        for key, value in self.headers.items():
            lines.append(f"  {key}: {value}")

        if body:
            lines += ["", "Body:", f"  {body.decode('utf-8', errors='replace')}"]

        response_body = "\n".join(lines).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {self.command} {self.path} 200 {elapsed_ms}ms", flush=True)

    # Map common HTTP methods to handle_request.
    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request
    do_PATCH = handle_request
    do_DELETE = handle_request
    do_HEAD = handle_request
    do_OPTIONS = handle_request

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        """Suppress the default BaseHTTPRequestHandler access log."""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Start a local HTTP server that logs every incoming request."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="TCP port to listen on (default: 8080)",
    )
    args = parser.parse_args()

    try:
        server = HTTPServer(("", args.port), LoggingHandler)
    except OSError as exc:
        if exc.errno in _ADDR_IN_USE:
            print(
                f"Error: port {args.port} is already in use. "
                "Choose a different port with --port.",
                file=sys.stderr,
            )
            sys.exit(1)
        raise

    host = socket.gethostname()
    print(f"Listening on http://{host}:{args.port}  (Ctrl+C to stop)")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
