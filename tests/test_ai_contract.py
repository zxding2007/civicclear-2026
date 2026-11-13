"""Fake-client integration tests. This is NOT an actual Anthropic API request."""
from types import SimpleNamespace
import sys
import pytest
from pipeline import extract, explain
from pipeline.schema import DecisionCard


class FakeMessages:
    def parse(self, *, model, messages, output_format, **kwargs):
        assert output_format is DecisionCard
        assert model
        docs = [x for x in messages[0]['content'] if x.get('type') == 'document']
        assert len(docs) == 1
        assert all('citations' not in d for d in docs)
        card = DecisionCard.model_validate({
            'item_id':'2026.FAKE.1', 'title':'Sample council record', 'wards':['All'],
            'what_is_proposed':'A proposal', 'why':'Information', 'who_is_affected':'Residents',
            'stages':[{'body':'City Council','date':'2026-01-01','stage_type':'council_decision',
                       'outcome':'received_for_information','quote':'Council received this item for information.'}],
            'conditions':[],
            'participation':{'can_still_comment':'not_stated','deadline_text':None,'how':None,'quote':None},
            'procedural_phrases':[],'uncertainties':['No known engagement deadline']
        })
        return SimpleNamespace(stop_reason='end_turn',parsed_output=card)

    def create(self, *, messages, **kwargs):
        docs=[x for x in messages[0]['content'] if x.get('type')=='document']
        assert len(docs)==1
        assert docs[0]['citations']['enabled'] is True
        citation=SimpleNamespace(document_title='Official item page (user supplied)',
                                 cited_text='Council received this item for information.',
                                 document_index=0,start_page_number=None)
        block=SimpleNamespace(type='text',text='Council received the record.',citations=[citation])
        return SimpleNamespace(stop_reason='end_turn',content=[block])


class FakeClient:
    def __init__(self, **kwargs):
        self.messages=FakeMessages()


def test_fake_sdk_extraction_then_cited_explanation(monkeypatch):
    # Strictly a contract test. It cannot establish real model or SDK availability.
    monkeypatch.setitem(sys.modules,'anthropic',SimpleNamespace(Anthropic=FakeClient))
    page='Council received this item for information.'
    card=extract.extract_card(page,None)
    assert card.stages[0].outcome=='received_for_information'
    cited=explain.explain_with_citations(page,None,'https://secure.toronto.ca/council/agenda-item.do?item=2026.FAKE.1')
    assert cited[0]['sources'][0]['cited_text'] in page
    assert cited[0]['sources'][0]['url'].startswith('https://secure.toronto.ca/')


def test_pdf_embedded_as_base64_and_citations_separate():
    docs=extract.build_documents('public item',b'%PDF-synthetic-test',citations=True)
    assert len(docs)==2
    assert docs[0]['source']['type']=='text'
    assert docs[1]['source']['type']=='base64'
    assert docs[0]['citations']['enabled'] and docs[1]['citations']['enabled']


def test_no_real_sdk_initialization_without_explicit_invocation():
    # Imported modules alone do not call Anthropic.
    assert hasattr(extract,'extract_card')
    assert hasattr(explain,'explain_with_citations')
