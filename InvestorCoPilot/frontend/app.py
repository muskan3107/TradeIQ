"""
app.py — InvestorCoPilot AI
Website-style experience: landing page → dashboard navigation.
All backend logic preserved.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from agent.agent_core import InvestorAgent
from tools.portfolio_manager import PortfolioManager

agent = InvestorAgent()
pm    = PortfolioManager()

MARKET_DATA = [
    {"index": "NIFTY 50",   "value": "22,147.00", "change": "+0.43%", "up": True},
    {"index": "SENSEX",     "value": "73,088.33", "change": "+0.38%", "up": True},
    {"index": "BANK NIFTY", "value": "47,312.50", "change": "-0.12%", "up": False},
    {"index": "NIFTY IT",   "value": "35,640.20", "change": "+1.21%", "up": True},
]
TOP_PICKS = [
    {"stock": "TCS",      "signal": "BUY",  "conf": 87, "reason": "Strong Q4 earnings beat",     "up": True},
    {"stock": "RELIANCE", "signal": "HOLD", "conf": 72, "reason": "Stable margins, monitor Jio", "up": True},
    {"stock": "INFOSYS",  "signal": "BUY",  "conf": 81, "reason": "Deal wins accelerating",      "up": True},
    {"stock": "HDFCBANK", "signal": "HOLD", "conf": 68, "reason": "NIM pressure, await clarity", "up": False},
]
NEWS_ITEMS = [
    {"tag": "AI Insight", "headline": "TCS Q4 revenue beats estimates by 3.2% — positive momentum"},
    {"tag": "Alert",      "headline": "RBI holds repo rate; banking sector outlook stable"},
    {"tag": "AI Insight", "headline": "Infosys raises FY25 guidance — deal pipeline robust"},
    {"tag": "Market",     "headline": "FII inflows surge ₹4,200 Cr — broad market rally expected"},
]

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

@keyframes fadeIn      { from{opacity:0} to{opacity:1} }
@keyframes slideUp     { from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:translateY(0)} }
@keyframes floatY      { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes pulseDot    { 0%,100%{opacity:1} 50%{opacity:.35} }
@keyframes barFill     { from{width:0} to{width:var(--w)} }

*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
body { background:#F5F5F5 !important; }

/* ── Container ── */
.gradio-container {
    background:#F5F5F5 !important;
    font-family:'Inter','Segoe UI',sans-serif !important;
    max-width:1200px !important; width:100% !important;
    margin:0 auto !important; padding:0 0 48px !important;
}
.gradio-container>.main,
.gradio-container>.wrap { padding:0 !important; box-shadow:none !important; background:transparent !important; }

/* ── Site nav ── */
#sitenav {
    position:sticky; top:0; z-index:200;
    background:#fff; border-bottom:3px solid #E11D2E;
    padding:0 32px; height:58px;
    display:flex; align-items:center; justify-content:space-between;
    box-shadow:0 2px 14px rgba(0,0,0,.08);
}
#sitenav-logo { font-size:1.2rem; font-weight:900; color:#E11D2E; letter-spacing:-.02em; cursor:pointer; }
#sitenav-logo span { color:#1E293B; }
#sitenav-links { display:flex; align-items:center; gap:6px; }
.snav-btn {
    border:none; background:transparent; padding:7px 16px;
    font-size:.82rem; font-weight:600; color:#475569; cursor:pointer;
    border-radius:8px; transition:all .15s;
}
.snav-btn:hover { background:#F1F5F9; color:#1E293B; }
.snav-cta {
    background:#E11D2E; color:#fff !important; border-radius:8px;
    padding:7px 18px; font-size:.82rem; font-weight:700;
    border:none; cursor:pointer;
    box-shadow:0 2px 8px rgba(225,29,46,.28);
    transition:all .15s;
}
.snav-cta:hover { background:#B91C1C; transform:scale(1.03); }
#sitenav-right { display:flex; align-items:center; gap:10px; }
#demo-pill {
    background:#FEF9C3; border:1px solid #FDE68A; border-radius:20px;
    padding:3px 10px; font-size:.68rem; font-weight:700; color:#92400E;
}
#status-pill {
    display:flex; align-items:center; gap:5px;
    background:#F0FDF4; border:1px solid #BBF7D0; border-radius:20px;
    padding:3px 10px; font-size:.7rem; font-weight:600; color:#16A34A;
}
#status-pill::before { content:"●"; font-size:.55rem; animation:pulseDot 1.8s infinite; }

/* ── Page wrapper ── */
.page { display:none; padding:0 32px; animation:fadeIn .35s ease both; }
.page.active { display:block; }

/* ══════════════════════════════════════════════════════
   LANDING PAGE
══════════════════════════════════════════════════════ */

/* Hero */
#hero {
    background:linear-gradient(160deg,#fff 0%,#FFF5F5 55%,#FEE2E2 100%);
    border-radius:0 0 24px 24px;
    padding:72px 48px 64px;
    display:grid; grid-template-columns:1fr 1fr; gap:48px; align-items:center;
    margin:0 -32px 48px; animation:slideUp .5s ease both;
}
@media(max-width:768px){ #hero{grid-template-columns:1fr;padding:40px 24px;margin:0 -24px 32px;} }

#hero-eyebrow {
    font-size:.72rem; font-weight:700; color:#E11D2E;
    text-transform:uppercase; letter-spacing:.12em; margin-bottom:14px;
}
#hero-title {
    font-size:3rem; font-weight:900; color:#1E293B;
    line-height:1.1; letter-spacing:-.03em; margin-bottom:16px;
}
#hero-title span { color:#E11D2E; }
#hero-sub {
    font-size:1.05rem; color:#475569; line-height:1.65; margin-bottom:10px;
}
#hero-tagline {
    font-size:.85rem; color:#94A3B8; font-style:italic; margin-bottom:28px;
}
#hero-btns { display:flex; gap:12px; flex-wrap:wrap; }

/* Floating card stack */
#hero-visual { position:relative; height:260px; }
.hv-card {
    position:absolute; background:#fff; border-radius:16px;
    padding:18px 22px; box-shadow:0 8px 32px rgba(0,0,0,.12); width:230px;
}
.hv-card:nth-child(1){ top:0;   left:10px; animation:floatY 4s ease-in-out infinite; }
.hv-card:nth-child(2){ top:70px; left:80px; animation:floatY 4s ease-in-out infinite .9s; }
.hv-card:nth-child(3){ top:140px; left:20px; animation:floatY 4s ease-in-out infinite 1.8s; }
.hv-ticker { font-size:.68rem; font-weight:700; color:#94A3B8; text-transform:uppercase; }
.hv-val    { font-size:1.25rem; font-weight:800; color:#1E293B; margin:4px 0; }

/* Problem/Solution cards */
.ps-grid {
    display:grid; grid-template-columns:repeat(2,1fr); gap:18px;
    margin-bottom:56px; animation:slideUp .5s ease .1s both;
}
@media(max-width:640px){ .ps-grid{grid-template-columns:1fr;} }
.ps-card {
    background:#fff; border-radius:16px; padding:24px 26px;
    box-shadow:0 2px 12px rgba(0,0,0,.07);
    border-top:4px solid #E11D2E;
    transition:transform .2s,box-shadow .2s;
}
.ps-card:hover { transform:translateY(-4px); box-shadow:0 10px 28px rgba(0,0,0,.12); }
.ps-icon  { font-size:1.8rem; margin-bottom:10px; }
.ps-title { font-size:1rem; font-weight:800; color:#1E293B; margin-bottom:6px; }
.ps-body  { font-size:.83rem; color:#64748B; line-height:1.55; margin-bottom:10px; }
.ps-highlight {
    background:#FEF2F2; border-left:3px solid #E11D2E;
    border-radius:0 8px 8px 0; padding:8px 12px;
    font-size:.8rem; color:#B91C1C; font-weight:600; line-height:1.45;
}

/* How it works */
#how-section { margin-bottom:56px; animation:slideUp .5s ease .15s both; }
.how-flow {
    display:flex; align-items:center; gap:0;
    background:#fff; border-radius:16px; padding:28px 24px;
    box-shadow:0 2px 12px rgba(0,0,0,.07); flex-wrap:wrap;
}
.how-step {
    flex:1; min-width:120px; text-align:center; padding:12px 8px;
}
.how-icon  { font-size:1.6rem; margin-bottom:8px; }
.how-label { font-size:.78rem; font-weight:700; color:#1E293B; }
.how-desc  { font-size:.7rem; color:#94A3B8; margin-top:3px; line-height:1.4; }
.how-arrow {
    font-size:1.2rem; color:#E11D2E; font-weight:700;
    padding:0 4px; flex-shrink:0;
}
@media(max-width:600px){ .how-arrow{display:none;} .how-step{min-width:80px;} }

/* Features */
.feat-grid {
    display:grid; grid-template-columns:repeat(2,1fr); gap:16px;
    margin-bottom:56px; animation:slideUp .5s ease .2s both;
}
@media(max-width:640px){ .feat-grid{grid-template-columns:1fr;} }
.feat-card {
    background:#fff; border-radius:14px; padding:22px 24px;
    box-shadow:0 2px 10px rgba(0,0,0,.07);
    display:flex; gap:16px; align-items:flex-start;
    transition:transform .2s,box-shadow .2s;
}
.feat-card:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(0,0,0,.11); }
.feat-icon-wrap {
    width:44px; height:44px; border-radius:12px;
    background:#FEF2F2; display:flex; align-items:center;
    justify-content:center; font-size:1.3rem; flex-shrink:0;
}
.feat-title { font-size:.92rem; font-weight:800; color:#1E293B; margin-bottom:4px; }
.feat-desc  { font-size:.78rem; color:#64748B; line-height:1.5; }

/* Landing CTA strip */
#landing-cta {
    background:linear-gradient(135deg,#1E293B,#E11D2E);
    border-radius:16px; padding:40px 36px;
    text-align:center; margin-bottom:16px;
    animation:slideUp .5s ease .25s both;
}

/* Section titles */
.section-title {
    font-size:1.5rem; font-weight:800; color:#1E293B;
    letter-spacing:-.02em; margin-bottom:6px;
}
.section-sub {
    font-size:.88rem; color:#64748B; margin-bottom:24px; line-height:1.5;
}

/* ══════════════════════════════════════════════════════
   DASHBOARD
══════════════════════════════════════════════════════ */

/* Dashboard nav strip */
#dash-topbar {
    background:#fff; border-bottom:2px solid #E11D2E;
    padding:10px 0; margin:0 -32px 20px;
    display:flex; align-items:center; justify-content:space-between;
    padding-left:32px; padding-right:32px;
    box-shadow:0 1px 6px rgba(0,0,0,.06);
}
#dash-portfolio-val { font-size:.9rem; font-weight:700; color:#1E293B; }

/* Tab pills */
.tab-nav button {
    border-radius:20px !important; padding:7px 20px !important;
    font-size:.82rem !important; font-weight:600 !important;
    border:1.5px solid #E2E8F0 !important; background:#fff !important;
    color:#475569 !important; cursor:pointer !important;
    box-shadow:0 1px 4px rgba(0,0,0,.05) !important;
    transition:all .18s ease !important;
}
.tab-nav button.selected,
.tab-nav button[aria-selected="true"] {
    background:#E11D2E !important; color:#fff !important;
    border-color:#E11D2E !important;
    box-shadow:0 3px 10px rgba(225,29,46,.28) !important;
    transform:translateY(-1px) !important;
}
.tab-nav button:hover:not(.selected):not([aria-selected="true"]) {
    background:#FEF2F2 !important; color:#E11D2E !important;
    border-color:#FECACA !important;
}

/* Market pulse */
#market-pulse {
    background:#1E293B; border-radius:14px; padding:16px 24px;
    margin-bottom:18px; display:flex; align-items:center;
    gap:24px; flex-wrap:wrap; box-shadow:0 4px 18px rgba(0,0,0,.14);
}
#pulse-label { font-size:.68rem; font-weight:700; color:#E11D2E;
               text-transform:uppercase; letter-spacing:.1em; white-space:nowrap; }
.pulse-item  { display:flex; flex-direction:column; gap:1px; }
.pulse-name  { font-size:.65rem; color:#94A3B8; font-weight:600; text-transform:uppercase; }
.pulse-val   { font-size:1rem; font-weight:800; color:#fff; }
.pulse-chg.up   { font-size:.75rem; font-weight:700; color:#4ADE80; }
.pulse-chg.down { font-size:.75rem; font-weight:700; color:#F87171; }
.pulse-div   { width:1px; height:32px; background:rgba(255,255,255,.1); }

/* Stat cards */
.stat-grid { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:20px; }
.stat-card {
    flex:1; min-width:140px; background:#fff; border-radius:14px;
    padding:18px 20px; box-shadow:0 2px 10px rgba(0,0,0,.07);
    text-align:center; transition:transform .2s,box-shadow .2s;
}
.stat-card:hover { transform:translateY(-3px); box-shadow:0 8px 22px rgba(0,0,0,.11); }
.stat-icon  { font-size:1.5rem; margin-bottom:5px; }
.stat-val   { font-size:1.9rem; font-weight:800; color:#E11D2E; line-height:1; }
.stat-label { font-size:.73rem; color:#64748B; margin-top:4px; font-weight:500; }

/* Market 2×2 */
.mkt-grid {
    display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-bottom:20px;
}
@media(max-width:520px){ .mkt-grid{grid-template-columns:1fr;} }
.mkt-card {
    background:#fff; border-radius:14px; padding:16px 20px;
    box-shadow:0 2px 10px rgba(0,0,0,.07); border-left:4px solid #E11D2E;
    transition:transform .2s,box-shadow .2s;
}
.mkt-card:hover { transform:translateY(-3px); box-shadow:0 8px 22px rgba(0,0,0,.11); }
.mkt-name { font-size:.67rem; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:.06em; }
.mkt-val  { font-size:1.35rem; font-weight:800; color:#1E293B; margin:4px 0 2px; }
.mkt-chg.up   { color:#16A34A; font-size:.82rem; font-weight:700; }
.mkt-chg.down { color:#E11D2E; font-size:.82rem; font-weight:700; }

/* Pick cards 2-col */
.pick-grid {
    display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-bottom:20px;
}
@media(max-width:520px){ .pick-grid{grid-template-columns:1fr;} }
.pick-card {
    background:#fff; border-radius:14px; padding:16px 20px;
    box-shadow:0 2px 10px rgba(0,0,0,.07);
    transition:transform .2s,box-shadow .2s;
}
.pick-card.up-card   { border-left:4px solid #16A34A; }
.pick-card.down-card { border-left:4px solid #E11D2E; }
.pick-card:hover { transform:translateY(-3px); box-shadow:0 8px 22px rgba(0,0,0,.11); }
.pick-stock  { font-size:1rem; font-weight:800; color:#1E293B; }
.pick-reason { font-size:.75rem; color:#64748B; margin-top:5px; line-height:1.4; }
.conf-bar { height:4px; border-radius:4px; background:#F1F5F9; margin-top:10px; overflow:hidden; }
.conf-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#E11D2E,#F97316); }

/* News feed */
.news-card {
    display:flex; background:#fff; border-radius:12px; margin-bottom:10px;
    box-shadow:0 1px 6px rgba(0,0,0,.06); overflow:hidden;
    transition:transform .18s,box-shadow .18s;
}
.news-card:hover { transform:translateY(-2px); box-shadow:0 6px 18px rgba(0,0,0,.10); }
.news-strip { width:4px; flex-shrink:0; }
.news-body  { padding:11px 16px; flex:1; }
.news-headline { font-size:.84rem; color:#1E293B; font-weight:500; line-height:1.45; }

/* Badges */
.badge {
    display:inline-block; border-radius:6px;
    padding:2px 10px; font-size:.7rem; font-weight:700; letter-spacing:.04em;
}
.badge-buy   { background:#DCFCE7; color:#15803D; }
.badge-hold  { background:#FEF9C3; color:#854D0E; }
.badge-sell  { background:#FEE2E2; color:#B91C1C; }
.badge-pos   { background:#DCFCE7; color:#15803D; }
.badge-neg   { background:#FEE2E2; color:#B91C1C; }
.badge-neu   { background:#F1F5F9; color:#475569; }
.badge-ai    { background:#EDE9FE; color:#6D28D9; }
.badge-alert { background:#FEF3C7; color:#92400E; }
.badge-mkt   { background:#E0F2FE; color:#0369A1; }

/* Generic card */
.card {
    background:#fff; border-radius:14px; padding:18px 22px;
    box-shadow:0 2px 10px rgba(0,0,0,.07); margin-bottom:14px;
    transition:transform .2s,box-shadow .2s;
}
.card:hover { transform:translateY(-2px); box-shadow:0 8px 22px rgba(0,0,0,.11); }

/* Confidence */
.conf-big   { font-size:2.8rem; font-weight:800; line-height:1; }
.conf-label { font-size:.76rem; color:#64748B; margin-top:3px; }

/* Metric chips */
.metric-row { display:flex; flex-wrap:wrap; gap:10px; margin:10px 0; }
.metric-chip {
    background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px;
    padding:10px 16px; min-width:140px; box-shadow:0 1px 3px rgba(0,0,0,.04);
    transition:transform .18s,box-shadow .18s;
}
.metric-chip:hover { transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,.09); }
.metric-chip .mc-label { font-size:.65rem; color:#94A3B8; text-transform:uppercase; letter-spacing:.06em; }
.metric-chip .mc-val   { font-size:1.1rem; font-weight:800; color:#1E293B; margin-top:3px; }

/* Portfolio */
.port-summary {
    background:linear-gradient(135deg,#1E293B,#334155);
    border-radius:14px; padding:20px 24px; margin-bottom:16px;
    display:flex; justify-content:space-between; align-items:center;
    box-shadow:0 4px 20px rgba(0,0,0,.14);
}
.port-card {
    background:#fff; border-radius:14px; padding:14px 20px;
    box-shadow:0 2px 10px rgba(0,0,0,.07); margin-bottom:10px;
    display:flex; justify-content:space-between; align-items:center;
    transition:transform .18s,box-shadow .18s;
}
.port-card:hover { transform:translateY(-2px); box-shadow:0 6px 18px rgba(0,0,0,.11); }
.port-stock { font-size:.95rem; font-weight:800; color:#1E293B; }
.port-meta  { font-size:.75rem; color:#64748B; margin-top:2px; }
.port-val   { font-size:1rem; font-weight:700; color:#1E293B; text-align:right; }

/* Decision stepper */
.step-item {
    display:flex; align-items:flex-start; gap:14px;
    border-radius:12px; padding:13px 18px; margin-bottom:8px;
    border-left:3px solid; transition:transform .18s;
}
.step-item:hover { transform:translateX(3px); }

/* Buttons */
.btn-primary {
    background:#E11D2E !important; color:#fff !important;
    border-radius:10px !important; border:none !important;
    font-weight:700 !important; padding:11px 28px !important;
    font-size:.9rem !important; cursor:pointer !important;
    box-shadow:0 3px 10px rgba(225,29,46,.28) !important;
    transition:transform .15s,background .15s,box-shadow .15s !important;
}
.btn-primary:hover {
    background:#B91C1C !important; transform:scale(1.03) !important;
    box-shadow:0 5px 16px rgba(225,29,46,.38) !important;
}
.btn-outline {
    background:transparent !important; color:#E11D2E !important;
    border:2px solid #E11D2E !important; border-radius:10px !important;
    font-weight:700 !important; padding:9px 24px !important;
    font-size:.9rem !important; cursor:pointer !important;
    transition:transform .15s,background .15s !important;
}
.btn-outline:hover { background:#FEF2F2 !important; transform:scale(1.03) !important; }

/* Alert */
.alert-box {
    background:#FEF2F2; border:1px solid #FECACA; border-radius:12px;
    padding:13px 18px; color:#B91C1C; font-size:.86rem; margin:8px 0;
}

/* Section label */
.sec-header {
    font-size:.68rem; font-weight:700; color:#94A3B8;
    text-transform:uppercase; letter-spacing:.1em; margin:18px 0 10px;
}

/* Inputs */
textarea, input[type=text], input[type=number] {
    border-radius:10px !important; border:1.5px solid #E2E8F0 !important;
    font-size:.88rem !important; background:#fff !important;
    transition:border-color .15s,box-shadow .15s !important;
}
textarea:focus, input:focus {
    border-color:#E11D2E !important; outline:none !important;
    box-shadow:0 0 0 3px rgba(225,29,46,.10) !important;
}

/* Responsive */
@media(max-width:768px){
    .gradio-container { padding:0 0 32px !important; }
    .page { padding:0 16px; }
    #sitenav { padding:0 16px; }
    #dash-topbar { padding-left:16px; padding-right:16px; margin:0 -16px 16px; }
    #market-pulse { padding:14px 16px; gap:14px; }
}

/* Hide Gradio chrome */
footer { display:none !important; }
.gr-prose { font-size:.88rem !important; }
.gradio-container .tabs { background:transparent !important; }
"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def _sitenav_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    total    = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div id="sitenav">
  <div id="sitenav-logo" onclick="showPage('landing')">
    InvestorCoPilot <span>AI</span>
  </div>
  <div id="sitenav-links">
    <button class="snav-btn" onclick="showPage('landing')">Home</button>
    <button class="snav-btn" onclick="showPage('landing'); scrollTo('#features')">Features</button>
    <button class="snav-cta" onclick="showPage('dashboard')">🚀 Launch App</button>
  </div>
  <div id="sitenav-right">
    <span style="font-size:.82rem;font-weight:600;color:#1E293B">Demo Portfolio ₹{total:,.0f}</span>
    <span id="demo-pill">Demo User: Rahul Sharma</span>
    <span id="status-pill">Active</span>
  </div>
</div>
<script>
function showPage(id) {{
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  var el = document.getElementById('page-' + id);
  if (el) el.classList.add('active');
  window.scrollTo({{top:0, behavior:'smooth'}});
}}
function scrollTo(sel) {{
  setTimeout(function(){{
    var el = document.querySelector(sel);
    if (el) el.scrollIntoView({{behavior:'smooth'}});
  }}, 100);
}}
// Start on landing
document.addEventListener('DOMContentLoaded', function() {{ showPage('landing'); }});
</script>"""


# ── Landing page sections ─────────────────────────────────────────────────────

def _hero_section() -> str:
    float_cards = """
    <div class="hv-card">
      <div class="hv-ticker">TCS</div>
      <div class="hv-val">₹3,920</div>
      <span class="badge badge-buy">▲ BUY &nbsp; 87%</span>
    </div>
    <div class="hv-card">
      <div class="hv-ticker">RELIANCE</div>
      <div class="hv-val">₹2,910</div>
      <span class="badge badge-hold">● HOLD &nbsp; 72%</span>
    </div>
    <div class="hv-card">
      <div class="hv-ticker">INFOSYS</div>
      <div class="hv-val">₹1,560</div>
      <span class="badge badge-buy">▲ BUY &nbsp; 81%</span>
    </div>"""
    return f"""
<div id="hero">
  <div>
    <div id="hero-eyebrow">🇮🇳 Built for the Indian Investor</div>
    <div id="hero-title">InvestorCoPilot <span>AI</span></div>
    <p id="hero-sub">
      An AI-powered investment assistant that thinks step-by-step,
      explains every decision, and reduces blind investing.
    </p>
    <p id="hero-tagline">Transparent. Intelligent. Reliable.</p>
    <div id="hero-btns">
      <button class="btn-primary" onclick="showPage('dashboard')">🚀 Start Demo</button>
      <button class="btn-outline" onclick="scrollTo('#features')">📊 View Features</button>
    </div>
  </div>
  <div id="hero-visual">{float_cards}</div>
</div>"""


def _problem_section() -> str:
    cards = [
        ("📈", "AI vs Human Analysts",
         "Studies suggest AI models can reach ~60% prediction accuracy in financial markets.",
         "Our goal: Improve this to 80–85% using structured reasoning + multi-step validation"),
        ("⚠️", "Blind AI Reliance Problem",
         "AI cannot replace human judgment in complex, fast-moving markets.",
         "Our solution: Confidence scoring + full reasoning transparency on every insight"),
        ("🌏", "Accessibility Gap",
         "Most investment tools are not accessible to non-English speaking Indian investors.",
         "Future-ready: Vernacular language support planned for Hindi, Tamil, Telugu"),
        ("🌱", "AI Energy Concern",
         "AI queries consume significantly more energy than traditional software.",
         "Optimized hybrid system: deterministic logic first, minimal AI usage only when needed"),
    ]
    html = ""
    for icon, title, body, highlight in cards:
        html += f"""
        <div class="ps-card">
          <div class="ps-icon">{icon}</div>
          <div class="ps-title">{title}</div>
          <p class="ps-body">{body}</p>
          <div class="ps-highlight">{highlight}</div>
        </div>"""
    return f"""
<div style="margin-bottom:56px">
  <div class="section-title">Problems We're Solving</div>
  <div class="section-sub">Why InvestorCoPilot AI exists — and why it matters for judges and investors alike.</div>
  <div class="ps-grid">{html}</div>
</div>"""


def _how_section() -> str:
    steps = [
        ("📄", "User Input",    "Upload PDF or ask a question"),
        ("🤖", "Agent Plans",   "Decides which tools to run"),
        ("🔧", "Tools Execute", "Extract, analyze, score"),
        ("📊", "Output Ready",  "Structured insight generated"),
        ("🎯", "Confidence",    "Reliability score attached"),
    ]
    items = ""
    for i, (icon, label, desc) in enumerate(steps):
        items += f"""
        <div class="how-step">
          <div class="how-icon">{icon}</div>
          <div class="how-label">{label}</div>
          <div class="how-desc">{desc}</div>
        </div>"""
        if i < len(steps) - 1:
            items += '<div class="how-arrow">→</div>'
    return f"""
<div id="how-section">
  <div class="section-title">How It Works</div>
  <div class="section-sub">A transparent, step-by-step agentic pipeline — no black boxes.</div>
  <div class="how-flow">{items}</div>
</div>"""


def _features_section() -> str:
    feats = [
        ("🧠", "Agent-Based Reasoning",
         "A planning agent decides which tools to invoke, in what order, based on your query — just like a human analyst would."),
        ("📊", "Portfolio-Aware Insights",
         "Every analysis is cross-referenced with your holdings to surface only what's relevant to you."),
        ("📉", "Confidence Scoring",
         "Every insight comes with a deterministic confidence score — no guessing, no hallucination."),
        ("⚙️", "Works Without AI Dependency",
         "Core extraction and scoring uses pure regex + rule-based logic. AI (Ollama) is optional and gracefully skipped."),
    ]
    html = ""
    for icon, title, desc in feats:
        html += f"""
        <div class="feat-card">
          <div class="feat-icon-wrap">{icon}</div>
          <div>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
          </div>
        </div>"""
    return f"""
<div id="features" style="margin-bottom:56px">
  <div class="section-title">Key Features</div>
  <div class="section-sub">What makes InvestorCoPilot AI different from a generic chatbot.</div>
  <div class="feat-grid">{html}</div>
</div>"""


def _landing_cta_section() -> str:
    return """
<div id="landing-cta">
  <div style="font-size:1.6rem;font-weight:800;color:#fff;margin-bottom:10px">
    Ready to see it in action?
  </div>
  <div style="font-size:.92rem;color:rgba(255,255,255,.75);margin-bottom:24px">
    Upload a real PDF report and watch the agent reason through it — step by step.
  </div>
  <button class="btn-primary" onclick="showPage('dashboard')"
          style="font-size:1rem;padding:13px 36px">
    🚀 Start Using Demo
  </button>
</div>"""


def _full_landing_html() -> str:
    return (
        _hero_section()
        + _problem_section()
        + _how_section()
        + _features_section()
        + _landing_cta_section()
    )


# ── Dashboard helpers ─────────────────────────────────────────────────────────

def _dash_topbar_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    total    = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div id="dash-topbar">
  <span style="font-size:.8rem;color:#64748B">
    👤 <strong>Rahul Sharma</strong> &nbsp;·&nbsp; Demo portfolio for showcasing personalized insights
  </span>
  <span id="dash-portfolio-val">Demo Portfolio ₹{total:,.0f}</span>
</div>"""


def _market_pulse_html() -> str:
    items = ""
    for i, m in enumerate(MARKET_DATA):
        cls = "up" if m["up"] else "down"
        arrow = "▲" if m["up"] else "▼"
        items += f"""
        <div class="pulse-item">
          <span class="pulse-name">{m['index']}</span>
          <span class="pulse-val">{m['value']}</span>
          <span class="pulse-chg {cls}">{arrow} {m['change']}</span>
        </div>"""
        if i < len(MARKET_DATA) - 1:
            items += '<div class="pulse-div"></div>'
    return f'<div id="market-pulse"><span id="pulse-label">📡 Market Pulse</span>{items}</div>'


def _stat_cards_html() -> str:
    stats = [("📡","47","Signals today"),("💡","12","Insights generated"),("🎯","78%","Avg confidence")]
    cards = "".join(f"""
    <div class="stat-card">
      <div class="stat-icon">{i}</div>
      <div class="stat-val">{v}</div>
      <div class="stat-label">{l}</div>
    </div>""" for i,v,l in stats)
    return f'<div class="stat-grid">{cards}</div>'


def _markets_tab_html() -> str:
    mkt = "".join(f"""
    <div class="mkt-card">
      <div class="mkt-name">{m['index']}</div>
      <div class="mkt-val">{m['value']}</div>
      <div class="mkt-chg {'up' if m['up'] else 'down'}">{'▲' if m['up'] else '▼'} {m['change']}</div>
    </div>""" for m in MARKET_DATA)

    sig_cls = {"BUY":"badge-buy","HOLD":"badge-hold","SELL":"badge-sell"}
    picks = "".join(f"""
    <div class="pick-card {'up-card' if p['up'] else 'down-card'}">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span class="pick-stock">{p['stock']}</span>
        <span class="badge {sig_cls[p['signal']]}">{p['signal']}</span>
      </div>
      <div class="pick-reason">{p['reason']}</div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:10px">
        <div class="conf-bar" style="flex:1"><div class="conf-fill" style="width:{p['conf']}%"></div></div>
        <span style="font-size:.73rem;font-weight:700;color:#475569">{p['conf']}%</span>
      </div>
    </div>""" for p in TOP_PICKS)

    tag_color = {"AI Insight":"#6D28D9","Alert":"#D97706","Market":"#0369A1"}
    tag_badge = {"AI Insight":"badge-ai","Alert":"badge-alert","Market":"badge-mkt"}
    news = "".join(f"""
    <div class="news-card">
      <div class="news-strip" style="background:{tag_color.get(n['tag'],'#94A3B8')}"></div>
      <div class="news-body">
        <span class="badge {tag_badge.get(n['tag'],'badge-mkt')}"
              style="margin-bottom:5px;display:inline-block">{n['tag']}</span>
        <div class="news-headline">{n['headline']}</div>
      </div>
    </div>""" for n in NEWS_ITEMS)

    return f"""
{_market_pulse_html()}
{_stat_cards_html()}
<div class="sec-header">Market Overview</div>
<div class="mkt-grid">{mkt}</div>
<div class="sec-header">Top Opportunities</div>
<div class="pick-grid">{picks}</div>
<div class="sec-header">Latest Insights</div>
{news}"""


def _metric_chips(metrics: dict) -> str:
    labels = {"revenue":"Revenue (₹ Cr)","profit":"Net Profit (₹ Cr)","margin":"Margin %","growth":"YoY Growth %"}
    chips = "".join(f"""
    <div class="metric-chip">
      <div class="mc-label">{label}</div>
      <div class="mc-val">{f"{metrics[k]:,.2f}" if metrics.get(k) is not None else "—"}</div>
    </div>""" for k, label in labels.items())
    return f'<div class="metric-row">{chips}</div>'


def _sentiment_badge(sentiment: dict) -> str:
    label = sentiment.get("sentiment","neutral")
    score = sentiment.get("score",0.5)
    pos   = sentiment.get("positive_signals",0)
    neg   = sentiment.get("negative_signals",0)
    cls   = {"positive":"badge-pos","negative":"badge-neg"}.get(label,"badge-neu")
    icon  = {"positive":"▲","negative":"▼"}.get(label,"●")
    bg    = {"positive":"#F0FDF4","negative":"#FEF2F2"}.get(label,"#F8FAFC")
    return f"""
<div class="card" style="display:flex;align-items:center;gap:18px;background:{bg}">
  <span class="badge {cls}" style="font-size:.88rem;padding:5px 16px">{icon} {label.upper()}</span>
  <div style="font-size:.8rem;color:#64748B">
    Score <strong>{score:.2f}</strong> &nbsp;|&nbsp;
    <span style="color:#16A34A;font-weight:600">+{pos} positive</span> &nbsp;
    <span style="color:#E11D2E;font-weight:600">−{neg} negative</span>
  </div>
</div>"""


def _confidence_card(conf: dict) -> str:
    pct   = conf.get("percentage",0)
    label = conf.get("label","Low")
    color = "#16A34A" if pct>=80 else "#D97706" if pct>=50 else "#E11D2E"
    factors = "".join(f"""
    <div style="display:flex;gap:8px;align-items:center;padding:5px 0;
                border-bottom:1px solid #F1F5F9;font-size:.79rem;color:#475569">
      <span>{"✅" if "✅" in f else "⚠️" if "⚠️" in f else "❌"}</span><span>{f}</span>
    </div>""" for f in conf.get("factors",[]))
    return f"""
<div class="card" style="display:flex;gap:24px;align-items:flex-start">
  <div style="text-align:center;min-width:88px">
    <div class="conf-big" style="color:{color}">{pct}%</div>
    <div class="conf-label">{label} Confidence</div>
    <div style="height:5px;border-radius:5px;background:#F1F5F9;margin-top:8px;overflow:hidden">
      <div style="height:100%;width:{pct}%;background:{color};border-radius:5px"></div>
    </div>
  </div>
  <div style="flex:1">{factors}</div>
</div>"""


def _portfolio_impact_card(impact: dict) -> str:
    msg   = impact.get("note") or impact.get("impact_message","No portfolio data.")
    sig   = impact.get("sentiment_signal","neutral")
    cls   = {"positive":"badge-pos","negative":"badge-neg"}.get(sig,"badge-neu")
    count = impact.get("positions_affected",0)
    return f"""
<div class="card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
    <span style="font-weight:700;font-size:.92rem;color:#1E293B">Portfolio Impact</span>
    <span class="badge {cls}">{sig.upper()}</span>
  </div>
  <div style="font-size:.84rem;color:#475569;line-height:1.5">{msg}</div>
  <div style="font-size:.74rem;color:#94A3B8;margin-top:8px">{count} position(s) affected</div>
</div>"""


def _trace_html(trace: list) -> str:
    STEP_MAP = [
        ("receive_task",       "Request received",       "Your query was received and the analysis was started."),
        ("plan_created",       "Analysis plan created",  "Decided which tools to run and in what order."),
        ("document_processor", "Document extracted",     "Read and extracted text from the uploaded report."),
        ("metric_extractor",   "Key metrics identified", "Found financial figures like revenue, profit, and margins."),
        ("sentiment_analyzer", "Sentiment analysed",     "Scanned the report for positive and negative signals."),
        ("portfolio_manager",  "Portfolio checked",      "Looked up your holdings to assess relevance."),
        ("alert_scanner",      "Alerts scanned",         "Checked for any active alerts on your positions."),
        ("confidence_engine",  "Confidence calculated",  "Scored the reliability of this analysis."),
        ("ai_enhancer",        "AI summary generated",   "Created a plain-English summary of the findings."),
        ("question_classifier","Question understood",    "Classified your question to find the best answer."),
        ("task_complete",      "Analysis complete",      "All steps finished. Results are ready."),
    ]
    def _st(r):
        l = r.lower()
        return "error" if "error:" in l else "done"

    COLOR = {"done":"#15803D","error":"#B91C1C"}
    BG    = {"done":"#F0FDF4","error":"#FEF2F2"}
    ICON  = {"done":"✅","error":"❌"}
    LBL   = {"done":"Completed","error":"Failed"}

    seen, steps = set(), []
    for raw in trace:
        for token, label, desc in STEP_MAP:
            if token in raw.lower() and token not in seen:
                seen.add(token)
                st = _st(raw)
                steps.append((ICON[st], label, desc, st))
                break

    if not steps:
        return "<p style='color:#94A3B8;font-size:.82rem;padding:8px 0'>No steps recorded.</p>"

    items = ""
    for i, (icon, label, desc, st) in enumerate(steps, 1):
        items += f"""
        <div class="step-item" style="background:{BG[st]};border-color:{COLOR[st]}">
          <div style="font-size:1.3rem;line-height:1">{icon}</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
              <span style="font-size:.73rem;font-weight:700;color:#94A3B8">Step {i}</span>
              <span style="font-size:.69rem;font-weight:700;color:{COLOR[st]};
                           background:#fff;border:1px solid {COLOR[st]};
                           border-radius:20px;padding:1px 8px">{LBL[st]}</span>
            </div>
            <div style="font-size:.9rem;font-weight:700;color:#1E293B">{label}</div>
            <div style="font-size:.77rem;color:#64748B;margin-top:2px">{desc}</div>
          </div>
        </div>"""
    return items


def _portfolio_summary_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    total    = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div class="port-summary">
  <div>
    <div style="font-size:.68rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:.08em">
      Demo Portfolio — Rahul Sharma
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#fff;margin-top:4px">₹{total:,.0f}</div>
    <div style="font-size:.74rem;color:#94A3B8;margin-top:4px">
      {len(holdings)} positions &nbsp;·&nbsp; Demo portfolio for showcasing personalized insights
    </div>
  </div>
  <span style="background:#FEF9C3;border:1px solid #FDE68A;border-radius:20px;
               padding:4px 12px;font-size:.7rem;font-weight:700;color:#92400E">Demo Mode</span>
</div>"""


def _portfolio_cards_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    if not holdings:
        return '<div class="alert-box">No holdings found. Add your first stock below.</div>'
    html = ""
    for h in holdings:
        value = h["quantity"] * h["avg_price"]
        html += f"""
<div class="port-card">
  <div>
    <div class="port-stock">{h['stock']}</div>
    <div class="port-meta">{h['quantity']} shares @ ₹{h['avg_price']:,.2f}</div>
  </div>
  <div class="port-val">₹{value:,.0f}</div>
</div>"""
    return html

# ─────────────────────────────────────────────────────────────────────────────
# BACKEND HANDLERS (logic unchanged)
# ─────────────────────────────────────────────────────────────────────────────

def handle_analyze(pdf_file, stock_name: str):
    if pdf_file is None:
        return '<div class="alert-box">⚠️ Please upload a PDF report first.</div>', "", "", "", "", ""
    task_data = {
        "pdf_path":   pdf_file.name,
        "stock_name": stock_name.strip().upper() if stock_name.strip() else None,
        "user_id":    "demo_user",
    }
    result = agent.receive_task("analyze_document", task_data)
    if not result.get("success"):
        warnings = result.get("warnings", ["Analysis failed."])
        return f'<div class="alert-box">⚠️ {" | ".join(warnings)}</div>', "", "", "", "", ""

    conf_html    = _confidence_card(result.get("confidence") or {})
    metrics_html = _metric_chips((result.get("metrics") or {}).get("metrics") or result.get("metrics") or {})
    sent_html    = _sentiment_badge(result.get("sentiment") or {})
    impact_html  = _portfolio_impact_card(result.get("portfolio_impact") or {})
    summary_html = ""
    if result.get("summary"):
        summary_html = f'<div class="card"><div class="sec-header">AI Summary</div><p style="font-size:.88rem;color:#1E293B;line-height:1.6">{result["summary"]}</p></div>'
    trace_html = _trace_html(result.get("reasoning_trace") or [])
    return "", conf_html, metrics_html, sent_html, impact_html + summary_html, trace_html


def handle_question(question: str):
    if not question.strip():
        return '<div class="alert-box">⚠️ Please enter a question.</div>', "", ""
    result = agent.receive_task("answer_question", {"question": question.strip(), "user_id": "demo_user"})

    qc  = result.get("question_class") or {}
    cat = qc.get("category", "general_query").replace("_", " ").title()
    qc_html = f"""
<div class="card" style="margin-bottom:12px">
  <div class="sec-header">Query Classification</div>
  <span class="badge badge-ai" style="font-size:.8rem;padding:3px 12px">{cat}</span>
</div>"""

    port = result.get("portfolio") or {}
    if isinstance(port, dict) and port.get("owns_stock"):
        port_html = _portfolio_impact_card(port)
    else:
        holdings = pm.get_all_holdings("demo_user")
        rows = "".join(
            f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #F1F5F9">'
            f'<span style="font-size:.83rem;font-weight:700">{h["stock"]}</span>'
            f'<span style="font-size:.82rem;color:#64748B">{h["quantity"]} @ ₹{h["avg_price"]:,.0f}</span>'
            f'<span style="font-size:.83rem;font-weight:700">₹{h["quantity"]*h["avg_price"]:,.0f}</span></div>'
            for h in holdings
        )
        port_html = f'<div class="card"><div class="sec-header">Demo Portfolio — Rahul Sharma</div><p style="font-size:.72rem;color:#94A3B8;margin:0 0 8px">Demo portfolio for showcasing personalized insights</p>{rows}</div>'

    conf_html  = _confidence_card(result.get("confidence") or {})
    trace_html = _trace_html(result.get("reasoning_trace") or [])
    return qc_html + port_html, conf_html, trace_html


def handle_add_stock(stock: str, qty: str, price: str):
    try:
        if not stock.strip():
            return '<div class="alert-box">⚠️ Stock ticker is required.</div>', _portfolio_cards_html()
        pm.add_holding("demo_user", stock.strip().upper(), int(qty), float(price))
        return (
            f'<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;'
            f'padding:11px 16px;color:#15803D;font-size:.86rem">'
            f'✅ {stock.upper()} added to Demo Portfolio.</div>',
            _portfolio_cards_html()
        )
    except Exception as e:
        return f'<div class="alert-box">⚠️ {e}</div>', _portfolio_cards_html()


# ─────────────────────────────────────────────────────────────────────────────
# GRADIO LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

def launch_app(port: int = 7860, share: bool = False):
    with gr.Blocks(
        css=CSS,
        title="InvestorCoPilot AI",
        theme=gr.themes.Soft(
            primary_hue=gr.themes.colors.red,
            neutral_hue=gr.themes.colors.slate,
            font=gr.themes.GoogleFont("Inter"),
        ),
    ) as demo:

        # ── Site nav (always visible) ─────────────────────────────────────────
        gr.HTML(_sitenav_html())

        # ── LANDING PAGE ──────────────────────────────────────────────────────
        with gr.Group(elem_id="page-landing", elem_classes="page active"):
            gr.HTML(_full_landing_html())

        # ── DASHBOARD ─────────────────────────────────────────────────────────
        with gr.Group(elem_id="page-dashboard", elem_classes="page"):
            gr.HTML(_dash_topbar_html())

            with gr.Tabs(elem_classes="tab-nav"):

                # 📊 Markets
                with gr.TabItem("📊 Markets"):
                    gr.HTML(_markets_tab_html())

                # 📄 Analyze
                with gr.TabItem("📄 Analyze"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.HTML('<div class="sec-header">Upload Report</div>')
                            pdf_input   = gr.File(label="PDF Report", file_types=[".pdf"])
                            stock_input = gr.Textbox(label="Stock Ticker (optional)", placeholder="e.g. TCS")
                            analyze_btn = gr.Button("🔍 Analyze Report", elem_classes="btn-primary")
                        with gr.Column(scale=2):
                            analyze_err     = gr.HTML()
                            analyze_conf    = gr.HTML()
                            analyze_metrics = gr.HTML()
                            analyze_sent    = gr.HTML()
                            analyze_impact  = gr.HTML()

                    with gr.Accordion("💡 How this insight was generated", open=False):
                        analyze_trace = gr.HTML()

                    analyze_btn.click(
                        fn=handle_analyze,
                        inputs=[pdf_input, stock_input],
                        outputs=[analyze_err, analyze_conf, analyze_metrics,
                                 analyze_sent, analyze_impact, analyze_trace],
                    )

                # 💬 Insights
                with gr.TabItem("💬 Insights"):
                    gr.HTML('<div class="sec-header">Ask About a Stock or Market</div>')
                    with gr.Row():
                        q_input = gr.Textbox(
                            placeholder="e.g. What is the impact on my TCS holding?",
                            label="", lines=2, scale=4,
                        )
                        q_btn = gr.Button("Ask", elem_classes="btn-primary", scale=1)

                    insights_main  = gr.HTML()
                    insights_conf  = gr.HTML()

                    with gr.Accordion("💡 How this insight was generated", open=False):
                        insights_trace = gr.HTML()

                    q_btn.click(
                        fn=handle_question,
                        inputs=[q_input],
                        outputs=[insights_main, insights_conf, insights_trace],
                    )

                # 📁 Portfolio
                with gr.TabItem("📁 Portfolio"):
                    gr.HTML(_portfolio_summary_html())
                    portfolio_display = gr.HTML(_portfolio_cards_html())

                    gr.HTML('<div class="sec-header" style="margin-top:20px">Add / Update Position</div>')
                    with gr.Row():
                        add_stock = gr.Textbox(label="Ticker",        placeholder="TCS",  scale=2)
                        add_qty   = gr.Textbox(label="Quantity",      placeholder="50",   scale=1)
                        add_price = gr.Textbox(label="Avg Price (₹)", placeholder="3850", scale=1)
                        add_btn   = gr.Button("Add", elem_classes="btn-primary", scale=1)

                    add_msg = gr.HTML()
                    add_btn.click(
                        fn=handle_add_stock,
                        inputs=[add_stock, add_qty, add_price],
                        outputs=[add_msg, portfolio_display],
                    )

    demo.launch(server_port=port, share=share)


if __name__ == "__main__":
    launch_app()
