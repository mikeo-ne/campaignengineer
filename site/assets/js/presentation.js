/* Online presentation deck */
(function () {
  const D = window.CAMPAIGN_DATA;
  const esc = v => CE.esc(v);
  const icon = n => CE.icon(n);
  const source = id => CE.sourceLink(id, id);
  const asset = key => D.assets[key] || '';

  const bulletList = list => `<ul>${(list || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
  const bodyHtml = value => Array.isArray(value) ? bulletList(value) : `<p>${esc(value || '')}</p>`;

  function cardHtml(card) {
    return `<div class="deck-card"><h3>${esc(card.title)}</h3>${bodyHtml(card.body)}</div>`;
  }

  function gridHtml(items, cols) {
    return `<div class="deck-grid cols-${cols}">${items.join('')}</div>`;
  }

  function referenceHtml(ids) {
    const links = (ids || []).map(source).join(' ');
    return `
      <div class="deck-grid cols-2">
        <div class="deck-card"><h3>References</h3><p class="source-line">${links}</p></div>
        <div class="deck-card"><img src="${esc(asset('party_cover'))}" alt="Party Riddim artwork" style="height:150px"><h3>Keep the files</h3><p><a href="${esc(asset('pdf'))}" download style="color:var(--gold)">Strategy PDF ${icon('download')}</a> · <a href="${esc(asset('pptx'))}" download style="color:var(--gold)">Editable slides ${icon('download')}</a></p></div>
      </div>`;
  }

  function photoSlide(s) {
    const extra = s.bullets ? `<div class="deck-card" style="margin-top:12px">${bulletList(s.bullets)}</div>` : '';
    return `
      <div class="deck-photo"><img src="${esc(asset(s.image))}" alt="${esc(s.headline)}"></div>
      <div class="deck-copy">
        <div class="deck-kicker">${esc(s.kicker)}</div>
        <h1>${esc(s.headline)}</h1>
        ${s.subhead ? `<h2 style="font-size:clamp(26px,3.4vw,46px);color:var(--gold);margin-top:8px">${esc(s.subhead)}</h2>` : ''}
        ${s.lede ? `<p class="deck-lede">${esc(s.lede)}</p>` : ''}
        ${extra}
      </div>`;
  }

  function htmlFor(s) {
    switch (s.layout) {
      case 'cover':
      case 'transition':
      case 'artist':
      case 'equation':
        return photoSlide(s);
      case 'bullets':
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h2>${esc(s.headline)}</h2>
          ${s.lede ? `<p class="deck-lede">${esc(s.lede)}</p>` : ''}
          <div class="deck-card" style="margin-top:14px">${bulletList(s.bullets)}</div>`;
      case 'cards': {
        const cols = s.cards.length === 3 ? 3 : 2;
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h2>${esc(s.headline)}</h2>
          ${s.lede ? `<p class="deck-lede">${esc(s.lede)}</p>` : ''}
          ${gridHtml(s.cards.map(cardHtml), cols)}`;
      }
      case 'quote':
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h2>${esc(s.headline)}</h2>
          <div class="deck-grid cols-2">
            <div class="deck-card"><h3>The promise</h3><p class="deck-lede" style="font-size:18px;color:var(--gold)">“${esc(s.quote)}”</p></div>
            <div class="deck-card"><h3>How I’ll make it real</h3><p>${esc(s.lede)}</p></div>
          </div>`;
      case 'collage': {
        const cards = s.images.map(x => `<div class="deck-card"><img src="${esc(asset(x.asset))}" alt="${esc(x.title)}" style="height:130px"><h3>${esc(x.title)}</h3><p>${esc(x.body)}</p></div>`);
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h2>${esc(s.headline)}</h2>
          ${s.lede ? `<p class="deck-lede">${esc(s.lede)}</p>` : ''}
          ${gridHtml(cards, 4)}`;
      }
      case 'timeline': {
        const cards = s.cards.map(x => `<div class="deck-card"><h3>${esc(x.title)}</h3><p>${esc(x.body)}</p></div>`);
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h2>${esc(s.headline)}</h2>
          ${s.lede ? `<p class="deck-lede">${esc(s.lede)}</p>` : ''}
          ${gridHtml(cards, 3)}`;
      }
      case 'thanks':
        return `
          <div class="deck-kicker">${esc(s.kicker)}</div>
          <h1>${esc(s.headline)}</h1>
          <p class="deck-lede">${esc(s.lede)}</p>
          ${referenceHtml(s.sources)}`;
      default:
        return `<div class="deck-kicker">${esc(s.kicker)}</div><h2>${esc(s.headline)}</h2>`;
    }
  }

  function buildSlides() {
    return D.slides.map(s => ({
      title: s.title,
      hero: ['cover', 'transition', 'artist', 'equation'].includes(s.layout),
      foot: s.foot || '',
      notes: s.notes || '',
      html: htmlFor(s)
    }));
  }

  function init() {
    if (!D) return;
    const slides = buildSlides();
    const deck = document.getElementById('deck');
    deck.innerHTML = slides.map((s, i) => `
      <section class="deck-slide ${s.hero ? 'hero-slide' : ''}" data-index="${i}" data-title="${esc(s.title)}">
        ${s.html}
        <div class="deck-foot"><span>7H · BARANGA · 2027</span><span>${s.foot || ''}</span><span>${String(i + 1).padStart(2, '0')} / ${slides.length}</span></div>
      </section>`).join('');

    const elements = [...deck.querySelectorAll('.deck-slide')];
    const counter = document.getElementById('deck-counter');
    const progress = document.getElementById('deck-progress');
    const notesPanel = document.getElementById('deck-notes');
    const notesBody = document.getElementById('deck-notes-body');
    let index = 0;

    function show(n) {
      index = Math.max(0, Math.min(slides.length - 1, n));
      elements.forEach((el, i) => el.classList.toggle('active', i === index));
      counter.textContent = `${index + 1} / ${slides.length}`;
      progress.style.width = `${((index + 1) / slides.length) * 100}%`;
      notesBody.textContent = slides[index].notes || '';
      history.replaceState(null, '', `#slide-${index + 1}`);
    }
    function fromHash() {
      const m = /slide-(\d+)/.exec(location.hash);
      show(m ? Number(m[1]) - 1 : 0);
    }
    document.getElementById('deck-prev').addEventListener('click', () => show(index - 1));
    document.getElementById('deck-next').addEventListener('click', () => show(index + 1));
    document.getElementById('deck-notes').addEventListener('click', () => notesPanel.classList.toggle('show'));
    document.getElementById('deck-print').addEventListener('click', () => window.print());
    document.getElementById('deck-full').addEventListener('click', () => {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
      else document.exitFullscreen && document.exitFullscreen();
    });
    document.addEventListener('keydown', e => {
      if (e.target.matches('input,textarea')) return;
      switch (e.key) {
        case 'ArrowRight': case 'PageDown': case ' ': e.preventDefault(); show(index + 1); break;
        case 'ArrowLeft': case 'PageUp': e.preventDefault(); show(index - 1); break;
        case 'Home': show(0); break;
        case 'End': show(slides.length - 1); break;
        case 'n': case 'N': notesPanel.classList.toggle('show'); break;
        case 'f': case 'F': document.getElementById('deck-full').click(); break;
        case 'p': case 'P': window.print(); break;
      }
    });
    window.addEventListener('hashchange', fromHash);
    fromHash();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
