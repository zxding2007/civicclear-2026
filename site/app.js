// CivicClear page script: the decision explorer and the tax calculator.
// Reads window.CIVICCLEAR (data.js, written by build_site.py). Never calls a model or a server.
// All record text goes into the page with textContent, never as HTML.
(function () {
  'use strict';
  var D = window.CIVICCLEAR;
  if (!D) return;

  // ---------- small helpers ----------
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function add(parent) { for (var i = 1; i < arguments.length; i++) if (arguments[i]) parent.appendChild(arguments[i]); return parent; }
  function safeUrl(u) {
    try { var x = new URL(u); return (x.protocol === 'https:' && /(^|\.)toronto\.ca$/.test(x.hostname)) ? x.href : null; }
    catch (e) { return null; }
  }
  function link(href, text, cls) {
    var u = safeUrl(href);
    if (!u) return el('span', cls, text);
    var a = el('a', cls, text); a.href = u; a.rel = 'noopener'; a.target = '_blank';
    return a;
  }
  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  function niceDate(s) {
    // "2026-04-14" -> "April 14, 2026"; "2026-05-20/21" -> "May 20 and 21, 2026"
    var m = /^(\d{4})-(\d{2})-(\d{2})(?:\/(\d{2}))?$/.exec(s || '');
    if (!m) return s || '';
    var day = String(+m[3]) + (m[4] ? ' and ' + (+m[4]) : '');
    return MONTHS[+m[2] - 1] + ' ' + day + ', ' + m[1];
  }
  function today() {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  // ---------- what each status means, in plain words ----------
  var STATUS = {
    received:            { big: 'Not approved', chip: 'Noted only', tone: 'no',
                           line: 'City Council only took note of this item. Taking note is not a vote to approve it.' },
    committee_only:      { big: 'Not final yet', chip: 'Committee only', tone: 'wait',
                           line: 'A committee voted on it. City Council has not made a final decision in this record.' },
    recommendation_only: { big: 'Only a recommendation', chip: 'Advice only', tone: 'wait',
                           line: 'City staff recommended it. No committee or Council vote is in this record.' },
    final_adopted:       { big: 'Approved by City Council', chip: 'Approved', tone: 'yes',
                           line: 'City Council adopted it. This is the final decision in this record.' },
    final_amended:       { big: 'Approved, with changes', chip: 'Approved, amended', tone: 'yes',
                           line: 'City Council adopted it after changing it. The changes are in the City’s record.' },
    unclear:             { big: 'Status unclear', chip: 'Unclear', tone: 'no',
                           line: 'The record could not be checked well enough to say where this stands.' }
  };
  var OUTCOME = {
    recommended: 'Recommended', adopted: 'Adopted', adopted_with_amendments: 'Adopted with amendments',
    adopted_without_amendments: 'Adopted without amendments', received_for_information: 'Received for information',
    referred: 'Referred', deferred: 'Deferred', other: 'Other'
  };
  var STEPS = [
    { type: 'staff_recommendation', name: 'Staff' },
    { type: 'committee_decision', name: 'Committee' },
    { type: 'council_decision', name: 'City Council' }
  ];

  // ---------- wards ----------
  var wardSel = document.getElementById('ward');
  (D.wards || []).forEach(function (w) {
    var o = el('option', null, 'Ward ' + w); o.value = w; wardSel.appendChild(o);
  });
  function wardMatch(item, ward) {
    var ws = item.card.wards || [];
    if (ws.indexOf('All') !== -1) return { kind: 'all', text: 'Applies to all 25 wards' };
    if (!ward) return null;
    if (ws.indexOf(ward) !== -1) return { kind: 'here', text: 'Names your ward' };
    return { kind: 'not', text: 'Not in your ward' };
  }
  function wardsText(item) {
    var ws = item.card.wards || [];
    if (ws.indexOf('All') !== -1) return 'All wards, city-wide';
    return (ws.length > 1 ? 'Wards ' : 'Ward ') + ws.join(', ');
  }

  // ---------- the list ----------
  var listEl = document.getElementById('list');
  var openEl = document.getElementById('open');
  var current = 0, tab = 0;

  function chip(text, tone) { return el('span', 'chip chip--' + tone, text); }

  function renderList() {
    var ward = wardSel.value;
    listEl.textContent = '';
    D.items.forEach(function (item, i) {
      var st = STATUS[item.status] || STATUS.unclear;
      var li = el('li');
      var b = el('button', 'ex__item');
      b.type = 'button';
      b.setAttribute('aria-current', i === current ? 'true' : 'false');
      b.setAttribute('aria-controls', 'open');
      var chips = el('span', 'ex__chips');
      add(chips, chip(st.chip, st.tone));
      var m = wardMatch(item, ward);
      if (m) add(chips, chip(m.text, m.kind === 'not' ? 'no' : 'here'));
      add(b, el('b', null, item.short_title), el('small', null, wardsText(item)), chips);
      b.addEventListener('click', function () { show(i, true); });
      li.appendChild(b);
      listEl.appendChild(li);
    });
  }

  // ---------- the open decision ----------
  function sourceLine(src) {
    if (!src) return null;
    var p = el('span', 'src');
    add(p, el('span', null, 'Source:'), link(src.source_url || src.url, src.source_name || src.document || 'City of Toronto'));
    return p;
  }

  function show(i, focus) {
    current = i;
    var item = D.items[i], card = item.card, meta = item.meta || {}, ev = item.evidence || null;
    var st = STATUS[item.status] || STATUS.unclear;
    var claims = (ev && ev.claims) || {};
    var root = el('div', 'op');
    var P = [0, 1, 2, 3, 4].map(function () { return el('div', 'op__panel'); });

    // title
    add(root, add(el('div', 'op__top'),
      el('span', 'op__id', 'Item ' + card.item_id),
      el('p', 'op__title', card.title),
      el('p', 'op__wards', wardsText(item))));

    // verdict
    var stageQuote = (card.stages[card.stages.length - 1] || {}).quote;
    add(P[0], add(el('div', 'verdict verdict--' + st.tone),
      el('span', 'verdict__label', 'Where it stands'),
      el('p', 'verdict__big', st.big),
      el('p', null, st.line)));

    // journey
    var j = el('div');
    add(j, el('p', 'op__label', 'The steps in this record'));
    var ol = el('ol', 'journey');
    var lastType = (card.stages[card.stages.length - 1] || {}).stage_type;
    STEPS.forEach(function (step) {
      var found = card.stages.filter(function (s) { return s.stage_type === step.type; });
      var li = el('li', found.length ? 'is-done' + (step.type === lastType ? ' is-last' : '') : '');
      add(li, el('b', null, step.name));
      if (found.length) {
        var s = found[found.length - 1];
        var k = card.stages.indexOf(s);
        add(li, el('span', null, (OUTCOME[s.outcome] || s.outcome) + ', ' + niceDate(s.date)), el('small', null, s.body));
        add(li, item.checks.stages[k] ? el('span', 'ok', 'Quote found') : el('span', 'bad', 'Quote not found'));
      } else {
        add(li, el('small', null, 'Not part of this record'));
      }
      ol.appendChild(li);
    });
    add(j, ol);
    if (stageQuote) add(j, add(el('p', 'src'), el('span', null, '“' + stageQuote + '”')));
    add(P[0], j);

    // near me
    var ward = wardSel.value;
    var m = wardMatch(item, ward);
    var near = el('div');
    add(near, el('p', 'op__label', 'Is it near me?'));
    var nearRow = el('div', 'near');
    if (m && m.kind === 'all') add(nearRow, chip('Yes', 'here'), el('p', null, 'It applies to every ward in Toronto.'));
    else if (m && m.kind === 'here') add(nearRow, chip('Yes', 'here'), el('p', null, 'The record names Ward ' + ward + '.'));
    else if (m && m.kind === 'not') add(nearRow, chip('No', 'no'), el('p', null, 'The record names ' + wardsText(item) + ', not Ward ' + ward + '.'));
    else add(nearRow, el('p', null, 'Choose your ward on the left to check. This record names ' + wardsText(item) + '.'));
    add(near, nearRow);
    add(P[1], near);

    // have your say
    var p = card.participation || {};
    var end = meta.participation_end_date;
    var say = el('div', 'say');
    var canSay = p.can_still_comment === 'yes' && end && end >= today();
    if (canSay) {
      say.className = 'say say--open';
      add(say, el('b', null, 'Yes, you can still comment until ' + niceDate(end) + '.'),
        el('p', null, p.how || ''),
        p.quote ? el('p', 'src', '“' + p.quote + '”') : null,
        link(meta.participation_source_url, 'Give feedback on the City page', 'btn btn--primary'));
    } else if (p.can_still_comment === 'yes' && end) {
      add(say, el('b', null, 'This comment period closed on ' + niceDate(end) + '.'),
        el('p', null, 'Check the City page for any new dates.'),
        link(meta.consultation_project_url || meta.item_url, 'Open the City page', 'btn btn--secondary'));
    } else {
      add(say, el('b', null, 'This record names no comment deadline.'),
        el('p', null, 'CivicClear never guesses a date. To speak or write to a committee about a future item, the City explains how here.'),
        link(D.have_your_say_url, 'See how to have your say', 'btn btn--secondary'));
    }
    add(P[1], add(el('div'), el('p', 'op__label', 'Can I still have a say?'), say));

    // what it is
    var dl = el('dl', 'facts3');
    [['What is proposed', card.what_is_proposed, 'what_is_proposed'],
     ['Why', card.why, 'why'],
     ['Who it touches', card.who_is_affected, 'who_is_affected']].forEach(function (r) {
      var dd = el('dd', null, r[1]);
      var s = sourceLine(claims[r[2]]);
      if (s) { dd.appendChild(el('br')); dd.appendChild(s); }
      add(dl, add(el('div'), el('dt', null, r[0]), dd));
    });
    add(P[2], add(el('div'), el('p', 'op__label', 'What it is about'), dl));

    // impacts (only where the evidence file has them)
    if (ev && ev.impacts && ev.impacts.length) {
      var im = el('div', 'impacts');
      ev.impacts.forEach(function (x) {
        add(im, add(el('div'), el('b', null, x.audience), el('span', null, x.potential_effect)));
      });
      add(P[2], add(el('div'), el('p', 'op__label', 'Who it might affect'), im));
    }

    // explanation with sources
    if (item.explanation && item.explanation.length) {
      var ul = el('ul', 'segs');
      item.explanation.forEach(function (seg) {
        var li = add(el('li'), el('p', null, seg.text));
        (seg.sources || []).forEach(function (s) {
          if (s.cited_text) add(li, el('blockquote', null, '“' + s.cited_text + '”'));
          add(li, add(el('span', 'src'), s.verified ? el('span', 'ok', 'Quote found') : el('span', 'bad', 'Quote not found'),
            link(s.url, s.document || 'City of Toronto')));
        });
        ul.appendChild(li);
      });
      add(P[4], add(el('div'), el('p', 'op__label', 'In the City’s words'), ul));
    }

    // words to know
    var words = el('dl', 'words');
    var seen = {};
    (card.procedural_phrases || []).forEach(function (ph) {
      var key = (ph.phrase || '').toLowerCase();
      seen[key] = true;
      add(words, add(el('div'), el('dt', null, '“' + ph.phrase + '”'), el('dd', null, ph.meaning_here)));
    });
    ['committee decision', 'staff recommendation'].forEach(function (k) {
      if (!seen[k] && D.glossary && D.glossary[k] && card.stages.some(function (s) { return s.stage_type.indexOf(k.split(' ')[0]) === 0; })) {
        add(words, add(el('div'), el('dt', null, k.charAt(0).toUpperCase() + k.slice(1)), el('dd', null, D.glossary[k])));
      }
    });
    if (words.children.length) add(P[2], add(el('div'), el('p', 'op__label', 'Words to know'), words));

    // not known yet
    var unk = (card.uncertainties || []).concat(card.conditions || []);
    if (unk.length) {
      var u = el('ul', 'unknowns');
      unk.forEach(function (t) { add(u, el('li', null, t)); });
      add(P[3], add(el('div'), el('p', 'op__label', 'What is not known yet'), u));
    }

    // links
    add(P[4], add(el('div', 'op__links'),
      link(meta.item_url, 'Open the City’s agenda item', 'btn btn--secondary'),
      meta.report_url ? link(meta.report_url, 'Read the staff report (PDF)', 'btn btn--secondary') : null));

    // the four parts as tabs: one shows at a time, so the window never needs to scroll
    var NAMES = ['Decision', 'Your say', 'Details', 'Unknowns', 'Sources'];
    var bar = el('div', 'op__tabs');
    bar.setAttribute('role', 'tablist');
    bar.setAttribute('aria-label', 'Parts of this decision');
    var btns = NAMES.map(function (name, t) {
      var b = el('button', 'op__tab', name);
      b.type = 'button';
      b.id = 'op-tab-' + t;
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-controls', 'op-panel-' + t);
      P[t].id = 'op-panel-' + t;
      P[t].setAttribute('role', 'tabpanel');
      P[t].setAttribute('aria-labelledby', b.id);
      b.addEventListener('click', function () { pick(t, false); });
      b.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (k) { e.preventDefault(); pick((t + k + NAMES.length) % NAMES.length, true); }
      });
      return b;
    });
    function pick(t, move) {
      tab = t;
      btns.forEach(function (b, n) {
        b.setAttribute('aria-selected', n === t ? 'true' : 'false');
        b.tabIndex = n === t ? 0 : -1;
        P[n].hidden = n !== t;
      });
      if (move) btns[t].focus();
    }
    if (canSay) {
      var hint = el('button', 'say-hint', 'You can still comment until ' + niceDate(end) + '. See how \u2192');
      hint.type = 'button';
      hint.addEventListener('click', function () { pick(1, true); });
      P[0].insertBefore(hint, P[0].children[1] || null);
    }
    btns.forEach(function (b) { bar.appendChild(b); });
    add(root, bar);
    P.forEach(function (x) { add(root, x); });
    // the pane's foot: where every line comes from, on every tab
    add(root, add(el('div', 'op__foot'),
      el('p', null, 'Checked against the City\u2019s record on ' + niceDate(meta.source_checked_on) + '. Team review: ' + (meta.human_review || 'pending') + '.'),
      link(meta.item_url, 'Open the City\u2019s agenda item', 'link')));
    pick(0, false);

    openEl.textContent = '';
    openEl.appendChild(root);
    openEl.scrollTop = 0;
    renderList();
    if (focus && window.matchMedia('(max-width: 1023px)').matches) openEl.focus({ preventScroll: false });
  }

  wardSel.addEventListener('change', function () { show(current, false); });
  try { var saved = localStorage.getItem('civicclear-ward'); if (saved) wardSel.value = saved; } catch (e) {}
  wardSel.addEventListener('change', function () { try { localStorage.setItem('civicclear-ward', wardSel.value); } catch (e) {} });
  show(0, false);

  // ---------- tax calculator: integer cents, rounded half up, like calculator.py ----------
  var tax = D.tax && D.tax.residential;
  if (!tax) return;
  var r25 = Math.round(tax['2025'].rate_percent * 1e6);   // 0.601087 -> 601087
  var r26 = Math.round(tax['2026'].rate_percent * 1e6);
  function cents(value, rateMicro) { return Math.floor((value * rateMicro + 500000) / 1e6); }
  function money(c) {
    var s = (Math.abs(c) / 100).toLocaleString('en-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return '$' + s;
  }
  // self-check against the worked example from calculator.py
  var ex = D.tax.example;
  if (ex && (cents(ex.assessed_value, r25) !== Math.round(ex.before * 100) || cents(ex.assessed_value, r26) !== Math.round(ex.after * 100))) {
    console.error('CivicClear: tax maths differs from calculator.py');
  }
  document.getElementById('rate-2025').textContent = tax['2025'].rate_percent + '%';
  document.getElementById('rate-2026').textContent = tax['2026'].rate_percent + '%';
  var pct = ((r26 - r25) / r25 * 100).toFixed(1);
  document.getElementById('rate-change').textContent = 'The residential rate went ' + (r26 >= r25 ? 'up ' : 'down ') + Math.abs(pct) + '% from 2025 to 2026. The same assessed value is used for both years.';

  var input = document.getElementById('value');
  var err = document.getElementById('value-err');
  function calc() {
    var raw = input.value.replace(/[\s,$]/g, '');
    var ok = /^\d{1,10}$/.test(raw);
    err.hidden = ok || raw === '';
    input.setAttribute('aria-invalid', ok || raw === '' ? 'false' : 'true');
    if (!ok) return;
    var v = parseInt(raw, 10);
    var b = cents(v, r25), a = cents(v, r26), d = a - b;
    document.getElementById('before').textContent = money(b);
    document.getElementById('after').textContent = money(a);
    document.getElementById('diff').textContent = (d >= 0 ? '+' : '−') + money(d) + ' a year';
    var top = Math.max(a, b) || 1;
    document.getElementById('bar-2025').style.setProperty('--w', (100 * b / top).toFixed(1) + '%');
    document.getElementById('bar-2026').style.setProperty('--w', (100 * a / top).toFixed(1) + '%');
    document.getElementById('month').textContent = 'About ' + money(Math.round(Math.abs(d) / 12)) + (d >= 0 ? ' more' : ' less') + ' a month.';
  }
  input.addEventListener('input', calc);
  input.addEventListener('blur', function () {
    var raw = input.value.replace(/[\s,$]/g, '');
    if (/^\d{1,10}$/.test(raw)) input.value = parseInt(raw, 10).toLocaleString('en-CA');
  });
  document.getElementById('calc').addEventListener('submit', function (e) { e.preventDefault(); calc(); });
  calc();
})();
