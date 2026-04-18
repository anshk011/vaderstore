/**
 * Valorant Store Checker — Frontend
 * Works standalone and as Telegram Mini App
 */

const API = '';  // same origin (Flask serves both)
const STORE_KEY = 'vsc_session';
const RIOT_LOGIN_URL = 'https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1&scope=account%20openid';

// Telegram WebApp integration
const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
  tg.setHeaderColor?.('#080808');
  tg.setBackgroundColor?.('#080808');
}

// Session state
let S = { access_token:'', entitlement_token:'', puuid:'', region:'ap', username:'', tag:'', client_version:'' };
let _loginWindow = null;
let _pollTimer   = null;
let _storeTimer  = null;

// ── Boot ──────────────────────────────────────────────────────────────────────
(function boot() {
  const saved = lsGet(STORE_KEY);
  if (saved && saved.access_token) {
    Object.assign(S, saved);
    showApp();
    loadAll();
  } else {
    showLogin();
  }
})();

// ── Login via window.open ─────────────────────────────────────────────────────
function openRiotLogin() {
  setLoginStatus('Opening Riot login...', true);
  
  _loginWindow = window.open(RIOT_LOGIN_URL, 'riot_login', 'width=480,height=640,menubar=no,toolbar=no,location=yes');
  
  if (!_loginWindow || _loginWindow.closed) {
    setLoginStatus('Popup blocked. Paste the URL manually below.', false);
    return;
  }

  // Poll the popup URL
  clearInterval(_pollTimer);
  _pollTimer = setInterval(() => {
    try {
      if (!_loginWindow || _loginWindow.closed) {
        clearInterval(_pollTimer);
        setLoginStatus('Window closed. Paste the URL if you completed login.', false);
        return;
      }
      const loc = _loginWindow.location?.href || '';
      if (loc.includes('playvalorant.com') && loc.includes('access_token=')) {
        clearInterval(_pollTimer);
        _loginWindow.close();
        setLoginStatus('Login detected! Processing...', true);
        handleLoginSuccess(loc);
      }
    } catch (e) {
      // Cross-origin — expected while on auth.riotgames.com
    }
  }, 500);
}

function setLoginStatus(msg, show) {
  const status = el('login-status');
  const text   = el('login-status-text');
  if (show) {
    status.style.display = 'flex';
    text.textContent = msg;
  } else {
    status.style.display = 'none';
  }
}

// ── Manual URL submit ─────────────────────────────────────────────────────────
async function submitManualUrl() {
  const raw = el('manual-url').value.trim();
  if (!raw) return;
  
  clearInterval(_pollTimer);
  if (_loginWindow && !_loginWindow.closed) _loginWindow.close();
  
  setLoginStatus('Processing...', true);
  await handleLoginSuccess(raw);
}

async function handleLoginSuccess(redirectUrl) {
  const at = extractParam(redirectUrl, 'access_token');
  const it = extractParam(redirectUrl, 'id_token');

  if (!at) {
    setLoginStatus('No access_token found in URL.', false);
    alert('No access_token found. Make sure you pasted the full redirect URL.');
    return;
  }

  try {
    const data = await post('/auth/finalize', { access_token: at, id_token: it || '' });
    if (data.error) throw new Error(data.error);
    onLoggedIn(data);
  } catch (e) {
    setLoginStatus('', false);
    alert(`Login failed: ${e.message}`);
  }
}

// ── Auth success ──────────────────────────────────────────────────────────────
function onLoggedIn(d) {
  S.access_token      = d.access_token;
  S.entitlement_token = d.entitlement_token;
  S.puuid             = d.puuid;
  S.username          = d.username || 'Agent';
  S.tag               = d.tag || '0000';
  S.region            = d.region || 'ap';
  S.client_version    = d.client_version || '';
  lsSave(STORE_KEY, S);
  showApp();
  loadAll();
}

// ── App ───────────────────────────────────────────────────────────────────────
function showLogin() {
  el('login-screen').style.display = 'block';
  el('app-screen').style.display   = 'none';
}

function showApp() {
  el('login-screen').style.display = 'none';
  el('app-screen').style.display   = 'block';
  el('h-username').textContent = S.username;
  el('h-tag').textContent      = `#${S.tag}`;
  el('h-region').textContent   = S.region.toUpperCase();
  el('region-select').value    = S.region;
}

function loadAll() {
  loadBalance();
  loadStore();
  loadNightMarket();
}

async function loadBalance() {
  try {
    const d = await postStore('/balance');
    el('b-vp').textContent  = fmt(d.vp);
    el('b-rad').textContent = fmt(d.radianite);
    el('b-kc').textContent  = fmt(d.freeagents);
  } catch (_) {}
}

async function loadStore() {
  const grid = el('store-grid');
  grid.innerHTML = skeletonCards(4); // Show loading skeletons
  try {
    const d = await postStore('/store');
    grid.innerHTML = '';
    if (!d.skins?.length) {
      grid.innerHTML = emptyHTML('🏪', 'No store data available.');
      return;
    }
    d.skins.forEach(s => grid.appendChild(skinCard(s)));
    if (d.expires_in) startTimer(d.expires_in);
  } catch (e) {
    grid.innerHTML = emptyHTML('⚠️', `Store failed: ${e.message}<br><br><button class="btn-primary" style="width:auto;padding:8px 16px;margin-top:12px" onclick="loadStore()">Retry</button>`);
  }
}

async function loadNightMarket() {
  const grid = el('nm-grid');
  try {
    const d = await postStore('/nightmarket');
    if (!d.active) return;
    grid.innerHTML = '';
    d.offers.forEach(s => grid.appendChild(nmCard(s)));
  } catch (_) {}
}

// ── Card builders ─────────────────────────────────────────────────────────────
function skeletonCards(count) {
  let html = '';
  for (let i = 0; i < count; i++) {
    html += `<div class="skin-card skeleton">
      <div class="skin-img-wrap sk" style="width:68px;height:42px"></div>
      <div class="skin-info" style="flex:1">
        <div class="sk" style="height:14px;width:${60 + Math.random()*20}%;margin-bottom:6px"></div>
        <div class="sk" style="height:11px;width:${30 + Math.random()*20}%"></div>
      </div>
      <div class="sk" style="height:16px;width:60px"></div>
    </div>`;
  }
  return html;
}

function skinCard(s) {
  const div = document.createElement('div');
  div.className = 'skin-card';
  div.innerHTML = `
    ${s.icon
      ? `<div class="skin-img-wrap"><img src="${s.icon}" alt="${s.name}" onerror="this.parentElement.innerHTML='<span style=font-size:20px>${weaponEmoji(s.name)}</span>'"></div>`
      : `<div class="skin-img-wrap">${weaponEmoji(s.name)}</div>`
    }
    <div class="skin-info">
      <div class="skin-name">${s.name}</div>
      <div class="skin-type">${weaponType(s.name)}</div>
    </div>
    <div class="skin-price">💠 ${s.price > 0 ? fmt(s.price) : '—'}</div>
  `;
  return div;
}

function nmCard(s) {
  const div = document.createElement('div');
  div.className = 'skin-card';
  div.style.flexDirection = 'column';
  div.style.alignItems = 'stretch';
  div.innerHTML = `
    <div style="display:flex;align-items:center;gap:12px">
      <div class="skin-img-wrap">${weaponEmoji(s.name)}</div>
      <div class="skin-info">
        <div class="skin-name">${s.name}</div>
        <div class="skin-type">${weaponType(s.name)}</div>
      </div>
    </div>
    <div class="nm-prices">
      <span class="nm-original">💠 ${fmt(s.original_price)}</span>
      <span class="nm-discounted">💠 ${fmt(s.discounted_price)}</span>
      ${s.discount_pct > 0 ? `<span class="nm-badge">-${Math.round(s.discount_pct)}%</span>` : ''}
    </div>
  `;
  return div;
}

// ── Timer ─────────────────────────────────────────────────────────────────────
function startTimer(secs) {
  clearInterval(_storeTimer);
  const el_ = el('store-timer');
  const tick = () => {
    if (secs <= 0) { el_.textContent = ''; return; }
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    el_.textContent = `${h}h ${pad(m)}m ${pad(s)}s`;
    secs--;
  };
  tick();
  _storeTimer = setInterval(tick, 1000);
}

// ── Settings ──────────────────────────────────────────────────────────────────
function changeRegion(r) {
  S.region = r;
  lsSave(STORE_KEY, S);
  el('h-region').textContent = r.toUpperCase();
  loadAll();
}

function logout() {
  localStorage.removeItem(STORE_KEY);
  location.reload();
}

// ── Tab switching ─────────────────────────────────────────────────────────────
function switchTab(name, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  el('tab-' + name).classList.add('active');
  btn.classList.add('active');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function postStore(path) {
  return post(path, {
    access_token:      S.access_token,
    entitlement_token: S.entitlement_token,
    puuid:             S.puuid,
    region:            S.region,
    client_version:    S.client_version,
  });
}

async function post(path, body) {
  const r = await fetch(API + path, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
  });
  const d = await r.json();
  if (!r.ok) {
    // Check if token expired
    if (r.status === 401 || (d.error && d.error.includes('401'))) {
      if (confirm('Your session has expired. Login again?')) {
        logout();
      }
    }
    throw new Error(d.error || d.detail || 'Request failed');
  }
  return d;
}

function extractParam(url, key) {
  for (const sep of ['#', '?']) {
    if (url.includes(sep)) {
      try {
        const p = new URLSearchParams(url.split(sep)[1]);
        const v = p.get(key);
        if (v) return v;
      } catch (_) {}
    }
  }
  return '';
}

const WEAPON_EMOJIS = { knife:'🗡️', melee:'🗡️', operator:'🎯', marshal:'🎯', outlaw:'🎯', judge:'💥', bucky:'💥' };
const WEAPON_NAMES  = ['Vandal','Phantom','Operator','Sheriff','Ghost','Classic','Frenzy','Spectre','Bulldog','Guardian','Marshal','Outlaw','Ares','Odin','Stinger','Judge','Bucky','Shorty','Knife','Melee'];

function weaponEmoji(n='') {
  const l = n.toLowerCase();
  for (const [k, v] of Object.entries(WEAPON_EMOJIS)) if (l.includes(k)) return v;
  return '🔫';
}
function weaponType(n='') {
  const l = n.toLowerCase();
  for (const w of WEAPON_NAMES) if (l.includes(w.toLowerCase())) return w;
  return 'Weapon';
}

function emptyHTML(icon, msg) {
  return `<div class="empty-state"><div class="empty-icon">${icon}</div><p>${msg}</p></div>`;
}

function fmt(n) { return (n || 0).toLocaleString(); }
function pad(n) { return String(n).padStart(2, '0'); }
function el(id) { return document.getElementById(id); }
function lsGet(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } }
function lsSave(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} }
