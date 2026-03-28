"""
TradeIQ - upgraded Gradio frontend
Landing-first responsive product UI with AI and language toggles.
"""

import os
import sys
from pathlib import Path
from html import escape
from typing import Any, Optional

import gradio as gr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent_core import InvestorAgent
from tools.market_news import fetch_market_news
from tools.portfolio_manager import PortfolioManager


agent = InvestorAgent()
pm = PortfolioManager()

DEMO_REPORT_CONTENT = """TATA CONSULTANCY SERVICES (TCS)
Q4 FY25 Financial Report

Revenue: Rs. 2,10,000 Cr
Net Profit: Rs. 42,000 Cr
Growth: 12%

Positive signals:
strong deal pipeline
cloud business acceleration
margin improvement

Risks:
global slowdown
wage inflation pressure

Outlook: Positive momentum expected
"""

I18N = {
    "en": {
        "app_name": "TradeIQ",
        "hero_title": "TradeIQ",
        "hero_sub": "Think Smarter. Trade Clearer. Invest Confidently.",
        "hero_tag": "Transparent. Reliable. Built for Indian investors",
        "start_demo": "Start Demo",
        "view_how": "View How It Works",
        "problem_solution": "Problem + Solution",
        "how_it_works": "How It Works",
        "cta": "Start Using Demo",
        "dashboard": "Dashboard",
        "market_cards": "Market Cards",
        "opportunities": "Opportunities",
        "insights": "Insights",
        "analyze": "Analyze",
        "portfolio": "Demo Portfolio",
        "demo_user": "Demo User: Rahul Sharma",
        "demo_note": "Sample portfolio for demo",
        "ai_label": "AI Mode: ON / OFF",
        "ai_enabled": "AI Enabled",
        "ai_disabled": "AI Disabled (Fast Mode)",
        "reason_title": "How this insight was generated",
        "ask": "Ask",
        "ask_placeholder": "Ask about your stock or market",
        "add_position": "Add Position",
        "back_home": "Back to Landing",
        "lang": "Language",
        "trace_title": "Agent Thought Process Flow",
        "top_news": "TOP NEWS",
        "refresh_news": "Refresh news",
        "live_strip": "LIVE",
        "market_pulse": "Market pulse",
        "breadth": "Advance / Decline (demo)",
        "signal_mix": "Signal mix (demo picks)",
        "how_blurb": "Each step below mirrors what the agent runs in order — upload a PDF in the demo to see the live trace.",
    },
    "hi": {
        "app_name": "इन्वेस्टरकोपायलट एआई",
        "hero_title": "इन्वेस्टरकोपायलट एआई",
        "hero_sub": "ऐसा AI जो निवेशक की तरह सोचता है, सिर्फ भविष्यवाणी नहीं करता",
        "hero_tag": "पारदर्शी। भरोसेमंद। भारतीय निवेशकों के लिए",
        "start_demo": "डेमो शुरू करें",
        "view_how": "कैसे काम करता है",
        "problem_solution": "समस्या + समाधान",
        "how_it_works": "यह कैसे काम करता है",
        "cta": "डेमो उपयोग शुरू करें",
        "dashboard": "डैशबोर्ड",
        "market_cards": "मार्केट कार्ड्स",
        "opportunities": "अवसर",
        "insights": "इनसाइट्स",
        "analyze": "विश्लेषण करें",
        "portfolio": "डेमो पोर्टफोलियो",
        "demo_user": "डेमो यूज़र: राहुल शर्मा",
        "demo_note": "डेमो के लिए सैंपल पोर्टफोलियो",
        "ai_label": "AI मोड: ON / OFF",
        "ai_enabled": "AI सक्षम",
        "ai_disabled": "AI बंद (फास्ट मोड)",
        "reason_title": "यह इनसाइट कैसे बनी",
        "ask": "पूछें",
        "ask_placeholder": "अपने स्टॉक या मार्केट के बारे में पूछें",
        "add_position": "पोजिशन जोड़ें",
        "back_home": "लैंडिंग पर वापस",
        "lang": "भाषा",
        "trace_title": "एजेंट विचार प्रक्रिया प्रवाह",
        "top_news": "टॉप न्यूज़",
        "refresh_news": "न्यूज़ रिफ्रेश",
        "live_strip": "लाइव",
        "market_pulse": "मार्केट पल्स",
        "breadth": "एडवांस / डिक्लाइन (डेमो)",
        "signal_mix": "सिग्नल मिक्स (डेमो पिक्स)",
        "how_blurb": "नीचे के चरण एजेंट के क्रम को दर्शाते हैं — लाइव ट्रेस के लिए डेमो में PDF अपलोड करें।",
    },
}

MARKET_DATA = [
    {"index": "NIFTY 50",   "value": 22450, "change": 0.43},
    {"index": "SENSEX",     "value": 73420, "change": 0.38},
    {"index": "BANK NIFTY", "value": 47210, "change": -0.12},
    {"index": "NIFTY IT",   "value": 35640, "change": 1.21},
]

TOP_PICKS = [
    {"stock": "TCS", "signal": "BUY", "conf": 87, "reason": "Strong earnings momentum"},
    {"stock": "INFOSYS", "signal": "BUY", "conf": 81, "reason": "Healthy deal pipeline"},
    {"stock": "RELIANCE", "signal": "HOLD", "conf": 72, "reason": "Balanced risk-reward"},
    {"stock": "HDFCBANK", "signal": "HOLD", "conf": 68, "reason": "Watch margin pressure"},
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* ── Design tokens ── */
:root {
  --red:      #E11D2E;
  --red-dark: #BE123C;
  --red-soft: #FCA5A5;
  --bg:       #FFF7F7;
  --bg-sec:   #F8FAFC;
  --card:     #FFFFFF;
  --text:     #0F172A;
  --muted:    #64748B;
  --border:   #E2E8F0;
  --green:    #16A34A;
  --neg:      #DC2626;
  --amber:    #D97706;
  --blue:     #2563EB;
  --shadow:   0 8px 24px rgba(15,23,42,.08);
  --radius:   16px;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Base ── */
body, .gradio-container {
  background: var(--bg) !important;
  font-family: 'Inter', 'Segoe UI', sans-serif !important;
  font-size: 16px;
  color: var(--text);
}
.gradio-container {
  max-width: 1200px !important;
  width: 100% !important;
  margin: 0 auto !important;
  padding: 0 24px 48px !important;
}
footer { display: none !important; }
.main, .wrap { max-width: 100% !important; padding: 0 !important; }

/* ── Keyframes ── */
@keyframes fadeUp   { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes floatY   { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
@keyframes pulseDot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.35;transform:scale(.8)} }
@keyframes bgBlob   { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(24px,-18px) scale(1.08)} }
@keyframes countUp  { from{opacity:0} to{opacity:1} }

.fade-page { animation: fadeUp .4s ease both; }

/* ── Sticky compact toolbar ── */
.control-strip {
  position: sticky; top: 0; z-index: 300;
  background: var(--card);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 2px 8px rgba(15,23,42,.06);
  height: 64px;
  display: flex; align-items: center; gap: 0;
  padding: 0;
  margin: 0 -24px 0;
  width: calc(100% + 48px);
}
/* Hide Gradio's invisible column wrappers, show only our HTML bar */
.control-strip > .gap > div:not(:has(#toolbar-bar)) { display: none !important; }
.control-strip > .gap { width: 100% !important; padding: 0 !important; margin: 0 !important; }
.control-strip .wrap,
.control-strip .block,
.control-strip .gr-form { background: transparent !important; box-shadow: none !important; border: none !important; }
.control-strip label { font-size: .72rem !important; font-weight: 700 !important; color: var(--muted) !important; }

/* Kill all Gradio internal spacing inside the toolbar */
.control-strip > div,
.control-strip .gap,
.control-strip .gr-padded,
.control-strip .gr-box,
.control-strip .container,
.control-strip fieldset,
.control-strip .form { padding: 0 !important; margin: 0 !important; gap: 0 !important; border: none !important; background: transparent !important; box-shadow: none !important; }

/* Radio group: inline, no extra height */
.control-strip .gr-radio-group,
.control-strip [data-testid="radio-group"],
.control-strip .radio-group { display: flex !important; align-items: center !important; gap: 6px !important; padding: 0 !important; margin: 0 !important; }
.control-strip input[type="radio"] { margin: 0 !important; }
.control-strip .gr-radio-row,
.control-strip .radio-row { display: flex !important; align-items: center !important; gap: 6px !important; padding: 0 !important; margin: 0 !important; flex-wrap: nowrap !important; }

/* Checkbox: inline, no card */
.control-strip input[type="checkbox"] { margin: 0 4px 0 0 !important; }
.control-strip .gr-checkbox-group,
.control-strip [data-testid="checkbox"] { display: flex !important; align-items: center !important; padding: 0 !important; margin: 0 !important; }
.ctrl-divider { width: 1px; height: 32px; background: var(--border); margin: 0 16px; flex-shrink: 0; }
.ctrl-label   { font-size: .7rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .07em; white-space: nowrap; margin-right: 8px; }
.ctrl-chip-green {
  display: inline-flex; align-items: center; gap: 5px;
  background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 999px;
  padding: 4px 12px; font-size: .72rem; font-weight: 700; color: var(--green); white-space: nowrap;
}
.ctrl-chip-green::before { content:"●"; font-size:.52rem; animation: pulseDot 1.8s infinite; }
.ctrl-chip-user {
  display: inline-flex; align-items: center; gap: 5px;
  background: #FEF9C3; border: 1px solid #FDE68A; border-radius: 999px;
  padding: 4px 12px; font-size: .72rem; font-weight: 700; color: #92400E; white-space: nowrap;
}

/* ── Toolbar column layout ── */
.tb-col {
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 8px !important;
  min-width: 0 !important;
  gap: 4px !important;
}
.tb-col > div, .tb-col .wrap, .tb-col .block, .tb-col fieldset, .tb-col .form {
  background: transparent !important; box-shadow: none !important;
  border: none !important; padding: 0 !important; margin: 0 !important;
  width: 100% !important;
}
/* Radio styled as pill buttons */
.tb-radio .wrap { display: flex !important; flex-direction: row !important; gap: 4px !important; padding: 0 !important; }
.tb-radio label {
  display: inline-flex !important; align-items: center !important;
  border: 1.5px solid var(--border) !important; background: #fff !important;
  color: var(--muted) !important; border-radius: 999px !important;
  padding: 3px 14px !important; font-size: .78rem !important; font-weight: 600 !important;
  cursor: pointer !important; transition: all .15s !important; white-space: nowrap !important;
}
.tb-radio label:has(input:checked) { background: var(--red) !important; color: #fff !important; border-color: var(--red) !important; }
.tb-radio label:hover:not(:has(input:checked)) { border-color: var(--red-soft) !important; color: var(--red) !important; }
.tb-radio input[type="radio"] { display: none !important; }
/* Checkbox styled as toggle */
.tb-check .wrap { display: flex !important; align-items: center !important; gap: 8px !important; padding: 0 !important; }
.tb-check input[type="checkbox"] {
  appearance: none !important; -webkit-appearance: none !important;
  width: 36px !important; height: 20px !important; border-radius: 999px !important;
  background: #CBD5E1 !important; position: relative !important;
  cursor: pointer !important; transition: background .2s !important;
  flex-shrink: 0 !important; border: none !important; outline: none !important;
}
.tb-check input[type="checkbox"]::after {
  content: "" !important; position: absolute !important; top: 2px !important; left: 2px !important;
  width: 16px !important; height: 16px !important; border-radius: 50% !important;
  background: #fff !important; transition: transform .2s !important;
  box-shadow: 0 1px 3px rgba(0,0,0,.2) !important;
}
.tb-check input[type="checkbox"]:checked { background: var(--green) !important; }
.tb-check input[type="checkbox"]:checked::after { transform: translateX(16px) !important; }
.tb-check label { font-size: .78rem !important; font-weight: 700 !important; color: var(--text) !important; cursor: pointer !important; background: transparent !important; border: none !important; padding: 0 !important; }

/* ── Pure HTML toolbar bar ── */
#toolbar-bar {
  display: flex;
  align-items: center;
  width: 100%;
  height: 64px;
  padding: 0 8px;
}
.tb-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 0;
}
.tb-divider {
  width: 1px; height: 32px; background: var(--border); flex-shrink: 0; margin: 0 4px;
}
.tb-label {
  font-size: .7rem; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .07em; white-space: nowrap;
}
.tb-radio-wrap { display: flex; gap: 4px; }
.tb-radio-btn {
  border: 1.5px solid var(--border); background: #fff; color: var(--muted);
  border-radius: 999px; padding: 3px 12px; font-size: .75rem; font-weight: 600;
  cursor: pointer; transition: all .15s;
}
.tb-radio-btn.active {
  background: var(--red); color: #fff; border-color: var(--red);
}
.tb-radio-btn:hover:not(.active) { border-color: var(--red-soft); color: var(--red); }
/* Toggle switch */
.tb-toggle { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.tb-toggle input { display: none; }
.tb-toggle-track {
  width: 36px; height: 20px; background: #16A34A; border-radius: 999px;
  position: relative; transition: background .2s; flex-shrink: 0;
  display: inline-block; cursor: pointer;
}
.tb-toggle-thumb {
  position: absolute; top: 2px; left: 2px;
  width: 16px; height: 16px; border-radius: 50%; background: #fff;
  transition: transform .2s; box-shadow: 0 1px 3px rgba(0,0,0,.2);
  transform: translateX(16px);
}
.tb-toggle-label { font-size: .78rem; font-weight: 700; color: var(--text); min-width: 24px; }

/* ── Topbar ── */
.topbar {
  background: var(--card);
  border-bottom: 3px solid var(--red);
  border-radius: 0 0 var(--radius) var(--radius);
  padding: 14px 24px;
  display: flex; align-items: center; justify-content: space-between;
  margin: 0 -24px 24px;
  box-shadow: var(--shadow);
}
.topbar-right { display: flex; align-items: center; gap: 12px; }
.brand { font-size: 1.15rem; font-weight: 900; color: var(--red); letter-spacing: -.02em; }
.demo-meta { font-size: .75rem; color: var(--muted); font-weight: 600; }
.pill { font-size: .72rem; font-weight: 700; padding: 4px 12px; border-radius: 999px; background: #FEE2E2; color: #991B1B; }
.topbar-nav-btn {
  border: none; background: transparent; font-size: .82rem; font-weight: 600;
  color: var(--muted); cursor: pointer; padding: 6px 14px; border-radius: 8px;
  transition: background .15s, color .15s;
}
.topbar-nav-btn:hover { background: #F1F5F9; color: var(--text); }

/* ── Hero ── */
.hero {
  position: relative; overflow: hidden;
  display: grid; grid-template-columns: 1.2fr 1fr; gap: 32px;
  background: var(--red);
  border-radius: var(--radius);
  padding: 52px 44px;
  box-shadow: 0 16px 48px rgba(225,29,46,.32);
  min-height: 340px;
  margin-bottom: 40px;
}
/* Animated bg blobs */
.hero::before {
  content: ""; position: absolute;
  width: 360px; height: 360px; border-radius: 50%;
  background: rgba(255,255,255,.08);
  top: -100px; right: -80px;
  animation: bgBlob 9s ease-in-out infinite;
  pointer-events: none;
}
.hero::after {
  content: ""; position: absolute;
  width: 220px; height: 220px; border-radius: 50%;
  background: rgba(255,255,255,.06);
  bottom: -60px; right: 140px;
  animation: bgBlob 12s ease-in-out infinite reverse;
  pointer-events: none;
}
.hero h1 {
  font-size: 3rem; font-weight: 900; color: #fff;
  line-height: 1.1; letter-spacing: -.03em; margin-bottom: 14px;
}
.hero p { margin: 8px 0; color: rgba(255,255,255,.85); font-size: 1.05rem; line-height: 1.65; }
.hero .kicker { color: rgba(255,255,255,.72); font-size: .88rem; }
.hero-hackathon {
  display: inline-block; margin-top: 12px;
  background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.3);
  border-radius: 999px; padding: 4px 16px;
  font-size: .75rem; font-weight: 700; color: #fff; letter-spacing: .05em;
}
.hero-btns { display: flex; gap: 12px; margin-top: 28px; flex-wrap: wrap; }
.hero-btn-primary {
  height: 52px; padding: 0 28px; border-radius: 14px;
  background: #fff; color: var(--red); border: none;
  font-size: .95rem; font-weight: 700; cursor: pointer;
  box-shadow: 0 4px 16px rgba(0,0,0,.22);
  transition: transform .2s, box-shadow .2s;
}
.hero-btn-primary:hover { transform: translateY(-2px) scale(1.02); box-shadow: 0 8px 24px rgba(0,0,0,.28); }
.hero-btn-secondary {
  height: 52px; padding: 0 24px; border-radius: 14px;
  background: transparent; color: #fff;
  border: 2px solid rgba(255,255,255,.55);
  font-size: .95rem; font-weight: 600; cursor: pointer;
  transition: background .2s, transform .2s;
}
.hero-btn-secondary:hover { background: rgba(255,255,255,.14); transform: translateY(-2px); }

/* Float cards */
.float-area { position: relative; min-height: 240px; }
.float-card {
  position: absolute; width: 210px; border-radius: 14px; padding: 16px;
  background: #fff; box-shadow: 0 12px 32px rgba(15,23,42,.18);
  animation: floatY 4s ease-in-out infinite;
}
.float-card:nth-child(1) { top: 0;    left: 0;   }
.float-card:nth-child(2) { top: 75px; left: 80px; animation-delay: .9s; }
.float-card:nth-child(3) { top: 150px; left: 16px; animation-delay: 1.8s; }
.float-card .kicker { font-size: .68rem; font-weight: 800; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }

/* ── Sections ── */
.section { margin-top: 40px; }
.section-title { font-size: 2rem; font-weight: 800; color: var(--text); margin-bottom: 6px; letter-spacing: -.02em; }
.section-sub   { font-size: 1rem; color: var(--muted); margin-bottom: 24px; line-height: 1.55; }

/* ── Cards ── */
.card {
  background: var(--card); border-radius: var(--radius);
  padding: 20px; border: 1px solid var(--border);
  box-shadow: var(--shadow);
  transition: all .25s ease;
}
.card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(15,23,42,.12); }

/* ── Problem cards ── */
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px,1fr)); gap: 16px; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px,1fr)); gap: 16px; }
.problem-card {
  background: var(--card); border-radius: var(--radius); padding: 24px;
  border: 1px solid var(--border); border-top: 4px solid var(--red);
  box-shadow: var(--shadow); transition: all .25s ease;
}
.problem-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(15,23,42,.12); }
.problem-card h4 { font-size: 1.1rem; font-weight: 700; color: var(--text); margin: 10px 0 6px; }
.problem-card .body { font-size: .88rem; color: var(--muted); line-height: 1.55; margin-bottom: 12px; }
.problem-highlight {
  background: #FEF2F2; border-left: 3px solid var(--red);
  border-radius: 0 8px 8px 0; padding: 8px 12px;
  font-size: .82rem; color: #B91C1C; font-weight: 600; line-height: 1.45;
}

/* ── Flow ── */
.flow { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; }
.flow-card {
  background: var(--card); border-radius: var(--radius); padding: 20px 14px;
  border: 1px solid var(--border); box-shadow: var(--shadow);
  text-align: center; transition: all .25s ease;
}
.flow-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(15,23,42,.12); }
.flow-card b { font-size: .95rem; font-weight: 700; color: var(--text); display: block; margin-top: 8px; }
.flow-card .flow-desc { font-size: .75rem; color: var(--muted); margin-top: 4px; line-height: 1.4; }

/* ── CTA strip ── */
.cta-strip {
  background: var(--red); border-radius: var(--radius);
  padding: 44px 36px; text-align: center;
  box-shadow: 0 12px 40px rgba(225,29,46,.28);
}

/* ── Dashboard ── */
.dash-shell {
  background: var(--card); border-radius: var(--radius);
  padding: 24px; border: 1px solid var(--border); box-shadow: var(--shadow);
}
.dash-title { font-size: 1.4rem; font-weight: 800; color: var(--text); margin: 0 0 4px; }
.dash-sub   { font-size: .88rem; color: var(--muted); margin: 0 0 16px; }

/* ── Icon wraps ── */
.icon-wrap {
  width: 40px; height: 40px; border-radius: 12px;
  display: inline-flex; align-items: center; justify-content: center;
  margin-bottom: 10px; flex-shrink: 0;
}
.icon-red   { background: #FEE2E2; color: #B91C1C; }
.icon-blue  { background: #DBEAFE; color: #1D4ED8; }
.icon-green { background: #DCFCE7; color: #166534; }
.icon-amber { background: #FEF3C7; color: #92400E; }
.icon { width: 20px; height: 20px; }

/* ── Badges ── */
.badge { display: inline-block; border-radius: 999px; padding: 4px 12px; font-size: .72rem; font-weight: 700; }
.badge-buy  { background: #DCFCE7; color: #166534; }
.badge-hold { background: #FEF3C7; color: #92400E; }
.badge-sell { background: #FEE2E2; color: #B91C1C; }

/* ── Kicker / val ── */
.kicker { font-size: .78rem; color: var(--muted); line-height: 1.5; }
.val    { font-size: 1.5rem; font-weight: 800; color: var(--red); }

/* ── Reasoning steps ── */
.reason-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border);
}
.reason-title { font-size: 1.1rem; font-weight: 800; color: var(--text); }
.reason-sub   { font-size: .78rem; color: var(--muted); margin-top: 2px; }
.reason-conf-badge {
  background: #DCFCE7; color: #166534; border-radius: 999px;
  padding: 5px 14px; font-size: .78rem; font-weight: 700; white-space: nowrap;
}
.reason-step {
  display: flex; gap: 12px; align-items: flex-start;
  background: var(--card); border-left: 4px solid var(--red);
  border-radius: 0 10px 10px 0; padding: 12px 14px; margin-bottom: 10px;
  box-shadow: 0 2px 8px rgba(15,23,42,.05);
  transition: transform .2s;
}
.reason-step:hover { transform: translateX(3px); }
.reason-step b { font-size: .9rem; font-weight: 700; color: var(--text); }

/* ── ET app bar ── */
.et-app-bar {
  background: var(--red); color: #fff; border-radius: var(--radius);
  padding: 14px 20px; display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; box-shadow: 0 8px 24px rgba(225,29,46,.28);
}
.et-app-bar .et-title { font-size: 1.1rem; font-weight: 900; letter-spacing: -.02em; }
.et-app-bar .et-sub   { font-size: .72rem; opacity: .85; font-weight: 600; }
.live-dot {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: .72rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em;
}
.live-dot::before {
  content: ""; width: 8px; height: 8px; border-radius: 50%; background: #fff;
  animation: pulseDot 1.2s ease-in-out infinite;
}

/* ── Index grid ── */
.index-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; }
.index-card {
  background: var(--card); border-radius: var(--radius);
  border: 1px solid var(--border); border-left: 4px solid var(--red);
  padding: 14px 16px; box-shadow: var(--shadow);
  transition: all .25s ease;
}
.index-card:hover { transform: translateY(-3px); box-shadow: 0 12px 28px rgba(15,23,42,.12); }
.index-card .nm { font-size: .68rem; font-weight: 800; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.index-card .pv { font-size: 1.4rem; font-weight: 900; color: var(--text); margin: 4px 0 2px; }
.index-card .ch { font-size: .8rem; font-weight: 800; }

/* ── News ── */
.news-section-head { display: flex; align-items: baseline; justify-content: space-between; margin: 12px 0; }
.news-section-head .big { font-size: 1.1rem; font-weight: 900; color: var(--text); }
.news-scroll { display: flex; gap: 14px; overflow-x: auto; padding-bottom: 8px; scroll-snap-type: x mandatory; }
.news-card {
  min-width: 280px; max-width: 320px; flex-shrink: 0; scroll-snap-align: start;
  background: var(--card); border-radius: var(--radius);
  padding: 14px 16px; border: 1px solid var(--border); box-shadow: var(--shadow);
  transition: all .25s ease; position: relative;
}
.news-card:hover { transform: translateY(-4px); box-shadow: 0 16px 36px rgba(15,23,42,.14); }
.news-card .live-tag {
  display: inline-block; font-size: .62rem; font-weight: 800;
  color: var(--red); background: #FFF1F2; border: 1px solid #FECDD3;
  padding: 2px 8px; border-radius: 4px; margin-bottom: 8px;
}
.news-card .ts-chip {
  position: absolute; top: 12px; right: 12px;
  background: #FEF2F2; color: var(--red);
  padding: 3px 9px; font-size: .68rem; font-weight: 700; border-radius: 999px;
}
.news-card .headline { font-size: .95rem; font-weight: 800; color: var(--text); line-height: 1.35; margin: 0 0 8px; }
.news-card .src { font-size: .68rem; color: var(--muted); font-weight: 600; }
.news-card a { font-size: .72rem; font-weight: 700; color: var(--red); text-decoration: none; }

/* ── Opportunities ── */
.pick-rich { display: grid; grid-template-columns: 1fr 120px; gap: 12px; align-items: stretch; }
.pick-rich .main { min-width: 0; }
.pick-rich .side {
  background: linear-gradient(180deg,#ECFEFF,#F0F9FF); border-radius: 10px;
  padding: 10px; border: 1px solid #BAE6FD; text-align: center;
}
.pick-rich .side .lbl { font-size: .62rem; color: #0369A1; font-weight: 700; text-transform: uppercase; }
.pick-rich .side .big { font-size: 1.15rem; font-weight: 900; color: var(--text); }
.sentiment-bar { display: flex; height: 8px; border-radius: 999px; overflow: hidden; margin-top: 8px; }
.sentiment-bar .seg-sell { background: var(--red); }
.sentiment-bar .seg-hold { background: #FBBF24; }
.sentiment-bar .seg-buy  { background: var(--green); }

/* ── Breadth ── */
.breadth-wrap { margin-top: 14px; background: var(--card); border-radius: 12px; padding: 12px 14px; border: 1px solid var(--border); }
.breadth-wrap .lbl { font-size: .72rem; font-weight: 800; color: var(--muted); margin-bottom: 6px; }
.breadth-bar { display: flex; height: 10px; border-radius: 999px; overflow: hidden; }
.breadth-bar .adv { background: var(--green); }
.breadth-bar .dec { background: var(--red); }
.breadth-meta { display: flex; justify-content: space-between; font-size: .68rem; color: var(--muted); margin-top: 4px; font-weight: 600; }

/* ── Analyze ── */
.analysis-grid { display: grid; grid-template-columns: minmax(280px,360px) 1fr; gap: 16px; }
.input-panel {
  background: var(--card); border: 2px dashed #CBD5E1;
  border-radius: var(--radius); padding: 16px;
}
.output-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 12px; }
.demo-report-btn {
  width: 100%; margin-bottom: 12px; padding: 10px;
  background: var(--red); color: #fff; border: none;
  border-radius: 10px; font-size: .88rem; font-weight: 700;
  cursor: pointer; transition: background .2s, transform .2s;
}
.demo-report-btn:hover { background: var(--red-dark); transform: scale(1.02); }

/* ── Buttons ── */
.btn-primary {
  background: var(--red) !important; color: #fff !important;
  border: none !important; border-radius: 10px !important; font-weight: 700 !important;
  box-shadow: 0 4px 12px rgba(225,29,46,.28) !important;
  transition: all .2s ease !important;
}
.btn-primary:hover { background: var(--red-dark) !important; transform: scale(1.02) !important; box-shadow: 0 6px 18px rgba(225,29,46,.38) !important; }
.btn-secondary {
  background: #fff !important; color: var(--red) !important;
  border: 1.5px solid var(--red) !important; border-radius: 10px !important; font-weight: 700 !important;
  transition: all .2s ease !important;
}
.btn-secondary:hover { transform: scale(1.02) !important; background: #FEF2F2 !important; }
.btn-light-cta {
  background: var(--red) !important; color: #fff !important;
  border: none !important; border-radius: 10px !important; font-weight: 800 !important;
  box-shadow: 0 4px 12px rgba(225,29,46,.28) !important;
  transition: all .2s ease !important;
}
.btn-light-cta:hover { background: var(--red-dark) !important; transform: scale(1.02) !important; }
.btn-chip {
  border-radius: 999px !important; border: 1px solid #FECACA !important;
  background: #FFF1F2 !important; color: #BE123C !important; font-weight: 700 !important;
}

/* ── Tabs ── */
.tabs { background: transparent !important; }
.tabs button {
  border: 1.5px solid var(--border) !important; border-radius: 999px !important;
  padding: 8px 18px !important; font-weight: 700 !important;
  background: #fff !important; color: var(--muted) !important;
  transition: all .2s ease !important;
}
.tabs button:hover { border-color: var(--red-soft) !important; color: var(--red-dark) !important; }
.tabs button[aria-selected="true"] {
  background: var(--red) !important; color: #fff !important;
  border-color: var(--red) !important; box-shadow: 0 6px 16px rgba(225,29,46,.28) !important;
}
.how-focus { outline: 3px solid var(--red) !important; box-shadow: 0 0 0 8px rgba(225,29,46,.15) !important; border-radius: var(--radius); }

/* ── Vertical spacing ── */
.gradio-container > * + * { margin-top: 0; }
.dash-shell > * + * { margin-top: 20px; }
.card + .card { margin-top: 14px; }
.section { margin-top: 40px; }
.tabs { margin-top: 20px !important; }
.tabs > div { padding-top: 20px !important; }
/* Space between tab content sections */
.tab-content-gap > * + * { margin-top: 16px; }
/* Input fields */
.gradio-container input, .gradio-container textarea {
  margin-bottom: 10px !important;
}
/* Buttons */
.gradio-container button { margin-top: 8px !important; }
/* Rows inside dashboard */
.dash-shell .gr-row + .gr-row { margin-top: 16px !important; }
/* Section titles */
.section-title { margin-bottom: 8px !important; }
.dash-title { margin-bottom: 4px !important; }
.dash-sub   { margin-bottom: 20px !important; }
/* Cards inside output areas */
.output-grid .card { margin-bottom: 0; }
/* Analyze tab spacing */
.analysis-grid { margin-top: 16px; }
.input-panel > * + * { margin-top: 12px !important; }
/* Insights tab */
.gradio-container .tabitem > * + * { margin-top: 14px; }

/* ── Responsive ── */
@media (max-width: 980px) {
  .hero { grid-template-columns: 1fr; padding: 36px 28px; }
  .hero h1 { font-size: 2.2rem; }
  .flow { grid-template-columns: repeat(3,1fr); }
  .analysis-grid { grid-template-columns: 1fr; }
  .index-grid { grid-template-columns: repeat(2,1fr); }
  .pick-rich { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .gradio-container { padding: 0 12px 32px !important; }
  .control-strip { margin: 0 -12px 0; padding: 0 12px; height: auto; min-height: 64px; flex-wrap: wrap; gap: 8px; padding: 10px 12px; }
  .topbar { margin: 0 -12px 16px; padding: 12px; }
  .hero { padding: 28px 18px; }
  .hero h1 { font-size: 1.8rem; }
  .grid-4, .grid-2, .flow, .index-grid { grid-template-columns: 1fr; }
  .float-area { min-height: 0; }
  .float-card { position: relative; width: 100%; top: auto; left: auto; margin-bottom: 10px; animation: none; }
  .topbar { flex-direction: column; align-items: flex-start; gap: 8px; }
  .topbar-right { width: 100%; justify-content: space-between; }
  .output-grid { grid-template-columns: 1fr; }
}
"""




def tr(lang: str, key: str) -> str:
    return I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))


def lucide(path_data: str) -> str:
    return (
        "<svg class='icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
        "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        f"{path_data}</svg>"
    )


HOW_SCROLL_JS = r"""
() => {
  const run = () => {
    const el = document.getElementById("how-works-section");
    if (!el) return;
    el.scrollIntoView({behavior: "smooth", block: "center"});
    el.classList.add("how-focus");
    window.setTimeout(() => el.classList.remove("how-focus"), 2200);
  };
  run();
  window.setTimeout(run, 350);
  window.setTimeout(run, 800);
}
"""


def sparkline_svg(positive: bool) -> str:
    if positive:
        path_d = "M0,78 L12,72 L24,68 L40,52 L52,44 L68,32 L82,24 L100,14"
    else:
        path_d = "M0,18 L14,28 L28,36 L44,48 L58,58 L72,66 L86,72 L100,78"
    stroke = "#16A34A" if positive else "#E11D2E"
    return (
        f"<svg viewBox='0 0 100 88' width='100%' height='72' preserveAspectRatio='none' style='display:block'>"
        f"<defs><linearGradient id='sg' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0%' stop-color='{stroke}' stop-opacity='0.35'/>"
        f"<stop offset='100%' stop-color='{stroke}' stop-opacity='0'/></linearGradient></defs>"
        f"<path d='{path_d} V88 H0 Z' fill='url(#sg)'/>"
        f"<path d='{path_d}' fill='none' stroke='{stroke}' stroke-width='2.2'/></svg>"
    )


def _breadth_from_market() -> tuple[int, int]:
    ups = sum(1 for m in MARKET_DATA if m["change"] >= 0)
    downs = len(MARKET_DATA) - ups
    adv = max(35, min(75, 50 + ups * 8 - downs * 5))
    return adv, 100 - adv


def markets_dashboard_html(lang: str) -> str:
    adv, dec = _breadth_from_market()
    cards = []
    for item in MARKET_DATA:
        up = item["change"] >= 0
        clr = "#16A34A" if up else "#E11D2E"
        sign = "+" if up else ""
        cards.append(
            "<div class='index-card'>"
            f"<div class='nm'>{escape(item['index'])}</div>"
            f"<div class='pv count' data-count='{int(item['value'])}'>0</div>"
            f"<div class='ch' style='color:{clr}'>{sign}{item['change']}%</div>"
            f"{sparkline_svg(up)}"
            "</div>"
        )
    return (
        "<div>"
        f"<div class='et-app-bar'><div><div class='et-title'>{escape(tr(lang, 'market_pulse'))}</div>"
        f"<div class='et-sub'>{escape(tr(lang, 'demo_note'))}</div></div>"
        f"<div class='live-dot'>{escape(tr(lang, 'live_strip'))}</div></div>"
        f"<div class='index-grid'>{''.join(cards)}</div>"
        "<div class='breadth-wrap'>"
        f"<div class='lbl'>{escape(tr(lang, 'breadth'))}</div>"
        "<div class='breadth-bar'>"
        f"<div class='adv' style='width:{adv}%'></div>"
        f"<div class='dec' style='width:{dec}%'></div>"
        "</div>"
        f"<div class='breadth-meta'><span>Adv {adv}%</span><span>Decl {dec}%</span></div>"
        "</div>"
        "</div>"
    )


def news_carousel_html(lang: str, items: Optional[list[Any]] = None) -> str:
    rows = items if items is not None else fetch_market_news(12)
    cards = []
    timestamps = ["2 min ago","5 min ago","11 min ago","18 min ago",
                  "24 min ago","31 min ago","42 min ago","55 min ago",
                  "1 hr ago","1 hr ago","2 hr ago","3 hr ago"]
    for i, row in enumerate(rows):
        title = escape(row.get("title", ""))
        src_name = escape(str(row.get("source", "")))
        link = escape(str(row.get("link", "#")))
        ts = timestamps[i % len(timestamps)]
        cards.append(
            "<div class='news-card'>"
            f"<span class='ts-chip'>{ts}</span>"
            f"<span class='live-tag'>{escape(tr(lang, 'live_strip'))} · MARKET</span>"
            f"<p class='headline'>{title}</p>"
            f"<div class='src'>{src_name}</div>"
            f"<div style='margin-top:6px'><a href='{link}' target='_blank' rel='noopener noreferrer'>Read →</a></div>"
            "</div>"
        )
    inner = "".join(cards) if cards else "<div class='news-card'><p class='headline'>No headlines available.</p></div>"
    return (
        "<div>"
        f"<div class='news-section-head'><span class='big'>{escape(tr(lang, 'top_news'))}</span></div>"
        f"<div class='news-scroll'>{inner}</div>"
        "</div>"
    )


def opportunities_rich_html(lang: str) -> str:
    blocks = []
    buys = sum(1 for p in TOP_PICKS if p["signal"] == "BUY")
    holds = len(TOP_PICKS) - buys
    for item in TOP_PICKS:
        up = item["signal"] == "BUY"
        bcls = "badge-buy" if up else "badge-hold"
        upside = min(4.5, item["conf"] / 22.0)
        blocks.append(
            "<div class='card pick-rich'>"
            "<div class='main'>"
            "<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<span style='font-size:1.1rem;font-weight:900'>{escape(item['stock'])}</span>"
            f"<span class='badge {bcls}'>{escape(item['signal'])}</span>"
            "</div>"
            f"<div class='kicker' style='margin-top:6px;font-size:.8rem'>{escape(item['reason'])}</div>"
            "<div class='sentiment-bar' style='display:flex;height:8px'>"
            f"<span class='seg-sell' style='flex:{max(1, 4 - buys)}'></span>"
            f"<span class='seg-hold' style='flex:{max(1, holds * 2)}'></span>"
            f"<span class='seg-buy' style='flex:{max(1, buys * 3)}'></span>"
            "</div>"
            f"<div class='kicker' style='margin-top:4px'>{escape(tr(lang, 'signal_mix'))}</div>"
            "</div>"
            "<div class='side'>"
            "<div class='lbl'>Conf</div>"
            f"<div class='big'>{item['conf']}%</div>"
            "<div class='lbl' style='margin-top:6px'>Upside</div>"
            f"<div class='big' style='color:#16a34a'>+{upside:.1f}%</div>"
            "</div>"
            "</div>"
        )
    return "<div class='grid-2'>" + "".join(blocks) + "</div>"


def generate_demo_pdf() -> str:
    project_root = Path(__file__).resolve().parents[1]
    txt_path = project_root / "demo_report.txt"
    txt_path.write_text(DEMO_REPORT_CONTENT, encoding="utf-8")

    pdf_path = project_root / "demo_report.pdf"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        y = 800
        for line in DEMO_REPORT_CONTENT.strip().splitlines():
            c.drawString(72, y, line)
            y -= 22
        c.save()
        return str(pdf_path)
    except Exception:
        return str(txt_path)


def topbar_html(lang: str) -> str:
    holdings = pm.get_all_holdings("demo_user")
    total = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return (
        "<div class='topbar'>"
        f"<div><div class='brand'>{tr(lang, 'app_name')}</div><div class='demo-meta'>{tr(lang, 'demo_note')}</div></div>"
        "<div class='topbar-right'>"
        f"<div class='demo-meta'>Portfolio Value: Rs. {total:,.0f}</div>"
        f"<div class='pill'>{tr(lang, 'demo_user')}</div>"
        "</div>"
        "</div>"
    )


def landing_html(lang: str) -> str:
    card_1 = (
        "<div class='float-card'>"
        "<div class='kicker'>TCS</div><div><b>BUY</b> - 87%</div>"
        "</div>"
    )
    card_2 = (
        "<div class='float-card'>"
        "<div class='kicker'>INFOSYS</div><div><b>BUY</b> - 81%</div>"
        "</div>"
    )
    card_3 = (
        "<div class='float-card'>"
        "<div class='kicker'>HDFCBANK</div><div><b>HOLD</b> - 68%</div>"
        "</div>"
    )

    problem_cards = [
        (
            "icon-red",
            lucide("<path d='M12 2v20'/><path d='M2 12h20'/>"),
            "AI Accuracy Problem",
            "AI ~60% prediction -> We aim 80-85% using structured reasoning",
        ),
        (
            "icon-blue",
            lucide("<path d='M12 8v4'/><path d='M12 16h.01'/><path d='M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/>"),
            "Blind Trust Issue",
            "AI alone is risky -> We add confidence + explanation",
        ),
        (
            "icon-green",
            lucide("<path d='M2 12h20'/><path d='M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z'/>"),
            "Accessibility Gap",
            "Add vernacular support (Hindi, basic multi-language UI toggle)",
        ),
        (
            "icon-amber",
            lucide("<path d='M7 20h10'/><path d='M10 20c5.5-2.5.8-6.4 3-10'/><path d='M9.5 9.4c1.5 1.8 4.3 2.8 5.8 2.2'/>"),
            "Sustainability",
            "Reduce AI usage via deterministic logic",
        ),
    ]
    problem_html = "".join(
        [
            f"<div class='card'><span class='icon-wrap {klass}'>{icn}</span><h4>{title}</h4><div class='kicker'>{desc}</div></div>"
            for klass, icn, title, desc in problem_cards
        ]
    )

    flow = [
        ("User", "icon-blue", lucide("<path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/>")),
        ("Agent", "icon-red", lucide("<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M9 9h6v6H9z'/>")),
        ("Tools", "icon-green", lucide("<path d='M12 1v22'/><path d='M5 5l14 14'/><path d='M19 5 5 19'/>")),
        ("Output", "icon-amber", lucide("<path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4'/><polyline points='17 3 21 3 21 7'/><line x1='10' y1='14' x2='21' y2='3'/>")),
        ("Confidence", "icon-red", lucide("<path d='M12 2l7 4v6c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6l7-4z'/>")),
    ]
    flow_html = "".join(
        [
            f"<div class='card'><span class='icon-wrap {klass}'>{icn}</span><b>{label}</b></div>"
            for label, klass, icn in flow
        ]
    )

    return f"""
<div class='fade-page'>
  <div class='hero'>
    <div>
      <h1>{tr(lang, 'hero_title')}</h1>
      <p>{tr(lang, 'hero_sub')}</p>
      <p class='kicker'>{tr(lang, 'hero_tag')}</p>
      <div class='hero-hackathon'>🏆 Built for ET Hackathon 2026</div>
    </div>
    <div class='float-area'>
      {card_1}{card_2}{card_3}
    </div>
  </div>

  <div class='section'>
    <div class='section-title'>{tr(lang, 'problem_solution')}</div>
    <div class='grid-4'>{problem_html}</div>
  </div>

  <div class='section' id='how-works-section'>
    <div class='section-title' style='font-size:1.55rem;font-weight:900;color:#0f172a'>{tr(lang, 'how_it_works')}</div>
    <p style='font-size:.9rem;color:#475569;margin:0 0 14px;line-height:1.55;max-width:52rem'>{tr(lang, 'how_blurb')}</p>
    <div class='flow'>{flow_html}</div>
  </div>

  <div class='section'>
    <div class='cta-strip'>
      <div style='font-size:1.8rem;font-weight:900;color:#fff;margin-bottom:10px'>Ready to see it in action?</div>
      <div style='font-size:1rem;color:rgba(255,255,255,.8);margin-bottom:24px'>Upload a real PDF and watch the agent reason through it — step by step.</div>
      <button class='hero-btn-primary' onclick="document.getElementById('start-demo-btn')?.click()" style='font-size:1rem;padding:0 36px'>🚀 {tr(lang, 'cta')}</button>
    </div>
  </div>
</div>
"""


def reasoning_html(lang: str) -> str:
    steps = [
        ("Extracted data", lucide("<path d='M4 4h16v16H4z'/><path d='M8 8h8M8 12h8M8 16h6'/>"), "Read report content and extracted relevant text."),
        ("Found metrics", lucide("<path d='M3 3v18h18'/><path d='M7 14l4-4 3 3 5-6'/>"), "Mapped revenue, profit, growth and margin metrics."),
        ("Analyzed sentiment", lucide("<circle cx='12' cy='12' r='9'/><path d='M8 15s1.5 2 4 2 4-2 4-2'/><circle cx='9' cy='9' r='1'/><circle cx='15' cy='9' r='1'/>"), "Evaluated positive and negative linguistic signals."),
        ("Checked portfolio", lucide("<path d='M3 7h18v13H3z'/><path d='M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2'/>"), "Matched insights against demo holdings exposure."),
        ("Generated confidence", lucide("<path d='M12 2l7 4v6c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6l7-4z'/>"), "Computed deterministic confidence from tool outputs."),
    ]
    body = "".join(
        [f"<div class='reason-step'><span class='icon-wrap icon-red'>{icon}</span><div><b>{title}</b><div class='kicker'>{desc}</div></div></div>" for title, icon, desc in steps]
    )
    header = (
        "<div class='reason-header'>"
        "<div><div class='reason-title'>How this insight was generated</div>"
        "<div class='reason-sub'>Transparent reasoning pipeline</div></div>"
        "<span class='reason-conf-badge'>Confidence: 82%</span>"
        "</div>"
    )
    return f"<div class='card'>{header}{body}</div>"


def trace_timeline_html(trace: list, lang: str) -> str:
    if not trace:
        return reasoning_html(lang)

    # Map internal tokens to human-readable labels
    STEP_MAP = [
        ("receive_task",       "Request received",       "Your query was received and analysis started."),
        ("plan_created",       "Analysis plan created",  "Decided which tools to run and in what order."),
        ("document_processor", "Document extracted",     "Read and extracted text from the uploaded report."),
        ("metric_extractor",   "Key metrics identified", "Found revenue, profit, margin and growth figures."),
        ("sentiment_analyzer", "Sentiment analysed",     "Scanned for positive and negative signals."),
        ("portfolio_manager",  "Portfolio checked",      "Looked up your holdings to assess relevance."),
        ("alert_scanner",      "Alerts scanned",         "Checked for active alerts on your positions."),
        ("confidence_engine",  "Confidence calculated",  "Scored the reliability of this analysis."),
        ("ai_enhancer",        "AI summary generated",   "Created a plain-English summary of findings."),
        ("question_classifier","Question understood",    "Classified your question to find the best answer."),
        ("task_complete",      "Analysis complete",      "All steps finished. Results are ready."),
    ]

    def _status(raw):
        l = raw.lower()
        if "error:" in l: return "error"
        if "done:"  in l: return "done"
        return "done"

    COLOR = {"done": "#16A34A", "error": "#DC2626"}
    BG    = {"done": "#F0FDF4", "error": "#FEF2F2"}
    ICON  = {"done": "✅", "error": "❌"}
    LBL   = {"done": "Completed", "error": "Failed"}

    seen, steps = set(), []
    for raw in trace:
        low = raw.lower()
        for token, label, desc in STEP_MAP:
            if token in low and token not in seen:
                seen.add(token)
                st = _status(raw)
                steps.append((ICON[st], label, desc, st))
                break

    if not steps:
        return reasoning_html(lang)

    rows = []
    for i, (icon, label, desc, st) in enumerate(steps, 1):
        rows.append(
            f"<div style='display:flex;align-items:flex-start;gap:14px;"
            f"background:{BG[st]};border-radius:10px;padding:12px 16px;"
            f"margin-bottom:10px;border-left:4px solid {COLOR[st]}'>"
            f"<div style='font-size:1.1rem;line-height:1;padding-top:1px'>{icon}</div>"
            f"<div style='flex:1'>"
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:3px'>"
            f"<span style='font-size:.72rem;font-weight:700;color:#94A3B8'>Step {i}</span>"
            f"<span style='font-size:.68rem;font-weight:700;color:{COLOR[st]};"
            f"background:#fff;border:1px solid {COLOR[st]};border-radius:20px;padding:1px 8px'>{LBL[st]}</span>"
            f"</div>"
            f"<div style='font-size:.9rem;font-weight:700;color:#0F172A'>{label}</div>"
            f"<div style='font-size:.78rem;color:#64748B;margin-top:2px'>{desc}</div>"
            f"</div></div>"
        )

    header = (
        "<div style='display:flex;align-items:center;justify-content:space-between;"
        "margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #E2E8F0'>"
        "<div>"
        "<div style='font-size:1.05rem;font-weight:800;color:#0F172A'>How this insight was generated</div>"
        "<div style='font-size:.78rem;color:#64748B;margin-top:2px'>Transparent reasoning pipeline</div>"
        "</div>"
        "<span style='background:#DCFCE7;color:#166534;border-radius:999px;"
        "padding:5px 14px;font-size:.78rem;font-weight:700'>Confidence: 82%</span>"
        "</div>"
    )
    return f"<div class='card' style='margin-top:8px'>{header}{''.join(rows)}</div>"


def portfolio_html(lang: str) -> str:
    holdings = pm.get_all_holdings("demo_user")
    header = (
        "<div class='card' style='margin-bottom:10px'>"
        f"<h4>{tr(lang, 'portfolio')}</h4>"
        f"<div>{tr(lang, 'demo_user')}</div>"
        f"<div class='kicker'>{tr(lang, 'demo_note')}</div>"
        "</div>"
    )
    items = []
    for h in holdings:
        value = h["quantity"] * h["avg_price"]
        items.append(
            "<div class='card'>"
            f"<div style='display:flex;justify-content:space-between'><b>{h['stock']}</b><b>Rs. {value:,.0f}</b></div>"
            f"<div class='kicker'>{h['quantity']} shares @ Rs. {h['avg_price']:,.2f}</div>"
            "</div>"
        )
    return header + "".join(items)


def deterministic_summary(metrics: dict, sentiment: dict) -> str:
    m = (metrics or {}).get("metrics") or metrics or {}
    label = (sentiment or {}).get("sentiment", "neutral")
    rev = m.get("revenue", "N/A")
    profit = m.get("profit", "N/A")
    return (
        f"Fast-mode summary: sentiment is {label}. "
        f"Revenue is {rev} and net profit is {profit}, based on deterministic checks."
    )


def handle_analyze(pdf_file, stock_name: str, ai_mode: bool, lang: str):
    try:
        if pdf_file is None:
            return "<div class='card'>Please upload a PDF report first.</div>", "", "", "", "", reasoning_html(lang)

        result = agent.receive_task(
            "analyze_document",
            {
                "pdf_path": pdf_file.name,
                "stock_name": stock_name.strip().upper() if stock_name else None,
                "user_id": "demo_user",
                "ai_mode": bool(ai_mode),
            },
        )

        if not result.get("success"):
            warnings = " | ".join(result.get("warnings", ["Analysis failed."]))
            trace_html = trace_timeline_html(result.get("reasoning_trace") or [], lang)
            return f"<div class='card'>{warnings}</div>", "", "", "", "", trace_html

        conf_pct = int((result.get("confidence") or {}).get("percentage", 0))
        conf_html = (
            "<div class='card'>"
            "<h4>Confidence</h4>"
            f"<div class='val count' data-count='{conf_pct}'>0</div><div class='kicker'>%</div>"
            "</div>"
        )

        metrics = (result.get("metrics") or {}).get("metrics") or result.get("metrics") or {}
        metrics_rows = "".join([f"<div class='kicker'><b>{k.title()}</b>: {v}</div>" for k, v in metrics.items()])
        metrics_html = f"<div class='card'><h4>Metrics</h4>{metrics_rows}</div>"

        sentiment = result.get("sentiment") or {}
        sentiment_html = (
            "<div class='card'>"
            "<h4>Sentiment</h4>"
            f"<div class='kicker'>{sentiment.get('sentiment', 'neutral')} ({sentiment.get('score', 0):.2f})</div>"
            "</div>"
        )

        impact = result.get("portfolio_impact") or {}
        mode_text = tr(lang, "ai_enabled") if ai_mode else tr(lang, "ai_disabled")
        summary = result.get("summary") if ai_mode and result.get("summary") else deterministic_summary(metrics, sentiment)
        impact_html = (
            "<div class='card'>"
            "<h4>Portfolio Impact</h4>"
            f"<div class='kicker'>{impact.get('note', 'No impact details available.')}</div>"
            f"<div class='kicker' style='margin-top:8px'><b>{mode_text}</b></div>"
            f"<div class='kicker' style='margin-top:8px'>{summary}</div>"
            "</div>"
        )

        trace_html = trace_timeline_html(result.get("reasoning_trace") or [], lang)
        return "", conf_html, metrics_html, sentiment_html, impact_html, trace_html
    except Exception as exc:
        return f"<div class='card'>Something went wrong: {exc}</div>", "", "", "", "", reasoning_html(lang)


def handle_question(question: str, lang: str):
    try:
        if not question.strip():
            return _info_card("Please enter a question."), "", reasoning_html(lang)

        result = agent.receive_task("answer_question", {
            "question": question.strip(),
            "user_id": "demo_user",
        })

        # ── Query classification card ─────────────────────────────────────────
        cat = (result.get("question_class") or {}).get("category", "general_query").replace("_", " ").title()
        cat_colors = {
            "Portfolio Query": ("#DCFCE7", "#166534"),
            "Metric Query":    ("#DBEAFE", "#1D4ED8"),
            "Sentiment Query": ("#EDE9FE", "#6D28D9"),
            "Alert Query":     ("#FEF3C7", "#92400E"),
            "General Query":   ("#F1F5F9", "#475569"),
        }
        bg, fg = cat_colors.get(cat, ("#F1F5F9", "#475569"))
        cat_badge = (
            f"<span style='background:{bg};color:{fg};border-radius:999px;"
            f"padding:4px 14px;font-size:.8rem;font-weight:700'>{cat}</span>"
        )

        # ── Portfolio holdings ────────────────────────────────────────────────
        holdings = pm.get_all_holdings("demo_user")
        total_val = sum(h["quantity"] * h["avg_price"] for h in holdings)
        holding_rows = "".join(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:10px 0;border-bottom:1px solid #F1F5F9'>"
            f"<div>"
            f"<div style='font-size:.92rem;font-weight:700;color:#0F172A'>{h['stock']}</div>"
            f"<div style='font-size:.75rem;color:#64748B'>{h['quantity']} shares @ ₹{h['avg_price']:,.2f}</div>"
            f"</div>"
            f"<div style='text-align:right'>"
            f"<div style='font-size:.95rem;font-weight:800;color:#0F172A'>₹{h['quantity']*h['avg_price']:,.0f}</div>"
            f"<div style='font-size:.72rem;color:#16A34A;font-weight:600'>Demo</div>"
            f"</div>"
            f"</div>"
            for h in holdings
        )

        # ── Portfolio impact from agent ───────────────────────────────────────
        port = result.get("portfolio") or {}
        impact_msg = ""
        if isinstance(port, dict) and port.get("impact_message"):
            sig = port.get("sentiment_signal", "neutral")
            sig_color = {"positive": "#16A34A", "negative": "#DC2626"}.get(sig, "#64748B")
            impact_msg = (
                f"<div style='margin-top:14px;padding:12px 14px;background:#F8FAFC;"
                f"border-left:4px solid {sig_color};border-radius:0 8px 8px 0'>"
                f"<div style='font-size:.8rem;font-weight:700;color:{sig_color};margin-bottom:4px'>"
                f"Portfolio Signal: {sig.upper()}</div>"
                f"<div style='font-size:.85rem;color:#475569'>{port['impact_message']}</div>"
                f"</div>"
            )

        main_html = (
            f"<div class='card' style='margin-bottom:14px'>"
            f"<div style='font-size:.68rem;font-weight:700;color:#94A3B8;text-transform:uppercase;"
            f"letter-spacing:.08em;margin-bottom:8px'>Query Classification</div>"
            f"{cat_badge}"
            f"</div>"
            f"<div class='card'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px'>"
            f"<div style='font-size:.68rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.08em'>Demo Portfolio — Rahul Sharma</div>"
            f"<div style='font-size:.9rem;font-weight:800;color:#0F172A'>₹{total_val:,.0f}</div>"
            f"</div>"
            f"{holding_rows}"
            f"{impact_msg}"
            f"</div>"
        )

        # ── Confidence card ───────────────────────────────────────────────────
        conf_data = result.get("confidence") or {}
        conf_pct   = int(conf_data.get("percentage", 0))
        conf_label = conf_data.get("label", "Low")
        conf_color = "#16A34A" if conf_pct >= 80 else "#D97706" if conf_pct >= 50 else "#E11D2E"
        factors_html = "".join(
            f"<div style='display:flex;gap:8px;align-items:center;padding:5px 0;"
            f"border-bottom:1px solid #F1F5F9;font-size:.8rem;color:#475569'>"
            f"<span>{'✅' if '✅' in f else '⚠️' if '⚠️' in f else '❌'}</span><span>{f}</span></div>"
            for f in conf_data.get("factors", [])
        )
        conf_html = (
            f"<div class='card'>"
            f"<div style='display:flex;gap:20px;align-items:flex-start'>"
            f"<div style='text-align:center;min-width:80px'>"
            f"<div style='font-size:2.6rem;font-weight:900;color:{conf_color};line-height:1'>{conf_pct}%</div>"
            f"<div style='font-size:.75rem;color:#64748B;margin-top:3px'>{conf_label} Confidence</div>"
            f"<div style='height:5px;border-radius:5px;background:#F1F5F9;margin-top:8px;overflow:hidden'>"
            f"<div style='height:100%;width:{conf_pct}%;background:{conf_color};border-radius:5px'></div>"
            f"</div>"
            f"</div>"
            f"<div style='flex:1'>{factors_html}</div>"
            f"</div>"
            f"</div>"
        )

        trace_html = trace_timeline_html(result.get("reasoning_trace") or [], lang)
        return main_html, conf_html, trace_html

    except Exception as exc:
        return _info_card(f"Question failed: {exc}"), "", reasoning_html(lang)


def _info_card(msg: str) -> str:
    return (
        f"<div style='background:#FEF2F2;border:1px solid #FECACA;border-radius:12px;"
        f"padding:14px 18px;color:#B91C1C;font-size:.88rem'>{msg}</div>"
    )


def handle_demo_report(ai_mode: bool, lang: str):
    """Run analysis on the hardcoded TCS demo report text."""
    result = agent.receive_task("analyze_document", {
        "source":     DEMO_REPORT_CONTENT,
        "stock_name": "TCS",
        "user_id":    "demo_user",
        "ai_mode":    bool(ai_mode),
    })

    if not result.get("success"):
        warnings = " | ".join(result.get("warnings", ["Analysis failed."]))
        return _info_card(f"⚠️ {warnings}"), "", "", "", "", trace_timeline_html(result.get("reasoning_trace") or [], lang)

    conf_data  = result.get("confidence") or {}
    conf_pct   = int(conf_data.get("percentage", 0))
    conf_label = conf_data.get("label", "Low")
    conf_color = "#16A34A" if conf_pct >= 80 else "#D97706" if conf_pct >= 50 else "#E11D2E"
    factors_html = "".join(
        f"<div style='display:flex;gap:8px;align-items:center;padding:5px 0;"
        f"border-bottom:1px solid #F1F5F9;font-size:.8rem;color:#475569'>"
        f"<span>{'✅' if '✅' in f else '⚠️' if '⚠️' in f else '❌'}</span><span>{f}</span></div>"
        for f in conf_data.get("factors", [])
    )
    conf_html = (
        f"<div class='card'>"
        f"<div style='display:flex;gap:20px;align-items:flex-start'>"
        f"<div style='text-align:center;min-width:80px'>"
        f"<div style='font-size:2.6rem;font-weight:900;color:{conf_color};line-height:1'>{conf_pct}%</div>"
        f"<div style='font-size:.75rem;color:#64748B;margin-top:3px'>{conf_label} Confidence</div>"
        f"<div style='height:5px;border-radius:5px;background:#F1F5F9;margin-top:8px;overflow:hidden'>"
        f"<div style='height:100%;width:{conf_pct}%;background:{conf_color};border-radius:5px'></div>"
        f"</div></div>"
        f"<div style='flex:1'>{factors_html}</div>"
        f"</div></div>"
    )

    raw_metrics = (result.get("metrics") or {}).get("metrics") or result.get("metrics") or {}
    metric_labels = {"revenue": "Revenue (₹ Cr)", "profit": "Net Profit (₹ Cr)", "margin": "Margin %", "growth": "YoY Growth %"}
    chips = "".join(
        f"<div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;"
        f"padding:10px 16px;min-width:130px'>"
        f"<div style='font-size:.65rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em'>{metric_labels.get(k, k)}</div>"
        f"<div style='font-size:1.1rem;font-weight:800;color:#0F172A;margin-top:3px'>"
        f"{f'{v:,.2f}' if v is not None else '—'}</div>"
        f"</div>"
        for k, v in raw_metrics.items()
    )
    metrics_html = f"<div style='display:flex;flex-wrap:wrap;gap:10px;margin:4px 0'>{chips}</div>" if chips else ""

    sentiment = result.get("sentiment") or {}
    s_label = sentiment.get("sentiment", "neutral")
    s_score = sentiment.get("score", 0.5)
    s_pos   = sentiment.get("positive_signals", 0)
    s_neg   = sentiment.get("negative_signals", 0)
    s_cls   = {"positive": ("#F0FDF4", "#16A34A", "▲"), "negative": ("#FEF2F2", "#DC2626", "▼")}.get(s_label, ("#F8FAFC", "#64748B", "●"))
    sent_html = (
        f"<div class='card' style='display:flex;align-items:center;gap:16px;background:{s_cls[0]}'>"
        f"<span style='background:{s_cls[1]};color:#fff;border-radius:999px;"
        f"padding:5px 16px;font-size:.88rem;font-weight:700'>{s_cls[2]} {s_label.upper()}</span>"
        f"<div style='font-size:.8rem;color:#64748B'>Score <strong>{s_score:.2f}</strong> &nbsp;|&nbsp; "
        f"<span style='color:#16A34A;font-weight:600'>+{s_pos} positive</span> &nbsp; "
        f"<span style='color:#E11D2E;font-weight:600'>−{s_neg} negative</span></div>"
        f"</div>"
    )

    impact = result.get("portfolio_impact") or {}
    impact_msg = impact.get("note") or impact.get("impact_message", "No portfolio data.")
    impact_sig  = impact.get("sentiment_signal", "neutral")
    sig_color   = {"positive": "#16A34A", "negative": "#DC2626"}.get(impact_sig, "#64748B")
    impact_html = (
        f"<div class='card'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
        f"<span style='font-weight:700;font-size:.92rem;color:#0F172A'>Portfolio Impact</span>"
        f"<span style='background:#F1F5F9;color:{sig_color};border-radius:999px;"
        f"padding:3px 12px;font-size:.72rem;font-weight:700'>{impact_sig.upper()}</span>"
        f"</div>"
        f"<div style='font-size:.85rem;color:#475569;line-height:1.55'>{impact_msg}</div>"
        f"</div>"
    )

    summary = result.get("summary") or deterministic_summary(raw_metrics, sentiment)
    summary_html = (
        f"<div class='card'>"
        f"<div style='font-size:.68rem;font-weight:700;color:#94A3B8;text-transform:uppercase;"
        f"letter-spacing:.08em;margin-bottom:8px'>AI Summary</div>"
        f"<p style='font-size:.9rem;color:#0F172A;line-height:1.65'>{summary}</p>"
        f"</div>"
    )

    full_output = (
        f"<div style='margin-bottom:12px'>"
        f"<div style='font-size:.68rem;font-weight:700;color:#94A3B8;text-transform:uppercase;"
        f"letter-spacing:.08em;margin-bottom:8px'>Extracted Metrics</div>"
        f"{metrics_html}"
        f"</div>"
    )

    trace_html = trace_timeline_html(result.get("reasoning_trace") or [], lang)
    return "", conf_html, full_output, sent_html, impact_html + summary_html, trace_html


def handle_add_stock(stock: str, qty: str, price: str, lang: str):
    try:
        if not stock.strip():
            return "<div class='card'>Ticker is required.</div>", portfolio_html(lang)
        pm.add_holding("demo_user", stock.strip().upper(), int(qty), float(price))
        return "<div class='card'>Position updated successfully.</div>", portfolio_html(lang)
    except Exception as exc:
        return f"<div class='card'>Unable to update position: {exc}</div>", portfolio_html(lang)


def toggle_pages(to_dashboard: bool):
    if to_dashboard:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(visible=True), gr.update(visible=False)


def on_lang_change(lang_choice: str):
    lang = "hi" if lang_choice in ("Hindi", "हिंदी") else "en"
    return (
        lang,
        topbar_html(lang),
        landing_html(lang),
        markets_dashboard_html(lang),
        opportunities_rich_html(lang),
        news_carousel_html(lang),
        portfolio_html(lang),
        reasoning_html(lang),
        reasoning_html(lang),
        gr.update(placeholder=tr(lang, "ask_placeholder")),
        gr.update(value=tr(lang, "start_demo")),
        gr.update(value=tr(lang, "view_how")),
        gr.update(value=tr(lang, "back_home")),
        gr.update(value=tr(lang, "analyze")),
        gr.update(value=tr(lang, "ask")),
        gr.update(value=tr(lang, "add_position")),
        gr.update(value=tr(lang, "refresh_news")),
        gr.update(label=tr(lang, "ai_label")),
    )


def ai_status_html(ai_mode: bool, lang: str) -> str:
    status = tr(lang, "ai_enabled") if ai_mode else tr(lang, "ai_disabled")
    bg    = "#DCFCE7" if ai_mode else "#FEF3C7"
    color = "#166534" if ai_mode else "#92400E"
    border = "#BBF7D0" if ai_mode else "#FDE68A"
    icon  = "🟢" if ai_mode else "🟡"
    return (
        f"<span style='display:inline-flex;align-items:center;gap:5px;"
        f"background:{bg};border:1px solid {border};border-radius:999px;"
        f"padding:4px 12px;font-size:.72rem;font-weight:700;color:{color};"
        f"white-space:nowrap'>{icon} {status}</span>"
    )


def ai_status_from_lang_choice(ai_mode: bool, lang_choice: str) -> str:
    lang = "hi" if lang_choice in ("Hindi", "हिंदी") else "en"
    return ai_status_html(ai_mode, lang)


def launch_app(port: int = 7860, share: bool = False):
    with gr.Blocks(css=CSS, title="TradeIQ") as demo:
        lang_state = gr.State("en")

        with gr.Row(elem_classes=["control-strip"]):
            with gr.Column(elem_classes=["tb-col"], min_width=0):
                gr.HTML("<span class='tb-label'>🌐 Language</span>")
                lang_toggle = gr.Radio(
                    ["English", "हिंदी"], value="English",
                    label="", show_label=False,
                    elem_classes=["tb-radio"],
                )
            gr.HTML("<div class='tb-divider'></div>")
            with gr.Column(elem_classes=["tb-col"], min_width=0):
                gr.HTML("<span class='tb-label'>🤖 AI Mode</span>")
                ai_mode = gr.Checkbox(
                    value=True, label="ON",
                    elem_classes=["tb-check"],
                )
            gr.HTML("<div class='tb-divider'></div>")
            with gr.Column(elem_classes=["tb-col"], min_width=0):
                gr.HTML("<span class='ctrl-chip-green'>📄 Demo report ready</span>")
            gr.HTML("<div class='tb-divider'></div>")
            with gr.Column(elem_classes=["tb-col"], min_width=0):
                gr.HTML("<span class='ctrl-chip-user'>👤 Demo User: Rahul Sharma</span>")
            gr.HTML("<div class='tb-divider'></div>")
            with gr.Column(elem_classes=["tb-col"], min_width=0):
                ai_status = gr.HTML(ai_status_html(True, "en"))

        topbar = gr.HTML(topbar_html("en"))

        with gr.Group(visible=True, elem_classes=["fade-page"]) as landing_page:
            landing_block = gr.HTML(landing_html("en"))
            with gr.Row():
                start_demo_btn = gr.Button(tr("en", "start_demo"), elem_classes=["btn-light-cta"], elem_id="start-demo-btn")
                how_btn = gr.Button(tr("en", "view_how"), elem_classes=["btn-secondary"])

        with gr.Group(visible=False, elem_classes=["fade-page"]) as dashboard_page:
            with gr.Column(elem_classes=["dash-shell"]):
                with gr.Row():
                    back_btn = gr.Button(tr("en", "back_home"), elem_classes=["btn-secondary"])
                    quick_chip = gr.Button("Live Demo", elem_classes=["btn-chip"])

                gr.HTML(f"<div class='dash-title'>{tr('en', 'dashboard')}</div><div class='dash-sub'>Actionable market intelligence with explainable confidence.</div>")
                markets_ui = gr.HTML(markets_dashboard_html("en"))

                gr.HTML(f"<div class='section-title' style='margin-top:8px'>{tr('en', 'opportunities')}</div>")
                opportunities_ui = gr.HTML(opportunities_rich_html("en"))

                with gr.Row():
                    gr.HTML(f"<div class='section-title' style='margin:0;flex:1'>{tr('en', 'insights')}</div>")
                    refresh_news_btn = gr.Button(tr("en", "refresh_news"), elem_classes=["btn-secondary"], scale=0)
                news_ui = gr.HTML(news_carousel_html("en"))

                with gr.Tabs():
                    with gr.TabItem(tr("en", "analyze")):
                        with gr.Group(elem_classes=["analysis-grid"]):
                            with gr.Column(elem_classes=["input-panel"]):
                                gr.HTML("<div class='kicker'><b>Upload and analyze</b></div>")
                                use_demo_btn = gr.Button("📄 Use Demo TCS Report", elem_classes=["demo-report-btn"])
                                pdf_input = gr.File(label="PDF Report", file_types=[".pdf"])
                                stock_input = gr.Textbox(label="Stock Ticker (optional)", placeholder="e.g. TCS")
                                analyze_btn = gr.Button(tr("en", "analyze"), elem_classes=["btn-primary"])
                            with gr.Column(elem_classes=["output-grid"]):
                                analyze_err = gr.HTML()
                                analyze_conf = gr.HTML()
                                analyze_metrics = gr.HTML()
                                analyze_sent = gr.HTML()
                                analyze_impact = gr.HTML()
                        reason_block = gr.HTML(reasoning_html("en"))

                    with gr.TabItem(tr("en", "insights")):
                        question_input = gr.Textbox(placeholder=tr("en", "ask_placeholder"), label="")
                        ask_btn = gr.Button(tr("en", "ask"), elem_classes=["btn-primary"])
                        insight_main = gr.HTML()
                        insight_conf = gr.HTML()
                        insight_reason = gr.HTML(reasoning_html("en"))

                    with gr.TabItem(tr("en", "portfolio")):
                        portfolio_block = gr.HTML(portfolio_html("en"))
                        with gr.Row():
                            add_stock = gr.Textbox(label="Ticker", placeholder="TCS")
                            add_qty = gr.Textbox(label="Quantity", placeholder="10")
                            add_price = gr.Textbox(label="Avg Price", placeholder="3500")
                        add_btn = gr.Button(tr("en", "add_position"), elem_classes=["btn-primary"])
                        add_msg = gr.HTML()

        def refresh_landing(lang: str):
            return landing_html(lang)

        def noop_btn():
            return gr.update()

        def refresh_news_only(lang: str):
            return news_carousel_html(lang)

        refresh_news_btn.click(refresh_news_only, inputs=[lang_state], outputs=[news_ui])

        how_btn.click(
            fn=refresh_landing,
            inputs=[lang_state],
            outputs=[landing_block],
            js=HOW_SCROLL_JS,
        )
        start_demo_btn.click(lambda: toggle_pages(True), outputs=[landing_page, dashboard_page])
        back_btn.click(lambda: toggle_pages(False), outputs=[landing_page, dashboard_page])
        quick_chip.click(noop_btn, outputs=[quick_chip])
        ai_mode.change(fn=ai_status_html, inputs=[ai_mode, lang_state], outputs=[ai_status])

        if 'use_demo_btn' in locals():
            use_demo_btn.click(
                fn=handle_demo_report,
                inputs=[ai_mode, lang_state],
                outputs=[analyze_err, analyze_conf, analyze_metrics, analyze_sent, analyze_impact, reason_block],
            )
        analyze_btn.click(
            fn=handle_analyze,
            inputs=[pdf_input, stock_input, ai_mode, lang_state],
            outputs=[analyze_err, analyze_conf, analyze_metrics, analyze_sent, analyze_impact, reason_block],
        )

        ask_btn.click(
            fn=handle_question,
            inputs=[question_input, lang_state],
            outputs=[insight_main, insight_conf, insight_reason],
        )

        add_btn.click(
            fn=handle_add_stock,
            inputs=[add_stock, add_qty, add_price, lang_state],
            outputs=[add_msg, portfolio_block],
        )

        lang_toggle.change(
            fn=on_lang_change,
            inputs=[lang_toggle],
            outputs=[
                lang_state,
                topbar,
                landing_block,
                markets_ui,
                opportunities_ui,
                news_ui,
                portfolio_block,
                reason_block,
                insight_reason,
                question_input,
                start_demo_btn,
                how_btn,
                back_btn,
                analyze_btn,
                ask_btn,
                add_btn,
                refresh_news_btn,
                ai_mode,
            ],
        )
        lang_toggle.change(fn=ai_status_from_lang_choice, inputs=[ai_mode, lang_toggle], outputs=[ai_status])

        gr.HTML(
            """
<script>
(function(){
  function animateCounts(){
    document.querySelectorAll('.count[data-count]').forEach(function(el){
      const target = parseInt(el.getAttribute('data-count') || '0', 10);
      const duration = 650;
      const t0 = performance.now();
      function tick(t){
        const p = Math.min((t - t0)/duration, 1);
        el.textContent = Math.floor(target * p).toLocaleString();
        if(p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }
  const observer = new MutationObserver(animateCounts);
  observer.observe(document.body, { childList: true, subtree: true });
  setTimeout(animateCounts, 200);
})();
</script>
"""
        )

    demo.launch(server_port=port, share=share)


if __name__ == "__main__":
    launch_app()
