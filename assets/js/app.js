/* Campaign site and reusable plan builder */
(function () {
  const D = window.CAMPAIGN_DATA;
  const esc = v => CE.esc(v);
  const icon = n => CE.icon(n);
  const fmt = v => CE.fmt(v);
  const add = (id, html) => { const el = document.getElementById(id); if (el) el.innerHTML = html; };
  const STORE = 'ce_campaigns_v2';

  function sourceRefs(text) {
    const urls = String(text || '').split('\n').map(x => x.trim()).filter(Boolean);
    const valid = urls.filter(u => CE.validUrl(u) || u.startsWith('briefs/') || u.startsWith('./') || u.startsWith('/'));
    return valid.map(u => {
      const label = u.includes('briefs/') ? 'Supplied brief' : (() => { try { return new URL(u, location.href).hostname.replace(/^www\./, ''); } catch (_) { return u; } })();
      return `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(label)} ${icon('external')}</a>`;
    }).join(' ');
  }

  function renderLinks() {
    add('official-links', D.links.map(l => `
      <a class="official-link" href="${esc(l.url)}" target="_blank" rel="noopener" title="${esc(l.note || l.label)}">${icon(l.icon || 'link')} ${esc(l.label)}</a>`).join(''));
  }

  function renderStartingPoint() {
    const album = D.catalog.find(r => r.title === 'CHAPTERS I NEVER WROTE');
    const cards = [
      { value: '7H', label: 'Baranga on the roster', note: 'First-party 7H Music Group site' },
      { value: fmt(D.snapshot.monthly_listeners), label: 'Spotify monthly listeners', note: '24 Nov 2026 starting line' },
      { value: D.awards.categories.length, label: 'UGHHA 2026 ballot listings', note: 'Album Of the Year + Rookie of the year' },
      { value: album.tracks.length, label: 'Tracks on CHAPTERS', note: 'Released 8 May 2026' }
    ];
    add('status-grid', cards.map(c => `
      <div class="stat"><div class="stat-value">${esc(c.value)}</div><strong>${esc(c.label)}</strong><span>${esc(c.note)}</span></div>`).join(''));
  }

  function renderSlideOrder() {
    add('structure-grid', D.slides.map(s => `
      <article class="structure-step">
        <span class="n">${String(s.no).padStart(2, '0')}</span>
        <div>
          <strong>${esc(s.title)}</strong>
          <p>${esc(s.lede || s.notes || '')}</p>
          <small>${esc(s.kicker)}</small>
        </div>
      </article>`).join(''));
  }

  function renderStrategy() {
    const st = D.strategy;
    add('strategy-hero', `
      <div class="strategy-main">
        <div class="section-kicker">The lane</div>
        <h3>${esc(st.positioning)}</h3>
        <p>${esc(st.visual_direction)}</p>
      </div>
      <div class="strategy-side">
        <div><span>Archetype</span><strong>${esc(st.archetype)}</strong></div>
        <div><span>Audience</span><strong>${esc(st.audience)}</strong></div>
        <div><span>Review</span><strong>${esc(D.meta.review_due)}</strong></div>
      </div>`);
    add('objectives-grid', st.objectives.map((o, i) => `
      <article class="objective-card"><span class="objective-no">0${i + 1}</span><h4>${esc(o.area)}</h4><p class="gold">${esc(o.target)}</p><p>${esc(o.channels)}</p><small>${esc(o.clarification)}</small></article>`).join(''));
    add('timeline', st.timeline.map(p => `
      <article class="phase"><div class="phase-head"><span>${esc(p.weeks)}</span><strong>${esc(p.phase)}</strong></div><p>${esc(p.theme)}</p><ul>${p.items.map(w => `<li><b>${esc(w.week)}</b> ${esc(w.title)}</li>`).join('')}</ul></article>`).join(''));
    const b = st.budget;
    add('budget-layout', `
      <article class="card"><h3>${esc(b.total)} allocated</h3><ul>${b.allocation.map(a => `<li>${esc(a.item)} · $${a.amount}</li>`).join('')}</ul></article>
      <article class="card"><h3>${esc(b.projected_gross)} projected gross</h3><ul>${b.revenue_lines.map(r => `<li>${esc(r.item)} · $${r.amount}</li>`).join('')}</ul></article>
      <article class="card"><h3>${esc(b.projected_net)} projected margin</h3><p>${esc(b.note)}</p><p>${esc(b.currency_note)}</p></article>`);
    add('measurement-list', st.measurement.map(m => `<li>${esc(m)}</li>`).join(''));
  }

  function renderSources() {
    add('sources-grid', D.sources.map((s, i) => `
      <a class="source-card" href="${esc(s.url)}" target="_blank" rel="noopener">
        <span class="source-id">R${String(i + 1).padStart(2, '0')} · ${esc(s.id)}</span>
        <strong>${esc(s.label)} ${icon('external')}</strong>
        <span>${esc(s.used_for)}</span>
        <small>${esc(s.kind)}</small>
      </a>`).join(''));
  }

  function barangaPlan() {
    return {
      id: 'baranga-2027', artistName: 'Baranga',
      project: 'CHAPTERS I NEVER WROTE + UGHHA 2026 ballot listings',
      objective: 'I’ll work toward 150,000+ new campaign-attributed streams, 2,500 Inner Circle members, 30+ DJ contacts, 150 merch units and one ticketed showcase.',
      audience: D.strategy.audience,
      territory: 'Kampala / East Africa', startDate: '', reviewDate: D.meta.review_due,
      budget: '$1,500',
      channels: 'Spotify, Apple Music, Boomplay, Audiomack, TikTok, Instagram Reels, YouTube, WhatsApp/Telegram, radio/TV',
      cadence: '2 YouTube posts/week; weekly playlist pitch; Friday analytics; daily community sweep.',
      visual: D.strategy.visual_direction,
      planStage: 'Ready to review',
      proofLinks: [
        'https://7hmusicgroupug.vercel.app/',
        'https://open.spotify.com/artist/5cDK2NGG0OhfT7Z2FpMgxX',
        'https://music.apple.com/us/album/chapters-i-never-wrote/6768973076',
        'https://open.spotify.com/album/1A3yUmi9B5GRwY0PjeQTMp',
        'https://survey.zohopublic.com/zs/oRBBCU',
        'https://support.spotify.com/artists/article/pitching-music-to-playlist-editors',
        'briefs/Baranga_12-Week_Marketing_Strategy.pdf',
        'briefs/Baranga_Concept_Note.jpg',
        'RESEARCH.md#assignment-slide-order'
      ].join('\n'),
      notes: 'I’ll set the launch date, campaign owner, currency, audio clearances, venue terms and Week 0 baselines with the team before launch.'
    };
  }

  function blankPlan() {
    return {
      id: '', artistName: '', project: '', objective: '', audience: '', territory: '',
      startDate: '', reviewDate: '', budget: '', channels: '', cadence: '', visual: '',
      planStage: 'Draft in progress', proofLinks: '', notes: ''
    };
  }

  function readForm() { return Object.fromEntries(new FormData(document.getElementById('campaign-form')).entries()); }
  function writeForm(state) {
    const form = document.getElementById('campaign-form');
    Object.entries(state || {}).forEach(([k, v]) => {
      const el = form.elements.namedItem(k);
      if (el) el.value = v ?? '';
    });
  }
  function toast(message) {
    const el = document.getElementById('builder-toast');
    if (!el) return;
    el.textContent = message; el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 2200);
  }
  function saved() { try { return JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (_) { return {}; } }
  function renderSaved(selected) {
    const select = document.getElementById('saved-campaigns');
    if (!select) return;
    const all = saved();
    const keys = Object.keys(all);
    select.innerHTML = keys.length ? keys.map(k => `<option value="${esc(k)}" ${k === selected ? 'selected' : ''}>${esc(all[k].artistName || k)}</option>`).join('') : '<option value="">No saved drafts yet</option>';
  }
  function renderPreview(state) {
    const links = sourceRefs(state.proofLinks);
    add('plan-preview-content', `
      <div class="preview-title"><span class="badge">${esc(state.planStage || 'Draft')}</span><h3>${esc(state.artistName || 'Untitled campaign')}</h3></div>
      <p class="muted">${esc(state.project || 'Add a project or release')}</p>
      <dl>
        <dt>Objective</dt><dd>${esc(state.objective || '—')}</dd>
        <dt>Audience</dt><dd>${esc(state.audience || '—')}</dd>
        <dt>Territory</dt><dd>${esc(state.territory || '—')}</dd>
        <dt>Budget</dt><dd>${esc(state.budget || '—')}</dd>
        <dt>Cadence</dt><dd>${esc(state.cadence || '—')}</dd>
        <dt>Visual</dt><dd>${esc(state.visual || '—')}</dd>
        <dt>Review</dt><dd>${esc(state.reviewDate || '—')}</dd>
        <dt>Notes</dt><dd>${esc(state.notes || '—')}</dd>
      </dl>
      <div class="source-line">${links || '<span class="muted">Add source links</span>'}</div>`);
  }

  function initBuilder() {
    const form = document.getElementById('campaign-form');
    if (!form) return;
    writeForm(barangaPlan());
    renderPreview(readForm());
    renderSaved();
    form.addEventListener('input', () => renderPreview(readForm()));
    form.addEventListener('change', () => renderPreview(readForm()));
    document.getElementById('use-baranga').addEventListener('click', () => { writeForm(barangaPlan()); renderPreview(readForm()); toast('Baranga plan loaded'); });
    document.getElementById('blank-campaign').addEventListener('click', () => { writeForm(blankPlan()); renderPreview(readForm()); toast('Blank plan ready'); });
    document.getElementById('save-campaign').addEventListener('click', () => {
      const state = readForm();
      const key = state.artistName ? `${state.artistName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${Date.now().toString(36).slice(-4)}` : `draft-${Date.now()}`;
      const all = saved(); all[key] = { ...state, id: key }; localStorage.setItem(STORE, JSON.stringify(all));
      renderSaved(key); toast('Draft saved in this browser');
    });
    document.getElementById('saved-campaigns').addEventListener('change', e => {
      const all = saved(); const state = all[e.target.value];
      if (state) { writeForm(state); renderPreview(state); }
    });
    document.getElementById('delete-campaign').addEventListener('click', () => {
      const key = document.getElementById('saved-campaigns').value;
      if (!key) return;
      const all = saved(); delete all[key]; localStorage.setItem(STORE, JSON.stringify(all));
      renderSaved(); toast('Draft deleted');
    });
    document.getElementById('export-json').addEventListener('click', () => {
      CE.downloadBlob('campaign-plan.json', JSON.stringify(readForm(), null, 2), 'application/json'); toast('JSON exported');
    });
    document.getElementById('export-md').addEventListener('click', () => {
      const s = readForm();
      const md = `# ${s.artistName || 'Campaign plan'}\n\nProject: ${s.project || '—'}\n\nObjective: ${s.objective || '—'}\n\nAudience: ${s.audience || '—'}\n\nTerritory: ${s.territory || '—'}\n\nBudget: ${s.budget || '—'}\n\nReview: ${s.reviewDate || '—'}\n\nNotes: ${s.notes || '—'}\n\nSources:\n${s.proofLinks || '—'}\n`;
      CE.downloadBlob('campaign-notes.md', md, 'text/markdown'); toast('Notes exported');
    });
    const file = document.getElementById('import-file');
    document.getElementById('import-plan').addEventListener('click', () => file.click());
    file.addEventListener('change', () => {
      const f = file.files[0]; if (!f) return;
      const reader = new FileReader();
      reader.onload = () => { try { const state = JSON.parse(reader.result); writeForm(state); renderPreview(state); toast('Plan imported'); } catch (_) { toast('That file is not a plan JSON'); } };
      reader.readAsText(f); file.value = '';
    });
  }

  function init() {
    if (!D) return;
    renderLinks();
    renderStartingPoint();
    renderSlideOrder();
    renderStrategy();
    renderSources();
    initBuilder();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
