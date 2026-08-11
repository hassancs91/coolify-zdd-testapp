"""zdd-testapp: deliberately tiny HTTP app for measuring Coolify deployment downtime.

Env knobs:
  APP_VERSION      string shown in every response body (default "v1") so the outside
                   probe can see WHICH build answered
  STARTUP_DELAY_S  seconds to sleep BEFORE binding the port (default 0) - simulates a
                   real app that boots slow (migrations, JIT warmup, big framework)
  GRACEFUL         "1" = catch SIGTERM, finish in-flight requests, then exit cleanly
                   (default "0" = die on SIGTERM like most unconfigured apps)
"""
import os
import signal
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "v1")
DELAY = float(os.environ.get("STARTUP_DELAY_S", "0"))
GRACEFUL = os.environ.get("GRACEFUL", "0") == "1"
STARTED = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
PID = os.getpid()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path.startswith("/health"):
            body = b"ok"
        else:
            body = f"zdd-testapp {VERSION} pid={PID} started={STARTED}".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    if DELAY:
        print(f"[app] sleeping {DELAY}s before binding port (simulated slow boot)", flush=True)
        time.sleep(DELAY)
    srv = ThreadingHTTPServer(("0.0.0.0", 3000), Handler)
    print(f"[app] {VERSION} pid={PID} listening on :3000 graceful={GRACEFUL}", flush=True)
    if GRACEFUL:
        def term(_sig, _frame):
            print("[app] SIGTERM: draining, finishing in-flight requests", flush=True)
            threading.Thread(target=srv.shutdown).start()
        signal.signal(signal.SIGTERM, term)
    srv.serve_forever()
    print("[app] stopped cleanly", flush=True)


if __name__ == "__main__":
    main()
