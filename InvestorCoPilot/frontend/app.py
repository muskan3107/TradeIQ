"""
InvestorCoPilot AI - upgraded Gradio frontend
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

DEMO_REPORT_CONTENT = """Company: TCS
Revenue increased to Rs. 2,10,000 Cr
Net profit grew by 12%
Strong deal pipeline
Risks: margin pressure, global slowdown
"""

I18N = {
    "en": {
        "app_name": "InvestorCoPilot AI",
        "hero_title": "InvestorCoPilot AI",
        "hero_sub": "AI that thinks like an investor, not just predicts",
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
    {"index": "NIFTY 50", "value": 22147, "change": 0.43},
    {"index": "SENSEX", "value": 73088, "change": 0.38},
    {"index": "BANK NIFTY", "value": 47312, "change": -0.12},
    {"index": "NIFTY IT", "value": 35640, "change": 1.21},
]

TOP_PICKS = [
    {"stock": "TCS", "signal": "BUY", "conf": 87, "reason": "Strong earnings momentum"},
    {"stock": "INFOSYS", "signal": "BUY", "conf": 81, "reason": "Healthy deal pipeline"},
    {"stock": "RELIANCE", "signal": "HOLD", "conf": 72, "reason": "Balanced risk-reward"},
    {"stock": "HDFCBANK", "signal": "HOLD", "conf": 68, "reason": "Watch margin pressure"},
]

CSS = """
:root {
  --primary: #E11D2E;
  --bg: #F5F5F5;
  --text: #0F172A;
  --muted: #64748B;
  --card: #FFFFFF;
  --good: #16A34A;
  --warn: #D97706;
}
* { box-sizing: border-box; }
body, .gradio-container {
  background: linear-gradient(180deg, #fff1f2 0%, #ffe4e6 45%, #fff1f2 100%) !important;
  font-family: Inter, Segoe UI, sans-serif !important;
}
.gradio-container {
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 auto !important;
  padding: 0 8px 20px !important;
}
footer { display: none !important; }
.main, .wrap { max-width: 100% !important; padding: 0 !important; }
.control-strip {
  background: #fff;
  border: 1px solid #fecdd3;
  border-radius: 14px;
  padding: 8px 10px;
  box-shadow: 0 8px 20px rgba(225, 29, 46, .08);
  margin-bottom: 10px;
}
.control-strip .wrap,
.control-strip .block {
  background: transparent !important;
  box-shadow: none !important;
}
.control-label {
  font-size: .72rem;
  color: #64748B;
  font-weight: 700;
  margin-bottom: 4px;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes floatY {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.fade-page {
  animation: fadeUp .35s ease;
}

.topbar {
  background: linear-gradient(120deg, #ffffff, #ffe4e6);
  border-bottom: 1px solid #fecdd3;
  border-radius: 0 0 14px 14px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  box-shadow: 0 6px 18px rgba(2, 8, 23, .06);
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand {
  font-size: 1.05rem;
  font-weight: 900;
  color: var(--primary);
}
.demo-meta {
  font-size: .75rem;
  color: #64748B;
  font-weight: 600;
}
.pill {
  font-size: .72rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  background: #fee2e2;
  color: #991b1b;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 18px;
  background: linear-gradient(145deg, #fff7f7, #fecdd3);
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 10px 24px rgba(2, 8, 23, .08);
  min-height: 290px;
}
.hero h1 {
  margin: 0 0 8px;
  font-size: 2.3rem;
  color: var(--text);
}
.hero p {
  margin: 6px 0;
  color: #475569;
}

.float-area { position: relative; min-height: 240px; }
.float-card {
  position: absolute;
  width: 210px;
  border-radius: 14px;
  padding: 14px;
  background: #fff;
  box-shadow: 0 10px 26px rgba(2, 8, 23, .14);
  animation: floatY 4s ease-in-out infinite;
}
.float-card:nth-child(1) { top: 0; left: 0; }
.float-card:nth-child(2) { top: 70px; left: 75px; animation-delay: .8s; }
.float-card:nth-child(3) { top: 140px; left: 18px; animation-delay: 1.6s; }

.section {
  margin-top: 22px;
}
.section-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 8px;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.flow {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}

.card {
  background: linear-gradient(180deg, #ffffff 0%, #fff7f7 100%);
  border-radius: 14px;
  padding: 14px;
  border: 1px solid #fee2e2;
  box-shadow: 0 8px 20px rgba(225, 29, 46, .10);
  transition: transform .2s, box-shadow .2s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(2, 8, 23, .12);
}
.dash-shell {
  background: linear-gradient(180deg, #fff, #fff5f5);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #fecdd3;
  box-shadow: 0 12px 28px rgba(225, 29, 46, .10);
}
.dash-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 8px;
}
.dash-sub {
  font-size: .85rem;
  color: #64748B;
  margin: 0 0 14px;
}

.icon-wrap {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  flex-shrink: 0;
}
.icon-red { background: #fee2e2; color: #b91c1c; }
.icon-blue { background: #dbeafe; color: #1d4ed8; }
.icon-green { background: #dcfce7; color: #166534; }
.icon-amber { background: #fef3c7; color: #92400e; }

.icon {
  width: 18px;
  height: 18px;
}

.badge {
  display: inline-block;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: .72rem;
  font-weight: 700;
}
.badge-buy { background: #dcfce7; color: #166534; }
.badge-hold { background: #fef3c7; color: #92400e; }

.kicker {
  font-size: .74rem;
  color: var(--muted);
}
.val {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--primary);
}

.reason-step {
  display: flex;
  gap: 10px;
  align-items: center;
  background: #f8fafc;
  border-left: 3px solid var(--primary);
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 8px;
}

.btn-primary {
  background: var(--primary) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  transition: transform .2s ease, background .2s ease !important;
}
.btn-primary:hover {
  background: #be123c !important;
  transform: scale(1.03) !important;
}
.btn-secondary {
  background: #fff !important;
  color: var(--primary) !important;
  border: 1.5px solid var(--primary) !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  transition: transform .2s ease !important;
}
.btn-secondary:hover {
  transform: scale(1.03) !important;
}
.btn-light-cta {
  background: #fff !important;
  color: #B91C1C !important;
  border: 1.5px solid #fecaca !important;
  border-radius: 10px !important;
  font-weight: 800 !important;
  transition: transform .2s ease, box-shadow .2s ease !important;
}
.btn-light-cta:hover {
  transform: scale(1.03) !important;
  box-shadow: 0 10px 20px rgba(225, 29, 46, .18) !important;
}
.btn-chip {
  border-radius: 999px !important;
  border: 1px solid #fecaca !important;
  background: #fff1f2 !important;
  color: #be123c !important;
  font-weight: 700 !important;
}

/* Better Gradio tabs look */
.tabs {
  background: transparent !important;
}
.tabs button {
  border: 1.5px solid #e2e8f0 !important;
  border-radius: 999px !important;
  padding: 8px 16px !important;
  font-weight: 700 !important;
  background: #fff !important;
  color: #475569 !important;
  transition: all .2s ease !important;
}
.tabs button:hover {
  border-color: #fda4af !important;
  color: #be123c !important;
}
.tabs button[aria-selected="true"] {
  background: #E11D2E !important;
  color: #fff !important;
  border-color: #E11D2E !important;
  box-shadow: 0 8px 18px rgba(225, 29, 46, .28) !important;
}
.how-focus {
  outline: 3px solid #E11D2E !important;
  box-shadow: 0 0 0 8px rgba(225, 29, 46, .18) !important;
  border-radius: 14px;
  transition: all .25s ease;
}

/* ET-style app strip */
.et-app-bar {
  background: #E11D2E;
  color: #fff;
  border-radius: 14px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  box-shadow: 0 10px 28px rgba(225, 29, 46, .35);
}
.et-app-bar .et-title {
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: -0.02em;
}
.et-app-bar .et-sub {
  font-size: .72rem;
  opacity: .9;
  font-weight: 600;
}
.live-dot {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.live-dot::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fff;
  animation: pulseDot 1.2s ease-in-out infinite;
}
@keyframes pulseDot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: .35; transform: scale(.85); }
}

/* News carousel */
.news-section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 8px 0 10px;
}
.news-section-head .big {
  font-size: 1.05rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: .04em;
}
.news-scroll {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
  scroll-snap-type: x mandatory;
}
.news-card {
  min-width: 280px;
  max-width: 320px;
  flex-shrink: 0;
  scroll-snap-align: start;
  background: #fff;
  border-radius: 14px;
  padding: 12px 14px;
  border: 1px solid #fecdd3;
  box-shadow: 0 8px 22px rgba(225, 29, 46, .08);
}
.news-card .live-tag {
  display: inline-block;
  font-size: .62rem;
  font-weight: 800;
  color: #E11D2E;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}
.news-card .headline {
  font-size: .95rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.35;
  margin: 0 0 8px;
}
.news-card .src {
  font-size: .68rem;
  color: #64748b;
  font-weight: 600;
}
.news-card a {
  font-size: .72rem;
  font-weight: 700;
  color: #E11D2E;
  text-decoration: none;
}

/* Index row + sparkline */
.index-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.index-card {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #fecdd3;
  padding: 10px 12px;
  box-shadow: 0 6px 18px rgba(225, 29, 46, .07);
}
.index-card .nm {
  font-size: .68rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: .05em;
}
.index-card .pv {
  font-size: 1.35rem;
  font-weight: 900;
  color: #0f172a;
  margin: 2px 0;
}
.index-card .ch {
  font-size: .78rem;
  font-weight: 800;
}

.pick-rich {
  display: grid;
  grid-template-columns: 1fr 120px;
  gap: 12px;
  align-items: stretch;
}
.pick-rich .main {
  min-width: 0;
}
.pick-rich .side {
  background: linear-gradient(180deg, #ecfeff, #f0f9ff);
  border-radius: 10px;
  padding: 8px 10px;
  border: 1px solid #bae6fd;
  text-align: center;
}
.pick-rich .side .lbl {
  font-size: .62rem;
  color: #0369a1;
  font-weight: 700;
  text-transform: uppercase;
}
.pick-rich .side .big {
  font-size: 1.15rem;
  font-weight: 900;
  color: #0f172a;
}
.sentiment-bar {
  display: flex;
  height: 8px;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 8px;
}
.sentiment-bar .seg-sell { background: #E11D2E; }
.sentiment-bar .seg-hold { background: #fbbf24; }
.sentiment-bar .seg-buy { background: #16a34a; }

.breadth-wrap {
  margin-top: 12px;
  background: #fff;
  border-radius: 12px;
  padding: 10px 12px;
  border: 1px solid #fecdd3;
}
.breadth-wrap .lbl {
  font-size: .72rem;
  font-weight: 800;
  color: #475569;
  margin-bottom: 6px;
}
.breadth-bar {
  display: flex;
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
}
.breadth-bar .adv { background: #16a34a; }
.breadth-bar .dec { background: #E11D2E; }
.breadth-meta {
  display: flex;
  justify-content: space-between;
  font-size: .68rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 600;
}

.analysis-grid {
  display: grid;
  grid-template-columns: minmax(280px, 360px) 1fr;
  gap: 12px;
}
.input-panel {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
}
.output-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

/* Cleaner file drop area */
.gradio-container .file-preview,
.gradio-container .file-wrap,
.gradio-container .file-dropzone {
  border-radius: 10px !important;
}

@media (max-width: 980px) {
  .hero { grid-template-columns: 1fr; }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .flow { grid-template-columns: repeat(2, 1fr); }
  .analysis-grid { grid-template-columns: 1fr; }
  .index-grid { grid-template-columns: repeat(2, 1fr); }
  .pick-rich { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .grid-4, .grid-2, .flow, .index-grid { grid-template-columns: 1fr; }
  .float-area { min-height: 0; }
  .float-card {
    position: relative;
    width: 100%;
    top: auto;
    left: auto;
    margin-bottom: 8px;
    animation: none;
  }
  .topbar { flex-direction: column; align-items: flex-start; gap: 8px; }
  .topbar-right { width: 100%; justify-content: space-between; }
  .output-grid { grid-template-columns: 1fr; }
  .control-strip { padding: 8px; }
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
    for row in rows:
        title = escape(row.get("title", ""))
        src = escape(str(row.get("source", "")))
        link = escape(str(row.get("link", "#")))
        cards.append(
            "<div class='news-card'>"
            f"<span class='live-tag'>{escape(tr(lang, 'live_strip'))} · MARKET</span>"
            f"<p class='headline'>{title}</p>"
            f"<div class='src'>{src}</div>"
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
    <div class='card' style='text-align:center;background:linear-gradient(130deg,#1f2937,#E11D2E);color:#fff;'>
      <h3 style='margin:6px 0 12px'>{tr(lang, 'cta')}</h3>
      <div class='kicker' style='color:#fff'>Live demo with transparent confidence and reasoning.</div>
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
    return f"<div class='card'><h4>{tr(lang, 'reason_title')}</h4>{body}</div>"


def trace_timeline_html(trace: list[str], lang: str) -> str:
    if not trace:
        return reasoning_html(lang)
    rows = []
    info_icon = lucide("<circle cx='12' cy='12' r='9'/><path d='M12 8v4'/><path d='M12 16h.01'/>")
    for i, line in enumerate(trace, 1):
        pretty = escape(line)
        rows.append(
            "<div class='reason-step'>"
            f"<span class='icon-wrap icon-blue'>{info_icon}</span>"
            f"<div><b>Step {i}</b><div class='kicker'>{pretty}</div></div>"
            "</div>"
        )
    return f"<div class='card'><h4>{tr(lang, 'trace_title')}</h4>{''.join(rows)}</div>"


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
            return "<div class='card'>Please enter a question.</div>", "", reasoning_html(lang)

        result = agent.receive_task("answer_question", {"question": question.strip(), "user_id": "demo_user"})
        cat = (result.get("question_class") or {}).get("category", "general_query").replace("_", " ").title()
        conf = int((result.get("confidence") or {}).get("percentage", 0))
        main_html = f"<div class='card'><h4>Query Category</h4><div class='kicker'>{cat}</div></div>"
        conf_html = f"<div class='card'><h4>Confidence</h4><div class='val count' data-count='{conf}'>0</div><div class='kicker'>%</div></div>"
        trace_html = trace_timeline_html(result.get("reasoning_trace") or [], lang)
        return main_html, conf_html, trace_html
    except Exception as exc:
        return f"<div class='card'>Question failed: {exc}</div>", "", reasoning_html(lang)


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
    lang = "hi" if lang_choice == "Hindi" else "en"
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
    bg = "#dcfce7" if ai_mode else "#fef3c7"
    color = "#166534" if ai_mode else "#92400e"
    return f"<div class='card' style='padding:10px 12px;background:{bg};color:{color}'><b>{status}</b></div>"


def ai_status_from_lang_choice(ai_mode: bool, lang_choice: str) -> str:
    lang = "hi" if lang_choice == "Hindi" else "en"
    return ai_status_html(ai_mode, lang)


def launch_app(port: int = 7860, share: bool = False):
    with gr.Blocks(css=CSS, title="InvestorCoPilot AI") as demo:
        lang_state = gr.State("en")

        with gr.Row(elem_classes=["control-strip"]):
            with gr.Column(scale=2):
                gr.HTML(f"<div class='control-label'>{tr('en', 'lang')}</div>")
                lang_toggle = gr.Radio(["English", "Hindi"], value="English", label="", show_label=False)
            with gr.Column(scale=3):
                gr.HTML(f"<div class='control-label'>{tr('en', 'ai_label')}</div>")
                ai_mode = gr.Checkbox(value=True, label="", show_label=False)
            generate_demo_pdf()
            with gr.Column(scale=4):
                demo_ready = gr.HTML("<div class='card' style='padding:10px 12px'><div class='kicker'><b>Demo report ready</b> - You can upload it in Analyze tab.</div></div>")
            with gr.Column(scale=3):
                ai_status = gr.HTML(ai_status_html(True, "en"))

        topbar = gr.HTML(topbar_html("en"))

        with gr.Group(visible=True, elem_classes=["fade-page"]) as landing_page:
            landing_block = gr.HTML(landing_html("en"))
            with gr.Row():
                start_demo_btn = gr.Button(tr("en", "start_demo"), elem_classes=["btn-light-cta"])
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
