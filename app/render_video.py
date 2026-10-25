"""Videoaulas: lê app/videos.json, valida e injeta os players nos painéis.

Cada vídeo vira um bloco `.vid` com só a capa (um botão). O player de verdade
(iframe do YouTube ou <video>) é criado pelo app.js no clique, para a página
não carregar nada de fora antes disso. Junto vão a caixa "aula assistida",
que é um `.pchk` como os das Partes e por isso já conta no progresso do
módulo, e a transcrição recolhível.

Onde o vídeo aparece:
  part ausente ou null  -> topo do módulo, logo abaixo do cabeçalho
  part = N              -> topo da "PARTE N" daquele módulo

Sem vídeo cadastrado nada é injetado e o HTML sai igual ao de antes.
"""

import html
import json
import re

import markdown

PROVIDERS = ("youtube", "file")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
URL_RE = re.compile(r"^(https://|\.{0,2}/|[A-Za-z0-9_])[^\s\"'<>]*$")
ALLOWED = {"id", "module", "part", "title", "duration", "provider", "src",
           "captions", "poster", "transcript"}


def load_videos(path="videos.json"):
    """Devolve a lista de vídeos validada. Erro de cadastro derruba o build."""
    data = json.loads(open(path, encoding="utf-8").read())
    videos = data.get("videos", []) if isinstance(data, dict) else data
    if not isinstance(videos, list):
        raise ValueError("videos.json: 'videos' deve ser uma lista")
    seen, places = set(), set()
    for i, v in enumerate(videos):
        where = f"videos.json, vídeo {i + 1} ({v.get('id', 'sem id') if isinstance(v, dict) else '?'})"
        if not isinstance(v, dict):
            raise ValueError(f"{where}: deve ser um objeto")
        extra = set(v) - ALLOWED
        if extra:
            raise ValueError(f"{where}: campo desconhecido {sorted(extra)}")
        for field in ("id", "module", "title", "provider", "src"):
            if not isinstance(v.get(field), str) or not v[field].strip():
                raise ValueError(f"{where}: falta o campo {field!r}")
        if not ID_RE.match(v["id"]):
            raise ValueError(f"{where}: id só com minúsculas, números e hífen")
        if v["id"] in seen:
            raise ValueError(f"{where}: id repetido")
        seen.add(v["id"])
        if not re.fullmatch(r"mod\d", v["module"]):
            raise ValueError(f"{where}: module deve ser mod0 a mod9")
        part = v.get("part")
        if part is not None and (not isinstance(part, int) or isinstance(part, bool) or part < 1):
            raise ValueError(f"{where}: part deve ser o número da Parte ou null")
        if (v["module"], part) in places:
            raise ValueError(f"{where}: já existe vídeo neste lugar ({v['module']}, part {part})")
        places.add((v["module"], part))
        if v["provider"] not in PROVIDERS:
            raise ValueError(f"{where}: provider deve ser um de {PROVIDERS}")
        if v["provider"] == "youtube" and not YOUTUBE_ID_RE.match(v["src"]):
            raise ValueError(f"{where}: em provider youtube, src é o id de 11 caracteres do vídeo, não a URL")
        for field in ("src", "captions", "poster") if v["provider"] == "file" else ("captions", "poster"):
            if v.get(field) is not None and not (isinstance(v[field], str) and URL_RE.match(v[field])):
                raise ValueError(f"{where}: {field} deve ser URL https ou caminho relativo")
        for field in ("duration", "transcript"):
            if v.get(field) is not None and not isinstance(v[field], str):
                raise ValueError(f"{where}: {field} deve ser texto")
    return videos


def warnings(videos):
    """Avisos de acessibilidade: não derrubam o build."""
    out = []
    for v in videos:
        if not (v.get("transcript") or "").strip():
            out.append(f"vídeo {v['id']} sem transcrição")
        if v["provider"] == "file" and not v.get("captions"):
            out.append(f"vídeo {v['id']} sem arquivo de legenda (.vtt)")
    return out


def render_video(v):
    esc = lambda s: html.escape(s or "", quote=True)
    attrs = f'data-vid="{esc(v["id"])}" data-provider="{esc(v["provider"])}" data-src="{esc(v["src"])}"'
    if v.get("captions"):
        attrs += f' data-captions="{esc(v["captions"])}"'
    poster = (f'<img class="vid-poster" src="{esc(v["poster"])}" alt="" loading="lazy">'
              if v.get("poster") else "")
    duration = f'<span class="vid-dur">{esc(v["duration"])}</span>' if v.get("duration") else ""
    kicker = "Aula de abertura" if v.get("part") is None else "Videoaula desta Parte"
    transcript = ""
    if (v.get("transcript") or "").strip():
        body = markdown.markdown(v["transcript"], extensions=["extra"])
        transcript = (f'<details class="vid-transcript"><summary>Transcrição da aula</summary>'
                      f'<div class="vid-transcript-body">{body}</div></details>')
    return (
        f'<div class="vid" {attrs}>'
        f'<button type="button" class="vid-cover" aria-label="Assistir à aula: {esc(v["title"])}">'
        f'{poster}<span class="vid-play" aria-hidden="true">▶</span>'
        f'<span class="vid-meta"><span class="vid-kicker">{kicker}</span>'
        f'<span class="vid-title">{esc(v["title"])}</span>{duration}</span></button>'
        f'<div class="vid-frame" hidden></div>'
        f'<label class="vid-done"><input type="checkbox" class="pchk vid-chk" '
        f'data-pid="{esc(v["module"])}-video-{esc(v["id"])}">'
        f'<span class="vid-done-label">Marcar aula como assistida</span></label>'
        f'{transcript}</div>'
    )


LANDING_ALLOWED = {"title", "duration", "provider", "src", "captions", "poster", "transcript"}


def load_landing_video(path="videos.json"):
    """Vídeo explicativo do topo da tela de apresentação: a chave
    "apresentacao" de videos.json (objeto como os outros, sem id, module e
    part). null ou ausente: o espaço não aparece. Erro de cadastro derruba o build."""
    data = json.loads(open(path, encoding="utf-8").read())
    v = data.get("apresentacao") if isinstance(data, dict) else None
    if v is None:
        return None
    where = "videos.json, apresentacao"
    if not isinstance(v, dict):
        raise ValueError(f"{where}: deve ser um objeto ou null")
    extra = set(v) - LANDING_ALLOWED
    if extra:
        raise ValueError(f"{where}: campo desconhecido {sorted(extra)}")
    for field in ("title", "provider", "src"):
        if not isinstance(v.get(field), str) or not v[field].strip():
            raise ValueError(f"{where}: falta o campo {field!r}")
    if v["provider"] not in PROVIDERS:
        raise ValueError(f"{where}: provider deve ser um de {PROVIDERS}")
    if v["provider"] == "youtube" and not YOUTUBE_ID_RE.match(v["src"]):
        raise ValueError(f"{where}: em provider youtube, src é o id de 11 caracteres do vídeo, não a URL")
    for field in ("src", "captions", "poster") if v["provider"] == "file" else ("captions", "poster"):
        if v.get(field) is not None and not (isinstance(v[field], str) and URL_RE.match(v[field])):
            raise ValueError(f"{where}: {field} deve ser URL https ou caminho relativo")
    return v


def render_landing_video(v):
    """Capa do vídeo da apresentação. O player nasce no clique (landing.js),
    como nas videoaulas: nada de fora carrega antes disso."""
    if not v:
        return ""
    esc = lambda s: html.escape(s or "", quote=True)
    attrs = f'data-provider="{esc(v["provider"])}" data-src="{esc(v["src"])}"'
    if v.get("captions"):
        attrs += f' data-captions="{esc(v["captions"])}"'
    poster = (f'<img class="vid-poster" src="{esc(v["poster"])}" alt="" loading="lazy">' if v.get("poster") else "")
    duration = f'<span class="vid-dur">{esc(v["duration"])}</span>' if v.get("duration") else ""
    transcript = ""
    if (v.get("transcript") or "").strip():
        body = markdown.markdown(v["transcript"], extensions=["extra"])
        transcript = (f'<details class="vid-transcript"><summary>Transcrição do vídeo</summary>'
                      f'<div class="vid-transcript-body">{body}</div></details>')
    return (
        f'<div class="vid lp-video" id="lpVideo" {attrs}>'
        f'<button type="button" class="vid-cover" aria-label="Assistir ao vídeo: {esc(v["title"])}">'
        f'{poster}<span class="vid-play" aria-hidden="true">▶</span>'
        f'<span class="vid-meta"><span class="vid-kicker">Conheça em vídeo</span>'
        f'<span class="vid-title">{esc(v["title"])}</span>{duration}</span></button>'
        f'<div class="vid-frame" hidden></div>{transcript}</div>'
    )


def inject(frag, videos):
    """frag: {mod: html do módulo}. Devolve ({mod: html com os vídeos de
    Parte}, {mod: html do vídeo de abertura}). Falha se o módulo ou a Parte
    de algum vídeo não existir."""
    out, openers = dict(frag), {}
    for v in videos:
        mod = v["module"]
        if mod not in out:
            raise ValueError(f"videos.json, vídeo {v['id']}: módulo {mod} não existe")
        block = render_video(v)
        if v.get("part") is None:
            openers[mod] = block
            continue
        # o <h2> de cada Parte é montado pelo build_pipeline.py com o título
        # em <span class="htext">PARTE N: ...</span>
        pat = re.compile(r'(<h2\b[^>]*>(?:(?!</h2>).)*<span class="htext">PARTE %d\b(?:(?!</h2>).)*</h2>)' % v["part"], re.S)
        new, n = pat.subn(lambda m: m.group(1) + block, out[mod], count=1)
        if n != 1:
            raise ValueError(f"videos.json, vídeo {v['id']}: não achei a PARTE {v['part']} em {mod}")
        out[mod] = new
    return out, openers
