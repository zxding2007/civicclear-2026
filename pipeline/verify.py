"""Source quote verification: normalize whitespace, not actual words."""
from functools import lru_cache
import io
import re
from pypdf import PdfReader


def normalize(value: str) -> str:
    return re.sub(r'\s+', ' ', value).strip().casefold()


def pdf_text(pdf_bytes: bytes | None) -> str:
    if not pdf_bytes:
        return ''
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return '\n'.join(page.extract_text() or '' for page in reader.pages)


def quote_is_in_sources(quote: str | None, item_page_text: str, report_text: str = '') -> bool:
    if not quote or not quote.strip():
        return False
    q = normalize(quote)
    return q in normalize(item_page_text) or q in normalize(report_text)


def verify_card(card, item_page_text: str, pdf_bytes: bytes | None = None) -> dict:
    report_text = pdf_text(pdf_bytes)
    check = lambda q: quote_is_in_sources(q, item_page_text, report_text)
    return {
        'stages': [check(s.quote) for s in card.stages],
        'phrases': [check(p.quote) for p in card.procedural_phrases],
        'participation': check(card.participation.quote) if card.participation.quote else None,
    }


def verify_explanation_segments(segments: list[dict], item_page_text: str, pdf_bytes: bytes | None = None) -> list[dict]:
    """Flag citations whose quoted wording is absent from supplied evidence.

    Conservative: a flagged quote can be true but hard to normalize after PDF
    text extraction; user must inspect it manually. Does not judge interpretation.
    """
    report_text = pdf_text(pdf_bytes)
    checked = []
    for segment in segments:
        entry = dict(segment)
        sources = []
        for source in segment.get('sources', []):
            s = dict(source)
            document_index = s.get('document_index')
            if 'document_index' not in s:
                # Older curated examples do not specify a document index.
                s['verified'] = quote_is_in_sources(s.get('cited_text'), item_page_text, report_text)
            elif type(document_index) is int and document_index == 0:
                s['verified'] = quote_is_in_sources(s.get('cited_text'), item_page_text)
            elif type(document_index) is int and document_index == 1:
                s['verified'] = quote_is_in_sources(s.get('cited_text'), report_text)
            else:
                s['verified'] = False
            sources.append(s)
        entry['sources'] = sources
        checked.append(entry)
    return checked
