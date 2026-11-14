"""Exercise the web API locally; AI requests are replaced with fake functions."""
import pytest
from fastapi.testclient import TestClient

import server
from pipeline.schema import DecisionCard

ITEM_ID = '2026.TEST1.1'
ITEM_URL = f'https://secure.toronto.ca/council/agenda-item.do?item={ITEM_ID}'
QUOTE = 'City Council received this item for information.'
PAGE = 'City Council Decision\n' + QUOTE + '\n' + ('The official record describes the proposal and its context. ' * 3)


@pytest.fixture
def client(monkeypatch):
    for name in ('CIVICCLEAR_ANALYST_PASSWORD', 'ANTHROPIC_API_KEY', 'DEEPSEEK_API_KEY',
                 'CIVICCLEAR_PROVIDER', 'CIVICCLEAR_MODEL'):
        monkeypatch.delenv(name, raising=False)
    return TestClient(server.app)


@pytest.fixture(params=['anthropic', 'deepseek'])
def enabled(client, monkeypatch, request):
    monkeypatch.setenv('CIVICCLEAR_ANALYST_PASSWORD', 'test-password')
    monkeypatch.setenv('CIVICCLEAR_PROVIDER', request.param)
    key = 'DEEPSEEK_API_KEY' if request.param == 'deepseek' else 'ANTHROPIC_API_KEY'
    monkeypatch.setenv(key, 'fake-key-never-sent')
    return request.param


def form(**overrides):
    return {'password': 'test-password', 'item_url': ITEM_URL, 'item_page': PAGE, **overrides}


def sample_card(item_id=ITEM_ID):
    return DecisionCard(
        item_id=item_id, title='Sample official decision', wards=['All'],
        what_is_proposed='A proposal', why='For consideration', who_is_affected='Residents',
        stages=[{'body': 'City Council', 'date': '2026-01-01',
                 'stage_type': 'council_decision', 'outcome': 'received_for_information', 'quote': QUOTE}],
        conditions=[], participation={'can_still_comment': 'not_stated', 'deadline_text': None,
                                      'how': None, 'quote': None},
        procedural_phrases=[], uncertainties=['No participation deadline established.'],
    )


def test_bootstrap_serves_verified_records_and_runtime(client):
    response = client.get('/api/bootstrap')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 4
    assert data['runtime'] == {
        'mode': 'connected', 'analysis_enabled': False, 'analysis_provider': 'anthropic',
    }
    assert all(all(item['checks']['stages']) for item in data['items'])
    assert data['tax']['example']['difference'] == 92.57
    assert client.get('/api/health').json() == {'status': 'ok'}


def test_bootstrap_exposes_configuration_without_secrets(client, enabled):
    response = client.get('/api/bootstrap')
    assert response.json()['runtime']['analysis_enabled'] is True
    assert response.json()['runtime']['analysis_provider'] == enabled
    assert 'fake-key-never-sent' not in response.text
    assert 'test-password' not in response.text


def test_website_and_unknown_api_are_separate(client):
    assert 'text/html' in client.get('/').headers['content-type']
    response = client.get('/api/not-a-route')
    assert response.status_code == 404
    assert response.json() == {'detail': 'API endpoint not found.'}


def test_workspace_destinations_are_separate_html_documents(client):
    pages = {
        '/index.html': 'overview', '/decisions.html': 'decisions',
        '/decision.html?id=2026.PH29.2': 'decision', '/calculator.html': 'calculator',
        '/sources.html': 'sources', '/analyse.html': 'analyse',
    }
    for path, page in pages.items():
        response = client.get(path)
        assert response.status_code == 200
        assert f'data-page="{page}"' in response.text
        assert 'href="decisions.html"' in response.text
        assert 'href="#/' not in response.text
        assert '{{title}}' not in response.text


def test_tax_uses_python_calculator(client):
    response = client.post('/api/tax', json={'assessed_value': 700000})
    assert response.status_code == 200
    assert response.json() == {
        'assessed_value': 700000, 'before': 4207.61, 'after': 4300.18, 'difference': 92.57,
        'rates': {'2025': 0.601087, '2026': 0.614311},
    }


@pytest.mark.parametrize('value', [-1, 100000001, '700000', True, None])
def test_tax_rejects_invalid_values(client, value):
    assert client.post('/api/tax', json={'assessed_value': value}).status_code == 422


@pytest.mark.parametrize('value', ['NaN', 'Infinity', '-Infinity'])
def test_tax_rejects_nonfinite_values_without_echoing_them(client, value):
    response = client.post('/api/tax', content='{"assessed_value":' + value + '}',
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 422
    assert all('input' not in detail for detail in response.json()['detail'])


def test_analysis_is_disabled_without_credentials(client, monkeypatch):
    def no_api(*args):
        pytest.fail('A disabled endpoint must not call the model')
    monkeypatch.setattr(server, 'extract_card', no_api)
    assert client.post('/api/analyse', data=form()).status_code == 503


def test_analysis_rejects_bad_password_before_ai(client, enabled, monkeypatch):
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Unauthorized API call'))
    response = client.post('/api/analyse', data=form(password='incorrect'))
    assert response.status_code == 401


@pytest.mark.parametrize('url', [
    'https://secure.toronto.ca.evil.example/council/agenda-item.do?item=2026.TEST1.1',
    'https://attacker@secure.toronto.ca/council/agenda-item.do?item=2026.TEST1.1',
    'http://secure.toronto.ca/council/agenda-item.do?item=2026.TEST1.1',
    'https://secure.toronto.ca/other?item=2026.TEST1.1',
    ITEM_URL + '&item=2026.TEST1.2',
    ITEM_URL + 'suffix',
    ITEM_URL + '#another-item',
])
def test_analysis_rejects_nonofficial_or_ambiguous_urls(client, enabled, monkeypatch, url):
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Invalid input reached API'))
    assert client.post('/api/analyse', data=form(item_url=url)).status_code == 422


def test_analysis_requires_substantive_cleaned_text(client, enabled, monkeypatch):
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Invalid input reached API'))
    response = client.post('/api/analyse', data=form(item_page='Communications\n' + ('Private name ' * 20)))
    assert response.status_code == 422


def test_analysis_rejects_invalid_and_oversized_pdf(client, enabled, monkeypatch):
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Invalid input reached API'))
    response = client.post('/api/analyse', data=form(), files={'report': ('report.pdf', b'not a pdf', 'application/pdf')})
    assert response.status_code == 422
    monkeypatch.setattr(server, 'MAX_PDF_BYTES', 10)
    response = client.post('/api/analyse', data=form(), files={'report': ('report.pdf', b'%PDF' + b'x' * 10, 'application/pdf')})
    assert response.status_code == 413


def test_analysis_returns_verified_unreviewed_item(client, enabled, monkeypatch):
    def extract(text, pdf):
        assert 'Private person' not in text
        assert pdf is None
        return sample_card()
    def explain(text, pdf, item_url):
        assert item_url == ITEM_URL
        return [{'text': 'The item was received.', 'sources': [{'cited_text': QUOTE, 'url': item_url}]}]
    monkeypatch.setattr(server, 'extract_card', extract)
    monkeypatch.setattr(server, 'explain_with_citations', explain)
    response = client.post('/api/analyse', data=form(item_page=PAGE + '\nCommunications\nPrivate person'))
    assert response.status_code == 200
    item = response.json()
    assert item['id'] == ITEM_ID
    assert item['status'] == 'received'
    assert item['checks']['stages'] == [True]
    assert item['explanation'][0]['sources'][0]['verified'] is True
    assert item['meta']['human_review'] == 'pending'
    assert item['meta']['source_checked_on'] is None
    assert item['meta']['generation_mode'] == 'ai_unreviewed'
    assert item['meta']['ai_provider'] == enabled
    assert item['meta']['ai_model']
    assert item['evidence'] is None


def test_analysis_rejects_model_item_mismatch(client, enabled, monkeypatch):
    monkeypatch.setattr(server, 'extract_card', lambda *args: sample_card('2026.TEST1.2'))
    monkeypatch.setattr(server, 'explain_with_citations', lambda *args: pytest.fail('Mismatched item reached second API call'))
    response = client.post('/api/analyse', data=form())
    assert response.status_code == 502
    assert 'different agenda item' in response.json()['detail']


def test_analysis_does_not_expose_provider_errors(client, enabled, monkeypatch):
    def fail(*args):
        raise RuntimeError('fake-key-never-sent private source text')
    monkeypatch.setattr(server, 'extract_card', fail)
    response = client.post('/api/analyse', data=form())
    assert response.status_code == 502
    assert 'fake-key-never-sent' not in response.text
    assert 'private source text' not in response.text


def test_deepseek_key_alone_enables_selected_provider(client, monkeypatch):
    monkeypatch.setenv('CIVICCLEAR_ANALYST_PASSWORD', 'test-password')
    monkeypatch.setenv('DEEPSEEK_API_KEY', 'private-deepseek-key')
    response = client.get('/api/bootstrap')
    assert response.json()['runtime'] == {
        'mode': 'connected', 'analysis_enabled': True, 'analysis_provider': 'deepseek',
    }
    assert 'private-deepseek-key' not in response.text


@pytest.mark.parametrize('provider', ['deepseek', 'unsupported'])
def test_selected_provider_cannot_use_another_providers_key(client, monkeypatch, provider):
    monkeypatch.setenv('CIVICCLEAR_ANALYST_PASSWORD', 'test-password')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'private-anthropic-key')
    monkeypatch.setenv('CIVICCLEAR_PROVIDER', provider)
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Wrong provider key reached model'))
    response = client.get('/api/bootstrap')
    assert response.json()['runtime']['analysis_enabled'] is False
    assert response.json()['runtime']['analysis_provider'] == ('deepseek' if provider == 'deepseek' else None)
    assert client.post('/api/analyse', data=form()).status_code == 503


def test_deepseek_rejects_unreadable_report_before_model(client, monkeypatch):
    import io
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    output = io.BytesIO()
    writer.write(output)
    monkeypatch.setenv('CIVICCLEAR_ANALYST_PASSWORD', 'test-password')
    monkeypatch.setenv('DEEPSEEK_API_KEY', 'unused-test-key')
    monkeypatch.setattr(server, 'extract_card', lambda *args: pytest.fail('Unreadable report reached model'))
    response = client.post('/api/analyse', data=form(), files={'report': ('scan.pdf', output.getvalue(), 'application/pdf')})
    assert response.status_code == 422
    assert 'selectable text' in response.json()['detail']
