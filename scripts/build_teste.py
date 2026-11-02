"""Gera uma versao de TESTE do site, sem login e sem pagamento, em _teste/.

Serve para mostrar a plataforma a alguem por um link publico: a pasta _teste/
pode ser arrastada inteira para um servico de hospedagem estatica.

E o mesmo build de sempre, so que rodado numa copia de app/ sem o
supabase_config.json, o que faz o build.py cair no modo offline (sem tela de
login nem de compra). Nao mexe em artifact/ nem na configuracao real.

A pasta sai completa, com manifesto, service worker e icones: servida por
https, a versao de teste tambem e instalavel e abre offline, igual ao site.

    python scripts\\build_teste.py

ATENCAO: quem tiver o link le o curso inteiro de graca. Nao deixe no ar depois
do teste.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_teste"
PAGES = ["index.html", "termos.html", "privacidade.html"]


def build(out=OUT):
    """Builda a versao sem login e grava em `out` tudo que o build.py gerou."""
    out = Path(out)
    with tempfile.TemporaryDirectory(prefix="itoefl_teste_") as tmp:
        work = Path(tmp)
        # supabase/functions/_shared: o build cola as regras de redação de lá
        for name in ("app", "consolidated", "legal", "supabase/functions/_shared"):
            shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns("__pycache__"))
        (work / "app" / "supabase_config.json").unlink(missing_ok=True)
        (work / "artifact").mkdir()

        # sys.executable, e nao "python": o do PATH pode ser outro
        # interpretador, sem o pacote markdown
        # o build.py também lê SUPABASE_URL e SUPABASE_PUBLISHABLE_KEY do
        # ambiente (CI): sem tirá-las, esta cópia sairia com login
        env = {k: v for k, v in os.environ.items() if k not in ("SUPABASE_URL", "SUPABASE_PUBLISHABLE_KEY")}
        for script in ("build_pipeline.py", "build.py"):
            subprocess.run([sys.executable, script], cwd=work / "app", check=True, capture_output=True, env=env)

        html = (work / "artifact" / "index.html").read_text(encoding="utf-8")
        # o build.py só escreve esta atribuição quando há Supabase configurado
        if "window.ITOEFL_SUPABASE=" in html:
            raise SystemExit("O build de teste saiu com Supabase configurado. Abortando.")

        # a pasta inteira, e nao so as paginas: sem manifest.json, sw.js e
        # icons/ o site nao instala nem abre offline. Copia por cima em vez
        # de apagar a pasta antes: dentro do OneDrive o Windows nega o rmdir.
        shutil.copytree(work / "artifact", out, dirs_exist_ok=True)
    return out


def main():
    out = build()
    print()
    print(f"Versao de teste (sem login) gerada em: {out}")
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        print(f"  {path.relative_to(out).as_posix()}: {max(1, path.stat().st_size // 1024)} KB")


if __name__ == "__main__":
    main()
