/* global DOUGA_THEMES */
const KEY = 'douga-theme';
const api = typeof chrome !== 'undefined' ? chrome : browser;
const list = document.getElementById('list');
const offBtn = document.getElementById('off');

function render(active) {
  list.textContent = '';
  DOUGA_THEMES.forEach((t) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'theme' + (t.id === active ? ' active' : '');
    btn.setAttribute('aria-pressed', String(t.id === active));

    const sw = document.createElement('span');
    sw.className = 'swatches';
    t.swatches.forEach((c) => {
      const dot = document.createElement('i');
      dot.style.background = c;
      sw.appendChild(dot);
    });

    const text = document.createElement('span');
    text.className = 'text';
    const title = document.createElement('strong');
    title.textContent = `Vol.${t.vol}  ${t.jp} ${t.name}`;
    const tag = document.createElement('small');
    tag.textContent = t.tagline;
    text.append(title, tag);

    btn.append(sw, text);
    btn.addEventListener('click', () => select(t.id));
    list.appendChild(btn);
  });
  offBtn.textContent = active === 'off' ? 'Turn skin on' : 'Turn skin off';
  offBtn.dataset.state = active === 'off' ? 'off' : 'on';
}

let current = DOUGA_THEMES[0].id;
let last = current;

function select(id) {
  current = id;
  if (id !== 'off') last = id;
  api.storage.local.set({ [KEY]: id });
  render(id);
}

offBtn.addEventListener('click', () => select(current === 'off' ? last : 'off'));

api.storage.local.get(KEY, (res) => {
  const id = res && res[KEY];
  if (id) { current = id; if (id !== 'off') last = id; }
  render(current);
});
