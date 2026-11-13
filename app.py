"""CivicClear — public-source council decisions explained without false certainty.

Run: streamlit run app.py
Default demo uses independently linkable council source excerpts; no API key required.
Live analysis is optional and protected by an administrator password.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import date
import streamlit as st
from calculator import compare
from pipeline.clean import strip_personal_sections
from pipeline.verify import verify_card, verify_explanation_segments
from pipeline.schema import DecisionCard
from pipeline.status import overall_status, LABELS

ROOT = Path(__file__).resolve().parent
ITEMS = ROOT / 'data' / 'items'
HAVE_YOUR_SAY = 'https://www.toronto.ca/city-government/council/council-committee-meetings/have-your-say/'

st.set_page_config(page_title='CivicClear | Toronto Decisions', page_icon='🏛️', layout='wide', initial_sidebar_state='expanded')
st.markdown('''<style>
.block-container {max-width: 1120px; padding-top: 2rem}
.metric {padding: .7rem 0}
small {color: #607084}
@media print {
  section[data-testid="stSidebar"], header, footer,
  div[data-testid="stButton"] {display:none !important}
  .block-container {max-width:none; padding:0}
}
</style>''', unsafe_allow_html=True)


def _read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


@st.cache_data(show_spinner=False)
def load_demo(item_id: str):
    folder = ITEMS / item_id
    meta = _read_json(folder / 'meta.json')
    cached = _read_json(folder / 'card.json')
    explanation = _read_json(folder / 'explanation.json')
    text = (folder / 'item_page.txt').read_text(encoding='utf8')
    card = DecisionCard.model_validate(cached['card'])
    checks = verify_card(card, text)
    explanation = verify_explanation_segments(explanation, text)
    return meta, card, checks, overall_status(card, checks['stages']), explanation, cached


def _status_box(code: str):
    label = LABELS.get(code, LABELS['unclear'])
    if code in {'final_adopted', 'final_amended'}:
        st.success('**DECISION STATUS**  ·  ' + label)
    elif code == 'received':
        st.warning('**DECISION STATUS**  ·  ' + label)
    elif code == 'committee_only':
        st.info('**DECISION STATUS**  ·  ' + label)
    else:
        st.warning('**DECISION STATUS**  ·  ' + label)


def _source_link(url: str, label: str = 'Open official record'):
    if url and url.startswith(('https://www.toronto.ca/', 'https://secure.toronto.ca/')):
        st.markdown(f'[{label}]({url})')


def _show_card(card: DecisionCard, status: str, verified: dict, explanation: list[dict], meta: dict, selected_ward: str):
    st.subheader(card.title)
    st.caption('Agenda item ' + card.item_id + ' · Source review: ' + meta.get('source_checked_on', 'unknown'))
    _status_box(status)
    if meta.get('human_review', 'pending') != 'complete':
        st.caption('Source-linked demonstration. Independent team review is still required before municipal deployment.')
    if meta.get('source_mode') == 'curated_public_excerpts':
        st.caption('Evidence excerpts are curated; consult the full official agenda item and report for context.')
    with st.container(border=True):
        st.markdown('**Is this about my ward?**')
        wards = card.wards
        if selected_ward == '(Select your ward)':
            st.write('Wards listed on the record: ' + ', '.join(wards))
        elif 'All' in wards or selected_ward in wards:
            st.success('The official record includes your selected ward.')
        else:
            st.info('Your ward is not listed on the official item. The policy may still have indirect citywide effects.')
        st.caption('Ward matching uses an area selected by the visitor, not their street address.')

    st.markdown('### Council Decoder')
    with st.container(border=True):
        st.markdown('**What is proposed?**')
        st.write(card.what_is_proposed)
        st.markdown('**Why?**')
        st.write(card.why)
        st.markdown('**Who may be affected?**')
        st.write(card.who_is_affected)

    st.markdown('### Decision timeline')
    stages = card.stages
    columns = st.columns(3)
    labels = ['Staff proposal / recommendation', 'Committee action', 'City Council decision']
    stage_types = ['staff_recommendation', 'committee_decision', 'council_decision']
    for col, typ, label in zip(columns, stage_types, labels):
        with col:
            with st.container(border=True):
                st.markdown('**' + label + '**')
                matching = [(i, stage) for i, stage in enumerate(stages) if stage.stage_type == typ]
                if not matching:
                    st.caption('Not established from the selected record')
                for idx, stage in matching:
                    st.write(stage.body)
                    st.caption(stage.date or 'Date not stated')
                    if verified['stages'][idx]:
                        st.markdown('**' + stage.outcome.replace('_', ' ').title() + '**')
                        with st.expander('Verbatim decision evidence'):
                            st.write('“' + stage.quote + '”')
                            _source_link(meta.get('item_url', ''), 'Official item page')
                    else:
                        st.error('Quote not verified — this stage does not count toward the status.')

    st.markdown('### Plain-language explanation with evidence')
    for segment in explanation:
        with st.container(border=True):
            st.write(segment.get('text', ''))
            srcs = segment.get('sources') or []
            if not srcs:
                st.warning('No direct citation. Verify against official documents.')
            else:
                with st.expander(f'View original evidence ({len(srcs)} source(s))'):
                    for src in srcs:
                        st.caption(src.get('document') or 'Source')
                        st.write('“' + (src.get('cited_text') or 'No text returned') + '”')
                        if not src.get('verified', False):
                            st.warning('Source excerpt could not be verified in supplied text; check manually.')
                        if src.get('page') is not None:
                            st.caption('PDF page ' + str(src['page']))
                        _source_link(src.get('url') or meta.get('report_url' if src.get('document_index') == 1 else 'item_url', ''), 'Official source')

    st.markdown('### Procedural language')
    glossary = _read_json(ROOT / 'data' / 'glossary.json')
    for phrase in card.procedural_phrases:
        with st.expander(phrase.phrase.title()):
            st.markdown('**Plain-language definition:** ' + glossary.get(phrase.phrase.lower(), 'See the council record for context.'))
            st.markdown('**In this item:** ' + phrase.meaning_here)
            st.caption('Quoted phrase: ' + phrase.quote)
            _source_link(meta.get('item_url', ''))

    st.markdown('### Have Your Say')
    part = card.participation
    if part.can_still_comment == 'yes' and verified.get('participation'):
        st.success('This record states participation is open. Confirm the details on the official page before acting.')
    elif part.can_still_comment == 'no' and verified.get('participation'):
        st.info('The cited record says this participation period is closed.')
    else:
        st.warning('A currently open comment period or deadline has **not been verified** for this item. Do not infer a deadline from the council meeting date.')
    if part.deadline_text and verified.get('participation'):
        st.write('Official stated deadline: ' + part.deadline_text)
    if part.how and verified.get('participation'):
        st.write('Method: ' + part.how)
    st.markdown(f'[Toronto: Have Your Say — participation instructions]({HAVE_YOUR_SAY})')
    _source_link(meta.get('item_url', ''), 'Check this item for upcoming meetings / notices')
    if card.item_id == '2026.PH29.2':
        st.info('The committee requested future community consultation and Q4 2026 recommendations; this alone does not prove registration is open now.')

    st.markdown('### Important conditions and uncertainties')
    for line in card.conditions:
        st.markdown('- **Condition:** ' + line)
    for line in card.uncertainties:
        st.markdown('- **Uncertainty:** ' + line)

    if card.item_id == '2026.CC38.1':
        show_tax_calculator()
    st.divider()
    st.caption('Primary record: ' + meta.get('item_url', ''))
    _source_link(meta.get('report_url', ''), 'Related City staff report (PDF)')
    st.caption('AI-assisted explanations are informational, not legal advice. Official records and notices control. Never treat staff proposals as final Council decisions.')
    st.caption('Print: Ctrl+P / Cmd+P in your browser. A source-linked layout is included.')


def show_tax_calculator():
    st.markdown('### Before & After · 2025 → 2026 residential municipal tax')
    st.caption('Illustrative annual estimate: City municipal portion including City Building Fund; excludes education tax, fees, rebates and assessment changes.')
    rates = _read_json(ROOT / 'data' / 'tax_rates.json')['residential']
    assessed = st.number_input('MPAC assessed value (CAD)', min_value=0, max_value=100_000_000, step=10_000, value=700_000)
    before_rate, after_rate = rates['2025']['rate_percent'], rates['2026']['rate_percent']
    result = compare(assessed, before_rate, after_rate)
    c1, c2, c3 = st.columns(3)
    c1.metric('2025 municipal tax estimate', f"${result['before']:,.2f}", f'{before_rate:.6f}%')
    c2.metric('2026 municipal tax estimate', f"${result['after']:,.2f}", f'{after_rate:.6f}%')
    c3.metric('Estimated difference', f"${result['difference']:,.2f}")
    st.caption('The comparison holds the assessed value constant. This is not the actual change to a specific household’s bill.')
    for year in ('2025', '2026'):
        data = rates[year]
        st.markdown(f"[{year} official Toronto tax decision]({data['url']}) — {data['source']}")


def _read_secret(key: str) -> str:
    # st.secrets may not be configured; accessing it raises FileNotFoundError.
    try:
        value = st.secrets.get(key)
        if value:
            return str(value)
    except (FileNotFoundError, KeyError):
        pass
    return os.getenv(key, '')


def live_analysis():
    st.markdown('## Analyse a new agenda item (admin only)')
    st.write('Paste an official item page and optionally upload its staff-report PDF. This feature makes paid API requests. Input is processed for this session only.')
    password = _read_secret('CIVICCLEAR_ANALYST_PASSWORD')
    api_key = _read_secret('ANTHROPIC_API_KEY')
    if not password or not api_key:
        st.warning('Live analysis is disabled because the administrator password and/or API key has not been configured. The public demo still works.')
        return
    candidate = st.text_input('Administrator password', type='password')
    if not candidate:
        return
    import hmac
    if not hmac.compare_digest(candidate, password):
        st.error('Incorrect access code.')
        return
    item_url = st.text_input('Official agenda item URL (must be secure.toronto.ca)', placeholder='https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.2')
    item_page = st.text_area('Paste official agenda item page text', height=230)
    upload = st.file_uploader('Optional: attach official staff report PDF', type=['pdf'])
    if st.button('Run source-linked analysis', type='primary'):
        from urllib.parse import urlparse
        url = urlparse(item_url.strip())
        if url.scheme != 'https' or url.hostname != 'secure.toronto.ca' or url.path != '/council/agenda-item.do':
            st.error('Provide a Toronto TMMIS agenda item URL (not a third-party site).')
            return
        if len(item_page.strip()) < 100:
            st.error('Paste the substantive agenda item page text (at least 100 characters).')
            return
        pdf = upload.getvalue() if upload else None
        if pdf and (len(pdf) > 20_000_000 or not pdf.startswith(b'%PDF')):
            st.error('Only standard PDFs under 20 MB are supported in this prototype.')
            return
        from pipeline.extract import extract_card
        from pipeline.explain import explain_with_citations
        # Put the key in the process environment only if it was supplied via Secrets.
        os.environ['ANTHROPIC_API_KEY'] = api_key
        cleaned = strip_personal_sections(item_page)
        try:
            import anthropic
            with st.spinner('Reading sources and verifying claims...'):
                card = extract_card(cleaned, pdf)
                check = verify_card(card, cleaned, pdf)
                status = overall_status(card, check['stages'])
                explanation = verify_explanation_segments(
                    explain_with_citations(cleaned, pdf, item_url), cleaned, pdf)
        except (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError, ValueError) as exc:
            st.error('Analysis failed. Check API access, uploaded PDF, or source length and retry. No partial answer is shown.')
            return
        import re
        if not re.fullmatch(r'20\d{2}\.[A-Z]+\d+\.\d+', card.item_id):
            st.error('The returned item identifier is invalid; results have been discarded.')
            return
        if card.item_id not in item_url:
            st.error('The model returned a different agenda item identifier; results have been discarded.')
            return
        st.warning('UNREVIEWED AI OUTPUT — verify every statement and citation before reusing this analysis.')
        meta = {'item_url':item_url, 'report_url':'', 'source_checked_on':'not human reviewed', 'human_review':'pending'}
        _show_card(card, status, check, explanation, meta, '(Select your ward)')


def main():
    st.title('🏛️ CivicClear')
    st.markdown('**City council decisions, in plain language — with the original evidence.**')
    st.caption('1 · Select a real agenda item     2 · Check its decision stage and ward     3 · Open sources and participation details')
    page = st.sidebar.radio('Pages', ['Explore decisions', 'Admin: new item'])
    st.sidebar.divider()
    st.sidebar.caption('Official sources: City of Toronto Toronto Meeting Management Information System (TMMIS).')
    if page != 'Explore decisions':
        live_analysis()
        return
    item_ids = sorted(p.name for p in ITEMS.iterdir() if p.is_dir() and (p/'card.json').exists())
    descriptions = {i: _read_json(ITEMS / i / 'meta.json')['title'] for i in item_ids}
    choice = st.sidebar.selectbox('Choose an item', item_ids, format_func=lambda i: i + ' · ' + descriptions[i])
    ward_list = _read_json(ROOT / 'data' / 'wards.json')
    ward = st.sidebar.selectbox('My ward (optional)', ['(Select your ward)'] + ward_list)
    try:
        meta, card, verified, status, explanation, cached = load_demo(choice)
        _show_card(card, status, verified, explanation, meta, ward)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        st.error('Could not load this source-backed item. Check the included JSON and source files.')

if __name__ == '__main__':
    main()
