"""Provider selection and DeepSeek contracts using HTTPX's in-memory transport."""
from dataclasses import FrozenInstanceError
import io
import json
import sys
from types import SimpleNamespace

import httpx
import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from pipeline import deepseek, explain, extract
from pipeline.provider import get_config

QUOTE = 'Council received this item for information.'
URL = 'https://secure.toronto.ca/council/agenda-item.do?item=2026.TEST1.1'


@pytest.fixture(autouse=True)
def no_real_credentials(monkeypatch):
    for name in ('CIVICCLEAR_PROVIDER', 'CIVICCLEAR_MODEL', 'ANTHROPIC_API_KEY', 'DEEPSEEK_API_KEY'):
        monkeypatch.delenv(name, raising=False)


def card_payload():
    return {
        'item_id': '2026.TEST1.1', 'title': 'Sample council record', 'wards': ['All'],
        'what_is_proposed': 'A proposal', 'why': 'Information', 'who_is_affected': 'Residents',
        'stages': [{'body': 'City Council', 'date': '2026-01-01', 'stage_type': 'council_decision',
                    'outcome': 'received_for_information', 'quote': QUOTE}],
        'conditions': [],
        'participation': {'can_still_comment': 'not_stated', 'deadline_text': None, 'how': None, 'quote': None},
        'procedural_phrases': [], 'uncertainties': ['No known engagement deadline'],
    }


def explanation_payload(index=0):
    return {'segments': [{'text': 'Council received the record.',
                          'sources': [{'document_index': index, 'cited_text': QUOTE}]}]}


def completion(payload, finish_reason='stop'):
    return {'choices': [{'finish_reason': finish_reason, 'message': {'content': json.dumps(payload)}}]}


@pytest.fixture
def fake_api(monkeypatch):
    """All requests use MockTransport; no DNS lookup or network connection occurs."""
    real_client = httpx.Client
    calls = []

    def install(responses):
        pending = iter(responses)
        def handler(request):
            calls.append(request)
            result = next(pending)
            if isinstance(result, Exception):
                raise result
            if isinstance(result, tuple):
                status, body = result
            else:
                status, body = 200, result
            return httpx.Response(status, json=body)
        monkeypatch.setattr(deepseek.httpx, 'Client', lambda **kwargs: real_client(
            transport=httpx.MockTransport(handler), **kwargs))
        monkeypatch.setenv('DEEPSEEK_API_KEY', 'fake-deepseek-key')
        return calls
    return install


@pytest.mark.parametrize('env,provider,model,key_env,key', [
    ({}, 'anthropic', 'claude-opus-5-5', 'ANTHROPIC_API_KEY', ''),
    ({'DEEPSEEK_API_KEY': 'deep-key'}, 'deepseek', 'deepseek-flash', 'DEEPSEEK_API_KEY', 'deep-key'),
    ({'ANTHROPIC_API_KEY': 'claude-key'}, 'anthropic', 'claude-opus-5-5', 'ANTHROPIC_API_KEY', 'claude-key'),
    ({'ANTHROPIC_API_KEY': 'claude-key', 'DEEPSEEK_API_KEY': 'deep-key'},
     'anthropic', 'claude-opus-5-5', 'ANTHROPIC_API_KEY', 'claude-key'),
    ({'CIVICCLEAR_PROVIDER': 'deepseek', 'ANTHROPIC_API_KEY': 'claude-key', 'DEEPSEEK_API_KEY': 'deep-key'},
     'deepseek', 'deepseek-flash', 'DEEPSEEK_API_KEY', 'deep-key'),
    ({'CIVICCLEAR_PROVIDER': 'anthropic', 'DEEPSEEK_API_KEY': 'deep-key'},
     'anthropic', 'claude-opus-5-5', 'ANTHROPIC_API_KEY', ''),
    ({'CIVICCLEAR_PROVIDER': 'deepseek', 'ANTHROPIC_API_KEY': 'claude-key'},
     'deepseek', 'deepseek-flash', 'DEEPSEEK_API_KEY', ''),
    ({'CIVICCLEAR_PROVIDER': 'deepseek', 'CIVICCLEAR_MODEL': 'selected-model', 'DEEPSEEK_API_KEY': 'deep-key'},
     'deepseek', 'selected-model', 'DEEPSEEK_API_KEY', 'deep-key'),
])
def test_provider_selection(env, provider, model, key_env, key):
    config = get_config(env)
    assert (config.provider, config.model, config.key_env, config.api_key) == (provider, model, key_env, key)


def test_config_is_frozen_and_does_not_repr_the_key():
    config = get_config({'DEEPSEEK_API_KEY': 'private-test-key'})
    assert config.label == 'DeepSeek'
    assert 'private-test-key' not in repr(config)
    with pytest.raises(FrozenInstanceError):
        config.model = 'different'


def test_invalid_provider_is_rejected():
    with pytest.raises(ValueError, match='anthropic or deepseek'):
        get_config({'CIVICCLEAR_PROVIDER': 'unrecognized'})


@pytest.mark.parametrize('provider,key_env', [('anthropic', 'ANTHROPIC_API_KEY'), ('deepseek', 'DEEPSEEK_API_KEY')])
def test_missing_selected_key_blocks_both_passes(monkeypatch, provider, key_env):
    monkeypatch.setenv('CIVICCLEAR_PROVIDER', provider)
    for run in (extract.extract_card, explain.explain_with_citations):
        with pytest.raises(ValueError, match=key_env):
            run(QUOTE, None)


def test_deepseek_dispatch_and_two_pass_json_contract(fake_api, monkeypatch):
    calls = fake_api([completion(card_payload()), completion(explanation_payload())])
    monkeypatch.setitem(sys.modules, 'anthropic', SimpleNamespace(
        Anthropic=lambda **kwargs: pytest.fail('DeepSeek dispatch initialized Anthropic')))
    card = extract.extract_card(QUOTE, None)
    segments = explain.explain_with_citations(QUOTE, None, URL)
    assert card.item_id == '2026.TEST1.1'
    assert len(calls) == 2
    for request in calls:
        assert str(request.url) == 'https://api.deepseek.com/chat/completions'
        assert request.headers['authorization'] == 'Bearer fake-deepseek-key'
        body = json.loads(request.content)
        assert body['model'] == 'deepseek-flash'
        assert body['thinking'] == {'type': 'disabled'}
        assert body['response_format'] == {'type': 'json_object'}
        assert 'JSON schema:' in body['messages'][0]['content']
        assert 'JSON example:' in body['messages'][0]['content']
    assert segments == [{'text': 'Council received the record.', 'sources': [{
        'document': 'Official item page (user supplied)', 'cited_text': QUOTE,
        'document_index': 0, 'page': None, 'url': URL,
    }]}]


def test_deepseek_model_override_is_read_after_import(fake_api, monkeypatch):
    calls = fake_api([completion(card_payload())])
    monkeypatch.setenv('CIVICCLEAR_MODEL', 'custom-deepseek-model')
    extract.extract_card(QUOTE, None)
    assert json.loads(calls[0].content)['model'] == 'custom-deepseek-model'


@pytest.mark.parametrize('response', [
    {}, {'choices': []}, {'choices': [None]},
    {'choices': [{'finish_reason': 'stop', 'message': {'content': None}}]},
    {'choices': [{'finish_reason': 'stop', 'message': {'content': '   \n '}}]},
    {'choices': [{'finish_reason': 'stop', 'message': {'content': '{broken json'}}]},
    completion(card_payload(), 'length'), completion(card_payload(), 'content_filter'),
    completion({'item_id': 'missing-required-fields'}),
])
def test_incomplete_malformed_or_unvalidated_output_is_rejected(fake_api, response):
    fake_api([response])
    with pytest.raises(RuntimeError, match='DeepSeek'):
        extract.extract_card(QUOTE, None)


@pytest.mark.parametrize('response', [
    (401, {'error': {'message': 'fake-deepseek-key'}}),
    (429, {'error': {'message': 'fake-deepseek-key'}}),
    (500, {'error': {'message': 'fake-deepseek-key'}}),
    httpx.ConnectError('fake-deepseek-key'),
    httpx.ReadTimeout('fake-deepseek-key'),
])
def test_provider_errors_do_not_expose_response_or_credentials(fake_api, response):
    fake_api([response])
    with pytest.raises(RuntimeError) as error:
        extract.extract_card(QUOTE, None)
    assert 'fake-deepseek-key' not in str(error.value)


@pytest.mark.parametrize('index', [True, '0', None, -1, 2])
def test_reference_requires_a_strict_valid_document_index(fake_api, index):
    fake_api([completion(explanation_payload(index))])
    with pytest.raises(RuntimeError, match='required structure'):
        explain.explain_with_citations(QUOTE, None, URL)


def test_reference_cannot_cite_an_absent_report(fake_api):
    fake_api([completion(explanation_payload(1))])
    with pytest.raises(ValueError, match='not supplied'):
        explain.explain_with_citations(QUOTE, None, URL)


@pytest.mark.parametrize('field,value', [('url', 'https://evil.example'), ('page', 8),
                                       ('document', 'Invented report'), ('verified', True)])
def test_model_cannot_supply_trusted_reference_metadata(fake_api, field, value):
    payload = explanation_payload()
    payload['segments'][0]['sources'][0][field] = value
    fake_api([completion(payload)])
    with pytest.raises(RuntimeError, match='required structure'):
        explain.explain_with_citations(QUOTE, None, URL)


@pytest.mark.parametrize('payload', [
    {'segments': []}, {'segments': [{'text': 'Statement', 'sources': []}]},
    {'segments': [{'text': ' ', 'sources': [{'document_index': 0, 'cited_text': QUOTE}]}]},
    {'segments': [{'text': 'Statement', 'sources': [{'document_index': 0, 'cited_text': ' '}]}]},
])
def test_explanations_require_nonempty_segments_and_quotes(fake_api, payload):
    fake_api([completion(payload)])
    with pytest.raises(RuntimeError, match='required structure'):
        explain.explain_with_citations(QUOTE, None, URL)


def pdf_bytes(text=None):
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=300)
    if text is not None:
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(('BT /F1 12 Tf 20 200 Td (' + text + ') Tj ET').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def test_pdf_is_extracted_locally_and_reference_metadata_is_derived(fake_api):
    calls = fake_api([completion(explanation_payload(1))])
    report = pdf_bytes(QUOTE)
    segments = explain.explain_with_citations('Agenda context', report, URL)
    body = json.loads(calls[0].content)
    user_content = body['messages'][1]['content']
    assert QUOTE in user_content
    assert '%PDF' not in user_content
    assert 'base64' not in user_content
    assert segments[0]['sources'][0] == {
        'document': 'Staff report (user supplied)', 'document_index': 1,
        'cited_text': QUOTE, 'page': None, 'url': None,
    }


@pytest.mark.parametrize('report', [b'', b'not a PDF', pdf_bytes()])
def test_empty_unreadable_and_scanned_pdfs_fail_before_request(monkeypatch, report):
    monkeypatch.setenv('DEEPSEEK_API_KEY', 'fake-deepseek-key')
    monkeypatch.setattr(deepseek.httpx, 'Client', lambda **kwargs: pytest.fail('Unreadable PDF reached external request'))
    with pytest.raises(ValueError, match='selectable text'):
        extract.extract_card(QUOTE, report)
