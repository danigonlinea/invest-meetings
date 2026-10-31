#!/usr/bin/env python3
"""Regenera INDEX.md a partir del frontmatter YAML de los `.md` del repositorio.

Uso: python3 tools/build_index.py

Lee `title`, `date`, `type`, `category`, `tags` y `status` de cada archivo con
frontmatter. No usa PyYAML: el frontmatter de este repositorio es plano
(`clave: valor` y listas entre corchetes).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "INDEX.md"

SKIP_DIRS = {".git", ".venv", "ytpipe", "tools", "node_modules", ".pytest_cache", "__pycache__", ".opencode", ".agents"}
KEYS = ("title", "date", "type", "category", "tags", "status")
FIELD = re.compile(r"^(\w+):\s*(.*)$")


def frontmatter(path: Path) -> dict | None:
    """Devuelve el frontmatter de un archivo `.md`, o None si no lo tiene."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    data: dict[str, str] = {}
    for line in text[3:end].splitlines():
        match = FIELD.match(line.strip())
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip().strip('"')
        if key in KEYS:
            data[key] = value
    return data


def artifacts() -> list[tuple[str, dict]]:
    """Devuelve (ruta relativa, frontmatter) de cada artefacto del repositorio."""
    found = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if relative.name in {"README.md", "INDEX.md"}:
            continue
        data = frontmatter(path)
        if data:
            found.append((str(relative), data))
    found.sort(key=lambda item: (item[1].get("date", ""), item[0]), reverse=True)
    return found


def cell(value: str) -> str:
    """Escapa el separador de la tabla markdown."""
    return value.replace("|", "\\|").strip()


def build(rows: list[tuple[str, dict]]) -> str:
    """Devuelve el texto completo de INDEX.md."""
    lines = [
        "# Índice del repositorio",
        "",
        "Mapa de todos los artefactos del repositorio `investing-meetings`. Lo genera "
        "`python3 tools/build_index.py` a partir del frontmatter YAML; no editar a mano.",
        "Un agente IA lee este archivo primero y después abre solo lo que necesita.",
        "",
        "| Ruta | Tipo | Categoría | Fecha | Título | Tags |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for relative, data in rows:
        lines.append(
            "| `{}` | {} | {} | {} | {} | {} |".format(
                cell(relative),
                cell(data.get("type", "")),
                cell(data.get("category", "")),
                cell(data.get("date", "")),
                cell(data.get("title", "")),
                cell(data.get("tags", "")),
            )
        )

    lines += [
        "",
        "**Total de artefactos indexados:** {}".format(len(rows)),
        "",
        "## Cómo llegar al dato",
        "",
        "| Pregunta | Ruta |",
        "| --- | --- |",
        "| ¿Cómo está mi cartera y qué hago con ella? | `finance/portfolio/` (empieza por `cartera-actual.md`) |",
        "| ¿Qué dicen los vídeos de La Pizarra de Andrés? | `finance/la-pizarra-de-andres/` o `ai/la-pizarra-de-andres/` |",
        "| ¿Qué dicen los webinars de MyInvestor? | `finance/myinvestor-webinars/catalogo.md` y luego la carpeta del webinar |",
        "| ¿Resumen consolidado del canal o revisión adversarial? | `finance/reports/`, `finance/revisions/` |",
        "| ¿Cómo se llama alguien, un canal o una entidad? | `reference/glossary.md` |",
        "",
        "Detalle de cada ruta, reglas de precisión y flujo de ingesta: `AGENTS.md`.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = artifacts()
    INDEX.write_text(build(rows), encoding="utf-8")
    print(f"escrito: {INDEX.relative_to(ROOT)} ({len(rows)} artefactos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
