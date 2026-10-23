/*!
 * DOUGA どうが — Japanese theme packs for YouTube
 * v__VERSION__ · https://github.com/__REPO__
 * Shortcuts:  Alt/Option + Shift + T  → next theme
 *             Alt/Option + Shift + X  → skin on / off
 */
(() => {
  'use strict';
  if (window.__dougaLoaded) return;
  window.__dougaLoaded = true;

  const KEY = 'douga-theme';
  const DEFAULT_THEME = '__DEFAULT__';
  const FONTS = '__FONTS__';
  const BASE = __BASE__;
  const THEMES = __THEMES__;
  const ORDER = Object.keys(THEMES);

  // Extension builds sync the choice through browser storage (popup); userscripts use localStorage.
  const ext = (() => {
    try {
      const api = typeof chrome !== 'undefined' ? chrome : typeof browser !== 'undefined' ? browser : null;
      return api && api.storage && api.storage.local ? api : null;
    } catch (_) { return null; }
  })();

  const readLocal = () => { try { return localStorage.getItem(KEY); } catch (_) { return null; } };
  const valid = (id) => id === 'off' || Object.prototype.hasOwnProperty.call(THEMES, id);

  let current = valid(readLocal()) ? readLocal() : DEFAULT_THEME;
  let lastTheme = current === 'off' ? DEFAULT_THEME : current;

  const style = document.createElement('style');
  style.id = 'douga-style';

  const mount = () => {
    const root = document.head || document.documentElement;
    if (root && !style.isConnected) root.appendChild(style);
  };

  const addFonts = () => {
    if (document.getElementById('douga-fonts')) return;
    const link = document.createElement('link');
    link.id = 'douga-fonts';
    link.rel = 'stylesheet';
    link.href = FONTS;
    (document.head || document.documentElement).appendChild(link);
  };

  const apply = (id, { save = true, announce = false } = {}) => {
    if (!valid(id)) id = DEFAULT_THEME;
    current = id;
    if (id !== 'off') lastTheme = id;
    style.textContent = id === 'off' ? '' : BASE + '\n' + THEMES[id].css;
    document.documentElement.dataset.douga = id;
    if (save) {
      try { localStorage.setItem(KEY, id); } catch (_) {}
      if (ext) { try { ext.storage.local.set({ [KEY]: id }); } catch (_) {} }
    }
    if (announce) toast(id === 'off' ? 'DOUGA ・ off' : `Vol.${THEMES[id].vol} ${THEMES[id].jp} ・ ${THEMES[id].name}`);
  };

  // Small on-page toast, built with DOM APIs only (YouTube enforces Trusted Types).
  let toastEl = null;
  let toastTimer = 0;
  const toast = (text) => {
    if (!document.body) return;
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.setAttribute('role', 'status');
      toastEl.style.cssText = [
        'position:fixed', 'left:50%', 'bottom:32px', 'transform:translateX(-50%)', 'z-index:2147483647',
        'padding:10px 18px', 'border-radius:999px', 'font:700 14px/1.2 "DotGothic16","M PLUS Rounded 1c",sans-serif',
        'letter-spacing:.06em', 'background:#0A0A0A', 'color:#FFFFFF', 'border:2px solid #FFFFFF',
        'box-shadow:4px 4px 0 rgba(0,0,0,.35)', 'pointer-events:none', 'transition:opacity .25s', 'opacity:0'
      ].join(';');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = '✦ ' + text;
    toastEl.style.opacity = '1';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastEl.style.opacity = '0'; }, 1600);
  };

  const setPlaceholder = () => {
    if (current === 'off') return;
    document.querySelectorAll('input[name="search_query"]').forEach((input) => {
      if (input.placeholder !== 'なにをみる？') input.placeholder = 'なにをみる？';
    });
  };

  const isTyping = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));

  window.addEventListener('keydown', (e) => {
    if (!e.altKey || !e.shiftKey || e.ctrlKey || e.metaKey || isTyping(e.target)) return;
    if (e.code === 'KeyT') {
      const base = current === 'off' ? lastTheme : current;
      const next = ORDER[(ORDER.indexOf(base) + 1) % ORDER.length];
      apply(next, { announce: true });
      e.preventDefault(); e.stopPropagation();
    } else if (e.code === 'KeyX') {
      apply(current === 'off' ? lastTheme : 'off', { announce: true });
      e.preventDefault(); e.stopPropagation();
    }
  }, true);

  apply(current, { save: false });
  mount();
  addFonts();
  if (!style.isConnected) document.addEventListener('readystatechange', mount);
  document.addEventListener('DOMContentLoaded', () => { mount(); addFonts(); setPlaceholder(); });
  document.addEventListener('yt-navigate-finish', setPlaceholder);
  setTimeout(setPlaceholder, 2000);

  if (ext) {
    try {
      ext.storage.local.get(KEY, (res) => {
        const id = res && res[KEY];
        if (valid(id) && id !== current) apply(id);
      });
      ext.storage.onChanged.addListener((changes, area) => {
        if (area === 'local' && changes[KEY] && valid(changes[KEY].newValue) && changes[KEY].newValue !== current) {
          apply(changes[KEY].newValue, { announce: true });
        }
      });
    } catch (_) {}
  }
})();
