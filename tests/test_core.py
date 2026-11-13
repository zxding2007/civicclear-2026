"""Unit tests for critical logic; never calls Anthropic or the internet."""
import json
from pathlib import Path
import pytest
from calculator import compare, municipal_tax
from pipeline.clean import strip_personal_sections
from pipeline.status import overall_status
from pipeline.verify import verify_card, quote_is_in_sources, verify_explanation_segments
from pipeline.schema import DecisionCard

ROOT = Path(__file__).resolve().parents[1]


def _card(stages):
    return DecisionCard(item_id='2026.TEST.1', title='Test', wards=['All'],
        what_is_proposed='Test', why='Test', who_is_affected='Test', stages=stages,
        conditions=[], participation={'can_still_comment':'not_stated','deadline_text':None,'how':None,'quote':None},
        procedural_phrases=[], uncertainties=[])


def _stage(stage_type, outcome, quote='verified phrase'):
    return {'body':'Test body','date':'2026-01-01','stage_type':stage_type,'outcome':outcome,'quote':quote}


def test_calculator_numbers():
    assert municipal_tax(700000, 0.614311) == 4300.18
    assert municipal_tax(700000, 0.601087) == 4207.61
    assert compare(700000, 0.601087, 0.614311) == {'before':4207.61,'after':4300.18,'difference':92.57}


def test_negative_value_rejected():
    with pytest.raises(ValueError): municipal_tax(-1, 0.61)


def test_clean_removes_public_correspondents_and_retains_decision():
    raw = ('## Council Decision\nCouncil received the item.\n'
           '#### Communications (Committee)\nMary Private wrote an email.\n'
           '#### Speakers\nTom Private spoke.\n'
           '#### Motions\nMotion to receive carried.')
    safe = strip_personal_sections(raw)
    assert 'Private' not in safe
    assert 'Motion to receive carried.' in safe
    assert 'Council received the item.' in safe


def test_clean_does_not_resume_on_untrusted_heading():
    raw = '## Communications\nName One\n### Unfamiliar Heading\nName Two\n## Motions\nFormal text'
    safe = strip_personal_sections(raw)
    assert 'Name One' not in safe and 'Name Two' not in safe
    assert 'Formal text' in safe


def test_quote_verification_is_conservative():
    assert quote_is_in_sources('Council adopted  it.', 'Council adopted  it.')
    assert quote_is_in_sources('Council adopted it.', 'Council\nadopted    it.')
    assert not quote_is_in_sources('Council approved ten million.', 'Council received a motion.')
    assert not quote_is_in_sources('', 'any text')


def test_final_council_priority_over_earlier_committee_receipt():
    card = _card([_stage('committee_decision','received_for_information'),
                  _stage('council_decision','adopted')])
    assert overall_status(card,[True,True]) == 'final_adopted'


def test_unverified_stage_cannot_become_adoption():
    card = _card([_stage('staff_recommendation','recommended'),
                  _stage('council_decision','adopted','fabricated')])
    assert overall_status(card,[True,False]) == 'recommendation_only'


def test_statuses():
    cases = [('council_decision','received_for_information','received'),
             ('council_decision','adopted_with_amendments','final_amended'),
             ('committee_decision','adopted_with_amendments','committee_only'),
             ('staff_recommendation','recommended','recommendation_only')]
    for typ,outcome,expected in cases:
        assert overall_status(_card([_stage(typ,outcome)]),[True]) == expected


def test_mismatched_verification_flags_fail():
    with pytest.raises(ValueError): overall_status(_card([_stage('council_decision','adopted')]),[])


@pytest.mark.parametrize('item_id,expected',[
    ('2026.DM41.4','received'),
    ('2026.PH29.2','committee_only'),
    ('2026.PH29.1','final_adopted'),
    ('2026.CC38.1','final_amended'),
])
def test_curated_cases_against_source_excerpt(item_id,expected):
    folder = ROOT / 'data' / 'items' / item_id
    cached = json.loads((folder/'card.json').read_text(encoding='utf8'))
    golden = json.loads((folder/'golden.json').read_text(encoding='utf8'))
    card = DecisionCard.model_validate(cached['card'])
    verified = verify_card(card,(folder/'item_page.txt').read_text(encoding='utf8'))
    assert all(verified['stages'])
    assert overall_status(card, verified['stages']) == expected == golden['expected_status']
    assert card.wards == golden['wards']
    assert card.participation.deadline_text is None
    assert golden['deadline_stated'] is False


def test_explanation_citations_verified():
    parts = [{'text':'short explanation','sources':[{'cited_text':'Council received item.'},
             {'cited_text':'fabricated words'}]}]
    checked = verify_explanation_segments(parts,'Council received item.')
    assert [v['verified'] for v in checked[0]['sources']] == [True, False]
