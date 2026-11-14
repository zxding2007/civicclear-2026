"""Serve the CivicClear website and its Python API from one origin.

Run locally with: uvicorn server:app --reload
The curated decisions and calculator need no API credentials. New-item analysis
uses the existing pipeline and returns an unreviewed preview without saving it.
"""
from __future__ import annotations

import hmac
import json
import os
import re
from pathlib import Path
from typing import Annotated
from urllib.parse import parse_qs, urlsplit

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')

from build_site import build
from calculator import compare
from pipeline.clean import strip_personal_sections
from pipeline.explain import explain_with_citations
from pipeline.extract import extract_card
from pipeline.provider import get_config
from pipeline.status import overall_status
from pipeline.verify import pdf_text, verify_card, verify_explanation_segments

MAX_PDF_BYTES = 20_000_000
ITEM_ID = re.compile(r'20\d{2}\.[A-Z]+\d+\.\d+')
app = FastAPI(title='CivicClear API', version='1.0.0')


@app.exception_handler(RequestValidationError)
async def validation_error(_request, error: RequestValidationError):
    # Inputs can include an analyst password; never echo submitted values.
    detail = [{key: item[key] for key in ('loc', 'msg', 'type')}
              for item in error.errors()]
    return JSONResponse(status_code=422, content={'detail': detail})


def analysis_enabled() -> bool:
    try:
        return bool(os.getenv('CIVICCLEAR_ANALYST_PASSWORD') and get_config().api_key)
    except ValueError:
        return False


@app.get('/api/health')
def health():
    return {'status': 'ok'}


@app.get('/api/bootstrap')
def bootstrap():
    try:
        data = build()
    except (OSError, ValueError, KeyError):
        raise HTTPException(503, 'The decision records could not be loaded. Please try again later.') from None
    try:
        provider = get_config().provider
    except ValueError:
        provider = None
    return {**data, 'runtime': {
        'mode': 'connected', 'analysis_enabled': analysis_enabled(),
        'analysis_provider': provider,
    }}


class TaxRequest(BaseModel):
    assessed_value: Annotated[float, Field(strict=True, ge=0, le=100_000_000, allow_inf_nan=False)]


@app.post('/api/tax')
def tax(request: TaxRequest):
    rates = json.loads((ROOT / 'data' / 'tax_rates.json').read_text(encoding='utf-8'))['residential']
    before_rate, after_rate = rates['2025']['rate_percent'], rates['2026']['rate_percent']
    return {
        'assessed_value': request.assessed_value,
        **compare(request.assessed_value, before_rate, after_rate),
        'rates': {'2025': before_rate, '2026': after_rate},
    }


def official_item_url(value: str) -> tuple[str, str]:
    """Accept exactly one Toronto agenda item identifier and return a clean URL."""
    try:
        url = urlsplit(value.strip())
        query = parse_qs(url.query, keep_blank_values=True, strict_parsing=True)
        identifiers = query.get('item', [])
        if (url.scheme != 'https' or url.netloc != 'secure.toronto.ca'
                or url.path != '/council/agenda-item.do' or url.fragment
                or set(query) != {'item'} or len(identifiers) != 1
                or not ITEM_ID.fullmatch(identifiers[0])):
            raise ValueError
    except ValueError:
        raise HTTPException(422, 'Enter an official Toronto agenda item URL with one valid item identifier.') from None
    item_id = identifiers[0]
    return f'https://secure.toronto.ca/council/agenda-item.do?item={item_id}', item_id


@app.post('/api/analyse')
def analyse(
    password: Annotated[str, Form()],
    item_url: Annotated[str, Form()],
    item_page: Annotated[str, Form()],
    report: Annotated[UploadFile | None, File()] = None,
):
    if not analysis_enabled():
        raise HTTPException(503, 'New-item analysis is not configured. You can still explore the saved decisions.')
    config = get_config()
    expected_password = os.environ['CIVICCLEAR_ANALYST_PASSWORD']
    if not hmac.compare_digest(password.encode('utf-8'), expected_password.encode('utf-8')):
        raise HTTPException(401, 'The analyst password is incorrect.')

    source_url, expected_id = official_item_url(item_url)
    cleaned = strip_personal_sections(item_page)
    if len(cleaned.strip()) < 100:
        raise HTTPException(422, 'Paste at least 100 characters of substantive official agenda text.')

    pdf = None
    if report is not None:
        pdf = report.file.read(MAX_PDF_BYTES + 1)
        if len(pdf) > MAX_PDF_BYTES:
            raise HTTPException(413, 'Choose a PDF no larger than 20 MB.')
        if not pdf.startswith(b'%PDF'):
            raise HTTPException(422, 'The report must be a standard PDF file.')
        if config.provider == 'deepseek':
            try:
                readable = bool(pdf_text(pdf).strip())
            except Exception:
                readable = False
            if not readable:
                raise HTTPException(422, 'DeepSeek needs a PDF with selectable text. Choose a text-based PDF or paste the report text with the agenda record.')

    try:
        card = extract_card(cleaned, pdf)
        if card.item_id != expected_id:
            raise HTTPException(502, 'The analysis returned a different agenda item. No result has been saved.')
        checks = verify_card(card, cleaned, pdf)
        status = overall_status(card, checks['stages'])
        explanation = verify_explanation_segments(
            explain_with_citations(cleaned, pdf, source_url), cleaned, pdf,
        )
    except HTTPException:
        raise
    except Exception:
        # Provider and PDF errors may include source text or request metadata.
        # Keep these details out of both the response and application logs.
        raise HTTPException(502, 'Analysis could not finish. Check the source text and PDF, then try again. No result has been saved.') from None

    return {
        'id': card.item_id,
        'short_title': card.title,
        'meta': {
            'item_id': card.item_id,
            'title': card.title,
            'item_url': source_url,
            'report_url': '',
            'source_mode': 'user_supplied_official_text',
            'source_checked_on': None,
            'human_review': 'pending',
            'generation_mode': 'ai_unreviewed',
            'ai_provider': config.provider,
            'ai_model': config.model,
        },
        'card': card.model_dump(),
        'checks': checks,
        'status': status,
        'explanation': explanation,
        'evidence': None,
    }


@app.api_route('/api', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'], include_in_schema=False)
@app.api_route('/api/{path:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'], include_in_schema=False)
def unknown_api(path: str = ''):
    raise HTTPException(404, 'API endpoint not found.')


# Keep this last so API requests never fall through to static HTML.
app.mount('/', StaticFiles(directory=ROOT / 'site', html=True), name='site')
