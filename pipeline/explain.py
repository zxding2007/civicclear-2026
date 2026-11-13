"""Optional cited explanation, separate from strict JSON extraction."""
from .extract import SYSTEM, MODEL, build_documents

QUESTION = '''Explain in simple English: (1) proposed and why, (2) stage and decision,
(3) affected geography and people, (4) confirmed ways to participate or unknowns.
Keep claims short. Cite each substantive sentence. Never infer future availability.'''


def explain_with_citations(item_page_text: str, pdf_bytes: bytes | None, item_url: str = '') -> list[dict]:
    import anthropic
    client = anthropic.Anthropic(timeout=90.0, max_retries=1)
    response = client.messages.create(
        model=MODEL, max_tokens=4000, system=SYSTEM,
        messages=[{'role': 'user', 'content': [
            *build_documents(item_page_text, pdf_bytes, citations=True),
            {'type': 'text', 'text': QUESTION},
        ]}],
    )
    if response.stop_reason != 'end_turn':
        raise RuntimeError('Cited explanation did not finish')
    result = []
    for block in response.content:
        if block.type != 'text' or not block.text.strip():
            continue
        references = []
        for c in (block.citations or []):
            references.append({
                'document': getattr(c, 'document_title', 'Official source'),
                'cited_text': getattr(c, 'cited_text', ''),
                'page': getattr(c, 'start_page_number', None),
                'document_index': getattr(c, 'document_index', None),
                'url': item_url if getattr(c, 'document_index', 0) == 0 else None,
            })
        result.append({'text': block.text, 'sources': references})
    return result
