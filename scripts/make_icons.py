"""Gera os ícones da PWA (app/icons/*.png) a partir da logo definida no build.py.

Roda uma vez, ou de novo se a logo mudar. Os PNGs gerados ficam versionados
em app/icons/ e o build.py só os copia para artifact/.

    python scripts\\make_icons.py

Precisa do Chrome instalado (renderiza o SVG num Chrome headless e tira o
print). Os ícones são "maskable": a flor ocupa a zona segura central (80%),
com fundo na cor do tema claro, para o Android poder recortar em círculo.
"""

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "app"
OUT_DIR = APP_DIR / "icons"

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

# cores do tema claro (app/styles.css, :root)
THEME = {
    "--bg": "#fbf4ea",
    "--accent": "#ef5a1f",
    "--accent-2": "#f7b733",
    "--accent-strong": "#c9430f",
}

SIZES = [192, 512]


def logo_svg():
    """Executa só o trecho do build.py que define LOGO_SVG (o resto do build
    roda no import e precisa dos fragmentos buildados)."""
    src = (APP_DIR / "build.py").read_text(encoding="utf-8")
    m = re.search(r"^_PETAL_COLORS = .*?^LOGO_SVG = \(.*?^\)\n", src, re.S | re.M)
    if not m:
        raise SystemExit("Não achei a definição de LOGO_SVG no build.py")
    ns = {}
    exec(m.group(0), ns)
    svg = ns["LOGO_SVG"]
    for var, hexv in THEME.items():
        svg = svg.replace(f"var({var})", hexv)
    return svg


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c.exists():
            return str(c)
    raise SystemExit("Chrome não encontrado")


def main():
    svg = logo_svg()
    chrome = find_chrome()
    OUT_DIR.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for size in SIZES:
            page = Path(tmp) / f"icon{size}.html"
            page.write_text(
                "<!DOCTYPE html><html><head><style>"
                f"html,body{{margin:0;width:{size}px;height:{size}px;background:{THEME['--bg']};overflow:hidden}}"
                "body{display:flex;align-items:center;justify-content:center}"
                f"svg{{width:{int(size * 0.72)}px;height:{int(size * 0.72)}px}}"
                f"</style></head><body>{svg}</body></html>",
                encoding="utf-8",
            )
            out = OUT_DIR / f"icon-{size}.png"
            subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                 f"--user-data-dir={Path(tmp) / 'profile'}",
                 f"--window-size={size},{size}", f"--screenshot={out}", page.as_uri()],
                check=True, capture_output=True, timeout=60,
            )
            print("gerado", out.relative_to(ROOT), out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
