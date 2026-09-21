"""Small staging-only TLS terminator for the isolated identity rehearsal.

It routes the two synthetic hostnames to the existing loopback services while
keeping the browser and ERP server-to-server callback on HTTPS. It is not a
production proxy and intentionally accepts only the two configured hosts.
"""

from __future__ import annotations

import argparse
import socket
import socketserver
import ssl
import threading
from pathlib import Path


ROUTES = {
    "staging.example.test": ("127.0.0.1", 13001),
    "erp-staging.example.test": ("127.0.0.1", 28000),
}


class ProxyHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        client = self.request
        client.settimeout(30)
        request = b""
        while b"\r\n\r\n" not in request and len(request) <= 64 * 1024:
            chunk = client.recv(4096)
            if not chunk:
                return
            request += chunk
        header = request.split(b"\r\n\r\n", 1)[0]
        host = ""
        for line in header.split(b"\r\n"):
            if line.lower().startswith(b"host:"):
                host = line.split(b":", 1)[1].strip().decode("ascii", "ignore").split(":", 1)[0].lower()
                break
        upstream_address = ROUTES.get(host)
        if upstream_address is None:
            return
        upstream = socket.create_connection(upstream_address, timeout=30)
        try:
            upstream.sendall(request)
            client.settimeout(None)
            upstream.settimeout(None)
            forward = threading.Thread(target=self._copy, args=(client, upstream), daemon=True)
            forward.start()
            self._copy(upstream, client)
            forward.join(timeout=5)
        finally:
            upstream.close()

    @staticmethod
    def _copy(source: socket.socket, target: socket.socket) -> None:
        try:
            while True:
                data = source.recv(64 * 1024)
                if not data:
                    break
                target.sendall(data)
        except (ConnectionError, OSError):
            pass


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--cert", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=str(Path(args.cert)), keyfile=str(Path(args.key)))
    with ThreadedServer((args.listen, args.port), ProxyHandler) as server:
        server.socket = context.wrap_socket(server.socket, server_side=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
