#!/usr/bin/env python3
"""Lista los webinars de MyInvestor y mantiene el catálogo del repositorio.

Uso:
    python3 tools/myinvestor_webinars.py list      # una línea TSV por webinar
    python3 tools/myinvestor_webinars.py catalogo  # reescribe finance/myinvestor-webinars/catalogo.md

El listado sale de las páginas públicas de
https://blog.myinvestor.es/escuelamyinvestor/webinars/ (paginadas). Cada
tarjeta trae el vídeo de YouTube en `data-plyr-embed-id` y el enlace del post
en el `<h2 class="title">`. No hay API con el webinar como campo: el vídeo vive
solo en el HTML del listado.
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

BASE = "https://blog.myinvestor.es/escuelamyinvestor/webinars/"
ROOT = Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "finance" / "myinvestor-webinars" / "catalogo.md"

ARTICLE = re.compile(r"<article\b.*?</article>", re.S)
EMBED = re.compile(r'data-plyr-embed-id="([^"]+)"')
TITLE = re.compile(r'<h2 class="title">\s*<a href="([^"]+)"[^>]*>(.*?)</a>', re.S)
VIDEO_ID = re.compile(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})")
EXCERPT = re.compile(r'<div class="excerpt">(.*?)</div>', re.S)
TAGS = re.compile(r"<[^>]+>")


def fetch(url: str) -> str:
    """Devuelve el HTML de una página. Un 404 significa fin del listado."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (investing-meetings)"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return ""
        raise


def clean(fragment: str) -> str:
    """Quita etiquetas y normaliza espacios y entidades HTML."""
    text = TAGS.sub(" ", fragment)
    text = html.unescape(text)
    text = text.replace("&hellip;", "…").replace("&amp;", "&")
    return " ".join(text.split())


def parse_page(page: str, url: str) -> list[dict]:
    """Devuelve un dict por tarjeta con vídeo de YouTube."""
    items = []
    for block in ARTICLE.findall(page):
        embed = EMBED.search(block)
        title = TITLE.search(block)
        if not embed or not title:
            continue
        video = VIDEO_ID.search(embed.group(1))
        if not video:
            continue
        excerpt = EXCERPT.search(block)
        items.append(
            {
                "video_id": video.group(1),
                "title": clean(title.group(2)),
                "post_url": title.group(1),
                "excerpt": clean(excerpt.group(1)) if excerpt else "",
                "listing_page": url,
            }
        )
    return items


def collect(max_pages: int = 60) -> list[dict]:
    """Recorre el listado paginado hasta la primera página sin webinars."""
    found: list[dict] = []
    seen: set[str] = set()
    for number in range(1, max_pages + 1):
        url = BASE if number == 1 else f"{BASE}page/{number}/"
        items = parse_page(fetch(url), url)
        if not items:
            break
        for item in items:
            if item["video_id"] in seen:
                continue
            seen.add(item["video_id"])
            found.append(item)
    return found


def ingested_ids() -> set[str]:
    """Lee los `source.video_id` de todos los transcript.json del repositorio."""
    ids = set()
    for path in ROOT.glob("*/*/*/transcript.json"):
        try:
            ids.add(json.loads(path.read_text(encoding="utf-8"))["source"]["video_id"])
        except (KeyError, ValueError):
            continue
    return ids


def folder_for(video_id: str) -> str:
    """Devuelve la ruta relativa de la carpeta del webinar, si existe."""
    for path in ROOT.glob("finance/myinvestor-webinars/*/transcript.json"):
        try:
            if json.loads(path.read_text(encoding="utf-8"))["source"]["video_id"] == video_id:
                return str(path.parent.relative_to(ROOT))
        except (KeyError, ValueError):
            continue
    return ""


def write_catalogo(items: list[dict]) -> Path:
    """Reescribe el catálogo markdown con el estado de cada webinar."""
    rows = []
    for item in items:
        folder = folder_for(item["video_id"])
        estado = "ingerido" if folder else "pendiente"
        rows.append((item, folder, estado))

    lines = [
        "---",
        'title: "Catálogo de webinars de MyInvestor"',
        f"date: {date.today().isoformat()}",
        "type: reference",
        "category: finance",
        "tags: [myinvestor, webinars, catalogo, youtube]",
        "status: living",
        "---",
        "",
        "# Catálogo de webinars de MyInvestor",
        "",
        "Fuente: <https://blog.myinvestor.es/escuelamyinvestor/webinars/>.",
        "Lo genera `python3 tools/myinvestor_webinars.py catalogo`; no editar a mano.",
        "",
        f"**Webinars con vídeo publicado:** {len(rows)} · "
        f"**ingeridos:** {sum(1 for _, _, e in rows if e == 'ingerido')} · "
        f"**pendientes:** {sum(1 for _, _, e in rows if e == 'pendiente')}",
        "",
        "| # | Título | Vídeo | Estado | Carpeta |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, (item, folder, estado) in enumerate(rows, start=1):
        link = f"https://www.youtube.com/watch?v={item['video_id']}"
        title = item["title"].replace("|", "\\|")
        lines.append(f"| {index} | [{title}]({item['post_url']}) | [{item['video_id']}]({link}) | {estado} | `{folder or '—'}` |")

    CATALOGO.parent.mkdir(parents=True, exist_ok=True)
    CATALOGO.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return CATALOGO


def main(argv: list[str]) -> int:
    command = argv[1] if len(argv) > 1 else "list"
    items = collect()
    if not items:
        print("no webinar found: the listing page changed its HTML", file=sys.stderr)
        return 1

    if command == "list":
        for item in items:
            print("\t".join([item["video_id"], item["title"], item["post_url"]]))
        print(f"# {len(items)} webinars", file=sys.stderr)
        return 0

    if command == "catalogo":
        path = write_catalogo(items)
        print(f"escrito: {path.relative_to(ROOT)} ({len(items)} webinars)")
        return 0

    if command == "pendientes":
        done = ingested_ids()
        for item in items:
            if item["video_id"] not in done:
                print("\t".join([item["video_id"], item["title"], item["post_url"]]))
        return 0

    print(f"comando desconocido: {command} (usa list, pendientes o catalogo)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
