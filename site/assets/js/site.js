/* Shared UI helpers for 7H Campaign Engineer */
(function () {
  const SPRITE = `
<svg class="sprite" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <symbol id="i-external" viewBox="0 0 24 24"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></symbol>
  <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h5"/></symbol>
  <symbol id="i-slides" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/><path d="m7 11 3-3 3 3 4-5"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="m5 13 4 4L19 7"/></symbol>
  <symbol id="i-alert" viewBox="0 0 24 24"><path d="M12 3 2.5 20h19z"/><path d="M12 9v5"/><path d="M12 17.5h.01"/></symbol>
  <symbol id="i-link" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.1 0l2-2a5 5 0 0 0-7.1-7.1l-1.1 1.1"/><path d="M14 11a5 5 0 0 0-7.1 0l-2 2A5 5 0 0 0 12 20.1l1.1-1.1"/></symbol>
  <symbol id="i-music" viewBox="0 0 24 24"><path d="M9 18V5l10-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/></symbol>
  <symbol id="i-award" viewBox="0 0 24 24"><circle cx="12" cy="8" r="5"/><path d="m8.5 12.5-1.5 8 5-3 5 3-1.5-8"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4"/><path d="M16 3v4"/><path d="M3 10h18"/></symbol>
  <symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></symbol>
  <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 2.5-5 6-5s6 2 6 5"/><path d="M16 5.5a3 3 0 0 1 0 5.8"/><path d="M18 15c2 .8 3 2.5 3 5"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></symbol>
  <symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3 3 15 0 18"/><path d="M12 3c-3 3-3 15 0 18"/></symbol>
  <symbol id="i-video" viewBox="0 0 24 24"><rect x="3" y="5" width="14" height="14" rx="2"/><path d="m17 10 4-2v8l-4-2"/></symbol>
  <symbol id="i-spark" viewBox="0 0 24 24"><path d="m12 2 1.7 6.3L20 10l-6.3 1.7L12 18l-1.7-6.3L4 10l6.3-1.7z"/><path d="M19 17l.7 2.3L22 20l-2.3.7L19 23l-.7-2.3L16 20l2.3-.7z"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/></symbol>
  <symbol id="i-note" viewBox="0 0 24 24"><path d="M5 4h14v16H5z"/><path d="M8 8h8"/><path d="M8 12h8"/><path d="M8 16h5"/></symbol>
  <symbol id="i-print" viewBox="0 0 24 24"><path d="M7 8V3h10v5"/><rect x="3" y="8" width="18" height="9" rx="2"/><path d="M7 17H5a2 2 0 0 1-2-2v-1a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v1a2 2 0 0 1-2 2h-2"/><rect x="7" y="14" width="10" height="7"/></symbol>
  <symbol id="i-fullscreen" viewBox="0 0 24 24"><path d="M4 9V4h5"/><path d="M20 9V4h-5"/><path d="M4 15v5h5"/><path d="M20 15v5h-5"/></symbol>
  <symbol id="i-left" viewBox="0 0 24 24"><path d="m15 5-7 7 7 7"/></symbol>
  <symbol id="i-right" viewBox="0 0 24 24"><path d="m9 5 7 7-7 7"/></symbol>
  <symbol id="i-save" viewBox="0 0 24 24"><path d="M5 3h12l2 2v16H5z"/><path d="M8 3v6h8V3"/><path d="M8 14h8v7H8z"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14"/><path d="M5 12h14"/></symbol>
  <symbol id="i-trash" viewBox="0 0 24 24"><path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 14h10l1-14"/><path d="M10 11v6"/><path d="M14 11v6"/></symbol>
  <symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 17V5"/><path d="m7 10 5-5 5 5"/><path d="M5 21h14"/></symbol>
  <symbol id="i-chart" viewBox="0 0 24 24"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/></symbol>
  <symbol id="i-mic" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v3"/><path d="M8 21h8"/></symbol>
  <symbol id="i-headphones" viewBox="0 0 24 24"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="13" width="4" height="7" rx="1"/><rect x="17" y="13" width="4" height="7" rx="1"/></symbol>
</svg>`;

  const CE = {
    data: window.CAMPAIGN_DATA || null,
    icon(name, cls = '') {
      return `<svg class="icon ${cls}" aria-hidden="true"><use href="#i-${name}"></use></svg>`;
    },
    esc(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
    },
    fmt(value) {
      return new Intl.NumberFormat('en-US').format(Number(value) || 0);
    },
    source(id) {
      return (this.data?.sources || []).find(s => s.id === id) || null;
    },
    sourceLink(id, label) {
      const s = this.source(id);
      if (!s) return '';
      const text = label || s.id;
      return `<a href="${this.esc(s.url)}" target="_blank" rel="noopener" title="${this.esc(s.label)}">${this.esc(text)} ${this.icon('external')}</a>`;
    },
    badge(kind, label) {
      const cls = String(kind || '').replace(/\s+/g, '-').replace(/_/g, '-');
      return `<span class="badge ${this.esc(cls)}">${this.esc(label || kind || 'note')}</span>`;
    },
    validUrl(url) {
      try { const u = new URL(url); return ['http:', 'https:'].includes(u.protocol); } catch (_) { return false; }
    },
    downloadBlob(filename, content, type = 'text/plain;charset=utf-8') {
      const blob = new Blob([content], { type });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    },
    init() {
      if (!document.querySelector('.sprite')) document.body.insertAdjacentHTML('afterbegin', SPRITE);
      const toggle = document.querySelector('.menu-toggle');
      const nav = document.querySelector('.nav');
      if (toggle && nav) toggle.addEventListener('click', () => nav.classList.toggle('open'));
      document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => nav && nav.classList.remove('open')));
      const path = location.pathname.split('/').pop() || 'index.html';
      document.querySelectorAll('.nav a').forEach(a => {
        const href = a.getAttribute('href') || '';
        if (href.startsWith(path) && !href.includes('#')) a.classList.add('active');
      });
      const year = document.querySelector('[data-year]');
      if (year) year.textContent = new Date().getFullYear();
    }
  };
  window.CE = CE;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => CE.init());
  else CE.init();
})();
