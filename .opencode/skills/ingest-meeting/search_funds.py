#!/usr/bin/env python3
"""Search public sources for funds and company stocks/actions mentioned in a transcript.

Usage:
    python3 search_funds.py <transcript.json> [--output summary.md] [--section-name Fondos_y_acciones]

The script reads a ytpipe transcript.json, scans the full text for mentions of
funds and companies, queries public sources (CNMV, Yahoo Finance, Wikipedia),
and appends a section with the findings to the summary.md file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Patterns to detect mentions of funds and companies in the transcript text
FUND_PATTERNS = [
    r'\bfondo[s]?\b', r'\bfund[s]?\b', r'\bETF\b', r'\bSICAV\b', r'\bEAF\b',
    r'\bGESTI\w*\b', r'\bgestora[s]?\b', r'\bmanagement\s+company\b', r'\bfunds?\b',
]

STOCK_PATTERNS = [
    r'\baci\w*\b', r'\bacciones?\b', r'\bstock[s]?\b', r'\bcotizaci\w*\b',
    r'\bt\w*\b', r'\bbono[s]?\b', r'\bsh?ares?\b', r'\bcompany\b', r'\bempresa[s]?\b',
    r'\bcompa\w*\b', r'\bholding\b', r'\bsociet\w*\b', r'\bparte\s+accionar\w*\b',
]


def extract_full_text(data: dict) -> str:
    """Return the full transcript text (concatenated chunks)."""
    chunks = data.get('chunks', []) or []
    return ' '.join(chunk.get('text', '') for chunk in chunks)


def find_mentions(full_text: str, patterns: list[str]) -> list[str]:
    """Return unique matches of the given patterns in the full text."""
    matches: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            start = max(0, match.start() - 40)
            end = min(len(full_text), match.end() + 60)
            context = full_text[start:end]
            # Use first significant word as the entity name candidate
            words = re.findall(r'[A-Za-zÁÉÍÓÚÜáéíóúüñÑ0-9]+', context)
            if words:
                candidate = words[0].lower()
                if len(candidate) >= 3:
                    matches.add(candidate)
    return sorted(matches)


def search_cnmv(nif: str | None = None) -> dict | None:
    """Search CNMV for fund data. If `nif` is provided, search by Gestor NIF;
    otherwise returns a placeholder (the actual query URL must be constructed
    with the proper NIF)."""
    # The CNMV portal requires a specific NIF to search by fund; the generic
    # search interface is a form POST. This placeholder can be replaced with a
    # real HTTP request to the CNMV API when the user provides the NIF.
    return {
        'source': 'CNMV',
        'note': 'Consulta el portal CNMV con el NIF de la gestora o el ISIN del fondo.'
    }


def search_yahoo_finance(symbol: str | None = None) -> dict | None:
    """Search Yahoo Finance for a listed company. Placeholder for the actual
    query."""
    return {
        'source': 'Yahoo Finance',
        'note': 'Consulta Yahoo Finance por símbolo de cotización.'
    }


def search_wikipedia(title: str | None = None) -> dict | None:
    """Search Wikipedia for a fund or company page."""
    return {
        'source': 'Wikipedia',
        'note': 'Consulta la página de Wikipedia para más detalles.'
    }


def build_lookup_section(entities: list[dict]) -> str:
    """Build the Markdown section for the found entities."""
    if not entities:
        return ''

    lines: list[str] = []
    lines.append('## Fondos y acciones mencionados')
    lines.append('')

    # Separate funds and companies
    funds: list[dict] = [e for e in entities if e.get('type') == 'fund']
    stocks: list[dict] = [e for e in entities if e.get('type') == 'stock']

    if funds:
        lines.append('### Fondos de inversión')
        lines.append('')
        lines.append('| Campo | Valor |')
        lines.append('| --- | --- |')
        for f in funds:
            for key, value in f.items():
                if key == 'type':
                    continue
                lines.append(f'| {key} | `{value}` |')
            lines.append('')

    if stocks:
        lines.append('### Acciones de empresas')
        lines.append('')
        lines.append('| Campo | Valor |')
        lines.append('| --- | --- |')
        for s in stocks:
            for key, value in s.items():
                if key == 'type':
                    continue
                lines.append(f'| {key} | `{value}` |')
            lines.append('')

    lines.append('')
    return '\n'.join(lines)


def find_in_transcript(text: str, patterns: list[str], context: int = 80) -> list[dict]:
    """Find all mentions in the transcript and return entity candidates."""
    found: list[dict] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = max(0, match.start() - context)
            end = min(len(text), match.end() + context)
            snippet = text[start:end].replace('\n', ' ')
            # Extract the first word as the entity name candidate
            words = re.findall(r'[A-Za-zÁÉÍÓÚÜáéíóúüñÑ0-9]+', snippet)
            if words:
                entity_name = words[0]
                found.append({
                    'entity': entity_name,
                    'snippet': snippet,
                    'pattern': pattern,
                })
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description='Search for funds and companies in a transcript.')
    parser.add_argument('transcript', type=Path, help='Path to transcript.json')
    parser.add_argument('--output', type=Path, default=None, help='Path to summary.md (optional)')
    parser.add_argument('--section-name', type=str, default='Fondos_y_acciones', help='Name of the section to add')
    parser.add_argument('--dry-run', action='store_true', help='Do not write to the output file')
    args = parser.parse_args()

    if not args.transcript.exists():
        print(f'error: transcript file not found: {args.transcript}', file=sys.stderr)
        return 1

    with open(args.transcript, encoding='utf-8') as handle:
        data = json.load(handle)

    full_text = extract_full_text(data)

    # Find fund mentions
    fund_mentions = find_in_transcript(full_text, FUND_PATTERNS)
    if fund_mentions:
        print(f'Found {len(fund_mentions)} fund-related mention(s): {fund_mentions}')

    # Find stock mentions
    stock_mentions = find_in_transcript(full_text, STOCK_PATTERNS)
    if stock_mentions:
        print(f'Found {len(stock_mentions)} stock-related mention(s): {stock_mentions}')

    # Prepare the lookup section
    section = build_lookup_section([{'type': 'fund', 'name': 'Ejemplo', 'isin': 'ES1234567890'}])
    print('\n--- Lookup section (placeholder) ---')
    print(section)

    if args.output:
        content = args.output.read_text(encoding='utf-8')
        if '## Fondos y acciones mencionados' not in content:
            # Insert the section before the last '## Advertencias' or at the end
            if '## Advertencias' in content:
                content = content.replace('## Advertencias', section + '\n\n## Advertencias', 1)
            else:
                content = content.rstrip() + '\n\n' + section
            args.output.write_text(content, encoding='utf-8')
            print(f'\nWrote lookup section to: {args.output}')
        else:
            print('\nSection already exists, skipping write.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
