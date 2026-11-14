"""CLI: python build_cache.py --item 2026.PH29.2 [--force]

Requires an operator-prepared item_page.txt; report.pdf optional.
Never uploads raw public correspondence sections. Does not touch demo fixtures unless
--force is supplied. Do not commit generated unreviewed data as authoritative.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from pipeline.clean import strip_personal_sections
from pipeline.extract import extract_card
from pipeline.provider import get_config
from pipeline.explain import explain_with_citations
from pipeline.verify import verify_card, verify_explanation_segments
from pipeline.status import overall_status

ROOT = Path(__file__).parent

def write_api_cache(folder: Path, force: bool = False) -> None:
    config = get_config()
    text_path = folder / 'item_page.txt'
    if not text_path.exists():
        raise FileNotFoundError(f'Missing: {text_path}')
    target = folder / 'card.json'
    if target.exists() and not force:
        raise FileExistsError('Refusing to overwrite a curated demo card without --force')
    meta_path = folder / 'meta.json'
    meta = json.loads(meta_path.read_text(encoding='utf8')) if meta_path.exists() else {}
    page_text = strip_personal_sections(text_path.read_text(encoding='utf8'))
    pdf_path = folder / 'report.pdf'
    pdf_bytes = pdf_path.read_bytes() if pdf_path.exists() else None
    if pdf_bytes and len(pdf_bytes) > 20_000_000:
        raise ValueError('Report is too large for the prototype; choose a smaller official file')
    card = extract_card(page_text, pdf_bytes)
    expected_id = folder.name
    if card.item_id != expected_id:
        raise ValueError(f'Agenda item mismatch: expected {expected_id}, model gave {card.item_id}')
    verification = verify_card(card, page_text, pdf_bytes)
    status = overall_status(card, verification['stages'])
    explanation = verify_explanation_segments(
        explain_with_citations(page_text, pdf_bytes, meta.get('item_url', '')), page_text, pdf_bytes)
    now = datetime.now(timezone.utc).isoformat()
    # Write ONLY after both API calls succeed; no partial cached output.
    output = {
        'card': card.model_dump(), 'verification': verification, 'status': status,
        'generation_mode': 'ai_unreviewed', 'generated_at': now,
        'provider': config.provider, 'model': config.model,
    }
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf8')
    (folder/'explanation.json').write_text(json.dumps(explanation, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'Wrote {expected_id}; status={status}; review against official source before publishing')

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env')
    parser = argparse.ArgumentParser()
    parser.add_argument('--item', required=True, help='Agenda ID, e.g. 2026.PH29.2')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    try:
        config = get_config()
    except ValueError as error:
        parser.error(str(error))
    if not config.api_key:
        parser.error(f'{config.key_env} is required for generation')
    write_api_cache(ROOT / 'data' / 'items' / args.item, args.force)
