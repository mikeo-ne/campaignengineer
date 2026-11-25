/* Download page enhancements */
(function () {
  const D = window.CAMPAIGN_DATA;
  const esc = v => CE.esc(v);
  const icon = n => CE.icon(n);

  function bytes(n) {
    n = Number(n) || 0;
    if (!n) return 'Size: unavailable';
    if (n < 1024 * 1024) return `Size: ${Math.max(1, Math.round(n / 1024))} KB`;
    return `Size: ${(n / (1024 * 1024)).toFixed(1)} MB`;
  }

  async function setSize(kind, url) {
    const el = document.querySelector(`[data-size="${kind}"]`);
    if (!el) return;
    try {
      const res = await fetch(url, { method: 'HEAD' });
      const len = res.headers.get('content-length');
      el.textContent = bytes(len);
    } catch (_) {
      el.textContent = 'Size: ready';
    }
  }

  function renderSources() {
    const ids = ['concept_note', 'brief', '7h_site', 'spotify_artist', 'apple_artist', 'apple_chapters', 'spotify_album', 'ughha_ballot', 'ughha_site', 'spotify_pitch', 'youtube_salo'];
    const chosen = ids.map(id => CE.source(id)).filter(Boolean);
    const html = chosen.map((s, i) => `
      <a class="source-card" href="${esc(s.url)}" target="_blank" rel="noopener">
        <span class="source-id">S${String(i + 1).padStart(2, '0')} · ${esc(s.id)}</span>
        <strong>${esc(s.label)} ${icon('external')}</strong>
        <span>${esc(s.used_for)}</span>
        <small>${esc(s.kind)}</small>
      </a>`).join('');
    const main = document.getElementById('source-grid');
    const compact = document.getElementById('download-sources');
    if (main) main.innerHTML = html;
    if (compact) compact.innerHTML = chosen.slice(0, 5).map(s => CE.sourceLink(s.id, s.id)).join('');
  }

  function initDownloadBoth() {
    const btn = document.getElementById('download-both');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const links = [
        'downloads/Baranga_12-Week_Campaign_Strategy.pdf',
        'downloads/Baranga_12-Week_Campaign_Slides.pptx'
      ];
      links.forEach((href, i) => setTimeout(() => {
        const a = document.createElement('a');
        a.href = href; a.download = href.split('/').pop();
        document.body.appendChild(a); a.click(); a.remove();
      }, i * 450));
      const original = btn.innerHTML;
      btn.innerHTML = `${icon('check')} Starting downloads…`;
      setTimeout(() => { btn.innerHTML = original; }, 1800);
    });
  }

  function init() {
    if (!D) return;
    renderSources();
    initDownloadBoth();
    setSize('pdf', D.assets.pdf);
    setSize('pptx', D.assets.pptx);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
