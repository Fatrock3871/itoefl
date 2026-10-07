"""Gera uma versao de TESTE do site, sem login e sem pagamento, em _teste/.

Serve para mostrar a plataforma a alguem por um link publico: a pasta _teste/
pode ser arrastada inteira para um servico de hospedagem estatica.

E o mesmo build de sempre, so que rodado numa copia de app/ sem o
supabase_config.json, o que faz o build.py cair no modo offline (sem tela de
login nem de compra). Nao mexe em artifact/ nem na configuracao real.

    python scripts\\build_teste.py

ATENCAO: quem tiver o link le o curso inteiro de graca. Nao deixe no ar depois
do teste.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_teste"
PAGES = ["index.html", "termos.html", "privacidade.html"]


def main():
    with tempfile.TemporaryDirectory(prefix="itoefl_teste_") as tmp:
        work = Path(tmp)
        for name in ("app", "consolidated", "legal"):
            shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns("__pycache__"))
        (work / "app" / "supabase_config.json").unlink(missing_ok=True)
        (work / "artifact").mkdir()

        subprocess.run(["python", "build_pipeline.py"], cwd=work / "app", check=True)
        subprocess.run(["python", "build.py"], cwd=work / "app", check=True)

        html = (work / "artifact" / "index.html").read_text(encoding="utf-8")
        # o build.py só escreve esta atribuição quando há Supabase configurado
        if "window.ITOEFL_SUPABASE=" in html:
            raise SystemExit("O build de teste saiu com Supabase configurado. Abortando.")

        OUT.mkdir(exist_ok=True)
        for page in PAGES:
            shutil.copyfile(work / "artifact" / page, OUT / page)

    print()
    print(f"Versao de teste (sem login) gerada em: {OUT}")
    for page in PAGES:
        print(f"  {page}: {(OUT / page).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
