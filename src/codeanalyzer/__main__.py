"""Entry point: serve the local-only web UI on 127.0.0.1.

Run with ``python -m codeanalyzer`` (or the ``codeanalyzer`` console script). The host is
fixed to 127.0.0.1 to preserve the local-only guarantee; only the port is configurable.
"""

from __future__ import annotations

import logging
import os
import socket
import webbrowser

from .web import create_app

HOST = "127.0.0.1"


def _resolve_port(preferred: int) -> int:
    """Return *preferred* if free, otherwise the next open port (so a busy 5000 from a
    previous run doesn't crash startup). Falls back to an OS-assigned port."""
    for candidate in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex((HOST, candidate)) != 0:  # nothing listening -> free
                return candidate
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return int(sock.getsockname()[1])


def main() -> None:
    preferred = int(os.environ.get("CODEANALYZER_PORT", "5000"))
    port = _resolve_port(preferred)
    if port != preferred:
        print(f"Port {preferred} is busy; using {port} instead.")
    app = create_app()
    base = f"http://{HOST}:{port}"
    # The access token (see web.server) must be presented on first load; bake it into the
    # URL we print and open so the user lands authenticated. Disabled => plain URL.
    token = app.config.get("ACCESS_TOKEN")
    url = base if os.environ.get("CODEANALYZER_NO_AUTH") == "1" else f"{base}/?t={token}"
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    print(f"codeAnalyzer running at {url}  (Ctrl+C to stop)")
    if os.environ.get("CODEANALYZER_NO_BROWSER") != "1":
        try:
            webbrowser.open(url)
        except Exception:  # noqa: BLE001 - opening a browser is best-effort
            pass
    app.run(host=HOST, port=port, debug=False)


if __name__ == "__main__":
    main()
