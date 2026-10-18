"""Checagem antes de publicar o site.

    python scripts\\prepublish_check.py            # tudo, inclusive o smoke test
    python scripts\\prepublish_check.py --sem-smoke

Reprova (saida 1) se:
  - legal/*.md ainda tem campo [PREENCHER: ...];
  - SITE_URL (app/site.json ou variavel de ambiente) e localhost ou nao e https;
  - app/supabase_config.json tem chave secreta (sb_secret_... ou JWT service_role);
  - ha credencial de teste do Mercado Pago (TEST-...) no app, no artifact ou
    na variavel de ambiente MP_ACCESS_TOKEN. O token de verdade mora nos
    secrets do Supabase, que este script nao le: conferir la a mao
    (docs/publicar.md);
  - o smoke test falha.

O smoke test chama problems(run_smoke=False) no fim e mostra o resultado so
como aviso: durante o desenvolvimento e normal isto reprovar.
"""

import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
from site_config import is_local, load_site_url  # noqa: E402

MP_TEST = re.compile(r"\bTEST-[0-9a-f]{4,}[0-9a-f-]*", re.I)


def _jwt_role(token):
    parts = token.split(".")
    if len(parts) != 3:
        return ""
    try:
        pad = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(pad)).get("role", "")
    except (ValueError, json.JSONDecodeError):
        return ""


def problems(run_smoke=True):
    out = []

    for md in sorted((ROOT / "legal").glob("*.md")):
        n = md.read_text(encoding="utf-8").count("[PREENCHER")
        if n:
            out.append(f"legal/{md.name}: {n} campo(s) [PREENCHER: ...] sem preencher")

    try:
        url = load_site_url()
        if is_local(url):
            out.append(f"SITE_URL ainda e local ({url}): trocar em app/site.json")
        elif not url.startswith("https://"):
            out.append(f"SITE_URL sem https ({url})")
    except SystemExit as e:
        out.append(str(e))

    cfg_path = ROOT / "app" / "supabase_config.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8-sig"))
        except ValueError:
            cfg = {}
            out.append("app/supabase_config.json nao e JSON valido")
        for k, v in cfg.items():
            if isinstance(v, str) and (v.startswith("sb_secret_") or _jwt_role(v) == "service_role"):
                out.append(f"app/supabase_config.json: o campo {k!r} e chave SECRETA. "
                           "No navegador vai so a publishable (sb_publishable_...) ou a anon")

    scan = [cfg_path] + list((ROOT / "app").glob("*.js")) + list((ROOT / "app").glob("*.json"))
    scan += [p for p in (ROOT / "artifact").glob("*") if p.is_file()]
    for p in scan:
        if p.exists() and MP_TEST.search(p.read_text(encoding="utf-8", errors="ignore")):
            out.append(f"{p.relative_to(ROOT)}: credencial de teste do Mercado Pago (TEST-...)")
    if os.environ.get("MP_ACCESS_TOKEN", "").startswith("TEST-"):
        out.append("MP_ACCESS_TOKEN no ambiente e de teste (TEST-...)")

    if run_smoke:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "smoke_test.py")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            tail = "\n".join((r.stdout or "").strip().splitlines()[-3:])
            out.append(f"smoke test falhou:\n{tail}")
    return out


def main():
    found = problems(run_smoke="--sem-smoke" not in sys.argv)
    if found:
        print("NAO PUBLICAR. Pendencias:")
        for f in found:
            print("  - " + f)
        sys.exit(1)
    print("Pronto para publicar.")


if __name__ == "__main__":
    main()
