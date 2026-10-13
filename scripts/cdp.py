"""Cliente minimo do Chrome DevTools Protocol, so com a biblioteca padrao.

O smoke test injeta um script e le o resultado por --dump-dom, o que nao
permite recarregar a pagina, mudar o tamanho da tela nem esperar um service
worker. Este modulo abre um Chrome headless com porta de depuracao e conversa
com ele por WebSocket, para os testes que precisam disso.

    from cdp import Browser
    with Browser() as b:
        b.viewport(375, 812, mobile=True)
        b.goto("http://127.0.0.1:8765/index.html")
        print(b.eval("document.title"))

Sem dependencia nova: socket, struct e json. Nao e um cliente completo, so o
que os testes do projeto usam.
"""

import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def find_chrome():
    for path in CHROME_CANDIDATES:
        if path.exists():
            return str(path)
    raise SystemExit("Chrome nao encontrado nos caminhos esperados. Ajuste CHROME_CANDIDATES em scripts/cdp.py.")


class _WebSocket:
    """WebSocket de cliente: handshake, frames de texto mascarados, ping/pong."""

    def __init__(self, url):
        rest = url.split("://", 1)[1]
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=30)
        key = base64.b64encode(os.urandom(16)).decode()
        # sem cabecalho Origin de proposito: o Chrome recusa origem desconhecida
        self.sock.sendall((
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        ).encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("handshake do WebSocket interrompido")
            buf += chunk
        if b" 101 " not in buf.split(b"\r\n", 1)[0]:
            raise ConnectionError("handshake do WebSocket recusado: " + buf[:120].decode(errors="replace"))
        self.buf = buf.split(b"\r\n\r\n", 1)[1]

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("WebSocket fechado pelo Chrome")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _frame(self, opcode, payload):
        head = bytes([0x80 | opcode])
        n = len(payload)
        if n < 126:
            head += bytes([0x80 | n])
        elif n < 65536:
            head += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            head += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        body = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(head + mask + body)

    def send(self, text):
        self._frame(0x1, text.encode("utf-8"))

    def recv(self, timeout):
        """Devolve a proxima mensagem de texto, ou None se o prazo estourar."""
        self.sock.settimeout(timeout)
        parts = []
        try:
            while True:
                b1, b2 = self._read(2)
                opcode, n = b1 & 0x0F, b2 & 0x7F
                if n == 126:
                    n = struct.unpack(">H", self._read(2))[0]
                elif n == 127:
                    n = struct.unpack(">Q", self._read(8))[0]
                payload = self._read(n)
                if opcode == 0x9:      # ping
                    self._frame(0xA, payload)
                    continue
                if opcode == 0x8:      # close
                    raise ConnectionError("WebSocket fechado pelo Chrome")
                if opcode in (0x0, 0x1, 0x2):
                    parts.append(payload)
                    if b1 & 0x80:
                        return b"".join(parts).decode("utf-8", errors="replace")
        except socket.timeout:
            return None

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class Browser:
    """Um Chrome headless com uma aba. Usar com `with`."""

    def __init__(self, width=1280, height=900):
        self.profile = Path(tempfile.mkdtemp(prefix="itoefl_cdp_"))
        self.proc = subprocess.Popen(
            [find_chrome(), "--headless=new", "--disable-gpu", "--remote-debugging-port=0",
             f"--user-data-dir={self.profile}", f"--window-size={width},{height}",
             "--no-first-run", "--no-default-browser-check", "--mute-audio", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        port_file = self.profile / "DevToolsActivePort"
        deadline = time.time() + 30
        def read_port():
            # no Windows o arquivo pode existir e ainda estar travado pelo
            # Chrome, que o está escrevendo: tentar de novo em vez de cair
            try:
                return port_file.read_text().strip()
            except OSError:
                return ""

        port_text = read_port()
        while not port_text:
            if time.time() > deadline:
                self.close()
                raise SystemExit("Chrome nao abriu a porta de depuracao em 30 s.")
            time.sleep(0.1)
            port_text = read_port()
        self.port = int(port_text.split()[0])
        targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/list").read())
        page = [t for t in targets if t.get("type") == "page"][0]
        self.ws = _WebSocket(page["webSocketDebuggerUrl"])
        self._id = 0
        self.events = []
        self.errors = []     # excecoes de JS e console.error vistos ate agora
        for domain in ("Page", "Runtime", "Log", "Network"):
            self.call(domain + ".enable")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        try:
            self.ws.close()
        except AttributeError:
            pass
        self.proc.terminate()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)

    def _note(self, msg):
        method, params = msg.get("method"), msg.get("params", {})
        if method == "Runtime.exceptionThrown":
            d = params.get("exceptionDetails", {})
            text = (d.get("exception") or {}).get("description") or d.get("text") or "excecao"
            self.errors.append(text.splitlines()[0])
        elif method == "Runtime.consoleAPICalled" and params.get("type") == "error":
            self.errors.append("console.error: " + " ".join(str(a.get("value", a.get("description", ""))) for a in params.get("args", [])))
        elif method == "Log.entryAdded" and params.get("entry", {}).get("level") == "error":
            e = params["entry"]
            self.errors.append("log: " + e.get("text", "") + " " + e.get("url", ""))
        self.events.append(msg)

    def call(self, method, params=None, timeout=60):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            raw = self.ws.recv(max(0.1, deadline - time.time()))
            if raw is None:
                continue
            msg = json.loads(raw)
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})
            self._note(msg)
        raise TimeoutError(method)

    def pump(self, seconds):
        """Le eventos por um tempo (deixa a pagina trabalhar)."""
        deadline = time.time() + seconds
        while time.time() < deadline:
            raw = self.ws.recv(max(0.05, deadline - time.time()))
            if raw is not None:
                self._note(json.loads(raw))

    def wait_event(self, name, timeout=30):
        deadline = time.time() + timeout
        seen = len(self.events)
        while time.time() < deadline:
            for msg in self.events[seen:]:
                if msg.get("method") == name:
                    return msg
            seen = len(self.events)
            raw = self.ws.recv(0.2)
            if raw is not None:
                self._note(json.loads(raw))
        raise TimeoutError(name)

    def goto(self, url, settle=0.5):
        mark = len(self.events)
        self.call("Page.navigate", {"url": url})
        self._wait_load(mark)
        self.pump(settle)

    def reload(self, settle=0.5):
        mark = len(self.events)
        self.call("Page.reload")
        self._wait_load(mark)
        self.pump(settle)

    def _wait_load(self, mark, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if any(m.get("method") == "Page.loadEventFired" for m in self.events[mark:]):
                return
            raw = self.ws.recv(0.2)
            if raw is not None:
                self._note(json.loads(raw))
        raise TimeoutError("a pagina nao terminou de carregar")

    def eval(self, expression, timeout=60):
        """Avalia JS e devolve o valor (JSON). Espera Promise."""
        res = self.call("Runtime.evaluate", {
            "expression": expression, "returnByValue": True, "awaitPromise": True, "userGesture": True,
        }, timeout=timeout)
        if "exceptionDetails" in res:
            d = res["exceptionDetails"]
            raise RuntimeError((d.get("exception") or {}).get("description") or d.get("text"))
        return res.get("result", {}).get("value")

    def wait_for(self, expression, timeout=20, step=0.2):
        """Espera a expressao JS ficar verdadeira. Devolve False se o prazo estourar."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            # no meio de uma navegacao a pagina ainda nao tem documento e a
            # expressao estoura: conta como "ainda nao" e tenta de novo
            try:
                if self.eval(expression):
                    return True
            except RuntimeError:
                pass
            self.pump(step)
        return False

    def set_files(self, selector, paths):
        """Escolhe arquivos num <input type=file>, como o aluno faria."""
        res = self.call("Runtime.evaluate", {"expression": f"document.querySelector({json.dumps(selector)})"})
        self.call("DOM.setFileInputFiles", {"files": [str(p) for p in paths], "objectId": res["result"]["objectId"]})

    def viewport(self, width, height, mobile=False, scale=1):
        self.call("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height, "deviceScaleFactor": scale, "mobile": mobile,
        })
        if mobile:
            self.call("Emulation.setTouchEmulationEnabled", {"enabled": True})

    def offline(self, on):
        self.call("Network.emulateNetworkConditions", {
            "offline": bool(on), "latency": 0, "downloadThroughput": -1, "uploadThroughput": -1,
        })

    def screenshot(self, path, full=False):
        res = self.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": bool(full)})
        Path(path).write_bytes(base64.b64decode(res["data"]))
