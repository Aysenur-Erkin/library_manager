(function(){
  const KEY = "ui:theme";
  function applyTheme(theme){
    const root = document.documentElement;
    if(theme === 'auto'){ root.removeAttribute('data-theme'); }
    else if(theme === 'dark'){ root.setAttribute('data-theme','dark'); }
    else { root.setAttribute('data-theme','light'); }
  }
  function currentTheme(){ return localStorage.getItem(KEY) || 'auto'; }
  function cycleTheme(){
    const order = ['auto','light','dark'];
    const next = order[(order.indexOf(currentTheme())+1)%order.length];
    localStorage.setItem(KEY, next); applyTheme(next);
    toast(`Theme: ${next}`, 'info'); updateToggleIcon(next);
  }
  function updateToggleIcon(theme){
    const btn = document.getElementById('themeToggle');
    if(!btn) return;
    const map = { auto:'🌓', light:'☀️', dark:'🌙' };
    btn.textContent = map[theme] || '🌓';
    btn.setAttribute('title', `Theme: ${theme} (click to change)`);
  }
  applyTheme(currentTheme());

  const container = document.createElement('div');
  container.className = 'toast-container';
  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(container);
    if(!document.getElementById('themeToggle')){
      const btn = document.createElement('button');
      btn.id = 'themeToggle';
      btn.className = 'theme-fab';
      btn.type = 'button';
      btn.addEventListener('click', cycleTheme);
      document.body.appendChild(btn);
      updateToggleIcon(currentTheme());
    }
  });

  function toast(message, type='info', opts={}){
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<span class="toast-msg">${message}</span>`;
    const close = document.createElement('button');
    close.className = 'toast-close'; close.type = 'button'; close.setAttribute('aria-label','Close'); close.innerHTML = '×';
    close.onclick = () => { t.classList.add('hide'); setTimeout(()=>t.remove(), 150); };
    t.appendChild(close);
    container.appendChild(t);
    setTimeout(() => { t.classList.add('show'); }, 10);
    const ttl = opts.ttl ?? 2500;
    if(ttl > 0){ setTimeout(() => { t.classList.add('hide'); setTimeout(()=>t.remove(), 150); }, ttl); }
  }
  window.toast = toast;
})();
