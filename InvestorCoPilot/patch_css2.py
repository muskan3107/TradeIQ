"""Replace CSS block with polished design system."""
with open('frontend/app.py', encoding='utf-8') as f:
    src = f.read()

css_start = src.find('CSS = """')
css_end   = src.find('"""', css_start + 8) + 3
assert css_start > 0 and css_end > css_start, "CSS block not found"
print(f"Replacing CSS block [{css_start}:{css_end}]")

NEW_CSS = r'''CSS = """
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
  padding: 0 24px;
  margin: 0 -24px 0;
}
.control-strip .wrap,
.control-strip .block,
.control-strip .gr-form { background: transparent !important; box-shadow: none !important; border: none !important; }
.control-strip label { font-size: .72rem !important; font-weight: 700 !important; color: var(--muted) !important; }
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
'''

src = src[:css_start] + NEW_CSS + src[css_end:]
with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(src)
print("CSS replaced successfully. New file length:", len(src))
