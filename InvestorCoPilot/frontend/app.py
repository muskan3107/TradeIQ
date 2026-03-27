"""
app.py — InvestorCoPilot AI  |  Premium Fintech Dashboard
ET-style, full-width, animated, responsive.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from agent.agent_core import InvestorAgent
from tools.portfolio_manager import PortfolioManager

agent = InvestorAgent()
pm    = PortfolioManager()

# ── Static demo data ──────────────────────────────────────────────────────────
MARKET_DATA = [
    {"index": "NIFTY 50",   "value": "22,147.00", "change": "+0.43%", "up": True},
    {"index": "SENSEX",     "value": "73,088.33", "change": "+0.38%", "up": True},
    {"index": "BANK NIFTY", "value": "47,312.50", "change": "-0.12%", "up": False},
    {"index": "NIFTY IT",   "value": "35,640.20", "change": "+1.21%", "up": True},
]
TOP_PICKS = [
    {"stock": "TCS",      "signal": "BUY",  "conf": 87, "reason": "Strong Q4 earnings beat",        "up": True},
    {"stock": "RELIANCE", "signal": "HOLD", "conf": 72, "reason": "Stable margins, monitor Jio",    "up": True},
    {"stock": "INFOSYS",  "signal": "BUY",  "conf": 81, "reason": "Deal wins accelerating",         "up": True},
    {"stock": "HDFCBANK", "signal": "HOLD", "conf": 68, "reason": "NIM pressure, await clarity",    "up": False},
]
NEWS_ITEMS = [
    {"tag": "AI Insight", "headline": "TCS Q4 revenue beats estimates by 3.2% — positive momentum",    "color": "#6D28D9"},
    {"tag": "Alert",      "headline": "RBI holds repo rate; banking sector outlook stable",             "color": "#92400E"},
    {"tag": "AI Insight", "headline": "Infosys raises FY25 guidance — deal pipeline robust",           "color": "#6D28D9"},
    {"tag": "Market",     "headline": "FII inflows surge ₹4,200 Cr — broad market rally expected",    "color": "#0369A1"},
]

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Keyframes ── */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes floatCard {
  0%,100% { transform: translateY(0px);   box-shadow: 0 8px 32px rgba(0,0,0,.13); }
  50%      { transform: translateY(-8px); box-shadow: 0 18px 40px rgba(0,0,0,.18); }
}
@keyframes pulse-dot {
  0%,100% { opacity: 1; }
  50%      { opacity: .4; }
}
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position:  400px 0; }
}

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #F5F5F5 !important; }

.gradio-container {
    background: #F5F5F5 !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    max-width: 1200px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 0 24px 40px !important;
}
.gradio-container > .main,
.gradio-container > .wrap { padding: 0 !important; box-shadow: none !important; background: transparent !important; }

/* ── Sticky top nav ── */
#topnav {
    position: sticky; top: 0; z-index: 100;
    background: #fff;
    border-bottom: 2px solid #E11D2E;
    padding: 12px 28px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 12px rgba(0,0,0,.09);
    margin-left: -24px; margin-right: -24px;
    margin-bottom: 20px;
}
#nav-title { font-size: 1.3rem; font-weight: 800; color: #E11D2E; letter-spacing: -.02em; }
#nav-sub   { font-size: .72rem; color: #64748B; margin-top: 1px; }
#nav-right { display: flex; align-items: center; gap: 14px; }
#portfolio-val { font-size: .92rem; font-weight: 700; color: #1E293B; }
#demo-badge {
    background: #FEF9C3; border: 1px solid #FDE68A;
    border-radius: 20px; padding: 3px 10px;
    font-size: .68rem; font-weight: 700; color: #92400E;
}
#status-dot {
    display: flex; align-items: center; gap: 5px;
    font-size: .72rem; color: #16A34A; font-weight: 600;
    background: #F0FDF4; border: 1px solid #BBF7D0;
    border-radius: 20px; padding: 3px 10px;
}
#status-dot::before {
    content: "●"; font-size: .58rem;
    animation: pulse-dot 1.8s ease-in-out infinite;
}

/* ── Landing hero ── */
#landing {
    background: linear-gradient(135deg, #fff 0%, #FFF5F5 60%, #FEE2E2 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(225,29,46,.08);
    animation: fadeSlideUp .6s ease both;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: center;
}
@media (max-width: 700px) { #landing { grid-template-columns: 1fr; padding: 28px 20px; } }

#landing-title {
    font-size: 2.1rem; font-weight: 800; color: #1E293B;
    line-height: 1.2; letter-spacing: -.03em; margin-bottom: 12px;
}
#landing-title span { color: #E11D2E; }
#landing-sub {
    font-size: .95rem; color: #64748B; line-height: 1.6; margin-bottom: 24px;
}
#landing-btns { display: flex; gap: 12px; flex-wrap: wrap; }

/* Floating card stack */
#card-stack { position: relative; height: 220px; }
.float-card {
    position: absolute; background: #fff; border-radius: 14px;
    padding: 16px 20px; box-shadow: 0 8px 32px rgba(0,0,0,.13);
    width: 220px;
}
.float-card:nth-child(1) { top: 0;   left: 20px; animation: floatCard 4s ease-in-out infinite; }
.float-card:nth-child(2) { top: 60px; left: 80px; animation: floatCard 4s ease-in-out infinite .8s; }
.float-card:nth-child(3) { top: 120px; left: 30px; animation: floatCard 4s ease-in-out infinite 1.6s; }
.fc-ticker { font-size: .7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; }
.fc-val    { font-size: 1.2rem; font-weight: 800; color: #1E293B; margin: 3px 0; }
.fc-badge  { display: inline-block; border-radius: 6px; padding: 2px 10px;
             font-size: .7rem; font-weight: 700; }

/* ── Tab pills ── */
.tab-nav button {
    border-radius: 20px !important; padding: 7px 22px !important;
    font-size: .83rem !important; font-weight: 600 !important;
    border: 1.5px solid #E2E8F0 !important; background: #fff !important;
    color: #475569 !important; cursor: pointer !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.06) !important;
    transition: all .2s ease !important;
}
.tab-nav button.selected,
.tab-nav button[aria-selected="true"] {
    background: #E11D2E !important; color: #fff !important;
    border-color: #E11D2E !important;
    box-shadow: 0 3px 10px rgba(225,29,46,.30) !important;
    transform: translateY(-1px) !important;
}
.tab-nav button:hover:not(.selected):not([aria-selected="true"]) {
    background: #FEF2F2 !important; color: #E11D2E !important;
    border-color: #FECACA !important; transform: translateY(-1px) !important;
}

/* ── Generic card ── */
.card {
    background: #fff; border-radius: 14px; padding: 18px 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07); margin-bottom: 14px;
    transition: transform .2s ease, box-shadow .2s ease;
    animation: fadeSlideUp .5s ease both;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }

/* ── Market pulse strip ── */
#market-pulse {
    background: #1E293B; border-radius: 14px; padding: 18px 24px;
    margin-bottom: 18px; display: flex; align-items: center;
    gap: 28px; flex-wrap: wrap;
    box-shadow: 0 4px 20px rgba(0,0,0,.15);
    animation: fadeSlideUp .4s ease both;
}
#pulse-label { font-size: .72rem; font-weight: 700; color: #E11D2E;
               text-transform: uppercase; letter-spacing: .1em; white-space: nowrap; }
.pulse-item { display: flex; flex-direction: column; gap: 2px; }
.pulse-name { font-size: .68rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; }
.pulse-val  { font-size: 1.05rem; font-weight: 800; color: #fff; }
.pulse-chg.up   { font-size: .78rem; font-weight: 700; color: #4ADE80; }
.pulse-chg.down { font-size: .78rem; font-weight: 700; color: #F87171; }
.pulse-divider  { width: 1px; height: 36px; background: rgba(255,255,255,.12); }

/* ── Market 2×2 grid ── */
.mkt-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 14px; margin-bottom: 20px;
}
@media (max-width: 540px) { .mkt-grid { grid-template-columns: 1fr; } }
.mkt-card {
    background: #fff; border-radius: 14px; padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07);
    border-left: 4px solid #E11D2E;
    transition: transform .2s, box-shadow .2s;
    animation: fadeSlideUp .5s ease both;
}
.mkt-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.mkt-name { font-size: .68rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
.mkt-val  { font-size: 1.4rem; font-weight: 800; color: #1E293B; margin: 5px 0 3px; }
.mkt-chg.up   { color: #16A34A; font-size: .84rem; font-weight: 700; }
.mkt-chg.down { color: #E11D2E; font-size: .84rem; font-weight: 700; }

/* ── Opportunities 2-col ── */
.pick-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 14px; margin-bottom: 20px;
}
@media (max-width: 540px) { .pick-grid { grid-template-columns: 1fr; } }
.pick-card {
    background: #fff; border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07);
    transition: transform .2s, box-shadow .2s;
    animation: fadeSlideUp .5s ease both;
}
.pick-card.up-card   { border-left: 4px solid #16A34A; }
.pick-card.down-card { border-left: 4px solid #E11D2E; }
.pick-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.pick-stock  { font-size: 1.05rem; font-weight: 800; color: #1E293B; }
.pick-reason { font-size: .76rem; color: #64748B; margin-top: 5px; line-height: 1.45; }
.pick-conf-bar { height: 4px; border-radius: 4px; background: #F1F5F9; margin-top: 10px; overflow: hidden; }
.pick-conf-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg,#E11D2E,#F97316); }

/* ── News feed ── */
.news-card {
    display: flex; align-items: flex-start; gap: 0;
    background: #fff; border-radius: 12px; margin-bottom: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,.06); overflow: hidden;
    transition: transform .18s, box-shadow .18s;
    animation: fadeSlideUp .5s ease both;
}
.news-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,.10); }
.news-strip { width: 4px; flex-shrink: 0; }
.news-body  { padding: 11px 16px; flex: 1; }
.news-headline { font-size: .86rem; color: #1E293B; font-weight: 500; line-height: 1.45; }

/* ── Badges ── */
.badge {
    display: inline-block; border-radius: 6px;
    padding: 2px 10px; font-size: .71rem; font-weight: 700; letter-spacing: .04em;
}
.badge-buy   { background: #DCFCE7; color: #15803D; }
.badge-hold  { background: #FEF9C3; color: #854D0E; }
.badge-sell  { background: #FEE2E2; color: #B91C1C; }
.badge-pos   { background: #DCFCE7; color: #15803D; }
.badge-neg   { background: #FEE2E2; color: #B91C1C; }
.badge-neu   { background: #F1F5F9; color: #475569; }
.badge-ai    { background: #EDE9FE; color: #6D28D9; }
.badge-alert { background: #FEF3C7; color: #92400E; }
.badge-mkt   { background: #E0F2FE; color: #0369A1; }

/* ── Hero stat cards ── */
.stat-grid {
    display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 20px;
}
.stat-card {
    flex: 1; min-width: 150px; background: #fff; border-radius: 14px;
    padding: 20px 22px; box-shadow: 0 2px 10px rgba(0,0,0,.07);
    text-align: center; transition: transform .2s, box-shadow .2s;
    animation: fadeSlideUp .5s ease both;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.stat-icon  { font-size: 1.7rem; margin-bottom: 6px; }
.stat-val   { font-size: 2rem; font-weight: 800; color: #E11D2E; line-height: 1; }
.stat-label { font-size: .76rem; color: #64748B; margin-top: 5px; font-weight: 500; }

/* ── Confidence display ── */
.conf-big   { font-size: 2.8rem; font-weight: 800; line-height: 1; }
.conf-label { font-size: .78rem; color: #64748B; margin-top: 3px; }

/* ── Metric chips ── */
.metric-row { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0; }
.metric-chip {
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 10px; padding: 10px 16px; min-width: 140px;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
    transition: transform .18s, box-shadow .18s;
}
.metric-chip:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.09); }
.metric-chip .mc-label { font-size: .66rem; color: #94A3B8; text-transform: uppercase; letter-spacing: .06em; }
.metric-chip .mc-val   { font-size: 1.1rem; font-weight: 800; color: #1E293B; margin-top: 3px; }

/* ── Portfolio cards ── */
.port-summary {
    background: linear-gradient(135deg,#1E293B,#334155);
    border-radius: 14px; padding: 20px 24px; margin-bottom: 16px;
    display: flex; justify-content: space-between; align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,.15);
    animation: fadeSlideUp .4s ease both;
}
.port-card {
    background: #fff; border-radius: 14px; padding: 14px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07); margin-bottom: 10px;
    display: flex; justify-content: space-between; align-items: center;
    transition: transform .18s, box-shadow .18s;
    animation: fadeSlideUp .5s ease both;
}
.port-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,.11); }
.port-stock { font-size: .95rem; font-weight: 800; color: #1E293B; }
.port-meta  { font-size: .76rem; color: #64748B; margin-top: 2px; }
.port-val   { font-size: 1rem; font-weight: 700; color: #1E293B; text-align: right; }

/* ── Decision stepper ── */
.step-item {
    display: flex; align-items: flex-start; gap: 14px;
    border-radius: 12px; padding: 13px 18px; margin-bottom: 8px;
    border-left: 3px solid; transition: transform .18s;
    animation: fadeSlideUp .4s ease both;
}
.step-item:hover { transform: translateX(3px); }

/* ── Loading overlay ── */
#loading-overlay {
    display: none; position: fixed; inset: 0; z-index: 9999;
    background: rgba(255,255,255,.88); backdrop-filter: blur(4px);
    align-items: center; justify-content: center; flex-direction: column; gap: 16px;
}
#loading-overlay.active { display: flex; }
.loading-dots span {
    display: inline-block; width: 10px; height: 10px; border-radius: 50%;
    background: #E11D2E; margin: 0 4px;
    animation: pulse-dot 1.2s ease-in-out infinite;
}
.loading-dots span:nth-child(2) { animation-delay: .2s; }
.loading-dots span:nth-child(3) { animation-delay: .4s; }

/* ── Buttons ── */
.btn-primary {
    background: #E11D2E !important; color: #fff !important;
    border-radius: 10px !important; border: none !important;
    font-weight: 700 !important; padding: 11px 28px !important;
    font-size: .9rem !important; cursor: pointer !important;
    box-shadow: 0 3px 10px rgba(225,29,46,.28) !important;
    transition: transform .15s, background .15s, box-shadow .15s !important;
}
.btn-primary:hover {
    background: #B91C1C !important; transform: scale(1.03) !important;
    box-shadow: 0 5px 16px rgba(225,29,46,.38) !important;
}
.btn-outline {
    background: transparent !important; color: #E11D2E !important;
    border: 2px solid #E11D2E !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: 9px 24px !important;
    font-size: .9rem !important; cursor: pointer !important;
    transition: transform .15s, background .15s !important;
}
.btn-outline:hover {
    background: #FEF2F2 !important; transform: scale(1.03) !important;
}

/* ── Alert / success ── */
.alert-box {
    background: #FEF2F2; border: 1px solid #FECACA;
    border-radius: 12px; padding: 13px 18px;
    color: #B91C1C; font-size: .86rem; margin: 8px 0;
    animation: fadeSlideUp .3s ease both;
}

/* ── Section label ── */
.sec-header {
    font-size: .69rem; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: .1em; margin: 18px 0 10px;
}

/* ── Inputs ── */
textarea, input[type=text], input[type=number] {
    border-radius: 10px !important; border: 1.5px solid #E2E8F0 !important;
    font-size: .88rem !important; background: #fff !important;
    transition: border-color .15s, box-shadow .15s !important;
}
textarea:focus, input:focus {
    border-color: #E11D2E !important; outline: none !important;
    box-shadow: 0 0 0 3px rgba(225,29,46,.10) !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .gradio-container { padding: 0 12px 24px !important; }
    #topnav { padding: 10px 16px; margin-left: -12px; margin-right: -12px; }
    #landing-title { font-size: 1.5rem; }
    .stat-grid { gap: 8px; }
}

/* ── Hide Gradio chrome ── */
footer { display: none !important; }
.gr-prose { font-size: .88rem !important; }
.gradio-container .tabs { background: transparent !important; }
"""

# ── HTML helpers ──────────────────────────────────────────────────────────────

def _topnav_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    total    = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div id="topnav">
  <div>
    <p id="nav-title">InvestorCoPilot AI</p>
    <p id="nav-sub">Your AI Investment Analyst</p>
  </div>
  <div id="nav-right">
    <span id="portfolio-val">Demo Portfolio ₹{total:,.0f}</span>
    <span id="demo-badge">Sample Data</span>
    <span id="status-dot">Active</span>
  </div>
</div>"""


def _landing_html() -> str:
    float_cards = """
    <div class="float-card">
      <div class="fc-ticker">TCS</div>
      <div class="fc-val">₹3,920</div>
      <span class="fc-badge" style="background:#DCFCE7;color:#15803D">▲ BUY  87%</span>
    </div>
    <div class="float-card">
      <div class="fc-ticker">RELIANCE</div>
      <div class="fc-val">₹2,910</div>
      <span class="fc-badge" style="background:#FEF9C3;color:#854D0E">● HOLD  72%</span>
    </div>
    <div class="float-card">
      <div class="fc-ticker">INFOSYS</div>
      <div class="fc-val">₹1,560</div>
      <span class="fc-badge" style="background:#DCFCE7;color:#15803D">▲ BUY  81%</span>
    </div>"""
    return f"""
<div id="landing">
  <div>
    <div id="landing-title">AI That Thinks<br><span>Like an Investor</span></div>
    <p id="landing-sub">
      Analyze markets, track portfolios, and get intelligent insights
      with full transparency — powered by deterministic AI.
    </p>
    <div id="landing-btns">
      <button class="btn-primary" onclick="document.querySelector('[data-testid=tab-Analyze], button[id*=Analyze]')?.click()">
        🚀 Start Analysis
      </button>
      <button class="btn-outline" onclick="document.querySelector('[data-testid=tab-Markets], button[id*=Markets]')?.click()">
        📊 View Demo
      </button>
    </div>
  </div>
  <div id="card-stack">{float_cards}</div>
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
            items += '<div class="pulse-divider"></div>'
    return f"""
<div id="market-pulse">
  <span id="pulse-label">📡 Market Pulse</span>
  {items}
</div>"""


def _hero_stats_html() -> str:
    stats = [
        ("📡", "47",  "Signals detected today"),
        ("💡", "12",  "Portfolio insights generated"),
        ("🎯", "78%", "Average confidence score"),
    ]
    cards = "".join(f"""
    <div class="stat-card">
      <div class="stat-icon">{icon}</div>
      <div class="stat-val">{val}</div>
      <div class="stat-label">{label}</div>
    </div>""" for icon, val, label in stats)
    return f'<div class="stat-grid">{cards}</div>'


def _markets_html() -> str:
    # Index cards
    mkt_cards = "".join(f"""
    <div class="mkt-card">
      <div class="mkt-name">{m['index']}</div>
      <div class="mkt-val">{m['value']}</div>
      <div class="mkt-chg {'up' if m['up'] else 'down'}">
        {'▲' if m['up'] else '▼'} {m['change']}
      </div>
    </div>""" for m in MARKET_DATA)

    # Pick cards with confidence bar
    sig_cls = {"BUY": "badge-buy", "HOLD": "badge-hold", "SELL": "badge-sell"}
    pick_cards = "".join(f"""
    <div class="pick-card {'up-card' if p['up'] else 'down-card'}">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span class="pick-stock">{p['stock']}</span>
        <span class="badge {sig_cls[p['signal']]}">{p['signal']}</span>
      </div>
      <div class="pick-reason">{p['reason']}</div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:10px">
        <div class="pick-conf-bar" style="flex:1">
          <div class="pick-conf-fill" style="width:{p['conf']}%"></div>
        </div>
        <span style="font-size:.74rem;font-weight:700;color:#475569">{p['conf']}%</span>
      </div>
    </div>""" for p in TOP_PICKS)

    # News feed with color strip
    tag_color = {"AI Insight": "#6D28D9", "Alert": "#D97706", "Market": "#0369A1"}
    tag_badge = {"AI Insight": "badge-ai", "Alert": "badge-alert", "Market": "badge-mkt"}
    news_items = "".join(f"""
    <div class="news-card">
      <div class="news-strip" style="background:{tag_color.get(n['tag'],'#94A3B8')}"></div>
      <div class="news-body">
        <span class="badge {tag_badge.get(n['tag'],'badge-mkt')}" style="margin-bottom:5px;display:inline-block">
          {n['tag']}
        </span>
        <div class="news-headline">{n['headline']}</div>
      </div>
    </div>""" for n in NEWS_ITEMS)

    return f"""
{_market_pulse_html()}
{_hero_stats_html()}
<div class="sec-header">Market Overview</div>
<div class="mkt-grid">{mkt_cards}</div>
<div class="sec-header">Top Opportunities</div>
<div class="pick-grid">{pick_cards}</div>
<div class="sec-header">Latest Insights</div>
{news_items}"""


def _metric_chips(metrics: dict) -> str:
    labels = {"revenue": "Revenue (₹ Cr)", "profit": "Net Profit (₹ Cr)",
              "margin": "Margin %", "growth": "YoY Growth %"}
    chips = "".join(f"""
    <div class="metric-chip">
      <div class="mc-label">{label}</div>
      <div class="mc-val">{f"{metrics[k]:,.2f}" if metrics.get(k) is not None else "—"}</div>
    </div>""" for k, label in labels.items())
    return f'<div class="metric-row">{chips}</div>'


def _sentiment_badge(sentiment: dict) -> str:
    label = sentiment.get("sentiment", "neutral")
    score = sentiment.get("score", 0.5)
    pos   = sentiment.get("positive_signals", 0)
    neg   = sentiment.get("negative_signals", 0)
    cls   = {"positive": "badge-pos", "negative": "badge-neg"}.get(label, "badge-neu")
    icon  = {"positive": "▲", "negative": "▼"}.get(label, "●")
    bg    = {"positive": "#F0FDF4", "negative": "#FEF2F2"}.get(label, "#F8FAFC")
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
    pct   = conf.get("percentage", 0)
    label = conf.get("label", "Low")
    color = "#16A34A" if pct >= 80 else "#D97706" if pct >= 50 else "#E11D2E"
    factors = "".join(f"""
    <div style="display:flex;gap:8px;align-items:center;padding:5px 0;
                border-bottom:1px solid #F1F5F9;font-size:.79rem;color:#475569">
      <span>{"✅" if "✅" in f else "⚠️" if "⚠️" in f else "❌"}</span>
      <span>{f}</span>
    </div>""" for f in conf.get("factors", []))
    return f"""
<div class="card" style="display:flex;gap:24px;align-items:flex-start">
  <div style="text-align:center;min-width:88px">
    <div class="conf-big" style="color:{color}">{pct}%</div>
    <div class="conf-label">{label} Confidence</div>
    <div style="height:5px;border-radius:5px;background:#F1F5F9;margin-top:8px;overflow:hidden">
      <div style="height:100%;width:{pct}%;background:{color};border-radius:5px;
                  transition:width .6s ease"></div>
    </div>
  </div>
  <div style="flex:1">{factors}</div>
</div>"""


def _portfolio_impact_card(impact: dict) -> str:
    msg   = impact.get("note") or impact.get("impact_message", "No portfolio data.")
    sig   = impact.get("sentiment_signal", "neutral")
    cls   = {"positive": "badge-pos", "negative": "badge-neg"}.get(sig, "badge-neu")
    count = impact.get("positions_affected", 0)
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
    def _st(raw):
        l = raw.lower()
        if "error:" in l: return "error"
        if "done:"  in l: return "done"
        return "done"

    ICON  = {"done": "✅", "error": "❌"}
    COLOR = {"done": "#15803D", "error": "#B91C1C"}
    BG    = {"done": "#F0FDF4", "error": "#FEF2F2"}
    LBL   = {"done": "Completed", "error": "Failed"}

    seen, steps = set(), []
    for raw in trace:
        low = raw.lower()
        for token, label, desc in STEP_MAP:
            if token in low and token not in seen:
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
              <span style="font-size:.74rem;font-weight:700;color:#94A3B8">Step {i}</span>
              <span style="font-size:.7rem;font-weight:700;color:{COLOR[st]};
                           background:#fff;border:1px solid {COLOR[st]};
                           border-radius:20px;padding:1px 8px">{LBL[st]}</span>
            </div>
            <div style="font-size:.9rem;font-weight:700;color:#1E293B">{label}</div>
            <div style="font-size:.78rem;color:#64748B;margin-top:2px">{desc}</div>
          </div>
        </div>"""
    return items


def _portfolio_summary_html() -> str:
    holdings = pm.get_all_holdings("demo_user")
    total    = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div class="port-summary">
  <div>
    <div style="font-size:.7rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:.08em">
      Demo Portfolio
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#fff;margin-top:4px">₹{total:,.0f}</div>
    <div style="font-size:.75rem;color:#94A3B8;margin-top:4px">
      {len(holdings)} positions &nbsp;·&nbsp; Simulated for demonstration
    </div>
  </div>
  <span style="background:#FEF9C3;border:1px solid #FDE68A;border-radius:20px;
               padding:4px 12px;font-size:.7rem;font-weight:700;color:#92400E">
    Demo Mode
  </span>
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

# ── Backend handlers (unchanged logic) ───────────────────────────────────────

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

    result = agent.receive_task("answer_question", {
        "question": question.strip(),
        "user_id":  "demo_user",
    })

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
        port_html = f'<div class="card"><div class="sec-header">Demo Portfolio</div><p style="font-size:.72rem;color:#94A3B8;margin:0 0 8px">Sample Data — simulated for demonstration</p>{rows}</div>'

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
            f'padding:11px 16px;color:#15803D;font-size:.86rem;animation:fadeSlideUp .3s ease both">'
            f'✅ {stock.upper()} added to your demo portfolio.</div>',
            _portfolio_cards_html()
        )
    except Exception as e:
        return f'<div class="alert-box">⚠️ {e}</div>', _portfolio_cards_html()


# ── Gradio layout ─────────────────────────────────────────────────────────────

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

        # Loading overlay (shown via JS on analyze click)
        gr.HTML("""
        <div id="loading-overlay">
          <div style="text-align:center">
            <div style="font-size:1.1rem;font-weight:700;color:#1E293B;margin-bottom:12px">
              🤖 AI is analyzing your report...
            </div>
            <div class="loading-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
        <script>
          function showLoading()  { document.getElementById('loading-overlay').classList.add('active'); }
          function hideLoading()  { document.getElementById('loading-overlay').classList.remove('active'); }
        </script>
        """)

        gr.HTML(_topnav_html())
        gr.HTML(_landing_html())

        with gr.Tabs(elem_classes="tab-nav"):

            # ── 📊 Markets ────────────────────────────────────────────────────
            with gr.TabItem("📊 Markets"):
                gr.HTML(_markets_html())

            # ── 📄 Analyze ────────────────────────────────────────────────────
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

            # ── 💬 Insights ───────────────────────────────────────────────────
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

            # ── 📁 Portfolio ──────────────────────────────────────────────────
            with gr.TabItem("📁 Portfolio"):
                gr.HTML(_portfolio_summary_html())
                portfolio_display = gr.HTML(_portfolio_cards_html())

                gr.HTML('<div class="sec-header" style="margin-top:20px">Add / Update Position</div>')
                with gr.Row():
                    add_stock = gr.Textbox(label="Ticker",       placeholder="TCS",  scale=2)
                    add_qty   = gr.Textbox(label="Quantity",     placeholder="50",   scale=1)
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
