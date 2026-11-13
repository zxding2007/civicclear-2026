"""Tests of source traceability & impact presentation (no network needed)."""
from pathlib import Path
import json
import pytest
from pipeline.evidence import valid_official_url, read_evidence, validate_evidence
from pipeline.schema import DecisionCard
from pipeline.verify import verify_card
from pipeline.status import overall_status

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('item_id,status',[('2026.PH29.2','committee_only'),('2026.PH29.1','final_adopted')])
def test_impact_cards_keep_real_decision_status(item_id,status):
    evidence = read_evidence(ROOT/'data/evidence_impact.json',item_id)
    assert len(evidence['impacts'])==3
    data = json.loads((ROOT/'data/items'/item_id/'card.json').read_text())
    card = DecisionCard.model_validate(data['card'])
    source=(ROOT/'data/items'/item_id/'item_page.txt').read_text()
    flags=verify_card(card,source)
    assert overall_status(card,flags['stages']) == status

@pytest.mark.parametrize('url',["https://evil.example/council", "http://secure.toronto.ca/x", "https://secure.toronto.ca.evil.example/x", "https://bad@evil.com/x"])
def test_unsafe_sources_blocked(url):
    assert not valid_official_url(url)

def test_every_impact_source_is_primary_and_disclosed():
    data=json.loads((ROOT/'data/evidence_impact.json').read_text())
    assert set(data['items'])=={'2026.PH29.1','2026.PH29.2'}
    assert 'NOT' not in data['audit_type'] or 'not signed' in data['audit_type'].lower()
    for record in data['items'].values():
        validate_evidence(record)
        for claim in record['claims'].values():
            assert valid_official_url(claim['source_url'])
            assert 'excerpt' in claim and 'note' in claim


def test_rejects_invented_claim_or_unsourced_impact():
    record = read_evidence(ROOT/'data/evidence_impact.json','2026.PH29.2')
    record['impacts'][0]['claim_ref']='a-model-invented-label'
    with pytest.raises(ValueError): validate_evidence(record)
