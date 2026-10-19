"""Endereco publico do site (SITE_URL), lido de app/site.json.

Unico ponto de verdade para tudo que precisa de URL absoluta: canonical,
og:url, sitemap, robots. A variavel de ambiente SITE_URL, se existir, vence
o arquivo (util num build de CI). Trocar de hospedagem = trocar este valor.
"""
import json
import os
import re
from pathlib import Path

_FILE = Path(__file__).with_name("site.json")


def load_site_url():
    raw = os.environ.get("SITE_URL", "").strip()
    if not raw:
        raw = (json.loads(_FILE.read_text(encoding="utf-8-sig")).get("SITE_URL") or "").strip()
    raw = raw.rstrip("/")
    if not re.fullmatch(r"https?://[^/\s?#]+", raw):
        raise SystemExit(f"SITE_URL invalido: {raw!r} (use https://dominio, sem caminho e sem barra no fim)")
    return raw


_EMAIL_RE = re.compile(r"[^@\s<>\"']+@[^@\s<>\"']+\.[a-z]{2,}", re.I)


def load_beta():
    """(beta ligado?, e-mail das sugestoes). Ambiente BETA e FEEDBACK_EMAIL
    vencem o app/site.json; e-mail fora do formato vira vazio."""
    cfg = json.loads(_FILE.read_text(encoding="utf-8-sig"))
    env = os.environ.get("BETA", "").strip().lower()
    beta = env in ("1", "true", "sim") if env else bool(cfg.get("BETA"))
    email = os.environ.get("FEEDBACK_EMAIL", "").strip() or (cfg.get("FEEDBACK_EMAIL") or "").strip()
    return beta, email if _EMAIL_RE.fullmatch(email) else ""


def is_local(url):
    return bool(re.match(r"https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])(:|$)", url))
