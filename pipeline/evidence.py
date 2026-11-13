"""Explainable, bounded citations for manually curated demo content.

An excerpt stored here is not proof of a live fetch; reviewers must consult the linked
City source directly. This module validates provenance and presentation contracts.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = frozenset({'secure.toronto.ca','www.toronto.ca','haveyoursay.toronto.ca'})
ALLOWED_KEYS = frozenset({'what_is_proposed','why','who_is_affected','status','conditions','participation'})


def valid_official_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == 'https' and parsed.hostname in ALLOWED_HOSTS and not parsed.username and not parsed.password


def read_evidence(path: str | Path, item_id: str) -> dict | None:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    record = data.get('items', {}).get(item_id)
    if record is not None:
        validate_evidence(record)
    return record


def validate_evidence(record: dict) -> None:
    claims = record.get('claims', {})
    if not {'what_is_proposed','why','who_is_affected','status'}.issubset(claims):
        raise ValueError('Missing required source-backed claim')
    for key, evidence in claims.items():
        if key not in ALLOWED_KEYS:
            raise ValueError(f'Unexpected claim name: {key}')
        if not valid_official_url(evidence.get('source_url','')):
            raise ValueError(f'Unapproved source URL in {key}')
        if len(evidence.get('excerpt', '').strip()) < 5:
            raise ValueError(f'No meaningful source excerpt in {key}')
        if not evidence.get('note', '').strip():
            raise ValueError(f'Missing evidentiary limitation in {key}')
    if len(record.get('impacts', [])) < 3:
        raise ValueError('Expected resident, business and community considerations')
    audiences=set()
    for item in record['impacts']:
        audiences.add(item.get('audience'))
        if item.get('claim_ref') not in claims:
            raise ValueError('Impact has no linked evidence claim')
        if not item.get('question') or not item.get('potential_effect'):
            raise ValueError('Impact must distinguish question and possible effect')
    if audiences != {'Residents','Local businesses','Community organizations'}:
        raise ValueError('Missing stakeholder category')
