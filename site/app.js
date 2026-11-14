/* Shared behaviour for CivicClear's separate HTML pages.
   Ordinary links load documents; Python supplies data and calculations when available. */
(function () {
  'use strict';
  const view = document.getElementById('view');
  const page = document.body.dataset.page || 'overview';
  const wardSelect = document.getElementById('ward-select');
  let data, connected = false, loadNotice = '', updateWardFilter = null, updateWardContext = null;
  const STATUS = {
    final_adopted: ['Council adopted', 'yes', 'Adopted by City Council'],
    final_amended: ['Adopted with changes', 'yes', 'Adopted with amendments by City Council'],
    committee_only: ['Committee only', 'wait', 'Committee action, not final Council approval'],
    received: ['Received only', 'no', 'Received for information, not an approval'],
    recommendation_only: ['Staff recommendation', 'wait', 'Staff recommendation only'],
    referred: ['Referred', 'wait', 'Referred for further consideration'],
    deferred: ['Deferred', 'wait', 'Decision deferred'],
    not_adopted: ['Not adopted', 'no', 'Not adopted'],
    unclear: ['Unclear', 'no', 'Status unclear; check the official record']
  };
  const ICONS = {
    record: '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6M8 13h8M8 17h5"/>',
    arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    chat: '<path d="M21 11a8 8 0 0 1-8 8H4l-3 3V11a10 10 0 0 1 20 0ZM7 10h10M7 14h6"/>',
    calculator: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h1m6 0h1m-8 4h1m6 0h1"/>',
    shield: '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6zM8 12l3 3 5-6"/>',
    search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'
  };
  // Escape all record fields before inserting markup. URLs have a separate allowlist.
  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function icon(name) { return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[name] || ICONS.record) + '</svg>'; }
  function status(item) { return STATUS[item.status] || STATUS.unclear; }
  function chip(item) { const s = status(item); return '<span class="chip chip--' + s[1] + '">' + esc(s[0]) + '</span>'; }
  function officialLink(url, label, cls) {
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== 'https:' || !/(^|\.)toronto\.ca$/.test(parsed.hostname)) return esc(label);
      return '<a class="' + (cls || '') + '" href="' + esc(parsed.href) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + ' <span aria-hidden="true">↗</span></a>';
    } catch (_) { return esc(label); }
  }
  function detailUrl(item) { return 'decision.html?id=' + encodeURIComponent(item.id); }
  function money(value) { return Number(value).toLocaleString('en-CA', {style:'currency',currency:'CAD'}); }
  function niceDate(value) {
    if (!value) return 'Not established';
    const m = /^(\d{4})-(\d{2})-(\d{2})(?:\/(\d{2}))?$/.exec(value);
    if (!m) return esc(value);
    const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    return months[+m[2]-1] + ' ' + +m[3] + (m[4] ? ' and ' + +m[4] : '') + ', ' + m[1];
  }
  function today() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
  }
  function isOpen(item) {
    return item.card.participation.can_still_comment === 'yes' && item.checks.participation === true &&
      Boolean(item.meta.participation_end_date) && today() <= item.meta.participation_end_date;
  }
  function matchesWard(item) { return !wardSelect.value || item.card.wards.includes('All') || item.card.wards.includes(wardSelect.value); }
  function wards(item) { return item.card.wards.includes('All') ? 'Citywide · All wards' : 'Ward ' + item.card.wards.join(', '); }
  function wardContext(item) {
    if (!wardSelect.value) return 'Select a ward to check whether the official record lists it. Indirect effects are still possible beyond the listed wards.';
    if (item.card.wards.includes('All')) return 'This is a citywide record. It includes your selected ward, but individual impacts may differ.';
    return matchesWard(item) ? 'Your selected ward is listed in the record. This does not establish your individual impact.' : 'This ward is not listed in the record. Indirect effects are still possible.';
  }
  function demoDisclosure() {
    return '<div class="demo-disclosure"><strong>Pre-generated demo data</strong><span>Browsing these examples does not call AI. Automated source checks have run; independent human review is pending.</span></div>';
  }
  function header(title, intro, eyebrow) {
    return '<div class="page-heading"><p class="eyebrow">' + esc(eyebrow || 'YOUR CITY, MADE CLEAR') + '</p><h1>' + esc(title) + '</h1><p>' + esc(intro) + '</p></div>';
  }
  function notice() {
    if (!loadNotice) return '';
    return '<div class="callout callout--info" role="status">' + esc(loadNotice) + ' <button class="btn btn-quiet" type="button" id="retry-connection">Try connection again</button></div>';
  }
  function mount(html) {
    view.innerHTML = notice() + html;
    const retry = document.getElementById('retry-connection');
    if (retry) retry.addEventListener('click', () => window.location.reload());
  }
  function row(item, summary) {
    return '<a class="decision-row" href="' + detailUrl(item) + '"><span class="icon-box">' + icon('record') + '</span>' +
      '<div class="row-content"><span class="row-title">' + esc(item.short_title) + '</span><span class="row-meta"><code>' + esc(item.id) + '</code><span>·</span><span>' + esc(wards(item)) + '</span></span>' +
      (summary ? '<p class="row-summary">' + esc(item.card.what_is_proposed) + '</p>' : '') + '</div>' + chip(item) + icon('arrow') + '</a>';
  }
  function statCard(label, value, detail, symbol) {
    return '<div class="stat-card"><p>' + esc(label) + '</p><span class="icon-box">' + icon(symbol) + '</span><strong>' + value + '</strong><small>' + esc(detail) + '</small></div>';
  }
  function overview() {
    const openItems = data.items.filter(isOpen);
    const council = data.items.filter(i => i.card.stages.some((s,n) => s.stage_type === 'council_decision' && i.checks.stages[n]));
    const relevant = wardSelect.value ? data.items.filter(matchesWard) : data.items;
    mount(header('A clearer view of Toronto.', 'Understand what was decided, what it means, and where your voice can count.') +
      demoDisclosure() +
      '<div class="stat-grid">' + statCard('Decision records', data.items.length, 'Curated Toronto examples', 'record') +
      statCard('Council outcomes', council.length, 'Including received-only items', 'shield') +
      statCard('Open feedback', openItems.length, 'Based on cited participation dates', 'chat') + '</div>' +
      '<div class="content-grid"><div class="view-stack"><section class="panel"><div class="section-title"><h2>' + (wardSelect.value ? 'Records naming your ward or citywide' : 'Explore city decisions') + '</h2><a href="decisions.html">View all decisions →</a></div><div class="decision-list">' +
      (relevant.length ? relevant.map(i => row(i,false)).join('') : '<p class="muted">None of these examples names your ward. Citywide records still apply.</p>') +
      '</div></section><section class="overview-note"><span class="icon-box">' + icon('shield') + '</span><div><strong>The decision is only part of the story.</strong><p>Staff recommendations, committee actions, and final Council decisions are different steps. We keep them separate so you can see where things stand.</p><a href="sources.html">Understand the process →</a></div></section></div>' +
      '<aside><section class="panel toolkit-panel"><p class="eyebrow">YOUR CIVIC TOOLKIT</p><span class="icon-box">' + icon('calculator') + '</span><h2>Put the numbers in context.</h2><p>Compare Toronto’s 2025 and 2026 municipal property tax at the same assessed value.</p><a class="btn btn-secondary" href="calculator.html">Open tax calculator ' + icon('arrow') + '</a></section>' +
      (openItems.length ? '<section class="panel feedback-panel"><span class="chip chip--here">Have your say</span><h3>' + esc(openItems[0].short_title) + '</h3><p>Feedback is advertised through ' + niceDate(openItems[0].meta.participation_end_date) + '. Check the City portal before submitting.</p><a href="' + detailUrl(openItems[0]) + '&tab=participation">See participation details →</a></section>' : '') +
      '<section class="panel"><h3>One phrase, decoded.</h3><dl class="info-list"><div><dt>“Received for information”</dt><dd>Council took note of the item. That does not mean it approved the proposal.</dd></div></dl></section></aside></div>' +
      '<p class="collection-note">These examples are not a live feed of all Council business. A ward missing from a record may still experience indirect effects.</p>');
  }
  function decisions() {
    mount(header('Explore decisions', 'Find a record, follow its decision timeline, and check the original evidence.', 'DECISION EXPLORER') +
      demoDisclosure() +
      '<div class="toolbar"><div class="field"><label for="decision-search">Search decisions</label><input id="decision-search" type="search" placeholder="Search a topic, title or agenda ID"></div>' +
      '<div class="field"><label for="status-filter">Decision status</label><select id="status-filter"><option value="">All statuses</option>' + [...new Set(data.items.map(i => i.status))].map(s => '<option value="' + s + '">' + esc(STATUS[s][0]) + '</option>').join('') + '</select></div>' +
      '<label><input id="ward-only" type="checkbox" ' + (wardSelect.value ? '' : 'disabled') + '> Names my ward or citywide</label></div>' +
      '<section class="panel"><div class="section-title"><h2>Decision records</h2><span id="result-count" class="muted" role="status"></span></div><div id="decision-results" class="decision-list"></div></section>' +
      '<p class="collection-note">This filter uses wards named in the official record. A ward that is not listed may still experience indirect effects.</p>');
    const search = document.getElementById('decision-search'), filter = document.getElementById('status-filter'), wardOnly = document.getElementById('ward-only');
    function update() {
      const q = search.value.trim().toLowerCase();
      const items = data.items.filter(i => (!filter.value || i.status === filter.value) && (!wardOnly.checked || matchesWard(i)) &&
        [i.id,i.card.title,i.card.what_is_proposed,i.card.who_is_affected,wards(i)].join(' ').toLowerCase().includes(q));
      document.getElementById('result-count').textContent = items.length + ' of ' + data.items.length + ' records';
      document.getElementById('decision-results').innerHTML = items.length ? items.map(i => row(i,true)).join('') : '<div class="empty-state">' + icon('search') + '<h2>No matching decisions</h2><p>Try a different search, status, or ward.</p><button id="clear-filters" class="btn btn-secondary">Clear filters</button></div>';
      const clear = document.getElementById('clear-filters');
      if (clear) clear.addEventListener('click', () => { search.value=''; filter.value=''; wardOnly.checked=false; update(); search.focus(); });
    }
    search.addEventListener('input',update); filter.addEventListener('change',update); wardOnly.addEventListener('change',update);
    updateWardFilter=()=>{wardOnly.disabled=!wardSelect.value;if(wardOnly.disabled)wardOnly.checked=false;update();};
    update();
  }
  function claim(item, field) {
    const evidence = item.evidence && item.evidence.claims[field];
    if (!evidence) return '';
    return '<details><summary>Source for this claim</summary><blockquote class="source-quote">' + esc(evidence.excerpt) + '</blockquote><p>' + esc(evidence.note) + '</p>' + officialLink(evidence.source_url,evidence.source_name) + '</details>';
  }
  function timeline(item) {
    return '<section class="panel"><div class="panel-header"><h2>The decision timeline</h2><span class="muted">Three distinct steps</span></div><div class="timeline">' +
      [['staff_recommendation','Staff recommendation'],['committee_decision','Committee action'],['council_decision','City Council decision']].map(([type,title],n) => {
        const stages = item.card.stages.map((s,i) => ({...s,verified:item.checks.stages[i]})).filter(s => s.stage_type===type);
        return '<div class="timeline-step"><span class="step-number">' + (n+1) + '</span><h3>' + title + '</h3>' +
          (stages.length ? stages.map(s => '<p>' + esc(s.body) + '</p><span class="chip chip--' + (s.verified ? 'yes':'no') + '">' + (s.verified ? esc(s.outcome.replace(/_/g,' ')) : 'Quote not verified') + '</span><p>' + niceDate(s.date) + '</p><details><summary>Original wording</summary><blockquote>' + esc(s.quote) + '</blockquote></details>').join('') : '<p>Not established from this record.</p>') + '</div>';
      }).join('') + '</div></section>';
  }
  function participation(item) {
    const p = item.card.participation, valid = item.checks.participation;
    let title='A current comment period is not verified', text='Do not infer a participation deadline from the meeting date. Check the City’s current notice for opportunities to take part.';
    if (isOpen(item)) { title='An opportunity to have your say'; text='The linked City portal advertises public feedback. Confirm the form is still open before submitting.'; }
    else if (valid && p.can_still_comment === 'yes' && item.meta.participation_end_date && today() > item.meta.participation_end_date) { title='The cited feedback period has passed'; text='Check the City project page for an extension or a new opportunity.'; }
    else if (valid && p.can_still_comment === 'no') { title='The cited participation period is closed'; text='Check the City’s current notices for further opportunities.'; }
    return '<section class="panel"><span class="chip chip--' + (isOpen(item)?'here':'no') + '">' + (isOpen(item)?'Have your say':'Participation') + '</span><h2 style="margin-top:16px">' + title + '</h2><p>' + text + '</p>' +
      (valid && p.deadline_text ? '<p><strong>Stated deadline:</strong> ' + esc(p.deadline_text) + '</p>' : '') +
      (valid && p.how ? '<p><strong>How to participate:</strong> ' + esc(p.how) + '</p>' : '') + claim(item,'participation') +
      '<div class="page-actions">' + (item.meta.participation_source_url ? officialLink(item.meta.participation_source_url,'Open the feedback portal','btn btn-primary') : '') + officialLink(data.have_your_say_url,'City participation instructions','btn btn-secondary') + '</div>' +
      (item.meta.consultation_project_url ? '<p>' + officialLink(item.meta.consultation_project_url,'City project updates') + '</p>' : '') +
      (item.id==='2026.PH29.2' ? '<p class="form-help">The April committee request anticipated Q4 2026. A separate City project update anticipates a final report in Q1 2027. These are plans, not final Council adoption.</p>' : '') + '</section>';
  }
  function sourceContent(item) {
    return '<section class="panel"><h2>Explanations and original evidence</h2><p>“Quote found” means the words occur in the supplied source. It does not confirm every interpretation.</p><ul class="source-list">' +
      (item.explanation || []).map(seg => '<li><p>' + esc(seg.text) + '</p>' + (seg.sources || []).map(s => '<blockquote class="source-quote">' + esc(s.cited_text) + '</blockquote><span class="chip chip--' + (s.verified?'yes':'wait') + '">' + (s.verified?'Quote found':'Quote not verified') + '</span> ' + officialLink(s.url || (s.document_index === 1 ? item.meta.report_url : item.meta.item_url),s.document || 'Supplied source') + (s.page ? '<small>PDF page ' + esc(s.page) + '</small>' : '')).join('') + (!(seg.sources || []).length?'<p class="form-help">No direct citation. Check the official source.</p>':'') + '</li>').join('') +
      '</ul><div class="page-actions">' + officialLink(item.meta.item_url,'Open official agenda item','btn btn-secondary') + (item.meta.report_url ? officialLink(item.meta.report_url,'Read staff report','btn btn-secondary') : '') + '</div></section>';
  }
  function detail(item, preview) {
    const card=item.card, s=status(item), pending=item.meta.human_review!=='complete';
    const matchedStages=item.checks.stages.filter(Boolean).length;
    const content = '<a class="btn btn-quiet" href="decisions.html">← All decisions</a>' + header(card.title,wards(item),'AGENDA ITEM ' + item.id) +
      '<div class="status-banner">' + chip(item) + '<strong> ' + esc(s[2]) + '</strong></div>' +
      (isOpen(item) ? '<section class="feedback-action" aria-labelledby="feedback-heading"><div><p class="eyebrow">HAVE YOUR SAY</p><h2 id="feedback-heading">Feedback advertised through ' + niceDate(item.meta.participation_end_date) + '</h2><p>Check the City portal to confirm the form is still open.</p></div><div class="feedback-actions">' + officialLink(item.meta.participation_source_url,'Give feedback','btn btn-primary') + '<button class="btn btn-secondary" id="participation-details" type="button">Participation details</button></div></section>' : '') +
      '<p id="ward-context" class="ward-context" aria-live="polite">' + esc(wardContext(item)) + '</p>' +
      (preview ? '<div class="callout" role="status"><strong>Unreviewed AI preview.</strong> Verify every statement against the official sources. This result has not been saved or published.</div>' : '') +
      timeline(item) + '<div class="tabs" role="tablist" aria-label="Decision details">' +
      [['decision','The decision'],['impact','Who it affects'],['participation','Have your say'],['sources','Sources'],['unknowns','Unknowns']].map(([id,label],n) => '<button class="tab" id="tab-' + id + '" type="button" role="tab" aria-controls="panel-' + id + '" aria-selected="' + (n===0) + '" tabindex="' + (n===0?'0':'-1') + '">' + label + '</button>').join('') + '</div>' +
      '<section id="panel-decision" role="tabpanel" aria-labelledby="tab-decision"><div class="detail-grid"><div class="view-stack"><section class="panel"><h2>What is proposed?</h2><p>' + esc(card.what_is_proposed) + '</p>' + claim(item,'what_is_proposed') + '</section><section class="panel"><h2>Why is it proposed?</h2><p>' + esc(card.why) + '</p>' + claim(item,'why') + '</section></div><aside><section class="panel"><h3>About this record</h3><dl class="info-list"><div><dt>Record origin</dt><dd>' + (preview?'Unreviewed AI preview':'Pre-generated demo data; no AI call on viewing') + '</dd></div><div><dt>Automated quotation checks</dt><dd>' + matchedStages + ' of ' + item.checks.stages.length + ' stage quotations matched. Status is calculated from matching stages.</dd></div><div><dt>Source check date</dt><dd>' + (item.meta.source_checked_on?niceDate(item.meta.source_checked_on):'Not yet human reviewed') + '</dd></div><div><dt>Independent human review</dt><dd>' + (pending?'Pending':'Complete') + '</dd></div><div><dt>Location</dt><dd>' + esc(wards(item)) + '</dd></div></dl><div class="page-actions">' + officialLink(item.meta.item_url,'Official record','btn btn-secondary') + '</div></section>' +
      (card.procedural_phrases.length?'<section class="panel"><h3>Words to know</h3><dl class="info-list">' + card.procedural_phrases.map(p => '<div><dt>' + esc(p.phrase) + '</dt><dd>' + esc(p.meaning_here) + '</dd></div>').join('') + '</dl></section>':'') + '</aside></div></section>' +
      '<section id="panel-impact" role="tabpanel" aria-labelledby="tab-impact" hidden><div class="view-stack"><section class="panel"><h2>Who may be affected?</h2><p>' + esc(card.who_is_affected) + '</p>' + claim(item,'who_is_affected') + '</section>' +
      ((item.evidence && item.evidence.impacts)||[]).map(i => '<section class="panel"><h3>' + esc(i.audience) + '</h3><p><strong>Official priority:</strong> ' + esc(i.grounded_priority) + '</p><p><strong>Possible effect:</strong> ' + esc(i.potential_effect) + '</p><p><strong>Question to consider:</strong> ' + esc(i.question) + '</p>' + claim(item,i.claim_ref) + '</section>').join('') + '<p class="form-help">Stakeholder considerations are not measured impacts or promises.</p></div></section>' +
      '<section id="panel-participation" role="tabpanel" aria-labelledby="tab-participation" hidden>' + participation(item) + '</section>' +
      '<section id="panel-sources" role="tabpanel" aria-labelledby="tab-sources" hidden>' + sourceContent(item) + '</section>' +
      '<section id="panel-unknowns" role="tabpanel" aria-labelledby="tab-unknowns" hidden><section class="panel"><h2>Conditions and uncertainties</h2><ul>' + [...card.conditions,...card.uncertainties,...((item.evidence&&item.evidence.tradeoffs)||[])].map(t => '<li>' + esc(t) + '</li>').join('') + '</ul>' + claim(item,'conditions') + '</section></section>';
    mount(content);
    updateWardContext=()=>{document.getElementById('ward-context').textContent=wardContext(item);};
    document.title=card.title+' · CivicClear';
    const tabs=[...view.querySelectorAll('[role="tab"]')];
    function selectTab(index,focus) {
      tabs.forEach((t,n) => { t.setAttribute('aria-selected',String(n===index)); t.tabIndex=n===index?0:-1; document.getElementById(t.getAttribute('aria-controls')).hidden=n!==index; });
      if(focus) tabs[index].focus();
    }
    tabs.forEach((t,n) => {
      t.addEventListener('click',()=>selectTab(n,false));
      t.addEventListener('keydown',e=>{ let next=n; if(e.key==='ArrowRight') next=(n+1)%tabs.length; else if(e.key==='ArrowLeft') next=(n+tabs.length-1)%tabs.length; else if(e.key==='Home') next=0; else if(e.key==='End') next=tabs.length-1; else return; e.preventDefault(); selectTab(next,true); });
    });
    const participationDetails=document.getElementById('participation-details');
    if(participationDetails)participationDetails.addEventListener('click',()=>selectTab(2,true));
    const requested=new URLSearchParams(location.search).get('tab');
    if(requested){ const index=tabs.findIndex(t=>t.id==='tab-'+requested); if(index>=0) selectTab(index,false); }
  }
  function calculator() {
    const rates=data.tax.residential;
    mount(header('Put your property tax in perspective.', 'Compare the municipal portion of your property tax at the same MPAC assessed value.', 'TAX CALCULATOR · 2025 TO 2026') +
      '<div class="calculator-grid"><section class="panel"><h2>Your assessed property value</h2><p>Use the MPAC assessment, which may differ from your home’s market value.</p><form id="tax-form"><div class="field"><label for="assessed-value">MPAC assessed value (CAD)</label><div class="money-input"><span aria-hidden="true">$</span><input id="assessed-value" name="assessed_value" inputmode="numeric" value="700,000" required aria-describedby="tax-help tax-error"></div><small id="tax-help" class="muted">Enter a whole-dollar amount from $0 to $100,000,000.</small></div><button class="btn btn-primary" type="submit" id="tax-submit">Calculate comparison ' + icon('arrow') + '</button><p id="tax-error" class="form-error" role="alert" hidden></p></form>' +
      '<div id="tax-results" aria-live="polite"></div></section><aside class="view-stack"><section class="panel"><h3>What this comparison includes</h3><dl class="info-list"><div><dt>Municipal property tax</dt><dd>The City’s residential rate, including the City Building Fund.</dd></div><div><dt>The same assessed value</dt><dd>We hold your assessment constant to isolate the change in municipal rates.</dd></div><div><dt>What is excluded</dt><dd>Education tax, fees, rebates, assessment changes, and other adjustments to your actual bill.</dd></div></dl></section><section class="panel"><h3>The rates behind the numbers</h3><dl class="info-list">' +
      ['2025','2026'].map(y=>'<div><dt>'+y+' · '+esc(rates[y].rate_percent)+'%</dt><dd>'+officialLink(rates[y].url,'Official '+y+' tax decision')+(rates[y].bylaw_url?'<br>'+officialLink(rates[y].bylaw_url,rates[y].bylaw_label):'')+'</dd></div>').join('') + '</dl><p class="form-help">Includes City Building Fund; excludes education tax. This comparison is not the actual change to a specific household’s tax bill.</p></section></aside></div>');
    const input=document.getElementById('assessed-value'), error=document.getElementById('tax-error'), submit=document.getElementById('tax-submit'), results=document.getElementById('tax-results');
    let requestNumber=0;
    function localTax(value,rate){ return Math.floor((value*Math.round(rate*1e6)+500000)/1e6)/100; }
    function validAmount(raw){ return /^\d+$/.test(raw) && Number(raw)<=100000000; }
    function clearEstimate(valid){
      results.innerHTML='<p class="form-help">'+(valid?'Select Calculate comparison to update your estimate.':'Enter a valid assessed value to calculate.')+'</p>';
      results.removeAttribute('aria-busy');
      if(valid)input.removeAttribute('aria-invalid');else input.setAttribute('aria-invalid','true');
    }
    async function calculate(event){
      if(event) event.preventDefault();
      const number=++requestNumber, raw=input.value.replace(/[\s,$]/g,'');
      error.hidden=true;
      if(!validAmount(raw)){ error.textContent='Enter a whole-dollar amount between $0 and $100,000,000.'; error.hidden=false; clearEstimate(false); return; }
      input.removeAttribute('aria-invalid'); const value=Number(raw);
      submit.disabled=true;
      results.setAttribute('aria-busy','true');
      try{
        let result;
        if(connected){
          const response=await fetch('api/tax',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({assessed_value:value})});
          if(!response.ok) throw new Error('The comparison could not be calculated. Please try again.');
          result=await response.json();
        }else{
          const before=localTax(value,rates['2025'].rate_percent),after=localTax(value,rates['2026'].rate_percent);
          result={before,after,difference:Math.round((after-before)*100)/100};
        }
        if(number!==requestNumber)return;
        const max=Math.max(result.before,result.after)||1;
        results.innerHTML='<div class="result-grid"><div class="result-card"><p>2025 municipal estimate</p><strong>'+money(result.before)+'</strong><small>per year</small></div><div class="result-card"><p>2026 municipal estimate</p><strong>'+money(result.after)+'</strong><small>per year</small></div></div><div class="result-bars">'+
          [['2025',result.before],['2026',result.after]].map(([y,v])=>'<div class="result-bar"><span>'+y+'</span><div class="bar-track"><div class="bar-fill" style="width:'+(v/max*100).toFixed(2)+'%"></div></div></div>').join('')+
          '</div><div class="tax-difference"><strong>'+(result.difference>=0?'+':'−')+money(Math.abs(result.difference))+' a year</strong><p class="muted">About '+money(Math.abs(result.difference)/12)+' '+(result.difference>=0?'more':'less')+' per month at this assessed value.</p></div><p class="form-help">'+(connected?'Calculated using the connected Python calculator.':'Calculated locally using the saved official rates.')+'</p>';
      }catch(e){if(number===requestNumber){error.textContent=e.message;error.hidden=false;results.innerHTML='';}}
      finally{if(number===requestNumber){submit.disabled=false;results.removeAttribute('aria-busy');}}
    }
    document.getElementById('tax-form').addEventListener('submit',calculate);
    input.addEventListener('input',()=>{requestNumber++;submit.disabled=false;error.hidden=true;clearEstimate(validAmount(input.value.replace(/[\s,$]/g,'')));});
    calculate();
  }
  function sources() {
    mount(header('Follow the evidence.', 'Understand where the records come from, how they are checked, and what remains uncertain.', 'SOURCES & METHOD')+
      demoDisclosure()+
      '<div class="content-grid"><div class="view-stack"><section class="panel"><h2>How a decision becomes a clear explanation</h2><ol class="method-list"><li><strong>Start with the City’s record</strong><p>Each example includes selected excerpts from official Toronto agenda and project pages, with links to the full source.</p></li><li><strong>Keep the stages separate</strong><p>Staff recommendations, committee actions, and Council decisions retain their own outcomes and evidence.</p></li><li><strong>Check the supporting words</strong><p>Source quotations are matched against the saved text. Only stages with matching quotations contribute to the displayed decision status.</p></li><li><strong>Leave room for uncertainty</strong><p>A quote match does not establish context or prove an interpretation. Human review remains necessary.</p></li></ol></section><section class="panel"><h2>Official records in this collection</h2><ul class="source-list">'+
      data.items.map(i=>'<li><h3>'+esc(i.short_title)+'</h3><p class="row-meta">'+esc(i.id)+' · Source check '+niceDate(i.meta.source_checked_on)+'</p>'+officialLink(i.meta.item_url,'City agenda item')+(i.meta.report_url?' · '+officialLink(i.meta.report_url,'Staff report (PDF)'):'')+'<small>Independent team review: '+esc(i.meta.human_review||'pending')+'</small></li>').join('')+
      '</ul></section></div><aside><section class="panel"><h3>About this prototype</h3><p>These four examples were curated from official records with AI assistance. They are saved examples, not live AI responses or a complete Council feed.</p><p>Independent human team sign-off is pending. Source links provide the full context.</p><span class="chip chip--wait">Review pending</span></section><section class="panel"><h3>What we do not infer</h3><ul class="plain-list"><li>A meeting date is not a comment deadline.</li><li>Committee action is not final Council approval.</li><li>A named ward is not a personal impact prediction.</li><li>Possible effects are not measured outcomes.</li></ul></section><section class="panel"><h3>Procedural language</h3><dl class="info-list">'+Object.entries(data.glossary).map(([k,v])=>'<div><dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd></div>').join('')+'</dl></section></aside></div>');
  }
  function analyse() {
    const enabled=connected&&data.runtime&&data.runtime.analysis_enabled;
    mount(header('Analyse an official record', 'Turn supplied City agenda text into an explanation with evidence, then review the result.', 'ANALYST WORKSPACE')+
      (!enabled?'<section class="panel empty-state"><span class="icon-box">'+icon('lock')+'</span><h2>Analyst access is not enabled</h2><p>'+(connected?'An administrator needs to configure an API key and analyst password before this tool can be used.':'This saved demo does not include record analysis. Open the connected Python app to use analyst tools.')+'</p><a class="btn btn-primary" href="decisions.html">Explore the example decisions '+icon('arrow')+'</a></section>':
      '<div class="detail-grid"><section class="panel"><form id="analysis-form" class="form-stack"><div class="field"><label for="analyst-password">Analyst password</label><input id="analyst-password" type="password" name="password" autocomplete="off" required></div><div class="field"><label for="item-url">Official agenda item URL</label><input id="item-url" name="item_url" type="url" placeholder="https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.2" required></div><div class="field"><label for="item-page">Official agenda page text</label><textarea id="item-page" name="item_page" minlength="100" placeholder="Paste the substantive official record, including its decision history." required></textarea></div><div class="field"><label for="report">Staff report PDF (optional)</label><input id="report" name="report" type="file" accept="application/pdf,.pdf"><small class="muted">PDF up to 20 MB. Review uploaded material for personal information first.</small></div><div class="callout"><strong>This uses the configured Claude API.</strong> Submitting sends the supplied text and optional PDF to Anthropic and may incur charges. The output is an unreviewed preview.</div><button id="analysis-submit" class="btn btn-primary" type="submit">Run source-linked analysis '+icon('arrow')+'</button><p id="analysis-message" role="status" hidden></p></form></section><aside><section class="panel"><h3>Before you begin</h3><ul class="plain-list"><li>Use an official Toronto agenda item and report.</li><li>Remove personal or sensitive material.</li><li>Verify every statement and citation before reuse.</li></ul><p class="form-help">Analysis does not save or publish a new decision.</p></section></aside></div>'));
    if(!enabled)return;
    const form=document.getElementById('analysis-form'),button=document.getElementById('analysis-submit'),message=document.getElementById('analysis-message');
    form.addEventListener('submit',async event=>{
      event.preventDefault();
      const upload=document.getElementById('report').files[0];
      if(upload&&upload.size>20000000){message.textContent='Choose a PDF no larger than 20 MB.';message.className='form-error';message.hidden=false;return;}
      const body=new FormData(form);
      if(!upload)body.delete('report');
      button.disabled=true;message.hidden=false;message.className='form-help';message.textContent='Reading the sources and checking the evidence. This may take a moment…';
      try{
        const response=await fetch('api/analyse',{method:'POST',body});
        const result=await response.json();
        if(!response.ok)throw new Error(typeof result.detail==='string'?result.detail:'Check the required fields and try again.');
        document.getElementById('analyst-password').value='';
        detail(result,true);view.focus();
      }catch(e){message.className='form-error';message.textContent=e.message;button.disabled=false;}
      finally{body.delete('password');}
    });
  }
  function render() {
    const names={overview:'Overview',decisions:'Decisions',decision:'Decision details',calculator:'Tax calculator',sources:'Sources & method',analyse:'Analyse a record'};
    document.getElementById('page-label').textContent=names[page]||'Overview';
    document.querySelectorAll('a[data-route]').forEach(a=>{if(a.dataset.route===(page==='decision'?'decisions':page))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    if(page==='decisions')decisions();
    else if(page==='decision'){
      const id=new URLSearchParams(location.search).get('id'),item=data.items.find(i=>i.id===id);
      if(item)detail(item,false);
      else mount(header('Decision not found','This record is not in the current collection.')+'<a class="btn btn-primary" href="decisions.html">Browse decisions →</a>');
    }else if(page==='calculator')calculator();
    else if(page==='sources')sources();
    else if(page==='analyse')analyse();
    else overview();
  }
  function navigation() {
    const sidebar=document.getElementById('sidebar'),menu=document.getElementById('menu-toggle'),scrim=document.getElementById('nav-scrim');
    const appBody=document.querySelector('.app-body'),closeButton=document.getElementById('sidebar-close');
    const mobile=window.matchMedia('(max-width:767px)');
    function close(restoreFocus){
      sidebar.classList.remove('is-open');scrim.hidden=true;menu.setAttribute('aria-expanded','false');appBody.inert=false;
      if(restoreFocus&&mobile.matches)menu.focus();
      sidebar.inert=mobile.matches;
    }
    mobile.addEventListener('change',()=>close(false));close(false);
    menu.addEventListener('click',()=>{
      sidebar.classList.add('is-open');scrim.hidden=false;menu.setAttribute('aria-expanded','true');sidebar.inert=false;
      sidebar.querySelector('a').focus();appBody.inert=mobile.matches;
    });
    scrim.addEventListener('click',()=>close(true));
    closeButton.addEventListener('click',()=>close(true));
    document.addEventListener('keydown',e=>{
      if(!mobile.matches||!sidebar.classList.contains('is-open'))return;
      if(e.key==='Escape'){e.preventDefault();close(true);return;}
      if(e.key==='Tab'){
        const controls=[...sidebar.querySelectorAll('a[href],button:not([disabled])')].filter(el=>el.getClientRects().length);
        const first=controls[0],last=controls[controls.length-1];
        if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
      }
    });
    // The browser handles navigation to separate documents; no router or hash interception.
    wardSelect.addEventListener('change',()=>{try{localStorage.setItem('civicclear-ward',wardSelect.value);}catch(_){} if(page==='overview')overview();else if(page==='decisions'&&updateWardFilter)updateWardFilter();else if(updateWardContext)updateWardContext();});
  }
  async function boot() {
    const saved=window.CIVICCLEAR;
    if(location.protocol!=='file:'){
      const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),8000);
      try{
        const response=await fetch('api/bootstrap',{signal:controller.signal});
        if(!response.ok){if(response.status!==404)loadNotice='The connection is unavailable. You are viewing saved example records.';throw new Error('unavailable');}
        const result=await response.json();
        if(!Array.isArray(result.items)||!result.runtime)throw new Error('Invalid response');
        data=result;connected=true;
      }catch(e){if(!loadNotice&&e.name==='AbortError')loadNotice='The connection timed out. You are viewing saved example records.';data=saved;}
      finally{clearTimeout(timeout);}
    }else data=saved;
    if(!data||!Array.isArray(data.items)){
      view.innerHTML='<section class="empty-state"><h1>We could not load the records</h1><p>Check your connection and try opening the app again.</p><button class="btn btn-primary" id="retry-load">Try again</button></section>';
      document.getElementById('retry-load').addEventListener('click',()=>location.reload());return;
    }
    const connection=document.getElementById('connection-status');
    connection.textContent=connected?'Python connected':'Saved demo';connection.dataset.mode=connected?'connected':'snapshot';
    connection.title=connected?'Records and calculations are served by the Python application.':'This version uses bundled records without a Python connection.';
    document.getElementById('decision-count').textContent=data.items.length;
    data.wards.forEach(w=>{const option=document.createElement('option');option.value=w;option.textContent='Ward '+w;wardSelect.appendChild(option);});
    try{const ward=localStorage.getItem('civicclear-ward');if(data.wards.includes(ward))wardSelect.value=ward;}catch(_){}
    navigation();render();
  }
  boot();
})();
