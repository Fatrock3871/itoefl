"""Servidor local da plataforma iTOEFL.

Serve a raiz do projeto e abre o site gerado em /artifact/index.html.
O index.html gerado por app/build.py ja tem CSS e JS embutidos, entao
tambem abre por duplo clique; o servidor apenas facilita o recarregar.

    python scripts\\serve.py            # porta 8000, abre o navegador
    python scripts\\serve.py 8080       # outra porta
    python scripts\\serve.py --no-open  # nao abre o navegador
"""

import functools
import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    args = sys.argv[1:]
    should_open = "--no-open" not in args
    ports = [int(a) for a in args if a.isdigit()]
    port = ports[0] if ports else 8000

    handler = functools.partial(Handler, directory=str(ROOT))
    socketserver.TCPServer.allow_reuse_address = True

    try:
        server = socketserver.TCPServer(("127.0.0.1", port), handler)
    except OSError as exc:
        print(f"Nao foi possivel usar a porta {port}: {exc}")
        print(f"Tente outra:  python scripts\\serve.py {port + 1}")
        return 1

    url = f"http://localhost:{port}/artifact/index.html"
    print(f"iTOEFL servindo {ROOT}")
    print(f"  -> {url}")
    print("  Ctrl+C para parar.\n")

    if should_open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
